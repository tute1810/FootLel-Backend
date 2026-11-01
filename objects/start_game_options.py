# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class StartGameOptions(BaseModel):
    is_last_round: bool
    is_daily_challenge: bool