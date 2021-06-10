
import os
import setting
import csv

iobuf = ''
iobufLen = 10000
logpath = ''
slash = '\\'

rootpath = setting.rootpath
# fucntion
def makepath(root, sub):
    pathSeq = (root, sub)
    return slash.join(pathSeq)

def  wirteCSV(strInfo, path, wroot = False):
    if wroot:
        path = makepath(rootpath, path)
    dirCC(path)
    with open(path, 'w+') as fp:
        fp.write(strInfo)

def writeCsvbyList(linelist, path):
    fp = open(path, 'w', newline='')
    cfpw = csv.writer(fp)
    for line in linelist:
        cfpw.writerow(line)
    fp.close()


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
    global logpath
    logpath = filepath
    print('logpath')
    print(logpath)


def writelog(strLoginfo):
    global iobuf
    iobuf += (strLoginfo + '\n')
    if len(iobuf) >= iobufLen:
        clearbuf()
    return

def clearbuf(strTail=''):

    global iobuf
    iobuf += strTail
    with open(logpath, 'a') as fp:
        fp.write(iobuf)
    iobuf = ''