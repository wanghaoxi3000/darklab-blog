---
date: "2017-04-20"
type: Post
category: Linux管理
slug: the-configuration-program-becomes-a-linux-service
tags: []
title: 配置程序成为Linux服务
status: Published
urlname: 4531936b-6f90-48a8-8d44-c663f3a660cd
updated: "2023-07-17 15:09:00"
---

最近写了个程序需要随 Linux 启动时自动运行起来, 查了一些方法后, 通过配置程序成为系统的服务实现了这个需求, 在此记录一下.

### 测试程序

```text
#! /bin/sh

while [ true ]
do
    echo "[`date +%Y%m%d-%H%M%S`]" >> /var/log/test_sh.log
    sleep 5
done

```

每 5 秒, 向/var/log/test_sh.log 输出一个当前时间的字符串, 保存为 test_sh

### 服务控制脚本

通过此服务控制脚本, 可以实现通过系统的 service 命令设置这个服务的 start, stop, 以及运行 status 查询状态, 保存为 tstd. 服务控制脚本后接 d 是一种惯例性的命名, 代表 daemon.

```text
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

通过以上注释, 可通过`chkconfig`或者`insserv`命令来安装服务, 指定服务的在 Linux 的对应的执行等级中自启动以及停止, 并设定启动顺序.

Linux 执行等级:

- 等级 0 表示：表示关机
- 等级 1 表示：单用户模式
- 等级 2 表示：无网络连接的多用户命令行模式
- 等级 3 表示：有网络连接的多用户命令行模式
- 等级 4 表示：不可用
- 等级 5 表示：带图形界面的多用户模式
- 等级 6 表示：重新启动

```text
TEST_BIN='/usr/sbin/test_sh'
source /etc/rc.status
test -x $TEST_BIN || exit 5

rc_reset

```

这一段在/usr/sbin/中检查服务对应的脚本程序是否存在, 并加载/etc/rc.status 这个脚本, rc.status 脚本中包含了 rc_reset, rc_status, rc_failed, rc_reset, rc_exit 等有用的命令, 可以通过接受上一条命令的结果, 在 service 命令执行时显示出不同的效果.

```text
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

killproc 则会通过通过向程序发送 SIGTERM 来终止程序的运行, 若程序没有响应, 还会依次发送 SIGHUP, 以及 SIGKILL 来删除程序, 确认程序已关闭后吗会删除程序产生的 PID 文件.

checkproc 会检查程序的状态, 根据程序的状态返回不同的值:

- 0: 服务运行中
- 1: 服务停止, 但是/var/run 下的 pid 文件仍然存在
- 2: 服务停止, 但是/var/lock 下的文件仍然存在
- 3: 服务没有在运行

### 安装脚本

```text
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

安装脚本使用 install 命令来拷贝脚本到指定目录, 并设置对应的权限. chkconfig 命令可以将这个自定义的服务添加到设定的执行等级的自启动中, 即在/etc/rc\*.d 中创建顺序对应的符号链接.
最后在/etc/cron.hourly 中创建了一个脚本来每小时自动拉起一次服务, 防止服务意外终止掉. 还可以通过 crontab 来创建更精确的自动拉起间隔.

以上脚本在 SUSE 下运行通过, 其他系统的部分命令不一样, 但整体流程应该是差不多的.

参考: [http://www.cnblogs.com/bangerlee/archive/2012/03/30/2412652.html](http://www.cnblogs.com/bangerlee/archive/2012/03/30/2412652.html)
