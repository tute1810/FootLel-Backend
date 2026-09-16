# IMPORT LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class GuestCredentials(BaseModel):
    user_name: str