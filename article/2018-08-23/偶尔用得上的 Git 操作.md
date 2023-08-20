---
date: "2018-08-23"
type: Post
category: 软件工具
slug: sometimes-useful-git-skill
tags:
  - Git
title: 偶尔用得上的 Git 操作
status: Published
urlname: 64eee45b-1c09-4042-99bb-97164e113a1d
updated: "2023-07-13 14:17:00"
---

### Git 工作流

一个不错的工作流图示

![](../../images/04b7d37d8e2c6ee7f471ed3db1f136bd.jpg)

### 创建一个空分支

```text
git checkout --orphan 分支名
```

### 删除远程分支和 tag

```text
git push origin :<branchName>
git push origin --delete <branchName>
git push origin --delete tag <tagname>
```

### 同步删除远程已被删除的分支

```text
git fetch -p
# 或者使用：
git remote prune origin
```
