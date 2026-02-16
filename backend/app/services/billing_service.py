import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.core.security import verify_razorpay_signature
from app.models.entities import PaymentTransaction
from app.repositories.subscription_repository import SubscriptionRepository


class BillingService:
    def __init__(self, subscription_repo: SubscriptionRepository):
        self.subscription_repo = subscription_repo

    async def create_subscription(self, org_id: int, plan_code: str):
        url = "https://api.razorpay.com/v1/subscriptions"
        payload = {"plan_id": plan_code, "total_count": 12, "customer_notify": 1}
        async with httpx.AsyncClient(auth=(settings.razorpay_key_id, settings.razorpay_key_secret)) as client:
            resp = await client.post(url, json=payload)
        if resp.status_code >= 400:
            raise HTTPException(status_code=502, detail=f"Razorpay error: {resp.text}")
        data = resp.json()
        sub = self.subscription_repo.create(
            organization_id=org_id,
            razorpay_subscription_id=data["id"],
            plan_code=plan_code,
            status=data.get("status", "created"),
        )
        return {"subscription_id": sub.razorpay_subscription_id, "checkout_data": data}

    def verify_and_process_webhook(self, db, payload: bytes, signature: str):
        if not verify_razorpay_signature(payload, signature):
            raise HTTPException(status_code=401, detail="Invalid Razorpay signature")
        import json

        event = json.loads(payload.decode())
        entity = event.get("payload", {}).get("subscription", {}).get("entity", {})
        sub_id = entity.get("id")
        if not sub_id:
            return {"ok": True}

        subscription = self.subscription_repo.get_by_external(sub_id)
        if subscription:
            subscription.status = entity.get("status", subscription.status)
            db.add(subscription)

        payment = event.get("payload", {}).get("payment", {}).get("entity")
        if payment and subscription:
            tx = PaymentTransaction(
                subscription_id=subscription.id,
                razorpay_payment_id=payment.get("id"),
                amount=payment.get("amount", 0) / 100,
                currency=payment.get("currency", "INR"),
                status=payment.get("status", "captured"),
                raw_payload=payment,
            )
            db.add(tx)
        db.commit()
        return {"ok": True}
