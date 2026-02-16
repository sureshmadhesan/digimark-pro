from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.billing_service import BillingService

router = APIRouter(prefix="/billing", tags=["billing"])


@router.post("/subscriptions")
async def create_subscription(plan_code: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = BillingService(SubscriptionRepository(db))
    return await service.create_subscription(user.organization_id, plan_code)


@router.post("/webhooks/razorpay")
async def razorpay_webhook(request: Request, x_razorpay_signature: str = Header(alias="X-Razorpay-Signature"), db: Session = Depends(get_db)):
    payload = await request.body()
    service = BillingService(SubscriptionRepository(db))
    return service.verify_and_process_webhook(db, payload, x_razorpay_signature)
