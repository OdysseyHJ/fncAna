import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import historyLib
import graphlib
import hjio

class CDrawParam:
    def __init__(self):
        self.graphtype = ''
        self.market = ''
        self.datatype = ''
        self.field = ''
        self.abbrx = False

    def setGraphtype(self, content):
        self.graphtype = content
    def setMarket(self, content):
        for key in historyLib.marketChn.keys():
            if content == historyLib.marketChn[key]:
                self.market = key
    def setDatatype(self, content):
        for key in historyLib.datatypeChn.keys():
            if content == historyLib.datatypeChn[key]:
                self.datatype = key
    def setField(self, content):
        for key in historyLib.statKeyChn.keys():
            if content == historyLib.statKeyChn[key]:
                self.field = key
    def setAbbrx(self, content):
        if content == 0:
            self.abbrx = False
        else:
            self.abbrx = True

    def show(self):
        print(self.graphtype, self.market, self.datatype, self.field, self.abbrx)
        hjio.writelog("{}, {}, {}, {}, {}".format(self.graphtype, self.market, self.datatype, self.field, self.abbrx))

class CHistoryDraw(QWidget):
    def __init__(self):
        super().__init__()
        self.drawparam = CDrawParam()
        self.initUI()

    def initUI(self):
        self.initCompose()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('绘图工具')
        self.setWindowIcon(QIcon('AC.jpg'))
        self.show()

    def initCompose(self):
        xPos = 100
        xOffset = 60
        yPos = 20
        lbYOffset = 8
        yOffset = 60
        xSize = 200
        ySize = 30

        self.lbGraphType = QLabel(self)
        self.lbGraphType.move(xPos-xOffset,yPos+lbYOffset)
        self.lbGraphType.setText('图表类型')
        self.lbGraphType.adjustSize()
        self.cbGraphType = QComboBox(self)
        self.cbGraphType.move(xPos, yPos)
        self.cbGraphType.resize(xSize, ySize)
        yPos += yOffset
        graphtypeList = ['全市场柱形图', '全站点曲线图']
        self.drawparam.setGraphtype(graphtypeList[0])
        self.cbGraphType.addItems(graphtypeList)
        self.cbGraphType.currentIndexChanged[str].connect(self.drawparam.setGraphtype)

        self.lbMarket = QLabel(self)
        self.lbMarket.move(xPos-xOffset,yPos+lbYOffset)
        self.lbMarket.setText('市场')
        self.lbMarket.adjustSize()
        self.cbMarket = QComboBox(self)
        self.cbMarket.move(xPos, yPos)
        self.cbMarket.resize(xSize, ySize)
        yPos += yOffset
        marketList = list(sorted(historyLib.marketChn.values()))
        self.drawparam.setMarket(marketList[0])
        self.cbMarket.addItems(marketList)
        self.cbMarket.currentIndexChanged[str].connect(self.drawparam.setMarket)

        self.lbDatatype = QLabel(self)
        self.lbDatatype.move(xPos-xOffset,yPos+lbYOffset)
        self.lbDatatype.setText('数据类型')
        self.lbDatatype.adjustSize()
        self.cbDatatype = QComboBox(self)
        self.cbDatatype.move(xPos, yPos)
        self.cbDatatype.resize(xSize, ySize)
        yPos += yOffset
        datatypeList = list(sorted(historyLib.datatypeChn.values()))
        self.drawparam.setDatatype(datatypeList[0])
        self.cbDatatype.addItems(datatypeList)
        self.cbDatatype.currentIndexChanged[str].connect(self.drawparam.setDatatype)

        self.lbField = QLabel(self)
        self.lbField.move(xPos-xOffset,yPos+lbYOffset)
        self.lbField.setText('统计数据')
        self.lbField.adjustSize()
        self.cbField = QComboBox(self)
        self.cbField.move(xPos, yPos)
        self.cbField.resize(xSize, ySize)
        yPos += yOffset
        fieldList = list(sorted(historyLib.statKeyChn.values()))
        self.drawparam.setField(fieldList[0])
        self.cbField.addItems(fieldList)
        self.cbField.currentIndexChanged[str].connect(self.drawparam.setField)

        self.lbAbbr = QLabel(self)
        self.lbAbbr.move(xPos-xOffset,yPos+lbYOffset)
        self.lbAbbr.setText('坐标缩放')
        self.lbAbbr.adjustSize()
        self.cbAbbr = QComboBox(self)
        self.cbAbbr.move(xPos, yPos)
        self.cbAbbr.resize(xSize, ySize)
        yPos += yOffset
        abbrList = ['否', '是']
        self.drawparam.setAbbrx(0)
        self.cbAbbr.addItems(abbrList)
        self.cbAbbr.currentIndexChanged[int].connect(self.drawparam.setAbbrx)

        self.qbtnDraw= QPushButton('绘图', self)
        self.qbtnDraw.clicked.connect(self.draw)
        self.qbtnDraw.resize(self.qbtnDraw.sizeHint())
        self.qbtnDraw.move(250, 400)

    def draw(self):
        self.drawparam.show()
        if self.drawparam.graphtype == '全市场柱形图':
            title = '{}-{}'.format(historyLib.datatypeChn[self.drawparam.datatype],
                                   historyLib.statKeyChn[self.drawparam.field])
            graphlib.drawBarGraph(title, self.drawparam.datatype, self.drawparam.field)
        elif self.drawparam.graphtype == '全站点曲线图':
            title = '{}-{}-{}'.format(historyLib.marketChn[self.drawparam.market],
                                      historyLib.datatypeChn[self.drawparam.datatype],
                                      historyLib.statKeyChn[self.drawparam.field])
            graphlib.drawPlotGraph(title, self.drawparam.market, self.drawparam.datatype, self.drawparam.field, self.drawparam.abbrx)

def init():

    app = QApplication(sys.argv)
    ex = CHistoryDraw()
    # ex2 = fncTable([1,2,3])
    # ex2.show()
    sys.exit(app.exec_())
