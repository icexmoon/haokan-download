import getopt
import sys
from .main import Main


def main():
    try:
        opts, args = getopt.gnu_getopt(
            sys.argv[1:], 'u:l:', ['uid=', 'limit='])
    except getopt.GetoptError as e:
        print("获取参数信息出错，错误提示：", e.msg)
        exit()
    mainProcess = Main()
    if len(opts) == 0:
        print("必须要至少输入参数uid")
        exit()
    else:
        uid = None
        limit = None
        for argKey, argVal in opts:
            if argKey == '-u' or argKey == '--uid':
                uid = argVal
            elif argKey == '-l' or argKey == '--limit':
                limit = int(argVal)
            else:
                pass
        mainProcess.main(uid, limit)
    exit()


main()
