# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status

# IMPORT INTERNAL LIBRARIES #
from objects import boolean_state
from database import user_stats

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/stat/get-leaderboard")
def get_leaderboard():
    leaderboard: list[tuple[str, int]] = user_stats.get_table_ranking()

    if leaderboard is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de ranking: no fue posible acceder al ranking")
    
    return { "result": "success", "leaderboard": leaderboard }

@router.post("/stat/set-user-dark-mode-state")
def set_dark_mode_state(boolean_state: boolean_state.BooleanState):
    if user_stats.set_dark_mode_config_state(boolean_state.user_id, boolean_state.boolean) == False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de dark mode: no se pudo guardar el valor")
    
    return { "result": "success" }

@router.post("/stat/set-user-animation-state")
def set_animation_state(boolean_state: boolean_state.BooleanState):
    if user_stats.set_animations_config_state(boolean_state.user_id, boolean_state.boolean) == False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de animacion: no se pudo guardar el valor")
    
    return { "result": "success" }

@router.post("/stat/set-user-compatibility-state")
def set_compatibility_state(boolean_state: boolean_state.BooleanState):
    if user_stats.set_compatibility_config_status(boolean_state.user_id, boolean_state.boolean) == False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de compatibilidad: no se pudo guardar el valor")
    
    return { "result": "success" }