from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.database import get_db
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def home(request: Request,db=Depends(get_db)):
    now = datetime.now()
    query = "SELECT amount FROM operations WHERE year = $1 AND month = $2 AND type = 'income'"

    income_operations = await db.fetch(query, now.year, now.month)
    income_amounts = [float(op["amount"]) for op in income_operations]

    query = "SELECT amount FROM operations WHERE year = $1 AND month = $2 AND type = 'expense'"

    expense_operations = await db.fetch(query, now.year, now.month)
    expense_amounts = [float(op["amount"]) for op in expense_operations]


    print(income_amounts)  
    print(expense_amounts)

    income = sum(income_amounts)
    expense = sum(expense_amounts)
    balanse =  income - expense 

    print(balanse,income,expense)

    return templates.TemplateResponse("index.html", {"request": request,"balanse":balanse,"expense":expense,"income":income})

