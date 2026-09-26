# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class UserRegisterCredentials(BaseModel):
    user_name: str
    user_email: str
    user_password: str