# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status

# IMPORT INTERNAL LIBRARIES #
from objects import user_id
from objects import user_name
from database import user_management

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/user/get-user-info")
def get_user_info(user_name: user_name.UserName):
    user_info = user_management.get_user_info(user_name.user_name)

    if user_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="error de informacion del usuario: no se pudo encontrar el usuario")

    return { "result": "success", "user_id": int(user_info[0]), "user_email": str(user_info[1]) }

@router.post("/user/eliminate-user")
def eliminate_user(user_id: user_id.UserId):
    if user_management.eliminate_user(user_id.user_id) == False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de eliminacion de usuario: no fue posible eliminar el usuario")
    
    return { "result": "success" }