# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status
from random import randint

# IMPORT INTERNAL LIBRARIES #
from objects import user_register_credentials
from objects import user_login_credentials
from database import authentication
from database import user_management

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/auth/user-login")
def user_login(user_login_credentials: user_login_credentials.UserLoginCredentials):
    if authentication.is_user_name_available(user_login_credentials.user_name) == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error de login: nombre de usuario incorrecto")

    user_password = user_management.get_user_password_with_user_name(user_login_credentials.user_name)

    if user_password is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error de login: no se encontro el usuario")

    if user_password != user_login_credentials.user_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="error de login: contrasenia incorrecta")

    return { "result": "success" }

@router.post("/auth/user-register")
def user_register(user_register_credentials: user_register_credentials.UserRegisterCredentials):
    if authentication.is_user_name_available(user_register_credentials.user_name) == False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error al registrarse: ese nombre de usuario ya esta en uso")

    if authentication.is_user_email_available(user_register_credentials.user_email) == False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error al registrarse: ese email ya esta en uso")

    if authentication.register_new_user(user_register_credentials.user_name, user_register_credentials.user_email, user_register_credentials.user_password) == False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error al registrarse: no se pudo registrar el usuario, intente de vuelta")

    return { "result": "success" }

@router.post("/auth/guest-login")
def guest_login():
    guest_name: str = "guest_" + str(randint(1000, 9999))

    if authentication.is_user_name_available(guest_name) == False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error de modo invitado: ese nombre de usuario ya esta en uso, intente de vuelta")

    return { "result": "success", "guest_name": guest_name }