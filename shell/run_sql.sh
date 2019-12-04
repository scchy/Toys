#!/bin/bash
source ~/.bash_profile
# revise date 2019-10-15

last_day=$1                                           # 20181201 本月第一天
LocalCode=$2
sql_file=$3
vtc_login=$4

bil_month=`echo "scale=0;$last_day/100" | bc`



function redo_loacl() {  #  ${bil_month}  ${sql_file}  ${local_id} 
    sql_fil_qza=${2%.*}
    sql_fil_qz=${sql_fil_qza##*/}
    # 最开始进行log文件存在判断
    if [ ! -d ~/vtc_log/log_${1} ];then mkdir -p ~/vtc_log/log_${1}; fi;
    if [ ! -f ~/vtc_log/log_${1}/${sql_fil_qz}_log_${1}_${3}.log ];then touch ~/vtc_log/log_${1}/${sql_fil_qz}_log_${1}_${3}.log; fi

    # 如果没有成功循环跑
    lg_now=~/vtc_log/log_${1}/${sql_fil_qz}_log_${1}_${3}.log
    lg_f_bool=`tail $lg_now  -n 1`
    until  [  "$lg_f_bool" = "rc=0" ];
    do
        LocalCode="$3"
        source  ~/vtc_script/vtc_base/sql_values.sh
        source  "$2"
        sh ~/vtc_script/vtc_base/vtc_connet.sh "$sql" $lg_now  $vtc_login

        lg_f_bool=`tail $lg_now  -n 1`
    done 
    echo "[ ${3} ] 脚本跑成功,开始下一个地市"; 
};


if [ "$LocalCode" = 'looplocal' ];then
    echo -e "\n>>>>>> now loop exec SQL ..........\n";
    for i in {A..K};
    do
        echo -e "\n>>>>>> now exec [ $i ] sql ..........\n";
        # 没有成功重新跑       	 
        redo_loacl ${bil_month}  ${sql_file}  $i
    done;
    echo -e "\n>>>>>> now finished loop <<<<<<<<<\n";
else
    echo -e "\n>>>>>> now exec [ $LocalCode ] sql ..........\n";
    redo_loacl ${bil_month}  ${sql_file}  $LocalCode
fi;
