---
date: "2023-08-27"
type: Post
category: 博客记录
slug: backup-notion-to-github
tags:
  - notion
summary: 在开始使用 Notion 编写文档并通过 NextNotion 来发布博客后，整个博客的管理和书写体验感觉流畅了不少，不过整个博客的数据放在 Notion 中，心里多少还是有些担忧，假如以后想再迁移到其他的平台岂不是很麻烦，最好有一种方法可以批量导出 Notion 中的文档为 markdown，这样就可以把数据掌握在自己手里，随时可以迁移，再通过 Git 来管理，每个文档还可以有变更的历史记录，再也没有后顾之忧。
title: 备份 Notion 文档到 Github
status: Published
urlname: 22562976-5d02-440f-bca6-042e5cb93a10
updated: "2023-08-27 21:57:00"
---

在开始使用 Notion 编写文档并通过 [NextNotion](https://github.com/tangly1024/NotionNext) 来发布博客后，整个博客的管理和书写体验感觉流畅了不少，不过整个博客的数据放在 Notion 中，心里多少还是有些担忧，假如以后想再迁移到其他的平台岂不是很麻烦，最好有一种方法可以批量导出 Notion 中的文档为 markdown，这样就可以把数据掌握在自己手里，随时可以迁移，再通过 Git 来管理，每个文档还可以有变更的历史记录，再也没有后顾之忧。

抱着这样的想法，我开始寻找是否有解决方案，期望的需求：

- 导出 Notion 中 Database 文档为 markdown
- 可以同时备份图片，并且修改文档中的图片链接为备份链接
- 能尽可能的自动化

在 Github 上搜索了一下，还行，已经有了不少的 Notion 备份方案。一些较早方案是需要手动 Notion 网页版 Cookie 中的 token_v2，调用 web 的导出接口来生成 Markdown。

| 项目名         | 地址                                                                                       | star | 最后更新时间 |
| -------------- | ------------------------------------------------------------------------------------------ | ---- | ------------ |
| notion-down    | [https://github.com/kaedea/notion-down](https://github.com/kaedea/notion-down)             | 111  | 2021-11-17   |
| notion-docsify | [https://github.com/qumuchegi/notion-docsify](https://github.com/qumuchegi/notion-docsify) | 32   | 2022-04-18   |
| notion-up      | [https://github.com/kaedea/notion-up](https://github.com/kaedea/notion-up)                 | 108  | 2021-11-22   |
| notion-backup  | [https://github.com/darobin/notion-backup](https://github.com/darobin/notion-backup)       | 312  | 2023-03-28   |
|                | 数据记录时间：2023-08-26                                                                   |      |              |

这一类方案好处是使用官方的 markdown 导出接口，文档转换出来的效果很好，不过 token_v2 存在一年的有效期，过期后需要手动重新获取，而且使用 web 接口毕竟是未公开的接口，随时有变动的可能，不是很推荐了。

Notion 如今已经推出了官方的 API，能通过官方 API 来备份文档的话那是最好不过了，还好，找到了这两个方案：

| 项目名        | 地址                                                                                     | star | 最后更新时间 |
| ------------- | ---------------------------------------------------------------------------------------- | ---- | ------------ |
| notion-md-gen | [https://github.com/bonaysoft/notion-md-gen](https://github.com/bonaysoft/notion-md-gen) | 79   | 2023-07-02   |
| elog          | [https://github.com/LetTTGACO/elog](https://github.com/LetTTGACO/elog)                   | 114  | 2023-08-18   |
|               | 数据记录时间：2023-08-26                                                                 |      |              |

这两个方案中，elog 的生态更好，有专门的团队维护，并且支持更多的平台，完全可以使用这个工具在其支持的平台中写作，然后统一发布到各其他平台。用来备个份当然也是措措有余了，跟着文档进行了下配置：

1. 为 Notion 建立一个 Integration Token，并连接到要备份的 Database，可以参见 elog 的[官网文档](https://elog.1874.cool/notion/gvnxobqogetukays#notion)
2. 在 GitHub 中建立一个仓库，用于保存备份数据
3. 新建一个 **elog.config.js，**用于配置导出数据所需的 token、ID，以及导出时是否过滤，保存方式、是否导出图片等选项
4. 如有特殊需求，可以创建一个 **formatext.js** 来自定义处理数据，我使用这个文件来处理了下 front matter 信息
5. 为了实现自动化，创建了 `.github/workflows/backup.yml` 方便此后通过 GitHub Action 来自动备份 Notion 数据

具体可以参考我的仓库地址：[https://github.com/wanghaoxi3000/darklab-blog](https://github.com/wanghaoxi3000/darklab-blog)

完成这些步骤后，我会在写完文章后，在终端调用下 GitHub Action 的触发接口：

```bash
curl -L -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -d '{"event_type": "backup"}' \
  https://api.github.com/repos/wanghaoxi3000/darklab-blog/dispatches
```

GitHub Action 便会开始下载 Notion 的数据，转换为 Markdown 格式，生成 front matter 信息，并按日期归档后推送到指定的仓库中了。
