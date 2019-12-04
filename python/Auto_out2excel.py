# -*- coding:utf-8 -*- 
# python 3.6
# Author:              Scc_hy
# Create date:         2019-10-08
# Function:            将数据导出到对应excel
# finish date           2019-10-09

## 调用包
import time 
import datetime
import os, sys, io
import re
import argparse
import vertica_python
import logging
import pandas as pd
from datetime import datetime
import shutil
from openpyxl import load_workbook
from progressing import My_Progress
from vertica2csv import Selection, conn_info
 


def parse_args():
      """
      调用程序
      """
      parser = argparse.ArgumentParser(description = "Call Perl Script")
      parser.add_argument('-path','--root_path', required = True, help = 'The perls file root path')
      args = parser.parse_args()
      return args



class Vtc_2_excel(object):
      """
      可直接指定need ，然后调用  main_sub 导出数据  
      也可以直接用 loop_vtc2excel 全部导出
      """
      def __init__(self, month, need = '', base_root = r'E:\Month_call_script'): 
            self.set_n()
            self.month = month
            self.sql_dict, self.fil_dict, self.excel_col_dict = self.fil_sql_dict()
            self.need_list = ['cust', 'sr', 'hb', 'srbig', 'srkm',  'srxf', 'srfj']
            self.need = self.need_list[self.n] if need == '' else need
            self.p = My_Progress(self.need_list, width = 25)
            self.base_root = base_root
            # 创建文件
            self.create_file()

      def set_n(self):
            self.n = 0

      def add_n(self):
            self.n += 1

      def create_file(self):
            path_need = os.path.join(self.base_root , self.fil_dict['dir_name_new'])
            if not os.path.exists(path_need):
                  os.makedirs(path_need)

      def month_add_sub(self, _dt, method = 'add'):
            """
            月份12进制 减法  
            param: _dt int 如：201908  
            param: method  计算方法 加 减
                  ['add', 'sub'] 
            """
            _dt = int(_dt)
            if method == 'sub':
                  out_dt = _dt - 1 if _dt % 100 != 1 else (_dt // 100 - 1) * 100 + 12  
            else: out_dt = _dt + 1  if _dt % 100 != 12 else (_dt // 100 + 1) * 100 +1
            return out_dt

      def fil_sql_dict(self):
            """
            对应月所需要导出的sql：  sql_dict  
            对应excel的文件名：  fil_dict  
            对应excel的表头：  excel_col_dict  
            """
            month_nd = self.month % 10000
            month_cur = datetime.now().strftime("%m%d")
            sql_dict = {
                  # 客户视图 
                  'cust_star' : "SELECT * FROM schema.start_tmp_new WHERE BIL_MONTH = '{}';".format(self.month),
                  'cust_channel' : "SELECT * FROM schema.qd_st_tmp_new WHERE BIL_MONTH = '{}';".format(self.month),
                  'cust_all' : "SELECT * FROM schema.czl_tmp_new WHERE BIL_MONTH = '{}';".format(self.month),
                  # 收入大数
                  'srbig_sql' : "SELECT * FROM schema.all_sr WHERE BIL_MONTH = '{}';".format(self.month),
                  # 收入视图——科目细化
                  'srkm_sql' : "SELECT * FROM schema.zysr_km_tj_amt WHERE BIL_MONTH = '{}';".format(self.month),  
                  # 收入视图 
                  'sr_sql' : "SELECT * FROM  schema.zysr_fx_{};".format(self.month),  
                  'hb_sql' : "SELECT * FROM schema.E_I_HUABEI  WHERE BIL_MONTH = '{}'  AND LATN_NAME IN ('04-嘉兴', '07-金华'); ".format(self.month), 
                  # 收入——到分局数据
                  'srxf_sql' : "SELECT * FROM schema.vl4_sr_tmp_new WHERE BIL_MONTH = '{}';".format(self.month), 
                  # 收入分解
                  'srfj_sql' : "SELECT * FROM schema.tmp_out11 WHERE BIL_MONTH = '{}';".format(self.month),
            }
            fil_dict = {
                  'dir_name_old': "{}视图数据&迁转".format(self.month_add_sub(self.month, method = 'sub')),
                  'dir_name_new': "{}视图数据&迁转".format(self.month),
                  # 客户视图 
                  'cust_fil' : '1901_{}客户视图_量&收_{}.xlsx'.format( month_nd, month_cur),
                  # 收入大数 
                  'srbig_fil' : '{}{}同期收入大数v2_{}.xlsx'.format(month_nd - 100, month_nd, month_cur),
                  # 收入视图——科目细化  
                  'srkm_fil' : '{}收入视图_科目细化_{}.xlsx'.format(month_nd, month_cur),

                  # 收入视图
                  'sr_fil' : '{}收入视图_{}.xlsx'.format(month_nd, month_cur),
                  'hb_fil' : '201808_{}嘉兴金华花呗还原v5_{}.xlsx'.format(month_nd, month_cur),
                  # 收入——到分局数据 
                  'srxf_fil' : '1812_{}分县分四大主量收入V3_{}.xlsx'.format(month_nd, month_cur),
                  # 收入分解
                  'srfj_fil' : '1801_{}收入分解_{}.xlsx'.format(month_nd, month_cur)
            }
            excel_col_dict = {
                  'cust_channel_columns'  : ['月份', '地市', '存增量', '发展渠道', '计费客户数', '在网客户数', '税后收入'], 
                  'cust_star_columns'  : ['月份', '地市', '存增量', '客户星级', '计费客户数', '在网客户数', '税后收入'], 
                  'cust_all_columns'  : ['月份', '地市', '存增量', '计费客户数'],
            }
            return  sql_dict, fil_dict, excel_col_dict


      def fil_name_and_sql(self):
            """
            返回新旧文件名 和 SQL
            param : srting  
                  ['cust', 'srbig', 'srkm', 'sr', 'hb', 'srxf', 'srfj]
            """
            need_old_dict = {
                  'cust' : '客户视图',
                  'srbig' : '收入大数',
                  'srkm' : '收入视图_科目细化',
                  'sr' : '收入视图_',
                  'hb' : '花呗还原',
                  'srxf' : '分县分',
                  'srfj' : '收入分解'
            }
            new_name = '{}/{}/{}'.format(self.base_root , self.fil_dict['dir_name_new'], self.fil_dict['{}_fil'.format(self.need)])
            old_name = '{}/{}/{}'.format(self.base_root , self.fil_dict['dir_name_old']
                                    , [i for i in os.listdir(os.path.join(self.base_root 
                                                            , self.fil_dict['dir_name_old'])) if need_old_dict[self.need] in i][0])
            sql = [[key,value] for key, value in self.sql_dict.items() if  'cust' in key] \
                  if self.need == 'cust' else self.sql_dict['{}_sql'.format(self.need)]
            return old_name, new_name, sql



      def del_dataframe(self, _dt):
            """
            部分文件需要增加计算字段
            """
            if self.need == 'hb':
                  _dt.iloc[:, -1] = _dt.iloc[:, -3] - _dt.iloc[:, -2]
            elif self.need == 'srxf':
                  _dt.iloc[:, 2] = _dt.iloc[:, 2].fillna('(null)')
                  _dt.iloc[:, -1] = _dt.iloc[:, 1].map(lambda x: x[3:])  \
                                    +_dt.iloc[:, 2].map(lambda x: x.replace('本级', '')\
                                                      .replace('区分公司', "分公司")\
                                                      .replace('市分公司', "分公司")\
                                                      .replace('县分公司',  "分公司")
                                                      ) 
            else: 
                  _dt = _dt
            return _dt
            

      def get_old_dt(self, filename, sheet_name = 0 , out_need = 'data'):
            """
            读取旧文件数据 或 仅返回字段名称
            """
            _dt = pd.read_excel(filename, sheet_name = sheet_name, header = 0)
            _dt_col = list(_dt.columns)
            return _dt if out_need == 'data' else _dt_col


      def connect_dt(self, filename, data_to_write, old_need, write_type = 'data', sheet_name = 0):
            """
            合并数据写入对应sheet
            当 write_type = 'data' 的时候写入合并数据   
            param: filename 文件名 需要输出的文件  
            param: sheet_name sheet名称  
            param: data_to_write vertica导出的pd.DataFrame数据 （无表头）  
            param: old_need pd.DataFrame / list   从以前数据中所需要的数据  
            param: write_type string   
                  'data' / 'list'  与 old_need相对应  
            """
            if write_type == 'data':
                  if self.need in ['hb', 'srxf']:
                        data_to_write['a'] = 1
                  data_to_write.columns = list(old_need.columns)
                  data_to_write = pd.concat([old_need, data_to_write], axis = 0)
            else: 
                  data_to_write.columns = old_need
            data_to_write = self.del_dataframe(data_to_write)

            # 判断是否存在文件并创建
            if not os.path.exists(filename):
                  dt_tmp = pd.DataFrame()
                  dt_tmp.to_excel(filename)

            excelWriter = pd.ExcelWriter(filename, engine = 'openpyxl')
            book = load_workbook(filename)
            excelWriter.book = book
            data_to_write.to_excel(excelWriter, sheet_name = sheet_name, header = True, index = False)
            excelWriter.save() 
            excelWriter.close()


      def main_sub(self):
            """
            提取一个需要的数据
            """
            sheet_name_dict = {
                  'cust_star' : '维系渠道',
                  'cust_channel': '发展渠道',
                  'cust_all': '总',
                  'srbig': '收入大数',
                  'srkm': '收入视图_科目细化',
                  'sr': '收入视图',
                  'hb': '花呗',
                  'srxf': '分县分四大主量',
                  'srfj' : '收入分解'
                  }
            write_type = 'data' if self.need in ['cust','hb' ,'srxf', 'srfj'] else 'columns'
            out_need = write_type
            old_name, new_name, sql = self.fil_name_and_sql()
            vtc_select = Selection(conn_info)
            vtc_select.__enter__()
            if self.need == 'cust':
                  for sql_i in sql:
                        old_need = self.get_old_dt(old_name, sheet_name = sheet_name_dict[sql_i[0]] , out_need = out_need)
                        print('>>>> 已经读取以前数据 .....')

                        slt_con = vtc_select.select(sql_i[1])
                        new_month_cust = pd.DataFrame(slt_con)
                        print('>>>> 已经读取需要导出数 .....')

                        self.connect_dt(new_name, new_month_cust, old_need, write_type = write_type, sheet_name = sheet_name_dict[sql_i[0]])
                        print('>>>> 已经将 [ {} ] 需要数据导到指定位置 <<<<< '.format(sheet_name_dict[sql_i[0]]))  
            else: 
                  old_need = self.get_old_dt(old_name, sheet_name = sheet_name_dict[self.need] , out_need = out_need)
                  print('>>>> 已经读取以前数据 .....')

                  slt_con = vtc_select.select(sql)
                  new_month_cust = pd.DataFrame(slt_con)
                  print('>>>> 已经读取需要导出数 .....')

                  self.connect_dt(new_name, new_month_cust, old_need, write_type = write_type,  sheet_name = sheet_name_dict[self.need])
                  print('>>>> 已经将 [ {} ] 需要数据导到指定位置 <<<<< '.format(sheet_name_dict[self.need]))           
            vtc_select.__exit__()

      def time_get(self):
            start_time = datetime.now()
            return start_time, start_time.strftime('%H:%M:%S')

      def loop_vtc2excel(self):
            start_time, start_print = self.time_get()
            print('{} 开始运行：..........'.format(start_print))
            for v in range(7):
                  msg = self.p.progress()
                  print('目前输出：{}， 进度为:{}'.format(self.need, msg))
                  self.main_sub()
                  if self.n < len(self.need_list) - 1:
                        self.add_n()
                        self.need = self.need_list[self.n]

            end_time, end_print = self.time_get()
            delt = (end_time - start_time).seconds
            delt_print = '{}分{}秒'.format(delt // 60 , delt % 60)
            print('{} 结束导出，耗时：{}'.format(end_print, delt_print))


if __name__ == '__main__':
      arg = parse_args()
      root_path = arg.root_path
      vtc2excel = Vtc_2_excel(201909, base_root = root_path)
      vtc2excel.loop_vtc2excel()

# os.getcwd()
# os.chdir(base_root)
# dir(os)
# ## copy rename
# shutil.copyfile(cust_fil_path_old, cust_fil_path)
