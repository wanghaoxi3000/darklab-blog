---
title: 偶尔用得上的MySQL操作
categories:
  - 数据库
tags:
  - MySQL技巧
toc: true
date: 2018-09-11 00:57:47
slug: Sometimes-useful-mysql-skill
---

### 数据库编码
查看数据库编码
```
use xxx
show variables like 'character_set_database';
```

切换数据库编码
```
alter database xxx CHARACTER SET gb2312;
```

### 修改自增ID
创建表格时设置自增ID从N开始：
```SQL
CREATE TABLE TABLE_1 (
        ID INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        NAME VARCHAR(5) NOT NULL 
    )
AUTO_INCREMENT = 100;
```

让自增ID从默认值开始, **但是注意：这个命令会清空数据包记录！**
```
TRUNCATE TABLE table1
```

设置user表自增ID从123456开始
```
alter table users AUTO_INCREMENT=123456;
```

### 无法远程登录
在已经修改配置文件中的地址为 `0.0.0.0` 但仍然无法远程登录的情况下, 一般是需要对数据库中的账户信息进行修改

#### 授权用户 (推荐)
```
mysql>GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION;
```

#### 直接修改 `user` 表
```
mysql>use mysql;
mysql>update user set host = '%' where user = 'root';
```

以上方法操作完成后还需执行 `FLUSH PRIVILEGES;` 刷新一遍权限

### 远程连接速度慢
有时远程连接到 MySQL 用时会很久, 同时本地连接 MySQL 正常. 出现这种问题的主要原因是默认安装的 MySQL 开启了 DNS 的反向解析.

#### MySQL DNS 反向解析
MySQL 接收到连接请求后，获得的是客户端的ip，为了更好的匹配 `mysql.user` 里的权限记录(某些是用 hostname 定义的).
 如果mysql服务器设置了dns服务器, 并且客户端 ip 在 DNS 上并没有相应的hostname, 那么这个过程很慢, 导致连接等待.

#### 禁用 DNS 反向解析
在 MySQL 的配置文件 `/etc/mysql/mysql.conf.d/mysqld.cnf` 中 `[mysqld]` 添加 `skip-name-resolve` 即可禁用 DNS 反向解析, 加快远程连接的速度. 同时这样配置后不能在 MySQL 的授权表中使用主机名了, 只能使用IP.
