exec_command=$@
sample_interval=0.01
perf_output=mem_$sample_interval.log
code_output=code_output.log

# 执行代码，获得进程id
$exec_command & > code_output.log
pid=$!

# echo $pid
echo "" > $perf_output
while true
do
    # 不等待获取内存的指令结束，直接执行下一条指令
    smem | grep $pid | grep -v grep | awk '{print $(NF-2)}' >> $perf_output & # > log.log
    sleep $sample_interval
    # 当python程序执行完毕，退出循环
    if [ `ps -ef | grep $pid | grep -v grep | wc -l` -eq 0 ]; then
        break
    fi
done
#
# 获取内存占用最大值
echo `cat $code_output`
echo `cat $perf_output | sort -n | tail -n 1`