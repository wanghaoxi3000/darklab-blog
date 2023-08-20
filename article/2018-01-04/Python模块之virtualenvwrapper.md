---
date: "2018-01-04"
type: Post
category: Python
slug: virtualenvwrapper-of-the-python-module
tags: []
title: Python模块之virtualenvwrapper
status: Published
urlname: 961c038c-8f49-478d-8c61-68f679680da0
updated: "2023-07-17 14:42:00"
---

Python 的`virtualenv`工具可以创建隔离的 Python 环境， `virtualenvwrapper`是`virtualenv`的进一步封装工具，可以让它更好用。

### 安装

Linux 系统下：

> pip install virtualenvwrapper

Windows 系统下：

> pip install virtualenvwrapper-win

### 配置环境变量

- **WORKON_HOME** 虚拟 Python 环境的生成路径，不设置会默认生成在家目录的.virtualenvs 文件夹下
- **VIRTUALENVWRAPPER_PYTHON** 当系统存在多个版本的 python 时，需要设置这个环境变量指定 Python 版本

### 使用方法

### 激活环境

Linux 下首次安装后需要手动激活环境

> source /usr/local/bin/virtualenvwrapper.sh

可以加入到~/.bash_profile 之类的地方，以后登录系统使用时无需重复初始化了

### 创建环境

> mkvirtualenv <name>

### 列出已有虚拟环境

> lsvirtualenv

### 切换环境

> workon <name>

### 退出环境

> deactivate

### 删除虚拟环境

> rmvirtualenv <name>
