# crud.py
from typing import List
from sqlalchemy.orm import Session, joinedload
from exceptions import ProductInfoInfoAlreadyExistError, ProductInfoNotFoundError
from models import ProductInfo, Prices
from schemas import CreateAndUpdateProduct


# Function to get list of product info
def get_all_products(session: Session, limit: int, offset: int) -> List[ProductInfo]:
    return session.query(ProductInfo).options(
        joinedload(ProductInfo.prices).joinedload(Prices.store),
        joinedload(ProductInfo.prices).joinedload(Prices.all_time_low_history)
    ).offset(offset).limit(limit).all()


# Function to  get info of a particular product
def get_product_info_by_id(session: Session, _id: int) -> ProductInfo:
    product_info = session.query(ProductInfo).get(_id)
    

    if product_info is None:
        raise ProductInfoNotFoundError()
    
    return product_info


# Function to add a new product info to the database
def create_product(session: Session, product_info: CreateAndUpdateProduct) -> ProductInfo:
    product_details = session.query(ProductInfo).filter(ProductInfo.model == product_info.model,
                                                        ProductInfo.manufacturer == product_info.manufacturer).first()
    if product_details is not None:
        prod_details = {
        'id': product_details.id,
        'type': product_details.type,
        'manufacturer': product_details.manufacturer,
        'model': product_details.model,
        'memory': product_details.memory,
        'memory_type': product_details.memory_type,
        'sku': product_details.sku
        }
        raise ProductInfoInfoAlreadyExistError( "Product Info Already Exists", prod_details)

    new_product_info = ProductInfo(**product_info.dict())
    session.add(new_product_info)
    session.commit()
    session.refresh(new_product_info)
    return new_product_info


# Function to update details of the product
def update_product_info(session: Session, _id: int, info_update: CreateAndUpdateProduct) -> ProductInfo:
    product_info = get_product_info_by_id(session, _id)

    if product_info is None:
        raise ProductInfoNotFoundError

    product_info.type = info_update.type
    product_info.manufacturer = info_update.manufacturer
    product_info.model = info_update.model
    product_info.memory = info_update.memory
    product_info.memory_type = info_update.memory_type
    product_info.sku = info_update.sku

    session.commit()
    session.refresh(product_info)

    return product_info


# Function to delete a product info from the db
def delete_product_info(session: Session, _id: int):
    product_info = get_product_info_by_id(session, _id)

    if product_info is None:
        raise ProductInfoNotFoundError

    session.delete(product_info)
    session.commit()

    return
