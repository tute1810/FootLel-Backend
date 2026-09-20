# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter
from random import randint

# IMPORT INTERNAL LIBRARIES #
from database import get_players

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/game/create-table")
def create_table():
    """
        E1  E2  E3
    N1    |   |
        ----------
    N2    |   |
        ----------
    N3    |   |
    """

    leagues_cout: int = 4
    leagues_name = ["premier", "bundesliga", "serie_a", "la_liga"]

    this_league_index: int = randint(0, leagues_cout - 1)
    # teams_of_random_league: list[str] = 
    return { "result": str(get_players.get_league_teams(leagues_name[this_league_index])) }