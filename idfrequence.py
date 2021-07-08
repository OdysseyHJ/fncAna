import json
import re

import hjio
import fncData
import temp

reqObjAll = []


# key:datatype id
# value: CIDFreq obj
reqIdDict = {}

class CReq:
    def __init__(self):
        self.codelist = ''
        self.datatype = ''
        self.datetime = ''
        self.idList = []

class CIDFreq:
    def __init__(self):
        self.id = 0
        self.req=count = 0
        self.freqByAllReq = 0.0
        self.freqByAllID = 0.0

def userReqFileProc(pathList):
    global reqObjAll
    index = 1
    total2proc = len(pathList)
    for path in pathList:
        print("process:{:.2f}%".format(index/total2proc * 100))
        index += 1
        strContent = hjio.readFile(path)
        reqlist = getUserReqList(strContent)
        reqObjlist = userReqListProc(reqlist)
        reqObjAll += (reqObjlist)
        # break
    print(len(reqObjAll))
    reqIdFreqStats()

    return

def getUserReqList(strContent):
    reqList = strContent.split('\n')
    return reqList

def userReqListProc(reqlist):
    reqObjlist = []
    for req in reqlist:
        if len(req) == 0:
            continue
        req = re.sub('\'', '\"', req, count=0)
        reqobj = CReq()
        try:
            jData = json.dumps(req)
            jDict = json.loads(jData)  #loads to str
            jDict = json.loads(jDict)  #loads to dict
        except:
            print(req)
            break

        reqobj.codelist = jDict['codelist']
        reqobj.datetime = jDict['datetime']
        reqobj.datatype = jDict['datatype']
        strIdlist = jDict['datatype'].split(',')
        for each in strIdlist:
            try:
                tempNum = int(each)
            except:
                continue
            reqobj.idList.append(tempNum)

        # print(reqobj.idList)
        reqObjlist.append(reqobj)
    return reqObjlist


def findDatatype(id):
    findres = []
    for each in reqObjAll:
        if id in each.idList:
            findres.append(each)
    return findres


def reqObjOutput(objlist, path):
    count = 1
    for reqobj in objlist:
        strUnit = '{}\n'.format(reqobj.datatype)
        hjio.writelog(strUnit)
        print(count)
        count += 1




def reqIdFreqStats():
    global reqIdDict
    for reqobj in reqObjAll:
        # print(reqobj.idList)
        for id in reqobj.idList:
            if id in reqIdDict.keys():
                reqIdDict[id].count += 1
            else:
                newCIDFreq = CIDFreq()
                newCIDFreq.id = id
                newCIDFreq.count = 1
                reqIdDict[id] = newCIDFreq
    return

def reqIdfreqOutput(path):
    idlist = list(reqIdDict.keys())
    # print(idlist)
    idlist.sort()

    lineList = []
    for id in idlist:
        lineInfo = [id, reqIdDict[id].count]
        # print(lineInfo)
        lineList.append(lineInfo)
    hjio.writeCsvbyList(lineList, path)




