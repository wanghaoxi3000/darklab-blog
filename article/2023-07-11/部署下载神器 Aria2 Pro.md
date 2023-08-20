---
date: "2023-07-11"
type: Post
category: 软件工具
slug: deploy-download-tool-aria2-pro
tags:
  - aria2
summary: 几年前刚搭建了黑群晖时，在群晖的 docker 中跑了一个网友改造的 aria2 下载器，包含了一个已经配置好的 aria2 内核和一个 AriaNG 控制页面。之后应该是一次也没更新过，如今这个 aria2 下载器下载BT种子的话已经基本没有任何速度。AriaNG 页面也落后了很多个版本了。想着更新一下，因此发现了这个项目：Aria2-Pro-Docker 。
title: 部署下载神器 Aria2 Pro
status: Published
urlname: c370350a-d366-45a1-b383-b5056de0e7b0
updated: "2023-07-19 01:11:00"
---

几年前刚搭建了黑群晖时，在群晖的 docker 中跑了一个网友改造的 aria2 下载器，包含了一个已经配置好的 aria2 内核和一个 AriaNG 控制页面。之后应该是一次也没更新过，如今这个 aria2 下载器下载 BT 种子的话已经基本没有任何速度。AriaNG 页面也落后了很多个版本了。想着更新一下，因此发现了这个项目：[Aria2-Pro-Docker](https://github.com/P3TERX/Aria2-Pro-Docker) 。

## 简介

简单摘录下 Aria2 Pro 的介绍

> 很多人在初次使用 Aria2 时会遇到 BT 下载无速度、文件残留占用空间、任务丢失等问题，所以会觉得 Aria2 并不好用，但事实并非如此。[Aria2 完美配置](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL1AzVEVSWC9hcmlhMi5jb25m)是博主经过长时间使用和研究官方文档后总结出来的一套配置方案，其最初目的是为了解决这些问题，而且为 Aria2 添加了额外的一些功能，经过一年多时间的打磨已经积累了大量的使用者和良好的口碑，其中不乏一些知名开源项目开发者、影视字幕组、科技视频 UP 主。之前一直使用[一键脚本](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL1AzVEVSWC9hcmlhMi5zaA)作为部署方案，为了满足小伙伴们使用 Docker 部署的需求，博主特意制作了基于 Aria2 完美配置和特殊定制优化的 Aria2 Docker

有关 Aria2 Pro 的详细介绍可以参看作者的说明页面：

[bookmark](https://p3terx.com/archives/docker-aria2-pro.html)

## 部署

按照作者的文档，部署的步骤也是比较简单的，Docker 或者 Docker compose 的方式可以直接参考作者的文档，这次我是部署到了家中的 K8S 来统一管理。主要配置了这些参数:

- 环境变量
  - RPC_SECRET: RPC 连接秘钥
  - RPC_PORT: RPC 端口，默认为 6800
  - LISTEN_PORT: BT 监听端口（TCP）、DHT 监听端口（UDP），默认为 6888
  - DISK_CACHE: 磁盘缓存设置，默认值 64M。建议在有足够的内存空闲情况下设置为适当增加大小，以减少磁盘 I/O ，提升读写性能，延长硬盘寿命。我的环境中改为了 256M。
- 暴露端口
  - TCP
    - 6800 RPC 连接端口
    - 6888 BT 监听端口
  - UDP
    - 6888 DHT 监听端口
  - 存储
    - /config 配置路径
    - /downloads 下载路径

存储挂载的数据卷使用了 NFS 来挂载群晖上的磁盘

```yaml
volumeMounts:
- mountPath: /config
  name: volume-nfs
  subPath: aria2/config
- mountPath: /downloads
  name: volume-nfs
	subPath: aria2/downloads

volumes:
  - name: volume-nfs
    nfs:
      path: /volume2/k8s
      server: server ip
```

## 使用

Aria2 Pro 只包含了 aria2 内核，没有控制页面，我一般使用的是 [AriaNg](https://github.com/mayswind/AriaNg)，可以自行搭建，也可以使用作者的 Demo 页面：[http://ariang.mayswind.net/latest](http://ariang.mayswind.net/latest)

Aria2 Pro 也提供了两个可以直接使用的页面：

| 链接                                                                      | 备注                                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [http://ariang.js.org](https://p3terx.com/go/aHR0cDovL2FyaWFuZy5qcy5vcmc) | [js.org](https://p3terx.com/go/aHR0cHM6Ly9qcy5vcmcv)  提供域名，[GitHub Pages](https://p3terx.com/go/aHR0cHM6Ly9wYWdlcy5naXRodWIuY29tLw)  提供网页服务                                                                                           |
| [http://ariang.eu.org](https://p3terx.com/go/aHR0cDovL2FyaWFuZy5ldS5vcmc) | [eu.org](https://p3terx.com/go/aHR0cHM6Ly9uaWMuZXUub3JnLw)  提供域名，[GitHub Pages](https://p3terx.com/go/aHR0cHM6Ly9wYWdlcy5naXRodWIuY29tLw)  提供网页服务，[Cloudflare](https://p3terx.com/go/aHR0cHM6Ly93d3cuY2xvdWRmbGFyZS5jb20v)  提供 CDN |

任选一个，启用了 https 的话可以方法以上两个链接的 https 页面，配置上服务器地址和密钥，即可正常使用了。试了下一些常用资源，速度都还不错，准备作为我新的日常下载工具啦。
