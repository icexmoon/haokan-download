import platform
import os
pwd = os.getcwd()
windowsHomePath = pwd
LinuxHomePath = pwd
config = {}
sysName = platform.system()
if sysName == "Windows":
    config["path"] = "\\"
    config["saveHome"] = windowsHomePath
elif sysName == "Linux":
    config["path"] = "/"
    config["saveHome"] = LinuxHomePath
else:
    print("本程序不支持当前操作系统")
    exit()
