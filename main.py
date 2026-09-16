# IMPORT LIBRARIES #
from fastapi import FastAPI

# IMPORT ROUTERS #
from routers import user_management
from routers import authentication

# CREATE THE API #
app = FastAPI(title="FootLel_api", version="0.1.0")

# INCLUDE THE ENDPOINTS TO THE API #
app.include_router(user_management.router)
app.include_router(authentication.router)