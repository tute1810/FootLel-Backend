# IMPORT EXTERNAL LIBRARIES #
import datetime

# IMPORT INTERNAL LIBRARIES #
from database import user_stats

# FUNCTIONS #
def update_daily_challenge_date():
    error = False
    current_date: str = datetime.datetime.now().strftime("%Y-%m-%d")
    db_current_date: str = user_stats.get_current_date()

    if db_current_date == current_date:
        daily_challenge_reset_return: bool | None = user_stats.reset_daily_challenge_state_to_all_users()

        if daily_challenge_reset_return is False or daily_challenge_reset_return is None:
            error = True

        user_stats.set_current_date(current_date)

    return current_date, db_current_date, db_current_date != current_date, error