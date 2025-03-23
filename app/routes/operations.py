from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.database import get_db
from datetime import datetime

router = APIRouter(prefix="/operations", tags=["operations"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def get_operations_page(request: Request):
    """Главная страница операций"""
    return templates.TemplateResponse("operations.html", {"request": request})

@router.get("/list", response_class=HTMLResponse)
async def get_latest_operations(request: Request, db=Depends(get_db)):
    """Получает 10 последних операций"""
    operations = await db.fetch("SELECT * FROM operations ORDER BY id DESC LIMIT 10")
    return templates.TemplateResponse("partials/operations_list.html", {"request": request, "operations": operations})

@router.get("/new", response_class=HTMLResponse)
async def show_operation_form(request: Request):
    """Возвращает HTML-форму для добавления операции"""
    return templates.TemplateResponse("partials/operation_form.html", {"request": request})

@router.post("/add", response_class=JSONResponse)
async def add_operation(request: Request, user_id: int = Form(...), type: str = Form(...), amount: float = Form(...), db=Depends(get_db)):
    """Добавляет новую финансовую операцию"""
    now = datetime.now()
    await db.execute(
        "INSERT INTO operations (user_id, type, amount, year, month) VALUES ($1, $2, $3, $4, $5)",
        user_id, type, amount, now.year, now.month
    )
    
    operations = await db.fetch("SELECT * FROM operations ORDER BY id DESC LIMIT 10")
    return templates.TemplateResponse("partials/operations_list.html", {"request": request, "operations": operations})

