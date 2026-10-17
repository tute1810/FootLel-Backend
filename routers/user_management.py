# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status

# IMPORT INTERNAL LIBRARIES #
from objects import user_id
from objects import user_name
from objects import user_info
from database import user_management
from database import authentication

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.get("/user/get-user-info/{user_name}")
def get_user_info(user_name: str):
    user_info = user_management.get_user_info(user_name)
    user_password = user_management.get_user_password_with_user_name(user_name)

    if user_info is None or user_password is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="error de informacion del usuario: no se pudo encontrar el usuario")

    return { "result": "success", "user_id": int(user_info[0]), "user_email": str(user_info[1]), "user_password": str(user_password) }

@router.delete("/user/eliminate-user/{user_id}")
def eliminate_user(user_id: int):
    if user_management.eliminate_user(user_id) == False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de eliminacion de usuario: no fue posible eliminar el usuario")
    
    return { "result": "success" }

@router.patch("/user/edit-user-info")
def edit_user_info(user_info: user_info.UserInfo):
    if authentication.is_user_name_used_by_another_user(user_info.user_id, user_info.user_name) == False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error al editar perfil: ese nombre de usuario ya esta en uso")

    if authentication.is_user_email_used_by_another_user(user_info.user_id, user_info.user_email) == False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error al editar perfil: ese email ya esta en uso")
    
    if user_management.change_user_data(user_info.user_id, user_info.user_name, user_info.user_email, user_info.user_password) == False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error al editar perfil: hubo un error al editar el perfil, intente de vuelta")
    
    return { "result": "success" }