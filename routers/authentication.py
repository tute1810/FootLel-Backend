# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status
from random import randint

# IMPORT INTERNAL LIBRARIES #
from objects import user_info, user_credentials
from database import authentication, user_management
from security import jwt

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/auth/user-login")
def user_login(user_credentials: user_credentials.UserCredentials):
    user_name: str = user_credentials.user_name
    db_user_name_unused: bool | None = authentication.is_user_name_available(user_name)

    if db_user_name_unused is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error de login: error al buscar el nombre de usuario")
    elif db_user_name_unused is True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error de login: nombre de usuario incorrecto")

    db_user_password: str | None = user_management.get_user_password_with_user_name(user_name)

    if db_user_password is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error de login: error al buscar la contrasenia")

    user_password: str = user_credentials.user_password

    if user_password != db_user_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="error de login: contrasenia incorrecta")

    db_user_id: int | None = user_management.get_user_id_with_user_name(user_name)

    if db_user_id is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de login: error al buscar el id del usuario")

    access_token: str = jwt.get_access_token(db_user_id)

    return { "result": "success", "access_token": access_token }

@router.post("/auth/user-register")
def user_register(user_info: user_info.UserInfo):
    user_name: str = user_info.user_name

    if authentication.is_user_name_available(user_name) is False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error de registro: nombre de usuario en uso")

    user_email: str = user_info.user_email

    if authentication.is_user_email_available(user_email) is False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error de registro: email en uso")

    user_password: str = user_info.user_password

    if authentication.register_new_user(user_name, user_email, user_password) is False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de registro: error al registrar el usuario")

    return { "result": "success" }

@router.post("/auth/guest-login")
def guest_login():
    guest_name: str = "guest_" + str(randint(10000, 99999))
    db_user_name_unused: bool | None = authentication.is_user_name_available(guest_name)

    if db_user_name_unused is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de modo invitado: error al buscar el nombre de invitado")
    elif db_user_name_unused is False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error de modo invitado: nombre de invitado ya esta usado, intente de vuelta")
    
    if authentication.register_guest(guest_name) is False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de modo invitado: error al registrar el invitado")

    db_guest_id: int | None = user_management.get_user_id_with_user_name(guest_name)

    if db_guest_id is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de modo invitado: error al obtener el id de invitado")

    access_token: str = jwt.get_access_token(db_guest_id)

    return { "result": "success", "access_token": access_token }