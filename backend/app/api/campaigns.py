from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.entities import AdAccount
from app.repositories.campaign_repository import CampaignRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.schemas.campaign import CampaignStatusRequest, CampaignWizardRequest
from app.services.ad_platform_service import AdPlatformService

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.post("")
async def create_campaign(payload: CampaignWizardRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.organization_id:
        raise HTTPException(status_code=400, detail="Organization is required")

    active_sub = SubscriptionRepository(db).get_active_by_org(user.organization_id)
    if not active_sub:
        raise HTTPException(status_code=402, detail="Active subscription required")

    account = db.query(AdAccount).filter(AdAccount.id == payload.ad_account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Ad account not found")

    campaign_repo = CampaignRepository(db)
    campaign = campaign_repo.create(
        organization_id=user.organization_id,
        ad_account_id=payload.ad_account_id,
        name=payload.name,
        goal=payload.goal,
        budget_daily=payload.budget_daily,
        wizard_payload=payload.model_dump(),
        status="queued",
    )
    adapter_payload = {
        "name": payload.name,
        "objective": payload.goal,
        "daily_budget": int(payload.budget_daily * 100),
        "status": "PAUSED",
    }
    remote_id = await AdPlatformService().create_campaign(account, adapter_payload)
    campaign.platform_campaign_id = remote_id
    campaign.status = "active"
    db.add(campaign)
    db.commit()
    return {"campaign_id": campaign.id, "platform_campaign_id": remote_id}


@router.patch("/{campaign_id}/status")
def update_campaign_status(campaign_id: int, payload: CampaignStatusRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    campaign = CampaignRepository(db).get(campaign_id)
    if not campaign or campaign.organization_id != user.organization_id:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign.status = payload.status
    db.add(campaign)
    db.commit()
    return {"campaign_id": campaign.id, "status": campaign.status}
