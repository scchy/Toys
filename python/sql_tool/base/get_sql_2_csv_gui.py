# python 3.6
# Author:              Scc_hy
# Create date:         2019-08-13
# Function:            生成pyqt界面
# Concats:             hyscc1994@foxmail.com   
# Tips



## 调用包
from ....vertica2csv import Selection, Write_select
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QApplication, QLineEdit, QTextEdit, QLabel, QComboBox, QMessageBox, QDesktopWidget, QTabWidget
from PyQt5.QtGui import QIcon, QFont 
import PyQt5.sip  
from PyQt5.QtCore import Qt
import os

class get_sql_Example(QWidget):
      def __init__(self):
            super().__init__()
            self.conn_info = {
                  "host": "xxx.xx.xxx.xx",
                  "port": "xxx",
                  "user": "xxx",
                  "password": "xxxx",
                  "database": "xxx",
                  "unicode_error": "replace"
                  }
            self.initUI()
            
      
      def initUI(self):
            self.qbtn3 = QPushButton('导出', self)
            # 按钮功能
            self.qbtn3.clicked.connect(self.write_out_msg) #  需要导出的sql



            zh_in = QLabel('输入账号')
            self.zh_inEdit = QLineEdit()
            self.zh_inEdit.setPlaceholderText('默认 lzwul')

            mm_in = QLabel('输入密码')
            self.mm_inEdit = QLineEdit()
            self.mm_inEdit.setPlaceholderText('默认 wul.vtc.142')

            delimiter_in = QLabel('文件分隔符')
            self.delimiter_inEdit = QLineEdit()
            self.delimiter_inEdit.setPlaceholderText('默认 ,')
            
            out_in = QLabel('输出文件路径')
            self.out_inEdit = QLineEdit()
            self.out_inEdit.setPlaceholderText("如 C:\\Users\\dell\\Desktop\\out.csv (默认导出exe所在目录下out.csv中)")

            need_sql3 = QLabel('输入SQL')
            self.need_sql3Edit = QTextEdit()
            self.need_sql3Edit.setPlainText('输入sql')

            out_msg = QLabel('导出情况')
            self.out_msgEdit = QTextEdit()
            _n = "\n" * 9
            self.out_msgEdit.setPlainText('输入到csv的导出情况{}Version: 1.0.0.2019.09\nContact: sunchengchao@bonc.com.cn'.format(_n))

            # 窗口布局 
            grid = QGridLayout()
            grid.setSpacing(16)
            grid = QGridLayout()
            grid.setSpacing(16)
            grid.addWidget(zh_in, 1, 0)
            grid.addWidget(self.zh_inEdit, 1, 1, 1, 1)
            grid.addWidget(mm_in, 1, 2)
            grid.addWidget(self.mm_inEdit, 1, 3, 1, 1)
            grid.addWidget(delimiter_in, 1, 4)
            grid.addWidget(self.delimiter_inEdit, 1, 5, 1, 1)
            
            grid.addWidget(out_in, 2, 0)
            grid.addWidget(self.out_inEdit, 2, 1, 1, 5)

            grid.addWidget(need_sql3, 3, 0)
            need_sql3.setAlignment(Qt.AlignTop)
            grid.addWidget(self.need_sql3Edit, 3, 1, 2, 5)

            grid.addWidget(out_msg, 5, 0)
            out_msg.setAlignment(Qt.AlignTop)
            grid.addWidget(self.out_msgEdit, 5, 1, 2, 5)

            grid.addWidget(self.qbtn3, 6, 0)

            self.setLayout(grid)
            
            self.set_decoration(self.need_sql3Edit)
            self.set_decoration(self.out_msgEdit)
            self.set_gui()

      def get_out_sql(self):
            """
            文本框提取sql事件
            """
            self.out_sql = self.need_sql3Edit.toPlainText()

      def get_concent_info(self):
            """
            获取账号密码 及输出文件位置
            """
            zh_in_detail = self.zh_inEdit.text()
            mm_in_detail = self.mm_inEdit.text()
            out_in_detail = self.out_inEdit.text() 
            delimiter = self.delimiter_inEdit.text() 
            self.conn_info['user'] = zh_in_detail if  zh_in_detail != '' else self.conn_info['user']
            self.conn_info['password'] = mm_in_detail if  mm_in_detail != '' else self.conn_info['password']
            self.out_file_path = out_in_detail if  out_in_detail != '' else os.path.join(os.curdir, 'out.csv')
            self.delimiter_f = delimiter  if  delimiter != '' else ','


      def write_out_msg(self):
            self.get_concent_info() #  获取账号密码 以及输出文件路径
            self.get_out_sql() # 获取需要导出的sql
            self.out_msgEdit.clear()
            msg = "已连接数据库...\n账号:{}\n...\n".format(self.conn_info['user'])
            self.out_msgEdit.setPlainText(msg)
            try:
                  vtc_select = Selection(self.conn_info).__enter__()
                  slt_con = vtc_select.select(self.out_sql)
                  # 写入文件 
                  write_select = Write_select(self.out_file_path, slt_con)
                  rows, columns , msg_vtc = write_select.wirte_2_file(self.delimiter_f)
                  msg += msg_vtc
                  vtc_select.__exit__()
                  self.out_msgEdit.clear()
                  self.out_msgEdit.setPlainText(msg)

            except:
                  msg += '导出失败, 请重新尝试'
                  self.out_msgEdit.clear()
                  self.out_msgEdit.setPlainText(msg)

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
