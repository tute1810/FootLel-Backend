import psycopg2 as db
from psycopg2 import sql

local_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a.oregon-postgres.render.com/footlel_db"
deployed_db_url = "postgresql://footlel_db_user:4s67LSdik8NJwqG5N6dCeFd3W46fcZaF@dpg-daks7dlbedkc73cttod0-a/footlel_db"
current_db_url = local_db_url



def get_league_teams(league: str, used_team1: str, used_team2: str):
    """Get league teams"""
    conn = None

    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        

        query = sql.SQL("""
            SELECT DISTINCT {league}
            FROM players
            WHERE {league} IS NOT NULL
            AND {league} NOT IN (%s, %s)
        """).format(
            league=sql.Identifier(league)
        )

        run.execute(query, (used_team1, used_team2))

        teams = run.fetchall()
        conn.commit()

        if teams == []:
            conn.rollback()
            conn.close()
            return None

        conn.close()
        return teams 
    except Exception as e:
        if conn:
            conn.rollback()
        print(e)
        return None
    finally:
        if conn:
            conn.close()
            


def get_random_players(team: str, league: str):
    """Get random players"""
    conn = None

    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        columns = {
            "premier": "premier",
            "bundesliga": "bundesliga",
            "serie_a": "serie_a",
            "la_liga": "la_liga"
            }
        column = columns[league]

        

        run.execute(f"""SELECT player_name, nationality FROM players WHERE {column} = %s ORDER BY RANDOM() LIMIT 3""",  (team,))

        teams = run.fetchall()
        conn.commit()

        if teams == []:
            conn.rollback()
            conn.close()
            return None

        conn.close()
        return teams 
    except Exception as e:
        if conn:
            conn.rollback()
        print(e)
        return None
    finally:
        if conn:
            conn.close()



def get_player(team: str, league: str, nationality: str):
    """Get player"""
    conn = None

    try:
        conn = db.connect(current_db_url)
        run = conn.cursor()
        
        columns = {
            "premier": "premier",
            "bundesliga": "bundesliga",
            "serie_a":"serie_a",
            "la_liga":"la_liga"
            }
        column = columns[league]

        run.execute(f"""SELECT player_name FROM players WHERE {column} = %s AND nationality = (%s) """,  (team,nationality))

        teams = run.fetchall()
        conn.commit()

        if teams == []:
            conn.rollback()
            conn.close()
            return None

        conn.close()
        return teams
    except Exception as e:
        if conn:
            conn.rollback()
        print(e)
        return None
    finally:
        if conn:
            conn.close()