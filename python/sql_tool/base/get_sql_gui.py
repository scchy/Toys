# python 3.6
# Author:              Scc_hy
# Create date:         2019-08-13
# Function:            生成pyqt界面
# Concats:             hyscc1994@foxmail.com   
# Tips

__doc__ = """
            快速生成11个地市的SQL 的 pyqt5界面
          """

## 调用包
from local_all_sql import locals_sql 
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QApplication, QLineEdit, QTextEdit, QLabel, QComboBox, QMessageBox, QDesktopWidget, QTabWidget
from PyQt5.QtGui import QIcon, QFont 
import PyQt5.sip  


class get_sql_Example(QWidget):
      def __init__(self):
            super().__init__()
            self.initUI()
            
      
      def initUI(self):
            self.qbtn = QPushButton('执行', self)
            self.qbtn.setToolTip('运行生成当前选择地市<b>SQL</b>')
            local_shoose = QLabel('选择地市')
            self.loacl_combox = QComboBox(self, minimumWidth=200)
            self.init_local_list()
            self.get_local()
            self.loacl_combox.currentIndexChanged.connect(self.get_local)


            need_sql = QLabel('输入SQL')
            out_sql = QLabel('输出SQL')
            # msg_lbl = QLabel('__version__:1.0.0.2019.08\tConnect: sunchengchao@bonc.com.cn')
            
            self.need_sqlEdit = QTextEdit()
            self.need_sqlEdit.setPlainText('输入sql')
            self.out_sqlEdit = QTextEdit()
            self.out_sqlEdit.setPlainText('生成选择地市的sql\n\n\n\n\n\n\nVersion: 1.0.0.2019.08\nContact: sunchengchao@bonc.com.cn')

            # 窗口布局 
            grid = QGridLayout()
            grid.setSpacing(16)

            grid.addWidget(need_sql, 1, 0)
            grid.addWidget(self.need_sqlEdit, 1, 1, 2, 1)

            grid.addWidget(local_shoose, 3, 0)
            grid.addWidget(self.loacl_combox, 3, 1, 1, 1)
            grid.addWidget(self.qbtn, 6, 0)

            grid.addWidget(out_sql, 4, 0)
            
            # reviewEdit控件跨度5行
            grid.addWidget(self.out_sqlEdit, 4, 1, 5, 1)
            # grid.addWidget(msg_lbl, 12, 1, 1, 1)
            

            self.setLayout(grid)
            
            self.set_decoration(self.need_sqlEdit)
            self.set_decoration(self.out_sqlEdit)
            self.set_gui()


      def init_local_list(self):
            """
            下拉框获取数据
            """
            items_list = ['A-XX', 'B-XX', 'C-XX', 'D-XX', 'E-XX', 'F-XX', 'G-XX'
                         , 'H-XX', 'I-XX', 'J-XX', 'K-XX', '$LocalCode-local变量' ,'ALL_LOCAL-全部地市']
            for i in items_list:
                  self.loacl_combox.addItem(i)
            self.loacl_combox.setCurrentText(items_list[-1])
            
      def get_local(self):
            """
            下拉改变后执行 
            """
            self.local = self.loacl_combox.currentText()
            self.local = self.local.split('-')[0]
            self.qbtn.clicked.connect(self.get_concent)
            if self.local == 'ALL_LOCAL':
                  self.qbtn.clicked.connect(self.get_all_sql)
            else:
                  self.qbtn.clicked.connect(self.get_loal_sql)         
            self.qbtn.resize(self.qbtn.sizeHint())

      def get_concent(self):
            """
            文本框提取sql事件
            """
            self.sql = self.need_sqlEdit.toPlainText()

      def get_all_sql(self):
            """
            文本框输出sql事件——全省
            """
            gt_sql = locals_sql(self.sql)
            sql_out = gt_sql.get_union_sql()
            self.out_sqlEdit.clear() 
            self.out_sqlEdit.setPlainText(sql_out)

      def get_loal_sql(self):
            """
            文本框输出sql事件——一个地市
            """
            gt_sql = locals_sql(self.sql)
            sql_out = gt_sql.get_loacl_sql(self.local)
            self.out_sqlEdit.clear() 
            self.out_sqlEdit.setPlainText(sql_out)

      def set_gui(self):
            """
            设置窗口大小，窗口名称
            以及窗口的图标
            """
            self.setGeometry(300, 300, 650, 400)
            self.center()
            self.setWindowTitle('BONC SQL_TOOL')    
            self.setWindowIcon(QIcon('./Qi.ico'))
            self.show()

      def set_decoration(self, the_obj):
            """
            其他修饰 字体等
            """
            font = QFont('Console', 10, QFont.Light)
            the_obj.setFont(font)

      def closeEvent(self, event):
            reply = QMessageBox.question(self, 'Exit',
                  "Are you sure to quit?", QMessageBox.Yes | 
                  QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                  event.accept()
            else:
                  event.ignore()        

      def center(self):
            
            #获得窗口
            qr = self.frameGeometry()
            #获得屏幕中心点
            cp = QDesktopWidget().availableGeometry().center()
            #显示到屏幕中心
            qr.moveCenter(cp)
            self.move(qr.topLeft())
            

if __name__ == '__main__':
      # 每个PyQt5应用必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数 
      app = QApplication(sys.argv)
      ex = get_sql_Example()
      sys.exit(app.exec_())
