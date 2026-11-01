# IMPORT EXTERNAL LIBRARIES #
import datetime

# IMPORT INTERNAL LIBRARIES #
from database import user_stats

# FUNCTIONS #
def update_daily_challenge_date():
    current_date: str = datetime.datetime.now().strftime("%Y-%m-%d")
    db_current_date: str | None = user_stats.get_current_date()

    if db_current_date is None or db_current_date is False:
        return True

    if db_current_date != current_date:
        daily_challenge_reset_return: bool | None = user_stats.reset_daily_challenge_state_to_all_users()

        if daily_challenge_reset_return is False or daily_challenge_reset_return is None:
            return True

        daily_challenge_current_date: bool | None = user_stats.set_current_date(current_date)

        if daily_challenge_current_date is False or daily_challenge_current_date is None:
            return True

    return False