Azure messaging services

## 设计模式

[发布订阅模式与观察者模式 - SegmentFault 思否](https://segmentfault.com/a/1190000038881989#:~:text=发布订阅模式（Pub-Sub Pattern）&text=在现在的发布订阅,分发它们给订阅者。)

### 观察者模式和发布订阅模式有什么区别？

我们先来看下这两个模式的实现结构：
![模式结构](Azure messaging services.assets/1460000038881992.png)

**观察者模式：** 观察者（Observer）直接订阅（Subscribe）主题（Subject），而当主题被激活的时候，会触发（Fire Event）观察者里的事件。

**发布订阅模式：** 订阅者（Subscriber）把自己想订阅的事件注册（Subscribe）到调度中心（Topic），当发布者（Publisher）发布该事件（Publish topic）到调度中心，也就是该事件触发时，由调度中心统一调度（Fire Event）订阅者注册到调度中心的处理代码。



Eg：



```js
  //有一家猎人工会，其中每个猎人都具有发布任务(publish)，订阅任务(subscribe)的功能
    //他们都有一个订阅列表来记录谁订阅了自己
    //定义一个猎人类
    //包括姓名，级别，订阅列表
    function Hunter(name, level){
        this.name = name
        this.level = level
        this.list = []
    }
    Hunter.prototype.publish = function (money){
        console.log(this.level + '猎人' + this.name + '寻求帮助')
        this.list.forEach(function(item, index){
            item(money)
        })
    }
    Hunter.prototype.subscribe = function (targrt, fn){
        console.log(this.level + '猎人' + this.name + '订阅了' + targrt.name)
        targrt.list.push(fn)
    }
    
    //猎人工会走来了几个猎人
    let hunterMing = new Hunter('小明', '黄金')
    let hunterJin = new Hunter('小金', '白银')
    let hunterZhang = new Hunter('小张', '黄金')
    let hunterPeter = new Hunter('Peter', '青铜')
    
    //Peter等级较低，可能需要帮助，所以小明，小金，小张都订阅了Peter
    hunterMing.subscribe(hunterPeter, function(money){
        console.log('小明表示：' + (money > 200 ? '' : '暂时很忙，不能') + '给予帮助')
    })
    hunterJin.subscribe(hunterPeter, function(){
        console.log('小金表示：给予帮助')
    })
    hunterZhang.subscribe(hunterPeter, function(){
        console.log('小金表示：给予帮助')
    })
    
    //Peter遇到困难，赏金198寻求帮助
    hunterPeter.publish(198)
    
    //猎人们(观察者)关联他们感兴趣的猎人(目标对象)，如Peter，当Peter有困难时，会自动通知给他们（观察者）` 

**发布订阅模式：**
  //定义一家猎人工会
    //主要功能包括任务发布大厅(topics)，以及订阅任务(subscribe)，发布任务(publish)
    let HunterUnion = {
        type: 'hunt',
        topics: Object.create(null),
        subscribe: function (topic, fn){
            if(!this.topics[topic]){
                  this.topics[topic] = [];  
            }
            this.topics[topic].push(fn);
        },
        publish: function (topic, money){
            if(!this.topics[topic])
                  return;
            for(let fn of this.topics[topic]){
                fn(money)
            }
        }
    }
    
    //定义一个猎人类
    //包括姓名，级别
    function Hunter(name, level){
        this.name = name
        this.level = level
    }
    //猎人可在猎人工会发布订阅任务
    Hunter.prototype.subscribe = function (topic, fn){
        console.log(this.level + '猎人' + this.name + '订阅了狩猎' + topic + '的任务')
        HunterUnion.subscribe(topic, fn)
    }
    Hunter.prototype.publish = function (topic, money){
        console.log(this.level + '猎人' + this.name + '发布了狩猎' + topic + '的任务')
        HunterUnion.publish(topic, money)
    }
    
    //猎人工会走来了几个猎人
    let hunterMing = new Hunter('小明', '黄金')
    let hunterJin = new Hunter('小金', '白银')
    let hunterZhang = new Hunter('小张', '黄金')
    let hunterPeter = new Hunter('Peter', '青铜')
    
    //小明，小金，小张分别订阅了狩猎tiger的任务
    hunterMing.subscribe('tiger', function(money){
        console.log('小明表示：' + (money > 200 ? '' : '不') + '接取任务')
    })
    hunterJin.subscribe('tiger', function(money){
        console.log('小金表示：接取任务')
    })
    hunterZhang.subscribe('tiger', function(money){
        console.log('小张表示：接取任务')
    })
    //Peter订阅了狩猎sheep的任务
    hunterPeter.subscribe('sheep', function(money){
        console.log('Peter表示：接取任务')
    })
    
    //Peter发布了狩猎tiger的任务
    hunterPeter.publish('tiger', 198)
    
    //猎人们发布(发布者)或订阅(观察者/订阅者)任务都是通过猎人工会(调度中心)关联起来的，他们没有直接的交流。` 

观察者模式和发布订阅模式最大的区别就是发布订阅模式有个事件调度中心。

观察者模式由具体目标调度，每个被订阅的目标里面都需要有对观察者的处理，这种处理方式比较直接粗暴，但是会造成代码的冗余。

而发布订阅模式中统一由调度中心进行处理，订阅者和发布者互不干扰，消除了发布者和订阅者之间的依赖。这样一方面实现了解耦，还有就是可以实现更细粒度的一些控制。比如发布者发布了很多消息，但是不想所有的订阅者都接收到，就可以在调度中心做一些处理，类似于权限控制之类的。还可以做一些节流操作。

观察者模式是不是发布订阅模式
--------------

网上关于这个问题的回答，出现了两极分化，有认为发布订阅模式就是观察者模式的，也有认为观察者模式和发布订阅模式是真不一样的。

其实我不知道发布订阅模式是不是观察者模式，就像我不知道辨别模式的关键是设计意图还是设计结构（理念），虽然《JavaScript设计模式与开发实践》一书中说了`分辨模式的关键是意图而不是结构`。

如果以结构来分辨模式，发布订阅模式相比观察者模式多了一个中间件订阅器，所以发布订阅模式是不同于观察者模式的；如果以意图来分辨模式，他们都是`实现了对象间的一种一对多的依赖关系，当一个对象的状态发生改变时，所有依赖于它的对象都将得到通知，并自动更新`，那么他们就是同一种模式，发布订阅模式是在观察者模式的基础上做的优化升级。

```

[观察者模式 vs 发布订阅模式 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/51357583)

Azure Doc：

发布与订阅模式：

[发布者-订阅者模式 - Azure Architecture Center | Microsoft Docs](https://docs.microsoft.com/zh-cn/azure/architecture/patterns/publisher-subscriber)





## Basic



### Architecture

![Image showing how Event Hubs, Service Bus, and Event Grid can be connected together.](Azure messaging services.assets/overview.png)

[Azure 消息 & 事件服务的选择 – 上篇 | Azure Docs](https://docs.azure.cn/zh-cn/articles/azure-operations-guide/internet-of-things/aog-internet-of-things-howto-select-message-event-service-part-1)



### 事件与消息

需要注意传递事件的服务和传递消息的服务之间的重要区别。

**事件 Event** 
事件是条件或状态更改的轻量级通知。事件的发布者对事件的处理方式没有期望。事件的消费者决定如何处理通知。事件可以是离散单元或系列的一部分。

（An event is a lightweight notification of a condition or a state change. The publisher of the event has no expectation about how the event is handled. The consumer of the event decides what to do with the notification. Events can be discrete units or part of a series.）

离散事件报告状态变化并且是可操作的。要进行下一步，消费者只需要知道发生了一些事情。事件数据有关于发生了什么的信息，但没有触发事件的数据。例如，事件通知消费者文件已创建。它可能有关于文件的一般信息，但它没有文件本身。离散事件非常适合需要扩展的无服务器解决方案。

（Discrete events report state change and are actionable. To take the next step, the consumer only needs to know that something happened. The event data has information about what happened but doesn't have the data that triggered the event. For example, an event notifies consumers that a file was created. It may have general information about the file, but it doesn't have the file itself. Discrete events are ideal for serverless solutions that need to scale.）

系列事件报告一个条件并且是可分析的。事件按时间顺序排列且相互关联。消费者需要按顺序排列的一系列事件来分析发生了什么。

（A series of events report a condition and are analyzable. The events are time-ordered and interrelated. The consumer needs the sequenced series of events to analyze what happened.）

事件用来描述程序的运行状态或环境的改变。例如鼠标移动、用户按键、窗口状态的改变、时钟计时、线程结束等等等等。 

**消息 Message**
消息是服务产生的原始数据，用于消费或存储在其他地方。消息包含触发消息管道的数据。消息的发布者对消费者如何处理消息有预期。双方之间存在合同。例如，发布者发送带有原始数据的消息，并期望消费者根据该数据创建一个文件，并在工作完成后发送响应。

（A message is raw data produced by a service to be consumed or stored elsewhere. The message contains the data that triggered the message pipeline. The publisher of the message has an expectation about how the consumer handles the message. A contract exists between the two sides. For example, the publisher sends a message with the raw data, and expects the consumer to create a file from that data and send a response when the work is done.）

消息实际上是一种通信的机制。操作系统往往会利用消息来通知应用程序某个事件的发生，但这并不意味着消息与事件就是一一对应的或者说是相当的。  
  例如，应用程序完全可以自己直接来监视某个事件的发生并对其做出响应，而不依赖于消息；反之，应用程序也可以在没有事件发生的情况下发送消息，完成通信的功能，或者模拟一次事件。

**更多区别描述**

事件是一个动作——用户触发的动作。   

消息是一个信息——传递给系统的信息。    

事件与消息的概念在计算机中较易混淆，但本质不同：  

事件由用户（操作电脑的人）触发且只能由用户触发，操作系统能够感觉到由用户触发的事件，并将此事件转换为一个（特定的）消息发送到程序的消息队列中。  

  这里强调的是：   

  可以说“用户触发了一个事件”，而不能说“用户触发了一个消息”。   

  用户只能触发事件，而事件只能由用户触发。   

  一个事件产生后，将被操作系统转换为一个消息，所以一个消息可能是由一个事件转换而来（或者由操作系统产生）。   

  一个消息可能会产生另一个消息，但一个消息决不能产生一个事件——时间只能由用户触发。     总结（事件：消息的来源）  

  事件：只能由用户通过外设的输入产生。 
  消息：（产生消息的来源有三个）   

  （1）   由操作系统产生。   

  （2）   由用户触发的事件转换而来。   

  （3）   由另一个消息产生。




### Comparison of services

| Service     | Purpose                         | Type                          | When to use                                 |
| :---------- | :------------------------------ | :---------------------------- | :------------------------------------------ |
| Event Grid  | Reactive programming            | Event distribution (discrete) | React to status changes                     |
| Event Hubs  | Big data pipeline               | Event streaming (series)      | Telemetry and distributed data streaming    |
| Service Bus | High-value enterprise messaging | Message                       | Order processing and financial transactions |

More：[Events, Data Points, and Messages - Choosing the right Azure messaging service for your data | Azure Blog and Updates | Microsoft Azure](https://azure.microsoft.com/en-us/blog/events-data-points-and-messages-choosing-the-right-azure-messaging-service-for-your-data/)

- **Azure 事件网格**——事件驱动的发布订阅模型（想想反应式编程）
- **Azure 事件中心**——多源大数据流管道（想想遥测数据）
- **Azure 服务总线**——传统的企业代理消息系统（取代 Azure 队列存储）



**事件网格和事件中心之间的区别**

1. 事件网格不保证事件的顺序，但事件中心使用有序序列的分区，因此它可以维护同一分区中事件的顺序。
2. 事件中心仅接受用于摄取数据的端点，并且不提供将数据发送回发布者的机制。另一方面，事件网格发送 HTTP 请求来通知发布者中发生的事件。
3. 事件网格可以触发 Azure 函数。对于事件中心，Azure 函数需要拉取和处理事件。
4. 事件网格是一种分发系统，而不是一种排队机制。如果一个事件被推入，它会立即被推出，如果它没有得到处理，它就永远消失了。除非我们将未传递的事件发送到存储帐户。这个过程被称为死信。
5. 在事件中心，数据最多可以保留 7 天，然后重播。这使我们能够从某个点恢复或从较旧的时间点重新启动并在需要时重新处理事件。

**事件中心和服务总线之间的区别**

对于外部发布者或接收者来说，服务总线和事件中心看起来非常相似，这就是很难理解两者之间的区别以及何时使用什么的原因。

1. 事件中心专注于事件流，其中服务总线更像是一个传统的消息传递代理。
2. 服务总线用作将在云中运行的应用程序连接到其他应用程序或服务并在它们之间传输数据的主干，而事件中心则更关心接收具有高吞吐量和低延迟的海量数据。
3. 事件中心将多个事件生成器与事件接收器分离，而服务总线旨在分离应用程序。
4. 服务总线消息传递支持消息属性“生存时间”，而事件中心的默认保留期为 7 天。
5. 服务总线具有消息会话的概念。它允许根据会话 ID 属性关联消息，而事件中心则不允许。
6. 服务总线消息被接收器拉出并且无法再次处理，而事件中心消息可以被多个接收器摄取。
7. 服务总线使用队列和主题的术语，而使用事件中心分区术语。



## [Azure Service Bus](https://www.cnblogs.com/AllenMaster/p/14000933.html)

[Azure Service Bus（一）入门简介 - Grant_Allen - 博客园 (cnblogs.com)](https://www.cnblogs.com/AllenMaster/p/14000933.html)

Azure Service Bus：是微软在Azure 上提供的一种 ”云消息服务“，在应用和服务之间传递消息时，即使消息的接受着处于脱机状态下，也不影响接收者在联机后接收信息。保证了消息数据的可靠性和持久性，同时数据通过消息在不同的应用程序和服务之间传输。 消息采用二进制格式，可能包含 JSON、XML 或纯文本。但是缺点就是成本和消息大小。Azure Service Bus 队列消息必须大于 64KB，同时还必须小于 256KB



这时候有人就说了，那 Azure Storage Queue 和Azure Service Bus 有啥区别？

　　Azure Storage Queue：允许我们存储大量的消息可以被使用者读取，并且队列消息非常灵活，如果初始使用者出现故障，则可以由不同的消费进程再次处理。队列可以在消费者之间保存状态。

　　Azure Service Bus：服务总线队列提供了一个代理消息通信模型。分布式应用程序可以在一个FIFO 模式中共享消息，同时单个消息只能由一个消息使用者接收。

| **Storage Queues**      | **Service Bus Queues** |
| ----------------------- | ---------------------- |
| 任意排序                | 使用FIFO保证排序       |
| 交付至少一次, 可能多次  | 至少交付一次，最多一次 |
| 30秒默认锁可以延长到7天 | 60秒的默认锁可以续订   |
| 支持就地更新消息内容    | 消息在一次消费后被删除 |
| 可以与 WF 集成          | 与 WCF和WF本地集成     |



**1.What's the message service**



**2.How many types of Azure message Service**



**3.What's the difference between message and event**



**4.What's the service bus**
**5.What's the service bus queue, topic**
**6.What's the difference between queue and topic**



**7.What's the relay**
**8.What the feature does relay provide**
**9.What's the difference between service bus and event hub**
**10.Can service bus guarantee the message order? Why**
**11.Can event hub guarantee the event order? Why**
**12.What's the event grid**
**13.How to restrict a client as only send / listen**
**14.What's the mechanism Service bus / event hub used to service concurrency**
**15.How many connection protocols do service bus / event hub support**