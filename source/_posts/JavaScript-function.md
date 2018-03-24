---
title: JavaScript函数
date: 2017/6/24 18:15:00
categories:
- JavaScript
toc: true
---

### 函数的调用

- 直接调用 foo();
- 对象方法 o.method();
- 构造器 new Function();
- call/apply/bind func.call(o);

### 函数声明和表达式

函数声明会被前置，函数表达式变量声明会被前置，但是值为`undefined`。

#### 函数声明
```
function func(a, b) {
    //do sth
}
```

#### 函数表达式
- 将函数赋值给一个变量
```
var func = function(a, b) {
    //do sth
};
```

- 匿名函数(IEF 立即执行函数表达式)
```
(function() {
    //do sth
})();
```

- 返回函数对象
```
return function() {
    //do sth
};
```

- 命名函数表达式(NEF)
```
var add = function foo(a, b) {
    //do sth
};
```

命名函数表达式存在一些经典的bug，例如在执行如下代码时：
```
var func = function nfe() {};
alert(func == nfe);
```
IE6会提示为`false`，IE9+中nfe外部并不可见，提示为`nfe is undefined`。

命名函数表达式主要可以应用在调试和递归调用时。
```
var func = funtion nfe(){/* do sth */ nfe();};
```
但也可直接通过`func`变量名来执行递归调用，因此命名函数表达式并不常用。

### function构造器
```
var func = new Function('a', 'b', 'console.log(a + b);');
func(1, 2); //3

var func = Function('a', 'b', 'console.log(a + b);');
func(1, 2)  //3
```

#### function构造器的作用域

```
Function('var localVal = "local"; console.log(localVal);')();
console.log(typeof localVal);
// result: local, undefined
// localVal仍未局部变量

var globalVal = 'global';
(function() {
    var localVal = 'local';
    Function('console.log(typeof localVal, typeof globalVal);')();
})();
//result: undefined, string
//local不可访问，全局变量global可以访问
```

### 各方式对比


| | 函数声明 | 函数表达式 | 函数构造器
---|---|---|---|
前置 | 是 |
允许匿名 | | 是 | 是 |
可立即调用 | | 是 | 是 |
在定义该函数的作用域通过函数名访问 | 是 |
没有函数名 | | | 是 |

### this

#### 全局的this
全局的this一般即是浏览器
```
console.log(this.document === document); //true
consloe.loh(this == window);    //true

this.a = 37
console.log(window.a);  //37
```

#### 一般函数的this
一般函数的this仍然指向全局对象，浏览器中即为window
```
fucntion f1(){
    return this;
}

f1() === window;    //true, global, object
```

严格模式下，this指向undefined
```
fucntion f2(){
    "use strict";
    return this;
}

f2() === undefined; //true
```

#### 作为对象方法的函数this
对象方法中的函数this会指向具体的对象
```
var o = {
    prop: 37;
    f: function() {
        return this.prop;
    }
};

console.log(o.f()); //logs 37
```

也可以通过外部定义函数
```
var o = {prop: 37};
function independent() {
    return this.prop;
}

o.f = independent
console.log(o.f()); //logs 37
```

#### 通过`call`和`apply`调用指定this
```
function add(c, d) {
    return this.a + this.b + c + d;
}

var o = {a:1, b:3};

add.call(o, 5, 7);  // 1 + 3 + 5 + 7 = 16 
add.apply(o, [10, 20]); //1 + 3 + 10 + 20 = 34


function bar() {
    console.log(Object.prototype.toString.call(this));
}

bar.call(7);    //"[object Number]"
```

一般模式和严格模式下使用`apply`的区别
```
function foo(x, y) {
    console.log(x, y, this);
}

foo.apply(null);    // undefined, undefined, window
foo.apply(undefined);    // undefined, undefined, window

// 严格模式下
foo.apply(null);    // undefined, undefined, null
foo.apply(undefined);    // undefined, undefined, undefined
```

#### 'bind'方法与this
通过ES5提供的bind方法，可以将函数的this绑定到一个对象上，bind之后this不可变。
```
function f(){
    return this.a
}

var g = f.bind({a: "test"}):
console.log(g());   //test

var o = {a: 37, f:f, g:g};
// g()中的this不会再改变
console.log(o.f(), o.g());  //37, test
```

### 函数属性和对象
```
function foo(x, y, z) {
    
    arguments.length;   //2
    arguments[0];   //1
    arguments[0] = 10;
    x;  // change to 10; 严格模式下仍然是1
    
    arguments[2] = 100;
    z;  // still undefined !!!
    arguments.callee === foo;   // true 严格模式下不能使用
}

foo(1, 2)
foo.length;     // 3
foo.name;       // "foo"
```

使用`bind()`方法currying函数
```
function add(a, b, c) {
    return a + b + c;
}

var func = add.bind(undefined, 100);
func(1, 2); // 100绑定到a上，result：103

var func2 = func.bind(undefoned, 200);
func2(10);  // 200绑定到b上，result：310
```

bind和new的使用
```
function foo() {
    this.b =100;
    return this.a;
}

var func = foo.bind({a:1});

func(); // 1
// 使用new时，除非指定返回一个对象，否则会返回this，
// 同时this会被初始化为一个空对象的prototype
new func(); //{b: 100}
```
