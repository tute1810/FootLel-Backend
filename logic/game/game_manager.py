# IMPORT EXTERNAL LIBRARIES #
from random import randint

# IMPORT INTERNAL LIBRARIES #
from database import get_players

# VARIABLES #
is_playing: bool = False
game_turn: int = 1

leagues_name: list[str] = ["premier", "bundesliga", "serie_a", "la_liga"]
nationalities_name: list[str] = ["Argentina", "Italia", "Inglaterra", "España", "Francia"]
winning_lines: list[list[int]] = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

teams_row: list[str] = []
nationalities_column: list[str] = []
player_names_matrix: list[list[str]] = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]
player_slots_matrix: list[list[int]] = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

# FUNCTIONS #
def start_game_board() -> tuple[list[str], list[str]]:
    # set "is_playing" to true #
    global is_playing
    is_playing = True

    # create the board #
    create_game_board()

    # return the headers that the "create_game_board" func generated #
    return teams_row, nationalities_column

def stop_game_board():
    global teams_row, nationalities_column, game_turn, is_playing, player_names_matrix, player_slots_matrix

    # reset game variables #
    is_playing = False
    game_turn = 1

    # reset board variables #
    teams_row = []
    nationalities_column = []
    player_slots_matrix = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    player_names_matrix = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

def create_game_board():
    global teams_row, nationalities_column, player_names_matrix, player_slots_matrix

    # create the variables that will store the game board #
    teams: list[str] = ["", "", ""]
    nationalities: list[str] = ["", "", ""]
    players: list[str] = []

    # repeat 3 times #
    for i in range(0, 3, 1):

        # pick a random league and store its name, not its index #
        random_league: str = leagues_name[randint(0, len(leagues_name) - 1)]

        # get all of the teams of the previous selected league #
        all_teams_of_random_league: list[str] = get_players.get_league_teams(random_league, teams[0], teams[1])

        # pick a random team of that whole list and store it on the "teams" var #
        teams[i] = all_teams_of_random_league[randint(0, len(all_teams_of_random_league) - 1)][0]

        # if the nationalities var is empty, then select the 3 nationalities alltogether #
        if nationalities[0] == "":
            
            # make a temporary copy of the nationalities name list so i can remove the ones that have been previously selected #
            temp_nationalities_name: list[str] = nationalities_name.copy()
            
            # repeat 3 times #
            for j in range(0, 3, 1):

                # pick a random nationality index #
                this_nationality_index: int = randint(0, len(temp_nationalities_name) - 1)

                # get the random nationality name with the previous selected index and store it in the "nationalities" var #
                nationalities[j] = temp_nationalities_name[this_nationality_index]

                # remove that random nationality from the temporary list so it does not get picked again #
                temp_nationalities_name.pop(this_nationality_index)

        # repeat 3 times #
        for j in range(0, 3, 1):

            # store the corresponding players of that selected team and those 3 nationalities on the "players" var #
            players.append(get_players.get_player(teams[i], random_league, nationalities[j])[0][0])

    # once we picked all of the board, store it on the global vars #
    teams_row = teams
    nationalities_column = nationalities
    for i in range(0, len(players), 1):
        row: int = i // 3
        column: int = i % 3
        player_names_matrix[row][column] = players[i]
        player_slots_matrix[row][column] = 0

def next_turn() -> bool:
    # increment the turn int #
    global game_turn
    game_turn += 1

    # return True if "game_turn" is odd and False if its even #
    return bool(game_turn % 2 != 0)

def player_guessed(player_guess: str) -> tuple[list[list[int]], bool, bool, bool] | None:

    # error out if the player is not in a game #
    if is_playing == False:
        return None

    global player_slots_matrix

    # repeat this code for the amount of players that exist #
    for i in range(0, (len(player_names_matrix) * len(player_names_matrix[0])), 1):
        row: int = i // 3
        column: int = i % 3

        # if the i player_name_matrix is equal to the guess the user made #
        if player_names_matrix[row][column] == player_guess:

            # if the slot the player guess is on is already occupied, do nothing and return the matrix
            if player_slots_matrix[row][column] != 0:
                return player_slots_matrix, False, False, False

            # set the slot to "1" to indicate that it belongs to the player #
            player_slots_matrix[row][column] = 1

            # check if any player won #
            somebody_won: bool; local_player_won: bool;
            somebody_won, local_player_won = check_winning_lines()
            if somebody_won == True:
                finished_player_slots_matrix: list[list[int]] = player_slots_matrix.copy()
                stop_game_board()
                return finished_player_slots_matrix, True, True, local_player_won

            # if the whole board has no "0" in it, that means there are no empty slots #
            if all(value != 0 for row in player_slots_matrix for value in row):
                
                # finish the game #
                finished_player_slots_matrix: list[list[int]] = player_slots_matrix.copy()
                stop_game_board()
                return finished_player_slots_matrix, True, True, False
            
            return player_slots_matrix, True, False, False
    return player_slots_matrix, False, False, False

def player2_guessed(player2_guess: str) -> tuple[list[list[int]], bool, bool, bool] | None:

    # error out if the player is not in a game #
    if is_playing == False:
        return None

    global player_slots_matrix

    # repeat this code for the amount of players that exist #
    for i in range(0, (len(player_names_matrix) * len(player_names_matrix[0])), 1):
        row: int = i // 3
        column: int = i % 3

        # if the i player_name_matrix is equal to the guess the user made #
        if player_names_matrix[row][column] == player2_guess:

            # if the slot the player guess is on is already occupied, do nothing and return the matrix
            if player_slots_matrix[row][column] != 0:
                return player_slots_matrix, False, False, False

            # set the slot to "1" to indicate that it belongs to the player #
            player_slots_matrix[row][column] = -1

            # check if any player won #
            somebody_won: bool; local_player_won: bool;
            somebody_won, local_player_won = check_winning_lines()
            if somebody_won == True:
                finished_player_slots_matrix: list[list[int]] = player_slots_matrix.copy()
                stop_game_board()
                return finished_player_slots_matrix, True, True, local_player_won

            # if the whole board has no "0" in it, that means there are no empty slots #
            if all(value != 0 for row in player_slots_matrix for value in row):
                
                # finish the game #
                finished_player_slots_matrix: list[list[int]] = player_slots_matrix.copy()
                stop_game_board()
                return finished_player_slots_matrix, True, True, False
            
            return player_slots_matrix, True, False, False
    return player_slots_matrix, False, False, False

def ai_guessed() -> tuple[list[list[int]], bool, bool] | None:
    
    # error out if the player is not in a game #
    if is_playing == False:
        return None

    global player_slots_matrix

    # store all the rows and columns where the player has a slot #
    player_slots_rows: list[int] = []
    player_slots_columns: list[int] = []

    for i in range(0, (len(player_names_matrix) * len(player_names_matrix[0])), 1):
        row: int = i // 3
        column: int = i % 3

        # check if that slot is from the player, then store it #
        if player_slots_matrix[row][column] == 1:
            player_slots_rows.append(row)
            player_slots_columns.append(column)

    # if there were no player slots, just return the matrix #
    if len(player_slots_rows) == 0:
        return player_slots_matrix, False, False

    # grab a random slot from all of the player slots #
    random_player_slot_index: int = randint(0, (len(player_slots_rows) - 1))
    selected_player_slot_packaged: list[int] = [ player_slots_rows[random_player_slot_index], player_slots_columns[random_player_slot_index] ]

    # repeat 8 times #
    for i in range(0, 8, 1):

        # get all of the possible directions #
        direction: tuple[int] = (0, 0)
        if i == 0:
            direction = (0, 1)
        elif i == 1:
            direction = (1, 1)
        elif i == 2:
            direction = (1, 0)
        elif i == 3:
            direction = (1, -1)
        elif i == 4:
            direction = (0, -1)
        elif i == 5:
            direction = (-1, -1)
        elif i == 6:
            direction = (-1, 0)
        elif i == 7:
            direction = (-1, 1)

        # if the direction is out of bounds or if there was an error on the direction code, try another dir #
        if direction == (0, 0) or _in_range(selected_player_slot_packaged[0] + direction[0], 0, 2) == False or _in_range(selected_player_slot_packaged[1] + direction[1], 0, 2) == False:
            continue

        # if the slot is occupied, then try with another dir #
        if player_slots_matrix[selected_player_slot_packaged[0] + direction[0]][selected_player_slot_packaged[1] + direction[1]] != 0:
            continue

        # 20% chance of not placing a slot there #
        if randint(1, 5) == 4:
            continue

        # put the ai slot and break from the for loop #
        player_slots_matrix[selected_player_slot_packaged[0] + direction[0]][selected_player_slot_packaged[1] + direction[1]] = -1

        # check if any player won #
        somebody_won: bool; local_player_won: bool;
        somebody_won, local_player_won = check_winning_lines()
        if somebody_won == True:
            finished_player_slots_matrix: list[list[int]] = player_slots_matrix.copy()
            stop_game_board()
            return finished_player_slots_matrix, True, local_player_won

        # if there are no more empty slots, then end the game #
        if all(value != 0 for row in player_slots_matrix for value in row):
            finished_player_slots_matrix: list[list[int]] = player_slots_matrix.copy()
            stop_game_board()
            return finished_player_slots_matrix, True, False

        # if there are more empty slots, then just return the new matrix without ending the game #
        return player_slots_matrix, False, False

    # if the ai could not place a slot, just return the same matrix #
    return player_slots_matrix, False, False

# simple function that returns if the value is inside a range #
def _in_range(value: int, minimum: int, maximum: int) -> bool:
    return minimum <= value <= maximum

# function that checks the board for any winning lines #
def check_winning_lines() -> tuple[bool, bool]:
    for i in range(0, len(winning_lines), 1):
        line_is_from_the_player: bool = False
        for j in range(0, len(winning_lines[i]), 1):

            # store the slot value #
            slot: int = player_slots_matrix[winning_lines[i][j] // 3][winning_lines[i][j] % 3]
            if slot != 0:
                if slot == 1:

                    # check if we are not on the first slot check #
                    if j > 0:
                        if line_is_from_the_player == False:
                            break
                    
                    # check if the last slot is the same and return true #
                    if j == 2:
                        return True, True

                    line_is_from_the_player = True
                elif slot == -1:

                    # check if we are not on the first slot check #
                    if j > 0:
                        if line_is_from_the_player == True:
                            break
                    
                    # check if the last slot is the same and return true #
                    if j == 2:
                        return True, False

                    line_is_from_the_player = False
            else:
                break
    return False, False