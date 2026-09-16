import psycopg2 as db


# vars
local_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a.oregon-postgres.render.com/footlel_db"
deployed_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a/footlel_db"
current_db_url = local_db_url


# Connect to the footlet database

def get_user_password_with_user_name(user_name: str):
    """Get user password with: user_name: str"""
    conn = db.connect(current_db_url)
    run = conn.cursor()
    
    run.execute("SELECT password_user FROM users WHERE user_name = (%s)", (user_name,))
    players = run.fetchall()
    
    conn.commit()
    if players == None:
        conn.rollback()
    return players

def register_new_user(user_name: str, email: str, password_user: str):
    """Sets new user with: user_name: str, email: str, password_user: str"""
    conn = db.connect(current_db_url)
    run = conn.cursor()
       
    try:
        
        run.execute("INSERT INTO users (user_name, email, password_user) VALUES (%s,%s,%s) ", (user_name, email, password_user))
        conn.commit()
    
    except db.errors.UniqueViolation:
        
        conn.rollback()
        
        return 'Usuario ya existente'
    return 'Usuario creado'
        
        
    
    
    
    
    
    
    

