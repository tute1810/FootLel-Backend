# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class UserLoginCredentials(BaseModel):
    user_name: str
    user_password: str