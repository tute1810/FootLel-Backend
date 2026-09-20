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
    N1    | X | X
        ----------
    N2    | X |
        ----------
    N3    |   | X
    """

    leagues_name: list[str] = ["premier", "bundesliga", "serie_a", "la_liga"]
    nationalities_name: list[str] = ["Argentina", "Italia", "Inglaterra", "España", "Francia"]

    teams: list[str] = ["", "", ""]
    nationalities: list[str] = ["", "", ""]
    players: list[str] = ["", "", ""]

    for i in range(0, 3, 1):
        this_league_index: int = randint(0, len(leagues_name) - 1)
        random_league: str = leagues_name[this_league_index]
        teams_of_random_league: list[str] = get_players.get_league_teams(random_league, teams[0], teams[1])
        random_team_of_random_league: str = teams_of_random_league[randint(0, len(teams_of_random_league) - 1)][0]
        teams[i] = random_team_of_random_league
        if nationalities[0] == "":
            temp_nationalities_name: list[str] = nationalities_name
            for j in range(0, 3, 1):
                this_nationality_index: int = randint(0, len(temp_nationalities_name) - 1)
                random_nationality: str = temp_nationalities_name[this_nationality_index]
                nationalities[j] = random_nationality
                temp_nationalities_name.pop(this_nationality_index)
        for j in range(0, 3, 1):
            players[i] = get_players.get_player(teams[i], random_league, nationalities[j])[0][0]
    return { "result": "success", "team_rows": str(teams), "nationality_columns": str(nationalities), "players_column_to_rows": str(players) }