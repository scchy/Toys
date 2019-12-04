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
from get_bat import Auto_get_exce_bat 
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QApplication, QLineEdit, QTextEdit, QLabel, QComboBox, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont 
from PyQt5.QtCore import Qt
import PyQt5.sip  


class get_bat_Example(QWidget):
      def __init__(self):
            super().__init__()
            self.initUI()
            
      
      def initUI(self):
            self.qbtn = QPushButton('执行', self)
            self.qbtn.clicked.connect(self.get_concent)
            self.qbtn.clicked.connect(self.get_bat)

            start_ql = QLabel('输入开始日期')
            end_ql = QLabel('输入结束日期')
            perl_ql = QLabel('输入perl文件名')
            out_ql = QLabel('输出')
            out_ql.setAlignment(Qt.AlignTop)
            
            self.start_Edit = QLineEdit()
            self.start_Edit.setPlaceholderText('如 201908')
            self.end_Edit = QLineEdit()
            self.end_Edit.setPlaceholderText('如 201908')
            self.perl_Edit = QLineEdit()
            self.perl_Edit.setPlaceholderText('如 example.pl 或者 example') 

            self.out_sqlEdit = QTextEdit()
            _n = "\n" * 19
            self.out_sqlEdit.setPlainText('perl文件执行bat{}Version: 1.0.0.2019.08\nContact: sunchengchao@bonc.com.cn'.format(_n))

            # 窗口布局 
            grid = QGridLayout()
            grid.setSpacing(16)

            grid.addWidget(start_ql, 1, 0)
            grid.addWidget(self.start_Edit, 1, 1)
            grid.addWidget(end_ql, 1, 2)
            grid.addWidget(self.end_Edit, 1, 3)
            grid.addWidget(perl_ql, 2, 0)
            grid.addWidget(self.perl_Edit, 2, 1, 1, 3)

            grid.addWidget(out_ql, 3, 0)   
            grid.addWidget(self.out_sqlEdit, 3, 1, 2, 3)

            grid.addWidget(self.qbtn, 4, 0)     

            self.setLayout(grid)   
            self.set_decoration(self.start_Edit)
            self.set_decoration(self.end_Edit)
            self.set_decoration(self.perl_Edit)
            self.set_gui()


      def get_concent(self):
            """
            文本框提取sql事件
            """
            self.start_dt = self.start_Edit.text()
            self.end_dt = self.end_Edit.text()
            self.perl_ = self.perl_Edit.text()


      def get_bat(self):
            """
            文本框输出sql事件——全省
            """
            get_bat = Auto_get_exce_bat(self.start_dt, self.end_dt, self.perl_)
            perl_msg = get_bat.get_exce_bat()
            self.out_sqlEdit.clear() 
            self.out_sqlEdit.setPlainText(perl_msg)


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
      ex = get_bat_Example()
      sys.exit(app.exec_())



# select distinct latn_id from ZJBIC.OFR_MAIN_ASSET_MON_a 
