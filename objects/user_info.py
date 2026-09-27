# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class UserInfo(BaseModel):
    user_id: int
    user_name: str
    user_email: str
    user_password: str