from pydantic import BaseModel, Field


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password_hash: str


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password_hash: str


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: str
    status: str = Field(max_length=50)


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    order_date: str
    status: str


class Products(BaseModel):
    id: int
    name: str = Field(max_length=32)
    description: str = Field(max_length=128)
    price: int


class ProductsIn(BaseModel):
    name: str = Field(max_length=32)
    description: str = Field(max_length=128)
    price: int