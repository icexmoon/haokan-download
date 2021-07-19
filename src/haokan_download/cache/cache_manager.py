from .cache_interface import CacheInterface
from .file_cache import FileCache


class CacheManager:
    """缓存管理"""
    cache: CacheInterface = None

    @classmethod
    def getCache(cls) -> CacheInterface:
        """获取当前系统使用的缓存模块"""
        if (cls.cache is None):
            cls.cache = FileCache()
        return cls.cache
