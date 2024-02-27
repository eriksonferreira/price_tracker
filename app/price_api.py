# api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from crud_prices import get_all_prices, create_price, get_price_info_by_id, update_price_info, delete_price_info
from database import get_db
from exceptions import PricesException
from schemas import Price, CreateAndUpdatePrice, PaginatedPrice, PriceWithDetails

router = APIRouter()


# Example of Class based view
@cbv(router)
class Prices:
    session: Session = Depends(get_db)

    # API to get the list of price info
    @router.get("/prices", response_model=PaginatedPrice, tags=["price"])
    def list_prices(self, limit: int = 10, offset: int = 0):

        prices_list = get_all_prices(self.session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": prices_list}

        return response

    # API endpoint to add a price info to the database
    @router.post("/prices", tags=["price"])
    def add_price(self, price_info: CreateAndUpdatePrice):

        try:
            price_info = create_price(self.session, price_info)
            return price_info
        except PricesException as cie:
            raise HTTPException(**cie.__dict__)


# API endpoint to get info of a particular price
@router.get("/prices/{price_id}", response_model=PriceWithDetails, tags=["price"])
def get_price_info(price_id: int, session: Session = Depends(get_db)):

    try:
        price_info = get_price_info_by_id(session, price_id)
        return price_info
    except PricesException as cie:
        raise HTTPException(**cie.__dict__)


# API to update a existing price info
@router.put("/prices/{price_id}", response_model=Price, tags=["price"])
def update_price(price_id: int, new_info: CreateAndUpdatePrice, session: Session = Depends(get_db)):

    try:
        price_info = update_price_info(session, price_id, new_info)
        return price_info
    except PricesException as cie:
        raise HTTPException(**cie.__dict__)


# API to delete a price info from the data base
@router.delete("/prices/{price_id}", tags=["price"])
def delete_price(price_id: int, session: Session = Depends(get_db)):

    try:
        return delete_price_info(session, price_id)
    except PricesException as cie:
        raise HTTPException(**cie.__dict__)
