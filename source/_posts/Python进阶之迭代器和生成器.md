---
title: Python进阶之迭代器和生成器
date: 2017/5/6 01:20:00
categories:
- Python
toc: true
---

### 可迭代对象
Python中任意的对象，只要它定义了可以返回一个迭代器的`__iter__`方法，或者定义了可以支持下标索引的`__getitem__`方法，那么它就是一个可迭代对象。简单来说，可迭代对象就是能提供迭代器的任意对象，**但可迭代对象本身并不一定是一个迭代器**。

### 迭代器
任意对象，只要定义了`next`(Python2) 或者`__next__`方法，它就是一个迭代器。迭代完毕后继续调用`__next__`方法会产生一个`StopIteration`异常。for循环即通过自动捕捉这个异常来停止迭代的。

#### 相关内置函数
- iter()：可以自动根据一个可迭代对象返回一个迭代器对象。
- next()：可以自动调用迭代器的`__next__()`方法。

```
a = iter([1,2,3])
a.__next__()
next(a)
a.__next__()

# 输出:
1
2
3
```

### 生成器
生成器也是一种迭代器，但是只能对其迭代一次。通过使用“for”循环，或者传递给任意可以进行迭代的函数和结构来遍历它们。大多数时候生成器是以函数配合`yield`来实现的，可以将`yield`看成一种特殊的`return`，每次会顺序返回一个新值。

```
def func():
    yield 1
    yield 2
    yield 3

a = func()
a.__next__()
a.__next__()
a.__next__()

# 输出:
1
2
3
```

#### 生成器使用场景
因为它们并没有把所有的值存在内存中，而是在运行时生成值。因此特别适合不想同一时间将所有计算出来的大量结果集分配到内存当中时的场景，特别是当结果集里还包含循环的时候。

```
# 计算斐波那契数列的生成器
def fibon(n):
    a = b = 1
    for i in range(n):
        yield a
        a, b = b, a + b
        
for x in fibon(1000000):
    print(x)
```

### 总结
了解完以上知识后，以一段综合代码进行下总结。

```
# Fei类中实现了__iter__方法，成为一个可迭代的类
class Fei:

    @staticmethod
    # 计算斐波那契数列的生成器
    def fibon(n):
        a = b = 1
        for i in range(n):
            yield a
            a, b = b, a + b

    # 返回一个计算前100斐波那契数列的生成器
    def __iter__(self):
        return Fei.fibon(100)

a = Fei()

# 使用for循环来遍历Fei类对象a
for i in a:
    print(i)
```
