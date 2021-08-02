import os

import hjio



#统计字段的定义
STAT_KEY_MARKET = 'market'
STAT_KEY_FILE_TYPE = 'data_file'
STAT_KEY_FIELD_CNT = 'field_count'
STAT_KEY_FILE_CNT = 'file_count'
STAT_KEY_STOREAGE_CNT = 'storage_count'
STAT_KEY_RECORD_CNT = 'record_count'

statKeySet = {
    STAT_KEY_MARKET,
    STAT_KEY_FILE_TYPE,
    STAT_KEY_FIELD_CNT,
    STAT_KEY_FILE_CNT,
    STAT_KEY_STOREAGE_CNT,
    STAT_KEY_RECORD_CNT,
}

#市场定义
# 历史数据处理时生成
marketSet = set()

#数据分类定义
DATA_FILE_DAYK = "*.day"
DATA_FILE_MINK = "*.min"
DATA_FILE_MIN5K = "*.mn5"
DATA_FILE_EXT = "*.ext"
DATA_FILE_LATEST_REAL = "*"
DATA_FILE_HISNOWS = "hisnows.now"
DATA_FILE_HISNOWI = "hisnowi.now"
DATA_FILE_HISTRACES = "histraces.trc"
DATA_FILE_HISTRACEI = "histracei.trc"
DATA_FILE_HISMINUTES = "hisminutes.trd"
DATA_FILE_HISMINUTEI = "hisminutei.trd"
DATA_FILE_HISCLOSE = "hiscloseauctiontraces.trc"
DATA_FILE_HISTICKS = "histicks.tic"
DATA_FILE_HISORDERS = "hisorders.tic"
DATA_FILE_HISBORDERS = "hisborders.ord"
DATA_FILE_HISSORDERS = "hissorders.ord"
DATA_FILE_HISOPEN = "hisopenauctiontraces.trc"
DATA_FILE_HISPRE = "hispretraces.trc"
DATA_FILE_HISAFTER = "hisafttraces.trc"

starTrans = {
    DATA_FILE_DAYK : "day",
    DATA_FILE_MINK : 'min',
    DATA_FILE_MIN5K : 'min5',
    DATA_FILE_EXT : 'extra',
    DATA_FILE_LATEST_REAL : 'real_latest_day',
}

datatypeSet = {
    starTrans[DATA_FILE_DAYK],
    starTrans[DATA_FILE_MINK],
    starTrans[DATA_FILE_MIN5K],
    starTrans[DATA_FILE_EXT],
    starTrans[DATA_FILE_LATEST_REAL],
    DATA_FILE_HISNOWS,
    DATA_FILE_HISNOWI,
    DATA_FILE_HISTRACES,
    DATA_FILE_HISTRACEI,
    DATA_FILE_HISMINUTES,
    DATA_FILE_HISMINUTEI,
    DATA_FILE_HISCLOSE,
    DATA_FILE_HISTICKS,
    DATA_FILE_HISORDERS,
    DATA_FILE_HISBORDERS,
    DATA_FILE_HISSORDERS,
    DATA_FILE_HISOPEN,
    DATA_FILE_HISPRE,
    DATA_FILE_HISAFTER,
}

#统计信息字典：
# key (hostname) --- value (dict)
#                     key (market) --- value (dict)
#                                       key (data type) --- value (CStatData)
statistic_data = {}

class CStatData:
    def __init__(self, host='', market='', type=''):
        self.host = host
        self.market = market
        self.type = type
        self.field_count = 0
        self.file_count = 0
        self.storage_count = 0
        self.record_count = 0
        self.count = 0

    def show(self):
        print(self.field_count, self.file_count, self.storage_count, self.record_count)
        return

    def data2list(self):
        return [
            self.host,
            self.market,
            self.type,
            self.field_count,
            self.file_count,
            self.storage_count,
            self.record_count,
        ]
# class CStatMarket:
#     def __init__(self, market):
#         self.market = market
#         self.dayk = CStatData()
#         self.extra = CStatData()
#         self.mink = CStatData()
#         self.min5k = CStatData()
#         self.latest_real = CStatData()
#         self.hisnowi = CStatData()
#         self.hisnows = CStatData()
#         self.histraces = CStatData()
#         self.histracei = CStatData()
#         self.hisminutes = CStatData()
#         self.hisminutei = CStatData()
#         self.hiscloseauctiontraces = CStatData()
#         self.histicks = CStatData()
#         self.hisorders = CStatData()
#         self.hisborders = CStatData()
#         self.hissorders = CStatData()
#         self.hisopenauctiontraces = CStatData()
#         self.hispretraces = CStatData()
#         self.hisafttraces = CStatData()



def getFileList(folderPath):
    fileList = []
    for root, dirs, files in os.walk(folderPath):
        for file in files:
            filepath = '{}\{}'.format(folderPath, file)
            fileList.append(filepath)
    return fileList

def history_data_proc(fileList):
    for file in fileList:

        hostname = file.split('\\')[-1].split('.')[0]
        statistic_data[hostname] = {}
        fileContent = hjio.readFile(file)
        lineList = fileContent.split('\n')


        index = 0
        while index < len(lineList):
            line = lineList[index]
            try:
                key = ''
                key, value = getKV(line)
            except:
                index += 1
                continue

            # print(key, value)

            #读到market才开始处理，否则不处理
            if key != STAT_KEY_MARKET:
                index += 1
                continue



            market = value

            if market not in marketSet:
                marketSet.add(market)

            datatype_dict = {}
            index += 1
            line = lineList[index]
            try:
                key = ''
                key, value = getKV(line)
            except:
                index += 1
                continue

            #处理分类数据信息
            while key == STAT_KEY_FILE_TYPE:
                fileType = value.split('/')[-1]
                if fileType in starTrans.keys():
                    fileType = starTrans[fileType]
                statDataObj = CStatData(hostname, market, fileType)
                try:
                    key1, value1 = getKV(lineList[index + 1])
                    key2, value2 = getKV(lineList[index + 2])
                    key3, value3 = getKV(lineList[index + 3])
                    key4, value4 = getKV(lineList[index + 4])
                    statDataObj.field_count = int(value1)
                    statDataObj.file_count = int(value2)
                    statDataObj.storage_count = int(value3)
                    statDataObj.record_count = int(value4)
                except:
                    pass
                    # print("error value", hostname, market, value, value1, value2, value3, value4)
                index += 5

                datatype_dict[fileType] = statDataObj
                # print(fileType)
                # statDataobj.show()
                line = lineList[index]
                try:
                    key = ''
                    key, value = getKV(line)
                except:
                    index += 1
                    break

            #处理完的市场加入dict
            statistic_data[hostname][market] = datatype_dict
    return


def getKV(line):
    parseList = line.split(':')
    if len(parseList) < 2:
        return None
    return (parseList[0], parseList[1])

def genCsv(path):
    tableHead = ['主机名',
                 '市场',
                 '数据分类',
                 '表格字段数',
                 '文件总数',
                 '文件总计存储空间',
                 '文件中记录总数']
    wholeTable = [tableHead]
    typeTableDict = {}

    hostList = list(statistic_data.keys())
    hostList.sort()
    for host in hostList:
        marketDict = statistic_data[host]
        marketList = list(marketDict.keys())
        marketList.sort()
        for market in marketList:
            datatypeDict = marketDict[market]
            datatypeList = list(datatypeDict.keys())
            datatypeList.sort()
            for filetype in datatypeList:
                dataObj = datatypeDict[filetype]
                lineInfo = dataObj.data2list()
                wholeTable.append(lineInfo)

                if filetype not in typeTableDict.keys():
                    typeTableDict[filetype] = [tableHead]
                typeTableDict[filetype].append(lineInfo)


    wholeTablePath = '{}\{}'.format(path, 'total_table.csv')
    hjio.writeCsvbyList(wholeTable, wholeTablePath)

    for key in typeTableDict.keys():
        tableName = '{}\{}.csv'.format(path, key)
        hjio.writeCsvbyList(typeTableDict[key], tableName)

    return





class CMarketDict:
    def __init__(self):
        self.MHD_Dict = {}
        self.MDH_Dict = {}
        self.summaryDict = {}

    def summaryDictInit(self):
        pass
        for market in self.MDH_Dict.keys():
            self.summaryDict[market] = {}

            for datatype in self.MDH_Dict[market].keys():
                self.summaryDict[market][datatype] = CStatData()
                AllDataObj = self.MDH_Dict[market][datatype]
                count = len(AllDataObj)
                for host in AllDataObj.keys():
                    dataObj = AllDataObj[host]
                    if self.summaryDict[market][datatype].field_count == 0:
                        self.summaryDict[market][datatype].field_count = dataObj.field_count
                    self.summaryDict[market][datatype].file_count += dataObj.file_count
                    self.summaryDict[market][datatype].record_count += dataObj.record_count
                    self.summaryDict[market][datatype].storage_count += dataObj.storage_count
                self.summaryDict[market][datatype].file_count //= (count)
                self.summaryDict[market][datatype].record_count //= (count)
                self.summaryDict[market][datatype].storage_count //= (count*1000)
                self.summaryDict[market][datatype].count = count

    def getDatatypeFieldList(self, datatype='day', field=STAT_KEY_FIELD_CNT):
        marketList = list(self.summaryDict.keys())
        dataList = []
        for market in marketList:
            if datatype not in self.summaryDict[market].keys():
                #有些市场没有特定的数据，这些数据置0
                dataList.append(0)
                continue

            if field == STAT_KEY_FIELD_CNT:
                dataList.append(self.summaryDict[market][datatype].field_count)
            elif field == STAT_KEY_FILE_CNT:
                dataList.append(self.summaryDict[market][datatype].file_count)
            elif field == STAT_KEY_STOREAGE_CNT:
                dataList.append(self.summaryDict[market][datatype].storage_count)
            elif field == STAT_KEY_RECORD_CNT:
                dataList.append(self.summaryDict[market][datatype].record_count)
            else:
                dataList.append(self.summaryDict[market][datatype].count)

        return (marketList, dataList)

    def gethostFieldList(self, market='shase', datatype='day', field=STAT_KEY_FIELD_CNT):
        hostdict = {}
        hostlist = []
        vallist = []
        if market not in self.MDH_Dict.keys():
            return ([],[])
        if datatype not in self.MDH_Dict[market].keys():
            return ([],[])

        datahandle = self.MDH_Dict[market][datatype]
        for host in datahandle.keys():
            value = 0
            if field == STAT_KEY_FIELD_CNT:
                value = datahandle[host].field_count
            elif field == STAT_KEY_FILE_CNT:
                value = datahandle[host].file_count
            elif field == STAT_KEY_STOREAGE_CNT:
                value = datahandle[host].storage_count
            elif field == STAT_KEY_RECORD_CNT:
                value = datahandle[host].record_count
            hostdict[host] = value
        print(hostdict)
        sortedDict = sorted(hostdict.items(), key=lambda d: d[1], reverse=False)

        for host,val in sortedDict:
            hostlist.append(host)
            vallist.append(val)
        return (hostlist, vallist)


siMarketDict = CMarketDict()
def MarketDataInit():
    for host in statistic_data.keys():
        hostData = statistic_data[host]
        for market in hostData.keys():
            marketData = hostData[market]
            for datatype in marketData.keys():
                dataObj = marketData[datatype]
                # print(datatype)
                if market not in siMarketDict.MHD_Dict.keys():
                    siMarketDict.MHD_Dict[market] = {}
                    siMarketDict.MDH_Dict[market] = {}

                if datatype not in siMarketDict.MDH_Dict[market].keys():
                    siMarketDict.MDH_Dict[market][datatype] = {}
                siMarketDict.MDH_Dict[market][datatype][host] = dataObj

    siMarketDict.summaryDictInit()
    # print()
    # for market in marketSet:
    #     for datatype in datatypeSet:
    #         print(market, datatype)
    #         siMarketDict.summaryDict[market][datatype].show()
    return




