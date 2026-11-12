# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class ChangeUserPassword(BaseModel):
    user_email: str
    user_password: str