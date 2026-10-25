# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status, Depends

# IMPORT INTERNAL LIBRARIES #
from objects import user_options
from database import user_config
from security import jwt

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.get("/config/get-user-config")
def get_user_config(user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    config_results: list[bool | None] = []
    config_results.extend([user_config.get_dark_mode_config_state(user_id), user_config.get_animations_config_state(user_id), user_config.get_compatibility_config_status(user_id)])

    for i in range(0, len(config_results), 1):
        if config_results[i] is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de obtencion de configuracion: error al obtener las opciones y preferencias del usuario")

    return { "result": "success", "dark_mode": config_results[0], "animation_state": config_results[1], "compatibility_mode": config_results[2] }

@router.patch("/config/set-user-config")
def set_user_config(user_options: user_options.UserOptions, user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    config_results: list[bool] = []
    config_results.extend([user_config.set_dark_mode_config_state(user_id, user_options.dark_mode), user_config.set_animations_config_state(user_id, user_options.animation_state), user_config.set_compatibility_config_status(user_id, user_options.compatibility_mode)])

    for i in range(0, len(config_results), 1):
        if config_results[i] is False:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de guardado de configuracion: error al guardar las opciones y preferencias del usuario")

    return { "result": "success" }