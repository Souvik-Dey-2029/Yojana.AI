from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    icon = Column(String, default="📋")
    description = Column(String)
    benefits = Column(String)
    max_income = Column(Integer)
    eligible_states = Column(JSON) # List of states
    eligible_occupations = Column(JSON)
    eligible_categories = Column(JSON)
    gender = Column(String, nullable=True) # "Male", "Female", or null
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)
    land_owned_required = Column(Boolean, default=False)
    required_documents = Column(JSON)
    deadline = Column(String)
    apply_url = Column(String)
    category = Column(String) # e.g., "Education", "Agri", "Social"
    guidance_steps = Column(JSON) # List of specific application steps

class UserSubscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_identifier = Column(String, unique=True, index=True)
    plan_type = Column(String, default="Free") # "Free", "Pro", "NGO"
    is_active = Column(Boolean, default=True)
