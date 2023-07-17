---
title: JavaScript 函数
date: 2017-06-24 18:15:00
categories:
- JavaScript
toc: true
slug: JavaScript-function
---

### JavaScript 特点
#### 函数
- js函数的参数并不会验证传递进来多少个参数, 也不会在乎传进来的参数是什么数据类型, 在函数体内可以用arguments对象来访问这个参数数组.
- arguments对象中的值会与命名参数的值同步修改, 即修改arguments值时会同步修改参数的值, 反之亦然.
- js中函数没有重载
- Js中每个函数都是Function类型的实例，因而与其他引用类型一样具有属性和方法。
- 函数内部有两个特殊对象arguments和this
  - arguments.callee 指向拥有这个arguments对象的函数。可用于消除与函数名的紧耦合
  - arguments.caller 保存着调用当前函数的函数的引用
  - this 对象引用的是函数据以执行的环境对象
- 函数中包含两个属性length和prototype
  - length 表示函数希望接收的命名参数个数
  - prototype 保存函数所有实例方法的真正所在，例如toString()和valueOf()等
- 每个函数包含的方法：`apply()`、`call()`和`bind()`

```
function factorial(num) {
    if (num <= 1) {
        return 1;
    } else {
        return num * arguments.callee(num - 1); //factorial(num -1)
    }
}
```

```
function outer() {
    inner();
}
function inner() {
    alert(inner.caller);
}

outer(); //在警告窗中显示outer()的源代码
```

```
window.color = "red";
var o = {color: "blue"};

function sayColor() {
    alert(this.color);
}

sayColor()； //red

o.sayColor = sayColor;
o.sayColor(); //blue
```

#### JavaScript 的变量和作用域
- 基本类型的复制是完全独立的复制值复制, 引用类型的复制实际上是复制的一份指针.
- js中所有函数的参数都是按值传递, 基本类型传递如同基本类型变量复制一样, 引用类型传递如同引用变量复制一样.
- try-catch语句的catch快和with语句会延长作用域链
- js中没有块级作用域, for/if花括号中定义的变量在花括号外也可访问.

#### 引用变量
- Js中面向对象未实现面向对象的类和接口等基本结构，一般称为引用类型或对象定义。
- 访问对象的属性除了通用的`.`，还可使用`[]`，从而通过变量来访问对象属性。
- 为了便于操作基本类型值，Js提供了基本类型的自动包装功能，每单读取一个基本类型值的时候，后台就会创建一个对应的基本包装类型的对象，并在调用后自动销毁。
- 由于基本包装类型和基本类型的含义并不一样，会导致typeof等操作产生不同的结果，不推荐显示实例化基本数据类型

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

| | 函数声明 | 函数表达式 | 函数构造器 |
| ----------------- | ----- | ----- | - |
| 前置                | 是     |       |   |
| 允许匿名              |       | 是     | 是 |
| 可立即调用             |       | 是     | 是 |
| 在定义该函数的作用域通过函数名访问 | 是     |       |   |
| 没有函数名             |       |       | 是 |

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
