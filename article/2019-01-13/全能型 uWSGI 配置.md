---
date: "2019-01-13"
type: Post
category: 软件工具
slug: versatility-uwsgi-config
tags:
  - Python
  - nginx
summary: 在进行 Python web 开发时，使用 Django、Flask 等框架开发完毕后，部署时通常需要选择一个支持 wsgi 协议的 Web 服务器程序。目前比较通用的选择是 nginx + uWSGI，使用 nginx 来处理静态文件请求，其余动态内容再转发给 uWSGI 交给 web 后台处理，网上这样的配置教程也是最多的。作为两款大名鼎鼎的服务器程序 nginx 负责静态文件，uWSGI 负责动态内容，各种在自己擅长的领域各施其职，的确效率很高，是高性能的 Python web 系统部署时的首选。不过有时用 Python 写了个小站点，性能需求并不高时。部署服务还要安装 nginx 和 uWSGI 两个服务器程序就显得有点麻烦了。能否把这些工作都交给一个服务器程序呢。
title: 全能型 uWSGI 配置
status: Published
urlname: 88579025-d6b7-43ae-98bb-12b52f90bcd9
updated: "2023-07-13 14:14:00"
---

## 全能型 uWSGI 配置

其实 uWSGI 也可以用来直接提供静态文件，虽然相比 nginx 效率要低一些，但部署时配置起来更为方便。只需在 uWSGI 的配置文件中添加 `static-map` 配置项。

### uWSGI 配置静态文件挂载点

通过 `--static-map mountpoint=path` 选项，uWSGI 即可将指定请求前缀映射到文件系统上的对应物理目录。

```text
--static-map /images=/var/www/img

```

通过以上配置，如接收到一个对 /images/logo.png 的请求，并且 /var/www/img/logo.png 存在，那么 uWSGI 将会提供它。否则，uWSGI 托管的应用会管理这个请求。

### uWSGI 配置路由

nginx 有时另外一个重要作用便是路由, uWSGI 在 1.9 版本后也提供了一个可编程的内部路由子系统，可以通过这个内部路由子系统来动态改变处理请求的方式。

例如将所有的 `http` 链接转到 `https` 地址下：

```text
route-uri = ^/$ redirect:<https://your.website.com>

```

### 完整配置

通过以上的选项，一个小站便可仅通过 uWSGI 部署起来了，顺便也分享下我的站点配置。

```text
[uwsgi]
; 特权端口只能通过 shared socket 来打开
shared-socket = 0.0.0.0:80
shared-socket = 0.0.0.0:443

; 打开 https 强制转换, 安全协议设置为 HIGH
http-to-https = =0
https = =1,214391966620557.pem,214391966620557.key,HIGH

; 在绑定端口后切换运行用户
uid = ubuntu
gid = ubuntu

; 配置运行虚拟环境及程序路径
virtualenv = /home/ubuntu/.virtualenvs/web/
chdir = /var/web/backend
wsgi-file = backend/wsgi.py
master = true
processes = 2
threads = 4
touch-reload=/var/web/backend/mcenter.reload

; 静态文件和路由配置
static-map = /static=/var/web/backend/static
route-uri = ^/$ redirect:<https://your.website.com>

; 开启状态监控
stats = 127.0.0.1:9191


```

## 参考资料

> 使用 uWSGI 提供静态文件 https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/StaticFiles.html  
> uWSGI 内部路由 https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/InternalRouting.html
