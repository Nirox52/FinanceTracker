from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import home, users

app = FastAPI()

# Подключение папки со статикой
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Подключение маршрутов
app.include_router(home.router)
app.include_router(users.router)
