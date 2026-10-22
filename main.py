# IMPORT LIBRARIES #
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# IMPORT ROUTERS #
import routers

# CREATE THE API #
app = FastAPI(title="FootLel_api", version="0.1.0")

# CORS STUFF #
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# INCLUDE THE ROUTERS TO THE API #
app.include_router(routers.authentication.router)
app.include_router(routers.game.router)
app.include_router(routers.user_management.router)
app.include_router(routers.user_stats.router)

@app.get("/")
def root():
    return {"status": "ok"}