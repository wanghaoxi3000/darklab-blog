---
date: "2016-10-20"
type: Post
category: Linux管理
slug: vi-skills
tags: []
title: Vi使用技巧
status: Published
urlname: d749a6fa-bee2-4c5a-a28d-33ba1c9e9d46
updated: "2023-07-17 15:12:00"
---

### 复制剪切

- v：选择
- y：复制
- d：剪切
- p：粘贴

### 查找

- /pattern<Enter>：向下查找 pattern 匹配字符串
- ?pattern<Enter>：向上查找 pattern 匹配字符串
- 使用了查找命令之后，使用如下两个键快速查找：
- n：按照同一方向继续查找
- N：按照反方向查找

### 撤销/重做

- u: 撤销上一个编辑操作
- ctrl + r: 回退前一个命令
- U: 行撤销，撤销所有在前一个编辑行上的操作

### 多窗口编辑

- sp <File>: 打开一个新窗口
- Ctrl + w + 方向键: 窗口跳转, 使用方法为先按 ctrl + w, 松开后再按下对应的方向键.
