
import CpuInfoProc
import fnclib
import fncData
import hjio
import setting
from hjperf import cTimeBand
import minConvert
import fncDataDict
import hjqt
import temp
import idfrequence

import time
import sys

MODE_DATA_DICT    = 0
MODE_FNC_ANA      = 1
MODE_REQ_FREQ_ANA = 2
MODE_REQ_FREQ_ID_SEARCH = 3
MODE_DATA_DICT_EXCEL = 4
MODE_FNC_ID_FIND = 5
MODE_HXINI_NAME_CHECK = 6

def main():

    # 日志初始化 必要
    hjio.init(setting.logpath)

    # 运行
    runByMode(0)

    # 清空日志缓存，写文件
    hjio.clearbuf('PROCESS END')

    return


def runByMode(modeType = 0):
    if modeType == MODE_DATA_DICT:
        ModeDataDict()
    elif modeType == MODE_FNC_ANA:
        ModeFncAna()
    elif modeType == MODE_REQ_FREQ_ANA:
        ModeReqFreqAna()
    elif modeType == MODE_DATA_DICT_EXCEL:
        ModeDataDictExcel()
    elif modeType == MODE_FNC_ID_FIND:
        ModeFncIDfind()
    elif modeType == MODE_HXINI_NAME_CHECK:
        ModeHxiniNameCheck()
    else:
        errinfo = "wrong mode type:{}".format(modeType)
        print(errinfo)
        hjio.writelog(errinfo)

    return

def ModeDataDict():
    timeBand = cTimeBand()
    timeBand.addTimePoint()

    fncData.init(setting.initPaht)
    timeBand.addTimePoint()

    # 数据字典exe
    fncDataDict.proc()

    # 打印处理时间信息
    print(timeBand.getTimeBand())
    return

def ModeFncAna():
    timeBand = cTimeBand()
    timeBand.addTimePoint()

    fncData.init(setting.initPaht)
    timeBand.addTimePoint()

    fileList = fnclib.getPathDepth(setting.fncAll, 2)
    # fileListAppend = fnclib.getPathDepth(setting.appendPath)
    timeBand.addTimePoint()
    # fileList += fileListAppend

    # 根据path信息,读取处理数据,处理生产基于host的信息并写文件
    fnclib.genFncStatistciInfo(fileList, setting.statInfoBaseHost)
    timeBand.addTimePoint()

    # 根据genFncStatistciInfo生产的信息，处理生产基于公式的统计信息
    fnclib.genfnccsv(setting.rootpath)
    timeBand.addTimePoint()

    # 生成基于hexin.ini文件字段id的信息
    fnclib.genHexinInfo(setting.rootpath)
    timeBand.addTimePoint()

    fnclib.saveNotExtDict(setting.notExInfo)

    # 打印处理时间信息
    print(timeBand.getTimeBand())

    return

def ModeReqFreqAna():
    timeBand = cTimeBand()
    timeBand.addTimePoint()

    hjio.writelog('PROCESS START')

    fncData.init(setting.initPaht)
    timeBand.addTimePoint()

    #id 分析
    pathList = fnclib.getFileDepth(setting.userReqPath, 1)
    idfrequence.userReqFileProc(pathList)
    idfrequence.reqIdfreqOutput(setting.idCountPath)

    # 打印处理时间信息
    print(timeBand.getTimeBand())

    return

def ModeReqFreqIDsearch(searchID = 0):
    timeBand = cTimeBand()
    timeBand.addTimePoint()

    fncData.init(setting.initPaht)
    timeBand.addTimePoint()

    # id 分析
    pathList = fnclib.getFileDepth(setting.userReqPath, 1)
    idfrequence.userReqFileProc(pathList)
    res = idfrequence.findDatatype(searchID)
    idfrequence.reqObjOutput(res, setting.idRefAna)

    # 打印处理时间信息
    print(timeBand.getTimeBand())

    return

def ModeDataDictExcel():
    fncData.init(setting.initPaht)
    fncData.dataDictTableProc(setting.excelDict)
    return


def ModeFncIDfind():
    fncData.init(setting.initPaht)
    idlist = [2977,3124,68517,3121,3119,3120,3138,3141,3139,3140,68519,68518,3126,3127,3130,3134,3131,3135,68521,68520,68508,68509,68510,68511,68512,68513,68514,68515,3128,3129,3132,3136,3133,3137,68522,68523]
    for id in idlist:
        if id in fncData.baseDict.keys():
            print(id)


# 查找hexin.ini中错误的命名
def ModeHxiniNameCheck():
    fncData.init(setting.initPaht)
    fobjdict = fncData.baseDict
    hxiniIDdict = fncData.hxID2obj
    hxiniNameDict = fncData.hxName2obj
    namelist = []
    for id in fobjdict.keys():
        for fobj in fobjdict[id]:
            fnamePrefix = fobj.getFilenamePrefix()
            if fnamePrefix in hxiniNameDict.keys() and hxiniNameDict[fnamePrefix].id != fobj.id:

                # if hxiniNameDict[fnamePrefix].id in hxiniIDdict.keys():
                    # del hxiniIDdict[hxiniNameDict[fnamePrefix].id]
                # hxiniIDdict[]
                namelist.append(fnamePrefix)
                # print(fnamePrefix, hxiniNameDict[fnamePrefix].id, fobj.id)
                newname = "{}_{}".format(fnamePrefix,fobj.id)

                # print("{}=0,{},{}".format(fobj.id, newname, newname))
                # print("mv {}.fnc {}.fnc".format(fnamePrefix, newname))
                print(hxiniNameDict[fnamePrefix].id)

    for name in temp.fncloadfail:
        if name not in namelist:
            print(name)
    return


if __name__ == '__main__':
    main()


