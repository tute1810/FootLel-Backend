import psycopg2 as db

# Connect to the footlet database

def show_players(jugadores):
    conn = db.connect("postgresql://neondb_owner:npg_nh35ETOQdHJL@ep-quiet-night-b4won4nr-pooler.c-6.us-east-2.aws.neon.tech/FootLel_db?sslmode=require&channel_binding=require")
    run = conn.cursor()
    
    run.execute("SELECT * FROM players WHERE premier_league ILIKE '%Manchester United%'")
    players = run.fetchall()
    print(players)
    
#show_players()

def login(user_name: str):
    conn = db.connect("postgresql://neondb_owner:npg_nh35ETOQdHJL@ep-quiet-night-b4won4nr-pooler.c-6.us-east-2.aws.neon.tech/FootLel_db?sslmode=require&channel_binding=require")
    run = conn.cursor()
    
    run.execute("SELECT password_user FROM users WHERE username = (%s)", (user_name,))
    players = run.fetchall()
    
    conn.commit()
    if players == None:
        conn.rollback()
    return players

def register(user_name: str, email: str, password_user: str):
    conn = db.connect("postgresql://neondb_owner:npg_nh35ETOQdHJL@ep-quiet-night-b4won4nr-pooler.c-6.us-east-2.aws.neon.tech/FootLel_db?sslmode=require&channel_binding=require")
    run = conn.cursor()
       
    try:
        
        run.execute("INSERT INTO users (username, email, password_user) VALUES (%s,%s,%s) ", (user_name, email, password_user))
        conn.commit()
    
    except db.errors.UniqueViolation:
        
        conn.rollback()
        
        return 'Usuario ya existente'
    return 'Usuario creado'
        
        
    
    
    
    
    
    
    
