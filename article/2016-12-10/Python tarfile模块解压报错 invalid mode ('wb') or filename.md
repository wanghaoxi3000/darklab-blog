---
date: "2016-12-10"
type: Post
category: Python
slug: python-tarfile-module-unzip-invalid-mode-('wb')-or-filename
tags: []
title: Python tarfile模块解压报错 invalid mode ('wb') or filename
status: Published
urlname: 351382cf-57e4-4fd1-a59b-2e95dc07fd20
updated: "2023-07-17 15:11:00"
---

### 问题原因

在使用 tarfile 模块解压一份 Linux 服务器上的打包文件时, 出现了错误提示: IOError: [Errno 22] invalid mode ('wb') or filename.
经过检查, 发现是因为打包文件中有文件名存在':'符号, 而 window 下的文件名是不能有':'符号的因而报错.

### 解决办法

通过搜索, 找到了种解决办法, 可以将解压时含':'的地方转换成'\_'等正常的符号

```text
extract = tarfile.open(file)
for f in extract:
    # add other unsavory characters in the brackets
    f.name = re.sub(r'[:]', '_', f.name)
extract.extractall(path=new_path)
extract.close()

```

来源

> http://stackoverflow.com/questions/30287036/python-tarfile-extraction-error-ioerror-errno-22-invalid-mode-wb-or-file
