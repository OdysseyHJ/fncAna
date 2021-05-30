import re
import os
import hashlib

import hjio
import fncData
from commonDef import HexinIni

# fnc解码映射表
g_decodeSymbolMap = {
    r'\^a'    :';',
    r'\^p'    :'(',
    r'\^P'    :')',
    r'\^s'    :'-',
    r'\^e'    :'=',
    r'\^c'    :',',
    r'\^r^n'  :r'\n',
    r'\^n'    :r'\n',
    r'\^r'    :r'\n',
    r'\^b'    :'[',
    r'\^B'    :']',
    r'\\t'     :'    ',

}

# fnc编码映射表
g_encodeSymbolMap = {
    '\)': r'^P',
    '\(': r'^p',
    ';': r'^a',
    '-': r'^s',
    '=': r'^e',
    ',': r'^c',
    '\[': r'^b',
    '\]': r'^B',
    r'\r\n': r'^r^n',
    r'\r': r'^r^n',
    r'\n': r'^r^n',
}

# key:CS实例名  value:HexinIni obj
g_hexinIniDict = {}

DIR_PLUGINS = 'plugins'
DIR_FREE = '@free'
DIR_LEVEL2 = '@level2'

# dir bit map
DIR_BIT_PLUGINS = 1
DIR_BIT_FREE = 2
DIR_BIT_LEVEL2 = 4



class fncObj:

    def __init__(self, id=0):
        self.id = id
        self.name = ''     #公式名
        self.fname = ''   #文件名
        self.path = ''     #文件路径
        self.content = '' #全部公式文件内容
        self.body = ''  #去除公式名字的文件内容
        self.directory = 0  #plugins/free/level2
        self.hostname = ''  #hostname
        self.period = 0  #适用周期
        self.algrithm = ''  #算法

    def showInfo(self):
        infoTmp = 'ID: {}  Name: {}  Fname: {}  Directory: {}\nPath: {}\nContent: {}\nBody: {}\n'
        strInfo = infoTmp.format(self.id, self.name, self.fname, self.directory, self.path, self.content, self.body)
        print(strInfo)

    def getDirBit(self):
        if self.directory == DIR_PLUGINS:
            return DIR_BIT_PLUGINS
        elif self.directory == DIR_FREE:
            return DIR_BIT_FREE
        elif self.directory == DIR_LEVEL2:
            return DIR_BIT_LEVEL2
        else:
            return 0



# 获取目标路径下的文本路径信息
# return [(current_path, [sub_path_list], [file_list]),(sub_path1, [sub_path_list], [file_list]), ...]
def getFileLib(folderPath):
    fileLib = []
    # print(os.walk(folderPath))
    for each in os.walk(folderPath):
        fileLib.append(each)

    return fileLib


# 获取路径下指定深度的目录路径
def getPathDepth(folderPath, depth = 1, fullPath = True):
    rootDepth = len(folderPath.split(os.path.sep))
    pathList = []
    endFlag = False

    for root, dirs, files in os.walk(folderPath):
        for name in dirs:
            # print(name)
            dirPath = os.path.join(root, name)
            dirDepth = len(dirPath.split(os.path.sep))
            if depth == (dirDepth - rootDepth):
                if fullPath:
                    pathList.append(dirPath)
                else:
                    pathList.append(name)
            elif depth < (dirDepth - rootDepth):
                endFlag = True
                break
        # if endFlag:
        #     break;

    return pathList


# 获取路径下指定深度的目录路径
def getFileDepth(folderPath, depth, fullPath = True):
    rootDepth = len(folderPath.split(os.path.sep))
    fileList = []
    endFlag = False

    for root, dirs, files in os.walk(folderPath):
        for fname in files:
            filePath = os.path.join(root, fname)
            dirDepth = len(filePath.split(os.path.sep))
            if depth == (dirDepth - rootDepth):
                if fullPath:
                    fileList.append(filePath)
                else:
                    fileList.append(fname)
            elif depth < (dirDepth - rootDepth):
                break


    return fileList

# 获取路径下fnc文件计数
# return (cntPlugin, cntFree, cntLevel2, cntPlugin+cntFree+cntLevel2)
#  plugin  @free  @level2  total
def getFncfileCount(folderPath):
    # pathName = folderPath.split(os.path.sep)[-1]
    cntPlugin = 0
    cntFree = 0
    cntLevel2 = 0

    fileLib = getFileLib(folderPath)
    for each in fileLib:

        if DIR_FREE in each[0].split('\\'):
            # cntFree += len(each[2])
            for file in each[2]:
                if isFncFile(file):
                    cntFree += 1
        elif DIR_LEVEL2 in each[0].split('\\'):
            # cntLevel2 += len(each[2])
            for file in each[2]:
                if isFncFile(file):
                    cntLevel2 += 1
        else:
            # cntPlugin += len(each[2])
            for file in each[2]:
                if isFncFile(file):
                    cntPlugin += 1

    return (cntPlugin, cntFree, cntLevel2, cntPlugin+cntFree+cntLevel2)


# 公式解码
def fncDecode(strFBody):
    decodedFBody = strFBody
    for key in g_decodeSymbolMap.keys():
        decodedFBody = re.sub(key, g_decodeSymbolMap[key], decodedFBody, count = 0)

    return decodedFBody

# 公式编码
def fncEncode(strFBody):
    encodedFBody = strFBody
    for key in g_encodeSymbolMap.keys():
        encodedFBody = re.sub(key, g_encodeSymbolMap[key], encodedFBody, count = 0)

    return encodedFBody


def getDesignedFilepath(filename, folderpath):
    filelib = getFileLib(folderpath)
    filepath = None
    for root, dirs, files in filelib:
        if filename in files:
            filepath = os.path.join(root, filename)
            break
    return filepath

def getVersion(rootPath):
    version = 'None'
    if None == rootPath:
        return version

    strInfo = str(hjio.readFile(rootPath, 'rb'))
    strPtn = r'(?<=version=).*'
    resList = re.findall(strPtn, strInfo)


    if len(resList) > 0:
        version = resList[0].split('\\n')[0]


    return version




g_statisTabhead = ('Hostname',
                   'CS实例',
                   'CS目录',
                   'plugins公式计数',
                 'free目录公式计数',
                 'level2目录公式计数',
                 '站点公式计数',
                 '公式缺失率',
                 '公式冲突率',
                 '公式冲突数',
                 '公式错误率',
                 '公式错误数',
                 '公式版本')


def genFncStatistciInfo(fileList, outputPath):
    strOut = ','.join(g_statisTabhead) + '\n'

    # hostname, CS目录, (统计信息), 缺失率, 冲突率, 错误率
    unitTmp = '{},{},{},{},{},{},{},{},{},{}\n'
    index = 1
    dedupFilter = set()
    hostSet = set()
    totaltoProcess = len(fileList)
    for path in fileList:
        pathName = path.split(os.path.sep)[-2]


        # 去重
        if pathName in dedupFilter:
            hjio.writelog('duplicated & filtered. host=' + pathName)
            continue
        dedupFilter.add(pathName)

        hostname = pathName.split('_hqserver')[0]
        hostSet.add(hostname)
        cspath = pathName.split('{}_'.format(hostname))[1].split('_plugins')[0]
        csinstance = '_'.join((hostname,cspath))

        # 打印处理进度
        print("process:{:.2f}%".format(index/totaltoProcess * 100))
        index += 1
        print(pathName)

        statisInfo = getFncfileCount(path)

        lossRatio = getRatioInAll(statisInfo[3], True)


        statisInfo = map(str, statisInfo)
        strStatisInfo = ','.join(statisInfo)

        # 处理hexin.ini文件，生产版本好信息，以及ID2NAME信息
        inHxinipath = getDesignedFilepath('hexin.ini', path)
        version = getVersion(inHxinipath)
        extpath = path.rsplit(os.path.sep, 1)[0]
        extHxinipath = getDesignedFilepath('hexin.ini', extpath)

        hxobj = hexinIniAnalysis(inHxinipath, extHxinipath, csinstance)
        g_hexinIniDict[csinstance] = hxobj
        hxidAllAddDict(hxobj)

        fncdict = getFncDict(path, hostname)
        errorStat = getErrorStat(fncdict)
        conflictStat = getConflictStat(fncdict)


        errorRatio = getRatioInAll(errorStat.total)
        conflictRatio = getRatioInAll(conflictStat.total)

        # gen fncAllmap 暂存
        fncAllmapAddDict(fncdict)

        #针对基准分析 base中缺少的公式：
        checkDictExist(fncdict)

        #统计冲突的公式id
        checkDictConflict(fncdict)

        strUnit = unitTmp.format(hostname, csinstance, cspath, strStatisInfo, lossRatio,
                                 conflictRatio, conflictStat.total,
                                 errorRatio, errorStat.total, version)
        strOut += strUnit


    hjio.wirteCSV(strOut, outputPath)

    hostlist = '\n'.join(hostSet)
    hjio.wirteCSV(hostlist, 'hostlist.csv', True)

def getRatioInAll(fncCnt, diff = False):
    Ratio = 0
    if diff:
        Ratio = (fncData.stdInfo[3] - fncCnt) / fncData.stdInfo[3]
    else:
        Ratio = fncCnt / fncData.stdInfo[3]
    Ratio = Ratio * 10000 // 1 / 100
    return Ratio



def isFncFile(filename):
    splitlist = filename.split('.')
    if len(splitlist) == 0:
        return False
    elif splitlist[-1] != 'fnc':
        return False
    return True





def getFncDict(folderPath, hostname = "None"):
    fncDict = {}
    filelib = getFileLib(folderPath)
    for root, dirs, files in filelib:
        for file in  files:
            if isFncFile(file) == False:
                hjio.writelog('getFncDict: not fnc file, name=' + file)
                continue

            filePath = os.path.join(root, file)
            with open(filePath, 'r') as fncFile:
                tmpfncObj = fncObj()
                try:
                    fnc = fncFile.read()
                except:
                    hjio.writelog('read fnc failed, fnc={}'.format(filePath))
                    continue

                # 去掉末尾换行、分号,按逗号分隔
                fncsplit = fnc.split('\n')[0].split(';')[0].split(',')
                if len(fncsplit) < 2:
                    hjio.writelog('getFncDict: error file, name=' + filePath)
                    continue
                try:
                    fncID = int(fncsplit[1])
                except:
                    hjio.writelog('read fnc failed, fnc={}'.format(filePath))
                    continue

                tmpfncObj.id = fncID
                tmpfncObj.fname = file
                tmpfncObj.path = filePath
                tmpfncObj.content = fnc
                tmpfncObj.name = fncsplit[0]
                tmpfncObj.body = fnc.split(',', 1)[1]
                tmpfncObj.hostname = hostname

                if len(fncsplit[3]) > 0:
                    tmpfncObj.algrithm = fncDecode(fncsplit[3])

                if len(fncsplit) == 5:
                    tmpfncObj.period = fncsplit[4]

                # print("hello " + hostname)

                pathSplit = filePath.split('\\')
                if DIR_FREE in pathSplit:
                    tmpfncObj.directory = DIR_FREE
                elif DIR_LEVEL2 in pathSplit:
                    tmpfncObj.directory = DIR_LEVEL2
                else:
                    tmpfncObj.directory = DIR_PLUGINS

                if fncID not in fncDict.keys():
                    fncDict[fncID] = [tmpfncObj]
                else:
                    fncDict[fncID].append(tmpfncObj)

    return fncDict

def checkIDexist(tup):
    existedTup = []
    for id in tup:
        if id in fncData.baseDict.keys():
            if len(fncData.baseDict[id]) > 1:
                hjio.writelog("basedict multiple! cnt=" + len(fncData.baseDict[id]))
            info = (id, fncData.baseDict[id][0].path)
            existedTup.append(info)
    return existedTup

class fncStat:
    fobjlist = []
    def __init__(self, plg = 0, free = 0, lvl2 = 0):
        self.plg = plg
        self.free = free
        self.lvl2 = lvl2
        self.total = plg+free+lvl2

    def showInfo(self):
        print(self.plg, self.free, self.lvl2, self.total)

    def refresh(self):
        self.total = self.plg + self.free + self.lvl2
        return self

def getErrorStat(compDict):

    errorStat = fncStat()
    for key in compDict.keys():
        for fobj in compDict[key]:
            if fobj.id in fncData.wrongFncID:
                if DIR_PLUGINS == fobj.directory:
                    errorStat.plg += 1
                elif DIR_FREE in fobj.directory:
                    errorStat.free += 1
                else:
                    errorStat.lvl2 += 1

    return errorStat.refresh()


def getConflictStat(compDict):
    conflictStat = fncStat()
    for key in compDict.keys():
        for fobj in compDict[key]:
            # print(key)
            if key not in fncData.baseDict.keys():
                continue
            for baseobj in fncData.baseDict[key]:
                # 目录相同，而且公式体不一样
                if fobj.directory == baseobj.directory and fobj.body != baseobj.body:
                    if DIR_PLUGINS == fobj.directory:
                        conflictStat.plg += 1
                    elif DIR_FREE in fobj.directory:
                        conflictStat.free += 1
                    else:
                        conflictStat.lvl2 += 1
    return conflictStat.refresh()

def checkDictExist(tmpdict):
    for value in tmpdict.values():
        for fncobj in value:
            fncData.notExDict = fncobjExistCA(fncobj, fncData.baseDict, False, fncData.notExDict)

def checkDictConflict(tmpdict):
    for value in tmpdict.values():
        for fncobj in value:
            fncData.conflicExDict = fncobjConflictCA(fncobj, fncData.baseDict, False, fncData.conflicExDict)
# exist check adn add
# 返回被修改的字典
def fncobjExistCA(fncobj, dictA, samedict = True, dictB = {}):
    key = fncobj.id
    dictOper = dictA
    if samedict == False:
        dictOper = dictB

    if key in dictA.keys():
        pass
    else:
        # dictA中不存在的部分记录到 dictOper中
        if key in dictOper.keys():
            dictOper[key].append(fncobj)
        else:
            dictOper[key] = [fncobj]

    return dictOper

# conflict check and add
# 返回被修改的字典
def fncobjConflictCA(fncobj, dictA, samedict = True, dictB = {}):
    key = fncobj.id
    fbody = fncobj.body
    dictOper = dictA
    if samedict == False:
        dictOper = dictB

    if key in dictA.keys():
        conflictFlag = True
        for fobj in dictA[key]:
            if fbody == fobj.body:
                conflictFlag = False
                break
        if conflictFlag:
            if key in dictOper.keys():
                dictOper[key].append(fncobj)
            else:
                dictOper[key] = [fncobj]

    return dictOper

###################################################################################
# 多层字典
# key: plugins,free,level2
# value dict --key :fncID
#            --value: dict --key:body
#                          --value: hostobj
class CHostList:
    def __init__(self, path, hostname = None):
        self.path = path
        self.hostlist = []
        if hostname != None:
            self.hostlist = [hostname]

    def append(self, hostname):
        self.hostlist.append(hostname)


g_fncAllmap = {}

def addFncObj(fncobj):
    global g_fncAllmap
    fid = fncobj.id
    fdir = fncobj.directory
    fbody = fncobj.body
    fhost = fncobj.hostname
    fpath = fncobj.path

    if fdir not in g_fncAllmap.keys():
        body2host = {}
        body2host[fbody] = CHostList(fpath, fhost)
        id2body = {}
        id2body[fid] = body2host
        g_fncAllmap[fdir] = id2body
    elif fid not in g_fncAllmap[fdir].keys():
        body2host = {}
        body2host[fbody] = CHostList(fpath, fhost)
        g_fncAllmap[fdir][fid] = body2host
    elif fbody not in  g_fncAllmap[fdir][fid].keys():
        g_fncAllmap[fdir][fid][fbody] = CHostList(fpath, fhost)
    else:
        g_fncAllmap[fdir][fid][fbody].append(fhost)

    # print('list info   ' +  str(g_fncAllmap[fdir][fid][fbody]))

    return True

def fncAllmapAddDict(fncdict):
    for key in fncdict.keys():
        for fobj in fncdict[key]:
            addFncObj(fobj)


def formatfncAllmap(path = None):
    global g_fncAllmap
    unitTmp = '{},{},{},{}\n'
    csvinfo = 'dir,fid,versTag,hostCnt\n'

    for fdir in g_fncAllmap.keys():

        for fid in g_fncAllmap[fdir].keys():
            verTag = 1
            fidContent = ''
            cmpContent = ''
            for fbody in  g_fncAllmap[fdir][fid].keys():
                hlobj = g_fncAllmap[fdir][fid][fbody]
                hnlist = hlobj.hostlist
                unitinfo = unitTmp.format(fdir, fid, verTag, len(hnlist))
                csvinfo += unitinfo
                fidContent += 'version: {}  Cnt:{}\nfbody: {}\nhostinfo:\n{}\n\n'.format(verTag, len(hnlist), fbody, '\n'.join(hnlist))

                transBody = fncDecode(fbody)
                cmpContent += 'version{} Cnt:{} \n{}\ntransfbody:\n{}\n\n'.format(verTag, len(hnlist), hlobj.path, transBody)

                verTag += 1

            totalContent = 'versionCnt:{}\n{}\n{}'.format(verTag-1, cmpContent, fidContent)
            if path != None:
                filename = '{}\公式主体统计-{}\{}.txt'.format(path, fdir, fid)
                hjio.wirteText(totalContent, filename)

    return csvinfo

def genfnccsv(path):
    csvinfo = formatfncAllmap(path)
    filename = "{}\{}".format(path, '公式主体统计.csv')
    hjio.wirteCSV(csvinfo, filename)
    return True

# 路径重命名，取hostname
def rename(pathlist):
    for file in pathlist:
        path = file.rsplit('\\', 1)[0]
        oldname = file.rsplit('\\', 1)[-1]
        newname = oldname.rsplit('_', 1)[0]
        tail = oldname.rsplit('_', 1)[-1]
        newfile = path + '\\' + newname
        if tail != 'plugins20210520':
            print('skip!')
            continue
        os.renames(file, newfile)
        # break

def saveNotExtDict(path):
    procDict = fncData.notExDict
    keylist = list(procDict.keys())
    keylist.sort()
    strInfo = 'lack Cnt:{}\n'.format(len(keylist))
    for key in keylist:
        unitInfo = 'fncid:{}\n'.format(key)
        dedupdict = {}
        verTag = 0
        for fobj in procDict[key]:
            if fobj.body not in dedupdict.keys():
                verTag += 1
                dedupdict[fobj.body] = verTag

            currTag = dedupdict[fobj.body]
            unitInfo += 'currTag{}  {}\n'.format(currTag, fobj.path)
        strInfo += unitInfo

    hjio.wirteText(strInfo, path)

def opPathlist(pathlist):
    strInfo = ''
    for path in pathlist:
        hostname = path.split('\\')[-1]
        strInfo += '{}\n'.format(hostname)

    file = r'hostlist.csv'
    hjio.wirteCSV(strInfo, file, True)

def genSetbyfileline(filepath):
    templist = hjio.readFile(filepath).split('\n')
    res = set(templist)
    return res

def compSet(setA, setB):
    listAB = setA-setB
    strAB = '\n'.join(listAB)
    listBA = setB-setA
    strBA = '\n'.join(listBA)
    return (strAB, strBA)

def compFilebyLineSet(path1, path2):
    setA = genSetbyfileline(path1)
    setB = genSetbyfileline(path2)
    strdiff = compSet(setA, setB)

    filediffAB = 'host信息\diffAB.txt'
    filediffBA = 'host信息\diffBA.txt'
    hjio.wirteCSV(strdiff[0], filediffAB, True)
    hjio.wirteCSV(strdiff[1], filediffBA, True)



def genFncDataDict(path):
    procDict = fncData.baseDict
    tablehead = 'ID,公式名,周期,市场,目录,其他标签,内容'
    tablelist = tablehead.split(',')
    # uintTmp = '{},{},{},{},{},{},{}\n'
    linelist = [tablelist]
    keylist = list(procDict.keys())
    keylist.sort()
    for key in keylist:
        for fobj in procDict[key]:
            fclist = fobj.content.split('\n')[0].split(',')
            fncID = key
            fncname = fclist[0]
            fncperiod = fclist[-1]
            if len(fclist) < 5:
                fncperiod = 0
            fncmarket = 'all'
            fncdir = fobj.directory
            fncother = ''
            fnccontent = fncDecode(fclist[3])
            lineUnit = [fncID, fncname, fncperiod, fncmarket, fncdir, fncother, fnccontent]
            linelist.append(lineUnit)

    hjio.writeCsvbyList(linelist, path)


def hexinIniAnalysis(inpath, extpath, istName):
    anaRes = HexinIni(istName)
    singlePath = False
    if inpath == None and extpath == None:
        hjio.writelog("hexin.ini error {}".format(istName))
        return None
    if inpath == None or extpath == None:
        singlePath = True

    inContent = ''
    extContent = ''
    if inpath != None:
        try:
            with open(inpath, 'r') as fpin:
                inContent = fpin.read()
        except:
            with open(inpath, 'rb') as fpin:
                if len(fpin.readline()) <= 200:
                    inContent = fpin.read()
        md5hash = hashlib.md5(inContent.encode())
        anaRes.inHxiniMd5 = md5hash.hexdigest()

    if extpath != None:
        try:
            with open(extpath, 'r') as fpext:
                extContent = fpext.read()
        except:
            with open(extpath, 'rb') as fpext:
                if len(fpext.readline()) <= 200:
                    extContent = fpext.read()
        md5hash = hashlib.md5(extContent.encode())
        anaRes.extHxiniMd5 = md5hash.hexdigest()

    if singlePath:
        content = inContent
        if extpath != None:
            content = extContent
        anaRes.idDict = hexiniContentProc(content, anaRes.idDict)
    else:
        if anaRes.inHxiniMd5 == anaRes.extHxiniMd5:
            anaRes.idDict = hexiniContentProc(inContent, anaRes.idDict)
        else:
            anaRes.idDict = hexiniContentProc(extContent, anaRes.idDict)
            anaRes.idDict = hexiniContentProc(inContent, anaRes.idDict)

    md5hash = hashlib.md5(str(anaRes.idDict).encode())
    anaRes.idDictMd5 = md5hash.hexdigest()

    # print(anaRes.istName)
    # print(anaRes.inHxiniMd5)
    # print(anaRes.extHxiniMd5)
    # print(anaRes.idDictMd5)
    return anaRes

def hexiniContentProc(content, baseDict = {}):
    linelist = content.split('\n')
    for line in linelist:
        unitlist = line.split(',')
        if len(unitlist) < 3:
            continue
        hid = unitlist[0].split('=')[0]
        try:
            hid = int(hid)
        except:
            hjio.writelog('hexin.ini error line, id can not be string:{}'.format(line))
            continue

        hname = unitlist[1]
        try:
            temp = int(hname)
            hjio.writelog('hexin.ini error line, dataname can not be number:{}'.format(line))
            continue
        except:
            pass


        # if hid in baseDict.keys():
        #     hjio.writelog()
        baseDict[hid] = hname

    return baseDict


def hexinInfoOutput(filepath):
    pass

# key:id   value:name dict
#             key: dataname  value: [ csIstName, ...]
g_hxidDict = {}

def hxidAllAddDict(hxobj):
    global g_hxidDict
    if None == hxobj:
        return
    istName = hxobj.istName
    for id in hxobj.idDict.keys():
        dataname = hxobj.idDict[id]
        if id not in g_hxidDict.keys():
            name2istname = {}
            name2istname[dataname] = [istName]
            g_hxidDict[id] = name2istname
        elif dataname not in g_hxidDict[id].keys():
            g_hxidDict[id][dataname] = [istName]
        else:
            g_hxidDict[id][dataname].append(istName)

    return True


def formatHexinIDAllmap(path):
    unitTmp = '{},{},{},{}\n'
    csvinfo = 'ID,DataName,versTag,CSIstCnt\n'

    for id in g_hxidDict.keys():
        verTag = 1
        fidContent = ''
        cmpContent = ''
        for dataname in g_hxidDict[id].keys():
            insNamelist = g_hxidDict[id][dataname]
            unitinfo = unitTmp.format(id, dataname, verTag, len(insNamelist))
            csvinfo += unitinfo
            cmpContent += 'version:{} DataName:{} Cnt:{}\n'.format(verTag, dataname, len(insNamelist))
            fidContent += 'version:{} DataName:{} Cnt:{}\n{}\n\n'.format(verTag, dataname, len(insNamelist), '\n'.join(insNamelist))

            verTag += 1
        totalContent = 'versionCnt:{}, ID:{}\n{}\n{}'.format(verTag - 1, id, cmpContent, fidContent)
        if path != None:
            filename = '{}\hexin字段统计\{}.txt'.format(path, id)
            hjio.wirteText(totalContent, filename)
    return csvinfo

def genHexinInfo(path):
    csvinfo = formatHexinIDAllmap(path)
    filename = "{}\{}".format(path, 'hexin字段统计.csv')
    hjio.wirteCSV(csvinfo, filename)
    return True