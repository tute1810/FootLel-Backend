# IMPORT LIBRARIES #
import random

from fastapi import APIRouter

# IMPORT OBJECTS #
from objects import user_credentials
from objects import guest_credentials
from database import authentication

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/auth/user-login")
def login(user_credentials: user_credentials.UserCredentials):
    user_password = authentication.get_user_password_with_user_name(user_credentials.user_name)
    if user_password == None:
        return {"message": "Usuario inactivo o no encontrado"}
    if user_password == user_credentials.user_password:
        return {"message": "si"}
    else:
        return {"message": "Contraseña incorrecta"}
    
@router.post("/auth/user-register")
def register(user_credentials: user_credentials.UserCredentials):
    resultado_registro = str(authentication.register_new_user(user_credentials.user_name, user_credentials.user_email,user_credentials.user_password))
    if resultado_registro == "Usuario creado":
        return {"message": "si"}
    else: 
        return {"message": resultado_registro}
    
@router.post("/auth/guest-login")
def guest():
    guest_name = "Guest67_" + str(random.randint(1000, 9999)) 
    return {"guest_name": guest_name}
