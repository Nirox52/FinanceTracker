from fastapi import APIRouter, Request, Depends, Form
from app.database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.utils.jwt import create_jwt_token

router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})

@router.get("/list", response_class=HTMLResponse)
async def get_users_list(request: Request, db=Depends(get_db)):
    users = await db.fetch("SELECT id, name FROM users")
    for id,user in enumerate(users):
        users[id] = user['name']
    return templates.TemplateResponse("partials/users_list.html", {"request": request, "users": users})

@router.get("/new", response_class=HTMLResponse)
async def show_user_form(request: Request):
    return templates.TemplateResponse("partials/user_form.html", {"request": request})

@router.post("/create", response_class=JSONResponse)
async def create_user(request: Request, name: str = Form(...), db=Depends(get_db)):
    """Создаёт пользователя и возвращает JWT-токен."""
    user_id = await db.fetchval("INSERT INTO users (name) VALUES ($1) RETURNING id", name)
    token = create_jwt_token(user_id, name)
    
    return {"message": "User created", "user_id": user_id, "name": name, "token": token}

