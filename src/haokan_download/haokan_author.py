import requests
from bs4 import BeautifulSoup
import random
import time
from .cache.cache_manager import CacheManager


class HaokanAuthor():
    TEN_HOURS = 10*3600

    def __init__(self, authorId):
        self.authorId = authorId
        self.name = ""
        self.videoList = []
        self.proxies = [
            {"http": "http://27.192.200.7:9000",
                "https": "http://103.103.3.6:8080"},
            {"http": "http://113.237.3.178:9999",
             "https": "http://113.237.3.178:9999"},
            {"http": "http://61.37.223.152:8080",
             "https": "http://45.228.188.241:999"},
            {"http": "http://118.117.188.171:3256",
             "https": "http://118.117.188.171:3256"},
            {"http": "http://104.254.238.122:20171",
             "https": "http://104.254.238.122:20171"},
            {"http": "http://47.104.66.204:80",
             "https": "http://211.24.95.49:47615"},
            {"http": "http://191.101.39.193:80",
             "https": "http://103.205.15.97:8080"},
            {"http": "http://112.104.28.117:3128",
             "https": "http://190.108.88.97:999"},
            {"http": "http://185.179.30.130:8080",
             "https": "http://185.179.30.130:8080"},
            {"http": "http://218.88.204.125:3256",
             "https": "http://81.30.220.116:8080"},
            {"http": "http://178.62.56.172:80",
             "https": "http://190.85.244.70:999"},
            {"http": "http://178.134.208.126:50824",
             "https": "http://178.134.208.126:50824"},
            {"http": "http://193.149.225.163:80",
             "https": "http://118.99.100.164:8080"},
            {"http": "http://182.87.136.228:9999",
             "https": "http://45.236.168.183:999"},
            {"http": "http://175.42.122.142:9999",
             "https": "http://175.42.122.142:9999"},
            {"http": "http://192.109.165.128:80",
             "https": "http://188.166.125.206:38892"},
            {"http": "http://181.3.91.56:10809",
             "https": "http://190.85.244.70:999"},
            {"http": "http://182.84.144.91:3256",
                "https": "http://182.84.144.91:3256"},
            {"http": "http://167.172.180.46:33555",
                "https": "http://167.172.180.46:33555"},
            {"http": "http://58.255.7.90:9999", "https": "http://58.255.7.90:9999"},
        ]
        self.useProxy = False
        self.headers = {
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    def getAuthorName(self):
        if self.name == "":
            self.name = self.getAuthorNameFromWeb()
        return self.name

    def getAuthorNameFromWeb(self):
        # ???????????????????????????
        cachedKey = "getAuthorNameFromWeb.{}".format(self.authorId)
        cache = CacheManager.getCache()
        cachedData = cache.getCachedData(cachedKey, self.__class__.TEN_HOURS)
        if cachedData is not None:
            return cachedData
        url = "https://haokan.hao123.com/author/"+self.authorId
        resp = self.tryRequestGet(url)
        # ???????????????????????????????????????????????????????????????
        resp.encoding = 'UTF-8'
        authorPageHtml = resp.text
        authorPageDom = BeautifulSoup(authorPageHtml, features="html5lib")
        # ????????????????????????
        authorNameTag = authorPageDom.find("h1", class_="uinfo-head-name")
        authorName = authorNameTag.string
        # ????????????
        cache.addCachedData(cachedKey, authorName)
        cache.save()
        return authorName

    def getVideoList(self):
        # ?????????
        # videoName1="?????????????????????2???"
        # videoName2="??????18??????????????????9???10??????1???2???1???"
        # videoSrc1="http://haokan.hao123.com/v?vid=15779938508150317940"
        # videoSrc2="http://haokan.hao123.com/v?vid=10123773370840967415"
        # return [{"videoName":videoName1,"videoSrc":videoSrc1},{"videoName":videoName2,"videoSrc":videoSrc2}]
        # ???????????????????????????
        cache = CacheManager.getCache()
        cachedKey = "getVideoList.{}".format(self.authorId)
        cachedData = cache.getCachedData(cachedKey, self.__class__.TEN_HOURS)
        if cachedData is not None:
            self.videoList = cachedData
        if len(self.videoList) > 0:
            return self.videoList
        self.dealHaokanResponse("https://haokan.hao123.com/author/" +
                                self.authorId+"?_format=json&rn=16&ctime=0&_api=1")
        # ?????????????????????
        cache.addCachedData(cachedKey, self.videoList)
        cache.save()
        return self.videoList

    def dealResponse(self, response):
        ctime = response['ctime']
        results = response['results']
        if len(results) > 0:
            for video in results:
                videoContent = video['content']
                videoName = videoContent['title']
                vid = videoContent['vid']
                videoSrc = "https://haokan.baidu.com/v?vid={!s}".format(vid)
                self.videoList.append(
                    {"videoName": videoName+'.flv', "videoSrc": videoSrc})
        return "https://haokan.hao123.com/author/"+self.authorId+"?_format=json&rn=16&ctime="+str(ctime)+"&_api=1"

    def dealHaokanResponse(self, url):
        resp = self.tryRequestGet(url)
        respJson = resp.json()
        response = respJson['data']['video']
        if int(response['response_count']) > 0:
            nextRequestUrl = self.dealResponse(response)
            self.dealHaokanResponse(nextRequestUrl)

    def getRandomProxy(self) -> dict:
        total = len(self.proxies)
        randomIndex = random.randint(1, total)-1
        return self.proxies[randomIndex]

    def tryRequestGet(self, url: str, tryTimes: int = 0):
        try:
            if self.useProxy:
                resp = requests.get(url, headers=self.headers,
                                    proxies=self.getRandomProxy())
            else:
                resp = requests.get(url, headers=self.headers)
        except requests.exceptions.ProxyError as e:
            if tryTimes >= 5:
                tryTimes += 1
                return self.tryRequestGet(url, tryTimes)
            else:
                print(e)
        else:
            print("3?????????????????????")
            time.sleep(3)
            return resp
