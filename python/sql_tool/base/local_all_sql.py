# python 3.6
# Author:              Scc_hy
# Create date:         2019-06-24
# Function:            快速生成11个地市的SQL
# Concats:             hyscc1994@foxmail.com   
# Tips

__doc__ = """
            核心部件
            快速生成11个地市的SQL
          """

# """
# 修饰符	描述
# re.I	使匹配对大小写不敏感
# re.L	做本地化识别（locale-aware）匹配
# re.M	多行匹配，影响 ^ 和 $
# re.S	使 . 匹配包括换行在内的所有字符
# re.U	根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.
# re.X	该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解
# """

## 调用包
import time 
from  datetime import datetime
import os 
import re
import argparse




class  locals_sql():
      def __init__(self, on_local_sql, fil_path = None):
            self.all_local = [chr(i) for i in range(ord('A'), ord('K') + 1)]
            self.on_local_sql = on_local_sql
            self.table_list, self.search_part = self.get_table_list()
            self.sql = self.get_union_sql()
            self.fil_path = os.path.join(os.curdir, 'sql_{}.sql'.format(datetime.now().strftime('%Y%m%d'))) if fil_path == None else fil_path

      def get_table_list(self):
            """
            多行匹配找出 带有 a-k 的表
            并生成用于全局匹配的part
            """
            table_list = re.findall(r'\b\w+\.\w+_[A-Ka-k]\b', self.on_local_sql, re.M)
            search_part = '(.*)'
            for i in table_list:
                  search_part += '{}(.*)'.format(i)
            return table_list, search_part

      def get_union_sql(self):
            """
            全局搜索分成 x 块，并生成11个地市的sql
            """
            a = re.search(r'{}'.format(self.search_part), self.on_local_sql, re.S)
            n = len(self.table_list)
            sql = ''
            for local in self.all_local:
                  for i in range(n):
                        sql += '{}{}{}'.format(a.group(i+1), self.table_list[i][:-1], local)
                  sql +=  '{}{}'.format(a.group(n + 1), '\nUNION ALL\n') if local != 'K' else '{}{}'.format(a.group(n + 1), ';') 
            return sql

      def get_loacl_sql(self, local):
            """
            生成指定地市的sql
            """
            a = re.search(r'{}'.format(self.search_part), self.on_local_sql, re.S)
            n = len(self.table_list)
            sql = ''
            for i in range(n):
                  sql += '{}{}{}'.format(a.group(i+1), self.table_list[i][:-1], local)
            sql +=  '{}{}'.format(a.group(n + 1), ';') 
            return sql


      def write_sql(self):
            f = open(self.fil_path, 'a+', encoding = 'utf8')
            f.write(self.sql)
            f.close()
   
