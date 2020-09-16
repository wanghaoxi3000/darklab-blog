---
title: 别名和类型再定义
categories:
  - Golang
tags:
  - Golang 基础
toc: true
date: 2020-09-16 20:50:00
---

Golang 语言中，我们可以用关键字`type`声明自定义的各种类型。在使用`type`时，声明的自定义类型有不同的区别。

<div style="text-align: center;">
    <img src="https://static-1256611153.file.myqcloud.com/img/picgo/20200916203327.png" width="640"/>
</div>
<!-- more -->


### 别名类型

```go
type MyString = string
```

这条语句表示，MyString是string类型的别名类型。别名类型与其源类型的区别只是在名称上，它们是完全相同的。源类型与别名类型是一对概念，是两个对立的称呼。别名类型主要是为了代码重构而存在的。详细的信息可参见 Go 语言官方的文档[Proposal: Type Aliases](https://golang.org/design/18130-type-alias)。

Go 语言内建的基本类型中就存在两个别名类型。`byte`是`uint8`的别名类型，而`rune`是`int32`的别名类型。


### 类型再定义

```go
type MyString2 string // 没有等号
```

这条语句表示，string类型再定义成了另外一个类型MyString2。这种方式也可以被叫做对类型的再定义。 **string可以被称为MyString2的潜在类型**。潜在类型的含义是，某个类型在本质上是哪个类型。

潜在类型相同的不同类型的值之间是可以进行类型转换的。因此，MyString2类型的值与string类型的值可以使用类型转换表达式进行互转。

但对于集合类的类型[]MyString2与[]string来说这样做却是不合法的，因为[]MyString2与[]string的潜在类型不同，分别是[]MyString2和[]string。另外，即使两个不同类型的潜在类型相同，它们的值之间也不能进行判等或比较，它们的变量之间也不能赋值。
