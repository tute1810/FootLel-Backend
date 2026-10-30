# IMPORT EXTERNAL LIBRARIES #
import psycopg2 as db
import os



# VARIABLES #
DB_URL: str = os.environ.get("DATABASE_URL")



# FUNCTIONS #
def create_game_mp(players_id:list[int])-> int|None:
    """Creates the game by adding {board}, {player_id}, if succesfull returns game_id """
    conn = None
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("""
            INSERT INTO games (players_id, board)
            VALUES (%s, %s)
            RETURNING game_id
        """, (players_id, board))

        game_id = run.fetchone()[0]
        conn.commit()

        return game_id

    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def delete_game_mp(game_id:int)->bool | None:
    """Deletes the game with the {game_id}, returns true if succesfull"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("DELETE FROM games WHERE game_id = (%s) ", (game_id,))
        rows = run.rowcount

        conn.commit()
        
        
        if rows == 1:
            return True
        else:
            return False
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush= True)
        return None
    finally:
        if conn:
            conn.close()

def get_board(game_id:int)->list[int]|None:
    """Gets the board using {game_id}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("SELECT board FROM games WHERE game_id = (%s)", (game_id,))
        actual_board = run.fetchone()
        
        if actual_board is None or actual_board[0] is None:
            return None

        return actual_board[0]
    except Exception as e:
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def get_player_turn(game_id:int)->bool|None:
    """Gets the player turn using {game_id}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("SELECT first_player_turn FROM games WHERE game_id = (%s)", (game_id,))
        actual_board = run.fetchone()

        return actual_board
    except Exception as e:
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def set_player_turn(first_player_turn:bool, game_id:int)->bool|None:
    """Modifies the {first_player_turn} returns true if succesfull"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("UPDATE games SET first_player_turn = %s WHERE game_id = %s ", (first_player_turn, game_id))
        rows = run.rowcount
        conn.commit()

        
        if rows == 1:
            return True
        else:
            return False
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def get_game_results(game_id:int)->list[()]|None:
    """Gets the game results using {game_id}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("SELECT game_ended, first_player_won FROM games WHERE game_id = (%s)", (game_id,))
        actual_board = run.fetchall()

        if actual_board[0] is None:
            return None
        if actual_board[0][0] is None:
            return None
        else:
            return actual_board[0]
    except Exception as e:
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def turn_ended_mp(board:list[list[int]], first_player_turn:bool, game_ended:bool, first_player_won:bool, game_id:int)->bool|None:
    """Modifies the {board}, {first_player_turn}, {game_ended}, {first_player_won} returns true if succesfull"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("UPDATE games SET board = %s, first_player_turn = %s, game_ended = %s, first_player_won = %s WHERE game_id = %s ", (board, first_player_turn, game_ended, first_player_won, game_id))
        rows = run.rowcount
        conn.commit()

        
        if rows == 1:
            return True
        else:
            return False
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def set_player_multiplayer_state_with_id(player_id:int, multiplayer_state:bool)->bool|None:
    """Modifies the {playing_multiplayer_game} returns true if succesfull"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("UPDATE users SET playing_multiplayer_game = %s WHERE pk_user_id = %s ", (multiplayer_state, player_id))
        rows = run.rowcount
        conn.commit()

        
        if rows == 1:
            return True
        else:
            return False
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def get_user_multiplayer_state(user_id: str)-> bool | None:
    """Get the {playing_multiplayer_game}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute(
        """SELECT playing_multiplayer_game FROM users WHERE pk_user_id = %s""", (user_id,)
        )
        multiplayer_state = run.fetchone()
        conn.commit()

        if multiplayer_state is None:
            return []
        
      
        return multiplayer_state[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def get_players_id_from_mp()-> list[()] | None:
    """Get all the {players_id}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute(
        """SELECT players_id, game_id FROM games"""
        )
        players_id = run.fetchall()
        conn.commit()

        if players_id is None:
            return None
        
      
        return players_id
    except Exception as e:
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()