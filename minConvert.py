
import sys
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QLineEdit, QApplication, QPushButton)



# class HJtime:
#     self

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.inputtime = 0
        self.outputtime = 0

    def initUI(self):
        self.lbl = QLabel(self)
        qle = QLineEdit(self)

        qle.move(60, 100)
        self.lbl.move(60, 80)

        qle.textChanged[str].connect(self.onChanged)

        # 初始化button
        qbtn = QPushButton('转换正常时间', self)
        qbtn.clicked.connect(self.thsmin2time)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)

        # 初始化button
        qbtn2 = QPushButton('转换同花顺时间', self)
        qbtn2.clicked.connect(self.time2thsmin)
        qbtn2.resize(qbtn2.sizeHint())
        qbtn2.move(50, 30)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QLineEdit')
        self.show()

    def onChanged(self, text):
        try:
            inttime = int(text)
            self.inputtime = inttime
            self.lbl.setText('')
            self.lbl.adjustSize()
        except:
            self.lbl.setText('input invalid!')
            self.lbl.adjustSize()


    def time2thsmin(self):
        '''yyyymmddHHMM'''
        stdtime = self.inputtime
        print(stdtime)
        year = stdtime // 100000000 % 10000
        month = stdtime // 1000000 % 100
        day = stdtime // 10000 % 100
        hour = stdtime // 100 % 100
        minute = stdtime % 100
        thsmin = (year - 1900) * (1<<20) + month * (1<<16) + day * (1<<11) + hour * (1<<6) + minute
        self.lbl.setText(str(thsmin))
        self.lbl.adjustSize()

    def thsmin2time(self):
        thsmin = self.inputtime

        stdtime = 222
        self.lbl.setText(str(stdtime))
        self.lbl.adjustSize()



def proc():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())