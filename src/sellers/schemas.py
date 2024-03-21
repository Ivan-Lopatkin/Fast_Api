from pydantic import BaseModel


class SellerOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    e_mail: str


class SellerIn(BaseModel):
    first_name: str
    last_name: str
    e_mail: str
    password: str


class Seller(SellerIn):
    id: int = None


class SellerUpdate(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    e_mail: str | None = None

class SellerLogIn(BaseModel):
    e_mail: str
    password: str