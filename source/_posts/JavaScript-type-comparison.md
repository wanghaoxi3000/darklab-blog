---
title: JavaScript类型比较
date: 2017/6/2 20:40:00
categories:
- JavaScript
toc: true
---

### JavaScript的类型
原始类型：

- number
- string
- boolean
- null
- undefined

对象类型：

- Object
  - function
  - Array
  - Date
  - ...

### 隐式转换
#### `+/-` 运算
- "37" + 7 = "377"
- "37" - 7 = 30

#### `==` 运算
以下为true：
- "1.23" == 1.23
- 0 == false
- null == undefined

### 比较运算
#### `===`严格等于
- 类型不同，返回false
- 类型相同，以下为true：
  - null === null
  - undefine === null
  - NaN != NaN
  - new Object != new Obejct

#### `==`等于
- 类型相同，同`===`
- 类型不同，尝试类型转换比较
  - null == undefined
  - number == string 转number
  - boolean == ? 转number
  - Object == number | string 尝试对象转换为基本类型
  - 其他：false

### 包装类型
为了便于操作基本类型值，Js提供了基本类型的自动包装功能，每单读取一个基本类型值的时候，后台就会创建一个对应的基本包装类型的对象，并在调用后自动销毁。

由于基本包装类型和基本类型的含义并不一样，会导致typeof等操作产生不同的结果，不推荐显示实例化基本数据类型

```
var a = "string";
alert(a.length);    //6

a.t = 3;
alert(a.t);         //undefined
```

### 类型检测
#### typeof
以下为true：
```
typeof 100 === “number”
typeof true === “boolean”
typeof function () {} === “function”
typeof(undefined) ) === “undefined”
typeof(new Object() ) === “object”
typeof( [1， 2] ) === “object”
typeof(NaN ) === “number”   //NaN也为number
typeof(null) === “object”
```

#### instanceof
`obj instanceof Object`  利用原型链进行判断，适用于对象间判断。它期望左边是一对象，右边是函数对象或函数构造器。

以下为true：
```
[1, 2] instanceof Array === true
new Object() instanceof Array === false
```

#### Object.prototype.toString.apply()
```
Object.prototype.toString.apply([]); === “[object Array]”;
Object.prototype.toString.apply(function(){}); === “[object Function]”;
Object.prototype.toString.apply(null); === “[object Null]”
Object.prototype.toString.apply(undefined); === “[object Undefined]”

// IE6/7/8 Object.prototype.toString.apply(null) 返回”[object Object]”

```

### 小结
- typeof
适合基本类型及function检测，遇到null失效。

- [[Class]]
通过{}.toString拿到，适合内置对象和基元类型，遇到null和undefined失效(IE678等返回[object Object])。

- instanceof
适合自定义对象，也可以用来检测原生对象，在不同iframe和window间检测时失效。

