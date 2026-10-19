import psycopg2 as db
import os

deployed_db_url = os.environ.get("Database_URL")

current_db_url = deployed_db_url



def get_league_teams(league: str, used_team1: str, used_team2: str):
    """Returns a list of tuples of the league teams"""
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



def get_player(team: str, league: str, nationality: str):
    """Returns a player from the team and nationality selected"""
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
