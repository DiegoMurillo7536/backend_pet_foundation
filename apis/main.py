from fastapi import FastAPI
import logging
from apis.foundations import foundation_app
from apis.donations import donation_app
# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Aplicación principal
app = FastAPI(
    title="Pet Foundation API",
    description="API para gestión de fundaciones de mascotas",
    version="1.0.0"
)

# Incluir los routers
app.include_router(foundation_app, prefix="/api/v1")
app.include_router(donation_app, prefix="/api/v1")