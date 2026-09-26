# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status

# IMPORT INTERNAL LIBRARIES #
from logic.game.game_manager import player_guessed, player2_guessed, ai_guessed, next_turn, start_game_board
from logic.stats.stats_manager import set_matches_stats, set_guesses_stats
from objects import user_id
from objects import player_guess

# CREATE THE ROUTER #
router = APIRouter()

# VARIABLES #
game_owner_id: int = -1

# ENDPOINT FUNCTIONS #
@router.post("/game/start")
def start_game(user_id: user_id.UserId):
    global game_owner_id
    
    game_owner_id = user_id.user_id

    row_headers: list[str]; column_headers: list[str]
    row_headers, column_headers = start_game_board()
    
    return { "result": "success", "row_headers": row_headers, "column_headers": column_headers, "local_player_turn": True }

@router.post("/game/player-guess")
def player_guesses(player_guess: player_guess.PlayerGuess):
    updated_board: list[list[int]]; correct_answer: bool; game_ended: bool; local_player_won: bool
    updated_board, correct_answer, game_ended, local_player_won = player_guessed(player_guess.player_guess)

    if updated_board is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="error de tablero: no estas en una partida")

    is_local_players_turn: bool = False
    if game_ended == False:
        is_local_players_turn = next_turn()

    # update stats #
    set_guesses_stats(game_owner_id, correct_answer)
    if game_ended == True:
        set_matches_stats(game_owner_id, local_player_won)

    return { "result": "success", "correct_answer": correct_answer, "game_ended": game_ended, "local_player_won": local_player_won, "board": updated_board, "local_player_turn": is_local_players_turn }

@router.post("/game/player2-guess")
def player2_guesses(player2_guess: player_guess.PlayerGuess):
    updated_board: list[list[int]]; correct_answer: bool; game_ended: bool; local_player_won: bool
    updated_board, correct_answer, game_ended, local_player_won = player2_guessed(player2_guess.player_guess)

    if updated_board is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="error de tablero: no estas en una partida")

    is_local_players_turn: bool = False
    if game_ended == False:
        is_local_players_turn = next_turn()

    # update stats #
    set_guesses_stats(game_owner_id, correct_answer)
    if game_ended == True:
        set_matches_stats(game_owner_id, local_player_won)

    return { "result": "success", "correct_answer": correct_answer, "game_ended": game_ended, "local_player_won": local_player_won, "board": updated_board, "local_player_turn": is_local_players_turn }


@router.post("/game/ai-guess")
def ai_guesses():
    updated_board: list[list[int]]; game_ended: bool; local_player_won: bool
    updated_board, game_ended, local_player_won = ai_guessed()

    if updated_board is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error de tablero: no estas en una partida")

    is_local_players_turn: bool = False
    if game_ended == False:
        is_local_players_turn = next_turn()

    # update stats #
    if game_ended == True:
        set_matches_stats(game_owner_id, local_player_won)

    return { "result": "success", "game_ended": game_ended, "local_player_won": local_player_won, "board": updated_board, "local_player_turn": is_local_players_turn }