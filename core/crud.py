from typing import Optional
from sqlalchemy.orm import Session

from core import models, logger


def get_domains(db: Session) -> list:
    return db.query(models.Domain).all()


def get_domain(db: Session, url: str) -> Optional[models.Domain]:
    domain = db.query(models.Domain).filter_by(url=url).first()
    return domain


def create_domain(db: Session, **domain_data) -> models.Domain:
    new_domain = models.Domain(**domain_data)
    db.add(new_domain)
    db.commit()
    return new_domain


def update_domain(db: Session, domain: models.Domain):
    db.add(domain)
    db.commit()
    return domain


def delete_domain(domain_url: str, db: Session):
    domain = get_domain(db, domain_url)
    if not domain:
        return False
    db.delete(domain)
    db.commit()
    return True
