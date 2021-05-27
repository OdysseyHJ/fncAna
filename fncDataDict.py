import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from enum import Enum

import fncData
from fnclib import fncObj
import fnclib


class Datatype(Enum):
    Int = 1
    String = 2
    float = 3

class CFncDataDict(QWidget):
    def __init__(self):
        super().__init__()


        # self.lblID = 0
        self.fobjIn = fncObj()
        self.sections = {}

        self.initUI()

    def initUI(self):
        self.initResDisplay()
        self.initLable()
        self.initBotton()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.qbtnSearch)
        # hbox.addWidget(cancelButton)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setGeometry(800, 400, 400, 800)
        self.setWindowTitle('公式字典')
        self.setWindowIcon(QIcon('AC.jpg'))
        self.show()

    def initResDisplay(self):
        xPos = 500
        yPos = 100
        self.DispInfo = QLabel(self)
        self.DispInfo.move(xPos, yPos)
        self.DispInfo.setText('')
        self.DispInfo.adjustSize()

    def initLable(self):

        horizonPos = 60
        horizonPosOff = 140
        vertiPos = 80
        secLine = 40

        # ID
        pos = (horizonPos, vertiPos)
        self.initSection(pos, 'ID', Datatype.Int)

        # 公式名
        vertiPos += secLine
        pos = (horizonPos, vertiPos)
        self.initSection(pos, 'Name', Datatype.String)

        # 公式内容匹配
        vertiPos += secLine
        pos = (horizonPos, vertiPos)
        self.initSection(pos, 'Content', Datatype.String)


    def initSection(self, pos, key='default', type = Datatype.String):
        xPos = pos[0]
        yPos = pos[1]

        self.sections[key] = CSection(self)

        # 标题
        self.sections[key].lblTitle.move(xPos, yPos+8)
        self.sections[key].lblTitle.setText(key)
        self.sections[key].lblTitle.adjustSize()

        # 输入框
        self.sections[key].qleIn.move(xPos+40, yPos)
        self.sections[key].qleIn.textChanged[str].connect(self.sections[key].inputChange)
        self.sections[key].type = type

        # 消息框
        self.sections[key].lblMsg.move(xPos+150, yPos+8)

    def initBotton(self):
        self.qbtnSearch = QPushButton('查询', self)
        self.qbtnSearch.clicked.connect(self.search)
        self.qbtnSearch.resize(self.qbtnSearch.sizeHint())
        self.qbtnSearch.move(700, 50)

        # qbtnSearch = QPushButton('查询', self)
        # qbtnSearch.clicked.connect(self.search)
        # qbtnSearch.resize(qbtnSearch.sizeHint())
        # qbtnSearch.move(700, 50)


    def search(self):
        fobj = self.getSearchFobj()
        searchRes = self.selectInDatabase(fobj)
        self.searchResShow(searchRes)

        self.fTable = fncTable(searchRes)

        return

    def getSearchFobj(self):
        fobj = fncObj()
        for key in self.sections.keys():
            if key == 'ID':
                fobj.id = self.sections[key].data
            elif key == 'Name':
                fobj.name = self.sections[key].data
            elif key == 'Content':
                fobj.algrithm = self.sections[key].data

        return fobj

    # @staticmethod
    def selectInDatabase(self, sfobj):
        res = []
        # 公式id匹配
        if sfobj.id != 0:
            if sfobj.id in fncData.baseDict.keys():
                res = fncData.baseDict[sfobj.id]
            else:
                return res
        else:
            keylist = list(fncData.baseDict.keys())
            keylist.sort()
            for key in keylist:
                res += fncData.baseDict[key]

        # 公式名字匹配
        tempRes = []
        try:
            if len(sfobj.name) != 0:
                for fobj in res:
                    if fobj.name.find(sfobj.name) >= 0:
                        tempRes.append(fobj)

                res = tempRes
        except:
            print('process name failed!')

        # 公式内容匹配
        tempRes = []
        try:
            print(type(sfobj.algrithm))
            if len(sfobj.algrithm) != 0:

                for fobj in res:
                    if fobj.algrithm.find(sfobj.algrithm) >= 0:
                        tempRes.append(fobj)
                res = tempRes
        except:
            print('process content failed!')

        return res

    def searchResShow(self, res):
        str = 'founded!'
        # disTemp = '{}\n'
        # for fobj in res:
        #     str += disTemp.format(fobj.fname)

        if len(res) == 0:
            str = 'not found!'

        self.DispInfo.setText(str)
        self.DispInfo.adjustSize()




class CSection:
    def __init__(self, cfdt):
        self.lblTitle = QLabel(cfdt)
        self.lblMsg = QLabel(cfdt)
        self.qleIn = QLineEdit(cfdt)
        self.data = 0
        self.type = Datatype.Int

    def inputChange(self, text):
        self.lblMsg.setText('')
        self.lblMsg.adjustSize()

        if self.type == Datatype.Int:
            self.data = 0
        elif self.type == Datatype.String:
            self.data = ''
        elif self.type == Datatype.float:
            self.data = 0.0

        if len(text) == 0:
            return

        if self.type == Datatype.Int:
            try:
                self.data = int(text)
            except:
                self.lblMsg.setText('input invalid!')
                self.lblMsg.adjustSize()
        else:
            self.data = text

        return



class fncTable(QTableWidget):
    def __init__(self,fobjlist, parent=None):
        super(fncTable, self).__init__(parent)

        self.setWindowTitle("公式表")
        # self.setWindowIcon(QIcon("male.png"))
        self.resize(960, 600)

        # 设置行数列数
        rowCnt = len(fobjlist)
        self.setRowCount(rowCnt)
        self.setColumnCount(5)

        # 设置行列标题
        rowNumList = [str(x) for x in range(1, rowCnt+1)]
        self.setVerticalHeaderLabels(rowNumList)
        columnNamelist = ['公式ID', '公式名', '文件名', '安装目录', '适用周期']
        self.setHorizontalHeaderLabels(columnNamelist)

        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)

        # 设置表格数据
        self.setTable(fobjlist)
        # self.resizeRowsToContents()
        # self.resizeColumnsToContents()

        self.show()
        #设置表格有两行五列。
        # self.setColumnWidth(0, 200)
        # self.setColumnWidth(4, 200)

    def setTable(self, fobjlist):
        for ii in range(len(fobjlist)):
            btn = FidButton(fobjlist[ii])
            btn.setDown(True)
            # 修改按钮大小
            btn.setStyleSheet("QPushButton{margin:3px};")
            btn.clicked.connect(btn.showInfo)
            # 将按钮添加到单元格
            self.setCellWidget(ii, 0, btn)
            self.setItem(ii, 1, QTableWidgetItem(str(fobjlist[ii].name)))
            self.setItem(ii, 2, QTableWidgetItem(str(fobjlist[ii].fname)))
            self.setItem(ii, 3, QTableWidgetItem(str(fobjlist[ii].directory)))
            self.setItem(ii, 4, QTableWidgetItem(str(fobjlist[ii].period)))



class FidButton(QPushButton):
    def __init__(self, fobj):
        super().__init__(str(fobj.id))

        self.fobj = fobj

    def showInfo(self):
        self.infoTbl = fncInfoTable(self.fobj)

class fncInfoTable(QTableWidget):
    def __init__(self, fobj):
        super().__init__()

        self.setWindowTitle("公式详细信息")

        # 设置大小
        self.resize(1200, 1000)

        # 设置行数列数
        rowCnt = 1
        columCnt = 3
        self.setRowCount(rowCnt)
        self.setColumnCount(columCnt)

        # 设置行列标题
        self.setVerticalHeaderLabels(['info'])
        columnNamelist = ['公式ID', '公式算法', '公式文件内容']
        self.setHorizontalHeaderLabels(columnNamelist)
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 600)
        self.setColumnWidth(2, 500)
        self.setRowHeight(0, 500)
        # self.setText
        # self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            # horizontalHeader().setCascadingSectionResizes(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 设置表格数据
        self.setTable(fobj)

        self.show()


    def setTable(self,fobj):
        item0 = QTableWidgetItem(str(fobj.id))
        item0.setTextAlignment(Qt.AlignTop)
        self.setItem(0, 0, item0)
        item1 = QTableWidgetItem(str(fobj.algrithm))
        item1.setTextAlignment(Qt.AlignTop)
        self.setItem(0, 1, item1)
        item2 = QTableWidgetItem(str(fobj.content))
        item2.setTextAlignment(Qt.AlignTop)
        self.setItem(0, 2, item2)

def proc():
    app = QApplication(sys.argv)
    ex = CFncDataDict()
    # ex2 = fncTable([1,2,3])
    # ex2.show()
    sys.exit(app.exec_())