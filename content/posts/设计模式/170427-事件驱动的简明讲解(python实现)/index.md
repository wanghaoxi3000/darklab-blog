---
title: 事件驱动的简明讲解(python实现)
date: 2017-04-27 23:02:00
categories:
- 设计模式
toc: true
slug: Brief-explanation-of-event-driven-(Python-Implementation)
---

转载至[http://www.cnblogs.com/thinkroom/p/6729480.html](http://www.cnblogs.com/thinkroom/p/6729480.html) 作者：码匠信龙

举个简单的例子：

有些人喜欢的某个公众号，然后去关注这个公众号，哪天这个公众号发布了篇新的文章，没多久订阅者就会在微信里收到这个公众号推送的新消息，如果感兴趣就打开来阅读。

![image](http://cdn.thinkingroom.me/%E5%85%AC%E4%BC%97%E5%8F%B7%E4%BE%8B%E5%AD%90.png?_=6729480)

事件驱动模型可以理解为上面的例子，是设计模式中观察者模式的一种典型应用。除了订阅公众号外，如你关注某人的微博，关注某人的简书，当被关注者发了个新状态或者新文章，你会收到他们新的消息，这些都可以理解为事件驱动模型。

实际上，世间万物各种属性的变化，我们都可以抽象为事件，最直观的是图形界面应用里，如常见的点击、双击、拖动操作，又或者是游戏里的英雄升级了，怪物死亡了等等，都可以视为一个事件发生了。而发送事件的事物称为事件源，对这个事件感兴趣的事物为监听者，事件发生后监听者会收到这个消息，然后做相应的反应。

例如上面公众号例子可以翻译为，监听器（订阅者）监听了（关注了）事件源（公众号），当事件源的发送事件时（公众号发布文章），所有监听该事件的监听器（订阅者）都会接收到消息并作出响应（阅读文章）。

1. 公众号为事件源
2. 订阅者为事件监听器
3. 订阅者关注公众号，相当于监听器监听了事件源
4. 公众号发布文章这个动作为发送事件
5. 订阅者收到事件后，做出阅读文章的响应动作

公众号例子按事件驱动可以理解成下图

![image](http://cdn.thinkingroom.me/%E5%85%AC%E4%BC%97%E5%8F%B7%E4%BE%8B%E5%AD%90%E7%BF%BB%E8%AF%91.png?_=6729480!)

所以事件驱动模式可以进一步抽象理解为由事件源，事件对象，以及事件监听器三元素构成，能完成监听器监听事件源、事件源发送事件，监听器收到事件后调用响应函数的动作。

事件驱动主要包含以下元素和操作函数：

**元素**
1. 事件源
2. 事件监听器
3. 事件对象

**操作函数**
4. 监听动作
5. 发送事件
6. 调用监听器响应函数

了解清楚了事件驱动的工作原理后，读者可以试着用自己熟悉的编程语言实现，编程主要实现下面的内容，笔者后续给python实现：

用户根据实际业务逻辑定义
- 事件源 EventSources
- 监听器 Listeners

事件管理者 EventManager

**成员**
1. 响应函数队列 Handlers
2. 事件对象 Event
3. 事件对象列表 EventQueue

**操作函数**
4. 监听动作 AddEventListener
5. 发送事件 SendEvent
6. 调用响应函数 EventProcess

在实际的软件开发过程中，你会经常看到事件驱动的影子，几乎所有的GUI界面都采用事件驱动编程模型，很多服务器网络模型的消息处理也会采用，甚至复杂点的数据库业务处理也会用这种模型，因为这种模型解耦事件发送者和接收者之间的联系，事件可动态增加减少接收者，业务逻辑越复杂，越能体现它的优势。下面，笔者用python实现EventManager事件管理类，大概就百来行代码左右。

```
# encoding: UTF-8
# 系统模块
from Queue import Queue, Empty
from threading import *
########################################################################
class EventManager:
    #----------------------------------------------------------------------
    def __init__(self):
        """初始化事件管理器"""
        # 事件对象列表
        self.__eventQueue = Queue()
        # 事件管理器开关
        self.__active = False
        # 事件处理线程
        self.__thread = Thread(target = self.__Run)

        # 这里的__handlers是一个字典，用来保存对应的事件的响应函数
        # 其中每个键对应的值是一个列表，列表中保存了对该事件监听的响应函数，一对多
        self.__handlers = {}

    #----------------------------------------------------------------------
    def __Run(self):
        """引擎运行"""
        while self.__active == True:
            try:
                # 获取事件的阻塞时间设为1秒
                event = self.__eventQueue.get(block = True, timeout = 1)  
                self.__EventProcess(event)
            except Empty:
                pass

    #----------------------------------------------------------------------
    def __EventProcess(self, event):
        """处理事件"""
        # 检查是否存在对该事件进行监听的处理函数
        if event.type_ in self.__handlers:
            # 若存在，则按顺序将事件传递给处理函数执行
            for handler in self.__handlers[event.type_]:
                handler(event)

    #----------------------------------------------------------------------
    def Start(self):
        """启动"""
        # 将事件管理器设为启动
        self.__active = True
        # 启动事件处理线程
        self.__thread.start()

    #----------------------------------------------------------------------
    def Stop(self):
        """停止"""
        # 将事件管理器设为停止
        self.__active = False
        # 等待事件处理线程退出
        self.__thread.join()

    #----------------------------------------------------------------------
    def AddEventListener(self, type_, handler):
        """绑定事件和监听器处理函数"""
        # 尝试获取该事件类型对应的处理函数列表，若无则创建
        try:
            handlerList = self.__handlers[type_]
        except KeyError:
            handlerList = []
            
        self.__handlers[type_] = handlerList
        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handlerList:
            handlerList.append(handler)
            
    #----------------------------------------------------------------------
    def RemoveEventListener(self, type_, handler):
        """移除监听器的处理函数"""
        #读者自己试着实现
        
    #----------------------------------------------------------------------
    def SendEvent(self, event):
        """发送事件，向事件队列中存入事件"""
        self.__eventQueue.put(event)

########################################################################
"""事件对象"""
class Event:
    def __init__(self, type_=None):
        self.type_ = type_      # 事件类型
        self.dict = {}          # 字典用于保存具体的事件数据
```

测试代码
```
#-------------------------------------------------------------------
# encoding: UTF-8
import sys
from datetime import datetime
from threading import *
from EventManager import *

#事件名称  新文章
EVENT_ARTICAL = "Event_Artical"

#事件源 公众号
class PublicAccounts:
    def __init__(self,eventManager):
        self.__eventManager = eventManager

    def WriteNewArtical(self):
        #事件对象，写了新文章
        event = Event(type_=EVENT_ARTICAL)
        event.dict["artical"] = u'如何写出更优雅的代码\n'
        #发送事件
        self.__eventManager.SendEvent(event)
        print u'公众号发送新文章\n'

#监听器 订阅者
class Listener:
    def __init__(self,username):
        self.__username = username

    #监听器的处理函数 读文章
    def ReadArtical(self,event):
        print(u'%s 收到新文章' % self.__username)
        print(u'正在阅读新文章内容：%s'  % event.dict["artical"])

"""测试函数"""
#--------------------------------------------------------------------
def test():
    listner1 = Listener("thinkroom") #订阅者1
    listner2 = Listener("steve")#订阅者2

    eventManager = EventManager()
    
    #绑定事件和监听器响应函数(新文章)
    eventManager.AddEventListener(EVENT_ARTICAL, listner1.ReadArtical)
    eventManager.AddEventListener(EVENT_ARTICAL, listner2.ReadArtical)
    eventManager.Start()

    publicAcc = PublicAccounts(eventManager)
    timer = Timer(2, publicAcc.WriteNewArtical)
    timer.start()
    
if __name__ == '__main__':
    test()
```