# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status, Depends

# IMPORT INTERNAL LIBRARIES #
from logic import game_manager, stats_manager
from objects import player_guess, start_game_options
from database import user_management
from security import jwt

# CREATE THE ROUTER #
router = APIRouter()

# VARIABLES #
games_in_progress: dict[int, game_manager.GameManager] = {}

# ENDPOINT FUNCTIONS #
@router.post("/game/start")
def start_game(start_game_options: start_game_options.StartGameOptions, user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    global games_in_progress

    game_in_progress: game_manager.GameManager
    if user_id not in games_in_progress:
        games_in_progress[user_id] = game_manager.GameManager(start_game_options.is_last_round, start_game_options.is_daily_challenge)
    game_in_progress = games_in_progress[user_id]

    row_headers: list[str]; column_headers: list[str]
    row_headers, column_headers = game_in_progress.start_game_board()

    if len(row_headers) == 0 or len(column_headers) == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de inicio de juego: se produjo un error al crear el tablero")
    
    return { "result": "success", "row_headers": row_headers, "column_headers": column_headers, "local_player_turn": True }

@router.post("/game/player-guess")
def player_guesses(player_guess: player_guess.PlayerGuess, user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    global games_in_progress

    game_owner_id: int = user_id; game_in_progress: game_manager.GameManager = games_in_progress[user_id]; is_owner_guest: bool | None = user_management.is_guest_with_user_id(game_owner_id)
    
    if is_owner_guest is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de adivinanza: error al obtener si el host es guest")

    updated_board: list[list[int]]; correct_answer: bool; game_ended: bool; local_player_won: bool; is_last_round: bool; is_daily_challenge: bool
    updated_board, correct_answer, game_ended, local_player_won, is_last_round, is_daily_challenge = game_in_progress.player_guessed(player_guess.player_guess)

    if updated_board is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de tablero: no estas en una partida")

    is_local_players_turn: bool = False
    if game_ended is False:
        is_local_players_turn = game_in_progress.next_turn()

    # update user stats #
    if is_owner_guest is False:
        stats_manager.set_guesses_stats(game_owner_id, correct_answer)
        if game_ended is True and is_last_round is True:
            print("setting matches stats for player guess")
            stats_manager.set_matches_stats(game_owner_id, local_player_won)
    if game_ended is True:
        del games_in_progress[game_owner_id]

    return { "result": "success", "correct_answer": correct_answer, "game_ended": game_ended, "local_player_won": local_player_won, "board": updated_board, "local_player_turn": is_local_players_turn }

@router.post("/game/player2-guess")
def player2_guesses(player2_guess: player_guess.PlayerGuess, user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    global games_in_progress

    game_owner_id: str = user_id; game_in_progress: game_manager.GameManager = games_in_progress[game_owner_id]; is_owner_guest: bool | None = user_management.is_guest_with_user_id(game_owner_id)
    
    if is_owner_guest is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de adivinanza: error al obtener si el host es guest")
    
    updated_board: list[list[int]]; correct_answer: bool; game_ended: bool; local_player_won: bool; is_last_round: bool; is_daily_challenge: bool
    updated_board, correct_answer, game_ended, local_player_won, is_last_round, is_daily_challenge = game_in_progress.player2_guessed(player2_guess.player_guess)

    if updated_board is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de tablero: no estas en una partida")

    is_local_players_turn: bool = False
    if game_ended is False:
        is_local_players_turn = game_in_progress.next_turn()

    # update user stats #
    if is_owner_guest is False:
        stats_manager.set_guesses_stats(game_owner_id, correct_answer)
        if game_ended is True and is_last_round is True:
            print("setting matches stats for player2")
            stats_manager.set_matches_stats(game_owner_id, local_player_won)
    if game_ended is True:
        del games_in_progress[game_owner_id]

    return { "result": "success", "correct_answer": correct_answer, "game_ended": game_ended, "local_player_won": local_player_won, "board": updated_board, "local_player_turn": is_local_players_turn }

@router.post("/game/ai-guess")
def ai_guesses(user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    global games_in_progress

    game_owner_id: str = user_id; game_in_progress: game_manager.GameManager = games_in_progress[game_owner_id]; is_owner_guest: bool | None = user_management.is_guest_with_user_id(game_owner_id)
    
    if is_owner_guest is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de adivinanza: error al obtener si el host es guest")
    
    updated_board: list[list[int]]; game_ended: bool; local_player_won: bool; is_last_round: bool; is_daily_challenge: bool
    updated_board, game_ended, local_player_won, is_last_round, is_daily_challenge = game_in_progress.ai_guessed()

    if updated_board is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de tablero: no estas en una partida")

    is_local_players_turn: bool = False
    if game_ended is False:
        is_local_players_turn = game_in_progress.next_turn()

    # update user stats #
    if game_ended is True:
        if is_owner_guest is False and is_last_round is True:
            stats_manager.set_matches_stats(game_owner_id, local_player_won)
            print("setting matches stats for AI guess")
        del games_in_progress[game_owner_id]

    return { "result": "success", "game_ended": game_ended, "local_player_won": local_player_won, "board": updated_board, "local_player_turn": is_local_players_turn }