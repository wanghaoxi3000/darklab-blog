---
date: "2020-10-01"
type: Post
category: Golang
slug: run-goroutine-by-ordered
tags:
  - Golang 基础
summary: Golang 中 goroutine 中的运行是无序的，如果要让多个 goroutine 顺序执行，例如每个 goroutine 在并行执行时顺序打印 0-9，这里记录一种通过 atomic 包的原子操作来实现的方法。
title: 多个goroutine按既定顺序运行
status: Published
urlname: 5254d509-659c-488c-9fc6-28b07901dd5d
updated: "2023-07-17 11:24:00"
---

Golang 中 goroutine 中的运行是无序的，如果要让多个 goroutine 顺序执行，例如每个 goroutine 在并行执行时顺序打印 0-9，这里记录一种通过 `atomic` 包的原子操作来实现的方法。

```go
package main

import (
	"fmt"
	"sync/atomic"
	"time"
)

func ParallelPrintOrderdNum() {
	var count uint32

	trigger := func(i uint32, fn func()) {
		for {
			if n := atomic.LoadUint32(&count); n == i {
				fn()
				atomic.AddUint32(&count, 1)
				break
			}
			// sleep 等代，让此 goroutine 有被调度的机会
			time.Sleep(time.Nanosecond)
		}
	}

	for i := uint32(0); i < 10; i++ {
		go func(i uint32) {
			fn := func() {
				fmt.Println(i)
			}
			trigger(i, fn)
		}(i)
	}

    // 主 goroutine 也需要等待
	trigger(10, func() {})
}

func main() {
	ParallelPrintOrderdNum()
}

```
