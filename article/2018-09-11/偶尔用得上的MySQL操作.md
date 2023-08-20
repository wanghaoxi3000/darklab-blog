---
date: "2018-09-11"
type: Post
category: 数据库
slug: sometimes-useful-mysql-skill
tags:
  - MySQL技巧
title: 偶尔用得上的MySQL操作
status: Published
urlname: a9ab7bf6-f568-4e0a-8f97-639be1acacf5
updated: "2023-07-17 14:41:00"
---

### 数据库编码

查看数据库编码

```text
use xxx
show variables like 'character_set_database';

```

切换数据库编码

```text
alter database xxx CHARACTER SET gb2312;

```

### 修改自增 ID

创建表格时设置自增 ID 从 N 开始：

```sql
CREATE TABLE TABLE_1 (
        ID INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        NAME VARCHAR(5) NOT NULL
    )
AUTO_INCREMENT = 100;

```

让自增 ID 从默认值开始, **但是注意：这个命令会清空数据包记录！**

```text
TRUNCATE TABLE table1

```

设置 user 表自增 ID 从 123456 开始

```text
alter table users AUTO_INCREMENT=123456;

```

### 无法远程登录

在已经修改配置文件中的地址为 `0.0.0.0` 但仍然无法远程登录的情况下, 一般是需要对数据库中的账户信息进行修改

### 授权用户 (推荐)

```text
mysql>GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION;

```

### 直接修改 `user` 表

```text
mysql>use mysql;
mysql>update user set host = '%' where user = 'root';

```

以上方法操作完成后还需执行 `FLUSH PRIVILEGES;` 刷新一遍权限

### 远程连接速度慢

有时远程连接到 MySQL 用时会很久, 同时本地连接 MySQL 正常. 出现这种问题的主要原因是默认安装的 MySQL 开启了 DNS 的反向解析.

### MySQL DNS 反向解析

MySQL 接收到连接请求后，获得的是客户端的 ip，为了更好的匹配 `mysql.user` 里的权限记录(某些是用 hostname 定义的).
如果 mysql 服务器设置了 dns 服务器, 并且客户端 ip 在 DNS 上并没有相应的 hostname, 那么这个过程很慢, 导致连接等待.

### 禁用 DNS 反向解析

在 MySQL 的配置文件 `/etc/mysql/mysql.conf.d/mysqld.cnf` 中 `[mysqld]` 添加 `skip-name-resolve` 即可禁用 DNS 反向解析, 加快远程连接的速度. 同时这样配置后不能在 MySQL 的授权表中使用主机名了, 只能使用 IP.
