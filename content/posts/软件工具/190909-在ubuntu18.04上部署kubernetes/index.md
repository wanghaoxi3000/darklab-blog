---
title: 在ubuntu18.04上部署kubernetes
categories:
  - 软件工具
tags:
  - kubernetes
toc: true
date: 2019-09-09 16:22:53
slug: deploy-kubernetes-on-ubuntu18
---


为了有个k8s的测试环境，使用了三台ubuntu18的系统搭建了一套k8s测试环境，主要参考了[和我一步步部署 kubernetes 集群](https://github.com/opsnull/follow-me-install-kubernetes-cluster)这个项目，这个项目对于如何一步步搭建起k8s集群环境已经很详细了，不过对于ubuntu 18.04的环境还是有一些小坑，这里记录一下。

<!-- more -->

### 主要环境版本
- ubuntu 3节点：ubuntu18.04
- kubernetes：v1.14.6
- docker：18.09.9

### 01.系统初始化和全局变量
[安装依赖包](https://github.com/opsnull/follow-me-install-kubernetes-cluster/blob/master/01.%E7%B3%BB%E7%BB%9F%E5%88%9D%E5%A7%8B%E5%8C%96%E5%92%8C%E5%85%A8%E5%B1%80%E5%8F%98%E9%87%8F.md#%E5%AE%89%E8%A3%85%E4%BE%9D%E8%B5%96%E5%8C%85)一节中，使用的安装命令会出现找不到`libseccomp`的错误，应该使用如下命令:
```
apt-get install -y conntrack ipvsadm ntp ipset jq iptables curl sysstat libseccomp2
```

[设置系统时区](https://github.com/opsnull/follow-me-install-kubernetes-cluster/blob/master/01.%E7%B3%BB%E7%BB%9F%E5%88%9D%E5%A7%8B%E5%8C%96%E5%92%8C%E5%85%A8%E5%B1%80%E5%8F%98%E9%87%8F.md#%E8%AE%BE%E7%BD%AE%E7%B3%BB%E7%BB%9F%E6%97%B6%E5%8C%BA)一节中，ubuntu18重启cron服务的命令为:
```
systemctl restart cron
```

#### 09-1.部署 coredns 插件
[部署 coredns 插件](https://github.com/opsnull/follow-me-install-kubernetes-cluster/blob/master/09-1.dns%E6%8F%92%E4%BB%B6.md)这一节在ubuntu18.04系统上部署coredns插件后，会出现coredns无法启动，报告CrashLoopBackOff的问题
```
root@ubuntu101:/opt/k8s/work/kubernetes/cluster/addons/dns/coredns# kubectl get all --all-namespaces
NAMESPACE     NAME                          READY   STATUS             RESTARTS   AGE
kube-system   pod/coredns-8b77fdfb9-76zj8   0/1     CrashLoopBackOff   7          15m
zai
NAMESPACE     NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE
default       service/
kubernetes   ClusterIP   10.254.0.1   <none>        443/TCP                  7h14m
kube-system   service/kube-dns     ClusterIP   10.254.0.2   <none>        53/UDP,53/TCP,9153/TCP   15m

NAMESPACE     NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
kube-system   deployment.apps/coredns   0/1     1            0           15m

NAMESPACE     NAME                                DESIRED   CURRENT   READY   AGE
kube-system   replicaset.apps/coredns-8b77fdfb9   1         1         0       15m
```

通过查看日志，可以观察到coredns启动中出现了`Loop (127.0.0.1:51377 -> :53) detected for zone "."`的问题:
```
root@ubuntu101:/opt/k8s/work/kubernetes/cluster/addons/dns/coredns# kubectl logs coredns-8b77fdfb9-76zj8 -n kube-system
.:53
2019-09-06T14:02:03.164Z [INFO] CoreDNS-1.3.1
2019-09-06T14:02:03.164Z [INFO] linux/amd64, go1.11.4, 6b56a9c
CoreDNS-1.3.1
linux/amd64, go1.11.4, 6b56a9c
2019-09-06T14:02:03.164Z [INFO] plugin/reload: Running configuration MD5 = 983e0715b6345402acc1b47b2543ece7
2019-09-06T14:02:03.164Z [FAT
AL] plugin/loop: Loop (127.0.0.1:51377 -> :53) detected for zone ".", see https://coredns.io/plugins/loop#troubleshooting. Query: "HINFO 9014994000123808639.4964161867797590684."
```

这应该是DNS服务检查到了一个循环查询的问题，解决方法是在`/etc/systemd/system/kubelet.service`中启动kubelet的命令后添加上`--resolv-conf=/run/systemd/resolve/resolv.conf`参数：
```
[Unit]
Description=Kubernetes Kubelet
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=docker.service
Requires=docker.service

[Service]
WorkingDirectory=/data/k8s/k8s/kubelet
ExecStart=/opt/k8s/bin/kubelet \
  --allow-privileged=true \
  --bootstrap-kubeconfig=/etc/kubernetes/kubelet-bootstrap.kubeconfig \
  --cert-dir=/etc/kubernetes/cert \
  --cni-conf-dir=/etc/cni/net.d \
  --container-runtime=docker \
  --container-runtime-endpoint=unix:///var/run/dockershim.sock \
  --root-dir=/data/k8s/k8s/kubelet \
  --kubeconfig=/etc/kubernetes/kubelet.kubeconfig \
  --config=/etc/kubernetes/kubelet-config.yaml \
  --hostname-override=ubuntu101 \
  --pod-infra-container-image=registry.cn-beijing.aliyuncs.com/images_k8s/pause-amd64:3.1 \
  --image-pull-progress-deadline=15m \
  --volume-plugin-dir=/data/k8s/k8s/kubelet/kubelet-plugins/volume/exec/ \
  --logtostderr=true \
  --resolv-conf=/run/systemd/resolve/resolv.conf \
  --v=2

Restart=always
RestartSec=5
StartLimitInterval=0

[Install]
WantedBy=multi-user.target
```

**参考：**

- https://stackoverflow.com/questions/53075796/coredns-pods-have-crashloopbackoff-or-error-state/53414041#53414041
- https://github.com/kubernetes/minikube/issues/3511
- https://coredns.io/plugins/loop/#troubleshooting
