---
title: shell编辑crontab任务
date: 2017/12/29 01:09:00
categories:
- Linux管理
toc: true
---

crontab是Linux下执行定时任务的工具，之前偶尔需要用到时都是通过执行`crontab -e`命令或者通过root身份直接编辑`/etc/cron.*/`下的文件来添加定时任务。这段时间遇到了需要通过shell来自动添加或删除crontab的需求。在shell中无法通过`crontab -e`来与crontab编辑器交互，同时执行命令的人不一定有root身份，也无法直接编辑`/etc/cron.*/`下的文件。

经过一番实践，通过`crontab -l`配合`sed`命令来完成了这个自动添加及删除crontab的操作，在此记录下。

#### crontab的语法
一张很明晰的crontab语法图，附在这以备用

![crontab的语法](http://ohyn8f189.bkt.clouddn.com/17-12-28/62834492.jpg)

#### shell控制脚本
```bash
#!/usr/bin/env bash

CUR_PATH=$(cd "$(dirname "$0")"; pwd)

# 要定时执行的任务
TASK_COMMAND="echo 'aaa' >> /var/cron_test"
# 要添加的crontab任务
CRONTAB_TASK="*/30 * * * * ${TASK_COMMAND}"
# 备份原始crontab记录文件
CRONTAB_BAK_FILE="${CUR_PATH}/crontab_bak"

# 创建crontab任务函数
function create_crontab()
{
    echo 'Create crontab task...'
    crontab -l > ${CRONTAB_BAK_FILE} 2>/dev/null
    sed -i "/.*${TASK_COMMAND}/d" ${CRONTAB_BAK_FILE}  # 已存在任务时会被sed删除，防止重复添加
    echo "${CRONTAB_TASK}" >> ${CRONTAB_BAK_FILE}
    crontab ${CRONTAB_BAK_FILE}
    
    echo 'Complete'
}

# 清除crontab任务函数
function clear_crontab(){
    echo 'Delete crontab task...'
    crontab -l > ${CRONTAB_BAK_FILE} 2>/dev/null
    sed -i "/.*${SCRIPT_NAME}/d" ${CRONTAB_BAK_FILE}
    crontab ${CRONTAB_BAK_FILE}
    
    echo 'Complete'
}

if [ $# -lt 1 ]; then
    echo "Usage: $0 [start | stop]"
    exit 1
fi

case $1 in
    'start' )
        create_crontab
        ;;
    'stop' )
        clear_crontab
        ;;
esac
```
