import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['Microsoft YaHei']

import historyLib


def drawBarGraph(title, datatype='day', fieldtype='hostcount', savPath=''):
    # print(title, datatype, fieldtype)
    X, Y1 = historyLib.siMarketDict.getDatatypeFieldList(datatype, fieldtype)
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
            drawPlotGraph('test', 'hk', 'day', historyLib.STAT_KEY_FIELD_CNT, True)


def drawPlotGraph(title, market, datatype, field, abbrx=False, savPath=''):
    # print(title, market, datatype, field, abbrx)
    X, Y = historyLib.siMarketDict.gethostFieldList(market, datatype, field)
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.plot(X, Y)

    xStep = 1
    xpos = np.arange(0, len(X), xStep)
    if abbrx:
        xStep = len(X) // 20
        if xStep < 1:
            xStep = 1
        print(xStep)
        ax.set_xticks(xpos[::xStep])  # 确定每个记号的位置
        ax.set_xticklabels(X[::xStep])  # 确定每个记号的内容

    plt.xticks(rotation=90)
    plt.title(title)
    plt.show()

    return
