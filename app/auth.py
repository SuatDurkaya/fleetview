from datetime import datetime, timedelta, timezone
from fastapi import Header, HTTPException
from passlib.context import CryptContext
import jwt

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"])

def verify_password(plain_password: str) -> bool:
    return pwd_context.verify(plain_password, settings.admin_password_hash)

def create_access_token() -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=12)
    payload = {"sub": settings.admin_username, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def verify_token(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Geçersiz token formatı")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token süresi dolmuş, tekrar giriş yap")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Geçersiz token")