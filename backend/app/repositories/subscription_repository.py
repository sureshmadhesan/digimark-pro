from app.models.entities import Subscription
from app.repositories.base import Repository


class SubscriptionRepository(Repository):
    def get_active_by_org(self, org_id: int) -> Subscription | None:
        return (
            self.db.query(Subscription)
            .filter(Subscription.organization_id == org_id, Subscription.status.in_(["active", "authenticated"]))
            .first()
        )

    def create(self, **kwargs) -> Subscription:
        model = Subscription(**kwargs)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_by_external(self, sub_id: str) -> Subscription | None:
        return self.db.query(Subscription).filter(Subscription.razorpay_subscription_id == sub_id).first()
