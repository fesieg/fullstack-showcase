from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.db.db_setup import init_db
from app.utils.logs import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001, ANN201
    # startup
    logger.info("Starting up the Bottle Return System API")
    logger.info("Initializing the database...")
    configure_logging()
    init_db()
    yield
    # shutdown


app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # all origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],  # allow all headers
)

app.include_router(api_router)
