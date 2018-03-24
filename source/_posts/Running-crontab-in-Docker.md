---
title: 在Docker中运行crontab
date: 2018/3/17 16:55:00
categories:
- Docker
toc: true
---

在把自己的项目通过Docker进行打包时，由于项目中用到了crontab，不过使用到的基础镜像`python:3.6-slim`并没有安装这项服务，记录下在镜像中安装和配置crontab的过程。

### Dockerfile
由于基础镜像中没有crontab服务，需要在打包自己镜像的Dockerfile中加入安装cron服务的步骤。

```Dockerfile
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

执行apt安装时注意加入`-y --no-install-recommends`，并且在安装完成后执行`rm -rf /var/lib/apt/lists/* && apt-get clean`命令，可以有效减小镜像的体积。

这样安装完cron服务后，crontab服务并不会自启动，还需要一个`docker-entrypoint.sh`启动脚本来添加crontab的启动命令。

### 启动脚本
```bash
#!/bin/bash
set -x

# 保存环境变量，开启crontab服务
env >> /etc/default/locale
/etc/init.d/cron start
```

`/etc/init.d/cron start`用于启动crontab服务，但这样启动的crontab服务中配置的定时命令是没有Dockerfile中设置的环境变量的。因此还需要在这之前执行`env >> /etc/default/locale`，这样有Dockerfile中通过`ENV`设置的环境变量在crontab中就可以正常读取了。
