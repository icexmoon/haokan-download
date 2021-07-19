from typing import Any
from .cache_interface import CacheInterface


class NoneCache(CacheInterface):
    def addCachedData(self, key: str, value: Any) -> None:
        pass

    def getCachedData(self, key, expired: float) -> Any:
        return None

    def save(self) -> None:
        pass
