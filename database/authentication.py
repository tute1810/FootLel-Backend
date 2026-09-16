import psycopg2 as db

local_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a.oregon-postgres.render.com/footlel_db"
deployed_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a/footlel_db"
current_db_url = local_db_url




def register_new_user(user_name: str, email: str, password_user: str):
    """Sets new user with: user_name: str, email: str, password_user: str"""
    conn = db.connect(current_db_url)
    run = conn.cursor()
       
    try:
        # Comprobar nombre o email en usuarios activos
        run.execute(
            """
            SELECT 1
            FROM users
            WHERE (user_name = %s OR email = %s)
              AND eliminated_user = FALSE
            """,
            (user_name, email)
        )

        if run.fetchone() is not None:
            conn.rollback()
            return 'Usuario ya existente'

        # Obtener siguiente ID
        run.execute(
            "SELECT COALESCE(MAX(pk_user_id), 0) + 1 FROM users"
        )
        id_user = run.fetchone()[0]
        
        run.execute(
            """
            INSERT INTO users
            (pk_user_id, user_name, email, password_user, eliminated_user)
            VALUES (%s, %s, %s, %s, FALSE)
            """,
            (id_user, user_name, email, password_user)
        )

        conn.commit()
        return 'Usuario creado'

    except Exception:
        conn.rollback()
        raise


def eliminate_user(id_user: int):
    """Eliminates user with: user_id: int"""
    conn = db.connect(current_db_url)
    run = conn.cursor()
        
    run.execute("UPDATE users SET eliminated_user = TRUE WHERE pk_user_id = (%s) ", (id_user,))
    conn.commit()