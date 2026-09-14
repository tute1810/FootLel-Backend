from fastapi import FastAPI
from endpoints import users

app = FastAPI(title="FootLel API", version="0.1.0")

app.include_router(users.router)

"""@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido al backend modular de FootLel!"}
"""
