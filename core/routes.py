from typing import List, Optional
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from core import crud, database, schemas, models, crawler

router = APIRouter(tags=["dates"], responses={404: {"description": "Not found"}})


# Dependency
def get_db():
    db = database.session_local()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/domains",
    response_model=List[schemas.DomainSchema],
    status_code=status.HTTP_200_OK,
)
def get_domains(db: Session = Depends(get_db)) -> list[schemas.DomainSchema]:
    """
    Fetches list of domains from database
    """
    domains = crud.get_domains(db)
    return domains


@router.post("/domains", status_code=status.HTTP_201_CREATED)
def post_domain(
    url: str, db: Session = Depends(get_db)
) -> Optional[schemas.DomainSchema]:
    """
    Creates domain entry in database
    """
    requested_domain = models.Domain(url=url)
    existing_domains = get_domains(db)
    if requested_domain in existing_domains:
        # TODO: Perhaps an other response code should be returned
        return None
    new_domain = crud.create_domain(db, url=url)
    return new_domain


@router.post("/crawl", status_code=status.HTTP_200_OK)
def crawl(url: str, db: Session = Depends(get_db)) -> Optional[str]:
    """
    Run crawler for requested domain
    """
    requested_domain = post_domain(url=url, db=db)
    # If post request return None means that the domain exists in db and no need to visit
    if not requested_domain:
        return None
    response_content = crawler.get(requested_domain.url)
    return response_content.decode("utf-8")


@router.delete("/domains", status_code=status.HTTP_200_OK)
def delete_domain(url: str, db: Session = Depends(get_db)):
    """
    Removes domain entry from database
    """
    if not crud.delete_domain(url, db):
        return None
    return None
