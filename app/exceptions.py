# exceptions.py
class ProductInfoException(Exception):
     ...


class ProductInfoNotFoundError(ProductInfoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Product Info Not Found"


class ProductInfoInfoAlreadyExistError(ProductInfoException):
    def __init__(self, msg, product_details):
        self.status_code = 409
        self.detail = msg
        self.product_details = product_details
    
    def to_response(self):
        return {
            "status_code": self.status_code,
            "content": {
                "message": self.detail,
                "product_details": self.product_details
            }
        }


class StoreException(Exception):
    ...


class StoreNotFoundError(StoreException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Store Info Not Found"


class StoreInfoAlreadyExistError(StoreException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Store Info Already Exists"



class HistoryException(Exception):
    ...


class HistoryNotFoundError(HistoryException):
    def __init__(self):
        self.status_code = 404
        self.detail = "History Info Not Found"


class HistoryInfoAlreadyExistError(HistoryException):
    def __init__(self):
        self.status_code = 409
        self.detail = "History Info Already Exists"


class PricesException(Exception):
    ...


class PricesNotFoundError(PricesException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Prices Info Not Found"


class PricesInfoAlreadyExistError(PricesException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Prices Info Already Exists"