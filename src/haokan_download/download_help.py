import sys
import os
from urllib import request
from .config import config


class DownloadHelp():
    def processReport(self, a, b, c):
        per = 100.0*a*b/c
        if per > 100:
            per = 1
        # sys.stdout.write(" "+"%.2f%% 已经下载的大小：%1d 文件大小：%1d"%(per,a*b,c)+'\r')
        # sys.stdout.flush()

    def download(self, url, fileName):
        request.urlretrieve(url, filename=fileName,
                            reporthook=self.processReport)

    def downloadByYouget(self, url, outputFile):
        if not os.path.exists(outputFile):
            os.mkdir(outputFile)
        print("you-get {} -o {}".format(url, outputFile))
        os.system('you-get "{}" -o "{}"'.format(url, outputFile))
