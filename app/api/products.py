from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from app.schemas import ProductResponse, ProductCreate
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products