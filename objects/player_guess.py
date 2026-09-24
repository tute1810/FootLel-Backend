# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class PlayerGuess(BaseModel):
    was_local_player_guessing: bool
    player_guess: str