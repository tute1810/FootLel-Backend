# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter

# IMPORT INTERNAL LIBRARIES #
from objects import user_id
from objects import user_name
from database import user_management

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/user/get-user-info")
def get_user_info(user_name: user_name.UserName):
    user_info = user_management.get_user_id(user_name.user_name)

    if user_info is None:
        return { "result": "user info error: could not fetch user info" }

    return { "result": "success", "user_id": int(user_info), "user_email": str(user_info) }

@router.post("/user/eliminate-user")
def eliminate_user(user_id: user_id.UserId):
    if user_management.eliminate_user(user_id.user_id) == False:
        return { "result": "user elimiation error: failed to eliminate user" }
    
    return { "result": "success" }