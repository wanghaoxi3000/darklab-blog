---
title: 博客装修记
categories:
  - 随笔
toc: true
date: 2022-07-23T17:14:45+08:00
slug: blog-decorate-record
description: 选定博客生成系统往往只是打造自己博客的第一步，这里记录了本博客从 hexo 迁移到 hugo 后，后续的功能集成步骤。
---

选定博客生成系统往往只是打造自己博客的第一步，这里记录了本博客从 hexo 迁移到 hugo 后，后续的功能集成步骤。
<!-- more -->

## 文章迁移
`hexo` 和 `hugo` 的文章目录布局还是有所区别的，为了快速迁移以往的文章，写了一个 Python 脚本来完成这个步骤，代码如下：

```Python
from datetime import date, datetime
import os
import re
import yaml


CONTENT_DIR = 'content'

files = os.listdir("_posts")

m = re.compile(r'---(.*)---', re.S)

for i in files:
    print(i)
    with open("_posts/" + i, "r") as f:
        content = f.read()
        f.seek(0)
        new_content = f.readlines()

    r = m.search(content)
    info = r.group(1)
    length = len(info.split('\n'))

    data = yaml.safe_load(info)
    new_content.insert(length-1, 'slug: ' + i + '\n')

    file_path = os.path.join(CONTENT_DIR, data['categories'][0], data['date'].strftime('%y%m%d') + '-' + data['title'])
    os.makedirs(file_path, exist_ok=True)

    with open(os.path.join(file_path, 'index.md'), 'w') as f:
        f.write(''.join(new_content))

```

## 建立新分支
由于代码的变化很大，在原来的博客代码库[darklab-blog](https://github.com/wanghaoxi3000/darklab-blog)，使用 `git checkout --orphan main` 新建了一个 空白的 main 分支，这样可以从零开始提交，和原来的分支独立，顺便也把主分支切换为和 main，和新的 Github 规范保持一致。

## 评论系统
以前 Hexo 使用的是 [valine](https://github.com/xCss/Valine) 系统，这次换到了 [giscus](https://giscus.app/) 系统，基于 GitHub Discussions 系统，感觉可以更轻量，维护成本可以更低。由于使用的主题已经添加了对应的支持，在 giscus 的网站页面按照步骤配置一遍后，将生成的ID添加到 config.yaml 配置中即可。

## 数据统计
基于百度统计或谷歌统计，可以查看到网站的访问数据，对于持续的迭代和改进还是有一定帮助。

### Google
在 https://search.google.com/search-console 即可获取网站的分析数据，查看数据需要对网站的所有权进行验证。谷歌统计支持通过 DNS 对网站所有权进行验证，在域名提供商配置一个对应的 TXT 解析即可查看到数据。

### Baidu
百度统计的网站是 https://tongji.baidu.com/，添加百度统计需要在网站的页面加入指定的代码，hugo stack 主题支持自定义页面头部和底部的内容，新增 layouts\partials\footer\custom.html 文件，加入百度统计的代码即可。

## Github Action
通过 Github Action，可以在向博客代码仓库推送代码更新后，自动更新网站。本博客的 Github Action 主要做了这几件事：

1. 拉取代码
2. 安装 Hugo
3. 生成静态页面
4. 上传到 COS 对象存储
5. 刷新 CDN

代码如下：

```yaml
name: Deploy Blog

on:
  push:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          submodules: true # Checkout private submodules(themes or something else).

      - name: Hugo setup
        uses: peaceiris/actions-hugo@v2.4.13
        with:
          hugo-version: latest
          extended: true

      - name: Run hugo build
        run: hugo

      - name: Upload website
        uses: saltbo/uptoc@v1.4.3
        with:
          driver: cos
          region: ap-hongkong
          bucket: ${{ secrets.TCLOUD_BUCKET_ID }}
          exclude: .cache,test
          dist: public
        env:
          UPTOC_UPLOADER_AK: ${{ secrets.TCLOUD_SECRET_ID }}
          UPTOC_UPLOADER_SK: ${{ secrets.TCLOUD_SECRET_KEY }}

      - name: Refresh CDN
        env:
          TENCENTCLOUD_SECRET_ID: ${{ secrets.TCLOUD_SECRET_ID }}
          TENCENTCLOUD_SECRET_KEY: ${{ secrets.TCLOUD_SECRET_KEY }}
        run: |
          pip install tccli
          tccli cdn PurgePathCache --cli-unfold-argument --Paths https://darkreunion.tech/ --FlushType flush
```