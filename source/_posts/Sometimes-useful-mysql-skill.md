---
title: 偶尔用得上的MySQL操作
categories:
  - 数据库
tags:
  - MySQL配置
toc: true
date: 2018-09-11 00:57:47
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