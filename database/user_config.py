# IMPORT EXTERNAL LIBRARIES #
import psycopg2 as db
import os



# VARIABLES #
DB_URL: str = os.environ.get("DATABASE_URL")



# FUNCTIONS #
def set_animations_config_state(user_id: int, state: bool)-> bool | None:
    """ set {user_animations} to the correct value and returns true if it was succesfull"""
    conn = None 
    try:    
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        not_state = not state
        
        run.execute("""UPDATE user_configuration SET user_animations = %s WHERE pk_user_id = (%s) AND user_animations = %s""", (state,user_id,not_state) )

        row = run.rowcount
        conn.commit()
       
        if row == 1:
            return True
        else:
           return False
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush = true)
        return None
    finally:
        if conn:
            conn.close()

def set_dark_mode_config_state(user_id: int, state: bool)-> bool | None:
    """ set {user_dark_mode} to the correct value and returns true if it was succesfull"""
    conn = None 
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        not_state = not state
        
        run.execute("""UPDATE user_configuration SET user_dark_mode = %s WHERE pk_user_id = (%s) AND user_dark_mode = %s""", (state, user_id, not_state) )
        
        row = run.rowcount
        conn.commit()
        if row == 1:
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

def set_compatibility_config_status(user_id: int, state: bool)-> bool | None:
    """set {user_compatibility} to its correct value, returns true if succesfull"""
    conn = None 
    try:
        
        
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        not_state = not state
        
        
        run.execute("""UPDATE user_configuration SET user_compatibility = %s WHERE pk_user_id = %s AND user_compatibility = %s""", (state, user_id, not_state) )
        
    
        row = run.rowcount
        conn.commit()
        if row == 1:
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
            
def get_compatibility_config_status(user_id:int)-> bool | None:
    """get {user_compatibility} value in form of a string using user_id"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
            
        run.execute("SELECT user_compatibility FROM user_configuration WHERE pk_user_id = (%s)", (user_id,) )
        status = run.fetchone()

        if status is None:
            return None
        
        conn.close()
        return status[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush = True)
        return None
    finally:
        if conn:
            conn.close()
def get_dark_mode_config_state(user_id:int)-> bool | None:
    """get {user_dark_mode status} in form of a string using user_id"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
            
        run.execute("SELECT user_dark_mode FROM user_configuration WHERE pk_user_id = (%s)", (user_id,) )
        status = run.fetchone()
      

        if status is None:
            return None
        
        conn.close()
        return status[0]
    except Exception as e:
        if conn:
            conn.rollback
        print(e, flush = True)
        return None
    finally:
        if conn:
            conn.close()

def get_animations_config_state(user_id: int)-> bool | None:
    """get user_animations status in form of a string using user_id"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
            
        run.execute("SELECT user_animations FROM user_configuration WHERE pk_user_id = (%s)", (user_id,) )
        status = run.fetchone()
        

        if status is None:
            
            return None
        
        
        return status[0]
    except Exception as e:
        if conn:
            conn.rollback
        print(e, flush = True)
        return None
    finally:
        if conn:
            conn.close()