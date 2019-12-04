#!/bin/bash
source ~/.bash_profile
## 运行模板  运行仅需要 该文件 + 文件名_sql.sql
## Create data: 2019-10-15
## 需要主要SQL 文件插入数据要用commit; sql 文件的变量同perl

last_day=20190901                                   # 运行时间 可以用该变量 ( `echo $(date +"%Y%m")01` )  就无需再输入参数直接在crontab中执行
LocalCode='looplocal'                               # 运行地市 或者 looplocal        
sql_file=~/vtc_script/try_sql.sql                   # 主要的SQL  路径
vtc_login=~/vtc_script/lzwul_login                  # 登录文件名  第一行为账号， 最后一行为密码


sh ~/vtc_script/vtc_base/run_sql.sh $last_day $LocalCode   "$sql_file"  $vtc_login
