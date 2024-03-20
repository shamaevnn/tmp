import asyncio
import logging
import sys

from app.db.base import database

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


async def connect_to_db() -> None:
    for i in range(1, 6):
        logger.info(f"Connecting to Database, attempt {i}")

        try:
            await database.connect()
        except ConnectionRefusedError:
            time_to_sleep = 1 * i
            logger.info(f"Trying to connect DB after {time_to_sleep} seconds...")
            await asyncio.sleep(time_to_sleep)
        else:
            break


async def close_db_connection() -> None:
    logger.info("Closing connection to database")

    await database.disconnect()

    logger.info("Connection closed")
