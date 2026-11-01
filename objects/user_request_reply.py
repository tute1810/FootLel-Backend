# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class UserRequestReply(BaseModel):
    friend_name: str
    reply: bool