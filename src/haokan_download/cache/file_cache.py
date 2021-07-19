from typing import Any
from .cache_interface import CacheInterface
from ..config import config
import time
import os
import json


class FileCache(CacheInterface):
    """文件缓存"""

    def __init__(self) -> None:
        super().__init__()
        self._cachedData: dict = {}  # 加载到内存中的缓存数据
        self._fileName: str = "cached.tmp"  # 缓存文件名称
        self._fileDir: str = "{}{}tmp".format(
            config["sysHome"], config["path"])  # 缓存文件目录
        self._filePath: str = "{}{}{}".format(
            self._fileDir, config["path"], self._fileName)  # 缓存文件保存路径
        # 从缓存文件加载缓存数据到内存
        self._loadCachedDataFromFile()

    def addCachedData(self, key: str, value: Any) -> None:
        currentTime = time.time()
        self._cachedData[key] = {"time": currentTime, "data": value}

    def getCachedData(self, key, expired: float = 1800) -> Any:
        if key not in self._cachedData:
            return None
        cachedData = self._cachedData[key]
        cachedTime = cachedData["time"]
        if(time.time() - cachedTime > expired):
            # 被缓存的数据已经过期
            self._cachedData.pop(key)
            return None
        else:
            # 没有过期
            return cachedData["data"]

    def save(self) -> None:
        self._saveCachedDataToFile()

    def _loadCachedDataFromFile(self):
        if not os.path.exists(self._filePath):
            # 缓存文件不存在,不加载
            pass
        else:
            # 从缓存文件加载到内存
            with open(file=self._filePath, mode='r', encoding='UTF-8') as fopen:
                text = fopen.read()
                if len(text) == 0:
                    pass
                else:
                    self._cachedData = json.loads(text)

    def _saveCachedDataToFile(self):
        if not os.path.exists(self._fileDir):
            os.mkdir(self._fileDir)
        fopen = open(file=self._filePath, mode='w', encoding='UTF-8')
        print(json.dumps(self._cachedData), file=fopen)
        fopen.close()
