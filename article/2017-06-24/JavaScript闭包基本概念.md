---
date: "2017-06-24"
type: Post
category: JavaScript
slug: the-basic-concept-of-javascript-closure
tags: []
title: JavaScript闭包基本概念
status: Published
urlname: 8810277f-eb6e-41cc-9ff1-022d45838b09
updated: "2023-07-17 15:03:00"
---

### 闭包的概念

维基百科中是这么解释闭包的：

- 计算机科学中，闭包(也称为词法闭包或函数闭包)是指一个函数或函数的引用，与一个引用环境绑定在一起。这个函数环境是一个存储该函数每个非局部变量(也叫自由变量)的表。
- 闭包，不同意一般函数，它允许一个函数在立即词法作用域外调用时，认可访问非本地变量。

### 闭包的例子

### 使用闭包

```javascript
function outer() {
  var localVal = 30;
  return function () {
    return localVal;
  };
}

var func = outer();
func();
```

outer 函数调用结束后，func 函数仍能访问外层的局部变量，即为闭包。

应用闭包，在前端编程中添加点击事件:

```javascript
!(function () {
  var localData = "localData here";
  document.addEventListener("click", function () {
    console.log(localData);
  });
})();
```

### 循环闭包错误

```javascript
document.body.innerHTML = "<div id=div1>aaa</div>"
    + "<div id=div2>bbb</div><div id=div3>ccc</div>";
for(var i=1; i<4; i++) {
    document.getElementById('div' + i).
        addEventListener('click', function() {
            alert(i);   // all are 4!
        }
}
```

因为 i 在发生点击事件时才会访问，以上例子中，全部点击事件均会提示 4。

解决办法：

```javascript
document.body.innerHTML = "<div id=div1>aaa</div>"
    + "<div id=div2>bbb</div><div id=div3>ccc</div>";
for(var i=1; i<4; i++) {
    !function(i) {
        document.getElementById('div' + i).
            addEventListener('click', function() {
                alert(i);   // all are 4!
            }
    }(i)
}
```
