# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter

# IMPORT INTERNAL LIBRARIES #
from objects import user_id
from objects import user_email
from database import user_management

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/user/get-user-id")
def get_user_id(user_email: user_email.UserEmail):
    user_id = user_management.get_user_id(user_email.user_email)

    if user_id is None:
        return { "result": "user id error: user with the specified email was not found" }

    return { "result": "success", "user_id": int(user_id) }

@router.post("/user/get-user-name")
def get_user_name(user_id: user_id.UserId):
    user_name = user_management.get_user_name(int(user_id.user_id))

    if user_name is None:
        return { "result": "user name error: user with the specified id was not found" }

    return { "result": "success", "user_name": str(user_name) }