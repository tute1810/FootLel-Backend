# IMPORT LIBRARIES #
from fastapi import APIRouter

# IMPORT OBJECTS #
from objects import user_id

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.get("/user/get-user")
def get_user(user_id: user_id.UserId):
    return id