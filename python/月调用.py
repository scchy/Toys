# -*- coding:utf-8 -*- 
# python 3.6
# Author:              Scc_hy
# Create date:         2019-08-08
# Function:            调用perl文件

## 调用包
import time 
import datetime
import os 
import re
import argparse
from progressing import My_Progress


def parse_args():
      """
      调用程序
      """
      parser = argparse.ArgumentParser(description = "Call Perl Script")
      parser.add_argument('-path','--root_path', required = True, help = 'The perls file root path')
      args = parser.parse_args()
      return args


class Month_call_script():
      """
      调用 root_path 目录下所有perl脚本
      """
      def __init__(self, base_root = "E:/Month_call_script"):
            self.time_now = datetime.datetime.now()
            self.year_month_day = self.time_now.strftime("%Y%m%d")
            self.year_month = self.time_now.strftime("%Y%m")

            ## 地区编码
            self.Local_ids = [chr(i) for i in range(ord("A"),ord("K")+1)]
            ## 获取文件夹下的文件 
            self.base_root = base_root
            self.perl_files = [i for i in os.listdir(self.base_root) if i[-2:] == 'pl']
            self.exec_array = self.get_exec_array()

      ## 生成windows执行语句
      def get_exec_array(self):
            # 生成配置命令  
            exec_array = []
            for i_pl in self.perl_files:
                  i_pl_abs = os.path.join(self.base_root, i_pl)
                  for  local in self.Local_ids:
                        log_i = os.path.join(self.base_root, 'log\{}log\{}_{}{}.log'.format(self.year_month, i_pl[:-3], local, self.year_month))
                        exc_i = "perl {} {}_{}.dir > {}".format(i_pl_abs, local, self.year_month_day, log_i)
                        exec_array.append(exc_i)
            return exec_array
 
      # 创建子程序
      def check_if_finished(self, need_checked_log_file):
            """
            读取文件然后正则匹配 rc=0   
            # test:  check_if_finished('E:/Month_call_script\\log\\201908log\\BASE_0_ZL_EK_HB_K201908.log')
            """
            f = open(need_checked_log_file, 'r', encoding = 'utf-8') 
            f_content = f.read()
            check = 0 if re.search('rc=0', f_content) == None  else 1
            f.close()
            massege = "==[ Finished ]== \n" if check == 1 else "XXXX{ need exec again }XXXX"
            log_file_message = re.search(r"(\w+\.log)", need_checked_log_file)
            print("Check The log file:  {}\n{}".format(log_file_message.group(1), massege))
            return check


      def exec_sub(self, exec_cmd, log_file):
            print("=====================================================================")
            print("NOW EXEC: {}  \n".format(exec_cmd))
            os.system(exec_cmd);
            check = self.check_if_finished(log_file)
            print("=====================================================================\n")
            return check


      def check_log_file_exists(self, check_log):
            """
            检测是否存在log文件夹不存在就创建
            E:/Month_call_script\\0_Base_data_pl\\log\\201908log\\BASE_0_ZL_EK_HB_K201908.log
            """
            exists_bool = os.path.exists(check_log)
            check_log_re = re.search(r'(.*log).*\.log$', check_log) 
            # 判断文件夹是否存在
            mk_path = check_log_re.group(1)
            mk_path_bool = os.path.exists(mk_path)
            if mk_path_bool == False:
                  os.makedirs(mk_path)
            return exists_bool


      def exc_perls(self):
            p = My_Progress(self.exec_array, width=45)
            for exec_i in self.exec_array:
                  re_exce_i = re.search(r'(\w+)\.pl \w_(\d{6})\d{2}\.dir > (.*\.log)$', exec_i) 
                  year_month_i = re_exce_i.group(2)
                  Fuction = re_exce_i.group(1)
                  check_log = re_exce_i.group(3)
                  print(">>>>>>>>>> Start:  {} --- {} <<<<<<<<<<<<<<".format(Fuction, year_month_i))
                  print("=============================  Check if Finished  =================")
                  loop = 0
                  if self.check_log_file_exists(check_log):
                        print("<< THE FILE HAS EXISTS >>\n")
                        check = self.check_if_finished(check_log) 
                        if check == 1:
                              print("<< The month and local has Finished >>\n")
                              next
                        else:
                              print("<< The month and local NOT Finished >>")
                              while(loop == 0): # 如果没有执行成功再执行一遍
                                    loop = self.exec_sub(exec_i, check_log)
                  else:
                        print("<< THE FILE NOT EXISTS >>\n")
                        while(loop == 0):# 如果没有执行成功再执行一遍
                              loop = self.exec_sub(exec_i, check_log)
                  print('进度: {}'.format(p_msg))
            print("\n<<<<<=========== All Perl Script Has Finished ===========>>>>>>")



if __name__ == "__main__":
      args = parse_args()
      base_root = args.root_path
      call_script =  Month_call_script(base_root)
      call_script.exc_perls()
