from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import FeatureFlag
import random

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/")
def get_all_flags(db: Session = Depends(get_db)):
    flags = db.query(FeatureFlag).all()
    return [
        {
            "key": f.key,
            "is_enabled": f.is_enabled,
            "rollout_percentage": f.rollout_percentage
        }
        for f in flags
    ]
@router.get("/{key}")
def get_flag(key: str, user_id: str, db: Session = Depends(get_db)):
    flag = db.query(FeatureFlag).filter_by(key=key).first()

    if not flag or not flag.is_enabled:
        return {"enabled": False}

    if random.randint(1, 100) <= flag.rollout_percentage:
        return {"enabled": True}

    return {"enabled": False}