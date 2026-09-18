import psycopg2 as db

local_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a.oregon-postgres.render.com/footlel_db"
deployed_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a/footlel_db"
current_db_url = deployed_db_url



def is_user_name_available(user_name: str):
    """check if the user name is available to use"""
    try:
        conn = db.connect(current_db_url)
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
    except:
        conn.close()
        return False

def is_user_email_available(user_email: str):
    """Check if the user email is available to use"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute("""SELECT 1 FROM users WHERE user_email = (%s) AND user_eliminated = FALSE""",(user_email,))
        check_user_email = run.fetchone()
        conn.commit()

        if check_user_email is not None:
            conn.rollback()
            return False

        conn.close()
        return True
    except: 
        conn.close()
        return False
    
def register_new_user(user_name: str, user_email: str, user_password: str):
    """Sets new user with: user_name: str, user_email: str, user_password: str"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()

        run.execute(
            "SELECT COALESCE(MAX(pk_user_id), 0) + 1 FROM users"
        )
        user_id = run.fetchone()[0]
            
        run.execute(
            """
            INSERT INTO users
            (pk_user_id, user_name, user_email, user_password, user_eliminated)
            VALUES (%s, %s, %s, %s, false)
            """,
            (user_id, user_name, user_email, user_password)
        )
            
        run.execute(""" INSERT INTO user_configuration (pk_user_id) VALUES (%s)""", (user_id,))
        run.execute(""" INSERT INTO user_stats (pk_user_id) VALUES (%s)""", (user_id,))
        conn.commit()
        
        conn.close()
        return True
    except:
        conn.rollback()
        conn.close()
        return False