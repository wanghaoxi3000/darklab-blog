---
title: 在 hexo 中使用 git submodules 管理主题
categories:
  - 软件工具
tags:
  - Git
  - hexo
  - git submodules
toc: true
date: 2019-01-03 22:04:48
---

`hexo` 中有着丰富的主题可以选择, 大部分的使用示例或者教程都是将主题 clone 到 theme 文件夹中来使用. 但这样来使用主题会存在如下的问题:

- theme 中的主题属于一个独立的 Git 项目, 有自己的 `.git` 项目文件夹, 提交 hexo 项目时默认不会提交 theme 的 `.git` 文件夹, 在其他电脑上 clone 后会失去 theme 原本的版本控制功能.
- 使用自己修改的主题时, 每次更改完主题, 需要在主题文件夹中提交一次, 然后再在 hexo 项目根文件夹中提交一次, 会产生两次修改内容一样的提交, 不够优雅.

还好万能的 Git 针对这种问题已经有了成熟的解决方案, 通过自带的 Git submodules 功能即可优雅的避免以上的问题.


## Git submodules 简介
Git submodules 称之为 Git 子模块. 子模块允许你将一个 Git 仓库作为另一个 Git 仓库的子目录. 它可以让你将另一个仓库克隆到自己的项目中, 同时还保持提交的独立. 它非常适合我们程序员在项目管理时遇到的一种情况: 某个工作中的项目需要包含并使用另一个项目.  这些包含的项目也许是第三方库, 或者你独立开发的, 用于多个父项目的库. 你想要把它们当做两个独立的项目, 同时又想在一个项目中使用另一个.

**在 hexo 中使用丰富的第三方主题的情况正非常符合这种情景**.


## Git submodules 使用
了解了 Git submodles 的使用场景后, 这么强力的工具如何在 hexo 中来使用呢. 在这里演示下我的用法.

首先初始化一个用来演示的 hexo 项目:
```
npm install hexo-cli -g
hexo init blog
cd blog
npm install
hexo server
```

执行以上操作后, 打开浏览器进入 http://localhost:4000/ 便可以预览到初始化好的 hexo 页面. 在项目的 `theme` 文件夹中可以看到使用了默认的 `landscape` 主题. 在这个 hexo 项目中建立起 Git 版本管理.
```
git init
git commit -m 'initial project'
```
现在一个 hexo 本地仓库已经建立好了并将初始化的文件提交了进去.

### 基础用法
现在我们使用 Git submodules 的方式来选择一个第三方主题来替换原本的 `landscape` 主题. 这里选择我比较喜欢的的 [pure](https://github.com/cofess/hexo-theme-pure) 主题.
```
git submodule add https://github.com/cofess/hexo-theme-pure themes/pure
```
git 便会将 `hexo-theme-pure` 主题作为一个项目子模块 clone 到 themes/pure 中. 同时 hexo 项目中会自动生成一个 `.gitmodules` 文件, 这个配置文件中保存了项目 URL 与已经拉取的本地目录之间的映射.

**.gitmodules 文件内容**
```
$ cat .gitmodules
[submodule "themes/pure"]
	path = themes/pure
	url = https://github.com/cofess/hexo-theme-pure
```

**git 目前状态**
```
$ git status
On branch master
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        new file:   .gitmodules
        new file:   themes/pure
```
可以看到, 虽然 themes/pure 是工作目录中的一个子目录, 但 Git 还是会将它视作一个子模块. 当不在那个目录中时, Git 并不会跟踪它的内容, 而是将它看作该仓库中的一个特殊提交.

主题 clone 好后, 按照主题的说明安装好需要的插件模块, 再执行 `hexo s`, 重新打开 http://localhost:4000/ 便可以看到使用新主题的博客页面了.

**提交新的 git 记录**
```
$ rm -rf themes/landscape
$ git commit -am 'added pure themes'
create mode 100644 .gitmodules
create mode 160000 themes/pure
```
删除旧的 `landscape` 主题, 使用 `git commit -am` 重新提交添加了 `pure` 主题的 hexo 项目, 可以看到 git 使用 160000 模式创建 themes/pure 记录. 这是 git 中的一种特殊模式, 它本质上意味着将一次提交记作一项目录记录, 而非将它记录成一个子目录或者一个文件.

**拉取含子模块的修改**

主题作为子模块添加到项目中后, 若主题作者有更新, 便可通过两种方法来拉取主题的更新内容.
1. 进入`themes` 下主题目录, 执行 `git fetch` 和 `git merge origin/master` 来 merge 上游分支的修改
2. 直接运行 `git submodule update --remote`, Git 将会自动进入子模块然后抓取并更新

更新后重新提交一遍, 子模块新的跟踪信息便也会记录到仓库中.

**拉取含子模块的项目**

使用 `git clone` 命令默认不会拉取项目中的子模块, 在 clone 后的项目中可以通过运行两个命令:
1. `git submodule init` 初始化本地配置文件
2. `git submodule update` 从该项目中抓取所有数据并检出父项目中列出的合适的提交

也可在 clone 使用 `git clone --recursive` 命令, git 就会自动初始化并更新仓库中的每一个子模块.


### 高级使用
通过子模块基础用法, 可以直接方便的跟踪管理一些的简单的主题. 但很多主题都存在一些自己的配置项目, 需要我们根据自己的需要来进行设置,  或者我们想要在主题的基础上自定义修改自己喜欢的主题,  这个时候就需要对主题进行修改并提交仓库以便在各处使用. 

不过对于主题仓库我们一般没有提交的权限, 不能提交到主题源仓库中. 此时可以通过 `fork` 功能, 在源主题上 fork 出自己项目, 从而在自己仓库中进行提交来跟踪修改.

这里我在 pure 主题上 fork 出了一个自己的主题仓库 [my-hexo-theme-pure](https://github.com/wanghaoxi3000/my-hexo-theme-pure), 使用这个仓库按照之前的步骤替换原本的主题来作为子模块.

**修改子模块**

当运行 `git submodule update` 从子模块仓库中抓取修改时, Git 将会获得这些改动并更新子目录中的文件, 但是会将子仓库留在一个称作 `游离的 HEAD` 的状态. 这意味着没有本地工作分支(例如 "master")跟踪改动, 此时做的任何改动都不会被跟踪. 因此, 我们首先需要进入子模块目录然后检出一个分支.
```
$ git checkout stable
Switched to branch 'stable'
```

若子分支仓库中有未同步的更新, 可通过 `git submodule update --remote --rebase` 来同步最新的内容. 之后便可以打开编辑器在子模块上工作修改代码了.

**同步源主题的修改**

主题作者发布了新的主题功能或者修复了Bug, 我们想同步到自己的自定义主题当中. 因为我们的自定义主题是从原主题中 fork 出来的, 可以通过 `git remote add source https://github.com/cofess/hexo-theme-pure` 命令将源主题仓库添加为子模块的 一个新的 `source` 仓库. 然后运行 `git fetch` 拉取修改后, 便可以通过 `git merge origin/master` 来同步源主题的更新了.

**发布子模块的修改**

子模块修改完成后, 我们便可以发布到仓库中, 以便在其他地方重新 clone 时可以使用最新的主题文件. 为了防止我们遗忘子模块的提交, 可以在 push 时通过 `git push --recurse-submodules=check` 命令,  如果任何提交的子模块改动没有推送那么 check 选项会直接使 push 操作失败.

另外也可以使用 `git push --recurse-submodules=on-demand` git 会自动尝试推送变更的子项目.

### 拓展用法
以上介绍了使用子模块来管理 themes 的方法, 实际上在 hexo 中还可以使用 子模块来管理 hexo 的静态部署文件. 对于使用 github 托管静态页面等部署方式的用户而言, 通过 `hexo-deployer-git` 插件可以方便的自动化部署静态页面.

**hexo-deployer-git 工作流程**

`hexo-deployer-git` 部署的方式是在 hexo 项目根目录下创建了一个 `.deploy_git` 文件夹, 并在其中创建了一个独立的 git 分支, 将生成静态文件移入这个文件夹中并推送到指定的地址. 但 `.deploy_git` 文件夹默认也被写入 `.gitignore` 文件中, hexo 项目 git 库不会记录这个文件夹, 同时 `hexo-deployer-git` 在每次部署时也不会自动同步服务器上的提交历史, 而是强制覆盖旧的提交. 在新的电脑或路径上重新 clone 后也会出现旧的静态文件记录丢失的情况, 重新 deploy 后服务器上旧的部署历史也会丢失.

如果想要保存每次的部署记录, 那么就可以将 `.deploy_git` 中的文件也看做一个子项目, 以子项目的形式提交到 hexo 主项目中保存, 就可以保持部署记录不丢失, 并且在任何地方重新 clone 时都可以恢复最新的记录.

**添加 .deploy_git 中分支为子项目**

`.deploy_git` 中是由部署插件在 hexo 项目上创建的一个独立分支, 只需通过传递 `-b` 选项将 hexo 项目的这个分支作为主项目的依赖即可, 例如部署在 `coding` 时, 使用的 `coding-pages` 分支:
```
git submodule add -b coding-pages <site>
```

## 参考资料
> Pro Git book - 子模块 https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E5%AD%90%E6%A8%A1%E5%9D%97
