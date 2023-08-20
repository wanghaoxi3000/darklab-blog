---
date: "2018-03-17"
type: Post
category: Docker
slug: running-crontab-in-docker
tags: []
title: 在Docker中运行crontab
status: Published
urlname: 3718ed3c-f70f-43ac-8eb2-51487ab5922c
updated: "2023-07-17 14:42:00"
---

在把自己的项目通过 Docker 进行打包时，由于项目中用到了 crontab，不过使用到的基础镜像`python:3.6-slim`并没有安装这项服务，记录下在镜像中安装和配置 crontab 的过程。

### Dockerfile

由于基础镜像中没有 crontab 服务，需要在打包自己镜像的 Dockerfile 中加入安装 cron 服务的步骤。

```docker
FROM python:3.6-slim
MAINTAINER whx3000 <wanghaoxi3000@163.com>

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    cron && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

RUN chmod +x ./docker-entrypoint.sh

ENV LC_ALL C.UTF-8
ENTRYPOINT ["./docker-entrypoint.sh"]

```

执行 apt 安装时注意加入`-y --no-install-recommends`，并且在安装完成后执行`rm -rf /var/lib/apt/lists/* && apt-get clean`命令，可以有效减小镜像的体积。

这样安装完 cron 服务后，crontab 服务并不会自启动，还需要一个`docker-entrypoint.sh`启动脚本来添加 crontab 的启动命令。

### 启动脚本

```bash
#!/bin/bash
set -x

# 保存环境变量，开启crontab服务
env >> /etc/default/locale
/etc/init.d/cron start

```

`/etc/init.d/cron start`用于启动 crontab 服务，但这样启动的 crontab 服务中配置的定时命令是没有 Dockerfile 中设置的环境变量的。因此还需要在这之前执行`env >> /etc/default/locale`，这样有 Dockerfile 中通过`ENV`设置的环境变量在 crontab 中就可以正常读取了。
