from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Event, Variant

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{experiment_id}")
def get_analytics(experiment_id: int, db: Session = Depends(get_db)):

    users = db.query(
        Event.variant_id,
        func.count(func.distinct(Event.user_id)).label("users")
    ).filter(
        Event.experiment_id == experiment_id,
        Event.event_type == "view"
    ).group_by(Event.variant_id).all()

    conversions = db.query(
        Event.variant_id,
        func.count(func.distinct(Event.user_id)).label("conversions")
    ).filter(
        Event.experiment_id == experiment_id,
        Event.event_type == "click"
    ).group_by(Event.variant_id).all()

    user_dict = {u.variant_id: u.users for u in users}
    conv_dict = {c.variant_id: c.conversions for c in conversions}

    variants = db.query(Variant).filter_by(experiment_id=experiment_id).all()

    result = []

    for v in variants:
        u = user_dict.get(v.id, 0)
        c = conv_dict.get(v.id, 0)
        cr = (c / u) if u > 0 else 0

        result.append({
            "variant": v.name,
            "users": u,
            "conversions": c,
            "conversion_rate": round(cr, 4)
        })

    return {
        "experiment_id": experiment_id,
        "results": result
    }