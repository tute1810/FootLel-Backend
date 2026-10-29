# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class UserRequestReply(BaseModel):
    user_id_request: int
    reply: bool