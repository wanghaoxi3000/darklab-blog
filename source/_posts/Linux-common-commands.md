---
title: Linux常用命令
date: 2017/12/29 01:09:00
categories:
  - Linux管理
tags:
  - Linux命令
toc: true
---

## 代理配置
### Bash代理配置
```
PROXY_ADDR='http://127.0.0.1:1080'
# socks5 代理格式
# PROXY_ADDR='socks5://bj-proxy.easystack.cn:8899'

export http_proxy=$PROXY_ADDR
export https_proxy=$PROXY_ADDR

# 全部协议均通过代理
# export all_proxy=$PROXY_ADDR
```

**取消代理**
```
unset http_proxy
unset https_proxy
```

### git 代理配置
```
git config --global https.proxy $PROXY_ADDR
git config --global https.proxy $PROXY_ADDR
```

**取消代理**
```
git config --global --unset http.proxy
git config --global --unset https.proxy
```


## 账户管理

### visudo

编辑/etc/sudoers 文件，管理可以使用 sudo 的用户

```
允许ubuntu用户在不输入该用户的密码的情况下使用所有命令
ubuntu  ALL=(ALL:ALL) NOPASSWD: ALL
```

## 文字处理

### wc

统计文件里面有多少单词, 多少行, 多少字符

- -l：仅列出行
- -w：仅列出多少字(英文单字)
- -m：多少字符

### sort

对 File 参数指定的文件中的行排序, 并将结果写到标准输出. 如果 File 参数指定多个文件, 那么 sort 命令将这些文件连接起来, 并当作一个文件进行排序

- -f：忽略大小写的差异，例如 A 与 a 视为编码相同
- -b：忽略最前面的空格符部分
- -M：以月份的名字来排序，例如 JAN, DEC 等等的排序方法
- -n：使用『纯数字』进行排序(默认是以文字型态来排序的)
- -r：反向排序
- -u：就是 uniq ，相同的数据中，仅出现一行代表
- -t：分隔符，默认是用 [tab] 键来分隔
- -k：以那个区间 (field) 来进行排序的意思

### uniq

uniq 命令可以去除排序过的文件中的重复行, 因此 uniq 经常和 sort 合用. 也就是说, 为了使 uniq 起作用, 所有的重复行必须是相邻的

- -i：忽略大小写字符的不同
- -c：进行计数
- -u：仅显示不重复的行

### cut

从一个文本文件或者文本流中提取文本列

- -d：后面接分隔字符。与 -f 一起使用
- -f：依据 -d 的分隔字符将一段信息分割成为数段，用 -f 取出第几段的意思
- -c：以字符 (characters) 的单位取出固定字符区间

### head

显示指定文件的前 10 行

- -n: 指定显示的行数

### tail

显示指定文件的后 10 行

- -n: 指定显示的行数

### dos2unix

将 windows 的换行格式"\r\n"转化成 Linux 的格式"\n"

## 文件系统

### df

检查文件系统的磁盘空间占用情况, 可以利用该命令来获取硬盘被占用了多少空间, 目前还剩下多少空间等信息

- -a: 全部文件系统列表
- -h: 方便阅读方式显示
- -H: 等于“-h”，但是计算式，1K=1000，而不是 1K=1024
- -i: 显示 inode 信息
- -k: 区块为 1024 字节
- -l: 只显示本地文件系统
- -m: 区块为 1048576 字节
- --no-sync: 忽略 sync 命令
- -P: 输出格式为 POSIX
- --sync: 在取得磁盘信息前，先执行 sync 命令
- -T: 文件系统类型

选择参数:

- --block-size=<区块大小> 指定区块大小
- -t<文件系统类型> 只显示选定文件系统的磁盘信息
- -x<文件系统类型> 不显示选定文件系统的磁盘信息
- --help 显示帮助信息
- --version 显示版本信息

### du

显示每个文件和目录的磁盘使用空间

- -a 或-all: 显示目录中个别文件的大小
- -b 或-bytes: 显示目录或文件大小时，以 byte 为单位
- -c 或--total: 除了显示个别目录或文件的大小外，同时也显示所有目录或文件的总和
- -k 或--kilobytes: 以 KB(1024bytes)为单位输出
- -m 或--megabytes: 以 MB 为单位输出
- -s 或--summarize: 仅显示总计，只列出最后加总的值
- -h 或--human-readable: 以 K，M，G 为单位，提高信息的可读性
- -x 或--one-file-xystem: 以一开始处理时的文件系统为准，若遇上其它不同的文件系统目录则略过
- -L<符号链接>或--dereference<符号链接>: 显示选项中所指定符号链接的源文件大小
- -S 或--separate-dirs: 显示个别目录的大小时，并不含其子目录的大小
- -X<文件>或--exclude-from=<文件>: 在<文件>指定目录或文件
- --exclude=<目录或文件>: 略过指定的目录或文件
- -D 或--dereference-args: 显示指定符号链接的源文件大小
- -H 或--si: 与-h 参数相同，但是 K，M，G 是以 1000 为换算单位
- -l 或--count-links: 重复计算硬件链接的文件

## 任务管理

### ps

显示当前的进程的快照信息

- -e：显示所有进程。
- -f：全格式。
- -h：不显示标题。
- -l：长格式。
- -w：宽输出。
- a：显示终端上的所有进程，包括其他用户的进程。
- r：只显示正在运行的进程。
- u：以用户为主的格式来显示程序状况。
- x：显示所有程序，不以终端机来区分。

常用的两种使用方式：

ps -ef：以标准格式显示进程的信息，包含的信息：

> UID PID PPID C STIME TTY TIME CMD

ps aux：以 BSD 的格式来显示 java 这个进程，包含的信息：

> USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND

### nohup

不挂断地运行命令，忽略所有挂断（SIGHUP）信号。在终端上执行任务后即使断掉终端后也会继续执行，一般配合&使用。那么在缺省情况下该作业的所有输出都被重定向到一个名为 nohup.out 的文件中，除非另外指定了输出文件。

```
nohup command > myout.file 2>&1
# 输出被重定向到myout.file文件中
```

## 软件管理

### apt-cache

apt-cache 是一个 apt 软件包管理工具，它可查询 apt 的二进制软件包缓存文件。

- show 显示软件的信息，包括版本号，安装状态和包依赖关系等
- madison 显示软件可安装的版本
- showpkg 搜索软件包，可用正则表达式
- policy 显示软件包的安装状态和版本信息

## 实用命令

### 加速 SCP 传输

```
tar -c source/ | pv | lz4 -B4 | ssh username@ip "lz4 -d |tar -xC dist/"
# pv 可显示压缩速度
# lz -B4 使用lz4算法以B4(64KB块大小)压缩
```

需进一步提升速度，可采用指定的完整性校验完整性校验和弱加密算法

```
tar -c source/ | pv | lz4 -B4 | ssh -c arcfour128 -o "MACs umac-64@openssh.com" username@ip "lz4 -d |tar -xC dist/"
```

参考：
[使用 tar+lz4/pigz+ssh 更快的数据传输](http://www.orczhou.com/index.php/2013/11/tranfer-data-faster-on-the-fly/)

### 系统测试

```shell
# 模拟高CPU利用率
cat /dev/urandom | gzip -9 | gzip -d | gzip -9 | gzip -d > /dev/null

# 使用 fio 测试系统 io 性能
fio --filename={} -direct=1 --iodepth=64 --rw=randrw --rwmixwrite=70 --ioengine=psync --bs=4k --size=500M --numjobs=30 --runtime=600 --name=mytest
```
