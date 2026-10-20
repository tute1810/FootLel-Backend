# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class PlayerGuess(BaseModel):
    user_strid: str
    player_guess: str