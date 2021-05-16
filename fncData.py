import fnclib
















# 统一包公式属性


# 统一库信息
# plugins 公式数
# @free 公式数
# @level2 公式数
# 公式总数 1034
stdInfo = (878, 85, 71, 1034)



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
                723573)

# key:fncid
# value:list [fncObj1, fncObj2, ...]
baseDict = {}




def init(folderpath):
    global baseDict
    baseDict = fnclib.getFncDict(folderpath, 'base')

    # for key in fncdict.keys():
    #     for each in fncdict[key]:
    #         each.showInfo()



