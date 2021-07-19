from abc import ABC, abstractmethod
from typing import Any


class CacheInterface(ABC):
    @abstractmethod
    def addCachedData(self, key: str, value: Any) -> None:
        """缓存数据
        key: 索引
        value: 被缓存的数据
        """
        pass

    @abstractmethod
    def getCachedData(self, key, expired: float = 1800) -> Any:
        """获取缓存数据
        key: 索引
        expired: 过期时间,单位秒,默认半小时
        """
        pass

    @abstractmethod
    def save(self)->None:
        """将缓存数据持久化保存"""
        pass
