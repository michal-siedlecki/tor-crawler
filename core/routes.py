import time
from typing import List, Optional, Iterable
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from core import crud, database, schemas, models, crawler, parser


class Router(APIRouter):
    crawl = True


router = Router(tags=["crawler api"], responses={404: {"description": "Not found"}})


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
def get_domains(db: Session = Depends(get_db)) -> Iterable[schemas.DomainSchema]:
    """
    Fetches list of domains from database
    """
    domains = crud.get_domains(db)
    return domains


@router.post(
    "/domains",
    status_code=status.HTTP_201_CREATED,
    response_model=Optional[schemas.DomainSchema],
)
def post_domain(
    url: str, db: Session = Depends(get_db)
) -> Optional[schemas.DomainSchema]:
    """
    Creates domain entry in database
    """
    if not router.crawl:
        return None
    url = parser.clean_url(url)
    requested_domain = models.Domain(url=url)
    existing_domains = get_domains(db)
    if requested_domain in existing_domains:
        return requested_domain
    new_domain = crud.create_domain(db, url=url)
    return new_domain


@router.post("/crawl", status_code=status.HTTP_200_OK)
def crawl(url: str, db: Session = Depends(get_db)) -> Optional[Iterable[str]]:
    """
    Run crawler for requested domain
    """
    requested_domain = post_domain(url=url, db=db)
    if requested_domain.last_visited:
        return None
    crawler_spider = crawler.Crawler(url=url)
    response_content = crawler_spider.get_page()
    requested_domain.last_visited = int(time.time())
    domain = crud.get_domain(db, requested_domain.url)
    crud.update_domain(db, domain=domain)
    if not response_content:
        return None
    requested_domain.is_thread = parser.is_bad_domain(response_content)
    child_domains = parser.extract_unique_domains(response_content)
    for d in child_domains:
        post_domain(d, db)
    return None


@router.delete("/domains", status_code=status.HTTP_204_NO_CONTENT)
def delete_domain(url: str, db: Session = Depends(get_db)):
    """
    Removes domain entry from database
    """
    if not crud.delete_domain(url, db):
        return None
    return None
