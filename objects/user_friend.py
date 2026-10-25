from pydantic import BaseModel

# CREATE THE OBJECT #
class UserFriend(BaseModel):
    friend_id: int