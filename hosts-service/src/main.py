from contextlib import asynccontextmanager

from fastapi import FastAPI

from router import router
from config.database import start_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)
