---
date: "2016-11-02"
type: Post
category: Linux编程
slug: linux-driven-development-basic-knowledge
tags: []
title: Linux驱动开发基础知识
status: Published
urlname: 0bd4d76f-8ce3-4f7a-9795-ec84b0b7b8ee
updated: "2023-07-17 15:13:00"
---

### 常用命令

- lsmod: list module,将模块列表显示)，功能是打印出当前内核中已经安装的模块列表
- insmod: install module，安装模块，功能是向当前内核中去安装一个模块，用法是 insmod xxx.ko
- modinfo: module information，模块信息，功能是打印出一个内核模块的自带信息。，用法是 modinfo xxx.ko
- rmmod: remove module，卸载模块，功能是从当前内核中卸载一个已经安装了的模块，用法是 rmmod xxx(注意卸载模块时只需要输入模块名即可，不需加.ko 后缀)
- mknod: 创建一个节点
- modprobe、depmod 等

### 常用宏

- MODULE_LICENSE: 模块的许可证. 一般声明为 GPL 许可证, 而且最好不要少, 否则可能会出现莫名其妙的错误(譬如一些明显存在的函数提升找不到).
- MODULE_AUTHOR: 声明模块作者, 可通过 modinfo 中查看
- MODULE_DESCRIPTION: 模块描述, 可通过 modinfo 中查看
- MODULE_ALIAS: 模块别名

### 驱动函数修饰符

- **init: 本质上是个宏定义，在内核源代码中就有#define **init xxxx. 这个**init 的作用就是将被他修饰的函数放入.init.text 段中去(本来默认情况下函数是被放入.text 段中), 整个内核中的所有的这类函数都会被链接器链接放入.init.text 段中，所以所有的内核模块的**init 修饰的函数其实是被统一放在一起的。内核启动时统一会加载.init.text 段中的这些模块安装函数，加载完后就会把这个段给释放掉以节省内存
- **exit: 类似于**init, 将函数链接进指定的段

### 调试信息

- printk(): 内核编程中使用 printk()来打印信息. printk 是 linux 内核源代码中自己封装出来的一个打印函数, 只能在内核源码范围内使用, 不能在应用编程中使用. 可设定 0-7 个打印级别, 一般默认为 4, 通过 dmesg 命令来查看.
- /proc/devices: 可查看到系统当前挂载的模块
