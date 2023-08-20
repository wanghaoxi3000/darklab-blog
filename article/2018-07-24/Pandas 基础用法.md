---
date: "2018-07-24"
type: Post
category: Python
slug: pandas-basic-usage
tags:
  - Python模块包
  - Pandas
  - 科学计算
  - 数据分析
title: Pandas 基础用法
status: Published
urlname: 3009bc34-4eb9-4513-a0a9-fba6db5329c9
updated: "2023-07-17 14:41:00"
---

pandas 是一个基于 Numpy 构建, 强大的数据分析工具包

**主要功能**

- 独特的数据结构 DataFrame, Series
- 集成时间序列功能
- 提供丰富的数学运算操作
- 灵活处理缺失数据

### Series 一维数组

Series 是一种类似于一维数组的对象, 由一组数据和一组与之相关的数据标签(索引)组成

创建方式

```python
pd.Series([4, 7 ,5, -3])
pd.Series([4, 7 ,5, -3], index=['a', 'b', 'c', 'd'])
pd.Series({'a':1, 'b', 2})
pd.Series(0, index=['a', 'b', 'c', 'd'])

# 获取值数组
sr = pd.Series([4, 7 ,5, -3])
sr.value

# 获取索引数组
sr = pd.Series([4, 7 ,5, -3])
sr.index

```

### Series 支持 array 的特性(下标)

- 从 ndarry 创建 Series
- 与标量直接运算
- 两个 Series 运算
- 索引
- 切片
- 通用函数 np.abs(sr)
- 布尔值过滤 sr[sr>0]

### Series 支持字典的特性(标签)

- 从字典创建 Series Series(dict)
- in 运算
- 键索引

**整数索引**

如果索引是整数, 则根据下标取值时总是面向标签的.
此时可通过 **loc**方法(将索引解释为标签)和**iloc**方法(将索引解释为下标)

### Series 数据计算

```python
sr1 = pd.Series([12,23,34], index=['c', 'a', 'd'])
sr2 = pd.Series([11,20,10], index=['d', 'c', 'a'])
print(sr1 + sr2)
# 相关计算方法 add, sub, div, mul

```

pandas 在进行两个 Series 对象运算时, 会按索引进行对齐然后计算.

**数据对齐**

若两个 Series 对象的索引不完全相同, 则结果的索引是两个操作数索引的并集. 如果只有一个对象在某索引下有值, 则结果中该索引的值为 NaN.

**缺失数据处理办法**

```python
sr1.add(sr2, fill_value=0) 填充缺失的值
dropna() 过滤掉值为NaN的行
fillna() 填充缺失数据
isnull() 返回布尔数组, 缺失值对应为True
notnull() 返回buer数据, 缺失值对应为False

# 过滤缺失数据
sr.dropna()
sr[data.notnull()]

```

### DataFrame

DataFrame 是一个表格型的数据结构, 含有一组有序的列. 可以看做是 Series 组成的字典, 并且公用一个索引.

创建 DataFrame 的方法有很多种

```python
# 手动创建
pd.DataFrame({'one':[1,2,3,4], 'two':[4,3,2,1]})
pd.DataFrame({'one':pd.Series([1,2,3], index=['a','b', 'c']), 'two':pd.Series([1,2,3,4], index=['a','b','c','d'])

# 从csv文件读取与写入
df.read_csv('filename.csv')
df.to_csv()

```

### 常用属性

- index 获取索引
- T 转置
- columns 获取列索引
- values 获取值数组
- describe() 获取快速统计

### 索引和切片

DataFrame 是一个二维数据类型, 所以有`行索引`和`列索引`, 可以通过标签和位置两种方法进行索引和切片

- loc 索引方法和 iloc 下标方法
  - 使用方法: 逗号隔开, 前面是行索引, 后面是列索引
  - 行/列索引部分可以是常规索引, 切片, 布尔值索引, 花式索引任意搭配

### 数据对齐与缺失数据

DataFrame 对象在运算时, 同样会进行数据对齐, 其行索引和列索引分别对齐

处理缺失数据的相关方法

- dropna(axis=0, where='any', ...)
- fillna()
- isnull()
- notnull()

### pandas 常用方法

- mean(axis=0, skipna=False) 对列(行)求平均值
- sum(axis=1) 对列(行)求和
- sort_index(axis, ..., ascending) 对列(行)索引排序
- sort_values(by, axis, ascending) 按某一列(行)的值排序
- apply(func, axis=0) 将自定义函数应用在各行或各列上, func 可返回标量或 Series
- NumPy 的通用函数同样适用于 pandas
- applymap(func) 将函数应用在 DataFrame 各个元素上
- map(func) 将函数应用在 Series 各个元素上

### 时间处理

pandas 基于`dateutil`来处理时间对象

- `dateutil.parser.parse()` dateutil 原生时间处理方法
- `pd.to_datetime()` pandas 成组处理时间对象
- `data_range()` 产生时间对象数组
  - start 开始时间
  - end 结束时间
  - periods 时间长度
  - freq 时间频率, 默认为'D', 可选为 H(our), W(eek), B(usiness), S(emi-)M(onth), (min)T(es), S(econd), A(year)

### 时间序列

时间序列是以时间对象为索引的 Series 或 DataFrame, datetime 对象作为索引时是存储在 DatetimeIndex 对象中的.

时间序列的特色功能:

- 传入"年"或"年月"作为切片方式
- 传入日期范围作为切片方式
- 丰富的函数支持: resample(), strftime(), ...

### 文件处理

- `read_csv` 和 `read_table` 函数
  - sep 制定分隔符, 可用正则表达式如'\s+'
  - header = None 指定文件无列名
  - name 指定列名
  - index_col 指定某列为索引
  - skip_row 指定跳过某些行
  - na_values 指定某些字符串表示缺失值
  - parse_dates 指定某些列是否被解析为日期, 类型为布尔值或列表
- `to_csv` 函数
  - sep 指定文件函数
  - na_rep 指定缺失值转换的字符串, 默认为空字符串
  - header=False 不输出列名一行
  - index=False 不输出行索引一列
  - columns 指定输出的列, 传入列表
