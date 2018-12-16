---
title: 偶尔用得上的 Git 操作
categories:
  - 软件工具
tags:
  - Git
toc: true
date: 2018-08-23 23:02:46
---

### Git 工作流
一个不错的工作流图示

![](https://darkreunion-1256611153.file.myqcloud.com/img/gitworkflow.jpg)

### 创建一个空分支
```
git checkout --orphan 分支名
```

### 删除远程分支和tag
```
git push origin :<branchName>
git push origin --delete <branchName>
git push origin --delete tag <tagname>
```

### 同步删除远程已被删除的分支
```
git fetch -p
# 或者使用：
git remote prune origin
```
