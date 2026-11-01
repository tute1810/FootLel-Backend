# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status, Depends

# IMPORT INTERNAL LIBRARIES #
from database import user_stats
from security import jwt

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.get("/stat/get-global-leaderboard")
def get_global_leaderboard():
    leaderboard: list[tuple[str, int]] | None = user_stats.get_global_leaderboard()

    if leaderboard is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de ranking: no fue posible acceder al ranking")

    return { "result": "success", "leaderboard": leaderboard }

@router.get("/stat/get-user-stats")
def get_user_stats(user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    user_stats_data: tuple[int] | None = user_stats.get_user_stats(user_id)

    if user_stats_data is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de obtencion de estadisticas: error al obtener las estadisticas del usuario")

    return { "result": "success", "user_points": user_stats_data[0], "guesses_made": user_stats_data[1], "correct_guesses": user_stats_data[2], "matches_played": user_stats_data[3], "matches_won": user_stats_data[4], "win_streak": user_stats_data[5] }