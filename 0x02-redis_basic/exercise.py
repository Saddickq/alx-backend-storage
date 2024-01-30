#!/usr/bin/env python3
""" redis basics"""


import redis
from typing import Union, Optional, Callable
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """doc class"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """doc class"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """doc class"""
    inkey = method.__qualname__ + ":inputs"
    outkey = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """doc class"""
        self._redis.rpush(inkey, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(outkey, str(res))
        return res

    return wrapper


def replay(method: Callable) -> None:
    """doc class"""
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))
    for inp, out in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                method.__qualname__, inp.decode("utf-8"), out.decode("utf-8")
            )
        )


class Cache:
    """class docs"""
    def __init__(self):
        """class initialisation"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """method docs"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """ doc method"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """doc method"""
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        """doc method"""
        return self.get(key, fn=int)
