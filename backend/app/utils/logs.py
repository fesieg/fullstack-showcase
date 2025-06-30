import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOG_DIR / "bottle_return_system.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(name)s: %(message)s")

file_handler = RotatingFileHandler(
    str(LOG_FILE),
    maxBytes=1024 * 1024,
    backupCount=2,
)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.propagate = False


def configure_logging() -> None:
    # capture uvicorn logs
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.addHandler(file_handler)

    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.addHandler(file_handler)

    # capture FastAPI logs
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.addHandler(file_handler)
    fastapi_logger.setLevel(logging.INFO)

    # set root logger level
    logging.getLogger().setLevel(logging.INFO)
