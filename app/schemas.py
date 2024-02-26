# schemas.py
from pydantic import BaseModel
# from models import ProductInfo
from typing import Optional, List
from datetime import datetime

# --------- Products ---------
# TO support creation and update APIs
class CreateAndUpdateProduct(BaseModel):
    type: str
    manufacturer: str
    model: str
    memory: str
    memory_type: str
    sku: str


# TO support list and get APIs
class Product(CreateAndUpdateProduct):
    id: int
    class Config:
        orm_mode = True


# To support list Products API
class PaginatedProductInfo(BaseModel):
    limit: int
    offset: int
    data: List[Product]

# --------- Store ---------
class CreateAndUpdateStore(BaseModel):
    name: str
    base_url: str
    logo: str


class Store(CreateAndUpdateStore):
    id: int
    class Config:
        orm_mode = True


class PaginatedStore(BaseModel):
    limit: int
    offset: int
    data: List[Store]

# --------- History ---------
class CreateAndUpdateHistory(BaseModel):
    product_id: int
    store_id: int
    price: float
    url: str
    date: datetime

class History(CreateAndUpdateHistory):
    id: int
    class Config:
        orm_mode = True


class PaginatedHistory(BaseModel):
    limit: int
    offset: int
    data: List[History]

# --------- Prices ---------
    
class CreateAndUpdatePrice(BaseModel):
    product_id: int
    store_id: int
    actual_price: float
    actual_price_credit: float
    all_time_low: int


class Price(CreateAndUpdatePrice):
    id: int
    class Config:
        orm_mode = True


class PaginatedPrice(BaseModel):
    limit: int
    offset: int
    data: List[Price]