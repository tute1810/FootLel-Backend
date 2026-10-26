import psycopg2 as db
import os
from datetime import date

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
    """get user stats in this order: user_points, guesses_made, correct_guesses, matches_played, matches_won, win_streak as a tuple"""
    
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
            
def get_global_leaderboard():
    """get the global rankings in form of a list[tuple[str, int]]"""

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

def set_user_daily_challenge_with_user_id(user_id: int, daily_challenge:bool):
    """Set the daily challenge state with the user_id and a bool returns True or False"""
    conn = None
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute("""UPDATE user_stats SET daily_challenge = (%s) WHERE pk_user_id = (%s)""", (daily_challenge, user_id) )
        
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



def get_user_daily_challenge_state_with_id(user_id: int):
    """Get active user id with user_email: str"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute(
        """SELECT daily_challenge FROM user_stats WHERE (pk_user_id = %s)""", (user_id,)
        )
        daily_challenge = run.fetchone()
        conn.commit()

        if daily_challenge is None:
            conn.rollback()
            conn.close()
            return None
        
        conn.close()
        return daily_challenge[0]
    except Exception as e:
        print(e, flush=True)
        return None
    
def set_current_date(current_date:str):
    """Set the current date"""
    conn = None
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute("""UPDATE backend_staff SET current_day = (%s)""", (current_date, ) )
        
        conn.commit()

        conn.close()
        return True
    
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return False
    finally:
        if conn:
            conn.close()

def get_current_date():
    """Gets the current date as a string"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute(
        """SELECT current_day FROM backend_staff""",
        )
        current_date = run.fetchone()
        conn.commit()

        if current_date is None:
            conn.rollback()
            conn.close()
            return ""
        
        conn.close()
        return current_date[0]
    except Exception as e:
        print(e, flush=True)
        return None


def reset_daily_challenge_state_to_all_users():
    """Set the daily challenge state to False"""
    conn = None
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute("""UPDATE user_stats SET daily_challenge = (%s)""", (False,) )
        
        rows = run.rowcount
        conn.commit()

        conn.close()
        if rows >= 1:
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
