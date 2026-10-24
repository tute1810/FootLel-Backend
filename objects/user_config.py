# IMPORT EXTERNAL LIBRARIES #
from pydantic import BaseModel

# CREATE THE OBJECT #
class UserConfig(BaseModel):
    config_1: bool
    config_2: bool
    config_3: bool