---
title: range 数组和切片的差异
date: 2020-10-13 00:19:00
categories:
  - Golang
tags:
  - Golang 基础
toc: true
slug: the-difference-of-range-array-and-slice
---

Go 语言的 range 表达式遵循如下两个规则：
1. range表达式只会在for语句开始执行时被求值一次，无论后边会有多少次迭代
2. range表达式的求值结果会被复制，也就是说，被迭代的对象是range表达式结果值的副本而不是原值
<!-- more -->

在使用 range 遍历数组和切片遇到需要修改遍历对象本身的情况时，便会出现差异。

### 遍历数组

```
package main

import "fmt"

func main() {
	numbers2 := [...]int{1, 2, 3, 4, 5, 6}
	maxIndex2 := len(numbers2) - 1
	for i, e := range numbers2 {
		if i == maxIndex2 {
			numbers2[0] += e
		} else {
			numbers2[i+1] += e
		}
	}
	fmt.Println(numbers2)
}

```

打印结果为：`[7 3 5 7 9 11]`。

range 循环中 e 并未随着数组改变，因为数组是值类型的。


### 遍历切片
```
package main

import "fmt"

func main() {
	numbers2 := []int{1, 2, 3, 4, 5, 6}
	maxIndex2 := len(numbers2) - 1
	for i, e := range numbers2 {
		if i == maxIndex2 {
			numbers2[0] += e
		} else {
			numbers2[i+1] += e
		}
	}
	fmt.Println(numbers2)
}

```

打印结果为：`[22 3 6 10 15 21]`。

range 循环中 e 并会随着数组改变而改变，因为切片是引用类型的。