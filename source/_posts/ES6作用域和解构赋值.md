---
title: ES6作用域和解构赋值
date: 2017/7/12 11:43:00
categories:
- JavaScript
toc: true
---

ES6 强制开启严格模式

### 作用域

- var 声明局部变量，for/if花括号中定义的变量在花括号外也可访问
- let 声明的变量为块作用域，变量不可重复定义
- const 声明常量，块作用域，声明时必须赋值，不可修改


```
// const声明的k指向一个对象，k本身不可变，但对象可变

function test() {
    const k={
        a:1
    }
    k.b=3;
    
    console.log(k);
}

test()
```

### 解构赋值
```
{
    let a, b, 3, rest;
    [a, b, c=3]=[1, 2];

    console.log(a, b);
}
//output: 1 2 3

{
    let a, b, 3, rest;
    [a, b, c]=[1, 2];

    console.log(a, b);
}
//output: 1 2 undefined

{
    let a, b, rest;
    [a, b, ...rest] = [1, 2, 3, 4, 5, 6];
    console.log(a, b, rest);
}
//output:1 2 [3, 4, 5, 6]

{
    let a, b;
    ({a, b} = {a:1, b:2})

    console.log(a ,b);
}
//output: 1 2
```

#### 使用场景

##### 变量交换
```
{
    let a = 1;
    let b = 2;
    [a, b] = [b, a];
    console.log(a, b);
}
```

##### 获取多个函数值
```
{
    function f(){
        return [1, 2]
    }
    let a, b;
    [a, b] = f();
    console.log(a, b);
}
```

##### 获取多个函数返回值
```
{
    function f(){
        return [1, 2, 3, 4, 5]
    }
    let a, b, c;
    [a,,,b] = f();
    console.log(a, b);
}
//output: 1 4

{
    function f(){
        return [1, 2, 3, 4, 5]
    }
    let a, b, c;
    [a, ...b] = f();
    console.log(a, b);
}
//output: 1 [2, 3, 4, 5]
```

##### 对象解构赋值
```
{
    let o={p:42, q:true};
    let {p, q, c=5} = o;

    console.log(p ,q);
}
//output: 42 true 5
```

##### 获取json值
```
{
    let metaData={
        title: 'abc',
        test: [{
            title: 'test',
            desc: 'description'
        }]
    }
    let {title:esTitle, test:[{title:cnTitle}]} = metaData;
    console.log(esTitle, cnTitle);
}
//Output: abc test
```

