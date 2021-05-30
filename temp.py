# # import qtpy
#
# import sys
# from PyQt5.QtCore import pyqtSignal, QPoint
# from PyQt5.QtGui import QFont, QEnterEvent, QPainter, QColor, QPen
# from PyQt5.QtWidgets import QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QGridLayout
# from PyQt5.QtWidgets import QLineEdit
# from PyQt5.QtWidgets import QLabel
# from PyQt5.QtGui import QIcon
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
# from PyQt5 import QtGui
# from PyQt5.QtCore import QSize
# from sqlalchemy import create_engine
# import time
# import pandas as pd
# from docx import Document
# import os
#
# backimg = 'D:\HJ_Mind-Note\fncprior.png'  # 设置背景图 不设置可能存在问题 自己图片路径
# icoimg = 'D:\HJ_Mind-Note\fncprior.png'  # ico图标
# # ------------------------------------------------------------------------------------------------------------------------
# #                                           数据库连接 及 导出
# # ------------------------------------------------------------------------------------------------------------------------
#
# class Conndatabase:
#     # 初始化连接数据库
#     def __init__(self, DATABASE, USER, PASSWORD, IP, PORT, NAME):
#         # 初始化oracle字符集 防止乱码
#         os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
#         self.DATABASE = DATABASE
#         self.USER = USER
#         self.PASSWORD = PASSWORD
#         self.IP = IP
#         self.PORT = PORT
#         self.NAME = NAME
#         self.POSTGRE = None
#         self._conn()
#
#     def _conn(self):
#         try:
#             if self.DATABASE == 'postgresql' or self.DATABASE == 'postgres':
#                 self.POSTGRE = create_engine(
#                     'postgresql://{}:{}@{}:{}/{}'.format(self.USER, self.PASSWORD, self.IP, self.PORT, self.NAME))
#             if self.DATABASE == 'oracle':
#                 # engine = create_engine("oracle+cx_oracle://username:password@host:port/servicename")
#                 gg = "oracle+cx_oracle://{}:{}@{}:{}/{}".format(self.USER, self.PASSWORD, self.IP, self.PORT, self.NAME)
#                 self.POSTGRE = create_engine(gg, encoding='utf-8', echo=True)
#             if self.DATABASE == 'mysql':
#                 self.POSTGRE = create_engine(
#                     'mysql+pymysql://{}:{}@{}:{}/{}'.format(self.USER, self.PASSWORD, self.IP, self.PORT, self.NAME))
#         except Exception as e:
#             print(e)
#             time.sleep(3)
#             self._conn()
#
#     # 获取表设计信息 只入参数据库名返回表名 入参数据库和表名返回对应字段信息
#     def tableinfo(self, databasename, *args):
#         # 此为MySQL
#         if self.DATABASE == 'mysql':
#             try:
#                 if args:
#                     tablename = args[0]
#                     sql = r'''select  column_name,is_nullable,data_type,character_maximum_length,column_comment from information_schema.columns where table_schema = '{}' AND table_name = '{}'
#         '''.format(databasename, tablename)
#                     info = pd.read_sql(sql, self.POSTGRE).values
#                 else:
#                     sql = r'''select  table_name,column_name,is_nullable,data_type,character_maximum_length,column_comment from information_schema.columns where table_schema = '{}'
#         '''.format(databasename)
#                     talbeinfo = pd.read_sql(sql, self.POSTGRE).values
#                     # 去重得到tablename
#                     info = set(talbeinfo[:, 0])
#                 return info
#             except Exception as e:
#                 print(e)
#                 return False
#         # 此为postgresql
#         elif self.DATABASE == 'postgresql' or self.DATABASE == 'postgres':
#             try:
#                 if args:
#                     tablename = args[0]
#                     sql = r'''select NAME,attnotnull,TYPE,case when type = 'timestamp(0) without time zone'  then 'nan'  when position = 0 then 'nan' else   substr(type,position('(' in type)+1,char_length(type) - position('(' in type) -1 ) end as length,COMMENT from (
#                                 SELECT
#                                  A.attname AS NAME,
#                                  A.attnotnull AS attnotnull,
#                                  format_type ( A.atttypid, A.atttypmod ) AS TYPE,
#                                  col_description ( A.attrelid, A.attnum ) AS COMMENT,
#                                  position('(' in format_type ( A.atttypid, A.atttypmod ))
#                                 FROM
#                                  pg_class AS C,
#                                  pg_attribute AS A
#                                 WHERE
#                                  C.relname = '{}'
#                                  AND A.attrelid = C.oid
#                                  AND A.attnum > 0)a
#  '''.format(tablename)
#                     info = pd.read_sql(sql, self.POSTGRE).values
#                 else:
#                     sql = r'''select tablename from pg_tables where schemaname='public' and position('_2' in tablename)=0;'''
#                     talbeinfo = pd.read_sql(sql, self.POSTGRE).values
#                     info = set(talbeinfo[:, 0])
#                 return info
#             except Exception as e:
#                 print(e)
#                 return False
#         elif self.DATABASE == 'oracle':
#             try:
#                 if args:
#                     tablename = args[0]
#                     sql = r'''select a.COLUMN_NAME,a.NULLABLE,a.DATA_TYPE,a.DATA_LENGTH,b.comments
#                                 from dba_tab_columns a,user_col_comments b
#                                 where a.column_name=b.column_name
#                                 and a.table_name = b.table_name
#                                 and a.table_name = '{}' '''.format(tablename)
#                     info = pd.read_sql(sql, self.POSTGRE).values
#                 else:
#                     sql = r'''select * from user_tab_comments'''
#                     talbeinfo = pd.read_sql(sql, self.POSTGRE).values
#                     info = set(talbeinfo[:, 0])
#                 return info
#             except Exception as e:
#                 print(e)
#                 return False
#
#         # 预留位
#         else:
#             print('目前数据库支持postgre,mysql,oracle')
#             return False
#
#     # 执行SQL 增查执行并返回 删和改只执行
#     def perform(self, SQL):
#         try:
#             return pd.read_sql(SQL, self.POSTGRE).values
#         except Exception as e:
#             print(e)
#             return True
#
#
# # 保存word文档
# def saveword(database, user, passwd, ip, port, database_name):
#     # 连接数据库信息
#     connmysql = Conndatabase(database, user, passwd, ip, port, database_name)
#     # connmysql = Conndatabase('mysql','root','rootsasa','192.168.0.29','3306','incontrol')
#     # 数据名
#     # database_name = 'incontrol'
#     # 获取到databasename下的所有的表
#     tablenames = connmysql.tableinfo(database_name)
#     # 文档
#     document = Document()
#     if not tablenames:
#         return False
#     try:
#         for tablename in tablenames:
#             tableinfo = connmysql.tableinfo(database_name, tablename)
#             # 文档标题
#             document.add_heading('{}表字段信息'.format(tablename), 2)
#             # 存入文档
#             table = document.add_table(rows=1, cols=5, style="Light Shading")
#             hdr_cells = table.rows[0].cells
#             hdr_cells[0].text = '字段'
#             hdr_cells[1].text = 'NULL'
#             hdr_cells[2].text = '类型'
#             hdr_cells[3].text = '长度'
#             hdr_cells[4].text = '说明'
#             for id, key, type, lenth, info in tableinfo:
#                 row_cells = table.add_row().cells
#                 row_cells[0].text = '{}'.format(id)
#                 row_cells[1].text = '{}'.format(key)
#                 row_cells[2].text = '{}'.format(type)
#                 try:
#                     row_cells[3].text = '{:.0f}'.format(float(lenth))
#                 except:
#                     row_cells[3].text = '{}'.format(lenth)
#                 row_cells[4].text = '{}'.format(info)
#     except Exception as e:
#         print(e)
#         return False
#     else:
#         # 保存文档名
#         if database == 'oracle':
#             document.save('oracle_{}库文档.docx'.format(user))
#         else:
#             document.save('{}_{}库文档.docx'.format(database, database_name))
#         return True
#
#
# # ------------------------------------------------------------------------------------------------------------------------
# #                                           pyqt5界面
# # ------------------------------------------------------------------------------------------------------------------------
#
# # 默认值设置 输入就是最后一次输入的值
# try:
#     with open('./export_doc_default.txt', 'r', encoding='utf8')as fr:
#         li = fr.readlines()
#         database_box_default = li[0].replace('\n', '')
#         user_box_default = li[1].replace('\n', '')
#         passwd_box_default = li[2].replace('\n', '')
#         ip_box_default = li[3].replace('\n', '')
#         port_box_default = li[4].replace('\n', '')
#         database_name_box_default = li[5].replace('\n', '')
#     if '.' not in ip_box_default:
#         raise Exception('使用初始值')
#     int(port_box_default)
# # 第一次初始值
# except Exception as e:
#     # default
#     database_box_default = 'mysql'
#     user_box_default = 'root'
#     passwd_box_default = '123456'
#     ip_box_default = '192.168.0.1'
#     port_box_default = '3306'
#     database_name_box_default = 'incontrol'
#
# # 样式
# StyleSheet = """
# /*最小化最大化关闭按钮通用默认背景*/
# #buttonMinimum,#buttonMaximum,#buttonClose {
#     border: none;
# }
# #buttonClose,#buttonMaximum,#buttonMinimum{
#     color:white;
# }
# /*悬停*/
# #buttonMinimum:hover,#buttonMaximum:hover {
#     color: white;
# }
# #buttonClose:hover {
#     color: white;
# }
# /*鼠标按下不放*/
# #buttonMinimum:pressed,#buttonMaximum:pressed {
#     color:white;
# }
# #buttonClose:pressed {
#     color: white;
# }
# """
#
#
# class TitleBar(QWidget):
#     # 窗口最小化信号
#     windowMinimumed = pyqtSignal()
#     # 窗口最大化信号
#     windowMaximumed = pyqtSignal()
#     # 窗口还原信号
#     windowNormaled = pyqtSignal()
#     # 窗口关闭信号
#     windowClosed = pyqtSignal()
#     # 窗口移动
#     windowMoved = pyqtSignal(QPoint)
#
#     def __init__(self, *args, **kwargs):
#         super(TitleBar, self).__init__(*args, **kwargs)
#         self.setStyleSheet(StyleSheet)
#         self.mPos = None
#         self.iconSize = 20  # 图标的默认大小
#         # 布局
#         layout = QHBoxLayout(self, spacing=0)
#         layout.setContentsMargins(0, 0, 0, 0)
#         # 窗口图标
#         self.iconLabel = QLabel(self)
#         #         self.iconLabel.setScaledContents(True)
#         layout.addWidget(self.iconLabel)
#         # 窗口标题
#         self.titleLabel = QLabel(self)
#         self.titleLabel.setStyleSheet("color:white")
#         self.titleLabel.setMargin(2)
#         layout.addWidget(self.titleLabel)
#         # 中间伸缩条
#         layout.addSpacerItem(QSpacerItem(
#             40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
#         # 利用Webdings字体来显示图标
#         font = self.font() or QFont()
#         font.setFamily('Webdings')
#         # 最小化按钮
#         self.buttonMinimum = QPushButton(
#             '0', self, clicked=self.windowMinimumed.emit, font=font, objectName='buttonMinimum')
#         layout.addWidget(self.buttonMinimum)
#         # 最大化/还原按钮
#         self.buttonMaximum = QPushButton(
#             '1', self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
#         layout.addWidget(self.buttonMaximum)
#         # 关闭按钮
#         self.buttonClose = QPushButton(
#             'r', self, clicked=self.windowClosed.emit, font=font, objectName='buttonClose')
#         layout.addWidget(self.buttonClose)
#         # 初始高度
#         self.setHeight()
#
#     def showMaximized(self):
#         if self.buttonMaximum.text() == '1':
#             # 最大化
#             self.buttonMaximum.setText('2')
#             self.windowMaximumed.emit()
#         else:  # 还原
#             self.buttonMaximum.setText('1')
#             self.windowNormaled.emit()
#
#     def setHeight(self, height=38):
#         """设置标题栏高度"""
#         self.setMinimumHeight(height)
#         self.setMaximumHeight(height)
#         # 设置右边按钮的大小
#         self.buttonMinimum.setMinimumSize(height, height)
#         self.buttonMinimum.setMaximumSize(height, height)
#         self.buttonMaximum.setMinimumSize(height, height)
#         self.buttonMaximum.setMaximumSize(height, height)
#         self.buttonClose.setMinimumSize(height, height)
#         self.buttonClose.setMaximumSize(height, height)
#
#     def setTitle(self, title):
#         """设置标题"""
#         self.titleLabel.setText(title)
#
#     def setIcon(self, icon):
#         """设置图标"""
#         self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))
#
#     def setIconSize(self, size):
#         """设置图标大小"""
#         self.iconSize = size
#
#     def enterEvent(self, event):
#         self.setCursor(Qt.ArrowCursor)
#         super(TitleBar, self).enterEvent(event)
#
#     def mouseDoubleClickEvent(self, event):
#         super(TitleBar, self).mouseDoubleClickEvent(event)
#         self.showMaximized()
#
#     def mousePressEvent(self, event):
#         """鼠标点击事件"""
#         if event.button() == Qt.LeftButton:
#             self.mPos = event.pos()
#         event.accept()
#
#     def mouseReleaseEvent(self, event):
#         '''鼠标弹起事件'''
#         self.mPos = None
#         event.accept()
#
#     def mouseMoveEvent(self, event):
#         if event.buttons() == Qt.LeftButton and self.mPos:
#             self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))
#         event.accept()
#
#
# # 枚举左上右下以及四个定点
# Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)
#
#
# class FramelessWindow(QWidget):
#     # 四周边距
#     Margins = 5
#
#     def __init__(self, *args, **kwargs):
#         super(FramelessWindow, self).__init__(*args, **kwargs)
#         palette1 = QtGui.QPalette()
#         palette1.setBrush(self.backgroundRole(), QtGui.QBrush(
#             QtGui.QPixmap(backimg)))  # 设置背景图片
#         self.setPalette(palette1)
#         self.setAutoFillBackground(True)
#         self.setGeometry(300, 100, 800, 550)
#         self._pressed = False
#         self.Direction = None
#         # 无边框
#         self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
#         # 鼠标跟踪
#         self.setMouseTracking(True)
#         # 布局
#         layout = QVBoxLayout(self, spacing=0)
#         layout.setContentsMargins(0, 0, 0, 0)
#         # 标题栏
#         self.titleBar = TitleBar(self)
#         layout.addWidget(self.titleBar)
#         # 信号槽
#         self.titleBar.windowMinimumed.connect(self.showMinimized)
#         self.titleBar.windowMaximumed.connect(self.showMaximized)
#         self.titleBar.windowNormaled.connect(self.showNormal)
#         self.titleBar.windowClosed.connect(self.close)
#         self.titleBar.windowMoved.connect(self.move)
#         self.windowTitleChanged.connect(self.titleBar.setTitle)
#         self.windowIconChanged.connect(self.titleBar.setIcon)
#
#     def setTitleBarHeight(self, height=38):
#         """设置标题栏高度"""
#         self.titleBar.setHeight(height)
#
#     def setIconSize(self, size):
#         """设置图标的大小"""
#         self.titleBar.setIconSize(size)
#
#     def setWidget(self, widget):
#         """设置自己的控件"""
#         if hasattr(self, '_widget'):
#             return
#         self._widget = widget
#         # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
#         self._widget.setAutoFillBackground(True)
#         self._widget.installEventFilter(self)
#         self.layout().addWidget(self._widget)
#
#     def move(self, pos):
#         if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
#             # 最大化或者全屏则不允许移动
#             return
#         super(FramelessWindow, self).move(pos)
#
#     def showMaximized(self):
#         """最大化,要去除上下左右边界,如果不去除则边框地方会有空隙"""
#         super(FramelessWindow, self).showMaximized()
#         self.layout().setContentsMargins(0, 0, 0, 0)
#
#     def showNormal(self):
#         """还原,要保留上下左右边界,否则没有边框无法调整"""
#         super(FramelessWindow, self).showNormal()
#         self.layout().setContentsMargins(0, 0, 0, 0)
#
#     def eventFilter(self, obj, event):
#         """事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式"""
#         if isinstance(event, QEnterEvent):
#             self.setCursor(Qt.ArrowCursor)
#         return super(FramelessWindow, self).eventFilter(obj, event)
#
#     def paintEvent(self, event):
#         """由于是全透明背景窗口,重绘事件中绘制透明度为1的难以发现的边框,用于调整窗口大小"""
#         super(FramelessWindow, self).paintEvent(event)
#         painter = QPainter(self)
#         painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.Margins))
#         painter.drawRect(self.rect())
#
#     def mousePressEvent(self, event):
#         """鼠标点击事件"""
#         super(FramelessWindow, self).mousePressEvent(event)
#         if event.button() == Qt.LeftButton:
#             self._mpos = event.pos()
#             self._pressed = True
#
#     def mouseReleaseEvent(self, event):
#         '''鼠标弹起事件'''
#         super(FramelessWindow, self).mouseReleaseEvent(event)
#         self._pressed = False
#         self.Direction = None
#
#     def mouseMoveEvent(self, event):
#         """鼠标移动事件"""
#         super(FramelessWindow, self).mouseMoveEvent(event)
#         pos = event.pos()
#         xPos, yPos = pos.x(), pos.y()
#         wm, hm = self.width() - self.Margins, self.height() - self.Margins
#         if self.isMaximized() or self.isFullScreen():
#             self.Direction = None
#             self.setCursor(Qt.ArrowCursor)
#             return
#         if event.buttons() == Qt.LeftButton and self._pressed:
#             self._resizeWidget(pos)
#             return
#         if xPos <= self.Margins and yPos <= self.Margins:
#             # 左上角
#             self.Direction = LeftTop
#             self.setCursor(Qt.SizeFDiagCursor)
#         elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
#             # 右下角
#             self.Direction = RightBottom
#             self.setCursor(Qt.SizeFDiagCursor)
#         elif wm <= xPos and yPos <= self.Margins:
#             # 右上角
#             self.Direction = RightTop
#             self.setCursor(Qt.SizeBDiagCursor)
#         elif xPos <= self.Margins and hm <= yPos:
#             # 左下角
#             self.Direction = LeftBottom
#             self.setCursor(Qt.SizeBDiagCursor)
#         elif 0 <= xPos <= self.Margins and self.Margins <= yPos <= hm:
#             # 左边
#             self.Direction = Left
#             self.setCursor(Qt.SizeHorCursor)
#         elif wm <= xPos <= self.width() and self.Margins <= yPos <= hm:
#             # 右边
#             self.Direction = Right
#             self.setCursor(Qt.SizeHorCursor)
#         elif self.Margins <= xPos <= wm and 0 <= yPos <= self.Margins:
#             # 上面
#             self.Direction = Top
#             self.setCursor(Qt.SizeVerCursor)
#         elif self.Margins <= xPos <= wm and hm <= yPos <= self.height():
#             # 下面
#             self.Direction = Bottom
#             self.setCursor(Qt.SizeVerCursor)
#
#     def _resizeWidget(self, pos):
#         """调整窗口大小"""
#         if self.Direction == None:
#             return
#         mpos = pos - self._mpos
#         xPos, yPos = mpos.x(), mpos.y()
#         geometry = self.geometry()
#         x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
#         if self.Direction == LeftTop:  # 左上角
#             if w - xPos > self.minimumWidth():
#                 x += xPos
#                 w -= xPos
#             if h - yPos > self.minimumHeight():
#                 y += yPos
#                 h -= yPos
#         elif self.Direction == RightBottom:  # 右下角
#             if w + xPos > self.minimumWidth():
#                 w += xPos
#                 self._mpos = pos
#             if h + yPos > self.minimumHeight():
#                 h += yPos
#                 self._mpos = pos
#         elif self.Direction == RightTop:  # 右上角
#             if h - yPos > self.minimumHeight():
#                 y += yPos
#                 h -= yPos
#             if w + xPos > self.minimumWidth():
#                 w += xPos
#                 self._mpos.setX(pos.x())
#         elif self.Direction == LeftBottom:  # 左下角
#             if w - xPos > self.minimumWidth():
#                 x += xPos
#                 w -= xPos
#             if h + yPos > self.minimumHeight():
#                 h += yPos
#                 self._mpos.setY(pos.y())
#         elif self.Direction == Left:  # 左边
#             if w - xPos > self.minimumWidth():
#                 x += xPos
#                 w -= xPos
#             else:
#                 return
#         elif self.Direction == Right:  # 右边
#             if w + xPos > self.minimumWidth():
#                 w += xPos
#                 self._mpos = pos
#             else:
#                 return
#         elif self.Direction == Top:  # 上面
#             if h - yPos > self.minimumHeight():
#                 y += yPos
#                 h -= yPos
#             else:
#                 return
#         elif self.Direction == Bottom:  # 下面
#             if h + yPos > self.minimumHeight():
#                 h += yPos
#                 self._mpos = pos
#             else:
#                 return
#         self.setGeometry(x, y, w, h)
#
#
# StyleSheet_2 = """
# QComboBox{
#         width: 150px;
#         height: 20px;
#         border-radius: 4px;
#         border: 1px solid rgb(111, 156, 207);
#         background: white;
# }
# QComboBox:enabled{
#         color: black;
# }
# QComboBox:!enabled {
#         color: rgb(80, 80, 80);
# }
# QComboBox:enabled:hover, QComboBox:enabled:focus {
#         color: rgb(51, 51, 51);
# }
# QComboBox::drop-down {
#         background: transparent;
# }
# QComboBox::drop-down:hover {
#         background: lightwhite;
# }
# QComboBox QAbstractItemView {
#         border: 1px solid rgb(111, 156, 207);
#         background: white;
#         outline: none;
# }
#  QLineEdit {
#         border-radius: 4px;
#         height: 20px;
#         border: 1px solid rgb(111, 156, 207);
#         background: white;
# }
# QLineEdit:enabled {
#         color: rgb(84, 84, 84);
# }
# QLineEdit:enabled:hover, QLineEdit:enabled:focus {
#         color: rgb(51, 51, 51);
# }
# QLineEdit:!enabled {
#         color: rgb(80, 80, 80);
# }
# """  # QComobox和QLineEdite的样式
#
# StyleSheet_btn = """
# QPushButton{
#     height:30px;
#     background-color: transparent;
#     color: white;
#     border: 2px solid #555555;
#     border-radius: 6px;
# }
# QPushButton:hover {
#     background-color: #5a8db9;
#     border-radius: 6px;
# }
# """  # 登录Button的样式
#
#
# class loginWnd(QWidget):
#     '''登录窗口'''
#
#     def __init__(self, *args, **kwargs):
#         super(loginWnd, self).__init__()
#         self._layout = QVBoxLayout(spacing=0)
#         self._layout.setContentsMargins(0, 0, 0, 0)
#         self.setAutoFillBackground(True)
#         self.setWindowOpacity(0.1)
#         self.setLayout(self._layout)
#         self._setup_ui()
#
#     def _setup_ui(self):
#         self.main_layout = QGridLayout()
#         self.main_layout.setAlignment(Qt.AlignCenter)
#
#         # 左侧文字提示
#         database = QLabel('数据库:')
#         database.setStyleSheet("color:white;")  # 文字样式
#         user_name = QLabel('用户名:')
#         user_name.setStyleSheet("color:white;")
#         passwd = QLabel('密码:')
#         passwd.setStyleSheet("color:white;")
#         IP = QLabel('IP:')
#         IP.setStyleSheet("color:white;")
#         port = QLabel('端口:')
#         port.setStyleSheet("color:white;")
#         self.kuming = QLabel(' ')
#         self.kuming.setStyleSheet("color:white;")
#
#         # 输入框
#         database_box = QLineEdit()
#         user_box = QLineEdit()
#         passwd_box = QLineEdit()
#         ip_box = QLineEdit()
#         port_box = QLineEdit()
#         database_name_box = QLineEdit()
#
#         # 数据库输入框的onchange事件
#         database_box.textChanged[str].connect(self.onChanged)
#
#         # 获取输入的值
#         self.database = database_box
#         self.user = user_box
#         self.passwd = passwd_box
#         self.ip = ip_box
#         self.port = port_box
#         self.database_name = database_name_box
#         # 设置输入框样式 及 设置到默认
#         database_box.setStyleSheet(StyleSheet_2)
#         database_box.setText(database_box_default)
#         user_box.setStyleSheet(StyleSheet_2)
#         user_box.setText(user_box_default)
#         passwd_box.setStyleSheet(StyleSheet_2)
#         passwd_box.setText(passwd_box_default)
#         ip_box.setStyleSheet(StyleSheet_2)
#         ip_box.setInputMask('000.000.000.000')
#         ip_box.setText(ip_box_default)
#         port_box.setStyleSheet(StyleSheet_2)
#         port_box.setInputMask('99999')
#         port_box.setText(port_box_default)
#         database_name_box.setStyleSheet(StyleSheet_2)
#         database_name_box.setText(database_name_box_default)
#         label = QLabel()  # 此处空一行
#         login_btn = QPushButton("生成word文档")
#         login_btn.setStyleSheet(StyleSheet_btn)
#         login_btn.clicked.connect(self.btn1_click)
#
#         # 输入框左边的文字
#         self.main_layout.addWidget(database, 0, 0, 1, 1)
#         self.main_layout.addWidget(user_name, 2, 0, 1, 1)
#         self.main_layout.addWidget(passwd, 4, 0, 1, 1)
#         self.main_layout.addWidget(IP, 6, 0, 1, 1)
#         self.main_layout.addWidget(port, 8, 0, 1, 1)
#         self.main_layout.addWidget(self.kuming, 10, 0, 1, 1)
#
#         # 输入框
#         self.main_layout.addWidget(database_box, 0, 1, 1, 2)
#         self.main_layout.addWidget(label, 1, 0, 1, 3)
#         self.main_layout.addWidget(user_box, 2, 1, 1, 2)
#         self.main_layout.addWidget(label, 3, 0, 1, 3)
#         self.main_layout.addWidget(passwd_box, 4, 1, 1, 2)
#         self.main_layout.addWidget(label, 5, 0, 1, 3)
#         self.main_layout.addWidget(ip_box, 6, 1, 1, 2)
#         self.main_layout.addWidget(label, 7, 0, 1, 3)
#         self.main_layout.addWidget(port_box, 8, 1, 1, 2)
#         self.main_layout.addWidget(label, 9, 0, 1, 3)
#         self.main_layout.addWidget(database_name_box, 10, 1, 1, 2)
#         self.main_layout.addWidget(label, 11, 0, 1, 3)
#         self.main_layout.addWidget(login_btn, 12, 0, 1, 3)
#         self._layout.addLayout(self.main_layout)
#
#     # oracle 用户只有服务名 如:ORCL
#     def onChanged(self, text):
#         if text.replace(' ', '') == 'oracle':
#             self.kuming.setText('服务名:')
#
#         else:
#             self.kuming.setText('库名:')
#
#     # 导出按钮
#     def btn1_click(self):
#         try:
#             database = self.database.displayText().replace(' ', '').lower()
#             user = self.user.displayText().replace(' ', '')
#             passwd = self.passwd.displayText().replace(' ', '')
#             ip = self.ip.displayText().replace(' ', '')
#             port = self.port.displayText().replace(' ', '')
#             database_name = self.database_name.displayText().replace(' ', '')
#             if database and user and passwd and ip and port and database_name:
#                 try:
#                     with open('./export_doc_default.txt', 'w', encoding='utf8')as fw:
#                         fw.writelines(
#                             database + '\n' + user + '\n' + passwd + '\n' + ip + '\n' + port + '\n' + database_name + '\n')
#                 except Exception as e:
#                     print(e)
#                     QMessageBox().information(self, '错误信息', '错误:{}'.format(e), QMessageBox.Yes)
#                 try:
#                     issuccess = saveword(database, user, passwd, ip, port, database_name)
#                     if not issuccess:
#                         raise Exception('请检查连接信息')
#                 except Exception as e:
#                     QMessageBox().information(self, '错误信息', '错误:{}'.format(e), QMessageBox.Yes)
#                 else:
#                     # 弹框  确定 16384  取消 65536
#                     a = QMessageBox().information(self, '关闭提示', '导出成功!是否继续?', QMessageBox.Yes | QMessageBox.No)
#                     if a == 65536:
#                         exit()
#                     if a == 16384:
#                         print('继续操作')
#             else:
#                 # 弹框
#                 QMessageBox().information(self, '警告', '请检查是否全部输入', QMessageBox.Yes)
#         except Exception as Error:
#             QMessageBox().information(self, '错误信息', '错误:{}'.format(Error), QMessageBox.Yes)
#
#
# def main():
#     ''':return:'''
#     app = QApplication(sys.argv)
#     mainWnd = FramelessWindow()
#     mainWnd.setWindowTitle('数据库文档导出')
#     mainWnd.setWindowIcon(QIcon(icoimg))  # ico图标log
#     mainWnd.setWidget(loginWnd(mainWnd))  # 窗口添加进来
#     mainWnd.show()
#     app.exec()
#
#
# def proc():
#
#     main()