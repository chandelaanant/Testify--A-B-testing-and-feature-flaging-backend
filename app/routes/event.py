from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Event

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def track_event(data: dict, db: Session = Depends(get_db)):
    event = Event(**data)
    db.add(event)
    db.commit()
    return {"status": "tracked"}