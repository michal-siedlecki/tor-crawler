import uuid
import requests
from typing import List
from fastapi import APIRouter, Body, Header, Depends
from starlette import status
from sqlalchemy.orm import Session

from core.config import settings

from core import crud, utils, database, schemas, models

router = APIRouter(tags=["api"], responses={404: {"description": "Not found"}})


# Dependency
def get_db():
    db = database.session_local()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/domains/",
    response_model=List[schemas.DomainSchema],
    status_code=status.HTTP_200_OK,
)
def read_domains(db: Session = Depends(get_db)):
    domains = crud.get_domains(db)
    return domains


@router.post(
    "/domains/",
    response_model=schemas.DomainSchema,
    status_code=status.HTTP_201_CREATED,
)
def post_domain(
    url: str = Body(..., title="url"),
    db: Session = Depends(get_db),
):
    date_fact = crud.create_domain(db=db, url=url)
    return date_fact


@router.post("/visit/")
def visit_url(url: str):
    proxy = {"http": settings.TOR_PROXY}
    response = requests.get(url, proxies=proxy)
    post_domain(url=url)
    return response.status_code
