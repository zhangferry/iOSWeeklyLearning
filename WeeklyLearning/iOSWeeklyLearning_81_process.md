# iOS 摸鱼周报 #81 |Apple 推出 Apple Business Connect

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题： Developer 设计开发加速器｜探索 iPad 最新技术，Apple 推出 Apple Business Connect
> * 本周学习：基础知识回顾：iOS 中的 const 修饰符
> * 内容推荐：本期将推荐近期的一些优秀博文，涵盖如何保护剪切板内容、SwiftUI 的视图风格、iOS 应用启动优化等方面的内容
> * 摸一下鱼：一款个人知识管理工具 MindForger，通过渲染高质量的图像、视频和动画展示数学之美。

## 本期话题

### [设计开发加速器线上讲座：探索 iPad 最新技术](https://developer.apple.com/events/view/U2U58S76GX/dashboard "设计开发加速器线上讲座：探索 iPad 最新技术") 

[@远恒之义](https://github.com/eternaljust)：本次课程将通过一系列创新性 App 的演示，带领您充分了解 iPad 最新技术特性，学习如何利用功能强大的 API 来让您的 App 在 iPad 的体验更上一层楼。活动时间：2023 年 2 月 16 日上午 10:00 (GMT+8) – 中午 12:00 (GMT+8) (UTC+08:00)，报名截止：2023 年 2 月 15 日。

### [Apple 推出 Apple Business Connect](https://www.apple.com.cn/newsroom/2023/01/introducing-apple-business-connect/ "Apple 推出 Apple Business Connect")

[@远恒之义](https://github.com/eternaljust)：近日，Apple 推出了 Apple Business Connect，这是一款全新的免费工具，让企业可以在地点卡中自定义显示精美图像、关键信息和特别促销活动。这款免费工具让各种规模的企业都能认领相应地址的地点卡，并自主设计关键信息在 Apple 地图、信息、钱包、Siri 等各种 app 中向超过十亿 Apple 用户展示的方式。Business Connect 的推出，方便了世界各地的 Apple 用户都能找到关于美食、购物、旅行目的地的精确信息。

![通过 Business Connect，企业可以向顾客展示优惠或促销信息，用户可还以在地图 app 地点卡中直接执行的多种操作](https://cdn.zhangferry.com/Images/81-apple-business-connect.png)

## 本周学习

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### 基础知识回顾：iOS 中的 const 修饰符

`const` 修饰符将其后的变量设置为常量，`const` 在 \* 之前和 \* 之后的区别在于，常量指针是否可以指向其他的 内存块。以 iOS 中的字符串为例：

#### NSString

```objective-c
NSString *const str1 = @"str1";
// str1 = @"str1***str1"; //报错:Cannot assign to variable 'str1' with const-qualified type 'NSString *const __strong'
```

如示例所示，常量指针已经指向 `@"str1"` ，不能再指向其他的内存 `@"str1***str1"` ，因此不能修改常量指针指向的内容，常量指针仍然指向原内存中的内容。因为是 `NSString` ，所以改变指针指向的内存，才能改变指针指向的内容，常量指针指向的内存不变，所指向的内容就不会变。

当 `const`修饰了 \* 时，常量指针可以指向其他的内存，释放掉原来的内存，从而可以修改常量指针指向的内容(因为指向的内存变了)：

```objective-c
NSString const *str2 = @"str2";
str2 = @"str2***str2";
```

#### NSMutableString

如果把 `NSString` 换成 `NSMutableString` 情况就不一样了。以下示例可以修改原内存中的内容，也可以指向其他的内存：

```objective-c
NSMutableString const *var1 = [@"str" mutableCopy]; 
[var1 appendString:@"__var"]; // 改变内存中的内容
var1 = [@"123" mutableCopy]; // var1指向新的内存 NSLog(@"var1:%@",var1);
```

而当 `const` 修饰 \* 时可以修改原内存中的内容，但是不能指向其他的内存:

```objective-c
NSMutableString *const var2 = [@"str" mutableCopy];
[var2 appendString:@"__var"];//改变内存中的内容
var2 = [@"123" mutableCopy];//var2不能指向新的内存，报错:Cannot assign to variable 'var2' with
const-qualified type 'NSMutableString *const __strong'
    NSLog(@"var2:%@", var2);
```


## 内容推荐

> 本期将推荐近期的一些优秀博文，涵盖如何保护剪切板内容、SwiftUI 的视图风格、iOS 应用启动优化等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[如何防止复制和粘贴到其他 iOS 应用程序中](https://blog.eidinger.info/prevent-copy-paste-into-other-ios-apps "如何防止复制和粘贴到其他 iOS 应用程序中") -- 来自：Marco Edinger

[@东坡肘子](https://www.fatbobman.com/): 在企业应用程序中，经常需要通过防止最终用户将内容复制和粘贴到其他应用程序中来保护敏感信息。在这篇文章中，作者将向你展示为 iOS 应用程序引入这种高级剪贴板保护功能的多种方法。

2、[掌握 Swift Concurrency 的 AsyncStream](https://www.donnywals.com/understanding-swift-concurrencys-asyncstream/ "掌握 Swift Concurrency 的 AsyncStream") -- 来自：Donny wals

[@东坡肘子](https://www.fatbobman.com/): 创建自定义的异步序列的最好方法是什么？实现 AsyncSequence 协议并构建你的 AsyncIterator 确实可以解决一切问题，但实现起来很繁琐而且容易出错。在这篇文章中，作者将向你展示如何利用 Swift 的 AsyncStream 来构建自定义的异步序列，在你需要的时候产生数值。

3、[SwiftUI 视图的样式 —— 视图样式是如何工作的](https://peterfriese.dev/posts/swiftui-styling-views/ "SwiftUI 视图的样式 —— 视图样式是如何工作的") -- 来自：Peter Friese

[@东坡肘子](https://www.fatbobman.com/): SwiftUI 视图的样式是一个强大的概念，让开发者在设计应用程序时具有很大的灵活性，且不会丢失我们使用的视图的语义。支持此概念的 SwiftUI 视图列表令人印象深刻：按钮、选择器、菜单、切换、指示器、文本和标签、集合视图、导航视图、窗口和工具栏以及组等。因此，下次在你需要定制 UI 元素的特殊外观时，请先查看苹果的文档，看看是否已经有满足你需求的风格。如果没有，本文将告诉你如何创建自定义样式。

4、[Dependencies —— Point Free 发布了新的开源依赖库](https://www.pointfree.co/blog/posts/92-a-new-library-to-control-dependencies-and-avoid-letting-them-control-you "Dependencies —— Point Free 发布了新的开源依赖库") -- 来自：Point Free

[@东坡肘子](https://www.fatbobman.com/): 依赖性是指你的应用程序中需要与不受你控制的外部系统交互的类型和功能。典型的例子是向服务器发出网络请求的 API 客户端，但也有一些看似无害的东西，如 UUID 和日期初始化器、文件访问、用户默认值，甚至时钟和计时器，都可以被认为是依赖关系。Point Free 将 TCA 中广受好评的依赖功能分离出来构建成一个独立且开源的依赖管理系统，以便让更多的开发者受益。

5、[云音乐 iOS 启动性能优化「开荒篇」](https://juejin.cn/post/7145672412883845127 "云音乐 iOS 启动性能优化「开荒篇」") -- 来自：网易云音乐技术团队

[@东坡肘子](https://www.fatbobman.com/): App 启动作为用户使用应用的第一个体验点，直接决定着用户对 App 的第一印象。网易云音乐作为一个有着近 10 年发展历史的 App，随着各种业务不停的发展和复杂场景的堆叠，不同的业务和需求不停地往启动链路上增加代码，这给 App 的启动性能带来了极大的挑战。而随着云音乐用户基数的不断扩大和深度使用，越来越多的用户反馈启动速度慢，况且启动速度过慢更甚至会降低用户的留存意愿。因此，云音乐 iOS App 急需要进行一个专项针对启动性能进行优化。本文将介绍云音乐技术团队在 App 启动优化方面所做出的努力。（ 编者同大多数评论的想法一致，在不解决开屏广告的情况下，一切基于技术层面的优化都很难让用户有较大的感知 ）

## 摸一下鱼

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

1、[openwrite](https://openwrite.cn/) 提供了基于`MarkDown`的写作工具以及一文多发的工具，适合需要做新媒体矩阵的程序员。

![](http://cdn.zhangferry.com/20230112163018.png)

2、[Asimov](https://github.com/stevegrunwell/asimov)  自动检查本地磁盘把开发依赖的文件包全部从 TimeMachine 移出掉的好用工具。

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #80 | 开发加速器 SwiftUI 中管理数据模型](https://mp.weixin.qq.com/s/eIQLuAIsRQ7eeEnsrL5QuA)

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
