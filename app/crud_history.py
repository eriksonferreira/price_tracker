# crud.py
from typing import List
from sqlalchemy.orm import Session
from exceptions import HistoryInfoAlreadyExistError, HistoryNotFoundError
from models import History
from schemas import CreateAndUpdateHistory
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
# Function to get list of product info
def get_all_historys(session: Session, limit: int, offset: int, product_id: Optional[int] = None, store_id: Optional[int] = None) -> List[History]:
    query = session.query(History)

    if product_id:
        query = query.filter(History.product_id == product_id)
    if store_id:
        query = query.filter(History.store_id == store_id)

    historys = query.offset(offset).limit(limit).all()

    # Convertendo o valor epoch para datetime
    for history in historys:
        if history.date:  # Certifique-se de que há um valor antes de converter
            history.date = datetime.fromtimestamp(history.date)

    return historys


# Function to  get info of a particular history
def get_history_info_by_id(session: Session, _id: int) -> History:
    history_info = session.query(History).get(_id)

    if history_info is None:
        raise HistoryNotFoundError

    return history_info


# Function to add a new history info to the database
def create_history(session: Session, history_info: CreateAndUpdateHistory) -> History:
    history_details = session.query(History).filter(
            History.product_id == history_info.product_id,
            History.store_id == history_info.store_id,
            History.price == history_info.price,
            History.price_credit == history_info.price_credit,
            History.sku == history_info.sku
        ).order_by(desc(History.id)).first()
    
    if history_details is not None:
        raise HistoryInfoAlreadyExistError

    new_history_info = History(**history_info.dict())
    session.add(new_history_info)
    session.commit()
    session.refresh(new_history_info)
    return new_history_info


# Function to update details of the history
def update_history_info(session: Session, _id: int, info_update: CreateAndUpdateHistory) -> History:
    history_info = get_history_info_by_id(session, _id)

    if history_info is None:
        raise HistoryNotFoundError

    history_info.product_id = info_update.product_id
    history_info.store_id = info_update.store_id
    history_info.price = info_update.price
    history_info.price_credit = info_update.price_credit
    history_info.url = info_update.url
    history_info.date = info_update.date

    
    session.commit()
    session.refresh(history_info)

    return history_info


# Function to delete a history info from the db
def delete_history_info(session: Session, _id: int):
    history_info = get_history_info_by_id(session, _id)

    if history_info is None:
        raise HistoryNotFoundError

    session.delete(history_info)
    session.commit()

    return
