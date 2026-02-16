from fastapi import FastAPI

from app.api import auth, billing, campaigns, organizations, reports
from app.core.database import Base, engine
from app.models.entities import Role, RoleName
from app.oauth import routes as oauth_routes

app = FastAPI(title="SocialMediaPro API")

app.include_router(auth.router)
app.include_router(organizations.router)
app.include_router(oauth_routes.router)
app.include_router(billing.router)
app.include_router(campaigns.router)
app.include_router(reports.router)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    from sqlalchemy.orm import Session

    db = Session(bind=engine)
    for role in RoleName:
        if not db.query(Role).filter(Role.name == role).first():
            db.add(Role(name=role))
    db.commit()
    db.close()


@app.get("/health")
def health():
    return {"status": "ok"}
