from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.entities import Campaign, CampaignMetric

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/metrics")
def metrics(from_date: datetime, to_date: datetime, platform: str | None = None, user=Depends(get_current_user), db: Session = Depends(get_db)):
    q = (
        db.query(CampaignMetric, Campaign)
        .join(Campaign, Campaign.id == CampaignMetric.campaign_id)
        .filter(
            Campaign.organization_id == user.organization_id,
            and_(CampaignMetric.metric_date >= from_date, CampaignMetric.metric_date <= to_date),
        )
    )
    if platform:
        q = q.filter(Campaign.wizard_payload["platform"].astext == platform)

    rows = q.all()
    return [
        {
            "campaign_id": campaign.id,
            "date": metric.metric_date,
            "impressions": metric.impressions,
            "clicks": metric.clicks,
            "cpc": metric.cpc,
            "spend": metric.spend,
        }
        for metric, campaign in rows
    ]
