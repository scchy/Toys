#!/bin/bash
source ~/.bash_profile
## 一般需要用到的变量
## Create data: 2019-10-10
## Scc_hy
## tip: 必须输入格式为  类似： 20190101

STMT_DATE=`date -d $last_day "+%Y-%m-%d"` 
BIL_MONTH=`date -d "$last_day -1 month" +%Y%m`      # 201811 上个月
BIL_MONTH1=`date -d "$last_day -2 month" +%Y%m`       # 201810 上上个月
BIL_MONTH2=`date -d "$last_day -3 month" +%Y%m`       # 201809 上三个月
BIL_MONTH3=`date -d "$last_day -4 month" +%Y%m`       # 201808 上四个月
last_med=`date -d "$last_day -1 day" +%Y-%m-%d`      # 2018-11-30      lats month last day 上个月最后一天
Cur_Year_Yyyy_Mm_Dd=`date -d $last_day "+%Y"`0101; # 当前年1月1号
Before_First_Day_Yyyy_Mm_Dd=`date -d "$last_day -1 month" +%Y-%m`01;    #上个月第一天
Cur_Year_Yyyy=`date -d "$last_day -1 month" +%Y`

declare -A local_chinese 
local_chinese=([A]="区域" [B]="区域" [C]="区域" [D]="区域" [E]="区域" [F]="区域" [G]="区域" [H]="区域" [I]="区域" [J]="区域" [K]="区域")

declare -A fengongsiz # 分公司
fengongsiz=([A]="区域" [B]="区域" [C]="区域" [D]="区域" [E]="区域" [F]="区域" [G]="区域" [H]="区域" [I]="区域" [J]="区域" [K]="区域")
fengongsi=${fengongsiz[$LocalCode]}

