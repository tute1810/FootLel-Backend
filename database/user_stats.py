import psycopg2 as db
from psycopg2 import sql
local_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a.oregon-postgres.render.com/footlel_db"
deployed_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a/footlel_db"
current_db_url = local_db_url



def set_user_matches_stats(matches_played: int, matches_won: int, matches_lost: int, user_id: int, points: int):
    
    """Set matches played, won and lost by the user id"""
    conn = None
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        
        
        run.execute("""UPDATE user_stats SET matches_played = (%s), matches_won = (%s), matches_lost = (%s), user_points = (%s) FROM users WHERE users.pk_user_id = (%s) AND user_stats.pk_user_id = %s AND users.user_eliminated = false""", (matches_played, matches_won, matches_lost, points, user_id, user_id) )
        rows = run.rowcount
        conn.commit()

        conn.close()
        if rows == 1:
            return True
        else:
           return False
    
    except Exception as e:
        print(e)
        return False
    finally:
        if conn:
            conn.close()
            
            
def set_user_guesses_stats(guesses_made: int, correct_guesses: int, user_id: int):
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
        
        print(e)
        return False
    finally:
        if conn:
            conn.close()
            
def set_user_win_streak(win_streak: int, user_id: int):
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
        print(e)
        return False
    finally:
        if conn:
            conn.close()
    

def get_user_stats(user_id: int):
    """get user stats in this order: guesses_made, correct_guesses, matches_played, matches_won, matches_lost, win_streak, user_points"""
    
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
        matches_lost,
        win_streak
        FROM user_stats
        WHERE pk_user_id = (%s)""", (user_id,))
        
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
        print(e)
        return None
    finally:
        if conn:
            conn.close()
            
            
def get_table_ranking():
    """Get the global rankings"""

    conn = None
    try:
        
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute("""
        SELECT
        user_stats.user_points,
        users.user_name
        FROM user_stats
        JOIN users
        ON user_stats.pk_user_id = users.pk_user_id
        WHERE users.user_eliminated = FALSE
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
        print(e)
        return None
    finally:
        if conn:
            conn.close()