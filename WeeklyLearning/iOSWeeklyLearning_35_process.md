# iOS摸鱼周报 第三十五期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * Tips：count vs isEmpty
> * 面试模块：Swift 中 struct 和 class 的区别，值类型和引用类型的区别。
> * 优秀博客：本期继续介绍几个优秀的 Swift 开源库。
> * 学习资料：戴铭的 Swift 小册子。
> * 开发工具：PhotoSweeper，一款快速而强大的重复照片清理器。

## 开发Tips

整理编辑：[zhangferry](zhangferry.com)

### count vs isEmpty

通常在判断一个字符串或者数组是否为空的时候有两种方式：`count == 0` 或者 `isEmpty`。我们可能会认为两者是一样的，`isEmpty` 内部实现就是 `count == 0`。但在 SwiftLint 的检验下，会强制要求我们使用使用 isEmpty 判空。由此可以判断出两者肯定还是存在不同的，今天就来分析下两者的区别。

count 和 isEmpty 这两个属性来源于 `Collection`，count 表示数量，这个没啥特别的，需要注意的是isEmpty的实现。在标准库中，它的定义是这样的：

```swift
extension Collection {
    var isEmpty: Bool { startIndex == endIndex }
}
```

集合的首索引和尾索引相等，则表示为空，这里只有一个比较，复杂度为 O(1)。

大部分集合类型都是走的该默认实现，但也有一些特定的集合类型会重写该方法，比如 `Set`：

```swift
extension Set {
    var isEmpty: Bool { count == 0 }
}
```

那为啥会出现两种不同的情况呢，我们再看 Collection 里对 count 的说明。

> **Complexity**: O(1) if the collection conforms to `RandomAccessCollection`; otherwise, O(**n**), where **n** is the length of the collection.

所以对于遵循了`RandomAccessCollection` 协议的类型，其count获取是 O(1) 复杂度，像是 Array；对于未遵循的类型，比如 String，其 count 复杂度就是 O(n)，但是isEmpty 却还是 O(1)。

这里的 Set 还要再特殊一些，因为其没有实现 `RandomAccessCollection` 却还是用 count 的方式判定是否为空，这是因为 Set 的实现方式不同，其 count 的获取就是 O(1) 复杂度。

当然为了简化记忆，我们可以总是使用 isEmpty 进行判空处理。

因为涉及多个协议和具体类型，这里再一张表示这几个协议和类型之间的关系图。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20211126004620.png)

[图片来源](https://itwenty.me/2021/10/understanding-swifts-collection-protocols/ "图片来源")

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

### Swift 中 struct 和 class 的区别，值类型和引用类型的区别

**struct & class**

在 Swift 中，其实 `class` 与 `struct` 之间的核心区别不是很多，有很多区别是值类型与引用类型这个区别隐形带来的天然的区别。

- `class` 可以继承，`struct` 不能继承（当然 `struct` 可以利用 `protocol` 来实现类似继承的效果。）；受此影响的区别有：

- - `struct` 中方法的派发方式全都是直接派发，而 `class` 中根据实际情况有多种派发方式，详情可看 [CoderStar｜Swift 派发机制](https://mp.weixin.qq.com/s?__biz=MzU4NjQ5NDYxNg==&mid=2247483768&idx=1&sn=0a6be7a9c5a374cbc5c5ba9a3c48020a&scene=21#wechat_redirec)；

- `class` 需要自己定义构造函数，`struct` 默认生成；

- `class` 是引用类型，`struct` 是值类型；受此影响的区别有：

- - `struct` 改变其属性受修饰符 let 影响，不可改变，`class` 不受影响；
  - `struct` 方法中需要修改自身属性时 (非 `init` 方法)，方法需要前缀修饰符 `mutating`；
  - `struct` 因为是值类型的原因，所以自动线程安全，而且也不存在循环引用导致内存泄漏的风险；
  - ...

- ...

**值类型 & 引用类型**

- 存储方式及位置：大部分值类型存储在栈上，大部分引用类型存储在堆上；
- 内存：值类型没有引用计数，也不会存在循环引用以及内存泄漏等问题；
- 线程安全：值类型天然线程安全，而引用类型需要开发者通过加锁等方式来保证；
- 拷贝方式：值类型拷贝的是内容，而引用类型拷贝的是指针，从一定意义上讲就是所谓的深拷贝及浅拷贝

你可以在 [CoderStar｜从 SIL 角度看 Swift 中的值类型与引用类型](https://mp.weixin.qq.com/s/6bvZ1YIhf2WCNsdkukTlew) 中查看详细内容。


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

1、[第三方日期处理库SwiftDate使用详解](https://www.hangge.com/blog/cache/detail_2222.html "@hangge｜第三方日期处理库SwiftDate使用详解") -- 来自航歌：hangge

[@东坡肘子](https://www.fatbobman.com/)：SwiftDate 是在所有苹果平台，甚至在 Linux 和 Swift 服务器端框架（如 Vapor 或 Kitura ）上操作和显示日期和时区的权威工具链。在 CocoaPods 上有超过 300 万的下载量。SwiftDate 功能强大，无论是简单的日期操作，还是复杂的业务逻辑都能满足。本文将对 SwiftDate 的使用方法做详尽说明。

2、[搞事情之 Vapor 初探](https://juejin.cn/post/6844903834659667981 "@PJHubs｜搞事情之 Vapor 初探") -- 来自掘金：PJHubs

[@东坡肘子](https://www.fatbobman.com/)：Vapor 是一个基于 Swift 语言的开源 Web 框架，可用于创建 RESTful API、网站和使用 WebSockets 的实时应用。在核心框架之外，Vapor 还提供了 ORM 、模板语言，以及用户身份验证和授权模块。本文主要记录了第一次上手 Vapor 所遇到的问题、思考和总结。

3、[用 Publish 创建博客](https://www.fatbobman.com/tags/publish/ "@东坡肘子｜用 Publish 创建博客") -- 来自肘子的Swift记事本：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：Publish 是一款专门为 Swift 开发者打造的静态网站生成器。它使用 Swift 语言构建整个网站，并支持主题、插件和其他大量的定制选项。本系列文章将通过三个篇幅分别介绍 Publish 的基本用法、主题定制以及插件开发。

4、[Using Realm and Charts with Swift 3 in iOS 10](https://medium.com/@skipadu/using-realm-and-charts-with-swift-3-in-ios-10-40c42e3838c0#.2gyymwfh8 "@Sami Korpela｜Using Realm and Charts with Swift 3 in iOS 10") -- 来自：Sami Korpela

[@我是熊大](https://github.com/Tliens)：一个十分强大并且是纯 Swift 的图表相关的开源框架 -- Charts。本文作者利用 Swift 中的轻量级数据库 Realm 和 Charts，构建了一个 Demo。篇幅较长，适合新手，但美中不足的是：Demo 基于 Swift 3。此外我早期写过一篇关于 Realm 的实践代码的文章：[如何降低Realm数据库的崩溃](https://juejin.cn/post/6844904143501557773 "@我是熊大｜如何降低Realm数据库的崩溃")，有兴趣可以看一下。

5、[今天我们来聊一聊WebSocket（iOS/Golang）](https://juejin.cn/post/6844904062408720391 "@齐舞647｜今天我们来聊一聊WebSocket（iOS/Golang）") -- 来自掘金：齐舞647

[@我是熊大](https://github.com/Tliens)：Starscream swift 中的 7k+ star 的 socket 开源库，本文作者利用 GO 和 Starscream，模拟了客户端和服务端 websocket 的交互过程，建议对 Socket 感兴趣的阅读。

6、[Hero Usage Guide](https://github.com/HeroTransitions/Hero/wiki/Usage-Guide "Hero Usage Guide") -- 来自：Hero官方

[@我是熊大](https://github.com/Tliens)：Hero 是我用过的最好的转场动画，没有之一，20k+ star 的成绩也表名了它在转场动画的地位；Hero 应该能满足绝大部分需求，这是它的官方使用手册。
## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 戴铭的 Swift 小册子

地址：https://github.com/ming1016/SwiftPamphletApp

戴老师用 Swift 写的、按照声明式 UI、响应式编程范式开发的 Swift 小册子。你可以在这本小册子中查询到 Swift 的语法指南，同时还有 Combine、 Concurrency 和 SwiftUI 这些库的使用指南，你还可以在这追踪到一些知名仓库、开发者的 Github 动态和本仓库的 Issues。由于是开源的，你也可以自己调试学习或者是为项目作出贡献。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### PhotoSweeper

**地址**：https://overmacs.com/

**软件状态**：$9.99，可以试用

**软件介绍**：

`PhotoSweeper` 是一款快速而强大的重复照片清理器，旨在帮助您在 Mac 上查找和删除重复和相似的照片。

我们可以考虑用在给应用瘦身时扫描相似图片资源场景下。

![PhotoSweeper](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/PhotoSweeper_MacBook.jpeg)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第三十四期](https://mp.weixin.qq.com/s/P0HjLDCIM3T-hAgQFjO1mg)

[iOS摸鱼周报 第三十三期](https://mp.weixin.qq.com/s/nznnGmBsqsrWcvZ4XFMttg)

[iOS摸鱼周报 第三十二期](https://mp.weixin.qq.com/s/6CyL0B6Zkf6KXRrfocohoQ)

[iOS摸鱼周报 第三十一期](https://mp.weixin.qq.com/s/DQpsOw90UsRg6A5WDyT_pg)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
