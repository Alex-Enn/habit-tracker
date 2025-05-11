# 🚀 Habit Tracker API

REST API для трекинга привычек с аутентификацией JWT, построенное на FastAPI и SQLAlchemy.

## 📦 Технологии
- **Python 3.11+**
- **FastAPI** (веб-фреймворк)
- **SQLAlchemy 2.0** (ORM)
- **PostgreSQL** (база данных)
- **JWT** (аутентификация)
- **Alembic** (миграции)
- **Pydantic v2** (валидация данных)

## 🛠️ Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/Alex-Enn/habit-tracker.git
cd habit-tracker
```
### 2. Настройка окружения
Создайте файл .env в корне проект
```ini
DATABASE_URL=postgresql://user:password@localhost:5432/habit_tracker
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
### 3. Установка зависимостей
Создайте файл .env в корне проект
```bash
pip install -r requirements.txt
```
### 4. Запуск сервера
```bash
uvicorn app.main:app --reload
```
API будет доступно на: http://localhost:8000

📚 Документация API
Swagger UI: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc

🧪 Тестирование
```bash
-m pytest tests/
```
