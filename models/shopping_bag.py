from sqlalchemy import Column, Integer, ForeignKey, Float, String
from database import Base
from sqlalchemy.orm import relationship

class ShoppingBag(Base):
    __tablename__ = "shopping_bags"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="shopping_bag")
    items = relationship("BagItem", back_populates="shopping_bag", cascade="all, delete-orphan")

    #TODO USER MODEL shopping_bag = relationship("ShoppingBag", back_populates="user", uselist=False)


class BagItem(Base):
    __tablename__ = "bag_items"

    id = Column(Integer, primary_key=True, index=True)
    bag_id = Column(Integer, ForeignKey("shopping_bags.id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False) 
    total_price = Column(Float)

    shopping_bag = relationship("ShoppingBag", back_populates="items")

    def __repr__(self):
        return f"<BagItem - (product_id={self.product_id}, quantity={self.quantity})>"
