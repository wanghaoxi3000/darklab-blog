---
title: Vi使用技巧
date: 2016-10-20 00:01:00
categories:
- Linux管理
toc: true
slug: Vi-skills
---

#### 复制剪切
- v：选择
- y：复制
- d：剪切
- p：粘贴

#### 查找
- /pattern<Enter>：向下查找pattern匹配字符串 
- ?pattern<Enter>：向上查找pattern匹配字符串 
- 使用了查找命令之后，使用如下两个键快速查找： 
- n：按照同一方向继续查找
- N：按照反方向查找

#### 撤销/重做
- u: 撤销上一个编辑操作
- ctrl + r: 回退前一个命令
- U: 行撤销，撤销所有在前一个编辑行上的操作

#### 多窗口编辑
- sp <File>: 打开一个新窗口
- Ctrl + w + 方向键: 窗口跳转, 使用方法为先按ctrl + w, 松开后再按下对应的方向键.