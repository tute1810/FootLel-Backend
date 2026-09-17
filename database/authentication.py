import psycopg2 as db

local_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a.oregon-postgres.render.com/footlel_db"
deployed_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a/footlel_db"
current_db_url = deployed_db_url




def register_new_user(user_name: str, user_email: str, user_password: str):
    """Sets new user with: user_name: str, user_email: str, user_password: str"""
    conn = db.connect(current_db_url)
    run = conn.cursor()
       
    try:
        # Comprobar nombre o user_email en usuarios activos
        run.execute(
            """
            SELECT 1
            FROM users
            WHERE (user_name = %s OR user_email = %s)
              AND eliminated_user = FALSE
            """,
            (user_name, user_email)
        )

        if run.fetchone() is not None:
            conn.rollback()
            conn.close()
            return 'Usuario ya existente'

        # Obtener siguiente ID
        run.execute(
            "SELECT COALESCE(MAX(pk_user_id), 0) + 1 FROM users"
        )
        user_id = run.fetchone()[0]
        
        run.execute(
            """
            INSERT INTO users
            (pk_user_id, user_name, user_email, user_password, eliminated_user)
            VALUES (%s, %s, %s, %s, FALSE)
            """,
            (user_id, user_name, user_email, user_password)
        )

        conn.commit()
        conn.close()
        return 'Usuario creado'

    except Exception:
        conn.rollback()
        conn.close()
        raise


def eliminate_user(user_id: int):
    """Eliminates user with: user_id: int"""
    conn = db.connect(current_db_url)
    run = conn.cursor()
        
    run.execute("UPDATE users SET eliminated_user = TRUE WHERE pk_user_id = (%s) ", (user_id,))
    conn.commit()
    conn.close()

