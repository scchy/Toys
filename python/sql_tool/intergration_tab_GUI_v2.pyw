# -*- coding: utf-8 -*-
# author: Scc_hy
# reviese date : 2019-09-23

import os
import sys
import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QApplication, QLineEdit, QTextEdit, QLabel, QComboBox, QMessageBox, QDesktopWidget, QTabWidget
from PyQt5.QtGui import QIcon, QFont , QColor, QCursor
import PyQt5.sip  
from PyQt5.QtCore import Qt
from base.local_all_sql import locals_sql 
from base.get_bat import Auto_get_exce_bat 
from base.get_sql_2_csv import Selection, Write_select


class TabDemo(QTabWidget):
    def __init__(self,parent=None):
        super(TabDemo, self).__init__(parent)
        self.conn_info = {
                "host": "xxxxx",
                "port": "xxx",
                "user": "xxx",
                "password": "xxxxx",
                "database": "xxx",
                "unicode_error": "replace"
                }
        #创建3个选项卡小控件窗口
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()

        #将三个选项卡添加到顶层窗口中
        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, "Tab 3")
        self.setTabText(0,'生成11个地市的SQL')
        self.setTabText(1,'快速生成bat')
        self.setTabText(2,'导出数据')
        str = "QTabBar::tab:selected{color:#C00000;background-color:rbg(255,200,255);margin-left: 1.5;margin-right: 0; } "\
        + "QTabBar::tab{width: 160px; height:20px; font:12px;}"
        self.setStyleSheet(str)


        #每个选项卡自定义的内容
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.center()
        self.set_gui()

    def tab1UI(self):

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
        _n = "\n" * 8
        self.out_sqlEdit.setPlainText('生成选择地市的sql{}Version: 1.0.0.2019.08\nContact: sunchengchao@bonc.com.cn'.format(_n))
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
        

        # grid.addWidget(msg_lbl, 12, 1, 1, 1)
        self.tab1.setLayout(grid)
        
        self.set_decoration(self.need_sqlEdit)
        self.set_decoration(self.out_sqlEdit)


    def init_local_list(self):
        """
        下拉框获取数据
        """
        items_list = ['A-xx', 'B-xx', 'C-xx', 'D-xx', 'E-xx', 'F-xx', 'G-xx'
                        , 'H-xx', 'I-xx', 'J-xx', 'K-xx', '$LocalCode-local变量' ,'ALL_LOCAL-全部地市']
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


    def tab2UI(self):
        self.qbtn_bat = QPushButton('执行', self)
        self.qbtn_bat.clicked.connect(self.get_concent_bat)
        self.qbtn_bat.clicked.connect(self.get_bat)

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

        self.out_batEdit = QTextEdit()
        _n = "\n" * 19
        self.out_batEdit.setPlainText('perl文件执行bat{}Version: 1.1.0.2019.08\nContact: sunchengchao@bonc.com.cn'.format(_n))

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
        grid.addWidget(self.out_batEdit, 3, 1, 2, 3)

        grid.addWidget(self.qbtn_bat, 4, 0)     


        self.set_decoration(self.start_Edit)
        self.set_decoration(self.end_Edit)
        self.set_decoration(self.perl_Edit)
        self.set_gui()

        #设置标题与布局
        self.tab2.setLayout(grid)

    def get_concent_bat(self):
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
        if self.start_dt == '' and self.end_dt == '' :
            perl_msg = '请输入需要生成bat的月份，如 201908'
        else:
            get_bat = Auto_get_exce_bat(self.start_dt, self.end_dt, self.perl_)
            perl_msg = get_bat.get_exce_bat()
        self.out_batEdit.clear() 
        self.out_batEdit.setPlainText(perl_msg)




    def tab3UI(self):
        self.qbtn3 = QPushButton('导出', self)
        # 按钮功能
        self.qbtn3.clicked.connect(self.write_out_msg) #  需要导出的sql

        zh_in = QLabel('输入账号')
        self.zh_inEdit = QLineEdit()
        self.zh_inEdit.setPlaceholderText('默认 xxxxx')

        mm_in = QLabel('输入密码')
        self.mm_inEdit = QLineEdit()
        self.mm_inEdit.setPlaceholderText('默认 xxxxx')

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

        self.tab3.setLayout(grid)
        
        self.set_decoration(self.need_sql3Edit)
        self.set_decoration(self.out_msgEdit)


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
            rows, columns , msg_vtc = write_select.wirte_2_file(delimiter = self.delimiter_f)
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
    app=QApplication(sys.argv)
    demo=TabDemo()
    demo.show()
    sys.exit(app.exec_())
