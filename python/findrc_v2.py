# python 3.6
# Author:              Scc_hy
# Create date:         2019-08-12
# Function:            检查当前文件下的log 文件是否都已经跑完，并给出需要跑的地市
# Version : 1.2 改为检查rc=0下面的地市
# Version : 1.3 增加清理日志; 增加进度条 


## 调用包
import os 
import re 
import argparse 
from datetime import  datetime
from tqdm import tqdm

def parse_args():
    """
    调用程序
    """
    parser = argparse.ArgumentParser(descroption = 'Check the log if finished')
    parser.add_argument('-path', '--base_root', required = True, help = 'The logs file')
    args = parser.parse_args()
    return args


class find_rc():
    """
    查看是否是一个地市已经跑完  
    如果有地市没有跑完  
    就生成需要跑的perl的log  
    """
    def __init__(self, base_root = None):
        self.base_root = os.curdir if base_root == None else base_root
        self.log_list = self.get_all_log()
        self.out_log_path = os.path.join(self.base_root, 'find_rc_{}.log'.format(datetime.now().strftime('%Y%m%d')))
        self.Local_ids = [chr(i) for i in range(ord('A'), ord('K') +1)]
        self.clear_file()
        

    def get_all_log(self):
        return [i for i in os.listdir(self.base_root) if '.log' in i and 'find_rc' not in i]

    ## 文件读取 
    def read_log(self, log_file):
        """
        文件读取
        """
        f = open(log_file, 'r', encoding = 'utf8')
        log_contet = f.read()
        f.close()
        return log_contet


    def find_finished_locals(self, log_contet):
        """
        找出完成的城市
        """
        finish_list = []
        for loacl in self.Local_ids:
            try:
                a = re.search(r'\brc=0\n\t\t(.*)\nFINISHED_CITY:({})--(.*)'.format(loacl), log_contet)
                finish_list.append(a.group(2))
            except:
                finish_list
        return finish_list

    
    def month_add_sub(self, _dt, method = 'add'):
        """
        月份12进制
        """
        _dt = str(_dt)
        if method == 'add':
            if(_dt[-2:] == '12'):
                    out = str(int(_dt[:4]) + 1) +'01' 
            else:
                    out = int(_dt) + 1
            return str(out) 
        else:
            if(_dt[-2:] == '01'):
                    out = str(int(_dt[:4]) - 1) +'12' 
            else:
                    out = int(_dt) - 1
            return str(out) 
            
    def clear_file(self):
        """
        清空日志
        """
        f = open(self.out_log_path, 'a+', encoding = 'utf8')
        f.seek(0)
        f.truncate()
        f.close()

    def write_log(self, msg):
        f = open(self.out_log_path, 'a+', encoding = 'utf8')
        f.write(msg)
        f.close()


    def need_exec(self, fil_name, local, if_finished):
        """
        :param : fil_name log文件名 
        :param loacl: [A-K] object
        :param if_finished: bool
        """
        fil_name_search = re.search(r"(.*)_(\d+).log", fil_name)
        perl_name = fil_name_search.group(1)
        log_dt = fil_name_search.group(2)
        start_dt = self.month_add_sub(log_dt)

        msg = "{} has not finished  {}:\n".format(perl_name, log_dt)
        print(msg[:-2])

        exc_i = "perl {}.pl {}_{}01.dir >>  {};\n".format(perl_name, local, start_dt, fil_name)
        self.write_log(exc_i)
        print(exc_i[:-2])


    def exec_perl(self):
        f = open(self.out_log_path, 'r', encoding = 'utf8')
        exc_list = f.readlines()
        f.close()
        exc_list_fi = [i for i in exc_list if 'finished' not in i]
        print("NOW EXCEC...")
        for exc_i in tqdm(exc_list_fi):
            print("Excecing: {}".format(exc_i))
            os.system(exc_i)

 
    def check_all_logs(self):
        """
        逐一文件读取：  
            检查是否11个地市都完成
            未完成的输出log需要进行的程序
        """
        for fil in self.log_list:
            log_contet = self.read_log(fil)
            finish_list = self.find_finished_locals(log_contet)
            not_finished_locals = list(set(self.Local_ids) - set(finish_list))
            if len(not_finished_locals) == 0:
                fil_name_search = re.search(r"(.*)_(\d+).log", fil)
                perl_name = fil_name_search.group(1)
                log_dt = fil_name_search.group(2)
                msg = "{} has finished {};\n".format(perl_name, log_dt)
                self.write_log(msg)
                print(msg[:-2])
            else:
                for local in not_finished_locals:
                    self.need_exec(fil, local, if_finished = len(finish_list) >= 11)



        
if __name__ == '__main__':
    try:
        args = parse_args()
        base_root = args.base_root
    except: 
        base_root = os.curdir

    f_rc = find_rc(base_root)
    f_rc.check_all_logs()
    try:
        f_rc.exec_perl()
    except: pass 
