---
title: mac 系统找不到 clang 头文件
categories:
  - 软件工具
tags:
  - mac
toc: true
date: 2022-09-13T20:48:00+08:00
slug: clang-header-file-not-fuound-under-mac
description: 入手了一台 MacBook Air m2, 开始进入 MAC 的生态, 不过刚装好常用的开发环境, 在编译一个 golang 项目时就出现了一个找不到头文件的问题.
---

入手了一台 MacBook Air m2, 开始进入 MAC 的生态, 不过刚装好常用的开发环境, 在编译一个 golang 项目时就出现了一个问题:
```
runtime/cgo
_cgo_export.c:3:10: fatal error: 'stdlib.h' file not found
```

看起来是由于这个 golang 项目中使用到了 cgo 的库, 但是编译时没有找到对应的头文件导致了这个问题.

## 尝试过的方法
首先在网上搜索了一番, 大部分的解决方案是这些:
1. `xcode-select install` 通过此命令安装开发者工具
2. `ln -s /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include /usr/include/c++/v1` 添加软链接

不过这些方案在我的环境上都不可行, 我已经安装过了 xcode, 并且执行过 xcode-select install, 修改软链接的方式由于 Mac 的限制, 调整起来会很麻烦. 直到了 stackoverflow 的这篇回答提供了一个方便的解决方法.

## 解决方案
原文地址: https://stackoverflow.com/a/61526989/596599

简单的说, 出现这个问题的原因在于默认的编译器使用的是 XCode SDK 中的, 需要调整为 CommandLineTools SDK. 命令如下:

```
#Check the current sdk
xcrun --show-sdk-path

#Change sdk
sudo xcode-select -s /Library/Developer/CommandLineTools          #Using CommandLineTools SDK
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer   #Using XCode.app SDK
```
