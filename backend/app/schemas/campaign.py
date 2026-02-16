from pydantic import BaseModel, Field


class CampaignWizardRequest(BaseModel):
    ad_account_id: int
    name: str
    goal: str
    budget_daily: float = Field(gt=0)
    location: str
    audience: dict
    creative: dict


class CampaignStatusRequest(BaseModel):
    status: str
