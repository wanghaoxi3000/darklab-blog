---
date: "2020-12-08"
type: Post
category: 软件工具
slug: sync-github-project-and-publish-on-coding
tags:
  - github
  - coding
  - devOps
summary: |-
  coding 提供了一套免费的静态页面服务，还可以自定义域名，本人的 airaNg 服务页面也是部署在coding的静态页面服务当中。不过 ariaNg 还会不断更新，如何在 ariaNg 原项目版本升级后自动更新自己部署的在 coding 的页面呢，这里利用 coding 自带的持续集成功能来完成这种自定义的操作。
  目前coding的静态页面服务已进行了修改，使用腾讯云的 oss 和 cdn 来部署了，虽然速度和稳定性有了提升，但可能也会产生费用。
title: 使用coding自动同步和部署Github项目
status: Published
urlname: c631f70a-8388-4ff0-bfb4-c3e41fc3ece0
updated: "2023-07-13 14:10:00"
---

[coding](https://coding.net/) 提供了一套免费的静态页面服务，还可以自定义域名，本人的 airaNg 服务页面也是部署在 coding 的静态页面服务当中。不过 [ariaNg](https://ariang.mayswind.net/) 还会不断更新，如何在 ariaNg 原项目版本升级后自动更新自己部署的在 coding 的页面呢，这里利用 coding 自带的持续集成功能来完成这种自定义的操作。

_目前 coding 的静态页面服务已进行了修改，使用腾讯云的 oss 和 cdn 来部署了，虽然速度和稳定性有了提升，但可能也会产生费用。_

<!-- more -->

## 工作流程

主要的原理是通过在 coding 中创建一个项目，并为这个项目启动两个持续集成任务，一个是定时同步 Github 上原项目的更改，另外一个是接收到代码的更新后，触发持续集成下载代码代码包，部署到项目静态页面。

## 持续集成任务配置

因为涉及到在持续集成任务中推送代码，需要在 coding 的个人配置页面先申请一个 token。部署完成后，使用了[server 酱](http://sc.ftqq.com/3.version)来推送结果。

### 定时同步任务

需要配置的环境变量

- GITHUB_REPO AriaNg 代码库原地址：[https://github.com/mayswind/AriaNg.git](https://github.com/mayswind/AriaNg.git)
- TOKEN_NAME Coding token name
- TOKEN_VALUE Coding token value
- PUSH_TOKEN Server 酱推送 token

Jenkins 流程定义

```text
pipeline {
  agent any
  stages {
    stage('clone github') {
      steps {
        sh 'git clone $GITHUB_REPO'
      }
    }
    stage('update repo') {
      steps {
        sh '''cd AriaNg

git config --global user.name "devOps"
git config --global user.email "devOps@coding.net"
git remote add coding "<https://${TOKEN_NAME}:${TOKEN_VALUE}@e.coding.net/username/ariaNg.git>"
git push --tags coding master:main'''
      }
    }
  }
  post {
    unsuccessful {
      sh 'curl -s -d "text=项目 ${PROJECT_NAME}: ${CCI_JOB_NAME} 构建失败" <https://sc.ftqq.com/${PUSH_TOKEN}.send>'

    }

  }
}

```

### 页面发布任务

需要配置的环境变量

- TOKEN_NAME Coding token name
- TOKEN_VALUE Coding token value
- PUSH_TOKEN Server 酱推送 token

Jenkins 流程定义

```text
pipeline {
  agent any
  stages {
    stage('检出') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: GIT_BUILD_REF]],
          userRemoteConfigs: [[
            url: GIT_REPO_URL,
            credentialsId: CREDENTIALS_ID
          ]]])
        }
      }
      stage('发布') {
        steps {
          sh '''REC_TAG=$(git describe --tags `git rev-list --tags --max-count=1`)
DIST_FILE=AriaNg-${REC_TAG}.zip
echo "Current code tag: ${REC_TAG}"

git checkout master
rm -rf $(ls)

wget <https://github.com/mayswind/AriaNg/releases/download/${REC_TAG}/${DIST_FILE}>
unzip ${DIST_FILE}
rm ${DIST_FILE}

git add -A
git commit --amend -m "Updated By devOps With Build ${REC_TAG}"
git push --force --quiet "<https://${TOKEN_NAME}:${TOKEN_VALUE}@e.coding.net/username/ariaNg.git>" master:master

curl -s -d "text=项目 ${PROJECT_NAME}: ${CCI_JOB_NAME} ${REC_TAG} 构建成功" <https://sc.ftqq.com/${PUSH_TOKEN}.send>'''
        }
      }
    }
    post {
      unsuccessful {
        sh 'curl -s -d "text=项目 ${PROJECT_NAME}: ${CCI_JOB_NAME} 构建失败" <https://sc.ftqq.com/${PUSH_TOKEN}.send>'

      }

    }
  }

```
