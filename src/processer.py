import datetime

from loguru import logger
from psycopg2.extensions import connection

import src.redis_queue


def process_images(
    file_count: int,
    table_name: str,
    redis_queue: src.redis_queue.RedisQueue,
    postgres_conn: connection,
):
    """Enque image from redis and store it's size in postgres."""
    logger.info("Starting recieving of images from Redis")

    counter = 0
    while counter < file_count or not redis_queue.empty():
        counter += 1
        image_bytes = redis_queue.get_blocking()
        logger.debug(f"Image number {counter} dequed.")
        if image_bytes:
            timestamp = datetime.datetime.now()
            size_bytes = len(image_bytes)
            with postgres_conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO {table_name} (added_at, size_bytes) VALUES (%s, %s)",
                    (timestamp, size_bytes),
                )
                postgres_conn.commit()
                logger.debug(f"Image number {counter} saved in DB.")
