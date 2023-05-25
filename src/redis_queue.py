from typing import Any

import redis


class RedisQueue:
    """Simple Redis queue implementation."""

    def __init__(self, name: str, redis_conn: redis.Redis):
        self.__db = redis_conn
        self.key = f"{name}"

    def qsize(self) -> int:
        return self.__db.llen(self.key)

    def empty(self) -> bool:
        return self.qsize() == 0

    def put(self, item) -> None:
        self.__db.rpush(self.key, item)

    def get_blocking(self, timeout=None) -> Any:
        item = self.__db.blpop(self.key, timeout=timeout)
        if item:
            item = item[1]
        return item

    def get(self) -> Any:
        item = self.__db.lpop(self.key)
        if item:
            item = item[1]
        return item
