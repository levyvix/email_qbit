from pathlib import Path

from loguru import logger


# Configure loguru
def setup_logger():
    log_path = Path(__file__).parent.parent / "logs"
    log_path.mkdir(exist_ok=True)

    # Remove default handler
    logger.remove()

    # Add file handler
    logger.add(
        log_path / "email_notifications.log",
        rotation="1 day",
        retention="7 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )

    # Add console handler
    logger.add(
        lambda msg: print(msg),
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )

    return logger


# Initialize logger
logger = setup_logger()
