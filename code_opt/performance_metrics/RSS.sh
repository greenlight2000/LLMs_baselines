#!/bin/bash

exec_command=$@ # 获取原指令
output=./perf.log

# echo output:$output
# echo exec_command:$exec_command
/usr/bin/time -o $output -f "%M" python empty_python.py > /dev/null
empty_RSS=`cat $output`

re=$(/usr/bin/time -o $output -f "user=%U,sys=%S,RSS=%M" $exec_command) # > /dev/null
#从输出文件中分别提取user,sys,RSS
user=`cat $output | grep user | awk -F ',' '{print $1}' | awk -F '=' '{print $2}'`
sys=`cat $output | grep sys | awk -F ',' '{print $2}' | awk -F '=' '{print $2}'`
RSS=`cat $output | grep RSS | awk -F ',' '{print $3}' | awk -F '=' '{print $2}'`

# times=$(($user+$sys))
memory=$(($RSS-$empty_RSS))

echo $re # 原程序返回结果
echo user_time:$user # CPU用户态执行时间
echo sys_time:$sys # CPU内核态执行时间
echo memory:$RSS-$empty_RSS=$memory # 最大内存占用（用原程序的RSS减去一个空程序的RSS，减少共享内存干扰）