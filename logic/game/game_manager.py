from random import randint
from database import get_players


# =====[ VARIABLES ]===== #
is_playing: bool = False
game_turn: int = 0

teams_row: list[str] = []
nationalities_column: list[str] = []
player_slots: dict[str, bool] = {}


def game_start() -> tuple[list[str], list[str]]:
    reset_game()

    global is_playing

    is_playing = True

    create_board()

    return teams_row, nationalities_column

def reset_game():
    global teams_row, nationalities_column, player_slots, game_turn, is_playing

    is_playing = False

    game_turn = 0

    teams_row = []
    nationalities_column = []
    player_slots = {}

def create_board():
    global teams_row, nationalities_column, player_slots

    leagues_name: list[str] = ["premier", "bundesliga", "serie_a", "la_liga"]
    nationalities_name: list[str] = ["Argentina", "Italia", "Inglaterra", "España", "Francia"]

    teams: list[str] = ["", "", ""]
    nationalities: list[str] = ["", "", ""]
    players: list[str] = []

    for i in range(0, 3, 1):
        this_league_index: int = randint(0, len(leagues_name) - 1)
        random_league: str = leagues_name[this_league_index]
        teams_of_random_league: list[str] = get_players.get_league_teams(random_league, teams[0], teams[1])
        random_team_of_random_league: str = teams_of_random_league[randint(0, len(teams_of_random_league) - 1)][0]
        teams[i] = random_team_of_random_league
        if nationalities[0] == "":
            temp_nationalities_name: list[str] = nationalities_name.copy()
            for j in range(0, 3, 1):
                this_nationality_index: int = randint(0, len(temp_nationalities_name) - 1)
                random_nationality: str = temp_nationalities_name[this_nationality_index]
                nationalities[j] = random_nationality
                temp_nationalities_name.pop(this_nationality_index)
        for j in range(0, 3, 1):
            players.append(get_players.get_player(teams[i], random_league, nationalities[j])[0][0])
    teams_row = teams
    nationalities_column = nationalities
    for i in range(0, len(players), 1):
        player_slots[players[i]] = False

def next_turn() -> bool:
    game_turn += 1

    return bool(game_turn % 2 != 0)

def turn_end(player_guess: str) -> tuple[dict[str, bool], bool]:
    if is_playing == False:
        return None

    for i in range(0, len(player_slots), 1):
        if player_guess == player_slots.keys()[i]:
            player_slots[i] = True
            return player_slots, True
    return player_slots, False