import logging
from contextlib import asynccontextmanager
from core.models import db_helper
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from logging_config import configure_logging
from api import router as api_router
from utils.measure_time import a_measure_time
from core.config import settings


# origins = [
#     settings.run.WEBSITE_HOSTNAME
# ]

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Starting application : lifespan")
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

# main_app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # Allow only specified origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allow all headers
# )

main_app.include_router(
    api_router,
)


@main_app.middleware("http")
@a_measure_time
async def log_request(request: Request, call_next):
    return await call_next(request)
