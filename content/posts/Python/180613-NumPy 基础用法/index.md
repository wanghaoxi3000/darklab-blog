---
title: NumPy 基础用法
categories:
  - Python
tags:
  - Python模块包 
  - Numpy
  - 科学计算
  - 数据分析
toc: true
date: 2018-06-13 00:16:38
slug: Numpy-basic-usage
---

NumPy 是高性能科学计算和数据分析的基础包. 它是 pandas 等其他各种工具的基础.

主要功能:
- ndarray 一个多维数组结构, 高效且节省空间
- 无需循环对整组数据进行快速运算的数学函数
- 线性代数, 随机数生成和傅里叶变换功能

### ndarry 多维数组
- 创建ndarry: `np.array(array_like)`
- 数组与列表的区别:
  - 数组对象类元素类型必须相同
  - 数组大小不可修改

### ndarry 常用属性
- T: 数组的转置
- size: 数组元素个数
- ndim: 数组的维数
- shape: 数组的维度大小(元组形式)
- dtype: 数组元素的数据类型

### ndarry 创建方法
- array() 将列表转为数组, 可选择显式指定 dtype 
- arange() range 的 numpy 版支持浮点数
- linspace() 类似 arange(), 第三个参数为数组长度
- zero() 根据指定形状和 dtype 创建全0数组
- ones() 根据指定形状和 dtype 创建全1数组
- empty() 根据指定形状和 dtype 创建空数组(内存随机值)
- eye() 根据指定边长和 dtype 创建单位矩阵

### ndarray 索引
- 一维数组索引 `a[5]`
- 多维数组索引 `a[2][3]`
- 新式写法 `a[2, 3]` (推荐)

- 对于一个数组, 选出其第1, 3, 4, 6, 7个元素, 组成新的二维数组: `a[[1,3,4,6,7]]`
- 布尔型索引, 选出所有大于5的偶数: `a[(a>5) & (a%2=0)]`
- 布尔型索引, 选出所有大于5的数和偶数: `a[(a>5) | (a%2=0)]`
- 对于一个二维数组, 选出其第一列和第三列, 组成新的二维数组: `a[:, [1, 3]]`

### ndarry 切片
- 一维数组的切片: 与列表类似
- 多维数组的切片: a[1:2, 3:4] a[:, 3:5] a[:, 1] (前行后列)
- 与列表切片的不同: 数组切片时并不会自动复制(而是创建一个视图), 在切片数组上的修改会影响原数组
- copy() 方法可以创建数组的深拷贝

### NumPy 通用函数
#### 浮点数特殊值
- nan(Not 啊Number) 不等于任何浮点数(nan != nan)
- inf(infinty) 比任何浮点数都大
- NumPy中创建特殊值 np.nan np.inf
- 在数据分析中, nan常被用做数据缺失值

#### 一元函数
**abs** **sqrt** exp log **ceil**(向上取整) **floor**(向下取整) **rint** **trunc** **modf** **isnan** **isinf** cos sin tan

#### 二元函数
add substract multiply divide power mod **maximum** **mininum**

#### 数学和统计方法
- sum 求和
- mean 求平均数
- std 求标准差
- var 求方差
- min 求最小值
- max 求方差
- argmin 求最小值索引
- argmax 求最大值索引

#### 随机数生成
- rand 给定形状产生随机数组(0到1之间的数)
- randin 给定形状产生随机整数
- choice 给定形状产随机选择
- shuffle 与random.shuffle相同
- uniform 给定形状产生随机数组
