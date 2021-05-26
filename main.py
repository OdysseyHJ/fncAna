
import CpuInfoProc
import fnclib
import fncData
import hjio
import time
import setting
from hjperf import cTimeBand



def main():
    # pathlist = fnclib.getPathDepth(setting.renamePath, 1)
    # fnclib.rename(pathlist)
    #
    # return

    # 比较hostname集合
    # fnclib.compFilebyLineSet(setting.repopath, setting.packpaht)
    # return



    # 时间打点初始化
    timeBand = cTimeBand()
    timeBand.addTimePoint()

    # 初始化 必要
    fncData.init(setting.initPaht)
    timeBand.addTimePoint()

    #生成数据字典
    fnclib.genFncDataDict(setting.confluencedict)
    return

    # 检查id是否在字典中
    # print(fnclib.checkIDexist(fncData.temp2check))

    # 处理原始数据信息,获取站点host信息
    # fileList = fnclib.getPathDepth(setting.oringinDataPath, 2)

    fileList = fnclib.getPathDepth(setting.fncAll, 1)
    # fileListAppend = fnclib.getPathDepth(setting.appendPath)
    timeBand.addTimePoint()
    # fileList += fileListAppend

    # 根据path信息,读取处理数据,处理生产基于host的信息并写文件
    fnclib.genFncStatistciInfo(fileList, setting.statInfoBaseHost)
    timeBand.addTimePoint()

    # 根据genFncStatistciInfo生产的信息，处理生产基于公式的统计信息
    fnclib.genfnccsv(setting.rootpath)
    timeBand.addTimePoint()

    fnclib.saveNotExtDict(setting.notExInfo)

    # 打印处理时间信息
    print(timeBand.getTimeBand())
    return



if __name__ == '__main__':
    main()


