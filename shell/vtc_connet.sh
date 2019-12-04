#!/bin/bash
source ~/.bash_profile
## vertcica 数据库连接 + SQL运行
## Create data: 2019-10-10
## Scc_hy

sql=$1
log_file=$2
vtc_login=$3

log_name=`head $vtc_login -n 1`
pass_word=`tail $vtc_login -n 1`

# 连接 + 运行sql
vsql -h IP.ip.ip.ip -d xxx -U ${log_name} -w $pass_word -e -i -C -c "$sql"  >> $log_file;

# 返回的状态
rc=$?
echo rc=$rc >> $log_file;
