# IMPORT EXTERNAL LIBRARIES #
import psycopg2 as db
import os



# VARIABLES #
DB_URL: str = os.environ.get("DATABASE_URL")



# FUNCTIONS #
def set_user_matches_stats(user_id: int, matches_played: int, matches_won: int, user_points: int) -> bool | None:
    """sets user's match stats in the following order: {matches_player}, {matches_won}, {user_points} with {user_id}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("""UPDATE user_stats SET matches_played = (%s), matches_won = (%s), user_points = (%s) FROM users WHERE users.pk_user_id = (%s) AND user_stats.pk_user_id = %s AND users.user_eliminated = false""", (matches_played, matches_won, user_points, user_id, user_id) )
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

def set_user_guesses_stats(user_id: int, guesses_made: int, correct_guesses: int) -> bool | None:
    """sets user's guess stats in the following order: {guesses_made}, {correct_guesses} with {user_id}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("""UPDATE user_stats SET guesses_made = (%s), correct_guesses = (%s) FROM users WHERE users.pk_user_id = (%s) AND user_stats.pk_user_id = %s AND users.user_eliminated = false""", (guesses_made, correct_guesses, user_id, user_id))
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

def set_user_win_streak(user_id: int, win_streak: int) -> bool | None:
    """sets user's win stats in the following order: {win_streak} with {user_id}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("""UPDATE user_stats SET win_streak = (%s) FROM users WHERE users.pk_user_id = (%s) AND user_stats.pk_user_id = %s AND users.user_eliminated = FALSE""", (win_streak, user_id, user_id))
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

def get_user_stats(user_id: int) -> tuple | None:
    """sets user's win stats in the following order: (user_points, guesses_made, correct_guesses, matches_played, matches_won, win_streak) with {user_id} as a tuple"""
    conn = None
    try:
        
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("""SELECT
        user_points,
        guesses_made,
        correct_guesses,
        matches_played,
        matches_won,
        win_streak
        FROM user_stats WHERE pk_user_id = (%s)""", (user_id,))
        stats = run.fetchall()
        
        if stats == [] or all(value is None for value in stats[0]):
            return []
        else:
            return stats[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()
            
def get_global_leaderboard() -> list[tuple] | None:
    """gets the global ranking table as a list of tuples containing (user_name, user_points)"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("""SELECT
        users.user_name,
        user_stats.user_points
        FROM user_stats JOIN users ON user_stats.pk_user_id = users.pk_user_id WHERE users.user_eliminated = false ORDER BY user_stats.user_points DESC""")
        ranking = run.fetchall()
        
        if ranking == [] or all(value is None for value in ranking[0]):
            return []
        else:
            return ranking
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def set_user_daily_challenge_with_user_id(user_id: int, daily_challenge: bool) -> bool | None:
    """sets the user's {daily_challenge} state with the {user_id}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("""UPDATE user_stats SET daily_challenge = (%s) WHERE pk_user_id = (%s)""", (daily_challenge, user_id))
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

def get_user_daily_challenge_state_with_id(user_id: int) -> bool | None:
    """gets the user's daily_challenge state with the {user_id}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("""SELECT daily_challenge FROM user_stats WHERE (pk_user_id = %s)""", (user_id,))
        daily_challenge = run.fetchone()

        if daily_challenge is None:
            return None
        else:
            return daily_challenge[0]
    except Exception as e:
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()
    
def set_current_date(current_date: str) -> bool | None:
    """sets the {current_date}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("""UPDATE backend_staff SET current_day = (%s)""", (current_date, ))
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

def get_current_date() -> str | None:
    """gets the current_date"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("""SELECT current_day FROM backend_staff""",)
        current_date = run.fetchone()

        if current_date is None:
            return None
        else:
            return current_date[0]
    except Exception as e:
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def reset_daily_challenge_state_to_all_users() -> bool | None:
    """sets all user's daily_challenge state to false"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("""UPDATE user_stats SET daily_challenge = (%s)""", (False,) )
        rows = run.rowcount
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()