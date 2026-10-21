# IMPORT EXTERNAL LIBRARIES #
import os
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Any
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# VARIABLES #
SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]
ALGORITHM: str = "HS256"
TOKEN_EXPIRE_MINUTES: int = 30

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/user-login")

# FUNCTIONS #
def get_access_token(user_id: int) -> str:
    payload: dict[str, str | datetime] = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)}

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def check_access_token_and_get_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])

        user_id: str | None = payload.get("sub")

        if not isinstance(user_id, str) or not user_id.isdigit():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="error de token: token incorrecto", headers={"WWW-Authenticate": "Bearer"})

        return int(user_id)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="error de token: token invalido o ha expirado")