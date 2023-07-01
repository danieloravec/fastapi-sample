from datetime import datetime, timedelta
from jose import jwt, JWTError
from config import settings


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({
        "exp": datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    })
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


# If we wanted to be able to revoke access by deleting the user, then checking if the user exists would be needed here.
# Since the token expires after a short time, we skip this check.
def is_auth_token_valid(token: str) -> bool:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload.get("user_id") is not None
    except JWTError:
        return False
