from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models   
from app.routes import decision, event, flag, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(decision.router, prefix="/decision")
app.include_router(event.router, prefix="/event")
app.include_router(flag.router, prefix="/flag")
app.include_router(analytics.router, prefix="/analytics")