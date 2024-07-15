from sqlalchemy import Column, Integer, String, Float
from ..dependencies.database import Base

class Sandwich(Base):
    __tablename__ = "sandwiches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)  # Specify length for String
    description = Column(String(255), index=True)  # Specify length for String
    price = Column(Float)

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)  # Specify length for String
    quantity = Column(Integer)

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    sandwich_id = Column(Integer)
    resource_id = Column(Integer)
    quantity = Column(Integer)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), index=True)  # Specify length for String
    date = Column(String(255), index=True)  # Specify length for String

class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer)
    sandwich_id = Column(Integer)
    quantity = Column(Integer)
