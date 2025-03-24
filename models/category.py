from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    products = relationship("Product", back_populates="category")