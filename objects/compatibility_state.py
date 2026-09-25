# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class CompatibilityState(BaseModel):
    compatibility_state: bool