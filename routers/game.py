# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter

# IMPORT INTERNAL LIBRARIES #
from logic.game.game_manager import turn_end, next_turn, game_start
from objects import player_guess

# CREATE THE ROUTER #
router = APIRouter()

# VARIABLES #
"""is_up_to_date: bool = True
local_players_turn: bool = True

# COMMUNICATION FUNCTIONS #
def turn_end_():
    correct_answer: bool = turn_end("")

    if correct_answer is None:
        return { "result": "turn error: not in a game" }

    return { "result": "success", "answer": str(correct_answer) }

def turn_start_(local_players_turn_: bool):
    global local_players_turn; global is_up_to_date

    local_players_turn = local_players_turn_
    is_up_to_date = False"""

# ENDPOINT FUNCTIONS #
@router.post("/game/start")
def start_game():
    column_headers: list[str]; row_headers: list[str];
    column_headers, row_headers = game_start()

    return { "result": "success", "column_headers": column_headers, "row_headers": row_headers, "local_player_turn": True }

@router.post("/game/guess")
def guess_player_and_start_new_turn(player_guess: player_guess.PlayerGuess):
    if player_guess.was_local_player_guessing == False:
        return None # ai

    updated_board: dict[str, bool]; correct_answer: bool;
    updated_board, correct_answer = turn_end(player_guess.player_guess)

    if updated_board is None:
        return { "result": "board error: not in a game" }

    is_local_players_turn: bool = next_turn()

    return { "result": "success", "correct_answer": correct_answer, "board": updated_board, "local_player_turn": is_local_players_turn }

"""@router.post("/game/create-table")
def create_table():
    pass

@router.post("/game/turn-ended")
def turn_ended():
    pass

@router.post("/game/has-turn-started")
def has_turn_started():
    if is_up_to_date == False:
        is_up_to_date = True
        return { "result": "success", "local_player_turn": str(local_players_turn) }
    return { "result": "up to date" }"""