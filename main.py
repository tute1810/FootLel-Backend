# IMPORT LIBRARIES #
from fastapi import FastAPI

# IMPORT ROUTERS #
from routers import user_management
from routers import authentication

# CREATE THE API #
app = FastAPI(title="FootLel_api", version="0.1.0")

# INCLUDE THE ENDPOINTS TO THE API #
app.include_router(user_management.router)
app.include_router(authentication.router)


from fastapi.middleware.cors import CORSMiddleware

# Esto le dice al backend "dejá pasar las peticiones que vengan de otros dominios"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ojo: En producción es mejor poner tu dominio exacto del frontend en vez de "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)