# iOS摸鱼周报 第十期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享大家开发过程遇到的经验教训及学习内容。虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug经历。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips

### 可以自动释放的单例
单例的优点是可以全局共享状态，无需重复建立对象。然而缺点也非常明显，滥用可能会引起内存问题，因为单例对象一旦建立，生命周期就变得和App一样长，在App被kill掉之前无法释放。
很多情况下，开发者并不希望生命周期这么长。这里推荐一种使用week关键字定义的单例对象，能巧妙做到在其使用者都释放时做到自动释放。
OC代码如下：
```
+ (instancetype)sharedInstance {
    static __weak __className *instance;
    __className *strongInstance = instance;
    @synchronized(self) {
        if (!strongInstance) {
            strongInstance = [[__className alloc] init];
            instance = strongInstance;
        }
    }
    return strongInstance;
}

```
也可以抽成宏定义：
```
//可以自动释放的单例
#define SINGLETON_H     +(instancetype)sharedInstance;

#define SINGLETON_AUTORELEASE_M(__class) \
+ (instancetype)sharedInstance {\
    static __weak __class *instance;\
    __class *strongInstance = instance;\
    @synchronized(self) {\
        if (!strongInstance) {\
            strongInstance = [[__class alloc] init];\
            instance = strongInstance;\
        }\
    }\
    return strongInstance;\
}

```

值得注意的是，使用这种方式定义的单例对象时，需要想明白希望该单例对象存活多久，从而选择合适的“父对象”持有该单例，不然该单例对象有可能提前释放。


## 那些Bug

### iOS 蓝牙设备名称缓存问题总结

整理编辑：[FBY展菲](https://juejin.cn/user/3192637497025335/posts)

**问题背景**

当设备已经在 App 中连接成功后，修改设备名称，App 扫描到的设备名称仍然是之前的名称（App 代码中获取名称的方式为 `perpheral.name`）。

**问题分析**

当以 APP 为中心连接其他的蓝牙设备时。首次连接成功过后，iOS系统内会将该外设缓存记录下来。下次重新搜索，得到的蓝牙设备名称 `peripheral.name`，直接打印得到的是之前缓存中的名称。

如果此期间蓝牙设备更新了名称，`peripheral.name` 这个参数并不会改变，所以需要换一种方式获取设备的名称，在广播数据包内有一个字段为 `kCBAdvDataLocalName`，可以实时获取当前设备名称。

**问题解决**

下面给出OC 和 Swift 的解决方法：

OC
```objectivec
-(void)centralManager:(CBCentralManager *)central didDiscoverPeripheral:(CBPeripheral *)peripheral advertisementData:(NSDictionary<NSString *,id> *)advertisementData RSSI:(NSNumber *)RSSI{
    NSString *localName = [advertisementData objectForKey:@"kCBAdvDataLocalName"];
} 
```
Swift

```swift
func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {
    let localName = advertisementData["kCBAdvDataLocalName"]
}
```

## 编程概念

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)

本期选题来源于林永坚的 [iOS开发进阶](https://t8.lagounews.com/dR5FRrRtcO4F8) 课程里的「跨平台架构：如何设计 BFF 架构系统？」这一节内容。如有表述不准确的地方，欢迎指出，定会随时改正。

### 什么是 RESTful

RESTful 里的 REST 是 Representational State Transfer 的缩写，翻译过来就是：表现层状态转化。它是一种互联网软件架构，处理的问题是如何开发在互联网环境中使用的软件。

从含义入手：表现层状态转化。表现层是互联网资源呈现的形式，例如 HTML，JSON 等，转化就是资源等数据的变化，查询数据，更新数据。

RESTful 架构一般满足以下三点即可：

1、一个 URI 代表一种资源

2、客户端和服务器之间，传递这种资源的某种表现层

3、客户端通过 4 个 HTTP 动词，对服务器端资源进行操作，实现“表现层状态转化“。

参考：[理解 RESTful 架构 - 阮一峰](https://www.ruanyifeng.com/blog/2011/09/restful.html "理解 RESTful 架构")

### 什么是 SOAP

SOAP，全称是 Simple Object Access Protocol，即简单对象访问协议。从 W3C SOAP 1.2 版开始，SOAP 这一缩写不再代表 Simple Object Access Protocol，而是仅仅作为协议名称而已。

SOAP 是一种相对古老（比 REST 还要早）的网络通信协议，它主是基于 XML 进行传输的。SOAP 和 REST 是早期互联网应用常用的两种方案。

对于应用程序开发来说，使程序之间进行因特网通信是很重要的。目前的应用程序通过使用远程过程调用（RPC）在诸如 DCOM 与 CORBA 等对象之间进行通信，但是 HTTP 不是为此设计的。RPC 会产生兼容性以及安全问题；防火墙和代理服务器通常会阻止此类流量。通过 HTTP 在应用程序间通信是更好的方法，因为 HTTP 得到了所有的因特网浏览器及服务器的支持。SOAP 就是被创造出来完成这个任务的。SOAP 提供了一种标准的方法，使得运行在不同的操作系统并使用不同的技术和编程语言的应用程序可以互相进行通信。

参考：[SOAP 简介 - 菜鸟](https://www.runoob.com/soap/soap-intro.html "SOAP 简介 - 菜鸟")

### 什么是 BFF

BFF，全称是 Backend For Frontend，即服务于前端的后端，它是一种解决 REST 接口数据冗余的架构模型。

在 REST 模型下每个接口都对于一个服务器请求，当出现多个端，接口越来越多的情况该架构会面临很多问题。而BFF 就是用于解决这类问题出现的。

你可以把 BFF 当作一个中间层，而引入 BBF 后，前端只需要向 BFF 发送一个请求，由 BFF 与后端进行交互，然后将返回值整合后返回给前端，降低前端与后端之间的耦合，方便前端接入。除了整合数据外，你还可以在 BFF 层对数据进行裁剪过滤，或者其他业务逻辑处理，而不用在多个前端中做相同的工作。当后端发生变化时，你只需要在 BFF 层做相应的修改，而不用修改多个前端，这极大地减少了的工作量。

随着业务的发展，单个 BFF 为了适配多端的差异可能会变得越来越臃肿，可维护性降低，开发成本也会越来越高。这时候就得考虑为对 BFF 层进行拆分，给每种用户体验不同的前端分别对应一个 BFF，比如 PC BFF、移动端 BFF（或者再细拆为 iOS BFF 和 Android BFF） 等等，所以 BFF 也称为面向特定用户体验的适配层。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210430111611.png)

参考：[BFF —— Backend For Frontend](https://www.jianshu.com/p/eb1875c62ad3 "BFF —— Backend For Frontend")

### 什么是 GraphQL

GraphQL（展开为 Graph Query Language）是 Facebook 开发的应用层查询语言，于 2015 年开源。注意这里是查询语言，跟 SQL 的 Structured Query Language 类似，也是一种 DSL。

>  GraphQL 的本质是程序员想对 JSON 使用 SQL。 —— 来自阮一峰的翻译

它是一种 BFF 的实现方案。REST 数据是通过一个个 URI 定位到的，而 GraphQL 的模型更像是对象模型。GraphQL 对你的 API 中的数据提供了一套易于理解的完整描述，使得客户端能够准确地获得它需要的数据，而且没有任何冗余，也让 API 更容易地随着时间推移而演进，还能用于构建强大的开发者工具。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/33034116-558F-40ED-B191-31D9E28715F2.png)

这里 GraphQL 起的是一个 API 网关的作用。

参考：[GraphQL](https://graphql.cn/ "GraphQL")

### 什么是 RPC

RPC，全称是 Remote Procedure Call，即远程过程调用。RPC 是一种进程间通信方式，它允许客户端应用直接调用另一台远程不同计算机上的服务端应用的方法，而不需要了解远程调用的实际通信细节实现。RPC 会做好数据的序列化和传输，使得远程调用就像本地调用一样方便，让创建分布式应用和服务变得更加简单。促使 RPC 诞生的领域既是分布式。

RPC 的工作流程大致是：客户端应用以本地调用的方式发起远程调用，将参数以及附加信息序列化为能够进行网络传输的消息体，并将消息发送给服务端。服务端对收到的消息进行反序列化后执行请求，然后将结果序列化为消息并返回给客户端。最后客户端接收到消息并反序列化得到数据。

![](https://user-gold-cdn.xitu.io/2017/11/23/15fe93fb307ec7e9?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

> RPC 框架可以看作一种代理模式，GoF 的《设计模式》一书中把它称作远程代理。通过远程代理，将网络通信、数据编解码等细节隐藏起来。客户端在使用 RPC 服务的时候，就像使用本地函数一样，无需了解跟服务器交互的细节。除此之外，RPC 服务的开发者也只需要开发业务逻辑，就像开发本地使用的函数一样，不需要关注跟客户端的交互细节。 —— 来自王争的《设计模式之美》

常见的 RPC 框架有：gRPC、Dubbo、rpcx、Motan、thrift、brpc、Tars 等等。


### 什么是 gRPC

gRPC 是 Google 开发的一个高性能、通用的开源 RPC 框架。它使用 HTTP/2 作为传输协议，protocol buffers 作为底层传输格式（默认），protocol buffers 还可以作为接口描述语言。

在 gRPC 里客户端应用可以像调用本地对象一样直接调用另一台不同的机器上服务端应用的方法，使得您能够更容易地创建分布式应用和服务。与许多 RPC 系统类似，gRPC 也是基于以下理念：定义一个服务，指定其能够被远程调用的方法（包含参数和返回类型）。在服务端实现这个接口，并运行一个 gRPC 服务器来处理客户端调用。在客户端拥有一个存根能够像服务端一样的方法。

![](https://www.grpc.io/img/landing-2.svg)

gRPC 客户端和服务端可以在多种环境中运行和交互 -- 从 Google 内部的服务器到你自己的笔记本，并且可以用任何 gRPC 支持的语言来编写。所以，你可以很容易地用 Java 创建一个 gRPC 服务端，用 Go、Python、Ruby 来创建客户端。此外，Google 最新 API 将有 gRPC 版本的接口，使你很容易地将 Google 的功能集成到你的应用里。

Facebook 的调试工具 [idb](https://fbidb.io/)（作为 WebDriverAgent 的替代者）里的 `idb_companion` 就是一个 gRPC 服务器。

参考：[what-is-grpc](https://grpc.io/docs/what-is-grpc/introduction/ "what-is-grpc")




## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)

1、[iOS14.5隐私追踪功能现重大bug！IDFA选项变灰且无法开启(附解决方案)](https://mp.weixin.qq.com/s/rqzI3iiwdPxtWyP8q4wXJg "iOS14.5隐私追踪功能现重大bug！IDFA选项变灰且无法开启（附解决方案") -- 来自公众号：七麦研究院

千呼万唤始出来——iOS14.5上线了。

2、[Swift 2021 生态调研报告](https://mp.weixin.qq.com/s/5SXAozM2c6Ivyzl7B9IfQQ "Swift 2021 生态调研报告") -- 来自公众号： 一瓜技术

Swift崛起一直是大家的共识，但是缺少量化数据。本文对Swift的覆盖量做了细致的分析，从数据层面可以分析Swift的形势。对开发者学习和转型有非常积极的意义。

3、[学会黑科技，一招搞定 iOS 14.2 的 libffi crash](https://mp.weixin.qq.com/s/XLqcCfcNhpCA8Tg6LknBCQ "学会黑科技，一招搞定 iOS 14.2 的 libffi crash") -- 来自公众号： 字节跳动技术团队

本文主要介绍了libffi在iOS14.2上崩溃的原因以及解决方案。如果有相关问题，可以参考本文解决。

4、[libffi探究](https://juejin.cn/post/6844904177609490440 "libffi探究") -- 来自掘金：酱了里个酱

如果对libffi不是很了解，可以通过本文来了解和认识下libffi。

5、[CALayer 的 filters](https://juejin.cn/post/6938583362093187086 "CALayer 的 filters") -- 来自掘金：rickytan

相信很多同学都遇到了哀悼模式黑白色的问题，本文介绍了一种快速便捷的方式，不过存在被拒风险，大家可以灵活把控。

6、[从底层分析一下存在跨进程通信问题的 NSUserDefaults 还能用吗？](https://mp.weixin.qq.com/s/Y1AHFN1kJ9kCjXdFOnUviA "从底层分析一下存在跨进程通信问题的 NSUserDefaults 还能用吗？") -- 来自公众号：酷酷的哀殿

之前字节的文章介绍了卡死的几种情况，其中包括NSUserDefaults造成的卡死。本文深入分析了NSUserDefaults造成卡死的原因以及用法。

7、[用树莓派打造一个超薄魔镜的简单教程](https://onevcat.com/2021/04/magicmirror/ "用树莓派打造一个超薄魔镜的简单教程") -- 来自博客：OneV's Den

看喵神如何使用树莓派 + 单向玻璃 + 显示器打造一个魔镜。实现原理是：贴紧墙面的一侧无光，类似监控室；我们生活的空间光线较为充足，类似被监控房间；在镜子后方屏幕发出的光，相当于“改善”了镜子内侧的光线条件，这部分光透过镜子，被我们看到，从而形成“镜中屏”的效果。




## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### [LearnOpenGL CN](https://learnopengl-cn.github.io/)

欢迎来到 OpenGL 的世界。这个工程只是我([Joey de Vries](http://joeydevries.com/))的一次小小的尝试，希望能够建立起一个完善的 OpenGL 教学平台。无论你学习 OpenGL 是为了学业，找工作，或仅仅是因为兴趣，这个网站都将能够教会你现代(Core-profile)  OpenGL 从基础，中级，到高级的知识。LearnOpenGL 的目标是使用易于理解的形式，使用清晰的例子，展现现代 OpenGL 的所有知识点，并与此同时为你以后的学习提供有用的参考。

> 该教程是[原教程](https://learnopengl.com/)的中文翻译教程

### [VisuAlgo](https://visualgo.net/en)

由新加坡国立大学的教授和学生发起、制作并完善的「数据结构和算法动态可视化」网站，在该网站你可以看到许多经典、非经典的，常见的、非常见的算法的可视化，清晰明了的图形化表现和实时的代码解读可以帮助读者更好地理解各种算法及数据结构。同时该网站支持自动问题生成器和验证器（在线测验系统）。

![Animation of Graph Traversal Algorithm](https://www.comp.nus.edu.sg/images/resources/20200309-graph-traversal.gif)

### [Announcing our Deprecated Books Repo!](https://www.raywenderlich.com/21965623-announcing-our-deprecated-books-repo)

raywenderlich 是一个学习编程的网站，他们有很大一部分课程和 `iOS` / `Swift` 有关。最近他们开源了一批将要被废弃的书籍。笔者看过其中的 `2D Games`、`3D Games`、`ARKit` 等书籍，其中介绍了 `SpriteKit` 和 `SceneKit` 的相关知识，书本会带着读者循序渐进，了解这些框架的原理以及如何应用。这次名单中还包含了 `Unity AR & VR`、`Realm` 和 `Server Side` 相关的书籍，这些书对于想要学习这些特定领域内容的读者来说是很好的选择。



## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

### SwitchHosts

**地址**：https://swh.app/zh/

**软件状态**：[开源](https://github.com/oldj/SwitchHosts)，免费

**使用介绍**

SwitchHosts 是一个管理、切换多个 hosts 方案的工具。它支持多个Host方案的不同组合；支持导入导出，方便协作分享；还可以通过Alfred插件进行快速切换。
![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210430084948.png)

### DevUtils

**地址**：https://devutils.app/

**软件状态**：[开源](https://github.com/DevUtilsApp/DevUtils-app)，部分功能付费

**使用介绍**

DevUtils是一个开源的开发工具聚合的应用。它包含了常用的时间戳解析，JSON格式化，Base64编解码，正则表达式测试等功能。有了它我们就可以放弃掉站长之家，各种JSON格式化网站的使用了。

大家如果不想付费，直接下源码，关掉付费验证就行。如果觉得软件有帮助且有支付能力的话希望还是可以支持下作者。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210430085707.png)

## 联系我们

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

[摸鱼周报第六期](https://zhangferry.com/2021/03/14/iOSWeeklyLearning_6/)

[摸鱼周报第七期](https://zhangferry.com/2021/03/28/iOSWeeklyLearning_7/)

[摸鱼周报第八期](https://zhangferry.com/2021/04/11/iOSWeeklyLearning_8/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
