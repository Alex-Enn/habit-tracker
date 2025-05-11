from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import timedelta

# Импорты из ваших модулей
from . import crud, models, schemas, auth
from .database import SessionLocal, engine

# Инициализация приложения
app = FastAPI(
    title="Habit Tracker API",
    description="API для трекера привычек",
    version="0.1.0",
    swagger_ui_parameters={
        "docExpansion": "none",
        "operationsSorter": "method"
    }
)

# Создание таблиц БД
models.Base.metadata.create_all(bind=engine)

# Настройка аутентификации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинт для регистрации
@app.post("/register/", response_model=schemas.Token)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    user = crud.create_user(db, user)
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Эндпоинт для входа
@app.post("/login/", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Получение текущего пользователя
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

# Защищенный эндпоинт
@app.get("/users/me/", response_model=schemas.User)
async def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user

# Работа с привычками
@app.post("/habits/", response_model=schemas.HabitResponse)
def create_habit(
    habit: schemas.HabitCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_user_habit(db, habit, current_user.id)

@app.get("/habits/", response_model=list[schemas.HabitResponse])
def read_habits(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_user_habits(db, current_user.id)

# Статистика
@app.get("/habits/{habit_id}/stats")
def get_stats(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    streak = crud.get_habit_streak(db, habit_id)
    return {"streak": streak, "habit_id": habit_id}