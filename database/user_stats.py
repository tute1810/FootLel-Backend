import psycopg2 as db
import os

deployed_db_url = os.environ.get("DATABASE_URL")

current_db_url = deployed_db_url

def set_user_matches_stats(user_id: int, matches_played: int, matches_won: int, points: int):
    
    """Set matches played, won and lost by the user id"""
    conn = None
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute("""UPDATE user_stats SET matches_played = (%s), matches_won = (%s), user_points = (%s) FROM users WHERE users.pk_user_id = (%s) AND user_stats.pk_user_id = %s AND users.user_eliminated = false""", (matches_played, matches_won, points, user_id, user_id) )
        rows = run.rowcount
        conn.commit()

        conn.close()
        if rows == 1:
            return True
        else:
           return False
    
    except Exception as e:
        print(e, flush=True)
        return False
    finally:
        if conn:
            conn.close()

def set_user_guesses_stats(user_id: int, guesses_made: int, correct_guesses: int):
    """Set guesses stats, with the amount of guesses made and the correct ones by the user id"""
    conn = None
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute("""UPDATE user_stats SET guesses_made = (%s), correct_guesses = (%s) FROM users WHERE users.pk_user_id = (%s) AND user_stats.pk_user_id = %s AND users.user_eliminated = false""", (guesses_made, correct_guesses , user_id, user_id) )
        
        rows = run.rowcount
        conn.commit()

        conn.close()
        if rows == 1:
            return True
        else:
           return False
    
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return False
    finally:
        if conn:
            conn.close()

def set_user_win_streak(user_id: int, win_streak: int):
    """ Updates the amount of win streaks that the user has"""
    conn = None
    
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute("""UPDATE user_stats SET win_streak = (%s) FROM users WHERE users.pk_user_id = (%s) AND user_stats.pk_user_id = %s AND users.user_eliminated = false""", (win_streak, user_id, user_id) )
    
        rows = run.rowcount
        conn.commit()

        conn.close()
        if rows == 1:
            return True
        else:
           return False
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return False
    finally:
        if conn:
            conn.close()

def get_user_stats(user_id: int):
    """get user stats in this order: user_points, guesses_made, correct_guesses, matches_played, matches_won, win_streak"""
    
    conn = None
    try:
        
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute("""
        SELECT
        user_points,
        guesses_made,
        correct_guesses,
        matches_played,
        matches_won,
        win_streak
        FROM user_stats
        WHERE pk_user_id = (%s)""", (user_id,))
        
        stats = run.fetchall()
        
        conn.commit()
        
        if stats == []:
            conn.rollback()
            conn.close()
            return None
        conn.close()
        return stats[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()
            
def get_table_ranking():
    """Get the global rankings in form of a list of tuples"""

    conn = None
    try:
        
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute("""
        SELECT
        users.user_name,
        user_stats.user_points
        FROM user_stats
        JOIN users
        ON user_stats.pk_user_id = users.pk_user_id
        WHERE users.user_eliminated = false
        ORDER BY user_stats.user_points DESC""")
        
        ranking = run.fetchall()
        
        conn.commit()
        
        if ranking == []:
            conn.rollback()
            conn.close()
            return None
        conn.close()
        return ranking
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def set_animations_config_state(user_id: int, state: bool):
    """ set user animation with user_id: int and state"""
    conn = None 
    try:    
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        not_state = not state
        
        run.execute("""UPDATE user_configuration SET user_animations = %s WHERE pk_user_id = (%s) AND user_animations = %s""", (state,user_id,not_state) )
        
        if run.rowcount > 0:
            conn.commit()
            
            return True
        else:
            conn.rollback()
            
            return False
    
    except Exception as e:
        print(e, flush=True)
        return False
    finally:
        if conn:
            conn.close()

def set_dark_mode_config_state(user_id: int, state: bool):
    """set user dark mode with user_id: int and state"""
    conn = None 
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        not_state = not state
        
        run.execute("""UPDATE user_configuration SET user_dark_mode = %s WHERE pk_user_id = (%s) AND user_dark_mode = %s""", (state, user_id, not_state) )
        
        
        if run.rowcount > 0:
            conn.commit()
            
            return True
        else:
            conn.rollback()
            
            return False
    
    except Exception as e:
        print(e, flush=True)
        return False
    finally:
        if conn:
            conn.close()

def set_compatibility_config_status(user_id: int, state: bool):
    """set compatibility mode with user_id: int and state"""
    conn = None 
    try:
        
        
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        not_state = not state
        
        
        run.execute("""UPDATE user_configuration SET user_compatibility = %s WHERE pk_user_id = %s AND user_compatibility = %s""", (state, user_id, not_state) )
        
        
        if run.rowcount > 0:
            conn.commit()
            
            return True
        else:
            conn.rollback()
            
            return False
    
    except Exception as e:
        print(e, flush=True)
        return False
    finally:
        if conn:
            conn.close()
            
def get_compatibility_config_status(user_id:int):
    """get user compatibility status in form of a string using user_id"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
            
        run.execute("SELECT user_compatibility FROM user_configuration WHERE pk_user_id = (%s)", (user_id,) )
        status = run.fetchone()
        conn.commit()

        if status is None:
            conn.rollback()
            conn.close()
            return None
        
        conn.close()
        return status[0]
    except Exception as e:
        print(e, flush=True)
        return None

def get_dark_mode_config_state(user_id:int):
    """get user dark mode status in form of a string using user_id"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
            
        run.execute("SELECT user_dark_mode FROM user_configuration WHERE pk_user_id = (%s)", (user_id,) )
        status = run.fetchone()
        conn.commit()

        if status is None:
            conn.rollback()
            conn.close()
            return None
        
        conn.close()
        return status[0]
    except Exception as e:
        print(e, flush=True)
        return None

def get_animations_config_state(user_id: int):
    """get user animations status in form of a string using user_id"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
            
        run.execute("SELECT user_animations FROM user_configuration WHERE pk_user_id = (%s)", (user_id,) )
        status = run.fetchone()
        conn.commit()

        if status is None:
            conn.rollback()
            conn.close()
            return None
        
        conn.close()
        return status[0]
    except Exception as e:
        print(e, flush=True)
        return None