# api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from crud_history import get_all_historys, create_history, get_history_info_by_id, update_history_info, delete_history_info
from database import get_db
from exceptions import HistoryException
from schemas import History, CreateAndUpdateHistory, PaginatedHistory
from typing import List, Optional
from fastapi.responses import JSONResponse


router = APIRouter()


# Example of Class based view
@cbv(router)
class Products:
    session: Session = Depends(get_db)

    # API to get the list of history info
    @router.get("/historys", response_model=PaginatedHistory, tags=["history"])
    def list_historys(
        self,
        session: Session = Depends(get_db),  # Dependência para a sessão do SQLAlchemy
        limit: int = 10,
        offset: int = 0,
        product_id: Optional[int] = None,
        store_id: Optional[int] = None,):

        historys_list = get_all_historys(session, limit, offset, product_id, store_id)
        response = {"limit": limit, "offset": offset, "data": historys_list}

        return response

    # API endpoint to add a history info to the database
    @router.post("/historys", tags=["history"])
    def add_history(self, history_info: CreateAndUpdateHistory):

        try:
            history_info = create_history(self.session, history_info)
            return history_info
        except HistoryException as cie:
            raise HTTPException(**cie.__dict__)


# API endpoint to get info of a particular history
@router.get("/historys/{history_id}", response_model=History, tags=["history"])
def get_history_info(history_id: int, session: Session = Depends(get_db)):

    try:
        history_info = get_history_info_by_id(session, history_id)
        return history_info
    except HistoryException as cie:
        raise HTTPException(**cie.__dict__)


# API to update a existing history info
@router.put("/historys/{history_id}", response_model=History, tags=["history"])
def update_history(history_id: int, new_info: CreateAndUpdateHistory, session: Session = Depends(get_db)):

    try:
        history_info = update_history_info(session, history_id, new_info)
        return history_info
    except HistoryException as cie:
        raise HTTPException(**cie.__dict__)


# API to delete a history info from the data base
@router.delete("/historys/{history_id}", tags=["history"])
def delete_history(history_id: int, session: Session = Depends(get_db)):

    try:
        return delete_history_info(session, history_id)
    except HistoryException as cie:
        raise HTTPException(**cie.__dict__)
