from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import rate_limit_auth
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(request: SignupRequest, raw_req: Request, db: Session = Depends(get_db)):
    rate_limit_auth(raw_req.client.host if raw_req.client else "unknown")
    service = AuthService(UserRepository(db))
    return service.signup(request.email, request.password)


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, raw_req: Request, db: Session = Depends(get_db)):
    rate_limit_auth(raw_req.client.host if raw_req.client else "unknown")
    service = AuthService(UserRepository(db))
    return service.login(request.email, request.password)


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: dict, db: Session = Depends(get_db)):
    service = AuthService(UserRepository(db))
    return service.issue_tokens(str(request["user_id"]))
