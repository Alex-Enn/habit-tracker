from sqlalchemy.orm import Session
from datetime import date, timedelta
from . import models, schemas, auth
from passlib.context import CryptContext

# Настройки для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str) -> models.User | None:
    """Получение пользователя по имени"""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Создание нового пользователя"""
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_habit(db: Session, habit_data: schemas.HabitCreate, user_id: int) -> models.Habit:
    """Создание новой привычки"""
    db_habit = models.Habit(**habit_data.dict(), user_id=user_id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

def get_user_habits(db: Session, user_id: int) -> list[models.Habit]:
    """Получение всех привычек пользователя"""
    return db.query(models.Habit).filter(models.Habit.user_id == user_id).all()

def add_habit_log(db: Session, habit_id: int, log_data: schemas.HabitLogCreate) -> models.HabitLog:
    """Добавление отметки о выполнении привычки"""
    db_log = models.HabitLog(**log_data.dict(), habit_id=habit_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_habit_streak(db: Session, habit_id: int) -> int:
    """Подсчет текущего стрика (дней подряд выполнения)"""
    logs = (
        db.query(models.HabitLog)
        .filter(
            models.HabitLog.habit_id == habit_id,
            models.HabitLog.status == "done"
        )
        .order_by(models.HabitLog.date.desc())
        .all()
    )
    
    streak = 0
    current_date = date.today()
    
    for log in logs:
        expected_date = current_date - timedelta(days=streak)
        if log.date == expected_date:
            streak += 1
        else:
            break
            
    return streak