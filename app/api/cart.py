from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Cart, Product
from app.schemas import CartItemCreate, CartResponse, CartItemResponse
from app.auth import get_current_user
from typing import List
from decimal import Decimal

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/items")
def add_to_cart(item: CartItemCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if product exists
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if item already exists in cart
    cart_item = db.query(Cart).filter(
        Cart.user_id == current_user.id,
        Cart.product_id == item.product_id
    ).first()
    
    if cart_item:
        # Update quantity
        cart_item.quantity = item.quantity
    else:
        # Create new cart item
        cart_item = Cart(
            user_id=current_user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)
    
    db.commit()
    return {"message": "Item added to cart"}

@router.delete("/items/{product_id}")
def remove_from_cart(product_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Find cart item
    cart_item = db.query(Cart).filter(
        Cart.user_id == current_user.id,
        Cart.product_id == product_id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart"
        )
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

@router.get("/", response_model=CartResponse)
def get_cart(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Get all cart items for the user
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    
    if not cart_items:
        return CartResponse(items=[], total_amount=Decimal("0.00"))
    
    items_response = []
    total_amount = Decimal("0.00")
    
    for cart_item in cart_items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        
        if product:
            item_total = product.price * cart_item.quantity
            total_amount += item_total
            
            items_response.append(CartItemResponse(
                product_id=product.id,
                product_name=product.name,
                product_price=product.price,
                quantity=cart_item.quantity,
                total_price=item_total
            ))
    
    return CartResponse(items=items_response, total_amount=total_amount)