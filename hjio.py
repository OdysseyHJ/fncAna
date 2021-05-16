
import os

iobuf = ''
iobufLen = 10000
logpath = ''

def  wirteCSV(strInfo, path):
    dirCC(path)
    with open(path, 'w+') as fp:
        fp.write(strInfo)

def wirteText(strInfo, path):
    dirCC(path)
    with open(path, 'w+') as fp:
        fp.write(strInfo)

def readFile(path, mode = 'r'):
    with open(path, mode) as fp:
        return fp.read()


def dirCC(path):
    pathlist = path.split(os.path.sep)
    for i in range(1,len(pathlist)):
        prefixPath = (os.path.sep).join(pathlist[:i])
        if not os.path.exists(prefixPath):
            os.mkdir(prefixPath)
    return prefixPath


def init(filepath):
    pass

def hjlog(strLoginfo):
    global iobuf
    iobuf += (strLoginfo + '\n')
    if len(iobuf) >= iobufLen:
        return

def writelog():
    pass