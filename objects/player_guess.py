# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class PlayerGuess(BaseModel):
    user_id: int
    player_guess: str