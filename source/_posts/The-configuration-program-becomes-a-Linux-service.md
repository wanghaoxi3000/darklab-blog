---
title: 配置程序成为Linux服务
date: 2017/4/20 23:50:00
categories:
- Linux管理
toc: true
---

最近写了个程序需要随Linux启动时自动运行起来, 查了一些方法后, 通过配置程序成为系统的服务实现了这个需求, 在此记录一下.


### 测试程序
```
#! /bin/sh

while [ true ]
do
    echo "[`date +%Y%m%d-%H%M%S`]" >> /var/log/test_sh.log
    sleep 5
done
```
每5秒, 向/var/log/test_sh.log 输出一个当前时间的字符串, 保存为test_sh


### 服务控制脚本
通过此服务控制脚本, 可以实现通过系统的service命令设置这个服务的start, stop, 以及运行status查询状态, 保存为tstd. 服务控制脚本后接d是一种惯例性的命名, 代表daemon.
```
#! /bin/sh

# chkconfig: 35 99 99
# descroption: service test script
# processname: test_sh


### BEGIN INIT INFO
# Provides:           tstd
# Required-Start:
# Should-Start: 
# Required-Stop: 
# Should-Stop: 
# Default-Start:      2 3 5
# Default-Stop:       0 1 2 6
# Description:        service test script 
#
### END INIT INFO
```
通过以上注释, 可通过`chkconfig`或者`insserv`命令来安装服务, 指定服务的在Linux的对应的执行等级中自启动以及停止, 并设定启动顺序.

Linux执行等级:
- 等级0表示：表示关机
- 等级1表示：单用户模式
- 等级2表示：无网络连接的多用户命令行模式
- 等级3表示：有网络连接的多用户命令行模式
- 等级4表示：不可用
- 等级5表示：带图形界面的多用户模式
- 等级6表示：重新启动

```
TEST_BIN='/usr/sbin/test_sh'
source /etc/rc.status
test -x $TEST_BIN || exit 5

rc_reset
```
这一段在/usr/sbin/中检查服务对应的脚本程序是否存在, 并加载/etc/rc.status这个脚本, rc.status脚本中包含了rc_reset, rc_status, rc_failed, rc_reset, rc_exit等有用的命令, 可以通过接受上一条命令的结果, 在service命令执行时显示出不同的效果.


```
case "$1" in
    start)
        echo "starting test daemon"
        startproc $TEST_BIN
        rc_status -v
        ;;
    
    stop)
        echo "stop test daemon"
        killproc $TEST_BIN
        rc_status -v
        ;;
        
    status)
        echo "stop test daemon"
        checkproc $TEST_BIN
        rc_status -v
        ;;
        
    *)
        echo "Usage: $0 { start | stop | status }"
        exit 1
        ;;
esac
```
startproc 默认通过程序的绝对路径和`/var/run/<basename>.pid` 来检索程序是否运行, 没有检索到时便以后台的方式来运行程序.

killproc则会通过通过向程序发送SIGTERM来终止程序的运行, 若程序没有响应, 还会依次发送SIGHUP, 以及SIGKILL来删除程序, 确认程序已关闭后吗会删除程序产生的PID文件.

checkproc会检查程序的状态, 根据程序的状态返回不同的值:
- 0: 服务运行中
- 1: 服务停止, 但是/var/run 下的pid文件仍然存在
- 2: 服务停止, 但是/var/lock 下的文件仍然存在
- 3: 服务没有在运行


### 安装脚本
```
#! /bin/sh

ROOT_DIR=$(echo $(cd "$(dirname "$0")"; pwd))

echo $ROOT_DIR
service tstd stop > /dev/null 2>&1

install -m 750 ${ROOT_DIR}/test_sh /usr/sbin/
install -m 750 ${ROOT_DIR}/tstd /etc/init.d/

chkconfig -a tstd > /dev/null 2>&1
service tstd start > /dev/null 2>&1
echo -e "#!/bin/sh \n service tstd start > /dev/null 2>&1" \
    > /etc/cron.hourly/tst_crontab

echo 'success'
```
安装脚本使用install命令来拷贝脚本到指定目录, 并设置对应的权限. chkconfig命令可以将这个自定义的服务添加到设定的执行等级的自启动中, 即在/etc/rc*.d中创建顺序对应的符号链接.
最后在/etc/cron.hourly中创建了一个脚本来每小时自动拉起一次服务, 防止服务意外终止掉. 还可以通过crontab来创建更精确的自动拉起间隔.

以上脚本在SUSE下运行通过, 其他系统的部分命令不一样, 但整体流程应该是差不多的.


参考: [http://www.cnblogs.com/bangerlee/archive/2012/03/30/2412652.html](http://www.cnblogs.com/bangerlee/archive/2012/03/30/2412652.html)
