# IMPORT EXTERNAL LIBRARIES #
import psycopg2 as db
import os



# VARIABLES #
DB_URL: str = os.environ.get("DATABASE_URL")



# FUNCTIONS #
def is_user_name_available(user_name: str):
    """check if the user name is available to use"""
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
           
        run.execute("""SELECT 1 FROM users WHERE user_name = (%s) AND user_eliminated = FALSE""",(user_name,))
        check_user_name = run.fetchone()
        conn.commit()

        if check_user_name is not None:
            conn.rollback()
            conn.close()
            return False
            
        conn.close()
        return True
    except Exception as e:
        print(e, flush=True)
        return None

def is_user_email_available(user_email: str):
    """Check if the user email is available to use"""
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("""SELECT 1 FROM users WHERE user_email = (%s) AND user_eliminated = FALSE""",(user_email,))
        check_user_email = run.fetchone()
        conn.commit()

        if check_user_email is not None:
            conn.rollback()
            return False

        conn.close()
        return True
    except Exception as e:
        print(e, flush=True)
        return False

def is_user_name_used_by_another_user(user_id: int, user_name: str):
    """get wether the user name is already used or not by another user excluding the user with using user_id"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("SELECT user_name FROM users WHERE pk_user_id != %s AND user_name = %s AND user_eliminated = false", (user_id,user_name))
        user_name = run.fetchone()
        conn.commit()

        if user_name is None:
            conn.rollback()
            conn.close()
            return False

        conn.close()
        return True
    except Exception as e:
        print(e, flush=True)
        return None
    finally :
        if conn:
            conn.close()

def is_user_email_used_by_another_user(user_id: int, user_email: str):
    """get wether the user email is already used or not by another user excluding the user with using user_id"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("SELECT user_email FROM users WHERE pk_user_id != %s AND user_email = %s AND user_eliminated = false", (user_id,user_email) )
        user_email = run.fetchone()
        conn.commit()

        if user_email is None:
            conn.rollback()
            conn.close()
            return False

        conn.close()
        return True
    except Exception as e:
        print(e, flush=True)
        return None
    finally :
        if conn:
            conn.close()

def register_new_user(user_name: str, user_email: str, user_password: str):
    """Sets new user with: user_name: str, user_email: str, user_password: str"""
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute(
            """
            INSERT INTO users
            (user_name, user_email, user_password, user_eliminated)
            VALUES (%s, %s, %s, false)
            RETURNING pk_user_id;
            """,
            (user_name, user_email, user_password)
        )
        user_id = run.fetchone()[0]

        run.execute(""" INSERT INTO user_configuration (pk_user_id) VALUES (%s)""", (user_id,))
        run.execute(""" INSERT INTO user_stats (pk_user_id, win_streak, user_points) VALUES (%s,0,0)""", (user_id,))
        run.execute(""" INSERT INTO friends (pk_user_id)  VALUES (%s)""", (user_id,))
        conn.commit()

        conn.close()
        return True
    except Exception as e:
        print(e, flush=True)
        return False

def register_guest(user_name: str):
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        
        run.execute(
            """
            INSERT INTO users
            (user_name, is_guest, user_email, user_password)
            VALUES (%s, True, %s, %s)
            """,
            (user_name,user_name, f"")
        )
        
        conn.commit()

        conn.close()
        return True
    except Exception as e:
        print(e, flush=True)
        return False