## 核心文件 `~/vtc_script/vtc_base/`
需要将下列文件放置在 /vtc_base/ 中
-   vtc_login      vertcia账号名 + 密码  
-   sql_values.sh  存储主要的SQL变量，变量名称和perl脚本一样  
-   vtc_connet.sh  连接数据库 & 运行SQL &  输出日志  
-   run_sql.sh     生成日志文件 & 检测是否跑数成功，未成功则再次执行 & 判断是跑一个地市还是全部地市  


## SQL及运行文件任何目录
try_sql.sql               主要的SQL;插入数据记得 commit; 文件内容 必须 在 sql=" "的双引号之间  
quick_start_vtcsql.sh     快速运行文件   
    需要输入 运行时间、运行地市/looplocal、sql文件的路径、登录文件的路径  
【注：】  
-    quick_start_vtcsql.sh + try_sql.sql 文件 <=> vertica.pl + vertica.bat  
-    quick_start_vtcsql.sh 和 try_sql.sql 文件路径可改  
-    vtc_login <=> C:\etl\etc\LOGON_PRT_VTC  路径建议不要改，可以创建多个  

## crontab 设置
类似：  
> `30 6 16 * * sh ~/vtc_script/quick_start_vtcsql.sh`
    
![模块流程图](https://github.com/scchy/Toys/blob/master/shell/%E6%A8%A1%E5%9D%97%E7%AE%80%E5%8D%95%E4%BB%8B%E7%BB%8D.jpg)
