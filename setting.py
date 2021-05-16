




# 文件配置路径
# 分析根路径

# fucntion
def makepath(root, sub):
    pathSeq = (root, sub)
    return slash.join(pathSeq)


slash = '\\'
rootpath = r'H:\HJ_Docs\公式统计'

initPaht = makepath(rootpath, r'最新公式包\plugins_add')
oringinDataPath = makepath(rootpath, r'true_online_plugins\true_online_plugins')



# output
statInfoBaseHost = makepath(rootpath, r'站点主体统计.csv')


