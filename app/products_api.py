# api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from crud_products import get_all_products, create_product, get_product_info_by_id, update_product_info, delete_product_info
from database import get_db
from exceptions import ProductInfoException
from schemas import Product, CreateAndUpdateProduct, PaginatedProductInfo

router = APIRouter()


# Example of Class based view
@cbv(router)
class Products:
    session: Session = Depends(get_db)

    # API to get the list of product info
    @router.get("/products", response_model=PaginatedProductInfo, tags=["products"])
    def list_products(self, limit: int = 10, offset: int = 0):

        products_list = get_all_products(self.session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": products_list}

        return response

    # API endpoint to add a product info to the database
    @router.post("/products", tags=["products"])
    def add_product(self, product_info: CreateAndUpdateProduct):

        try:
            product_info = create_product(self.session, product_info)
            return product_info
        except ProductInfoException as cie:
            raise HTTPException(**cie.__dict__)


# API endpoint to get info of a particular product
@router.get("/products/{product_id}", response_model=Product, tags=["products"])
def get_product_info(product_id: int, session: Session = Depends(get_db)):

    try:
        product_info = get_product_info_by_id(session, product_id)
        return product_info
    except ProductInfoException as cie:
        raise HTTPException(**cie.__dict__)


# API to update a existing product info
@router.put("/products/{product_id}", response_model=Product, tags=["products"])
def update_product(product_id: int, new_info: CreateAndUpdateProduct, session: Session = Depends(get_db)):

    try:
        product_info = update_product_info(session, product_id, new_info)
        return product_info
    except ProductInfoException as cie:
        raise HTTPException(**cie.__dict__)


# API to delete a product info from the data base
@router.delete("/products/{product_id}", tags=["products"])
def delete_product(product_id: int, session: Session = Depends(get_db)):

    try:
        return delete_product_info(session, product_id)
    except ProductInfoException as cie:
        raise HTTPException(**cie.__dict__)
