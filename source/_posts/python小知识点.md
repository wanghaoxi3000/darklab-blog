---
title: python小知识点
date: 2016/12/10 17:03:00
categories:
- Python
toc: true
---

### 默认参数陷阱
```
def foo(a1, args = []):
    print "args before = %s" % (args)
    args.insert(0, 10)
    args.insert(0, 99999)
    print "args = %s " % (args)

def main():
    foo('a')
    foo('b')
```

输出:
```
args before = []
args = [99999, 10] 
args before = [99999, 10]
args = [99999, 10, 99999, 10] 
```
函数中的参数默认值是一个可变的list, 函数体内修改了原来的默认值，而python会将修改后的值一直保留，并作为下次函数调用时的参数默认值

Python manual中的说法:

**Default parameter values are evaluated when the function definition is executed.** This means that the expression is evaluated once, when the function is defined, and that that same “pre-computed” value is used for each call. This is especially important to understand when a default parameter is a mutable object, such as a list or a dictionary: if the function modifies the object (e.g. by appending an item to a list), the default value is in effect modified. This is generally not what was intended. A way around this is to use None as the default, and explicitly test for it in the body of the function, e.g.:
```
def whats_on_the_telly(penguin=None):
    if penguin is None:
        penguin = []
    penguin.append("property of the zoo")
    return penguin
```

参考:
> http://www.cnblogs.com/ukessi/archive/2010/01/25/python-function-default-parameter-value-problem.html

### is 和 ==
is 比较的是两个对象是否是同一个对象, == 比较两个对象的值是否一样.

### range 和 xrange
range可以返回一个可以用于所有目的的普通列表对象，而xrange将返回一个特殊目的的对象，尤其适用于迭代操作，但是xrange并不返回一个迭代器，如果需要这样一个迭代器，可以调用iter(xrange(x))。xrange返回的特殊目的对象比range返回的列表对象消耗较少的内存（范围比较大的时候）。但是对特殊目的对象执行循环操作的开销略微高于对列表执行循环的开销。
```
>>> print range(5)
[0, 1, 2, 3, 4]
>>> print xrange(5)
xrange(5)
```

### 强制访问私有属性
通过 实例化对象名._类名__私有属性名 可以强制访问私有属性