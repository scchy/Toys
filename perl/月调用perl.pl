#!/usr/bin/perl
# Author:              Scc_hy
# Create date:         2019-06-06
# Function:            调用perl文件

## 调用包
use POSIX; # 时间包
use strict;
use Time::HiRes qw(gettimeofday tv_interval);

################################################  生成配置命令   ################################################
my $year_month_day = strftime("%Y%m%d",localtime());
my $year_month = strftime("%Y%m",localtime());
my @Local_id = qw/ A B C D E F G H I J K /;
## 打开文件
my $dir_root = $ARGV[0];
$dir_root =~ s|(\\)|\/|g; 

my $dir =   "${dir_root}/*.pl"; ## 调用文件目录
my @dir = glob( $dir );


my $id; # local_id 内元素的名
my $d; # 文件 内元素的名
my @exec_array; # 生成配置命令存放数组
my $n = 0;
foreach  $d (@dir){
      $d =~ /(.*)\/(.*)\./mg;
      my $d_dir = $1;
      my $d_name = $2;
      foreach  $id (@Local_id){
            @exec_array[$n] =  "perl $d ${id}_${year_month_day}.dir >${d_dir}/log/${year_month}log/${d_name}_${id}${year_month}.log\n";
            $n++;
      }
}
;


# 创建子程序
sub check_if_finished{
      my $f = $_[0];
      my $MYFILE;
      $f =~ /(\w+\.log)$/g;
      my $exc_pl = $1;
      print "check_if_finished: $exc_pl \n";
      open (MYFILE, "<$f") || die ("Could not open file"); 
      my @array = <MYFILE>;
      my $check = grep {/rc=0/} @array ; # 寻找 rc=0 
      print $check, "\n";
      if($check == 1){
            print "==[ Finished ]== \n\n";
      }else{
            print "XXXX{ need exec again }XXXX \n";
      }
      close(MYFILE);
      return $check;
}
;

sub exec_sub{
      my $check;
      my ($exec_cmd, $log) = @_;
      print "=====================================================================\n";
      print "NOW EXEC: $exec_cmd  \n";
      system("$exec_cmd");
      print "Check Log File : $log\n";
      $check = &check_if_finished($log) ;
      print "=====================================================================\n\n";
      return $check;
}
;

sub if_log_exist{
      my $check_log = $_[0];
      $check_log =~ /(.*log).*\.log/g;
      my $log_path = $1;
      my $chek_bool =  -e $check_log;
      if($chek_bool ne 1){
            mkdir( $log_path );
      }
      return $chek_bool
}
;

## 执行文件 
my $exec ;
foreach  $exec (@exec_array){
      $exec =~ /(\w+)\.pl (.*)\.dir >(.*\.log)/mg;
      my $check_log = $3;
      my $Fuction = $1;
      my $loop = 0;
      print ">>>>>>>>>> Start:  $Fuction --- $year_month <<<<<<<<<<<<<<\n";
      print "=============================  Check if Finished  =================\n";
      if(&if_log_exist($check_log) == 1){
            print '<< THE FILE HAS EXISTS >>'."\n";
            my $check = &check_if_finished($check_log);  
            if ($check == 1){
                  print '<< The month and local has Finished >>'."\n\n";
                  next;
            }else{
                  print '<< The month and local NOT Finished >>'."\n";
                  while($loop == 0){ # 如果没有执行成功再执行一遍
                        $loop = &exec_sub( $exec, $check_log );
                  }
            }
      }else{
            print '<< THE FILE NOT EXISTS >>'."\n";
            while($loop == 0){ # 如果没有执行成功再执行一遍
                  $loop = &exec_sub( $exec, $check_log );
            }
      }

}



print "\n<<<<<=========== All Perl Script Has Finished ===========>>>>>>\n";
