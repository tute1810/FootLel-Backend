# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter

# IMPORT INTERNAL LIBRARIES #
from logic.game.game_manager import player_guessed, ai_guessed, next_turn, game_start
from objects import player_guess

# CREATE THE ROUTER #
router = APIRouter()

# ENDPOINT FUNCTIONS #
@router.post("/game/start")
def start_game():
    print("start", flush=True)
    column_headers: list[str]; row_headers: list[str];
    column_headers, row_headers = game_start()

    return { "result": "success", "column_headers": column_headers, "row_headers": row_headers, "local_player_turn": True }

@router.post("/game/player-guess")
def player_guesses(player_guess: player_guess.PlayerGuess):
    print("player")
    updated_board: list[list[int]]; correct_answer: bool; game_ended: bool;
    updated_board, correct_answer, game_ended = player_guessed(player_guess.player_guess)

    if updated_board is None:
        return { "result": "board error: not in a game" }

    is_local_players_turn: bool = next_turn()

    return { "result": "success", "correct_answer": correct_answer, "game_ended": game_ended, "board": updated_board, "local_player_turn": is_local_players_turn }

@router.post("/game/ai-guess")
def ai_guesses():
    print("ia")
    updated_board: list[list[int]]; game_ended: bool;
    updated_board, game_ended = ai_guessed()

    if updated_board is None:
        return { "result": "board error: not in a game" }

    is_local_players_turn: bool = next_turn()

    return { "result": "success", "game_ended": game_ended, "board": updated_board, "local_player_turn": is_local_players_turn }