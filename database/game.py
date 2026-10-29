# IMPORT EXTERNAL LIBRARIES #
import psycopg2 as db
import os
from psycopg2 import sql



# VARIABLES #
DB_URL: str = os.environ.get("DATABASE_URL")



# FUNCTIONS #
def get_all_teams_from_a_league(league: str, used_team1: str, used_team2: str) -> list[tuple] | None:
    """returns a list of tuples of all of the teams present in the {league} provided excluding {used_team1} and {used_team2}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        query = sql.SQL("""SELECT DISTINCT {league} FROM players WHERE {league} IS NOT NULL AND {league} NOT IN (%s, %s)""").format(league=sql.Identifier(league))
        run.execute(query, (used_team1, used_team2))
        teams = run.fetchall()

        if teams == [] or all(value is None for value in teams[0]):
            return []
        else:
            return teams
    except Exception as e:
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()

def get_all_players_from_a_team_with_nationality(team: str, league: str, nationality: str) -> list[tuple] | None:
    """returns a list of tuples of all of the players present in the {team} with the provided {nationality}"""
    conn = None
    try:
        conn = db.connect(DB_URL)
        run = conn.cursor()
        
        columns = {"premier": "premier", "bundesliga": "bundesliga", "serie_a": "serie_a", "la_liga": "la_liga"}
        column = columns[league]

        run.execute(f"""SELECT player_name FROM players WHERE {column} = %s AND nationality = (%s)""", (team, nationality))
        players = run.fetchall()

        if players == [] or all(value is None for value in players[0]):
            return []
        else:
            return players[0]
    except Exception as e:
        print(e, flush=True)
        return None
    finally:
        if conn:
            conn.close()