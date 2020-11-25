---
title: Go-Advance 总结
categories:
  - Golang
tags:
  - Golang 基础
toc: true
date: 2020-11-25 16:38:00
---


看完了 [go-advice](https://github.com/cristaloleg/go-advice), 记录下一些要点和自己值得注意的地方。

<!-- more -->

## Go 箴言

*   不要通过共享内存进行通信，通过通信共享内存
*   并发不是并行
*   通道编排；互斥体序列化
*   接口越大，抽象就越弱
*   使零值有用
*   `interface{}` 什么也没说
*   Gofmt 的风格不是人们最喜欢的，但 gofmt 是每个人的最爱
*   一点点复制比一点点依赖更好
*   系统调用必须始终使用构建标记进行保护
*   必须始终使用构建标记保护 Cgo
*   Cgo 不是 Go
*   对于不安全的 package，没有任何保证
*   清楚比聪明更好
*   反射永远不清晰
*   错误就是价值观
*   不要只检查错误，还要优雅地处理它们
*   设计架构，命名组件，记录细节
*   文档是供用户使用的
*   不要恐慌

Author: Rob Pike See more: [https://go\-proverbs.github.io/](https://go-proverbs.github.io/)


## Go 之禅

*   每个 package 实现单一的目的
*   显式处理错误
*   尽早返回，而不是使用深嵌套
*   让调用者选择并发
*   在启动一个 goroutine 时，需要知道何时它会停止
*   避免 package 级别的状态
*   简单很重要
*   编写测试以锁定 package API 的行为
*   如果你觉得慢，先编写 benchmark 来证明
*   节制是一种美德
*   可维护性

Author: Dave Cheney See more: [https://the\-zen\-of\-go.netlify.com/](https://the-zen-of-go.netlify.com/)

## 代码

#### 用 `chan struct{}` 来传递信号, `chan bool` 表达的不够清楚

刚开始使用Go时，需要使用chan来传递一个信号时，并没有一个明确的约束，`chan int`，`chan bool`等，都在使用。

但使用`struct{}`时是最推荐的，字面量struct{}代表了空的结构体类型，空结构体类型变量不占内存空间，内存地址相同，既不包含任何字段也没有任何方法。该类型的值所需的存储空间几乎可以忽略不计。相比其他类型，也可以一目了然是用来传递信号的。

#### 30 * time.Second 比 time.Duration(30) * time.Second 更好

需要将无类型的 const 包装在类型中，编译器会找出来。最好将 const 移到第一位：

```go
// BAD
delay := time.Second * 60 * 24 * 60

// VERY BAD
delay := 60 * time.Second * 60 * 24

// GOOD
delay := 24 * 60 * 60 * time.Second
```

#### 用 a := []T{} 来简单初始化 slice

相比 `make` 这样的写法更快捷，可以借鉴。

#### 从一个 slice 生成简单的随机元素

```go
[]string{"one", "two", "three"}[rand.Intn(3)]
```