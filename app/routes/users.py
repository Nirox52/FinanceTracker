from fastapi import APIRouter, Request, Depends, Form
from app.database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})

@router.get("/list", response_class=HTMLResponse)
async def get_users_list(request: Request, db=Depends(get_db)):
    users = await db.fetch("SELECT id, name FROM users")
    return templates.TemplateResponse("partials/users_list.html", {"request": request, "users": users})

@router.get("/new", response_class=HTMLResponse)
async def show_user_form(request: Request):
    return templates.TemplateResponse("partials/user_form.html", {"request": request})

@router.post("/create", response_class=HTMLResponse)
async def create_user(request: Request, name: str = Form(...), db=Depends(get_db)):
    await db.execute("INSERT INTO users (name) VALUES ($1)", name)
    users = await db.fetch("SELECT id, name FROM users")
    return templates.TemplateResponse("partials/users_list.html", {"request": request, "users": users})

