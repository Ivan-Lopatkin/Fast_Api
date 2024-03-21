import jwt
from bcrypt import gensalt
from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.orm import Session
import random
from src.sellers.models import Seller
from src.sellers.schemas import SellerLogIn
from src.auth.utils import get_password_hash, verify_password, get_access_token, get_refresh_token, verify_code
from database import get_session

router = APIRouter(
    tags=['Auth'],

)


    
@router.post('/token')
def login(request: Request, response: Response, user: SellerLogIn = Depends(SellerLogIn)):
    with next(get_session()) as session:
        if session.query(Seller).filter(Seller.e_mail == user.e_mail).first():
            if verify_password(user.password, email=user.e_mail, session=session):
                access_token = get_access_token(user.e_mail)
                refresh_token = get_refresh_token(user.e_mail)
                response.set_cookie('access_token', access_token, httponly=True, secure=True)
                response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True)
                return {'status': 'ok',
                        'details': {
                            'access_token': access_token,
                            'refresh_token': refresh_token
                            }
                        }
            return {'status': 'fail',
                    'details': 'wrong password'}
        return {'status': 'fail',
                'details': 'user not found'}



