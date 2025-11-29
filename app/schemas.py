from pydantic import BaseModel, EmailStr
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Product schemas
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: Decimal
    created_at: datetime

    class Config:
        from_attributes = True

# Cart schemas
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemResponse(BaseModel):
    product_id: int
    product_name: str
    product_price: Decimal
    quantity: int
    total_price: Decimal

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total_amount: Decimal

    class Config:
        from_attributes = True

# Order schemas
class OrderCreate(BaseModel):
    pass  # Empty for now, we'll use cart contents

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    product_price: Decimal
    quantity: int

    class Config:
        from_attributes = True

class OrderDetailResponse(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True

# Payment/Order status schemas
class OrderStatusUpdate(BaseModel):
    status: str