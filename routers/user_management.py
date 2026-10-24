# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, Depends, HTTPException, status

# IMPORT INTERNAL LIBRARIES #
from objects import user_info
from database import user_management, authentication
from security import jwt

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.get("/user/get-user-info")
def get_user_info(user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    db_user_name_and_email: tuple | None = user_management.get_user_info(user_id)

    if db_user_name_and_email is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="error de datos del usuario: usuario no existente o error al buscar los datos del usuario")
    
    return { "result": "success", "user_name": db_user_name_and_email[0], "user_email": db_user_name_and_email[1] }

@router.delete("/user/eliminate-user")
def eliminate_user(user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    if user_management.eliminate_user(user_id) is False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de eliminacion de usuario: error al eliminar el usuario")
    
    return { "result": "success" }

@router.patch("/user/edit-user-info")
def edit_user_info(user_info: user_info.UserInfo, user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    user_name: str = user_info.user_name
    user_name_already_in_use: bool | None = authentication.is_user_name_used_by_another_user(user_id, user_name)

    if user_name_already_in_use is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de edicion de perfil: error al verificar nombres de usuario en uso")
    elif user_name_already_in_use is True:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error de edicion de perfil: nombre de usuario en uso")

    user_email: str = user_info.user_email
    user_email_already_in_use: bool | None = authentication.is_user_email_used_by_another_user(user_id, user_email)

    if user_email_already_in_use is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de edicion de perfil: error al verificar emails de usuario en uso")
    if user_email_already_in_use is True:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error al editar perfil: email en uso")

    user_password: str = user_info.user_password
    
    if user_management.change_user_data(user_id, user_name, user_email, user_password) is False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error al editar perfil: error al editar los datos del usuario")
    
    return { "result": "success" }