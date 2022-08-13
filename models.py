from sqlalchemy import Boolean,Float,Integer,String,Column
from database import Base

#Table Schema
class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float,unique=True, index=True)
    long = Column(Float,unique=True, index=True)
    location = Column(String,unique=True, index=True)