import uuid

from sqlalchemy.orm import Session
from core import models


def get_domains(db: Session):
    return db.query(models.Domain).all()


def create_domain(db: Session, **domain_data):
    new_domain = models.Domain(**domain_data)
    db.add(new_domain)
    db.commit()
    return new_domain


def delete_domain(domain_id: uuid.UUID, db: Session):
    domain = db.query(models.Domain).filter(models.Domain.id == domain_id).first()
    if not domain:
        return False
    db.delete(domain)
    db.commit()
    return True
