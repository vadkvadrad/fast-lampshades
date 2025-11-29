from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Cart, Product, Order, OrderItem
from app.schemas import OrderResponse, OrderDetailResponse
from app.auth import get_current_user
from typing import List
from decimal import Decimal

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
def create_order(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Get user's cart items
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Calculate total amount
    total_amount = Decimal("0.00")
    for cart_item in cart_items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if product:
            total_amount += product.price * cart_item.quantity
    
    # Create order
    order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status="pending"
    )
    db.add(order)
    db.flush()  # Get the order ID without committing
    
    # Create order items and copy product data
    for cart_item in cart_items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if product:
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                product_price=product.price,
                quantity=cart_item.quantity
            )
            db.add(order_item)
    
    # Clear user's cart
    db.query(Cart).filter(Cart.user_id == current_user.id).delete()
    
    db.commit()
    
    # Refresh to get the created order with ID
    db.refresh(order)
    return order

@router.post("/{order_id}/pay", response_model=OrderResponse)
def pay_order(order_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order cannot be paid"
        )
    
    # Mock payment - just update status
    order.status = "paid"
    db.commit()
    db.refresh(order)
    
    return order

@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(order_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending orders can be cancelled"
        )
    
    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/{order_id}", response_model=OrderDetailResponse)
def get_order(order_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Get order items
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    
    return OrderDetailResponse(
        id=order.id,
        user_id=order.user_id,
        total_amount=order.total_amount,
        status=order.status,
        created_at=order.created_at,
        items=order_items
    )

@router.get("/", response_model=List[OrderResponse])
def get_orders(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders