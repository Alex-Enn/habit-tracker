from pydantic import BaseModel
from datetime import date

# Схема для создания привычки
class HabitCreate(BaseModel):
    name: str

# Схема для отметки о выполнении
class HabitLogCreate(BaseModel):
    date: date
    status: str  # "done" или "skipped"

# Схема для возврата привычки (ответ API)
class HabitResponse(BaseModel):
    id: int
    name: str
    user_id: int

    class Config:
        from_attributes = True  # Ранее 'orm_mode = True' в Pydantic v1
        
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True