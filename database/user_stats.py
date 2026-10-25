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
    """Get the global rankings in form of a list[list[str, int]]"""

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