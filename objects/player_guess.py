# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class PlayerGuess(BaseModel):
    player_guess: str