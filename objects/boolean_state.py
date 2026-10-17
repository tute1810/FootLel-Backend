# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class BooleanState(BaseModel):
    user_id: int
    boolean: bool