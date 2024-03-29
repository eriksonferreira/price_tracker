# schemas.py
from pydantic import BaseModel, validator   
# from models import ProductInfo
from typing import Optional, List
from datetime import datetime

# --------- Store ---------
class CreateAndUpdateStore(BaseModel):
    name: str
    base_url: str
    logo: str
    update_min_time: Optional[int]
    update_max_time: Optional[int]


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
    sku: str
    price: float
    price_credit: float
    url: str
    date: int

class History(BaseModel):
    id: int
    product_id: int
    store_id: int
    sku: str
    price: float
    price_credit: float
    url: str
    date: datetime  # Certifique-se de que o tipo esperado é datetime

    @validator('date', pre=True)
    def convert_epoch_to_datetime(cls, value):
        # A conversão só ocorre se o valor for um int (ou seja, um timestamp epoch)
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        return value

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
    all_time_low: Optional[int] = None
    actual_price_id: Optional[int] = None


class Price(CreateAndUpdatePrice):
    id: int
    actual_price_id_info: Optional[History] = None
    all_time_low_history: Optional[History] = None
    class Config:
        orm_mode = True


class PaginatedPrice(BaseModel):
    limit: int
    offset: int
    data: List[Price]

    
# --------- Products ---------
# TO support creation and update APIs
class CreateAndUpdateProduct(BaseModel):
    type: str
    manufacturer: str
    model: str
    memory: str
    memory_type: str
    sku: str
    image: Optional[str]


# TO support list and get APIs
class Product(CreateAndUpdateProduct):
    id: int
    prices: Optional[List[Price]] = None  # Novo campo para preços relacionados
    class Config:
        orm_mode = True


class StoreDetail(BaseModel):
    id: int
    name: str
    base_url: str
    logo: str
    update_min_time: Optional[int]
    update_max_time: Optional[int]

    class Config:
        orm_mode = True

class HistoryDetail(BaseModel):
    id: int
    price: float
    price_credit: float
    url: str
    date: datetime

    class Config:
        orm_mode = True


class StoreWithDetails(Store):
    prices: Optional[List[Price]] = None
    history: Optional[List[History]] = None

    class Config:
        orm_mode = True


class PriceWithDetails(Price):
    store: Optional[StoreDetail] = None
    actual_price_id_info: Optional[History] = None
    all_time_low_history: Optional[HistoryDetail] = None

    class Config:
        orm_mode = True

class ProductWithPrices(Product):
    prices: Optional[List[PriceWithDetails]] = None

    class Config:
        orm_mode = True

# To support list Products API
class PaginatedProductInfo(BaseModel):
    limit: int
    offset: int
    data: List[ProductWithPrices]  # Atualize para usar ProductWithPrices

    class Config:
        orm_mode = True