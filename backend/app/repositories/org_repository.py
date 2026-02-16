from app.models.entities import Organization
from app.repositories.base import Repository


class OrganizationRepository(Repository):
    def create(self, business_name: str, gst_number: str | None, billing_address: str | None) -> Organization:
        org = Organization(
            business_name=business_name,
            gst_number=gst_number,
            billing_address=billing_address,
        )
        self.db.add(org)
        self.db.commit()
        self.db.refresh(org)
        return org
