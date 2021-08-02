import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['Microsoft YaHei']

import historyLib


def drawBarGraph(title, datatype='day', fieldtype='hostcount', savPath=''):
    X, Y1 = historyLib.siMarketDict.getDatatypeFieldList(datatype, fieldtype)
    # X, Y2 = historyLib.siMarketDict.getDatatypeFieldList(field=historyLib.STAT_KEY_FILE_CNT)
    # X, Y3 = historyLib.siMarketDict.getDatatypeFieldList(field=historyLib.STAT_KEY_STOREAGE_CNT)
    # X, Y4 = historyLib.siMarketDict.getDatatypeFieldList(field=historyLib.STAT_KEY_RECORD_CNT)
    width=1
    xpos = np.arange(0, len(X)*1.5, 1.5)
    if len(X) == 0:
        print(datatype)

    fig, ax = plt.subplots(figsize=(10, 8))
    bars1 = plt.barh(xpos, Y1, align='center', height=width, alpha=0.9, label='Category A')

    ax.set_yticks(xpos)  # 确定每个记号的位置
    ax.set_yticklabels(X)  # 确定每个记号的内容

    plt.title(title)

    autolabelH(bars1, ax)

    if len(savPath) == 0:
        plt.show()
    else:
        graph_fullpath = '{}\{}.png'.format(savPath, title)
        plt.savefig(graph_fullpath)
    return

#给每个柱子上面添加标注
def autolabelH(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        width = rect.get_width()
        ax.annotate('{}'.format(width),
              xy=(width, rect.get_y() + rect.get_height() / 2),
              xytext=(3, 0),  # 3 points vertical offset
              textcoords="offset points",
              ha='left', va='center'
              )

#给每个柱子上面添加标注
def autolabelV(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
              xy=(rect.get_x() + rect.get_dwith() / 2, height),
              xytext=(0, 3),  # 3 points vertical offset
              textcoords="offset points",
              ha='center', va='top'
              )

def drawBarAll(path=''):
    # drawBarGraph('test', savPath=path)
    for datatype in historyLib.datatypeSet:
        drawBarGraph('{}数据-文件总数'.format(datatype), datatype, historyLib.STAT_KEY_FILE_CNT, savPath=path)
        drawBarGraph('{}数据-数据大小(kB)'.format(datatype), datatype, historyLib.STAT_KEY_STOREAGE_CNT, savPath=path)
        drawBarGraph('{}数据-记录总数'.format(datatype), datatype, historyLib.STAT_KEY_RECORD_CNT, savPath=path)
        drawBarGraph('{}数据-表字段数'.format(datatype), datatype, historyLib.STAT_KEY_FIELD_CNT, savPath=path)
        drawBarGraph('{}数据-统计站点总数'.format(datatype), datatype,  savPath=path )

def drawPlotAll(path=''):
    for market in historyLib.marketSet:
        for datatype in historyLib.datatypeSet:
            drapPlotGraph('test', 'shase', 'day', historyLib.STAT_KEY_FILE_CNT)



def drapPlotGraph(title, market, datatype, field, savPath=''):
    X, Y = historyLib.siMarketDict.gethostFieldList(market, datatype, field)
    print(X)
    plt.plot(X, Y)

    plt.xticks(rotation=45)
    plt.title(title)

    plt.show()

    return
