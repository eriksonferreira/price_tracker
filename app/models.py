from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Float, DateTime
import sqlalchemy as sa
from database import Base
import enum


class ProductInfo(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    manufacturer = Column(String)
    model = Column(String)
    memory = Column(String)
    memory_type = Column(String)
    sku = Column(String)


class Store(Base):
    __tablename__ = "store"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    base_url = Column(String)
    logo = Column(String)


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, sa.ForeignKey(ProductInfo.id))
    store_id = Column(Integer, sa.ForeignKey(Store.id))
    price = Column(Float)
    url = Column(String)
    date = Column(DateTime)


class Prices(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, sa.ForeignKey(ProductInfo.id))
    store_id = Column(Integer, sa.ForeignKey(Store.id))
    actual_price = Column(Float)
    actual_price_credit = Column(Float)
    all_time_low = Column(Integer, sa.ForeignKey(History.id))

