import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]
ALGORITHM: str = "HS256"
TOKEN_EXPIRE_MINUTES: int = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_access_token(user_id: str) -> str:
    payload = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES),}
    print({"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES),}, flush=True)

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM,)

def check_access_token_and_return_user_id(token: str = Depends(oauth2_scheme),) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM],)

        user_id = payload.get("sub")

        if not isinstance(user_id, str) or not user_id:
            raise InvalidTokenError("Missing user ID")

        return user_id
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token",headers={"WWW-Authenticate": "Bearer"},)