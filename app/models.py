from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from datetime import datetime
from app.database import Base

class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_active = Column(Boolean, default=True)


class Variant(Base):
    __tablename__ = "variants"
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    name = Column(String)
    weight = Column(Integer)


class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    experiment_id = Column(Integer)
    variant_id = Column(Integer)


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer)
    variant_id = Column(Integer)
    user_id = Column(String)
    event_type = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class FeatureFlag(Base):
    __tablename__ = "feature_flags"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    is_enabled = Column(Boolean)
    rollout_percentage = Column(Integer)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="developer")