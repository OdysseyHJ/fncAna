from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class MyTable(QTableWidget):
    def __init__(self,parent=None):
        super(MyTable, self).__init__(parent)
        self.setWindowTitle("我是一个表格")
        # self.setWindowIcon(QIcon("male.png"))
        self.resize(920, 240)
        self.setColumnCount(5)
        self.setRowCount(2)
        #设置表格有两行五列。
        self.setColumnWidth(0, 200)
        self.setColumnWidth(4, 200)
        # self.setRowHeight(1, 500)
        #设置第一行高度为100px，第一列宽度为200px。

        self.table()

    def table(self):
        self.setItem(0,0,QTableWidgetItem("           你的名字"))
        self.setItem(0,1,QTableWidgetItem("性别"))
        self.setItem(0,2,QTableWidgetItem("出生日期"))
        self.setItem(0,3, QTableWidgetItem("职业"))
        self.setItem(0,4, QTableWidgetItem("收入"))
        #添加表格的文字内容.
        self.setHorizontalHeaderLabels(["第一行", "第二行", "第三行", "第四行", "第五行"])
        self.setVerticalHeaderLabels(["第一列", "第二列"])


        #设置表头
        lbp = QLabel()
        lbp.setPixmap(QPixmap("Male.png"))
        self.setCellWidget(1,1,lbp)
        #在表中添加一张图片
        twi = QTableWidgetItem("      新海诚")
        twi.setFont(QFont("Times", 10, ))
        self.setItem(1,0,twi)
        #添加一个自己设置了大小和类型的文字。
        dte = QDateTimeEdit()
        dte.setDateTime(QDateTime.currentDateTime())
        dte.setDisplayFormat("yyyy/MM/dd")
        dte.setCalendarPopup(True)
        self.setCellWidget(1,2,dte)
        #添加一个弹出的日期选择，设置默认值为当前日期,显示格式为年月日。
        cbw = QComboBox()
        cbw.addItem("医生")
        cbw.addItem("老师")
        cbw.addItem("律师")
        self.setCellWidget(1,3,cbw)
        #添加了一个下拉选择框
        sb = QSpinBox()
        sb.setRange(1000,10000)
        sb.setValue(5000)#设置最开始显示的数字
        sb.setDisplayIntegerBase(10)#这个是显示数字的进制，默认是十进制。
        sb.setSuffix("元")#设置后辍
        sb.setPrefix("RMB: ")#设置前辍
        sb.setSingleStep(100)
        self.setCellWidget(1,4,sb)

def proc():
    app = QApplication(sys.argv)
    myTable = MyTable()
    myTable.show()
    app.exit(app.exec_())