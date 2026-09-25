# IMPORT LIBRARIES #
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# IMPORT ROUTERS #
from routers import user_management
from routers import authentication
from routers import game
from routers import user_stats

# CREATE THE API #
app = FastAPI(title="FootLel_api", version="0.1.0")

# CORS STUFF #
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# INCLUDE THE ROUTERS TO THE API #
app.include_router(user_management.router)
app.include_router(authentication.router)
app.include_router(game.router)
app.include_router(user_stats.router)

@app.get("/")
def root():
    return {"status": "ok"}