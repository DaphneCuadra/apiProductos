from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import productos
from fastapi.staticfiles import StaticFiles
# Crea UNA sola instancia de FastAPI con toda la configuración
app = FastAPI(
    title="API de gestión de productos",
    version="1.0.0",
    description="API para gestionar productos usando FastAPI y Oracle"
)

# Configuración CORS (debe venir ANTES de incluir los routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8100"], 
    allow_credentials=True, 
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
    allow_headers=["*"],   
    expose_headers=["*"],    
    max_age=3600
)

# Ruta de ejemplo
@app.get("/")
def read_root():
    return {"mensaje": "Hola desde FastAPI"}

# Incluir routers
app.include_router(productos.router)
app.mount("/static", StaticFiles(directory="static"), name="static")