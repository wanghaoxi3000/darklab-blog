---
title: 'kafka学习笔记-搭建基于k8s的kafka测试环境'
categories:
  - kafka
tags:
  - kafka
  - k8s
toc: true
date: 2021-04-18 18:00:00
---

准备深入的学习下kafka，先从搭建一个开发环境，编写一个简单的测试程序开始吧。
<!-- more -->


## 搭建Kafka开发环境
使用如下的 Yaml 文件在K8S中搭建一个测试可用的 Kafka 实例。

**deployment.yaml**
```yaml
kind: Deployment
apiVersion: apps/v1
metadata:
  name: kafka-dev
  namespace: dev
  labels:
    app: kafka-dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kafka-dev
  template:
    metadata:
      labels:
        app: kafka-dev
      containers:
        - name: zookeeper
          image: 'docker.io/bitnami/zookeeper:3-debian-10'
          ports:
            - name: tcp-zookeeper
              containerPort: 2181
              protocol: TCP
          env:
            - name: ALLOW_ANONYMOUS_LOGIN
              value: 'yes'
          resources:
            limits:
              memory: 512Mi
          volumeMounts:
            - name: host-time
              readOnly: true
              mountPath: /etc/localtime
            - name: zookeeper-data
              mountPath: /bitnami
          imagePullPolicy: IfNotPresent
        - name: kafka
          image: 'docker.io/bitnami/kafka:2-debian-10'
          ports:
            - name: tcp-kafka
              containerPort: 9092
              protocol: TCP
          env:
            - name: KAFKA_CFG_ZOOKEEPER_CONNECT
              value: 'localhost:2181'
            - name: ALLOW_PLAINTEXT_LISTENER
              value: 'yes'
            - name: KAFKA_LISTENERS
              value: 'PLAINTEXT://:9092'
            - name: KAFKA_ADVERTISED_LISTENERS
              value: 'PLAINTEXT://192.168.50.35:9092'
          resources:
            limits:
              memory: 1Gi
          volumeMounts:
            - name: host-time
              readOnly: true
              mountPath: /etc/localtime
            - name: kafka-data
              mountPath: /bitnami
          imagePullPolicy: IfNotPresent
    spec:
      volumes:
        - name: host-time
          hostPath:
            path: /etc/localtime
            type: ''
        - name: zookeeper-data
          emptyDir: {}
        - name: kafka-data
          emptyDir: {}
```

**service.yaml**
```yaml
kind: Service
apiVersion: v1
metadata:
  name: kafka
  namespace: dev
  labels:
    app: kafka
  annotations:
    kubesphere.io/creator: admin
spec:
  ports:
    - name: tcp-kafka
      protocol: TCP
      port: 9092
      targetPort: 9092
      nodePort: 30667
  selector:
    app: kafka-dev
  clusterIP: 10.233.10.125
  type: NodePort
  externalIPs:
    - 192.168.50.35
  sessionAffinity: None
  externalTrafficPolicy: Cluster
```

为了方便部署，kafka和zookeeper部署到了同一个pod中，可以直接通过localhost来直接访问。另外需要注意的是 `KAFKA_ADVERTISED_LISTENERS` 要配置为一个外部可访问的地址，才能在集群外进行访问。这里使用我的机器地址`192.168.50.35`，在service.yaml中，同样需要配置上`externalIPs:[192.168.50.35]`，这样可以直接使用`192.168.50.35:9092`来访问kafka，而无需使用分配的nodePort端口号。


## 代码测试
通过编写一个生产者和消费者，来测试搭建的kafka测试环境是否可用。

### 编写 Kafka 生产者
使用 `gopkg.in/Shopify/sarama.v1` 库编写一个Golang版本的消息生产者，用同步模式向`web_log` Topic中发送一条`this is a test log`的消息。

**producer.go**

```golang
package main

import (
	"log"

	sarama "gopkg.in/Shopify/sarama.v1"
)

func main() {
	// 设置消费者相关配置
	config := sarama.NewConfig()

	config.Producer.RequiredAcks = sarama.WaitForAll          // 发送完数据需要leader和follow都确认
	config.Producer.Partitioner = sarama.NewRandomPartitioner // 选择分区（此处随机设置一个分区）
	config.Producer.Return.Successes = true                   // 成功交付的消息将在success channel返回
	config.Producer.Return.Errors = true

	// 构造⼀个消息
	msg := &sarama.ProducerMessage{}
	msg.Topic = "web_log"
	msg.Value = sarama.StringEncoder("this is a test log")

	// 连接kafka
	client, err := sarama.NewSyncProducer([]string{"192.168.50.35:9092"}, config)
	if err != nil {
		panic(err)
	}
	defer client.Close()

	// 发送消息
	pid, offset, err := client.SendMessage(msg)
	if err != nil {
		panic(err)
	}
	log.Printf("pid:%v offset:%v\n", pid, offset)
}
```

代码执行结果:
```
2021/04/12 20:25:02 pid:0 offset:3
```

### 编写 Kafka 消费者
再基于 `gopkg.in/Shopify/sarama.v1` 编写一个Golang的同步消费者客户端，客户端中创建了`c1`和`c2`两个客户端

**consumer.go**

```
package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"sync"

	"gopkg.in/Shopify/sarama.v1"
)

type consumerGroupHandler struct {
	name string
}

func (consumerGroupHandler) Setup(_ sarama.ConsumerGroupSession) error   { return nil }
func (consumerGroupHandler) Cleanup(_ sarama.ConsumerGroupSession) error { return nil }
func (h consumerGroupHandler) ConsumeClaim(sess sarama.ConsumerGroupSession, claim sarama.ConsumerGroupClaim) error {
	for msg := range claim.Messages() {
		fmt.Printf("%s Message topic:%q partition:%d offset:%d  value:%s\n", h.name, msg.Topic, msg.Partition, msg.Offset, string(msg.Value))
		// 手动确认消息
		sess.MarkMessage(msg, "")
	}
	return nil
}

func consume(group *sarama.ConsumerGroup, wg *sync.WaitGroup, name string) {
	fmt.Println(name + "start")
	wg.Done()
	ctx := context.Background()
	for {
		topics := []string{"web_log"}
		handler := consumerGroupHandler{name: name}
		err := (*group).Consume(ctx, topics, handler)
		if err != nil {
			panic(err)
		}
	}
}

func main() {
	config := sarama.NewConfig()
	config.Version = sarama.V0_10_2_0
	config.Consumer.Return.Errors = false
	config.Consumer.Offsets.Initial = sarama.OffsetOldest

	client, err := sarama.NewClient([]string{"192.168.50.35:9092"}, config)
	if err != nil {
		panic(err)
	}
	defer client.Close()

	group1, err := sarama.NewConsumerGroupFromClient("c1", client)
	if err != nil {
		panic(err)
	}
	defer group1.Close()

	group2, err := sarama.NewConsumerGroupFromClient("c2", client)
	if err != nil {
		panic(err)
	}
	defer group2.Close()

	var wg sync.WaitGroup

	wg.Add(2)
	go consume(&group1, &wg, "c1")
	go consume(&group2, &wg, "c2")
	wg.Wait()

	signals := make(chan os.Signal, 1)
	signal.Notify(signals, os.Interrupt)
	<-signals
}
```

代码执行结果:
```
c2 Message topic:"web_log" partition:0 offset:3  value:this is a test log
c1 Message topic:"web_log" partition:0 offset:3  value:this is a test log
```

Producer 发送到 Kafka 中的消息已被 Consumer 成功接收到。

## 总结
这里在k8s搭建了一个测试可用的kafka环境，并通过简单的生产者和消费者程序进行了测试，方便之后可以更深入的学习kafka。
