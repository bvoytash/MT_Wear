from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum


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
    is_paid = Column(Boolean, default=False)

    status = Column(Enum(OrderStatus), nullable=False)

    user_profile = relationship("UserProfile", back_populates="orders")
    shopping_bag = relationship("ShoppingBag", back_populates="order")


    # order_number = f"ORD-{new_shopping_bag.id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    #     new_order = Order(
    #     user_profile_id=user_profile_id,
    #     shopping_bag_id=new_shopping_bag.id,
    #     created=datetime.utcnow(),
    #     order_number=order_number,
    #     is_paid=False,
    #     status=OrderStatus.PREPARING
    # )
    
    # db.add(new_order)
    # db.commit()