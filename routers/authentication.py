# IMPORT LIBRARIES #
from fastapi import APIRouter

# IMPORT OBJECTS #
from objects import user_credentials
from objects import guest_credentials

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/auth/user-login")
def login(user_credentials: user_credentials.UserCredentials):
    return user_credentials

@router.post("/auth/user-register")
def register(user_credentials: user_credentials.UserCredentials):
    return user_credentials

@router.post("/auth/guest-login")
def guest(guest_credentials: guest_credentials.GuestCredentials):
    return guest_credentials