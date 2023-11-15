---
date: "2023-11-15"
type: Post
category: Golang
slug: golang-use-functional-options-pattern-to-set-config
tags:
  - Golang 技法
summary: 在需要传递和初始化校验参数列表的时候使用这种方式来传递配置参数.
title: Golang 使用 Functional Options Pattern 传递参数
status: Published
urlname: afdb2f97-8c68-471a-b29f-cc0924862d04
updated: "2023-11-15 17:59:00"
---

在很多开源库中, 可以看到这种方式来传递配置参数, 如: zap、GRPC 等.

它经常用在需要传递和初始化校验参数列表的时候使用，比如我们现在需要初始化一个 HTTP server，里面可能包含了 port、timeout 等等信息，但是参数列表很多，不能直接写在函数上，并且我们要满足灵活配置的要求，毕竟不是每个 server 都需要很多参数。那么我们可以：

- 设置一个不导出的 struct 叫 options，用来存放配置参数；
- 创建一个类型  `type Option func(options *options) error`，用这个类型来作为返回值；

比如我们现在要给 HTTP server 里面设置一个 port 参数，那么我们可以这么声明一个 WithPort 函数，返回 Option 类型的闭包，当这个闭包执行的时候会将 options 的 port 填充进去：

```go
type options struct {
        port *int
}

type Option func(options *options) error

func WithPort(port int) Option {
                // 所有的类型校验，赋值，初始化啥的都可以放到这个闭包里面做
        return func(options *options) error {
                if port < 0 {
                        return errors.New("port should be positive")
                }
                options.port = &port
                return nil
        }
}
```

假如我们现在有一个这样的 Option 函数集，除了上面的 port 以外，还可以填充 timeout 等。然后我们可以利用 NewServer 创建我们的 server：

```go
func NewServer(addr string, opts ...Option) (*http.Server, error) {
        var options options
            // 遍历所有的 Option
        for _, opt := range opts {
                    // 执行闭包
                err := opt(&options)
                if err != nil {
                        return nil, err
                }
        }

        // 接下来可以填充我们的业务逻辑，比如这里设置默认的port 等等
        var port int
        if options.port == nil {
                port = defaultHTTPPort
        } else {
                if *options.port == 0 {
                        port = randomPort()
                } else {
                        port = *options.port
                }
        }

        // ...
}
```

初始化 server：

```go
server, err := httplib.NewServer("localhost",
                httplib.WithPort(8080),
                httplib.WithTimeout(time.Second))
```

这样写的话就比较灵活，如果只想生成一个简单的 server，我们的代码可以变得很简单：

```go
server, err := httplib.NewServer("localhost")
```
