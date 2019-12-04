# python 3.6
# Author:              Scc_hy
# Create date:         2019-06-24
# Function:            快速生成执行bat
# Concats:             hyscc1994@foxmail.com   
# Tips

__doc__ = """
            可以生成一个月也可以生成连续月的命令
            """


## 调用包
import time 
import datetime
import os 
import re



class Auto_get_exce_bat():
      def __init__(self, start_dt, end_dt, exc_perl ):
            try:
                  self.exc_perl = exc_perl.split('.')[0]
            except:
                  self.exc_perl = exc_perl
            self.Local_id = [chr(i) for i in range(ord('A'), ord('K') + 1)]
            self.start_dt = start_dt
            self.end_dt = end_dt
            self.swap()

      def swap(self):
            if str(self.start_dt) == '' or str(self.end_dt) == '': # 当只输入一个月份的时候
                  self.start_dt = self.end_dt if str(self.end_dt) != '' else self.start_dt
                  self.end_dt = self.start_dt if str(self.start_dt) != '' else self.end_dt
            start_dt = int(self.start_dt)
            end_dt = int(self.end_dt)
            if  start_dt > end_dt:
                  change = end_dt
                  self.end_dt = start_dt
                  self.start_dt = change

      def month_add_sub(self, _dt):
            """
            月份12进制 加法
            """
            _dt = int(_dt)
            return  _dt + 1  if _dt % 100 != 12 else (_dt // 100 + 1) * 100 +1

      def write_month_dt(self): 
            """
            将一个月执行的数据写入文件
            """
            out_msg = ''
            exc_m = self.month_add_sub(self.start_dt)
            for local in self.Local_id:
                  out_msg += "perl {}.pl {}_{}01.dir >> {}_{}.log\n".format(self.exc_perl, local, exc_m, self.exc_perl, self.start_dt)
            return out_msg

      def get_exce_bat(self):
            out_msg = ''
            while (int(self.start_dt) < int(self.end_dt) + 1):
                  out_msg += self.write_month_dt() + "\n"
                  self.start_dt = self.month_add_sub(self.start_dt)
            return out_msg



if __name__ == '__main__':
      print('start')
      get_bat = Auto_get_exce_bat(201812, 201901, 'exc_perl' )
      print('get bat....')
      out_msg = get_bat.get_exce_bat()
      print(out_msg)
