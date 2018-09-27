---
title: Python 内置方法
categories:
  - Python
tags:
  - Python基础知识
toc: true
date: 2018-09-27 22:40:49
---

### 迭代相关
- iter(): 将一个序列转换成迭代器
- next(): 自动调用对象的`__next__()`方法来迭代对象
- map(): 将一个序列值作为参数，依次调用一个函数，在python2中直接返回列表，但在python3中返回迭代器
```
# map经常配合lambdas来使用
items = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, items))

# 用于循环调用一列表的函数
def multiply(x):
        return (x*x)
def add(x):
        return (x+x)

funcs = [multiply, add]
for i in range(5):
    value = map(lambda x: x(i), funcs)
    print(list(value))

# Output:
# [0, 0]
# [1, 2]
# [4, 4]
# [9, 6]
# [16, 8]
```
- filter(): 过滤列表中的元素，并且返回一个由所有符合要求的元素所构成的列表，在python2中直接返回列表，但在python3中返回迭代器
```
number_list = range(-5, 5)
less_than_zero = filter(lambda x: x < 0, number_list)
print(list(less_than_zero))  

# Output: [-5, -4, -3, -2, -1]
```

- enumerate()：遍历数据并自动计数，并且有许多有用的可选参数
```
# 配置从哪个数字开始枚举
my_list = ['apple', 'banana', 'grapes', 'pear']
for c, value in enumerate(my_list, 1):
    print(c, value)

# 输出:
(1, 'apple')
(2, 'banana')
(3, 'grapes')
(4, 'pear')
```

- for-else
Python中for循环还有一个else从句，这个else从句会在循环正常结束时执行，因而可以常常搭配break来使用。
```
for item in container:
    if search_something(item):
        # Found it!
        process(item)
        break
else:
    # Didn't find anything..
    not_found_in_container()
```

### 对象自省
- dir()：返回一个列出了一个对象所拥有的属性和方法的列表，如果不传入参数，那么它会返回当前作用域的所有名字
- type()：返回一个对象的类型
- id()：返回任意不同种类对象的唯一ID


## 扩展
### functools
- Reduce()当需要对一个列表进行一些计算并返回结果时，Reduce 是个非常有用的函数。
```
from functools import reduce
product = reduce( (lambda x, y: x * y), [1, 2, 3, 4] )

# Output: 24
```
