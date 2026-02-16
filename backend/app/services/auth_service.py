from datetime import timedelta

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import create_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def signup(self, email: str, password: str):
        if self.user_repo.get_by_email(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        user = self.user_repo.create(email=email, password_hash=hash_password(password))
        return self.issue_tokens(str(user.id))

    def login(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return self.issue_tokens(str(user.id))

    def issue_tokens(self, user_id: str):
        access = create_token(user_id, timedelta(minutes=settings.access_token_exp_minutes), "access")
        refresh = create_token(user_id, timedelta(minutes=settings.refresh_token_exp_minutes), "refresh")
        return {"access_token": access, "refresh_token": refresh}
