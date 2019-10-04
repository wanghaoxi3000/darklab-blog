---
title: '[转载]搭建基于Docker的OpenVPN服务'
date: 2019/10/4 21:02:00
categories:
- 软件工具
tags:
- OpenVPN
toc: true
---

原文链接：http://dockone.io/article/214

## 介绍

本教程将介绍如何使用[Docker](https://www.docker.com)来设置和运行[OpenVPN](http://openvpn.net/index.php/open-source)容器。

OpenVPN提供了一种方法来创建TLS加密（SSL的演进）的虚拟专用网络（VPN）。它可以防止网络流量被窃取和中间人（MITM）攻击。专用网络可以用来安全地连接设备，例如，它可以把在不安全的WiFi环境下的笔记本电脑或移动电话连接到远程服务器，然后走Internet流量。它也可用于互联网设备之间的安全连接。
<!-- more -->

Docker提供了一种封装OpenVPN服务进程和配置数据的方式，以便更容易管理。Docker的OpenVPN镜像是预建的，它包含了在一个稳健环境中运行服务器所需的所有依赖。镜像中包含自动化构建标准案例的脚本，想要手动配置也可以。Docker卷容器可以保存配置以及 EasyRSA PKI证书数据。

[Docker Registry](https://registry.hub.docker.com)是一个中央存储仓库，它包含官方以及用户开发的Docker镜像。在本教程中使用的镜像是用户贡献的（译者注：非官方），你可以在[kylemanna/ OpenVPN](https://registry.hub.docker.com/u/kylemanna/openvpn/)中找到。该镜像由基于[GitHub仓库](https://github.com/kylemanna/docker-openvpn)的Docker Registry云构建服务组装而成。链接在GitHub上的云服务器构建增加了审计Docker 镜像的功能，使用户可以查看源Dockerfile和相关的代码，称为[Trusted Build](http://blog.docker.com/2013/11/introducing-trusted-builds/)。当GitHub仓库的代码有更新，那么新的Docker image就会被构建并发布到Docker Registry。

## 使用案例

*   在不可信的公共（无线）网络安全的路由到互联网
*   用于连接笔记本电脑，办公室电脑，家用电脑，或移动电话的专用网络
*   用于不具备NAT穿越能力，在NAT路由后面用来安全服务的私有网络

## 目标

*   在Ubuntu14.04 LTS创建Docker守护进程。
*   创建用来保存配置数据的[Docker卷容器](https://docs.docker.com/userguide/dockervolumes/#creating-and-mounting-a-data-volume-container)。
*   生成EasyRSA PKI数字证书（CA）。
*   提取自动生成的客户端配置文件。
*   配置可选数量的OpenVPN客户端。
*   处理在开机时启动Docker容器。
*   介绍高级主题。
    **需要准备的知识**
*   Linux shell知识。本教程假定用户能够建立并运行Linux守护进程。
*
    远程服务器上的root访问权限
    *   一台[DigitalOcean的单核CPU/512内存](https://www.digitalocean.com)，且运行Ubuntu14.04操作系统的机器。
    *   只要主机具有QEMU/ KVM或Xen虚拟化技术，虚拟主机就能运行; **OpenVZ的将无法正常工作**。
    *   你需要在服务器上的root访问权限。本教程假定用户正在运行的是可以使用sudo的非特权用户。如果需要，可以查看在[Ubuntu14.04关于用户管理的 Digital Ocean的教程](https://www.digitalocean.com/community/tutorials/how-to-add-and-delete-users-on-an-ubuntu-14-04-vps)。
*
    本地客户端设备，如Android手机、笔记本电脑或PC。几乎所有的操作系统都提供了OpenVPN客户端支持。

## 步骤 1－创建、测试Docker

Docker发展的非常快，而Ubuntu的LTS版本没有及时跟上。为了解决这一问题，我们需要安装一个PPA，以便获取最新的Docker版本。

添加上游的Docker库包签名密钥。`apt-key`命令通过`sudo`来提升权限，所以可能会提示用户输入密码。

```
curl https://get.docker.io/gpg | sudo apt-key add -
```

**提示**：如有必要，在闪烁的光标处输入你的sudo密码。

添加上游Docker库到系统列表：

```
echo deb http://get.docker.io/ubuntu docker main | sudo tee /etc/apt/sources.list.d/docker.list
```

更新软件包列表，并安装Docker：

```
sudo apt-get update && sudo apt-get install -y lxc-docker
```

将用户添加到 `docker`组，以保证它能与Docker守护进程正常通信，`sammy`是你的用户名。**退出并重新登录以确保新组生效**：

```
sudo usermod -aG docker sammy
```

重现登陆后，可以使用 `id`命令验证组成员，如下：
```
uid=1001(test0) gid=1001(test0) groups=1001(test0),27(sudo),999(docker)
```
可选：在一个简单的Debian Docker 镜像中（`-rm` 退出后清理容器 `-it`用于交互）运行`bash` 来验证我们在主机上的Docker操作：
```
docker run --rm -it debian:jessie bash -l
```
当Docker载入镜像和建立容器时，会输出如下内容：
```
Unable to find image 'debian:jessie' locally
debian:jessie: The image you are pulling has been verified
511136ea3c5a: Pull complete
36fd425d7d8a: Pull complete
aaabd2b41e22: Pull complete
Status: Downloaded newer image for debian:jessie
root@de8ffd8f82f6:/#
```
一旦在容器内你看到 `root@&lt;container id>:/#`提示，这表示当前shell是在一个容器中。为了确认它不在主机，检查容器中运行的Debian的版本：
```
cat /etc/issue.net
```
在进行写操作时，预期OpenVPN会输出：
```
Debian GNU/Linux jessie/sid
```
如果你看到一个不同版本的Debian，那也没关系。输入 `logout`退出容器，主机的提示会再次出现。

## 步骤2－建立easyrsa PKI证书存储

这一步对于那些熟悉OpenVPN或经常使用PKI的服务的人来说也非常麻烦。幸运的是，Docker和Docker镜像中的脚本通过生成配置文件以及所有必要的验证文件来简化这一步。

创建一个卷容器。本教程将使用`$ ovpn_data`环境变量。默认`ovpn-data`值推荐使用单个OpenVPN Docker容器服务，这样在Shell中我们就可以使用环境变量：
```
OVPN_DATA="ovpn-data"
```
使用 `busybox`作为一个最小的Docker镜像，创建一个空Docker volume容器：
```
docker run --name $OVPN_DATA -v /etc/openvpn busybox
```
初始化 `ovpn_data`容器，它将包含配置文件和证书，并用你的FQDN替代`vpn.example.com`。`vpn.example.com`的值必须是完全合格的域名，你需要用它来与服务器通信，这里假设你已经配置了[DNS](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-host-name-with-digitalocean)。另外，也可以使用IP地址，但不推荐。
```
docker run --volumes-from $OVPN_DATA --rm kylemanna/openvpn ovpn_genconfig -u udp://vpn.example.com:1194
```
生成EasyRSA PKI 证书授权中心时，可能会要求你输入CA私有密钥的密码。
```
docker run --volumes-from $OVPN_DATA --rm -it kylemanna/openvpn ovpn_initpki
```
**注意， `$OVPN_DATA`容器的安全性很重要。**它包含所有的承担服务和客户端证书的私钥。记住它并适当地控制访问权限。默认的OpenVPN脚本通过密码来为CA key提高安全性以及防止发行假证书。
更多关于备份证书存储细节看下面的结论。

## 步骤3－开始OpenVPN服务

使用`nano`或`vim`创建一个[Upstart](https://www.digitalocean.com/community/tutorials/the-upstart-event-system-what-it-is-and-how-to-use-it)初始化文件来自动运行OpenVPN服务进程（更多关于 [Docker Host Integration](https://docs.docker.com/articles/host_integration/) ）的Docker容器：
```
sudo vim /etc/init/docker-openvpn.conf
```
内容放在 `/etc/init/docker-openvpn.conf`:
```
description "Docker container for OpenVPN server"
start on filesystem and started docker
stop on runlevel [!2345]
respawn
script
exec docker run --volumes-from ovpn-data --rm -p 1194:1194/udp --cap-add=NET_ADMIN kylemanna/openvpn
end script
```
使用Upstart初始化机制来启动进程：
```
sudo start docker-openvpn
```
通过看 `STATUS`列确认容器开启，容器没有立即崩溃：
```
test0@tutorial0:~$ docker ps
CONTAINER ID        IMAGE                      COMMAND             CREATED             STATUS              PORTS                    NAMES
c3ca41324e1d        kylemanna/openvpn:latest   "ovpn_run"          2 seconds ago       Up 2 seconds        0.0.0.0:1194->1194/udp   focused_mestorf
```
## 步骤4－生成客户端证书和配置文件

在本节中我们将使用在上步创建的PKI CA 创建一个客户端证书。一定要适当的替换`CLIENTNAME`（不一定非要是FQDN）。在客户端的名字是用来识别正在运行的OpenVPN客户端的机器（例如，“家用电脑”，“笔记本电脑”，“nexus5“等）。`easyrsa`工具会提示CA密码。这是我们上面在 `ovpn_initpki`命令阶段设定的密码。创建客户端证书：
```
docker run --volumes-from $OVPN_DATA --rm -it kylemanna/openvpn easyrsa build-client-full CLIENTNAME nopass
```
当所有的客户端都创建之后，服务就可以准备接受连接了。

客户端需要证书以及配置文件来进行连接。嵌入式脚本自动执行此任务，允许用户在一个单独的文件填写配置，最后传送到客户端。同样，要适当更换`CLIENTNAME`：
```
docker run --volumes-from $OVPN_DATA --rm kylemanna/openvpn ovpn_getclient CLIENTNAME > CLIENTNAME.ovpn
```
作为结果的clientname.ovpn文件包含连接到VPN所必要的私钥和证书。 **要确保这些文件的安全，不要乱放**。你需要用他们把**.ovpn**文件安全地传输到客户端。出于安全考虑，在传送文件时，尽可能地避免使用公共服务，如电子邮件或云存储。
如果可以，推荐使用SSH / SCP，HTTPS，USB和microSD卡进行转移。

## 步骤5－准备OpenVPN客户端

下面是运行在客户端上的命令和操作，用以连接到上文配置的OpenVPN服务。
**Ubuntu和Debian的分布通过原生OpenVPN**
在Ubuntu12.04/14.04和Debian wheezy/jessie客户端（或者类似的）：
安装OpenVPN：
```
sudo apt-get install openvpn
```
从服务上复制客户端配置文件，设置安全权限：
```
sudo install -o root -m 400 CLIENTNAME.ovpn /etc/openvpn/CLIENTNAME.conf
```
配置初始化脚本, 自动启动所有匹配/etc/openvpn/*.conf的配置：
```
echo AUTOSTART=all | sudo tee -a /etc/default/openvpn
```
重启OpenVPN客户端的服务进程：
```
sudo /etc/init.d/openvpn restart
```
**Arch Linux通过原生OpenVPN**
安装OpenVPN：
```
pacman -Sy openvpn
```
从服务上复制客户端配置文件，设置安全权限：
```
sudo install -o root -m 400 CLIENTNAME.ovpn /etc/openvpn/CLIENTNAME.conf
```
启动OpenVPN客户端的服务进程：
```
systemctl start openvpn@CLIENTNAME
```
可选：启动时配置systemd 来开始/etc/openvpn/CLIENTNAME.conf ：
```
systemctl enable openvpn@CLIENTNAME
```
**MacOS X通过tunnelblick**

下载并安装[tunnelblick](https://code.google.com/p/tunnelblick/)。
从服务器复制 `CLIENTNAME.ovpn`到Mac。
通过双击 `*.ovpn`文件导入配置. TunnelBlick将引用和导入配置。
打开TunnelBlick，选择配置，然后选择连接。

**Android通过OpenVPN连接**

从Google Play商店安装[OpenVPN Connect App](https://play.google.com/store/apps/details?id=net.openvpn.openvpn)。
以安全的方式从服务器复制 `CLIENTNAME.ovpn`到Android设备上。USB或MicroSD卡更加安全。把文件放到你的SD卡上便于打开。
导入配置： **菜单**->**导入**->**从SD卡导入文件**：
选择 **连接**。

## 步骤6－验证操作

有几种通过VPN路由来验证网络连接的方法。
**网页浏览器**
访问网站来确定外部IP地址。外部IP地址应该是OpenVPN服务器。
试试 [google“what is my ip”](http://goo.gl/OWYTAK)或[icanhazip.com](https://icanhazip.com)。
**命令行**
从命令行， `wget`或`curl`命令派上用场。以`curl`为例：
```
curl icanhazip.com
```
以 `wget`为例：
```
wget -qO - icanhazip.com
```
预期的反应应该是OpenVPN服务器的IP地址。
另一个选择是使用 `dig`或使用`host`到一个特殊配置的DNS服务器做专用的DNS查询。基于`host`的例子：
```
host -t A myip.opendns.com resolver1.opendns.com
```
基于 `dig`的例子：
```
dig +short myip.opendns.com @resolver1.opendns.com
```
预期的反应应该是OpenVPN服务器的IP地址。
**额外检查**
回顾你的网络接口的配置。在基于UNIX操作系统，这跟运行 `ifconfig`终端，查找OpenVPN的`tunX`接口一样简单。
审核日志。在UNIX操作系统，旧的distributions审核 `/var/log`，在systemd distributions审核`journalctl`。

## 结论

这里创建和运行的Docker镜像是开源的，而且功能远超本文的描述。你可以在[docker-openvpn的GitHub仓库](https://github.com/kylemanna/docker-openvpn)浏览源代码或者创建修改分支。