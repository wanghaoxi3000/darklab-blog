---
title: py2exe转换参数
date: 2016/11/8 00:40:00
categories:
- Python
toc: true
---

在公司用python写了个统计数据并通过xlsxwriter模块生成excel的小工具, 完成后使用py2exe转换成exe文件过程中遇到了些问题, 记录下.

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

转换过程中会提示找不到xlsxwriter模块, 查了下是因为py2exe还不支持egg模块的打包, 解决办法是将Python27\Lib\site-packages目录下的xlsxwriter模块egg文件解压后复制到工程目录即可