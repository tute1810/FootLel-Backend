# IMPORT EXTERNAL LIBRARIES #
from fastapi import APIRouter, HTTPException, status, Depends

# IMPORT INTERNAL LIBRARIES #
from logic import game_manager, stats_manager, date_manager
from objects import player_guess, start_game_options,user_friend
from database import user_management, user_stats, game,multiplayer_game
from security import jwt

# CREATE THE ROUTER #
router = APIRouter()

# VARIABLES #
games_in_progress: dict[int, game_manager.GameManager] = {}
multiplayer_games_in_progress: dict[int, game_manager.GameManager] = {}

# ENDPOINT FUNCTIONS #
@router.post("/test/test")
def test():
    test = game.get_all_teams_from_a_league("premier", "", "")

    test2 = game.get_all_players_from_a_team_with_nationality("Liverpool", "premier", "france")

    return { str(test), str(test2) }

@router.post("/game/start")
def start_game(start_game_options: start_game_options.StartGameOptions, user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    if start_game_options.is_daily_challenge is True:
        error: bool = date_manager.update_daily_challenge_date()

        if error is True:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de daily challenge: error al resetear el estado del daily challenge")
        
        user_daily_challenge_state: bool | None = user_stats.get_user_daily_challenge_state_with_id(user_id)

        if user_daily_challenge_state is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de inicio de juego: error al obtener el estado del daily challenge del usuario")
        elif user_daily_challenge_state is True:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error de inicio de juego: el usuario ya ha completado el daily challenge hoy, vuelve mañana")

    global games_in_progress

    game_in_progress: game_manager.GameManager
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

    game_owner_id: int = user_id; game_in_progress: game_manager.GameManager = games_in_progress.get(game_owner_id)

    if game_in_progress is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de adivinanza: no estas en un juego")
    
    is_owner_guest: bool | None = user_management.is_guest_with_user_id(game_owner_id)
    
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
            stats_manager.set_matches_stats(game_owner_id, is_daily_challenge, local_player_won)
            if is_daily_challenge is True:
                user_stats.set_user_daily_challenge_with_user_id(game_owner_id, True)
    if game_ended is True:
        del games_in_progress[game_owner_id]

    return { "result": "success", "correct_answer": correct_answer, "game_ended": game_ended, "local_player_won": local_player_won, "board": updated_board, "local_player_turn": is_local_players_turn }

@router.post("/game/player2-guess")
def player2_guesses(player2_guess: player_guess.PlayerGuess, user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    global games_in_progress

    game_owner_id: int = user_id; game_in_progress: game_manager.GameManager = games_in_progress.get(game_owner_id)
    
    if game_in_progress is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de adivinanza: no estas en un juego")
    
    is_owner_guest: bool | None = user_management.is_guest_with_user_id(game_owner_id)

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
            stats_manager.set_matches_stats(game_owner_id, is_daily_challenge, local_player_won)
            if is_daily_challenge is True:
                user_stats.set_user_daily_challenge_with_user_id(game_owner_id, True)
    if game_ended is True:
        del games_in_progress[game_owner_id]

    return { "result": "success", "correct_answer": correct_answer, "game_ended": game_ended, "local_player_won": local_player_won, "board": updated_board, "local_player_turn": is_local_players_turn }

@router.post("/game/ai-guess")
def ai_guesses(user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    global games_in_progress

    game_owner_id: int = user_id; game_in_progress: game_manager.GameManager = games_in_progress.get(game_owner_id)

    if game_in_progress is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error de adivinanza: no estas en un juego")
    
    is_owner_guest: bool | None = user_management.is_guest_with_user_id(game_owner_id)
    
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
            stats_manager.set_matches_stats(game_owner_id, is_daily_challenge, local_player_won)
            if is_daily_challenge is True:
                user_stats.set_user_daily_challenge_with_user_id(game_owner_id, True)
        del games_in_progress[game_owner_id]

    return { "result": "success", "game_ended": game_ended, "local_player_won": local_player_won, "board": updated_board, "local_player_turn": is_local_players_turn }

@router.post("/game/start-multiplayer-game")
def start_multiplayer_game(user_friend: user_friend.UserFriend, user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    friend_name: int = user_friend.friend_name
    
    if friend_name == "":
        pass
    else:
        friend_id: int | None = user_management.get_user_id_with_user_name(friend_name)
        
        if friend_id is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de inicio de juego multijugador: usuario de la solicitud no encontrado")

        game_id: int | None = multiplayer_game.create_game_mp([user_id, friend_id])

        multiplayer_game.set_player_multiplayer_state_with_id(user_id, True)
        multiplayer_game.set_player_multiplayer_state_with_id(friend_id, True)

        if game_id is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error de inicio de juego multijugador: error al crear el juego multijugador")

    return { "result": "success" }

@router.post("/game/join-multiplayer-game")
def join_multiplayer_game(user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    global multiplayer_games_in_progress

    match_started: bool = False
    game_id: int = -1
    multiplayer_board: list = []
    if multiplayer_game.get_user_multiplayer_state(user_id) is True:
        match_started = True
        game_boards: list[tuple] = multiplayer_game.get_players_id_from_mp()

        if game_boards is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error al unirse juego multijugador: error al obtener los jugadores del juego multijugador")

        is_first_player: bool = False
        for i in range(0, len(game_boards), 1):
            for j in range(0, len(game_boards[i][0]), 1):
                if game_boards[i][0][j] == user_id:
                    game_id = game_boards[i][1]
                    if j == 0:
                        is_first_player = True
                    break

        multiplayer_game_in_progress: game_manager
        if is_first_player is True:
            multiplayer_games_in_progress[game_id] = game_manager.GameManager(False, False)
            multiplayer_game_in_progress = multiplayer_games_in_progress[game_id]
            multiplayer_board = multiplayer_game_in_progress.start_game_board()
        else:
            multiplayer_game_in_progress = multiplayer_games_in_progress.get(game_id)

            if multiplayer_game_in_progress is None:
                match_started = False
            else:
                multiplayer_board = multiplayer_game_in_progress.get_game_board(True)
        
    return { "result": "success", "match_started": match_started, "game_id": game_id, "board": multiplayer_board }

@router.post("/game/multiplayer-guess")
def multiplayer_guess(player_guess: player_guess.PlayerGuess, user_id: int = Depends(jwt.check_access_token_and_get_user_id)):
    pass