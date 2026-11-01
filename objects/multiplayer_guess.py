# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class MultiplayerGuess(BaseModel):
    game_id: int
    player_guess: str