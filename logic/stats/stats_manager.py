from database import user_stats

def set_matches_stats(user_id: int, match_won: int) -> bool:
    # guesses_made, correct_guesses, matches_played, matches_won, matches_lost, win_streak, user_points #
    all_user_stats = user_stats.get_user_stats(user_id)
    
    if all_user_stats is None:
        return False

    match_won_value: int = 0
    points_value: int = 2
    if match_won == True:
        match_won_value = 1
        points_value = 10

    return user_stats.set_user_matches_stats(user_id, all_user_stats[0][3] + 1, all_user_stats[0][4] + match_won_value, all_user_stats[0][0] + points_value)
    
def set_guesses_stats(user_id: int, correct_guess: bool):
    # guesses_made, correct_guesses, matches_played, matches_won, matches_lost, win_streak, user_points #
    all_user_stats = user_stats.get_user_stats(user_id)
    
    if all_user_stats is None:
        return False
    
    correct_guess_value: int = 0
    if correct_guess == True:
        correct_guess_value = 1

    return user_stats.set_user_guesses_stats(user_id, all_user_stats[0][1] + 1, all_user_stats[0][2] + correct_guess_value)