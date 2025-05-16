from fastapi import FastAPI
from app.routers import usuarios

app = FastAPI(
    title="API de gestión de productos",
    version="1.0.0",
    description="API para gestionar productos usando FastAPI y Oracle"
)

#Traeremos lo de las rutas(routers):
app.include_router(usuarios.router)