

import os

g_filePath = r"D:\HJ_EX_logs\20210319\cpuInfo"
g_outFile = r"D:\HJ_EX_logs\20210319\cpuInfo\analysisResult.dat"
# cpuPDict = {
#     0 : "0~5%",
#     1 : "5~10%",
#     2 :
# }

# g_TimeAvail = (9, 10, 110, 111, 112, 13, 14)
# 9:00 am - 11:30 am    13:00 pm - 15:00 pm
g_openAm  =  90000
g_closeAm = 113000
g_openPm  = 130000
g_closeAm = 150000

# time 112233  (11:22:33)
def timeCheck(time):
    if (time >= g_openAm and time <= g_closeAm) or (time >= g_openPm and time <= g_closePm):
        return True
    else:
        return False

def getTime(str):
    time = str.split(' ')[1]
    return int(time)

def getCpuUsage(str):
    CpuUsage = (str.split('=')[1]).split(',')[0]
    return float(CpuUsage)

def getMemUsage(str):
    MemUsage = (str.split(',')[1]).split('=')[1]
    return int(MemUsage)

def getData(filePath):
    data = []
    with open(filePath, 'r') as dataSource:
        originData = dataSource.read()
        dataList = originData.split('\n')
        # print(dataList)
        for line in dataList:
            if len(line) <= 10:
                continue

            time = getTime(line)
            CpuUsage = getCpuUsage(line)
            MemUsage = getMemUsage(line)
            data.append((time, CpuUsage, MemUsage))

    return  data


# 从路径下获取文件信息
def getFileList():
    file_list = list(os.walk(g_filePath))[0][2]
    return file_list

def Proc():
    fileList = getFileList()

    with open(g_outFile, 'w') as outfile:
        for eachfile in fileList:
            fp = r"{0}\{1}".format(g_filePath, eachfile)


            data = getData(fp)
            if len(data) == 0:
                print(eachfile)
                continue
            print(data)

            MemMaxTup = data[0]
            MemAverage = 0

            # with open(fp, 'r') as cpuInfoFile:
            #     cpuInfo = cpuInfoFile.read()
            #     cpuInfoList = cpuInfo.split('\n')
            # print(cpuInfoList)
            cpuPDict = {}
            perUint = 10
            CpuMax = 300
            for i in range(0, CpuMax//perUint):
                key = '{0}%~{1}%'.format(i * perUint, (i + 1) * perUint)
                cpuPDict[key] = 0
            cpuPDict['{0}%~'.format(CpuMax)] = 0

            for eachTup in data:
                MemAverage += eachTup[2]
                if eachTup[2] > MemMaxTup[2]:
                    MemMaxTup = eachTup
                    # cpuInfoNList.append(float(eachStr))

                attr = eachTup[1] // perUint
                if attr == 0:
                    key = '0%~{0}%'.format(perUint)
                elif attr < 20:
                    key = '{0}%~{1}%'.format( int((attr - 1) * perUint), int(attr * perUint))
                else:
                    key = '{0}%~'.format(CpuMax)

                cpuPDict[key] += 1

            MemAverage = round(MemAverage/len(data), 2)
            MemUsageInfo = 'MaxUsage:{0}  MaxTime:{1}   MemAvg:{2}'.format(MemMaxTup[2], MemMaxTup[0], MemAverage)

            CpuUsageInfo = '{0}:\n'.format(eachfile)
            for pkey in cpuPDict.keys():
                percent = round(cpuPDict[pkey] / len(data) * 100, 2)
                CpuUsageInfo += '{0} : {1} %\n'.format(pkey, percent)

            outInfo = '{0}\n{1}\n'.format(MemUsageInfo, CpuUsageInfo)

            outfile.write(outInfo)













