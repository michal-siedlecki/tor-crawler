from fastapi import FastAPI
from core.config import settings
from core import models, routes
from .database import engine

models.BaseModel.metadata.create_all(bind=engine)


description = """
Tor Crawler Description
"""


app = FastAPI(
    title="Dates facts - REST API",
    openapi_url="/openapi.json",
    secret_key=settings.APP_SECRET_KEY,
    description=description,
    version="0.0.1",
    contact={
        "name": "Michał Siedlecki",
        "email": "siedlecki.michal@gmail.com",
    },
)

app.include_router(routes.router)
