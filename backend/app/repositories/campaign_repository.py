from app.models.entities import Campaign
from app.repositories.base import Repository


class CampaignRepository(Repository):
    def create(self, **kwargs) -> Campaign:
        campaign = Campaign(**kwargs)
        self.db.add(campaign)
        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def get(self, campaign_id: int) -> Campaign | None:
        return self.db.query(Campaign).filter(Campaign.id == campaign_id, Campaign.deleted_at.is_(None)).first()

    def list_by_org(self, org_id: int) -> list[Campaign]:
        return self.db.query(Campaign).filter(Campaign.organization_id == org_id, Campaign.deleted_at.is_(None)).all()
