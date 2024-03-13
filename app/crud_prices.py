# crud.py
from typing import List
from sqlalchemy.orm import Session, joinedload
from exceptions import PricesInfoAlreadyExistError, PricesNotFoundError
from models import Prices, History
from schemas import CreateAndUpdatePrice, Price
from telegram.app.services import message_send


# Function to get list of product info
def get_all_prices(session: Session, limit: int, offset: int) -> List[Prices]:
    return session.query(Prices).options(
        joinedload(Prices.actual_price_id_info)  # Correctly load the relationship
    ).offset(offset).limit(limit).all()



# Function to  get info of a particular price
def get_price_info_by_id(session: Session, _id: int) -> Prices:
    price_info = session.query(Prices).get(_id)

    if price_info is None:
        raise PricesNotFoundError

    return price_info


# Function to add a new price info to the database
def create_price(session: Session, price_info: CreateAndUpdatePrice) -> Prices:
    price_details = session.query(Prices).filter(Prices.product_id == price_info.product_id, 
                                                 Prices.store_id == price_info.store_id, 
                                                 Prices.actual_price == price_info.actual_price).first()
    if price_details is not None:
        raise PricesInfoAlreadyExistError

    new_price_info = Prices(**price_info.dict())
    session.add(new_price_info)
    session.commit()
    session.refresh(new_price_info)
    return new_price_info


# Function to update details of the price
def update_price_info(session: Session, _id: int, info_update: CreateAndUpdatePrice) -> Prices:
    price_info = get_price_info_by_id(session, _id)

    if price_info is None:
        raise PricesNotFoundError

    price_info.product_id = info_update.product_id
    price_info.store_id = info_update.store_id
    price_info.actual_price = info_update.actual_price
    price_info.actual_price_credit = info_update.actual_price_credit
    if info_update.all_time_low is not None:
        price_info.all_time_low = info_update.all_time_low
    
    session.commit()
    session.refresh(price_info)

    return price_info


# Function to delete a price info from the db
def delete_price_info(session: Session, _id: int):
    price_info = get_price_info_by_id(session, _id)

    if price_info is None:
        raise PricesNotFoundError

    session.delete(price_info)
    session.commit()

    return
