from sqlalchemy.orm import Session
from .db_models import Scheme

def get_schemes(db: Session):
    return db.query(Scheme).all()

def get_scheme_by_id(db: Session, scheme_id: str):
    return db.query(Scheme).filter(Scheme.id == scheme_id).first()

def get_eligible_schemes(db: Session, filter_criteria: dict = None):
    query = db.query(Scheme)
    # Advanced filtering can be added here
    return query.all()
