# IMPORT EXTERNAL LIBRARIES #
import psycopg2 as db
import os



# VARIABLES #
DB_URL: str = os.environ.get("DATABASE_URL")



# FUNCTIONS #
def set_animations_config_state(user_id: int, state: bool):
    """ set user animation with user_id: int and state"""
    conn = None 
    try:    
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        not_state = not state
        
        run.execute("""UPDATE user_configuration SET user_animations = %s WHERE pk_user_id = (%s) AND user_animations = %s""", (state,user_id,not_state) )


        conn.commit()
        return True
    
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
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        not_state = not state
        
        run.execute("""UPDATE user_configuration SET user_dark_mode = %s WHERE pk_user_id = (%s) AND user_dark_mode = %s""", (state, user_id, not_state) )
        

        conn.commit()
        return True
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
        
        
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        not_state = not state
        
        
        run.execute("""UPDATE user_configuration SET user_compatibility = %s WHERE pk_user_id = %s AND user_compatibility = %s""", (state, user_id, not_state) )
        
        conn.commit()
        return True
    
    except Exception as e:
        print(e, flush=True)
        return False
    finally:
        if conn:
            conn.close()
            
def get_compatibility_config_status(user_id:int):
    """get user compatibility status in form of a string using user_id"""
    try:
        conn = db.connect(DB_URL)
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
        print(e)
        return None

def get_dark_mode_config_state(user_id:int):
    """get user dark mode status in form of a string using user_id"""
    try:
        conn = db.connect(DB_URL)
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
        print(e)
        return None

def get_animations_config_state(user_id: int):
    """get user animations status in form of a string using user_id"""
    try:
        conn = db.connect(DB_URL)
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
        print(e)
        return None