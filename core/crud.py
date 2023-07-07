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


def update_domain(db: Session, domain: models.Domain):
    db.add(domain)
    db.commit()
    return domain


def delete_domain(domain_url: str, db: Session):
    domain = db.query(models.Domain).filter(models.Domain.url == domain_url).first()
    if not domain:
        return False
    db.delete(domain)
    db.commit()
    return True
