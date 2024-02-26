# crud.py
from typing import List
from sqlalchemy.orm import Session
from exceptions import StoreInfoAlreadyExistError, StoreNotFoundError
from models import Store
from schemas import CreateAndUpdateProduct


# Function to get list of product info
def get_all_stores(session: Session, limit: int, offset: int) -> List[Store]:
    return session.query(Store).offset(offset).limit(limit).all()


# Function to  get info of a particular store
def get_store_info_by_id(session: Session, _id: int) -> Store:
    store_info = session.query(Store).get(_id)

    if store_info is None:
        raise StoreNotFoundError

    return store_info


# Function to add a new store info to the database
def create_store(session: Session, store_info: CreateAndUpdateProduct) -> Store:
    store_details = session.query(Store).filter(Store.name == store_info.name).first()
    if store_details is not None:
        raise StoreInfoAlreadyExistError

    new_store_info = Store(**store_info.dict())
    session.add(new_store_info)
    session.commit()
    session.refresh(new_store_info)
    return new_store_info


# Function to update details of the store
def update_store_info(session: Session, _id: int, info_update: CreateAndUpdateProduct) -> Store:
    store_info = get_store_info_by_id(session, _id)

    if store_info is None:
        raise StoreNotFoundError

    store_info.name = info_update.name
    store_info.base_url = info_update.base_url
    store_info.logo = info_update.logo
    
    session.commit()
    session.refresh(store_info)

    return store_info


# Function to delete a store info from the db
def delete_store_info(session: Session, _id: int):
    store_info = get_store_info_by_id(session, _id)

    if store_info is None:
        raise StoreNotFoundError

    session.delete(store_info)
    session.commit()

    return
