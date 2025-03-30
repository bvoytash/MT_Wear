from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean, Enum as SQLEnum
from database import Base
from sqlalchemy.orm import relationship
from datetime import timezone, datetime
from enum import Enum
from models.shopping_bag import BagItem


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

    created = Column(DateTime, default=datetime.now(timezone.utc))
    order_number = Column(String, unique=True, nullable=True)
    

    is_paid = Column(Boolean, default=False)
    status = Column(SQLEnum(OrderStatus), nullable=False)

    user_profile = relationship("UserProfile", back_populates="orders")
    bag_items = relationship("BagItem", back_populates="order", cascade="all, delete-orphan")


    def generate_order_number(self):
        date_part = self.created.strftime("%Y%m%d")  # Format: YYYYMMDD
        self.order_number = f"ORD-{date_part}-{self.id}"