from datetime import datetime, timedelta

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.core.security import encrypt_secret
from app.models.entities import AdAccount, Platform

router = APIRouter(prefix="/oauth", tags=["oauth"])


@router.post("/google/callback")
async def google_callback(code: str, account_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )
    if token_resp.status_code >= 400:
        raise HTTPException(status_code=400, detail=f"Google OAuth error: {token_resp.text}")
    tokens = token_resp.json()

    ad = AdAccount(
        organization_id=user.organization_id,
        platform=Platform.GOOGLE,
        external_account_id=account_id,
        encrypted_access_token=encrypt_secret(tokens["access_token"]),
        encrypted_refresh_token=encrypt_secret(tokens.get("refresh_token", "")) if tokens.get("refresh_token") else None,
        token_expires_at=datetime.utcnow() + timedelta(seconds=tokens.get("expires_in", 3600)),
    )
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return {"ad_account_id": ad.id}


@router.post("/meta/callback")
async def meta_callback(code: str, ad_account_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_resp = await client.get(
            "https://graph.facebook.com/v21.0/oauth/access_token",
            params={
                "client_id": settings.meta_client_id,
                "client_secret": settings.meta_client_secret,
                "redirect_uri": settings.meta_redirect_uri,
                "code": code,
            },
        )
    if token_resp.status_code >= 400:
        raise HTTPException(status_code=400, detail=f"Meta OAuth error: {token_resp.text}")
    token = token_resp.json().get("access_token")

    ad = AdAccount(
        organization_id=user.organization_id,
        platform=Platform.META,
        external_account_id=ad_account_id,
        encrypted_access_token=encrypt_secret(token),
        encrypted_refresh_token=None,
        token_expires_at=None,
    )
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return {"ad_account_id": ad.id}
