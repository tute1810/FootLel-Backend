# IMPORT EXTERNAL LIBRARIES #
import psycopg2 as db
import os



# VARIABLES #
DB_URL: str = "postgresql://footlel_db_f0iu_user:HApPoL4jEAIJsvxd6F7IwXW7NjzUeBoa@dpg-db8kuetg1s2s73ak7q30-a.oregon-postgres.render.com/Footlet"



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
        actual_board = run.fetchall()
        conn.commit()

        if actual_board[0] is None:
            return None
        if actual_board[0][0] is None:
            return []
        else:
            return actual_board
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def turn_ended_mp(board:list[int], first_player_turn:bool, game_ended:bool, first_player_won:bool, game_id:int)->bool|None:
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