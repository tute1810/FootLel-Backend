# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status

# IMPORT INTERNAL LIBRARIES #
from logic.game.game_manager import GameManager
from logic.stats.stats_manager import StatsManager
from objects import user_id
from objects import player_guess

# CREATE THE ROUTER #
router = APIRouter()

# VARIABLES #
games_in_progress: dict[int, GameManager] = {}

# ENDPOINT FUNCTIONS #
@router.post("/game/start")
def start_game(user_id: user_id.UserId):
    global games_in_progress

    game_in_progress: GameManager
    if user_id.user_id not in games_in_progress:
        games_in_progress[user_id] = GameManager()
    game_in_progress = games_in_progress[user_id]

    row_headers: list[str]; column_headers: list[str]
    row_headers, column_headers = game_in_progress.start_game_board()
    
    return { "result": "success", "row_headers": row_headers, "column_headers": column_headers, "local_player_turn": True }

@router.post("/game/player-guess")
def player_guesses(player_guess: player_guess.PlayerGuess):
    global games_in_progress

    # VARIABLES #
    game_owner_id: int = player_guess.user_id; game_in_progress: GameManager = games_in_progress[game_owner_id]
    updated_board: list[list[int]]; correct_answer: bool; game_ended: bool; local_player_won: bool
    
    updated_board, correct_answer, game_ended, local_player_won = game_in_progress.player_guessed(player_guess.player_guess)

    if updated_board is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="error de tablero: no estas en una partida")

    is_local_players_turn: bool = False
    if game_ended == False:
        is_local_players_turn = game_in_progress.next_turn()

    # update stats #
    StatsManager.set_guesses_stats(game_owner_id, correct_answer)
    if game_ended == True:
        StatsManager.set_matches_stats(game_owner_id, local_player_won)

        del games_in_progress[game_owner_id]

    return { "result": "success", "correct_answer": correct_answer, "game_ended": game_ended, "local_player_won": local_player_won, "board": updated_board, "local_player_turn": is_local_players_turn }

@router.post("/game/player2-guess")
def player2_guesses(player2_guess: player_guess.PlayerGuess):
    global games_in_progress

    # VARIABLES #
    game_owner_id: int = player2_guess.user_id; game_in_progress: GameManager = games_in_progress[game_owner_id]
    updated_board: list[list[int]]; correct_answer: bool; game_ended: bool; local_player_won: bool
    
    updated_board, correct_answer, game_ended, local_player_won = game_in_progress.player2_guessed(player2_guess.player_guess)

    if updated_board is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="error de tablero: no estas en una partida")

    is_local_players_turn: bool = False
    if game_ended == False:
        is_local_players_turn = game_in_progress.next_turn()

    # update stats #
    StatsManager.set_guesses_stats(game_owner_id, correct_answer)
    if game_ended == True:
        StatsManager.set_matches_stats(game_owner_id, local_player_won)

        del games_in_progress[game_owner_id]

    return { "result": "success", "correct_answer": correct_answer, "game_ended": game_ended, "local_player_won": local_player_won, "board": updated_board, "local_player_turn": is_local_players_turn }


@router.post("/game/ai-guess")
def ai_guesses(user_id: user_id.UserId):
    global games_in_progress

    # VARIABLES #
    game_owner_id: int = user_id.user_id; game_in_progress: GameManager = games_in_progress[game_owner_id]
    updated_board: list[list[int]]; game_ended: bool; local_player_won: bool
    
    updated_board, game_ended, local_player_won = game_in_progress.ai_guessed()

    if updated_board is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error de tablero: no estas en una partida")

    is_local_players_turn: bool = False
    if game_ended == False:
        is_local_players_turn = game_in_progress.next_turn()

    # update stats #
    if game_ended == True:
        StatsManager.set_matches_stats(game_owner_id, local_player_won)

        del games_in_progress[game_owner_id]

    return { "result": "success", "game_ended": game_ended, "local_player_won": local_player_won, "board": updated_board, "local_player_turn": is_local_players_turn }