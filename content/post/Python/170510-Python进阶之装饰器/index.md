---
title: Python进阶之装饰器
date: 2017-05-10 22:46:00
categories:
- Python
toc: true
slug: Python-advanced-decorator
---

### 函数也是对象
要理解Python装饰器，首先要明白在Python中，函数也是一种对象，因此可以把定义函数时的函数名看作是函数对象的一个引用。既然是引用，因此可以将函数赋值给一个变量，也可以把函数作为一个参数传递或返回。同时，函数体中也可以再定义函数。

### 装饰器本质
可以通过编写一个纯函数的例子来还原装饰器所要做的事。
```
def decorator(func):
    
    def wrap():
        print("Doing someting before executing func()")
        func()
        print("Doing someting after executing func()")

    return wrap


def fun_test():
    print("func")


fun_test = decorator(fun_test)
fun_test()

# Output:
# Doing someting before executing func()
# func
# Doing someting after executing func()
```

1. `fun_test`所指向的函数的引用传递给`decorator()`函数
2. `decorator()`函数中定义了`wrap()`子函数，这个子函数会调用通过`func`引用传递进来的`fun_test()`函数，并在调用函数的前后做了一些其他的事情
3. `decorator()`函数返回内部定义的`wrap()`函数引用
4. `fun_test`接收`decorator()`返回的函数引用，从而指向了一个新的函数对象
5. 通过`fun_test()`调用新的函数执行`wrap()`函数的功能，从而完成了对`fun_test()`函数的前后装饰

### Python中使用装饰器
在Python中可以通过`@`符号来方便的使用装饰器功能。
```
def decorator(func):
    
    def wrap():
        print("Doing someting before executing func()")
        func()
        print("Doing someting after executing func()")

    return wrap

@decorator
def fun_test():
    print("func")


fun_test()

# Output:
# Doing someting before executing func()
# func
# Doing someting after executing func()
```

装饰的功能已经实现了，但是此时执行:
```
print(fun_test.__name__)

# Output:
# wrap
```
`fun_test.__name__`已经变成了`wrap`，这是应为`wrap()`函数已经重写了我们函数的名字和注释文档。此时可以通过`functools.wraps`来解决这个问题。`wraps`接受一个函数来进行装饰，并加入了复制函数名称、注释文档、参数列表等等功能。这可以让我们在装饰器里面访问在装饰之前的函数的属性。

更规范的写法：
```
from functools import wraps

def decorator(func):
    @wraps(func)
    def wrap():
        print("Doing someting before executing func()")
        func()
        print("Doing someting after executing func()")

    return wrap


@decorator
def fun_test():
    print("func")


fun_test()
print(fun_test.__name__)

# Output:
# Doing someting before executing func()
# func
# Doing someting after executing func()
# fun_test
```

### 带参数的装饰器
通过返回一个包裹函数的函数，可以模仿wraps装饰器，构造出一个带参数的装饰器。

```
from functools import wraps

def loginfo(info='info1'):
    def loginfo_decorator(func):
        @wraps(func)
        def wrap_func(*args, **kwargs):
            print(func.__name__ + ' was called')
            print('info: %s' % info)
            
            return func(*args, **kwargs)
        return wrap_func
    return loginfo_decorator
    
@loginfo()
def func1():
    pass
    
func1()

# Output:
# func1 was called
# info: info1

@loginfo(info='info2')
def func2():
    pass

func2()
# Output:
# func2 was called
# info: info2
```

### 装饰器类
通过编写类的方法也可以实现装饰器，并让装饰器具备继承等面向对象中更实用的特性

首先编写一个装饰器基类：
```
from functools import wraps

class loginfo:
    def __init__(self, info='info1'):
        self.info = info
        
    def __call__(self, func):
        @wrap
        def wrap_func(*args, **kwargs):
            print(func.__name__ + ' was called')
            print('info: %s' % self.info)
            
            self.after()    # 调用after方法，可以在子类中实现
            return func(*args, **kwargs)
        return wrap_func

    def after(self):
        pass


@loginfo(info='info2')
def func1():
    pass
    
# Output:
# func1 was called
# info: info1
```

再通过继承`loginfo`类，扩展装饰器的功能：
```
class loginfo_after(loginfo):
    def __init__(self, info2='info2', *args, **kwargs):
        self.info2 = info2
        super(loginfo_after, self).__init__(*args, **kwargs)

    def after(self):
        print('after: %s' % self.info2)


@loginfo_after()
def func2():
    pass

func2()
    
# Output:
# func2 was called
# info: info1
# after: info2
```
