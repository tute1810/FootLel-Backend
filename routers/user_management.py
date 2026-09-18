# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter

# IMPORT INTERNAL LIBRARIES #
from objects import user_id
from objects import user_name
from database import user_management

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/user/get-users-table")
def get_users_table():
    users_table = user_management.get_users_table()

    if users_table is None:
        return { "result": "users table error: could not fetch users" }

    return { "result": "success", "users_table": str(users_table) }

@router.post("/user/get-user-info")
def get_user_info(user_name: user_name.UserName):
    user_info = user_management.get_user_info(user_name.user_name)

    if user_info is None:
        return { "result": "user info error: could not fetch user info" }

    return { "result": "success", "user_id": int(user_info[0]), "user_email": str(user_info[1]) }

@router.post("/user/eliminate-user")
def eliminate_user(user_id: user_id.UserId):
    ab = user_management.eliminate_user(user_id.user_id)
    if ab[0] == False:
        return { "result": "user elimiation error: failed to eliminate user", "error": ab[1] }
    
    return { "result": "success" }