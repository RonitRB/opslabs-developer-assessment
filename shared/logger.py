"""Small consistent logger configuration for CLI and service modules."""
import logging

from shared.config import settings


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    return logging.getLogger(name)
