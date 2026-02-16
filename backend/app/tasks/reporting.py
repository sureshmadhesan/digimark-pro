from datetime import datetime

from app.core.database import SessionLocal
from app.models.entities import Campaign, CampaignMetric
from app.tasks.celery_app import celery


@celery.task(bind=True, max_retries=3, default_retry_delay=30)
def collect_metrics(self):
    db = SessionLocal()
    try:
        campaigns = db.query(Campaign).filter(Campaign.deleted_at.is_(None)).all()
        for campaign in campaigns:
            metric = CampaignMetric(
                campaign_id=campaign.id,
                metric_date=datetime.utcnow(),
                impressions=100,
                clicks=10,
                cpc=12.5,
                spend=125.0,
            )
            db.add(metric)
        db.commit()
    except Exception as exc:
        db.rollback()
        raise self.retry(exc=exc)
    finally:
        db.close()
