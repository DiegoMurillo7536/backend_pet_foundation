from fastapi import FastAPI
from apis.foundations import foundation_app
from apis.donations import donation_app
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Pet Foundation API",
    description="API para gestión de fundaciones de mascotas",
    version="1.0.0"
)

origin = [
    os.getenv("FRONTEND_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(foundation_app, prefix="/api/v1")
app.include_router(donation_app, prefix="/api/v1")
