from __future__ import annotations

import time
import typing as t

T = t.TypeVar("T")


class FixedBucket(t.Generic[T]):
    """
    Fixed size FIFO container.
    """

    def __init__(self, size: int):
        self._data: list[T | None] = [None] * size
        self._cur = 0
        self._size = size
        self._flag_full = False

    def put(self, v: T):
        self._data[self._cur] = v
        self._cur += 1
        if self._cur == self._size:
            self._cur = 0
            self._flag_full = True

    @property
    def data(self):
        return self._data[: self._cur] if not self._flag_full else self._data

    def __len__(self):
        return self._cur if not self._flag_full else self._size

    def __getitem__(self, sl: slice):
        if not self._flag_full:
            return self._data[: self._cur][sl]
        return (self._data[self._cur :] + self._data[: self._cur])[sl]


class TokenBucket:
    """
    Dynamic token bucket
    """

    def __init__(self, init_amount: int = 0):
        self._amount = init_amount
        self._last_consume_time = time.time()

    def consume(self, take_amount: int, avg_rate: float, burst_size: int):
        now = time.time()
        inc = (now - self._last_consume_time) * avg_rate
        current_amount = min(inc + self._amount, burst_size)
        if take_amount > current_amount:
            return False
        self._amount, self._last_consume_time = current_amount - take_amount, now
        return True
