import enum
from sqlalchemy import Column, Integer, DECIMAL, Text, String, func, ForeignKey, DateTime, Enum

from sqlalchemy.orm import relationship
from src.utils.db import DBModel


class OrderStatus(str, enum.Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED="cancelled"
class DeliveryZone(str, enum.Enum):
    DHAKA = "dhaka"
    OUTSIDE_DHAKA = "outside_dhaka"

class Order(DBModel):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('mango_products.id', ondelete="CASCADE"), nullable=False)
    quantity = Column(DECIMAL(10, 2), nullable=False)
    
    total_price = Column(DECIMAL(10, 2), nullable=False)
    delivery_zone = Column(String(20), nullable=False)
  
    delivery_charge=Column(DECIMAL(10,2),nullable=False)
    final_price=Column(DECIMAL(10,2),nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    full_name=Column(String(100),nullable=False)
    email=Column(String(50),nullable=False)
    phone_number=Column(String(20),nullable=False)
    city=Column(String(50),nullable=False)
    postal_code=Column(String(20),nullable=False)
    address=Column(Text,nullable=False)
    note=Column(Text,nullable=True)

    

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

   
    user = relationship("UserModel", back_populates="orders")
    product = relationship("MangoProduct", back_populates="orders")

   

   

  










   

 