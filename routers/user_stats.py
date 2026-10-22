# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status, Depends

# IMPORT INTERNAL LIBRARIES #
from objects import boolean_state
from database import user_stats
from security import jwt 

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.get("/stat/get-leaderboard")
def get_leaderboard():
    leaderboard: list[tuple[str, int]] = user_stats.get_table_ranking()

    if leaderboard is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de ranking: no fue posible acceder al ranking")
    
    return { "result": "success", "leaderboard": leaderboard }

"""
user_points,
guesses_made,
correct_guesses,
matches_played,
matches_won,
win_streak
"""
""""""
@router.get("/stat/get-user-stats")
def get_user_stats(user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    user_stats_data: tuple[int, int, int, int, int] | None = user_stats.get_user_stats(user_id)
    print(user_stats_data, flush=True)

    if user_stats_data is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de obtencion de estadisticas: error al obtener las estadisticas del usuario")

    return { "result": "success", "user_points": user_stats_data[0], "guesses_made": user_stats_data[1], "correct_guesses": user_stats_data[2], "matches_played": user_stats_data[3], "matches_won": user_stats_data[4], "win_streak": user_stats_data[5] }

@router.patch("/stat/set-user-dark-mode-state")
def set_dark_mode_state(boolean_state: boolean_state.BooleanState, user_id: int=Depends(jwt.check_access_token_and_get_user_id)):
    if user_stats.set_dark_mode_config_state(user_id, boolean_state.boolean) is False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de dark mode: no se pudo guardar el valor")
    
    return { "result": "success" }

@router.patch("/stat/set-user-animation-state")
def set_animation_state(boolean_state: boolean_state.BooleanState,user_id: int=Depends(jwt.check_access_token_and_get_user_id)):
    if user_stats.set_animations_config_state(user_id, boolean_state.boolean) is False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de animacion: no se pudo guardar el valor")
    
    return { "result": "success" }

@router.patch("/stat/set-user-compatibility-state")
def set_compatibility_state(boolean_state: boolean_state.BooleanState,user_id: int=Depends(jwt.check_access_token_and_get_user_id)):
    if user_stats.set_compatibility_config_status(user_id, boolean_state.boolean) is False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de compatibilidad: no se pudo guardar el valor")
    
    return { "result": "success" } 