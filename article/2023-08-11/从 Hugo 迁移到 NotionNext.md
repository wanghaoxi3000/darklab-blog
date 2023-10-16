---
date: "2023-08-11"
type: Post
category: 博客记录
slug: migrate-blog-to-notionnext-from-hugo
tags:
  - NotionNext
  - hugo
  - notion
  - blog
summary: 曾经在 一周随笔20230226 这篇博文中描述了下我心目中理想的 Blog 系统，吐槽了下写博文时的一些很不爽的地方，也一直在寻找更好的 Blog 系统。直到无意间发现了 NotionNext，一下就有了哎哟不错喔，这应该就是我想要的博客系统这种感觉。甚至马上就想开始动手迁移我的博客，没有当初从 Hexo 迁移到 Hugo 的时那种纠结。
title: 从 Hugo 迁移到 NotionNext
status: Published
urlname: 396270c6-a77e-4a97-992e-e273e0a24892
updated: "2023-10-08 17:59:00"
---

曾经在 [一周随笔 20230226](https://darkreunion.tech/article/one-week-essay-20230226) 这篇博文中描述了下我心目中理想的 Blog 系统，吐槽了下写博文时的一些很不爽的地方，也一直在寻找更好的 Blog 系统。直到无意间发现了 [NotionNext](https://github.com/tangly1024/NotionNext)，一下就有了哎哟不错喔，这应该就是我想要的博客系统这种感觉。甚至马上就想开始动手迁移我的博客，没有当初从 Hexo 迁移到 Hugo 的时那种纠结。

在写下这篇文章时，这个博客站已经完成了从 Hugo 到 [NotionNext](https://github.com/tangly1024/NotionNext) 的迁移，更新好了各种配置，稳定运行了一段时间了，可以开始安心的写这篇文章啦。

吸引我的几点：

- 基于 notion，在 notion 中写作体验很好, 有效降低了写作的阻力
- 主题漂亮，NotionNext 的几个主题风格不错, 颜值也是一种生产力
- 定制化方便，菜单、网站公共这些直接在 notion 中即可编辑
- 部署方便，通过 vercel 直接一件部署成本，没啥运维成本
- 开源免费，而且作者更新的很勤快，之前也看过几款基于 notion 的建站产品不过都要付费

当然，NotionNext 也还不算完美，我觉得还有几个痛点：

迁移麻烦，如果之前有使用其他博客系统的话，要迁移到 NotionNext 得看 notion 是否支持。虽然 notion 也有了对应的 API，但是感觉支持的还不多，我是写了一个 Python 脚本来导入，通过 notion 的 token_v2 调用的 web api，但是 web api 经常在变化，Python 的库已经不能直接调用了，还有手动更改下库的代码才能成功导入，而且部分文章在导入后出现了问题，需要手动再调整。

不能备份到 Git，虽然 notion 也是一个不小的平台了，数据应该还算有保障，但是毕竟数据没在自己手上，如果能支持自动备份文章到 Git 的话会安心不少，不过搜了下 Github 上已经有了不少备份 notion 的工具，应该有路径，需要后面再研究下。

还有就是 NotionNext 还比较新，时不时有些小 bug，很多配置的更新还有靠修改源代码。目前看起来这个项目主要还是作者一个人在维护，贡献者不多，虽然作者很勤快，但是感觉开源软件要有长久的生命力的话还是需要一个活跃的社区。

这里简单记录下我的迁移脚本，用于将我的 hugo 迁移到 NotionNext，hugo 中的文件结构可以很自由，主要记录下思路。

用到的库：

- pyyaml
- python-dateutil
- notion
- md2notion

```python
import glob
import io
import json
import os

import yaml
from dateutil.parser import parse
from md2notion.upload import upload
from notion.client import NotionClient
from notion.collection import NotionDate


def read_post_file(post_path):
    pathname = os.path.join(post_path, "**/*.md")

    index = 0
    bloglist = []
    for fp in glob.iglob(pathname, recursive=True):
        with open(fp, "r", encoding="utf-8") as mdFile:
            mdStr = mdFile.read()
            mdStr = mdStr.strip("-").strip()
            mdChunks = mdStr.split("---", 1)
            header = yaml.safe_load(mdChunks[0])

            slug = header["slug"].lower()
            content = mdChunks[1].lstrip("\n")
            summary = header.get("description")
            des_list = content.split("<!-- more -->")
            if len(des_list) > 1 and summary is None:
                summary = des_list[0].strip("\n")

            date = header.get("date")
            if isinstance(date, str):
                date = parse(date)

            content = content.replace("<!-- more -->", "", 1)

            page = {
                "filepath": fp,
                "title": header["title"],
                "slug": slug,
                "category": header.get("categories"),
                "tags": header.get("tags", []),
                "summary": summary,
                # "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "date": date.date(),
                "content": content,
            }

        bloglist.append(page)
        index += 1

    bloglist.sort(key=lambda x: x["date"], reverse=True)
    return bloglist


def upload_notion(bloglist: list):
    token_v2 = ""
    collection_view_id = "https://www.notion.so/xxxxx"

    client = NotionClient(
        token_v2
    )
    cv = client.get_collection_view(
        collection_view_id
    )

    with open('record.json', 'r') as f:
        record = json.load(f)

    index = 1
    for page in bloglist:
        if page["slug"] in record["imported"]:
            print("skip article", page.get("title"))
            index += 1
            continue

        print(f"{index}/{len(bloglist)}:Uploading {page.get('filepath')}")

        row = cv.collection.add_row()
        row.type = "Post"
        row.date = NotionDate(page["date"])
        row.title = page["title"]
        row.slug = page["slug"]
        row.category = page["category"][0]
        if page["tags"]:
            row.tags = page["tags"]
        row.status = "Draft"
        if page.get("summary"):
            row.summary = page["summary"]

        mdFile = io.StringIO(page.get("content"))
        mdFile.__dict__["name"] = page["filepath"]

        try:
            upload(mdFile, row)
        except Exception as e:
            print(e)
            with open('record.json', 'w') as f:
                json.dump(record, f, ensure_ascii=False, indent=4)
            exit(1)

        index += 1
        record["imported"].append(page["slug"])


if __name__ == "__main__":
    bloglist = read_post_file("content/posts")
    upload_notion(bloglist)
```

notion 库中代码存在问题需要手动改下：

notion/client.py 313 行和 notion/store.py 280 行的 limit 改为 100。

相关 Issue：

[https://github.com/NarekA/git-notion/issues/1](https://github.com/NarekA/git-notion/issues/1)

[https://github.com/knightjoel/notion-py/commit/521013095e96a05b80edd3e007c931c78a55ce6b](https://github.com/knightjoel/notion-py/commit/521013095e96a05b80edd3e007c931c78a55ce6b)

最后再碎碎念几下：

有搜索到这篇日本一位作者的文章 [https://dev.classmethod.jp/articles/output-github-repos-release-note-to-notion-db/](https://dev.classmethod.jp/articles/output-github-repos-release-note-to-notion-db/)，有尝试通过 notion 的开放 API 来导入，不过一直没成功，放弃..

也有考虑过使用 [思源笔记](https://github.com/siyuan-note/siyuan) 配合这个发布 [插件](https://github.com/terwer/sy-post-publisher) 来作为博客解决方案，感觉也是不错的选择，而且可以更方便，不过是思源笔记开源版本没有移动客户端，作为博客记录还没有付费的动力，看到了 NotionNext 后也放弃了，可以作为一个备选方案。
