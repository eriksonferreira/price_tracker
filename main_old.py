from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import app.products_api as products_api
import app.store_api as store_api
import app.history_api as history_api
import app.price_api as price_api


tags_metadata = [
    {
        "name": "products",
        "description": "Operations with products.",
    },
    {
        "name": "store",
        "description": "Manage stores.",
    },
    {
        "name": "history",
        "description": "Manage hitory.",
    },
    {
        "name": "price",
        "description": "Manage prices.",
    },
]


# Initialize the app
app = FastAPI(openapi_tags=tags_metadata)
allowed_origins = [
    "http://localhost:3000",
    "https://price-tracker-frontend.rj.r.appspot.com",
    "https://tracker.ferreirasolutions.com.br"  # Add more origins as needed
]

# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(products_api.router)
app.include_router(store_api.router)
app.include_router(history_api.router)
app.include_router(price_api.router)

# GET operation at route '/'
@app.get('/')
def health_check():
    return {"message": "Everything seems alright.."}
