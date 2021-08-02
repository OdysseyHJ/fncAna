
import hjio



# 文件配置路径
# 分析根路径


slash = '\\'


# home path
# rootpath = r'H:\HJ_Docs\公式统计'

# ths path
# rootpath = r'D:\HJ_EX_Docs\公式原始数据'
# rootpath = r'D:\HJ_EX_Docs\公式原始数据\新版本统计信息'
rootpath = r'D:\HJ_EX_Docs\HQSERVER\HQSERVER-2630'


def makepath(root, sub):
    pathSeq = (root, sub)
    return slash.join(pathSeq)

# initPaht = makepath(rootpath, r'最新公式包\plugins_add')
initPath = r'.\plugins'
oringinDataPath = makepath(rootpath, r'true_online_plugins\true_online_plugins')

appendPath = makepath(rootpath, r'HJNBxxx')

# fncAll = makepath(rootpath, r'fncAll20210529')
fncAll = makepath(rootpath, r'fncAll20210531')
renamePath = makepath(rootpath, r'renameFolder')

# output
statInfoBaseHost = makepath(rootpath, r'站点主体统计.csv')
notExInfo = makepath(rootpath, r'base缺少的公式.txt')


# host analysis
repopath = makepath(rootpath, r'host信息\正式环境.txt')
packpaht = makepath(rootpath, r'host信息\packres.txt')
# diffABpaht = makepath(rootpath, r'host信息\diffAB.txt')
# diffBApaht = makepath(rootpath, r'host信息\diffBA.txt')

# 数据字典
confluencedict = makepath(rootpath, r'数据字典\dict1.csv')
excelDict = makepath(rootpath, r'数据字典\excelDict.csv')


# 日志路径
# logpath = makepath(rootpath, r'\log\\')
logpath = r'.\log\\'

# 用户录包
userReqPath = makepath(rootpath, r'用户请求录包')
idRefAna = makepath(rootpath, r'UserReqAna.txt')
idCountPath = makepath(rootpath, r'reqIDcount.csv')

###################################################
#          history data
###################################################
history_data_path = makepath(rootpath, r'\history_data\stat')
table_path = makepath(rootpath, r'\table')
graph_bar_path = makepath(rootpath, r'\graph\bar')
graph_plot_path = makepath(rootpath, r'\graph\plot')