from datetime import datetime, timedelta

import httpx

from app.core.config import settings
from app.core.security import decrypt_secret
from app.models.entities import AdAccount, Platform


class AdPlatformService:
    async def create_campaign(self, account: AdAccount, payload: dict) -> str:
        access_token = decrypt_secret(account.encrypted_access_token)
        if account.platform == Platform.GOOGLE:
            # Simplified request format for Google Ads API endpoint proxy.
            url = f"https://googleads.googleapis.com/v16/customers/{account.external_account_id}/campaigns:mutate"
            body = {"operations": [{"create": payload}]}
            headers = {"Authorization": f"Bearer {access_token}", "developer-token": "set-in-env"}
        else:
            url = f"https://graph.facebook.com/v21.0/act_{account.external_account_id}/campaigns"
            body = payload | {"access_token": access_token}
            headers = {}

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, json=body, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        return data.get("resource_name") or data.get("id") or "unknown"

    async def refresh_google_token(self, refresh_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
            )
            response.raise_for_status()
            payload = response.json()
            payload["expires_at"] = datetime.utcnow() + timedelta(seconds=payload["expires_in"])
            return payload
