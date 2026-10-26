# IMPORT EXTERNAL LIBRARIES #
import datetime

# IMPORT INTERNAL LIBRARIES #
from database import user_stats

# FUNCTIONS #
def update_daily_challenge_date():
    current_date: str = datetime.datetime.now().strftime("%Y-%m-%d")
    db_current_date: str = user_stats.get_current_date()

    print(f"current_date: {current_date}, db_current_date: {db_current_date}", flush=True)

    if db_current_date != current_date:
        user_stats.reset_daily_challenge_state_to_all_users()
        user_stats.set_current_date(current_date)