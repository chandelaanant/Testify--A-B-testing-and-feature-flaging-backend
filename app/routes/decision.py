from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Variant
from app.logic import assign_variant

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_decision(user_id: str, experiment_id: int, db: Session = Depends(get_db)):
    variants = db.query(Variant).filter_by(experiment_id=experiment_id).all()

    variant_id = assign_variant(user_id, experiment_id, db, variants)
    variant = next(v for v in variants if v.id == variant_id)

    return {
        "experiment_id": experiment_id,
        "variant_id": variant.id,
        "variant": variant.name
    }