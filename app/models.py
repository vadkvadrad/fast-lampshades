from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        CheckConstraint("price > 0", name="check_price_positive"),
    )


class Cart(Base):
    __tablename__ = "carts"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
    )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default='pending')  # 'pending', 'paid', 'cancelled'
    created_at = Column(TIMESTAMP, server_default=func.now())


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, nullable=False, primary_key=True)
    product_name = Column(String(255), nullable=False)  # snapshot at order time
    product_price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)