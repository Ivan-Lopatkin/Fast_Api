from fastapi import APIRouter, Request
from typing import Union
from fastapi.responses import ORJSONResponse, Response
from starlette import status
from database import get_session
from src.auth.utils import validate_access_token
from src.books.models import Book
from src.books.schemas import ReturnedBook, IncomingBook, ReturnedAllBooks
from src.sellers.models import Seller

router = APIRouter(
    tags=['Books'])

@router.post("/books/")  # Прописываем модель ответа
async def create_book(request: Request, book: IncomingBook):  # прописываем модель валидирующую входные данные
    token = request.cookies.get('access_token')
    try:
        validate_access_token(token)
    except:
        return {'status': 'fail',
                'details': 'access token expired'}
    # TODO запись в БД
    session = next(get_session())
    seller = session.query(Seller).filter(Seller.id == book.seller_id).first()
    item = Book(
        title=book.title,
        author=book.author,
        year=book.year,
        count_pages=book.count_pages,
        seller_id=book.seller_id,
    )
    seller.books.append(item)
    session.add(item)
    session.add(seller)
    session.commit()
    session.close()

    # return new_book  # Так можно просто вернуть объект
    return book  # Возвращаем объект в формате Json с нужным нам статус-кодом, обработанный нужным сериализатором.


# Ручка, возвращающая все книги
@router.get("/books/", response_model=ReturnedAllBooks)
async def get_all_books():
    session = next(get_session())
    books = session.query(Book).all()

    return {"books": books}


# Ручка для получения книги по ее ИД
@router.get("/books/{book_id}")
async def get_book(book_id: int):
    session = next(get_session())
    book = session.query(Book).filter(Book.id == book_id).first()
    if not book:
        return {"status": "fail", "message": "Book not found"}
    returned_book = ReturnedBook(**book.__dict__)

    return returned_book

# Ручка для удаления книги
@router.delete("/books/{book_id}")
async def delete_book(book_id: int):
    session = next(get_session())
    book = session.get(Book, book_id)
    if not book:
        return {"status": "fail", "message": "Book not found"}
    session.delete(book)
    session.commit()
    return {"status": "ok"}


# Ручка для обновления данных о книге
@router.put("/books/{book_id}")
async def update_book(request: Request, book_id: int, book: ReturnedBook):
    token = request.cookies.get('access_token')
    try:
        validate_access_token(token)
    except:
        return {'status': 'fail',
                'details': 'access token expired'}
    session = next(get_session())
    book_bd = session.get(Book, book_id)
    if not book_bd:
        return {"status": "fail", "message": "Book not found"}
    if book.title:
        book_bd.title = book.title
    if book.author:
        book_bd.author = book.author
    if book.year:
        book_bd.year = book.year
    if book.count_pages:
        book_bd.count_pages = book.count_pages
    if book.seller_id:
        book_bd.seller_id = book.seller_id
    session.add(book_bd)
    session.commit()
    return book