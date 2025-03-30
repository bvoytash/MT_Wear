from sqlalchemy import Column, Integer, ForeignKey, Float, String
from database import Base
from sqlalchemy.orm import relationship


class BagItem(Base):
    __tablename__ = "bag_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False) 
    product_id = Column(Integer, nullable=False, index=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)
    size =Column(String, nullable=True)
    total_price = Column(Float)

    order = relationship("Order", back_populates="bag_items")

    def __repr__(self):
        return f"<BagItem - (product_id={self.product_id}, quantity={self.quantity})>"
