---
title: 国内镜像源
categories:
  - Linux管理
tags:
  - mirror
  - 镜像源
toc: true
date: 2020-06-16 19:50:00
slug: source-mirrors-change
---

国内的网络问题，经常需要替换软件本身的更新源，加快软件的下载速度。这里记录下常用国内镜像源。

主要使用阿里云镜像源服务：[https://developer.aliyun.com/mirror/](https://developer.aliyun.com/mirror/)

<!-- more -->

## Linux 系统

### Ubuntu

```
sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list
sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list
```

### Fedora

```
su
cd /etc/yum.repos.d/
mv fedora.repo fedora.repo.backup
mv fedora-updates.repo fedora-updates.repo.backup
wget -O /etc/yum.repos.d/fedora.repo http://mirrors.aliyun.com/repo/fedora.repo
wget -O /etc/yum.repos.d/fedora-updates.repo http://mirrors.aliyun.com/repo/fedora-updates.repo
dnf clean all
dnf makecache
```
