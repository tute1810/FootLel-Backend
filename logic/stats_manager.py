# IMPORT INTERNAL LIBRARIES #
from database import user_stats

# FUNCTIONS #
def set_matches_stats(user_id: int, daily_challenge: bool, match_won: bool) -> bool:
    """
    all_user_stats:
    user_points,
    guesses_made,
    correct_guesses,
    matches_played,
    matches_won,
    win_streak
    """

    all_user_stats: tuple[int] | None = user_stats.get_user_stats(user_id)
    
    if all_user_stats is None:
        return False

    match_won_value: int
    points_value: int = 0
    win_streak_value: int = 0

    if match_won is True:
        match_won_value = 1
        if daily_challenge is True:
            win_streak_value = all_user_stats[5] + 1
            points_value = win_streak_value * 10
    else:
        match_won_value = 0
        if daily_challenge is True:
            win_streak_value = 0
            points_value = 2

    if daily_challenge is True:
        if user_stats.set_user_win_streak(user_id, win_streak_value) is False:
            return False

    return user_stats.set_user_matches_stats(user_id, all_user_stats[3] + 1, all_user_stats[4] + match_won_value, all_user_stats[0] + points_value)

def set_guesses_stats(user_id: int, correct_guess: bool) -> bool:
    """
    all_user_stats:
    user_points,
    guesses_made,
    correct_guesses,
    matches_played,
    matches_won,
    win_streak
    """
    
    all_user_stats: tuple[int] | None = user_stats.get_user_stats(user_id)
    
    if all_user_stats is None:
        return False

    return user_stats.set_user_guesses_stats(user_id, all_user_stats[1] + 1, all_user_stats[2] + int(correct_guess))