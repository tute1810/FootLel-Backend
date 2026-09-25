from random import randint
from database import get_players
import logging
import sys

# LOGS #
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


# =====[ VARIABLES ]===== #
is_playing: bool = False
game_turn: int = 0

teams_row: list[str] = []
nationalities_column: list[str] = []
player_slots: dict[str, bool] = {}

player_names_matrix: list[list[str]] = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]
player_slots_matrix: list[list[int]] = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]



def game_start() -> tuple[list[str], list[str]]:
    global is_playing

    is_playing = True

    create_board()
    _ = next_turn()

    return teams_row, nationalities_column

def reset_game():
    global teams_row, nationalities_column, game_turn, is_playing, player_names_matrix, player_slots_matrix

    is_playing = False

    game_turn = 0

    teams_row = []
    nationalities_column = []
    player_slots_matrix = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    player_names_matrix = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

def create_board():
    global teams_row, nationalities_column, player_names_matrix, player_slots_matrix

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
        row: int = i // 3
        column: int = i % 3
        player_names_matrix[row][column] = players[i]
        player_slots_matrix[row][column] = 0

def next_turn() -> bool:
    global game_turn
    game_turn += 1

    return bool(game_turn % 2 != 0)

def player_guessed(player_guess: str) -> tuple[list[list[int]], bool, bool] | None:
    logger.info("----------player guessed func------------")
    if is_playing == False:
        logger.info("not playing")
        return None

    global player_names_matrix, player_slots_matrix

    for i in range(0, (len(player_names_matrix) * len(player_names_matrix[0])), 1):
        row: int = i // 3
        column: int = i % 3
        if player_names_matrix[row][column] == player_guess:
            logger.info("le pegaste")
            player_slots_matrix[row][column] = 1
            
            if all(value != 0 for row in player_slots_matrix for value in row):
                logger.info("juego terminado")
                reset_game()
                return player_slots_matrix, True, True
            
            return player_slots_matrix, True, False
    return player_slots_matrix, False, False

def ai_guessed() -> tuple[list[list[int]], bool] | None:
    logger.info("----------ai guessed func------------")
    if is_playing == False:
        logger.info("not playing")
        return None

    global player_names_matrix, player_slots_matrix

    player_slots_rows: list[int] = []
    player_slots_columns: list[int] = []
    for i in range(0, (len(player_names_matrix) * len(player_names_matrix[0])), 1):
        row: int = i // 3
        column: int = i % 3

        if player_slots_matrix[row][column] == 1:
            logger.info("detecte un slot del jugador")
            player_slots_rows.append(row)
            player_slots_columns.append(column)

    if len(player_slots_rows) == 0:
        logger.info("ia terminada: no habia slots del jogadore")
        return player_slots_matrix, False

    random_player_slot_index: int = randint(0, (len(player_slots_rows) - 1))
    selected_player_slot_packaged: list[int] = [ player_slots_rows[random_player_slot_index], player_slots_columns[random_player_slot_index] ]
    logger.info("slot del jugador random seleccionado es: " + str(selected_player_slot_packaged))

    slot_selected: bool = False
    for i in range(0, 4, 1):
        if i < 2:
            if i == 0:
                new_row: int = selected_player_slot_packaged[0] - 1
                if _in_range(new_row, 0, 2) == False:
                    continue

                if player_slots_matrix[new_row][selected_player_slot_packaged[1]] == 0:
                    if randint(0, 1) == 1:
                        logger.info("eleji arriba")
                        player_slots_matrix[new_row][selected_player_slot_packaged[1]] = -1
                        slot_selected = True
                        break
            else:
                new_row: int = selected_player_slot_packaged[0] + 1
                if _in_range(new_row, 0, 2) == False:
                    continue

                if player_slots_matrix[new_row][selected_player_slot_packaged[1]] == 0:
                    if randint(0, 1) == 1:
                        logger.info("eleji abajo")
                        player_slots_matrix[new_row][selected_player_slot_packaged[1]] = -1
                        slot_selected = True
                        break
        else:
            if i == 2:
                new_column: int = selected_player_slot_packaged[1] - 1
                if _in_range(new_column, 0, 2) == False:
                    continue

                if player_slots_matrix[selected_player_slot_packaged[0]][new_column] == 0:
                    if randint(0, 1) == 1:
                        logger.info("eleji izq")
                        player_slots_matrix[selected_player_slot_packaged[0]][new_column] = -1
                        slot_selected = True
                        break
            else:
                new_column: int = selected_player_slot_packaged[1] + 1
                if _in_range(new_column, 0, 2) == False:
                    continue

                if player_slots_matrix[selected_player_slot_packaged[0]][new_column] == 0:
                    if randint(0, 1) == 1:
                        logger.info("eleji der")
                        player_slots_matrix[selected_player_slot_packaged[0]][new_column] = -1
                        slot_selected = True
                        break

    if slot_selected == False:
        logger.info("le erre a los slots vacios")
        return player_slots_matrix, False
    else:
        if all(value != 0 for row in player_slots_matrix for value in row):
            logger.info("juego terminado, no hay mas slots vacios")
            reset_game()
            return player_slots_matrix, True
        else:
            logger.info("puse slot")
            return player_slots_matrix, False

def _in_range(value, minimum, maximum):
    return minimum <= value <= maximum