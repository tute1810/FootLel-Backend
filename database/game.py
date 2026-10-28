# IMPORT EXTERNAL LIBRARIES #
import psycopg2 as db
import os
from psycopg2 import sql



# VARIABLES #
DB_URL: str = os.environ.get("DATABASE_URL")



# FUNCTIONS #
def get_league_teams(league: str, used_team1: str, used_team2: str)-> tuple[list] | None :
    """Returns a list of tuples of the league teams"""
    conn = None

    try:
        conn = db.connect(DB_URL)
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

        if teams == [] or all(value is None for value in teams[0]):
            conn.rollback()
            conn.close()
            return []

        conn.close()
        return teams[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def get_player(team: str, league: str, nationality: str)-> tuple[list] | None:
    """Returns a list of tuples of the players from the team and nationality selected"""
    conn = None

    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        columns = {
            "premier": "premier",
            "bundesliga": "bundesliga",
            "serie_a":"serie_a",
            "la_liga":"la_liga"
            }
        column = columns[league]

        run.execute(f"""SELECT player_name FROM players WHERE {column} = %s AND nationality = (%s) """,  (team,nationality))

        player = run.fetchall()
        conn.commit()

        if player == [] or all(value is None for value in player[0]):
            return []
        else:
            return player[0]
    except Exception as e:
        if conn:
            conn.rollback()
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()