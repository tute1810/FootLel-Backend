from fastapi import FastAPI
from database.database import engine, Base
import models.user
from routers import users

# Crea las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FootLel API", version="0.1.0")

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido al backend modular de FootLel!"}
