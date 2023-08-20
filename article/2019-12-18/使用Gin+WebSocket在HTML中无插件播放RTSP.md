---
date: "2019-12-18"
type: Post
category: 项目架构
slug: use-gin-and-websocket-to-play-rtsp-video
tags:
  - Gin
  - WebSocket
  - RTSP
  - Go
summary: |-
  项目地址：gin-rtsp

  在后台的开发中遇到了对接显示摄像头视频流的需求。目前获取海康及大华等主流的摄像头的视频流使用的基本都是RTSP协议。不过HTML页面并不能直接播放RTSP协议的视频流，查询了一番各种网页播放RTSP的资料，有如下的一些方案：
title: 使用Gin+WebSocket在HTML中无插件播放RTSP
status: Published
urlname: 8456f952-9d1d-4ebd-8a23-542c69ba7d68
updated: "2023-07-17 14:32:00"
---

_项目地址：_[_gin-rtsp_](https://github.com/wanghaoxi3000/gin-rtsp)

在后台的开发中遇到了对接显示摄像头视频流的需求。目前获取海康及大华等主流的摄像头的视频流使用的基本都是 RTSP 协议。不过 HTML 页面并不能直接播放 RTSP 协议的视频流，查询了一番各种网页播放 RTSP 的资料，有如下的一些方案：

- 插件开发播放：使用 ActiveX 等浏览器插件的方式来播放，海康和大华的浏览器管理页面便是通过安装浏览器插件来播放视频的。视频播放稳定，延时短，但是对技术要求较高，对于 chrome 等现代浏览器也存在兼容性问题，并不想考虑。
- RTSP 转 HLS：使用 FFMPEG 将 RTSP 转为 HLS，推流到流服务器，如安装了`nginx-rtmp-module`模块的 nginx，用这个方案测试了下，HLS 协议在 PC 端和移动端的浏览器的播放都很稳，但是用 HLS 协议的直播流延时很大，至少有 15 秒左右，对于低延时视频的需求只能 PASS。
- RTSP 转 RTMP：与上一方案类似，使用 FFMPEG 将 RTSP 转为 RTMP 推到流服务器分发播放，相比 HLS 延时很低，本来已经准备使用这个方案了，但是前端使用的 video.js 库总是会偶现无法加载视频的问题，而且播放 RTMP 需要使用到 Flash，在 chrome 等浏览器中已经默认禁止加载逐步淘汰，只能抛弃。
- WebSocket：最终在万能的`Github`上翻到了一个[**JSMpeg**](https://github.com/phoboslab/jsmpeg/)项目，采用 FFMPEG 转为 MPEG1 Video 通过 WebSocket 代理推送到前端直接解码播放的方案。测试了下，延迟低，无需插件，画面质量也可以根据需要调整，效果很不错。

[**JSMpeg**](https://github.com/phoboslab/jsmpeg/)项目示例的 WebSocket 代理使用的是 JS，简单实现了单个视频源的播放功能。我们的后台使用的是 golang 的 Gin 框架，会有多个网页客户端播放多个视频流。好在看了下 JS 的代码，这个 WebSocket 代理的原理并不难，在 Gin 中集成 WebSocket 也很方便。这里记录下我的集成方案。

## 主要模块

- API 接口：接收 FFMPEG 的推流数据和客户端的 HTTP 请求，将客户端需要播放的 RTSP 地址转换为一个对应的 WebSocket 地址，客户端通过这个 WebSocket 地址便可以直接播放视频，为了及时释放不再观看的视频流，这里设计为客户端播放时需要在每隔 60 秒的时间里循环请求这个接口，超过指定时间没有收到请求的话后台便会关闭这个视频流。
- FFMPEG 视频转换：收到前端的请求后，启动一个 Goroutine 调用系统的 FFMPEG 命令转换指定的 RTSP 视频流并推送到后台对应的接口，自动结束已超时转换任务。
- WebSocket Manager：管理 WebSocket 客户端，将请求同一 WebSocket 地址的客户端添加到一个 Group 中，向各个 Group 广播对应的 RTSP 视频流，删除 Group 中已断开连接的客户端，释放空闲的 Group。

这里大致介绍下这三个主要模块的实现要点。

### API 接口

API 接收客户端发送的包含了需要播放 RTSP 流地址的 Json 数据，格式如：

```text
{
    "url":"rtsp://admin:admin@192.168.1.11:554/cam/realmonitor?channel=1&subtype=0"
}

```

在有多个客户端需要播放相同的 RTSP 流地址时，需要保证返回对应的 WebSocket 地址相同，这里使用了 UUID v3 来将 RTSP 地址散列化保证返回的地址相同。

[service/rtsptrans.go](https://github.com/wanghaoxi3000/gin-rtsp/blob/e19e6ccd39a8f720c1178b9c5b865cdbbbcd13f8/service/rtsptrans.go#L37)

```javascript
processCh := uuid.NewV3(uuid.NamespaceURL, splitList[1]).String()
playURL := fmt.Sprintf("/stream/live/%s", processCh)

```

FFMPEG 转换的视频数据也会通过 HTTP 协议传回服务端，每帧 byte 数据会以`'\n'`结束，在 go 语言中可以通过`bufio`模块来读出这样的数据。

[api/rtsp.go](https://github.com/wanghaoxi3000/gin-rtsp/blob/e19e6ccd39a8f720c1178b9c5b865cdbbbcd13f8/api/rtsp.go#L24)

```javascript
bodyReader := bufio.NewReader(c.Request.Body)

for {
	data, err := bodyReader.ReadBytes('\n')
	if err != nil {
		break
	}
}

```

### FFMPEG 视频转换

视频转换模块会在收到需要转换的 RTSP 流地址后，启动一个 FFMPEG 子进程来转换 RTSP 视频流，这里是使用`exec.Command`来完成：

[service/rtsptrans.go](https://github.com/wanghaoxi3000/gin-rtsp/blob/ae4ae486c002574161193fd8a7cb8b7dd15b8044/service/rtsptrans.go#L57)

```text
params := []string{
	"-rtsp_transport",
	"tcp",
	"-re",
	"-i",
	rtsp,
	"-q",
	"5",
	"-f",
	"mpegts",
	"-fflags",
	"nobuffer",
	"-c:v",
	"mpeg1video",
	"-an",
	"-s",
	"960x540",
	fmt.Sprintf("http://127.0.0.1:3000/stream/upload/%s", playCh),
}

cmd := exec.Command("ffmpeg", params...)
cmd.Stdout = nil
cmd.Stderr = nil
stdin, err := cmd.StdinPipe()

```

通过 FFMPEG 的 -q 和 -s 参数可以调试视频的质量和分辨率。为了简便，命令的 stdout 和 stderr 都赋值为了 nil，实际项目中可以保存到日志中方便排查问题。为了及时释放不再播放的资源，客户端停止请求超过一定时间后，FFMPEG 子进程会自动关闭，通过 golang 的 select 可以很方便的实现这个功能。

[service/rtsptrans.go](https://github.com/wanghaoxi3000/gin-rtsp/blob/ae4ae486c002574161193fd8a7cb8b7dd15b8044/service/rtsptrans.go#L94)

```text
for {
	select {
	case <-*ch:
		util.Log().Info("reflush channel %s rtsp %v", playCh, rtsp)

	case <-time.After(60 * time.Second):
		stdin.Write([]byte("q"))
		err = cmd.Wait()
		if err != nil {
			util.Log().Error("Run ffmpeg err:%v", err.Error)
		}
		return
	}
}

```

这里的`*ch` channel 通过一个 map 和每个子进程关联，子进程关闭时需要从 map 中清除，需要考虑并发的问题，可以使用`sync.Map`来保证线程安全。

### WebSocket Manager

WebSocket Manager 负责对页面上请求视频数据的 ws 客户端进行管理，在 Gin 中，主要是使用`github.com/gorilla/websocket`这个库来开发相关功能。**JSMpeg**库连接 WebSocket 时使用到了`Sec-WebSocket-Protocol`这个 header，需要对其处理：

```text
upgrader := websocket.Upgrader{
	// cross origin domain
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
	// 处理 Sec-WebSocket-Protocol Header
	Subprotocols: []string{ctx.GetHeader("Sec-WebSocket-Protocol")},
}
conn, err := upgrader.Upgrade(ctx.Writer, ctx.Request, nil)

```

ws 客户端连接后，会分配一个唯一的 UUID，放入到 URL 对应的 Group 中，相同 Group 下的客户端会收到同一视频流的数据。客户端断开连接后，需要从 Group 中删除，同时释放掉已经为空的 Group。这个过程同样需要考虑到并发的问题，WebSocket Manager 通过单独启动一个 Goroutine 监听注册，断开连接，广播的三个对应的 golang 的 channel，来统一管理各个 Group，可以很好的解决这个问题。具体实现在 [service/wsservice.go#L75](https://github.com/wanghaoxi3000/gin-rtsp/blob/ae4ae486c002574161193fd8a7cb8b7dd15b8044/service/wsservice.go#L75)，代码比较长就不贴了。

## 测试

项目需要运行在安装有 FFMPEG 程序的环境中。通过编写了一份 Dockerfile 已经封装好了需要的环境，可以使用 Docker build 后，以 Docker 的方式运行。

```text
$ docker build -t ginrtsp .
$ docker run -td -p 3000:3000 ginrtsp

```

### 使用内置的 FFMPEG 转换

将需要播放的 RTSP 流地址提交到 /stream/play 接口，例如：

```text
POST /stream/play
{
   "url": "rtsp://admin:password@192.168.3.10:554/cam/realmonitor?channel=1&subtype=0"
}

```

后台可以正常转换此 RTSP 地址时便会返回一个对应的地址，例如：

```text
{
    "code": 0,
    "data": {
        "path": "/stream/live/5b96bff4-bdb2-3edb-9d6e-f96eda03da56"
    },
    "msg": "success"
}

```

编辑`html`文件夹下 view-stream.html 文件，将 script 部分的 url 修改为此地址，在浏览器中打开，便可以看到视频了。

### 手动运行 FFMPEG

由于后台转换 RTSP 的进程在超过 60 秒没有请求后便会停止，也可以通过手动运行 ffmpeg 命令，来更方便地在测试状态下查看视频。

```text
ffmpeg -rtsp_transport tcp -re -i 'rtsp://admin:password@192.168.3.10:554/cam/realmonitor?channel=1&subtype=0' -q 0 -f mpegts -c:v mpeg1video -an -s 960x540 http://127.0.0.1:3000/stream/upload/test

```

通过如上命令，运行之后在 view-stream.html 文件的 url 中填入对应的地址为/stream/upload/test，在浏览器中打开查看视频。

显示效果

![](../../images/70e4d96b58b81fef1f40647cba84e126.png)

## 总结

得益于**JSMpeg**项目的强大，实现一个 WebSocket 的在网页上播放 RTSP 视频流还是很简单的了。随着 golang 语言日渐成熟，基于现成的库也可以方便的在 Gin 中添加 WebSocket 功能。需要注意主要是并发时，对 FFMPEG 子进程，WebSocket 客户端的增删问题，好在 golang 天生对并发有良好的支持，gouroutine，channel，sync 库这些 golang 核心知识掌握好了便可很好的应对这些问题。
