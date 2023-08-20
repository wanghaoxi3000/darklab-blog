---
date: "2016-11-08"
type: Post
category: Python
slug: py2exe-conversion-parameters
tags: []
title: py2exe转换参数
status: Published
urlname: 11f072de-5ee2-401b-946c-59daf3f6a1ad
updated: "2023-07-17 15:12:00"
---

在公司用 python 写了个统计数据并通过 xlsxwriter 模块生成 excel 的小工具, 完成后使用 py2exe 转换成 exe 文件过程中遇到了些问题, 记录下.

```python
from distutils.core import setup

import sys

sys.argv.append('py2exe')   # 直接执行python setup.py即可转换

includes = ['xlsxwriter']
options = {
    'py2exe':
        {
            'compressed': 1,
            'optimized': 2,
            'includes': includes,
            'dll_excludes': ['w9xpopen.dll'],   # 排除w9xpopen这个win9x才需要的dll文件
            'bundle_files': 1                   # 将生成的调用文件打包进exe文件
        }
}

setup(
    option=options,
    zipfile=None,           # 将生成的library.zip打包进exe文件
    console=['_init_.py']
)

```

转换过程中会提示找不到 xlsxwriter 模块, 查了下是因为 py2exe 还不支持 egg 模块的打包, 解决办法是将 Python27\Lib\site-packages 目录下的 xlsxwriter 模块 egg 文件解压后复制到工程目录即可
