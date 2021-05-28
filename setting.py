
import hjio



# 文件配置路径
# 分析根路径


slash = '\\'


# home path
# rootpath = r'H:\HJ_Docs\公式统计'

# ths path
rootpath = r'D:\HJ_EX_Docs\公式原始数据'
# rootpath = r'D:\HJ_EX_Docs\公式原始数据\新版本统计信息'


def makepath(root, sub):
    pathSeq = (root, sub)
    return slash.join(pathSeq)

initPaht = makepath(rootpath, r'最新公式包\plugins_add')
oringinDataPath = makepath(rootpath, r'true_online_plugins\true_online_plugins')

appendPath = makepath(rootpath, r'HJNBxxx')

fncAll = makepath(rootpath, r'fncAll20210520')
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