from typing import Annotated

from fastapi import FastAPI, Response, status, Depends, Request
from src.sellers.routers import router as seller_router
from src.books.routers import router as books_router
from src.auth.router import router as auth_router


app = FastAPI()

app.include_router(books_router, prefix='/api/v1')
app.include_router(seller_router, prefix='/api/v1')
app.include_router(auth_router, prefix='/api/v1')