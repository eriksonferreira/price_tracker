from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import products_api
import store_api
import history_api
import price_api
from telegram.app.api.v1.api import api_router
from telegram.app.config import settings
from fastapi.middleware.cors import CORSMiddleware

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
    {
        "name": "telegram",
        "description": "Send telegram messages.",
    },
]


# Initialize the app
app = FastAPI(openapi_tags=tags_metadata)

allowed_origins = [
    "http://localhost:3000",
    "https://price-tracker-frontend.rj.r.appspot.com/"  # Add more origins as needed
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
app.include_router(api_router, prefix="/telegram")

# GET operation at route '/'
@app.get('/')
def health_check():
    return {"message": "Everything seems alright.."}
