from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from schemas import Base


class Coffee(Base):
    __tablename__ = "coffee"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    category = Column(String(200))
    description = Column(String(200))
    reviews = Column(ARRAY(String))

    users = relationship("User", back_populates="coffee")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "reviews": self.reviews,
        }


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    has_sale = Column(Boolean, default=False)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey("coffee.id"))

    coffee = relationship("Coffee", back_populates="users")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "has_sale": self.has_sale,
            "address": self.address,
            "coffee": self.coffee.to_dict() if self.coffee else None,
        }