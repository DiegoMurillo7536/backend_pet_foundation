from fastapi import FastAPI
from apis.foundations import foundation_app
from apis.donations import donation_app

app = FastAPI(
    title="Pet Foundation API",
    description="API para gestión de fundaciones de mascotas",
    version="1.0.0"
)

app.include_router(foundation_app, prefix="/api/v1")
app.include_router(donation_app, prefix="/api/v1")
