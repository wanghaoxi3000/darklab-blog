---
date: "2017-01-22"
type: Post
category: 数据库
slug: mysql-will-surely-know-notes
tags: []
title: MySQL必知必会笔记
status: Published
urlname: 4fe27424-e1b9-4e3a-a456-3d9ce383e8b4
updated: "2023-07-17 15:10:00"
---

## 数据库和表的增删改

### 创建数据库

```text
CREATE  DATABASE 数据库名;

# mysql中还可使用如下语句
CREATE SCHEMA 数据库名;

```

### 数据库选择

```text
USE 数据库名;

```

### 创建表

```text
create table students
(
	id int unsigned not null auto_increment primary key,
	name char(8) not null,
	sex char(4) not null,
	age tinyint unsigned not null,
	tel char(13) null default "-"
);

```

### 重命名表名

```text
RENAME TABLE 旧表名 TO 新表名;

```

### 删除数据库和表

```text
DROP DATABASE 数据库名;
DROP TABLE 表名;

```

## 插入和更新数据

### 使用 INSERT 插入行

```text
INSERT INTO Customer
VALUES(NULL,
'100 Main Street',
'Los Angles',
'CA');

```

插入一个新客户到 customers 表。存储到每个表列中的数据在 VALUES 子句中给出，对每个列必须提供一个值。虽然这种语法很简单，但并不安全，应该尽量避免使用。
更安全的写法:

```text
INSERT INTO Customer(cust_name,
    cust_address,
    cust_city,
    cust_state)
VALUES('Pep E',
    '100 Main Street',
    'Los Angeles',
    'CA');

```

这种写法即使表的结构改变，此 INSERT 语句仍然能正确工作。

### 使用 UPDATA 更新数据

```text
UPDATA Customers
SET cust_email = 'elmer@fudd.com'
WHERE cust id = 10005;

```

### 使用 IGNORE 忽略错误

如果用 UPDATE 语句更新多行，并且在更新这些行中的一行或多行时出一个现错误，则整个 UPDATE 操作被取消。为即使是发生错误，也继续进行更新，可使用 IGNORE 关键字：

```text
UPDATE IGNORE customers...

```

### 使用 DELETE 删除数据

```text
WHERE FROM customers
WHERE cust_id = 10006;

```

如果想从表中删除所有行，不要使用 DELETE。可使用 TRUNCATE TABLE 语句，它完成相同的工作，但速度更快(TRUNCATE 实际是删除原来的表并重新创建一个表，而不是逐行删除表中的数据)。

## 表的查询

### 查询列

```text
SELECT 列名 FROM 表名;

```

### 查询列中不重复项 DISTINCT

```text
SELECT DISTINCT 列名 FROM 表名;

```

### 限制结果数量 LIMIT

```text
SELECT 列名 FROM 表名 LIMIT 数量;

```

### 排序结果

```text
SELECT 列名 FROM 表名 ORDER BY 一个或多个列的名字;

```

默认为升序排列, 若要降序排序, 通过 DESC 可指定降序排序.

```text
SELECT 列名 FROM 表名 ORDER BY 一个或多个列的名字 DESC;

```

### 过滤结果

```text
SELECT 列名 FROM 表名 WHERE 条件;

//使用LIKE来匹配通配符
SELECT 列名 FROM 表名 WHERE 列名 LIKE 条件;

//使用REGEXP来使用正则表达式
SELECT 列名 FROM 表名 WHERE 列名 REGEXP 条件;

```

SQL 的不等于通过'<>'来表示, 判断 NULL 通过 IS NULL 来表示, BETWEEN .. AND ..或者 IN (.., ..)表示范围.
多个条件组合时, AND 比 OR 的优先级要高.
MySQL 中正则表达式不区分大小写, 若要区分大小写, 可用 REGEXP BINARY.

### 组合查询

利用 UNION，组合数条 SQL 查询结果作为单个查询结果集返回。这些组合查询通常称为并或复合查询.

```text
SELECT vend_id, prod_id, prod_price
FROM products
WHERE prod_price <=5
UNION
SELECT vend_id, prod_id, prod_price
FROM products
WHERE vend_id IN (1001, 1002);

```

## 拼接

### Concat 函数实现拼接

```text
SELECT Concat (列名1, '(', 列名2, ')') FROM 表名 WHERE 条件;

```

多数 DBMS 通过+或||来实现拼接, MySQL 通过 Concat()函数来实现.

### 命名列的别名

```text
SELECT Concat (列名1, '(', 列名2, ')') AS 新列名 FROM 表名 WHERE 条件;

```

通过 AS 关键字, 讲拼接后的列命名一个别名.

### 子查询

```text
SELECT cust_id
FROM orders
WHERE order_num IN (SELECT order_num
                    FROM orderitems
                    where prod_id = 'TNT2');

```

使用 IN 来进行子查询

```text
SELECT cust_name,
       cust_state,
       (SELECT COUNT(*)
        FROM orders
        WHERE　orders.cust_id = custom.cust_id) AS orders
FROM customers
ORDER BY cust name;

```

## 函数

### 文本函数

- Upper() 文本转换为大写
- Soundex() 寻找读音相近的数据
- Trim() 删除多余的空格
- RTrim() 删除右侧多余的空格
- LTrim() 删除左侧多余的空格

### 日期及时间处理函数

![image](../../images/a4736a4f957306bcd7d190ea5734b5ff.jpg)

### 数值处理函数

![image](../../images/b602884e2667e950f40ae755be159d31.jpg)

### 聚集函数

![image](../../images/1cdca358588195fd169f383c6d9096dc.png)

可在函数中以 DISTINCT 来仅汇总不同的值

```text
SELECT AVG(DISTINCT prod_price) AS avg_price
FROM products
WHERE vend_id = 1003;

```

## 分组

### 在 SELECT 语句的 GROUP BY 子句中建立分组

```text
SELECT vend_id, COUNT(*) AS num_prods
FROM products
GROUP BY vend_id;

```

### 通过 HAVING 来在分组中过滤数据

```text
SELECT cust_id, COUNT(*) AS orders
FROM orders
GROUP BY cust_id
HAVING COUNT(*) >= 2;

```

### 分组使用的注意事项

- GROUP BY 子句可以包含任意数目的列。这使得能对分组进行嵌套，为数据分组提供更细致的控制
- 在建立分组时，指定的所有列都一起计算
- GROUP BY 子句中列出的每个列都必须是检索列或有效的表达式（但不能是聚集函数）, 如果在 SELECT 中使用表达式，则必须在 GROUP BY 子句中指定相同的表达式, 不能使用别名
- 除聚集计算语句外， SELECT 语句中的每个列都必须在 GROUP BY 子句中给出
- 如果分组列中具有 NULL 值，则 NULL 将作为一个分组返回。如果列中有多行 NULL 值，它们将分为一组
- GROUP BY 子句必须出现在 WHERE 子句之后， ORDER BY 子句之前
- 一般在使用 GROUP BY 子句时，应该也给出 ORDER BY 子句。这是保证数据正确排序的唯一方法

## 联结

### 使用 WHERE 创建等值联结

```text
SELECT vend_name, prod_name, prod_price
FROM vendors, products
WHERE vendors.vend_id = products.vend_id
ORDER BY vend_name, prod_name;

```

### 使用 INNER JOIN 创建等值联结

```text
SELECT vend_name, prod_name, prod_price
FROM vendors INNER JOIN products
ON vendors.vend_id = products.vend_id;

```

### 联结多个表

```text
SELECT vend_name, prod_name, prod_price
FROM vendors, products
WHERE vendors.vend_id = products.vend_id
    AND orderitems.prod_id = products.prod_id;

```

### 自联结

自联结通常作为外部语句用来替代从相同表中检索数据时使用的子查询语句。虽然最终的结果是相同的，但有时候处理联结远比处理子查询快得多。

```text
SELECT p1.prod_id, p1.prod_name
FROM products AS p1, producrs AS p2
WHERE p1.vend_id = p2.vend_id
AND p2.prod_id = 'DTNTR';

//等价于
SELECT prod_id, prod_name
FROM products
WHERE vend_id = (SELECT vend_id FROM products
                WHERE prod_id = 'DTNTR');

```

### 自然联结

无论何时对表进行联结，应该至少有一个列出现在不止一个表中（被联结的列）。标准的联结返回所有数据，甚至相同的列多次出现。 自然联结排除多次出现，使每个列只返回一次。

```text
//通配符只对第一个表使用。所有其他列明确列出，所以没有重复的列被检索出来
SELECT c.*, o.order_num, o.order_date, oi.prod_id, oi.quantity, OI.price
FROM customers AS c, orders AS o, orderitem AS oi
WHERE c.cust_id = o.cust_id
AND oi.order_num = o.order_num
AND prod_id = 'FB';

```

### 外部联结

许多联结将一个表中的行与另一个表中的行相关联。但有时候会需要包含没有关联行的那些行。例如，可能需要使用联结来完成以下工作：

- 对每个客户下了多少订单进行计数，包括那些至今尚未下订单的客户
- 列出所有产品以及订购数量，包括没有人订购的产品

```text
SELECT customers.cust_id, orders.order_num
FROM custormers, INNER JOIN orders
ON customers.cust_id = order.cust_id;

```

MySQL 不支持简化字符*=和=*的使用，这两种操作符在其他 DBMS 中是很流行的。
