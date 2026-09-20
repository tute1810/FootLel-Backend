# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter
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
        return { "result": "login error: user name incorrect" }

    user_password = user_management.get_user_password_with_user_name(user_login_credentials.user_name)

    if user_password is None:
        return { "result": "login error: user name was not found" }

    if user_password != user_login_credentials.user_password:
        return { "result": "login error: user password is incorrect" }

    return { "result": "success" }

@router.post("/auth/user-register")
def user_register(user_register_credentials: user_register_credentials.UserRegisterCredentials):
    if authentication.is_user_name_available(user_register_credentials.user_name) == False:
        return { "result": "register error: user name already in use" }

    if authentication.is_user_email_available(user_register_credentials.user_email) == False:
        return { "result": "register error: user email already in use" }

    if authentication.register_new_user(user_register_credentials.user_name, user_register_credentials.user_email, user_register_credentials.user_password) == False:
        return { "result": "register error: could not register user. maybe try again?" }

    return { "result": "success" }

@router.post("/auth/guest-login")
def guest_login():
    guest_name: str = "guest_" + str(randint(1000, 9999))

    if authentication.is_user_name_available(guest_name) == False:
        return { "result": "guest error: user name already in use. maybe Try again?" }

    return { "result": "success", "guest_name": guest_name }