---
title: MySQL 配置优化
date: 2018-04-05 11:37:05
categories:
- 数据库
tags:
- MySQL配置
toc: true
slug: MySQL-config-adjust
---

## CentOS系统参数优化
### 内核相关参数 /etc/sysctl.conf
```
net.core.somaxconn=65535  # TCP监听队列，可调为2048以上
net.core.netdev_max_backlog=65535   #  每个网络接口接收数据包的速率比内核快时允许发送到队列中的数目
net.ipv4.tcp_max_syn_backlog=65535  # 还未获得连接的请求可保存在内存中的数目，超过的数目可能会被抛弃

net.ipv4.tcp_fin_timeout=10  # TCP连接最大等待时间
net.ipv4.tcp_tw_reuse=1      # 缩短以加快TCP资源的回收
net.ipv4.tcp_tw_recycle=1

net.core.wmem_default=87380  # TCP接收和发送缓冲区的默认值和最大值
net.core.wmem_max=16777216
net.core.rmem_default=87380
net.core.rmem_max=16777216

net.ipv4.tcp_keepalive_time=120  # 缩短以减少失效连接所占用TCP资源的数量
net.ipv4.tcp_keepalive_intvl=30
net.ipv4.tcp_keepalive_probes=3

kernel.shmmax=4294967295  # Linux内核参数中最重要的参数之一，用于定义单个共享内存段的最大值
                          # 这个参数应该足够大，以便能在一个共享内存段容纳下整个Innodb缓冲池的大小
                          # 这个值大小对于64位Linux系统，可取最大值位物理内存值-1byte，
                          # 建议值为大于物理内存的一半，一般取大于Innodb缓冲池的大小即可

vm.swappiness=0           # 除非虚拟内存完全满了，否则不要使用交换区
```

### Linx PAM 插入式认证模块的配置文件/etc/security/limit.conf
```
# 添加如下两行到此文件末尾，增加资源限制 
# *     对所有用户有效
# soft  当前系统生效的设置
# hard  表明系统中所能设定的最大值
# 65535 表示所限制的资源是打开文件的最大数目

* soft mofile 65535  
* hard nofile 65535
```

### 磁盘调度策略 /sys/block/devname/queue/scheuler
```
# 使用如下方式来开启deadline调度策略

echo deadline > /sys/block/sda/queue/scheuler
```

## 存储引擎选择
### MyISAM 
适用场景:
- 非事务性应用
- 只读类应用
- 空间类应用(5.7版本前唯一支持空间函数引擎)

### Innodb引擎
特性:
- 事物型引擎
- 完全支持ACID特性(原子 一致 隔离 持久)
- Redo Log 和 Undo Log
- 支持行级索, 可以最大程度的支持并发

使用表空间进行数据存储, `innodb_file_per_table` 参数为 `on` 时使用独立表空间(ibd后缀文件), `off` 时使用系统表空间(ibdataX)

功能差异:
- 系统表空间5.5及以前版本无法简单收缩文件大小
- 独立表空间可通过 `optimize table` 命令收缩系统空间
- 独立表空间存在IO瓶颈
- 独立表空间可以同时向多个文件刷新数据

**建议使用 Innodb 独立表空间(5.6及以后版本的默认表空间)**

查看状态:
通过 `show engine innodb status` 可以查看 innodb 引擎的状态信息

适用场景:
- 适合大多数OLTP(联机事务处理)应用

### CSV
特点:
- 数据以文本方式储存在文件中
    - .CSV文件存储表内容
    - .CSM文件存储表的元数据如表状态和数据量
    - .frm文件存储表结构信息
- 以CSV格式进行数据存储
- 所有列必须都是不能为NULL的
- 不支持索引, 不适合在线处理
- 可以对数据文件直接编辑

适用场景:
- 适合作为数据交换的中间表

### Archive
特点:
- 以zlib对表数据进行压缩, 磁盘I/O更少
- 数据存储在 ARZ 为后缀的文件中
- 只支持 insert 和 select 操作
- 只允许在自增ID列上加索引

适用场景:
- 日志和数据采集类应用

### Memory
特点:
- 也称为HEAP存储引擎, 所有数据保存在内存中, 数据易失, 需要数据可再生
- 支持 HASH(默认, 适合等值查找) 索引和 BTree(适合范围查找) 索引
- 所有字段都为固定长度 varchar(10)=char(10)
- 不支持 BLOG 和 TEXT 等大字段
- Memory 存储引擎使用表级锁
- 最大大小由 `max_heap_table_size` 参数决定

适用场景:
- 用于查找或者是映射表, 如邮编和地区的对应表
- 用于保存数据分析中产生的中间表
- 用于缓存周期性聚合数据的结果表

### Federated
特点:
- 提供了访问远程MySQL服务器上表的方法
- 本地不存储数据, 数据全部放到远程服务器上
- 本地需要保存表结构和远程服务器的连接信息

使用方法:
- 默认禁止, 启用需要在启动时增加federated参数

使用场景:
- 偶尔的统计分析及手工查询
