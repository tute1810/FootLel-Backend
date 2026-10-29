# IMPORT EXTERNAL LIBRARIES #
import psycopg2 as db
import os



# VARIABLES #
DB_URL: str = os.environ.get("DATABASE_URL")



# FUNCTIONS #
def get_users_table():
    """Get users table, returns a list of tuples"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("SELECT * FROM users",)
        users = run.fetchall()
        conn.commit()

        
        return users
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def get_user_name(user_id: int):
    """get user_name in form of a string using user_id"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
            
        run.execute("SELECT user_name FROM users WHERE pk_user_id = (%s) AND user_eliminated = false", (user_id,) )
        user_name = run.fetchone()

        if user_name is None:
            return None
        else:
            return user_name[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def get_user_password_with_user_name(user_name: str):
    """Get user password with: user_name: str in form of a string or None if the user doesnt exist or is deactivated"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("SELECT user_password FROM users WHERE user_name = (%s) AND user_eliminated = false", (user_name,))
        user_password = run.fetchone()
        conn.commit()

        if user_password is None:
            return ""
        
        return user_password[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def get_user_password_with_user_id(user_id: int):
    """get user password with user id"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute("SELECT user_password FROM users WHERE pk_user_id = (%s) AND user_eliminated = false", (user_id,))
        user_password = run.fetchone()
        conn.commit()

        if user_password is None:
            return ""
        
        
        return user_password[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def get_user_id_with_user_name(user_name: str):
    """Get active user id with user_name: str"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute(
        """SELECT pk_user_id FROM users WHERE (user_name = %s) AND user_eliminated = FALSE""", (user_name,)
        )
        user_id = run.fetchone()
        conn.commit()

        if user_id is None:
            return None
        
        return user_id[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def get_user_id(user_email: str):
    """Get active user id with user_email: str"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute(
        """SELECT pk_user_id FROM users WHERE (user_email = %s) AND user_eliminated = FALSE""", (user_email,)
        )
        user_id = run.fetchone()
        conn.commit()

        if user_id is None:
            return -1
        

        return user_id[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def eliminate_user(user_id: int):
    """Eliminates user with: user_id: int"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("UPDATE users SET user_eliminated = true WHERE pk_user_id = (%s) AND user_eliminated = false ", (user_id,))
        rows = run.rowcount
        run.execute("DELETE FROM friends WHERE pk_user_id = %s", (user_id,))
        run.execute("DELETE FROM user_configuration WHERE pk_user_id = %s", (user_id,))
        run.execute("DELETE FROM user_stats WHERE pk_user_id = %s", (user_id,))
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

def change_password(user_id: int, user_password: str):
    """Change passowrd from active user with user_id: int and user_password: str """
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute(""" UPDATE users SET user_password = (%s) WHERE pk_user_id = (%s)""", (user_password,user_id ))
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

def change_user_data(user_id:int, user_name: str, user_email: str, user_password: str):
    """Change the user user_email, user_name and the user_password with user_name:str, user_email, user_password using user_id)"""
    try:
        conn = db.connect(DB_URL)
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
            return True

        string: str = "SET "
        for i in range(0, len(data_to_update), 1):
            string += data_to_update[i] + ", "

        string = string.strip(", ")

        run.execute(f""" UPDATE users {string} WHERE pk_user_id = (%s) """, (user_id,))
        print(f""" UPDATE users {string} WHERE pk_user_id = (%s) """, (user_id,), flush=True)
        conn.commit()

        conn.close()
        return True
    except Exception as e:
        print(e, flush=True)
        return False

def get_user_info(user_id: int):
    """get user_name and user_email with user_id"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("SELECT user_name, user_email FROM users WHERE pk_user_id = (%s) AND user_eliminated = false", (user_id,))
        user_name_and_email = run.fetchall()
        conn.commit()

        if user_name_and_email is None:
            return []

        conn.close()
        return user_name_and_email[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()
            
def get_guest_id_with_name(guest_name: str):
    """Get active user id with user_email: str"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute(
        """SELECT pk_user_id FROM users WHERE (user_name = %s) AND is_guest = True""", (guest_name,)
        )
        guest_id = run.fetchone()
        conn.commit()

        if guest_id is None:
            return -1
        
      
        return guest_id[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def is_guest_with_user_id(user_id:int):    
    """Get guest status with user id"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        run.execute(
        """SELECT is_guest FROM users WHERE (pk_user_id = %s)""", (user_id,)
        )
        is_guest = run.fetchone()[0]
        conn.commit()

        if is_guest is None:
            return []
        
        
        return is_guest
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def get_user_friends(user_id:int):
    """get user friends, returns a list ids"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("SELECT friends_id FROM friends WHERE pk_user_id = %s", (user_id,))
        friends = run.fetchall()
       
        
        if friends[0] is None:
            return None
        if friends[0][0] is None:
            return []
        else:
            return friends[0][0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()
    
def add_user_friend(user_id:int, friend_id:int):
    """add user friend"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("UPDATE friends SET friends_id = array_append( COALESCE(friends_id, ARRAY[]::INTEGER[]),%s) WHERE pk_user_id = %s AND NOT (%s = ANY( COALESCE(friends_id, ARRAY[]::INTEGER[])))  ", (friend_id, user_id, friend_id))
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
            
def delete_one_user_friend(user_id:int, friend_id:int):
    """Deletes one friend from the user with the ids"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("UPDATE friends SET friends_id = array_remove(friends_id, %s) WHERE pk_user_id = %s ", (friend_id, user_id))
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

def get_user_friend_request(user_id:int):
    """get user friends request, returns a list ids"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("SELECT friend_request FROM friends WHERE pk_user_id = %s", (user_id,))
        friends = run.fetchall()
        
        
        if friends[0] is None:
            return None
        if friends[0][0] is None:
            return []
        else:
            return friends[0][0]    
    except Exception as e:
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def add_user_friend_request(user_id:int, friend_id:int):
    """add user friend request"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("UPDATE friends SET friend_request = array_append( COALESCE(friend_request, ARRAY[]::INTEGER[]),%s) WHERE pk_user_id = %s AND NOT (%s = ANY( COALESCE(friend_request, ARRAY[]::INTEGER[])))  ", (friend_id, user_id, friend_id))
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

def delete_one_user_friend_request(user_id:int, friend_id:int):
    """Deletes one request from the user with the ids"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("UPDATE friends SET friend_request = array_remove(friend_request, %s) WHERE pk_user_id = %s ", (friend_id, user_id))
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

def get_user_match_request(user_id:int):
    """get user friends match requests, returns a list ids"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("SELECT match_request FROM friends WHERE pk_user_id = %s", (user_id,))
        friends = run.fetchall()
        
        
        if friends[0] is None:
            return None
        if friends[0][0] is None:
            return []
        else:
            return friends[0][0]
    except Exception as e:
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()


def add_user_match_request(user_id:int, friend_id:int):
    """add user friend match request"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("UPDATE friends SET match_request = array_append( COALESCE(match_request, ARRAY[]::INTEGER[]),%s) WHERE pk_user_id = %s AND NOT (%s = ANY( COALESCE(match_request, ARRAY[]::INTEGER[])))  ", (friend_id, user_id, friend_id))
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

def delete_one_user_match_request(user_id:int, friend_id:int):
    """Deletes one match request from the user with the ids"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()

        run.execute("UPDATE friends SET match_request = array_remove(match_request, %s) WHERE pk_user_id = %s ", (friend_id, user_id))
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