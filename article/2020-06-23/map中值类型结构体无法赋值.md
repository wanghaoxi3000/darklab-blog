---
date: "2020-06-23"
type: Post
category: Golang
slug: the-value-type-struct-of-map-cannot-assign
tags:
  - Golang 基础
summary: 在Golang中，当一个map的value为一个值类型的结构体时，是不能对其赋值的，修改结构体的数值的。
title: map中值类型结构体无法赋值
status: Published
urlname: de496bfb-9b9d-4b57-8faa-d40e479c7d41
updated: "2023-07-17 11:29:00"
---

在 Golang 中，当一个 map 的 value 为一个值类型的结构体时，是不能对其赋值的，修改结构体的数值的。

### 示例代码

```javascript
package main

import "fmt"

type person struct {
	name string
	age  int
	sex  string
}

func main() {
	//建立结构体map
	s := make(map[int]person)

	//给map赋值
	s[1] = person{"tony", 20, "man"}
	fmt.Println(s[1])

	//修改map里结构体的成员属性的值
	s[1].name = "tom" // cannot assign to struct field s[1].name in map
	fmt.Println(s[1].name)
}

```

以上代码在对`s[1]`的结构体执行赋值操作`s[1].name = "tom"`时，便会产生`cannot assign to struct field s[1].name in map`的错误。

### 错误原因

- `x = y` 这种赋值的方式，你必须知道 `x`的地址，然后才能把值 `y` 赋给 `x`。
- 但 `go` 中的 `map` 的 `value` 本身是不可寻址的，因为 `map` 的扩容的时候，可能要做 `key/val pair`迁移，`value` 本身地址是会改变的
- `value`不支持寻址，因而无法赋值

### 解决方法

在需要对 map 中结构体进行赋值修改的操作时，需要在 map 中保存结构体的地址，这时便可以赋值了。

```text
package main

import "fmt"

type person struct {
	name string
	age  int
	sex  string
}

func main() {
	//建立结构体map，声明为结构体地址
	s := make(map[int]*person)

	//给map赋值
	s[1] = &person{"tony", 20, "man"}
	fmt.Println(s[1])

	//修改map里结构体的成员属性的值
	s[1].name = "tom"
	fmt.Println(s[1].name)
}


```
