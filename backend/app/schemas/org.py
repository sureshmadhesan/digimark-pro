from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    business_name: str
    gst_number: str | None = None
    billing_address: str | None = None
