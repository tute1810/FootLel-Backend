# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class DarkModeState(BaseModel):
    dark_mode_state: bool