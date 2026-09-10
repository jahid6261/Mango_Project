
from sqlalchemy import Column,Integer,String,Boolean,DateTime,Enum,func,ForeignKey
import enum
from src.utils.db import DBModel
from sqlalchemy.orm import relationship


class UserRole(enum.Enum):
    user='user'
    admin='admin'
    


class UserModel(DBModel):
    
    __tablename__ = 'users'
    id= Column(Integer,primary_key=True,index=True)
    
    first_name=Column(String,nullable=False)
    last_name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True,index=True)
    password=Column(String,nullable=False)
    number=Column(String(15),unique=True,index=True)
    address=Column(String(255),nullable=True)
    role=Column(Enum(UserRole),default=UserRole.user)
    is_active = Column(Boolean, default=False)
    activation_token = Column(String, nullable=True)
   
    created_at=Column(DateTime(timezone=True),server_default=func.now()) 
    updated_at=Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now())
    
    
    reviews = relationship("Review", back_populates="user")
    orders = relationship(
        "Order",
        back_populates="user"
    )
    reset_otps = relationship(
    "PasswordOTP",
    back_populates="user",
    cascade="all, delete-orphan"
)



class PasswordOTP(DBModel):

    __tablename__= "password_reset_otps"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),
                   nullable=False,index=True,)
    otp=Column(String(64),nullable=False)
    expires_at=Column(DateTime(timezone=True),nullable=False)
    is_used=Column(Boolean,default=False,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("UserModel", back_populates="reset_otps")
