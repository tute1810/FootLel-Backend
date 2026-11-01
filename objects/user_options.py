# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class UserOptions(BaseModel):
    dark_mode: bool
    animation_state: bool
    compatibility_mode: bool