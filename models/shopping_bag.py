from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime, Boolean
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

class ShoppingBag(Base):
    __tablename__ = "shopping_bags"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=True)
    items = relationship("BagItem", back_populates="shopping_bag", cascade="all, delete-orphan")
    order = relationship("Order", back_populates="shopping_bag")


class BagItem(Base):
    __tablename__ = "bag_items"

    id = Column(Integer, primary_key=True, index=True)
    bag_id = Column(Integer, ForeignKey("shopping_bags.id"), nullable=False, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)
    size =Column(String, nullable=True)
    total_price = Column(Float)

    shopping_bag = relationship("ShoppingBag", back_populates="items")

    def __repr__(self):
        return f"<BagItem - (product_id={self.product_id}, quantity={self.quantity})>"



class OrderStatus(Enum):
    PREPARING = "preparing"
    ACCEPTED = "accepted"
    SENT = "sent"
    CANCELED = "canceled"
    REJECTED = "rejected"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False)
    shopping_bag_id = Column(Integer, ForeignKey("shopping_bags.id", ondelete="CASCADE"), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    order_number = Column(String, unique=True, nullable=False)
    is_paid = Column(Column(Boolean, default=False))
    status = Column(Enum(OrderStatus), nullable=False)

    user_profile = relationship("UserProfile", back_populates="orders")
    shopping_bag = relationship("ShoppingBag", back_populates="order")
