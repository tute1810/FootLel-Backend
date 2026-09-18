import psycopg2 as db

local_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a.oregon-postgres.render.com/footlel_db"
deployed_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a/footlel_db"
current_db_url = deployed_db_url

def get_user_name(user_id: int):
    """Get user_name in form of a string using user_id"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
            
        run.execute("SELECT user_name FROM users WHERE pk_user_id = (%s) AND user_eliminated = false", (user_id,) )
        user_name = run.fetchone()
        conn.commit()

        if user_name is None:
            conn.rollback()
            conn.close()
            return None
        
        conn.close()
        return user_name[0] 
    except:        
        conn.rollback()
        conn.close()
        return None

def get_user_password_with_user_name(user_name: str):
    """Get user password with: user_name: str in form of a string or None if the user doesnt exist or is deactivated"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute("SELECT user_password FROM users WHERE user_name = (%s) AND user_eliminated = false", (user_name,))
        user_password = run.fetchone()
        conn.commit()

        if user_password is None:
            conn.rollback()
            conn.close()
            return None
        
        conn.close()
        return user_password[0]
    
        
    except:   
        conn.rollback()
        conn.close()
        return None

def get_user_id(user_email: str):
    """Get active user id with user_email: str"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute(
        """SELECT pk_user_id FROM users WHERE (user_email = %s) AND user_eliminated = FALSE""", (user_email,)
        )
        user_id = run.fetchone()
        conn.commit()

        if user_id is None:
            conn.rollback()
            conn.close()
            return None
        
        conn.close()
        return user_id[0]
    except Exception as e:
        print(e)
        return None

def eliminate_user(user_id: int):
    """Eliminates user with: user_id: int"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
            
        run.execute("UPDATE users SET user_eliminated = TRUE WHERE pk_user_id = (%s) ", (user_id,))
        conn.commit()

        conn.close()
        return True
    except:
        conn.rollback()
        conn.close()
        return False

def change_password(user_id: int, user_password: str):
    """Change passowrd from active user with user_id: int and user_password: str """
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute(""" UPDATE users SET user_password = (%s) WHERE pk_user_id = (%s)""", (user_password,user_id ))
        conn.commit()

        conn.close()
        return True
    except:
        conn.rollback()
        conn.close()
        return False

def change_user_data(user_id:int, user_name: str, user_email: str, user_password: str):
    """Change the user user_email, user_name and the user_password with user_name:str, user_email, user_password using user_id)"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute(""" UPDATE users SET user_name = %s, user_email = %s, user_password = %s  WHERE pk_user_id = (%s) """, (user_name, user_email, user_password, user_id))
        conn.commit()

        conn.close()
        return True    
    except:
        conn.rollback() 
        conn.close()  
        return False