# api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from crud_store import get_all_stores, create_store, get_store_info_by_id, update_store_info, delete_store_info
from database import get_db
from exceptions import StoreException
from schemas import Store, CreateAndUpdateStore, PaginatedStore

router = APIRouter()


# Example of Class based view
@cbv(router)
class Stores:
    session: Session = Depends(get_db)

    # API to get the list of store info
    @router.get("/stores", response_model=PaginatedStore, tags=["store"])
    def list_stores(self, limit: int = 10, offset: int = 0):

        stores_list = get_all_stores(self.session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": stores_list}

        return response

    # API endpoint to add a store info to the database
    @router.post("/stores", tags=["store"])
    def add_store(self, store_info: CreateAndUpdateStore):

        try:
            store_info = create_store(self.session, store_info)
            return store_info
        except StoreException as cie:
            raise HTTPException(**cie.__dict__)


# API endpoint to get info of a particular store
@router.get("/stores/{store_id}", response_model=Store, tags=["store"])
def get_store_info(store_id: int, session: Session = Depends(get_db)):

    try:
        store_info = get_store_info_by_id(session, store_id)
        return store_info
    except StoreException as cie:
        raise HTTPException(**cie.__dict__)


# API to update a existing store info
@router.put("/stores/{store_id}", response_model=Store, tags=["store"])
def update_store(store_id: int, new_info: CreateAndUpdateStore, session: Session = Depends(get_db)):

    try:
        store_info = update_store_info(session, store_id, new_info)
        return store_info
    except StoreException as cie:
        raise HTTPException(**cie.__dict__)


# API to delete a store info from the data base
@router.delete("/stores/{store_id}", tags=["store"])
def delete_store(store_id: int, session: Session = Depends(get_db)):

    try:
        return delete_store_info(session, store_id)
    except StoreException as cie:
        raise HTTPException(**cie.__dict__)
