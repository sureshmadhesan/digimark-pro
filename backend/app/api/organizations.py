from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.entities import Role, RoleName
from app.repositories.org_repository import OrganizationRepository
from app.schemas.org import OrganizationCreate

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("")
def create_organization(payload: OrganizationCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    org = OrganizationRepository(db).create(payload.business_name, payload.gst_number, payload.billing_address)
    owner_role = db.query(Role).filter(Role.name == RoleName.OWNER).first()
    user.organization_id = org.id
    user.role_id = owner_role.id if owner_role else None
    db.add(user)
    db.commit()
    return {"organization_id": org.id, "role": "Owner"}
