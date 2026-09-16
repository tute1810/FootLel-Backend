import psycopg2 as db

local_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a.oregon-postgres.render.com/footlel_db"
deployed_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a/footlel_db"
current_db_url = local_db_url



def get_users_info():
    """Get users info"""
    conn = db.connect(current_db_url)
    run = conn.cursor()
    
    run.execute("SELECT * FROM users", )
    players = run.fetchall()
    
    conn.commit()
    return players

def get_user_password_with_user_name(user_name: str):
    """Get user password with: user_name: str"""
    conn = db.connect(current_db_url)
    run = conn.cursor()
    
    run.execute("SELECT password_user FROM users WHERE user_name = (%s) AND eliminated_user = false", (user_name,))
    players = run.fetchall()
    
    conn.commit()
    if players == None:
        conn.rollback()
    return players