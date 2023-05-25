import os

from loguru import logger

import src.redis_queue


def collect_images(image_dir: str, redis_queue: src.redis_queue.RedisQueue):
    """Read images from directory and add it to Redis queue."""
    logger.info("Starting queuing images in Redis.")
    for filename in os.listdir(image_dir):
        filepath = os.path.join(image_dir, filename)
        with open(filepath, "rb") as f:
            image_bytes = f.read()
            redis_queue.put(image_bytes)
            logger.debug(f"Image {filepath} queued.")
