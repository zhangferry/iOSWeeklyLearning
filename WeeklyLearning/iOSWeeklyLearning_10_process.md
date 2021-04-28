# iOS摸鱼周报 第十期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享大家开发过程遇到的经验教训及学习内容。虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug经历。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips



## 那些Bug

### iOS 蓝牙设备名称缓存问题总结

整理编辑：[FBY展菲](https://juejin.cn/user/3192637497025335/posts)

**问题背景**

* 当设备已经在 App 中连接成功后
* 修改设备名称
* App 扫描到的设备名称仍然是之前的名称
* App 代码中获取名称的方式为（perpheral.name）

**问题分析**

当 APP 为中心连接其他的蓝牙设备时。

首次连接成功过后，iOS系统内会将该外设缓存记录下来。

下次重新搜索时，搜索到的蓝牙设备时，直接打印 （peripheral.name），得到的是之前缓存中的蓝牙名称。

如果此期间蓝牙设备更新了名称，（peripheral.name）这个参数并不会改变，所以需要换一种方式获取设备的名称，在广播数据包内有一个字段为 kCBAdvDataLocalName，可以实时获取当前设备名称。

**问题解决**

下面给出OC 和 Swift 的解决方法：

OC

```
-(void)centralManager:(CBCentralManager *)central didDiscoverPeripheral:(CBPeripheral *)peripheral advertisementData:(NSDictionary<NSString *,id> *)advertisementData RSSI:(NSNumber *)RSSI{
        NSString *localName = [advertisementData objectForKey:@"kCBAdvDataLocalName"];
} 
```

Swift

```
func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {
        let localName = advertisementData["kCBAdvDataLocalName"]
}
```

## 编程概念

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)

### 什么是 BFF

BFF，全称是 Backend For Frontend，即服务于前端的后端。BFF 是一种架构。

你可以把 BFF 当作一个中间层，原先前端某个页面可能需要向后端发送多个请求，并将这多个返回结果用于渲染一个页面。而引入 BBF 后，前端只需要向 BFF 发送一个请求，由 BFF 与后端进行交互，然后将返回值整合后返回给前端，降低前端与后端之间的耦合，方便前端接入。除了整合数据外，你还可以在 BFF 层对数据进行裁剪过滤，或者其他业务逻辑处理，而不用在多个前端中做相同的工作。当后端发生变化时，你只需要在 BFF 层做相应的修改，而不用修改多个前端，这极大地减少了的工作量。

随着业务的发展，单个 BFF 为了适配多端的差异可能会变得越来越臃肿，可维护性降低，开发成本也会越来越高。这时候就得考虑为对 BFF 层进行拆分，给每种用户体验不同的前端分别对应一个 BFF，比如 PC BFF、移动端 BFF（或者再细拆为 iOS BFF 和 Android BFF） 等等，所以 BFF 也称为面向特定用户体验的适配层。

要实现 BFF 架构，你可以使用 GraphQL，REST 等技术。

![配图](https://upload-images.jianshu.io/upload_images/3100944-f5d383cf1d142e29.png?imageMogr2/auto-orient/strip|imageView2/2/w/627/format/webp)

图片来源：https://www.jianshu.com/p/eb1875c62ad3

### 什么是 RPC

有两种进程间通信方式（IPC，Inter-Process Communication）：LPC 和 RPC。

LPC，全称是 Local Procedure Cal，即本地过程调用。LPC 的基础是以下提到的 RPC，LPC 对在同一台计算机上运行的进程间通讯进行了优化。

RPC，全称是 Remote Procedure Call，即远程过程调用。它允许客户端应用直接调用另一台远程不同计算机上的服务端应用的方法，而不需要了解远程调用的实际通信细节实现，使得远程调用就像本地调用一样方便。RPC 让创建分布式应用和服务变得更加简单。

从发起远程调用到接收到数据返回结果，大致过程是：

1. 服务消费方（client）调用以本地调用方式调用服务；
2. client stub 接收到调用后负责将方法、参数等组装成能够进行网络传输的消息体；
3. client stub 找到服务地址，并将消息发送到服务端；
4. server stub 收到消息后进行解码；
5. server stub 根据解码结果调用本地的服务；
6. 本地服务执行并将结果返回给 server stub；
7. server stub 将返回结果打包成消息并发送至消费方；
8. client stub 接收到消息，并进行解码；
9. 服务消费方得到最终结果。

RPC 相当于将 step2-step8 的步骤进行了封装。

![配图](https://user-gold-cdn.xitu.io/2017/11/23/15fe93fb307ec7e9?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

RPC 有许多成熟、开源的实现方案，常见的 RPC 框架有：gRPC、Dubbo、rpcx、Motan、thrift、brpc、Tars 等等。

参考：https://juejin.cn/post/6844903574506323976

### 什么是 gRPC

gRPC，全称是 gRPC Remote Procedure Calls，是 Google 开发的一个高性能、通用的开源 RPC 框架。

在 gRPC 里客户端应用可以像调用本地对象一样直接调用另一台不同的机器上服务端应用的方法，使得您能够更容易地创建分布式应用和服务。与许多 RPC 系统类似，gRPC 也是基于以下理念：定义一个服务，指定其能够被远程调用的方法（包含参数和返回类型）。在服务端实现这个接口，并运行一个 gRPC 服务器来处理客户端调用。在客户端拥有一个存根能够像服务端一样的方法。

![](http://www.grpc.io/img/grpc_concept_diagram_00.png)

gRPC 客户端和服务端可以在多种环境中运行和交互 - 从 Google 内部的服务器到你自己的笔记本，并且可以用任何 gRPC 支持的语言来编写。所以，你可以很容易地用 Java 创建一个 gRPC 服务端，用 Go、Python、Ruby 来创建客户端。此外，Google 最新 API 将有 gRPC 版本的接口，使你很容易地将 Google 的功能集成到你的应用里。

参考：[gRPC 官方文档中文版V1.0](http://doc.oschina.net/grpc?t=58008)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)



## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

1、[LearnOpenGL CN](https://learnopengl-cn.github.io/)

欢迎来到 OpenGL 的世界。这个工程只是我([Joey de Vries](http://joeydevries.com/))的一次小小的尝试，希望能够建立起一个完善的 OpenGL 教学平台。无论你学习 OpenGL 是为了学业，找工作，或仅仅是因为兴趣，这个网站都将能够教会你现代(Core-profile)  OpenGL 从基础，中级，到高级的知识。LearnOpenGL 的目标是使用易于理解的形式，使用清晰的例子，展现现代 OpenGL 的所有知识点，并与此同时为你以后的学习提供有用的参考。

> 该教程是[原教程](https://learnopengl.com/)的中文翻译教程

2、[VisuAlgo](https://visualgo.net/en)

由新加坡国立大学的教授和学生发起、制作并完善的「数据结构和算法动态可视化」网站，在该网站你可以看到许多经典、非经典的，常见的、非常见的算法的可视化，清晰明了的图形化表现和实时的代码解读可以帮助读者更好地理解各种算法及数据结构。同时该网站支持自动问题生成器和验证器（在线测验系统）。

![Animation of Graph Traversal Algorithm](https://www.comp.nus.edu.sg/images/resources/20200309-graph-traversal.gif)

3、[Announcing our Deprecated Books Repo!](https://www.raywenderlich.com/21965623-announcing-our-deprecated-books-repo)

raywenderlich 是一个学习编程的网站，他们有很大一部分课程和 `iOS` / `Swift` 有关。最近他们开源了一批将要被废弃的书籍。笔者看过其中的 `2D Games`、`3D Games`、`ARKit` 等书籍，其中介绍了 `SpriteKit` 和 `SceneKit` 的相关知识，书本会带着读者循序渐进，了解这些框架的原理以及如何应用。这次名单中还包含了 `Unity AR & VR`、`Realm` 和 `Server Side` 相关的书籍，这些书对于想要学习这些特定领域内容的读者来说是很好的选择。



## 工具推荐

整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### Application Name

**地址**：

**软件状态**：

**使用介绍**



## 联系我们

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

[摸鱼周报第六期](https://zhangferry.com/2021/03/14/iOSWeeklyLearning_6/)

[摸鱼周报第七期](https://zhangferry.com/2021/03/28/iOSWeeklyLearning_7/)

[摸鱼周报第八期](https://zhangferry.com/2021/04/11/iOSWeeklyLearning_8/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
