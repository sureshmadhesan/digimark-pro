from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.entities import RoleName, User


ATTEMPTS: dict[str, list[datetime]] = defaultdict(list)


def rate_limit_auth(client_ip: str):
    now = datetime.utcnow()
    attempts = [a for a in ATTEMPTS[client_ip] if now - a < timedelta(minutes=1)]
    if len(attempts) >= 20:
        raise HTTPException(status_code=429, detail="Too many auth attempts")
    attempts.append(now)
    ATTEMPTS[client_ip] = attempts


def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = int(payload["sub"])
    except (JWTError, ValueError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_roles(*roles: RoleName):
    def checker(user: User = Depends(get_current_user)):
        if not user.role or user.role.name not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user

    return checker
