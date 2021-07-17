import sys
from .download_help import DownloadHelp
import os
from .config import config
from .haokan_author import HaokanAuthor
class Main():
    def programExit(self, message):
        sys.stdout.writelines([message+"\r\n", "program exit"])
        exit()

    def main(self, authorId, limit=None):
        haokanAuthor = HaokanAuthor(authorId)
        authorName = haokanAuthor.getAuthorName()
        if len(authorName) == 0:
            self.programExit("没有找到视频作者信息，请检查作者id是否有误")
        sys.stdout.write("匹配到视频作者："+authorName+"\r\n")
        # 读取存储目录，检查是否有用户名称命名的文件夹，若没有，新建
        saveHome = config['saveHome']
        nowSaveDir = saveHome+config['path']+authorName+'('+authorId+')'
        if not os.path.exists(nowSaveDir):
            os.mkdir(nowSaveDir)
            sys.stdout.writelines(["创建视频存储目录："+nowSaveDir+"\r\n"])
        # 读取视频作者的所有视频列表
        sys.stdout.write("正在查询该作者的所有视频，请稍候\r\n")
        videoList = haokanAuthor.getVideoList()
        # print(videoList)
        # exit()
        videoNum = len(videoList)
        if videoNum == 0:
            self.programExit("没有找到该作者的视频列表")
        # 从本地读取已下载文件列表
        localVideoList = os.listdir(nowSaveDir)
        # 如果本地已经有视频中没有，加入待下载列表
        downloadList = []
        if len(localVideoList) > 0:
            for videoItem in videoList:
                if not videoItem['videoName'] in localVideoList:
                    downloadList.append(videoItem)
        else:
            # 本地没有已下载视频，将视频列表全部加入待下载列表
            downloadList = videoList
        # 如果指定限量下载，对待下载列表切片
        if limit is not None:
            limit = int(limit)
            downloadList = downloadList[:limit]
        videoNum = len(downloadList)
        if videoNum == 0:
            self.programExit("该作者的视频均已下载到本地")
        sys.stdout.write("总共找到视频作者"+authorName+"的"+str(videoNum)+"个未下载视频，是否开始下载：(y/n)")
        command = input()
        if command != 'y':
            self.programExit("用户取消下载")
        sys.stdout.write("开始下载，总共"+str(videoNum)+"个视频\r\n")
        downloader = DownloadHelp()
        alreadyDownNum = 0
        for videoInfo in downloadList:
            downloader.downloadByYouget(videoInfo['videoSrc'],
                                nowSaveDir+config["path"]+videoInfo['videoName'])
            alreadyDownNum += 1
            p = 100.0*alreadyDownNum/videoNum
            if p < 1:
                p = 1
            sys.stdout.write(" 下载进度 %.2f%%" % (p)+" 最新下载的文件为 " +
                            videoInfo['videoName']+"\r\n")
        self.programExit("全部文件已下载完毕")
