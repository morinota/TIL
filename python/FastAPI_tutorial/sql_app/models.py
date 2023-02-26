from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import OrmBaseClass


class User(OrmBaseClass):
    __tablename__ = "users"

    # create model attributes(fields) = RDB columns
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # create relationships(このtableに関連する他のtableからの値を含む magic attributes)
    items = relationship("Item", back_populates="owner")


class Item(OrmBaseClass):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
