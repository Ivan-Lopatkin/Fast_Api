import random
from datetime import datetime, timedelta
from typing import Type
import smtplib as smtp
import jwt
from bcrypt import hashpw, gensalt, checkpw
from datetime import timezone
from dotenv import load_dotenv
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_session
from src.sellers.models import Seller


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'



def get_password_hash(password: str, salt: str | bytes) -> bytes:
    password = password.encode('utf-8')
    if isinstance(salt, str):
        return hashpw(password, salt.encode('utf-8'))
    if isinstance(salt, bytes):
        return hashpw(password, salt)
    raise TypeError("Salt must be a string or bytes")


def verify_password(password: str, email: str | None = None, session: Session | None = None) -> bool:
    if not session:
        session = next(get_session())
    user = None
    if email:
        user: Type[Seller] | None = session.query(Seller).filter(Seller.e_mail == email).first()
    if not user:
        return False
    print(user.password, password)
    return user.password == password


def get_access_token(username: str, role: str = None) -> str:
    payload = {
        'sub': username,
        'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        'iat': datetime.utcnow(),
        'role': role
    }
    return jwt.encode(payload, SECRET_KEY, ALGORITHM, headers={'alg': 'HS256', 'typ': 'JWT_access'})



def get_refresh_token(username: str) -> str:
    payload = {
        'sub': username,
        'exp': datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        'iat': datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, ALGORITHM, headers={'alg': 'HS256', 'typ': 'JWT_refresh'})


def update_tokens(token: str) -> dict:
    username = jwt.decode(token, SECRET_KEY, ALGORITHM)['sub']
    print(username)
    access_token = get_access_token(username)
    refresh_token = get_refresh_token(username)
    return {'access_token': access_token, 'refresh_token': refresh_token}


def validate_access_token(token: str) -> bool:

    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],
                   options={'verify_signature': True, 'verify_exp': True})
        return True

    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail='Expired token') from e

    except jwt.InvalidSignatureError as e:
        raise HTTPException(status_code=401, detail='Invalid signature') from e
    



def verify_code(server_code: str, user_code: str) -> bool:
    return server_code == user_code