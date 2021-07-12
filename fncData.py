
import os
import re

from commonDef import HexinIni
import fnclib
import hjio
import temp
from hjperf import cTimeBand



# 统一包公式属性


# 统一库信息
# plugins 公式数
# @free 公式数
# @level2 公式数
# 公式总数 1034
stdInfo = (894, 85, 71, 1050)



# 错误公式ID统计
wrongFncID = (527527, # 1 3 5 10 15 分钟涨幅系列
                527526,
                3934664,
                461438,
                461439,
                199637,
                1116622, #5日涨幅
                330796, # 指数代码错误
                461407,
                461408,
                461409,
                592544,
                592723,
                723572,
                723573,
                723653,
1509838,
              )

# key:fncid
# value:list [fncObj1, fncObj2, ...]
baseDict = {}


# key fnncid
# value:list [fncObj1, fncObj2, ...]
notExDict = {}

# key fnncid
# value:list [fncObj1, fncObj2, ...]
conflicExDict = {}


# hexin base
hexinIniBase = None

# id 2 HexinIniUnit, name 2 HexinIniUnit
hxID2obj = {}
hxName2obj = {}

def init(folderpath):
    timeBand = cTimeBand()
    timeBand.addTimePoint()
    global baseDict
    baseDict = fnclib.getFncDict(folderpath, 'git_base')
    # fnclib.fncAllmapAddDict(baseDict)
    timeBand.addTimePoint()
    # global hexinIniBase
    extpath = folderpath.rsplit(os.path.sep, 1)[0]
    extHxinipath = fnclib.getDesignedFilepath('hexin.ini', extpath)
    # hexinIniBase = fnclib.hexinIniAnalysis(None, extHxinipath, 'git_base')
    # fnclib.hxidAllAddDict(hexinIniBase)

    global hxID2obj
    global hxName2obj
    hexinRes = fnclib.getHxiniDatadict(extHxinipath)
    hxID2obj = hexinRes[0]
    hxName2obj = hexinRes[1]
    timeBand.addTimePoint()
    # print(timeBand.getTimeBand())
    hjio.writelog("fnc data init successsfully! timeband:{}".format(str(timeBand.getTimeBand())))
    return

def baseDictInit(folderpath):
    timeBand = cTimeBand()
    timeBand.addTimePoint()
    global baseDict
    baseDict = fnclib.getFncDict(folderpath, 'git_base')
    timeBand.addTimePoint()
    hjio.writelog("fnc load complete! timeband:{}".format(str(timeBand.getTimeBand())))
    return

def hexiniConfInit(folderpath):
    timeBand = cTimeBand()
    timeBand.addTimePoint()
    extpath = folderpath.rsplit(os.path.sep, 1)[0]
    extHxinipath = fnclib.getDesignedFilepath('hexin.ini', extpath)
    global hxID2obj
    global hxName2obj
    hexinRes = fnclib.getHxiniDatadict(extHxinipath)
    hxID2obj = hexinRes[0]
    hxName2obj = hexinRes[1]
    timeBand.addTimePoint()
    hjio.writelog("hexin.ini init complete! timeband:{}".format(str(timeBand.getTimeBand())))
    return


upperLetterSet = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'}

def hexinUnitRef(str2find, retIDlist = False):
    if len(str2find) == 0:
        hjio.writelog("hexinUnitRef, error:zero str!")
        return

    str2find = str2find.upper()
    refNamelist= []
    for name in hxName2obj.keys():
        headIndex = str2find.find(name)
        if headIndex >= 0:
            nameLen = len(name)

            # 避免函数名匹配出错，字符串字串重复匹配问题，这里对系统函数做了检查
            if ((headIndex-1 < 0) or (str2find[headIndex-1] not in upperLetterSet)) \
                    and ((headIndex + nameLen >= len(str2find)) or (str2find[headIndex+nameLen] not in upperLetterSet)):
                refNamelist.append(name)

    refIDlist = []
    if retIDlist:
        for name in refNamelist:
            refIDlist.append(hxName2obj[name])
        return retIDlist

    return refNamelist


def fnchexinUnitRefAna(fncobj):
    str2find = fncobj.algrithm
    refNamelist = hexinUnitRef(str2find)

    hqReflist = []
    fdReflist = []
    funcReflist = []
    otherReflist = []

    if None != refNamelist:
        for name in refNamelist:
            smName = hexinUnitSegment(name)
            if smName == SM_HQ_NAME:
                hqReflist.append(name)
            elif smName == SM_FD_NAME:
                fdReflist.append(name)
            elif smName == SM_FUNC_NAME:
                funcReflist.append(name)
            else:
                otherReflist.append(name)

    anaRes = [
        ','.join(hqReflist),
        ','.join(fdReflist),
        ','.join(otherReflist),
        ','.join(funcReflist),
    ]

    return anaRes


DATA_ID_MASK = 0x00000fff
SM_HQ_NAME = 'HQ'
SM_FD_NAME = 'FD'
SM_WT_NAME = 'WT'
SM_FUNC_NAME = 'FUNC'
SM_USERS_NAME = 'USERS'
SM_TEXT_NAME = 'TEXT'
SM_OTHER_NAME = 'OTHER'

SM_HQ_BEGIN = 1
SM_FD_BEGIN = 301
SM_WT_BEGIN = 2102
SM_FUNC_BEGIN = 2203
SM_USERS_BEGIN = 2504
SM_TEXT_BEGIN = 3505
SM_OTHER_BEGIN = 3606
SM_END = 4905


def hexinUnitSegment(name='',id=0):
    if id == 0:
        if len(name) == 0:
            hjio.writelog("hexinUnitSegment, error:id = 0, zero str")
            return
        else:
            try:
                id = hxName2obj[name].id
            except:
                hjio.writelog("hexinUnitSegment, error:id = 0, str = {}".format(name))
                return

    if SM_HQ_BEGIN <= id and id < SM_FD_BEGIN:
        return SM_HQ_NAME
    elif SM_FD_BEGIN <= id and id < SM_WT_BEGIN:
        return SM_FD_NAME
    elif SM_WT_BEGIN <= id and id < SM_FUNC_BEGIN:
        return SM_WT_NAME
    elif SM_FUNC_BEGIN <= id and id < SM_USERS_BEGIN:
        return SM_FUNC_NAME
    elif SM_USERS_BEGIN <= id and id < SM_TEXT_BEGIN:
        return SM_USERS_NAME
    elif SM_TEXT_BEGIN <= id and id < SM_OTHER_BEGIN:
        return SM_TEXT_NAME
    else:
        return SM_OTHER_NAME

def hexinSmName2Table(smName):
    if smName == SM_HQ_NAME:
        return '基础行情'
    elif smName == SM_FD_NAME:
        return '财务数据'
    else:
        return '计算指标'

def getFncName(fobj):
    if fobj.id in hxID2obj.keys():
        return hxID2obj[fobj.id].name
    else:
        return fobj.getFilenamePrefix()

def dataDictTableProc(path):
    # tableHead = ['']
    # lineTemp = '{id},{name},{descript},{fnctype},{market},{zqtype},' \
    #            '{tradetype},{datatype},{period},{default_period},' \
    #            '{comment},{filename},{algrithm},{updatetime},' \
    #            '{refbase},{reffd},{refohter},{reffunc},{dir}'
    # lineTemp = '{id},{name},{fnctype},{period},{default_period},' \
    #            '{filename},{algrithm},{dir},' \
    #             '{refdata}'
               # '{refbase},{reffd},{refohter},{reffunc}'
    keylist = list(baseDict.keys())
    keylist.sort()

    tablehead = [  "id",
                    "名称",
                    "含义",
                    "类型（基础行情/财务/指标）",
                    "市场+权限（范围：上海/level-1、深圳/level-2等）",
                    "证券类型（指数、股票、基金、债券、期货、期权、权证）",
                    "交易分类（取值范围：盘前、盘中、盘后）",
                    "数据分类（范围：快照、分时、k线、明细、逐笔成交、逐笔委托）",
                    "时间周期（minN、dayN、weekN、yearN、stream、now）",
                    "指标默认计算分类和周期",
                    "周期区间",
                    "周期值",
                    "说明",
                    "公式文件",
                    "公式目录",
                    "公式内容",
                    "更新时间",
                    "引用数据项（基础数据）",
                    "引用数据项（财务数据）",
                    "引用数据项（其他数据）",
                    "引用系统函数",]
    linelist = [tablehead]
    for key in keylist:
        for fobj in baseDict[key]:
            if isHighFreqID(fobj.id) == False:
                continue
            fname = getFncName(fobj)
            refAnaRes = fnchexinUnitRefAna(fobj)
            periodRange = fobj.getStrPeriodRange()
            defaultPeriod = fobj.getDefaultPeriodItem()
            periodItem = fobj.getStrPeriodItem()
            line = [fobj.id,
                    fname,
                    fobj.name,
                    '指标',
                    '', #市场权限
                    '', #证券类型
                    '', #交易分类
                    '', #数据分类
                    periodItem,
                    defaultPeriod,
                    periodRange,
                    fobj.period,
                    '', #说明
                    fobj.fname,
                    fobj.directory,
                    fobj.algrithm,
                    '2021-6-6',
                    ]
            line += refAnaRes
            linelist.append(line)
    hjio.writeCsvbyList(linelist, path)
    return

def isHighFreqID(id):
    # print(len(temp.highFreqID))
    if id in temp.highFreqID:
        return True
    return False








# 待校验
temp2check = (3142,3119,3120
,3143,3126,3127
,68873,68508,68509
,3144,3128,3129
,3138,3141
,3130,3134
,68510,68511
,3132,3136
,3139,3140
,3131,3135
,68512,68513
,3133,3137
,68519,68518
,68521,68520
,68514,68515
,68522,68523
, 2977
, 3124
, 68517
,3121)


