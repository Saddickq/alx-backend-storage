#!/usr/bin/env python3


import redis
from typing import Union, Optional, Callable
from uuid import uuid4


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """doc doc method"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """doc doc method"""
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        """doc doc method"""
        return self.get(key, fn=int)
