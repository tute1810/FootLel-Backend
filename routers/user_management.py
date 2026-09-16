# IMPORT LIBRARIES #
from fastapi import APIRouter

# IMPORT OBJECTS #
from objects import user_id
from database import user_management

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/user/get-user")
def get_user(user_id: user_id.UserId):
    return user_management.get_user_name(user_id)