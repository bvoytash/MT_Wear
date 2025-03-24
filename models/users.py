from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password = Column(String(64))
    is_admin = Column(Boolean, default=False)

    profile = relationship("UserProfile", back_populates="user", uselist=False)

    def to_dict(self):
        return {
            "email": self.email,
            "is_admin": self.is_admin,
            "profile": self.profile.to_dict(),
        }


class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)
    city = Column(String(50), nullable=True)
    postal_code = Column(String(20), nullable=True)

    user = relationship("User", back_populates="profile", passive_deletes=True)

    def to_dict(self):
        return {
            "phone_number": self.phone_number,
            "address": self.address,
            "city": self.city,
            "postal_code": self.postal_code,
        }
