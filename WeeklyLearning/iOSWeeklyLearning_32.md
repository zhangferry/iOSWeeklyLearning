# iOS 摸鱼周报 第三十二期

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：Mac 版 TestFlight 已经上线。
> * Tips：介绍了关于中间层的一些概念，前后端之间的现状以及需要解决的问题等。
> * 面试模块：能否向编译后的类增加实例变量？能否向运行时动态创建的类增加实例变量？为什么？
> * 博客主题：Swift 关键字。
> * 学习资料：来自字节跳动的 OKR 学习网站；一个关于 SwiftUI 的 Cheat Sheet —— Fucking SwiftUI。
> * 开发工具：一个允许你在 App Store 上搜索 iOS 应用程序并下载应用程序包的命令行工具 —— ipatool。

## 本期话题

### [使用 TestFlight 测试 Mac App](https://developer.apple.com/news/?id=0bemba6j "使用 TestFlight 测试 Mac App")

现在，你可以邀请用户试用你的 Mac app 的 Beta 版，在发布前为你提供宝贵的反馈。通过 TestFlight，你可以对多达 10000 名测试人员发出邀请。TestFlight 在 Mac 端的使用与移动端无异。

安装地址：https://apps.apple.com/cn/app/testflight/id899247664

版本要求：最低 macOS 12.0（Monterey）

## 开发 Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### 关于中间层的一些概念

> 本文基于经验、个人理解及参考资料整理而出。本文以前端作为接口调用方，服务端称为接口提供者，本文指出的中间层概念是作者理解的，如果有误欢迎指正。

在传统的开发分层中，前端工程师负责前端界面层的研发，数据接口由服务端工程师提供。随着微服务架构的发展，服务端的功能更加细致，而前端与用户贴近，其数据展示是多变繁杂的。

中间层，用户接口或 **Web** 客户端与底层或数据库之间的逻辑层，早期也被称为**粘合层**，其作用是粘合前端及后端之间的形象比喻。

#### 前后端交流的困境

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20211104223956.png)

由于前端直接与服务端进行对接，会导致以下问题：

##### 前端和服务端考虑的问题不一致

前端在开发过程中需要考虑用户体验等信息，而服务端因为服务下沉及解耦等原因一般其提供独立的方法实现独立的功能。

##### 前端入口多

前端目前有客户端（iOS， Android），PC 端及 H5 端，对待不同的前端类型可能需要不同的接口，如果用同一接口的话，需要服务端进行适配，增大了服务端的工作量。

##### 前端需求变化大

作为面向用户侧的前端开发来说，其需求变化是频繁的，对数据要求也是不同的。服务端接口的返回值一般不是前端想要的，并且会返回远超前端想要的内容。服务端会提供不同样式的返回值，导致前端需要兼容，**入口越多，兼容成本越大**。

##### 安全问题

越多的底层接口的暴露意味着需要保护的内容也越多，越多的底层服务被暴露出来，其底层实现逻辑也越容易被分析然后加以攻击。

##### 客户端更新问题

大部分情况下并不会要求客户去强制更新客户端，如果出现旧接口迁移或改造，且保留原接口的话，这种迁移和改造的必要性将会大打折扣。

这些问题导致前端和服务端之间关于 API 接口颗粒度的争吵，越来越常见。

* **服务端提供的接口是面向前端业务还是通用服务**

* **前端希望接口更能贴近业务及其他性能问题**

#### 中间层能够解决的问题

BFF 理念中最重要的一点是 **服务自治**，谁用谁处理。通过中间层我们可以处理一些问题。

##### 前后端分离

比起业务，服务端应该更多考虑接口的性能，服务能力。由中间层来实现前后端的交流，前端需求和后端需求分开了，便于后期维护

##### 易于维护和修改的API

1. 不同的服务端可能提供不同的接口，对于前端来说对接不同接口会导致成本的增加，并且不利于前端对接口进行统一的处理。

2. 使用中间层能够统一处理接口返回的数据， 前端获取的数据可以经过中间层来进行处理，可以大大减少各端开发者的调用时间。
3. 便于 Mock 数据， 由中间层定义前端的数据格式，可以在服务端 Mock 数据，后续对接接口时，只需要对中间层进行修改，便于调试。

##### 更安全

接口之间可能存在敏感信息需要传递到下一个接口，使用中间层完成多接口**串联**可以减少这种敏感数据的暴露。

服务端可以限制只有中间层才能对后台进行访问，降低攻击的可能性。

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20211104224017.png)

#### 中间层的限制及滥用

在明确是否使用中间层之前，需要明确这几点：

1. 中间层不能**防止错误**的出现。中间层是一个中转服务，服务端还需要与中间层进行沟通，这个过程被简化了，但是并没有消除。中间层更多的是统一和聚合，而不是真正底层逻辑的实现，这些实现还需要服务端实现。
2. 避免**重复逻辑**的中间层分割。我们可以有多个中间层，但是这种分割应该基于具体的用户体验而不是特定的设备。例如基于用户的需求来分割中间层是可以接受的，例如订单、产品分类等，但是根据 iOS， Android，PC， H5 来区分就是不明智的。
3. 不要过分**依赖**中间层。中间层不是万能的，它可以优化用户体验，提升开发效率，但是它仅仅是一个中转层，过多的中间层逻辑处理仅仅是原来服务端的套壳，对于接口等还需要合理的设计。

#### 问题

当然还有其他问题，例如中间层谁来开发、谁来部署、谁来运维这些问题，留待后续讨论。有两个阿里的关于中间层的引申阅读，可以来看看。

#### 参考资料

[Pattern: Backends For Frontends](https://link.zhihu.com/?target=http%3A//samnewman.io/patterns/architectural/bff/ "Pattern: Backends For Frontends")

[The BFF Pattern (Backend for Frontend): An Introduction](https://blog.bitsrc.io/bff-pattern-backend-for-frontend-an-introduction-e4fa965128bf "The BFF Pattern (Backend for Frontend): An Introduction")

[Developer Experience First —— TWA 的理念与实践（附演讲视频）](https://zhuanlan.zhihu.com/p/32219319 "Developer Experience First —— TWA 的理念与实践（附演讲视频）")

[Serverless For Frontend 前世今生](https://zhuanlan.zhihu.com/p/77095720 "Serverless For Frontend 前世今生")

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

Q：能否向编译后的类增加实例变量？能否向运行时动态创建的类增加实例变量？为什么？

A：

* 不能向编译后的类增加实例变量。类的内存布局在编译时就已经确定，类的实例变量列表存储在 class_ro_t Struct 里，编译时就确定了内存大小无法修改，所以不能向编译后的类增加实例变量。
* 能向运行时动态创建的类增加实例变量。运行时动态创建的类只是通过 alloc 分配了类的内存空间，没有对类进行内存布局，内存布局是在类初始化过程中完成的，所以能向运行时动态创建的类增加实例变量。

```objectivec
Class newClass = objc_allocateClassPair([NSObject class], "Person", 0);
class_addIvar(newClass, "_age", 4, 1, @encode(int));
class_addIvar(newClass, "_name", sizeof(NSString *), log2(sizeof(NSString *)), @encode(NSString *));
objc_registerClassPair(newClass); // 要在类注册之前添加实例变量
```

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

本周博客主题：Swift 关键字

在还没有学习 Swift 时，听过好几次部门内关于 Swift 的分享。依稀记得在分享会上听到了各种各样的新颖的概念，见到一些在 OC 中没有见过的关键字。希望本次主题能为 OC 的同学扫清一些学习 Swift 的障碍。

1、[Swift-29个关键字，助力开发（万字长文）](https://juejin.cn/post/6844904112119611399 "Swift-29个关键字，助力开发（万字长文）") -- 来自掘金：SunshineBrother

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：推荐新手阅读，对 Swift 比较熟悉的同学可以简单浏览校验下是否有不清楚的概念。文中有对应的示例代码，帮助大家理解。

2、[Swift 的闭包为什么选用 in 关键字？](https://www.zhihu.com/question/53539254 "Swift 的闭包为什么选用 in 关键字？") -- 来自知乎

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：Swift 闭包为什么用 in 可能很多同学都没有思考过。这个问题比较有意思，信息量也不是很密集，也比较轻松。该话题有人列出了苹果工程师对此的解释。

3、[细说 Swift 4.2 新特性：Dynamic Member Lookup](https://juejin.cn/post/6844903621306351624 "细说 Swift 4.2 新特性：Dynamic Member Lookup") -- 来自掘金：没故事的卓同学

[@东坡肘子](https://www.fatbobman.com)：`@dynamicMemberLookup` 中文可以叫动态查找成员。在使用 `@dynamicMemberLookup` 标记了对象后（对象、结构体、枚举、protocol），实现了 `subscript(dynamicMember member: String)` 方法后我们就可以访问到对象不存在的属性。如果访问到的属性不存在，就会调用到实现的 `subscript(dynamicMember member: String)` 方法，key 作为 member 传入这个方法。

4、[解析 Swift 中的 @discardableResult](https://xie.infoq.cn/article/fef30fd533cdff4278f0a85ff "解析 Swift 中的 @discardableResult") -- 来自：SwiftMic

[@东坡肘子](https://www.fatbobman.com)：`@discardableResult` 属性可能很少被人熟知，但是对于想消除方法返回值未被使用的警告来说的话，该属性还是很有用的，只需要在对应方法前添加 `@discardableResult` 属性即可。但是，还是要考虑是否真的需要忽略该类警告，因为有些情况下及时处理返回结果可能是一种更好的解决方案。

5、[“懒”点儿好](https://swift.gg/2016/03/25/being-lazy/ "“懒”点儿好") -- 来自：SwiftGG

[@我是熊大](https://github.com/Tliens)：这是一个优化的小技巧--使用 lazy 关键字，可以用于属性、闭包初始化等场景；不仅如此，就连 let 修饰的常量，默认也是 lazy 的，还有其他相关的 lazy 小技巧，推荐阅读。

6、[访问控制](https://swiftgg.gitbook.io/swift/swift-jiao-cheng/26_access_control "访问控制") -- 来自：SwiftGG

[@我是熊大](https://github.com/Tliens)：在 Swift 中，类、结构体、协议、属性、方法默认访问级别都是 internal，此外还有更多的访问级别需要我们了解，尤其是在做组件、模块时；学好关键字助你设计更好的代码。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### OKR.com

地址：https://www.okr.com/

来自字节跳动的 OKR 学习网站。你可能或多或少听说过 OKR 这个概念，但没有深入了解过。OKR 是一套协助组织进行目标管理的工具和方法，它能帮助团队明确目标、聚焦重点。该网站会从 OKR 是什么开始，带你了解 OKR 理论的优缺点，价值在哪，或者适不适合你的个人或你的公司规划，你还能在网站上面找到许多关于 OKR 的资源。

### Fucking SwiftUI

地址：https://fuckingswiftui.com/

Fucking SwiftUI 是一个关于 SwiftUI 的 Cheat Sheet。这上面有许多许多（关于技术的和无关技术的都有）关于 SwiftUI 的问答，类似 "我该学 SwiftUI 么"、"SwiftUI 中 List 如何使用？"、"SwiftUI 会取代 UIKit 么？" 等等问题，也有几乎所有 SwiftUI 控件的使用方式，希望能帮到大家。（如果你的浏览器不能打脏话可以使用这个链接：https://goshdarnswiftui.com/）

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### ipatool

**地址**：https://github.com/majd/ipatool

**软件状态**：免费，[开源](https://github.com/majd/ipatool)

**软件介绍**：

`ipatool` 是一个允许你在 `App Store` 上搜索 iOS 应用程序并下载应用程序包的命令行工具。当然，这过程中需要你的账户以及密码，并且也只能下载账户过去已经下载过的应用程序。相对于使用 `Apple Configurator 2` 操作更加便捷一些。

![ipatool](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/demo.gif)
> 注意 gif 中的 `ipa` 命令实际使用中可能为 `ipatool`

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS 成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第三十一期](https://mp.weixin.qq.com/s/DQpsOw90UsRg6A5WDyT_pg)

[iOS摸鱼周报 第三十期](https://mp.weixin.qq.com/s/KNyIcOKGfY5Ok-oSQqLs6w)

[iOS摸鱼周报 第二十九期](https://mp.weixin.qq.com/s/TVBQgYuycelGBwTaCSfmxQ)

[iOS摸鱼周报 第二十八期](https://mp.weixin.qq.com/s/dKOkF_P5JvQnDLq09DOzaQ)

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/WechatIMG384.jpeg)
