# IMPORT LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class UserCredentials(BaseModel):
    user_name: str
    user_email: str
    user_password: str