# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status

# IMPORT INTERNAL LIBRARIES #
from objects import dark_mode_state
from objects import animation_state
from objects import compatibility_state
from database import user_stats

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/stat/set-user-dark-mode-state")
def set_dark_mode_state(dark_mode_state: dark_mode_state.DarkModeState):
    if user_stats.set_dark_mode_config_state(dark_mode_state) == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="error de dark mode: no se pudo guardar el valor")
    
    return { "result": "success" }

@router.post("/stat/set-user-animation-state")
def set_animation_state(animation_state: animation_state.AnimationState):
    if user_stats.set_animation_config_state(animation_state) == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="error de animacion: no se pudo guardar el valor")
    
    return { "result": "success" }

@router.post("/stat/set-user-compatibility-state")
def set_compatibility_state(compatibility_state: compatibility_state.CompatibilityState):
    if user_stats.set_compatibility_config_state(compatibility_state) == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="error de compatibilidad: no se pudo guardar el valor")
    
    return { "result": "success" }