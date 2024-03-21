import pydantic.fields
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class User_register(BaseModel):
    e_mail: str
    password: str
    

class User_login(BaseModel):
    username_or_email: str
    password: str
