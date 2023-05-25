import os
import threading

from loguru import logger
import psycopg2
import redis

from src.collecter import collect_images
from src.processer import process_images
from src.settings import Settings
import src.redis_queue


IMAGE_DIRECTORY = "./images"
TABLE_NAME = "images"


if __name__ == "__main__":
    # Counting files in image directory
    count = 0
    for path in os.listdir(IMAGE_DIRECTORY):
        if os.path.isfile(os.path.join(IMAGE_DIRECTORY, path)):
            count += 1
    logger.debug(f"There is {count} files in directory.")

    # Creating Redis and Postgres connections
    settings = Settings()
    with redis.Redis(host=settings.redis_host, port=settings.redis_port) as redis_conn:
        with psycopg2.connect(
            database=settings.pg_database,
            user=settings.pg_user,
            password=settings.pg_password,
            host=settings.pg_host,
            port=settings.pg_port,
        ) as postgres_conn:
            logger.info("PG and Redis connected.")

            # Checking if table in Postgres exists and creating if not
            with postgres_conn.cursor() as cur:
                cur.execute(
                    f"CREATE TABLE IF NOT EXISTS public.{TABLE_NAME} "
                    "(added_at timestamptz, size_bytes integer);"
                )

            # Creating queue to store images
            redis_queue = src.redis_queue.RedisQueue("image_queue", redis_conn)

            # Starting 2 threads to collect and process images
            image_collect_thread = threading.Thread(
                target=collect_images, args=(IMAGE_DIRECTORY, redis_queue)
            )
            image_process_thread = threading.Thread(
                target=process_images,
                args=(count, TABLE_NAME, redis_queue, postgres_conn),
            )
            image_collect_thread.start()
            image_process_thread.start()
