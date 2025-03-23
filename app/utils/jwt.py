import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60  # Токен будет действителен 60 минут

def create_jwt_token(user_id: int, name: str) -> str:
    """Генерирует JWT-токен с user_id и name."""
    payload = {
        "sub": str(user_id),
        "name": name,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt_token(token: str) -> dict:
    """Декодирует JWT-токен и возвращает данные пользователя."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

