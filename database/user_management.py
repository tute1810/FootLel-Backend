import psycopg2 as db

deployed_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a.oregon-postgres.render.com/footlel_db"
local_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a/footlel_db"
current_db_url = deployed_db_url



def get_users_table():
    """Get users table"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()

        run.execute("SELECT * FROM users",)
        users = run.fetchall()
        conn.commit()

        conn.close()
        return users
    except Exception as e:
        print(e)
        return None

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
    except Exception as e:
        print(e)
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
    except Exception as e:
        print(e)
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
    conn = None
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()

        run.execute("UPDATE users SET user_eliminated = true WHERE pk_user_id = (%s) AND user_eliminated = false ", (user_id,))
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

def change_password(user_id: int, user_password: str):
    """Change passowrd from active user with user_id: int and user_password: str """
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        run.execute(""" UPDATE users SET user_password = (%s) WHERE pk_user_id = (%s)""", (user_password,user_id ))
        conn.commit()

        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def change_user_data(user_id:int, user_name: str, user_email: str, user_password: str):
    """Change the user user_email, user_name and the user_password with user_name:str, user_email, user_password using user_id)"""
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        data_to_update: list[str] = []
        if user_name != "":
            data_to_update.append( "user_name = \'" + user_name + "\'")
        if user_email != "":
            data_to_update.append( "user_email = \'" + user_email + "\'")
        if user_password != "":
            data_to_update.append( "user_password = \'" + user_password + "\'")
        
        if len(data_to_update) == 0:
            conn.close()
            return False

        string: str = "SET "
        for i in range(0, len(data_to_update), 1):
            string += data_to_update[i] + ", "

        string = string.strip(", ")

        run.execute(f""" UPDATE users {string} WHERE pk_user_id = (%s) """, (user_id,))
        conn.commit()

        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def get_user_info(user_name: str):
    """Get user_email and user_id with user_name"""
    conn = None
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()

        run.execute("SELECT pk_user_id, user_email FROM users WHERE user_name = (%s) AND user_eliminated = false", (user_name,) )
        user_id_email = run.fetchall()
        conn.commit()

        if user_id_email == []:
            conn.rollback()
            conn.close()
            return None

        conn.close()
        return user_id_email[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e)
        return None
    finally:
        if conn:
            conn.close()

def change_user_data(user_id:int, user_name: str, user_email: str, user_password: str):
    """Change the user user_email, user_name and the user_password with user_name:str, user_email, user_password using user_id)"""
    conn = None
    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()

        run.execute(""" UPDATE users SET user_name = %s, user_email = %s, user_password = %s  WHERE pk_user_id = (%s)  AND user_eliminated = false """, (user_name, user_email, user_password, user_id))
        conn.commit()
        
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        if conn:
            conn.close()