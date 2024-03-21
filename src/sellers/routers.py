from typing import Union

from fastapi import APIRouter, Depends, Request
from fastapi.responses import ORJSONResponse, Response
from sqlalchemy.orm import Session
from starlette import status
from database import get_session
from src.books.models import Book
from src.sellers.schemas import SellerOut, SellerIn, SellerUpdate, Seller
from src.sellers.models import Seller as SellerModel
from database import get_session
from src.auth.utils import validate_access_token

router = APIRouter(
    tags=['Sellers'])



@router.post('/seller', response_model=SellerOut, status_code=201)
async def create_seller(seller: SellerIn = Depends(SellerIn)):
    session: Session = next(get_session())
    seller_model = SellerModel(
        first_name=seller.first_name,
        last_name=seller.last_name,
        e_mail=seller.e_mail,
        password=seller.password
    )
    session.add(seller_model)
    session.flush()
    seller = SellerOut(**seller_model.__dict__)
    session.commit()
    session.close()

    return seller


@router.get('/seller', response_model=list[SellerOut])
async def get_all_sellers():
    session: Session = next(get_session())
    sellers = session.query(SellerModel).all()
    session.close()
    return sellers


@router.get('/seller/{seller_id}', response_model=Union[SellerOut, dict])
async def get_seller(seller_id: int):
    session: Session = next(get_session())
    seller = session.query(SellerModel).filter(SellerModel.id == seller_id).first()
    if not seller:
        return {'status': 'fail',
                'details': 'seller not found'}
    session.close()
    seller = Seller(**seller.__dict__)

    return seller


@router.put('/seller/{seller_id}', response_model=Union[SellerOut, dict])
async def update_seller(seller_id: int, seller: SellerUpdate = Depends(SellerUpdate)):
    session: Session = next(get_session())
    seller_bd = session.query(SellerModel).filter(SellerModel.id == seller.id).first()
    if not seller_bd:
        return {'status': 'fail',
                'details': 'seller not found'}
    if seller.first_name:
        seller_bd.first_name = seller.first_name
    if seller.last_name:
        seller_bd.last_name = seller.last_name
    if seller.e_mail:
        seller_bd.e_mail = seller.e_mail
    session.add(seller_bd)
    session.commit()
    session.close()
    seller = Seller(**seller_bd.__dict__)
    return seller



@router.delete('/seller/{seller_id}', response_model=dict)
async def delete_seller(request: Request, seller_id: int):
    token = request.cookies.get('access_token')
    try:
        validate_access_token(token)
    except:
        return {'status': 'fail',
                'details': 'access token expired'}
    session: Session = next(get_session())
    id = session.query(SellerModel.id).filter(SellerModel.id == seller_id).first()
    if not id:
        return {'status': 'fail',
                'details': 'seller not found'}
    seller = session.query(SellerModel).filter(SellerModel.id == seller_id).first()
    for book in session.query(Book).filter(Book.seller_id == seller_id).all():
        session.delete(book)
    session.delete(seller)
    session.commit()
    return {'ok': True}
