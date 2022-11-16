# iOS 摸鱼周报 #64 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [iPhone 14 / Pro 系列卫星 SOS 紧急求救服务已在美国和加拿大正式推出](https://www.ithome.com/0/654/091.htm "iPhone 14 / Pro 系列卫星 SOS 紧急求救服务已在美国和加拿大正式推出")

[@远恒之义](https://github.com/eternaljust)：卫星 SOS 紧急求救服务是 Apple 今年发布所有 iPhone 14 / Pro 系列机型提供的新功能，用户能够在没有蜂窝网络和 Wi-Fi 信号覆盖区域通过卫星紧急服务发送消息。从 11 月 15 号开始，美国和加拿大的 iPhone 14 / Pro 系列用户可通过卫星使用紧急 SOS，此服务还将于 12 月在法国、德国、爱尔兰和英国推出。[Apple 官网关于卫星紧急求救](https://support.apple.com/en-us/HT213426 "Use Emergency SOS via satellite on your iPhone 14")的介绍说明，用户使用前必须升级到 iOS 16.1 正式版系统，同时从 iPhone 14 / Pro 系列手机激活之日起，此服务两年内免费使用。遗憾的是，国行版 iPhone 14 / Pro 系列不支持此服务功能。

![Use Emergency SOS via satellite on your iPhone 14](https://cdn.zhangferry.com/Images/iphone-14-emergency-sos-via-satellite.png)

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)


## 内容推荐

> 本期将推荐最近的一些优秀博文

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[Swift 正则速查手册](https://onevcat.com/2022/11/swift-regex/ "Swift 正则速查手册") -- 来自：王巍

[@东坡肘子](https://www.fatbobman.com/): 与其他语言和平台相比，正则表达式一直是 Swift 语言一个相当大的痛点。Swift 5.7 引入了大量与正则表达式相关的改进。作者在本文中对与新正则有关的话题、方法与示例进行了详尽整理。

2、[深入理解 Aspects 设计原理](http://chuquan.me/2022/11/13/understand-principle-of-aspects/ "深入理解 Aspects 设计原理") -- 来自：楚权

[@东坡肘子](https://www.fatbobman.com/): Aspects 是一款轻量且简易的面向切面编程的框架，其基于 Objective-C Runtime 原理实现。Aspects 允许开发者对类的所有实例的实例方法或单个实例的实例方法添加额外的代码，并且支持设置代码的执行时机。本文记录作者在阅读 Aspects 源码后的一些收获和思考。

3、[Swift 包管理器中的二进制目标](https://www.avanderlee.com/optimization/binary-targets-swift-package-manager/ "Swift 包管理器中的二进制目标") -- 来自：Antoine van der Lee

[@东坡肘子](https://www.fatbobman.com/): Swift Package Manager（SPM）允许软件包将 xcframework bundle 声明为可用目标。该技术通常用于提供对闭源库的访问，并且可以通过减少获取 SPM 存储库所花费的时间来提高 CI 性能。在向项目添加二进制目标时，必须考虑其优缺点，并了解 xcframeworks 在它们支持的平台上所能发挥作用。

4、[如何在 SwiftUI 中创建条形图](https://mp.weixin.qq.com/s/xPykVjkb9aLtu8rha3tQqA "如何在 SwiftUI 中创建条形图") -- 来自：Swift 社区

[@东坡肘子](https://www.fatbobman.com/): Apple 在 WWDC 2022 期间宣布了一个名为 Swift Charts 的全新框架，方便开发者创建与苹果官方水准相当的图表应用。本文是 Swift 社区推出的有关 Swift Charts 系列文章中的一篇，其他内容还包括：[如何创建折线图](https://mp.weixin.qq.com/s/V_qXskB41WYHwaPdV877mg)、[在 Swift 图表中使用 Foudation 库中的测量类型](https://mp.weixin.qq.com/s/V_qXskB41WYHwaPdV877mg) 等内容。

5、[用 ViewInspector 进行 SwiftUI 视图的单元测试](https://augmentedcode.io/2022/11/14/basic-unit-tests-for-swiftui-view-with-viewinspector/ "用 ViewInspector 进行 SwiftUI 视图的单元测试") -- 来自：Toomas Vahter

[@东坡肘子](https://www.fatbobman.com/): 为 UIKit 代码编写单元测试很容易，但对于 SwiftUI 的视图来说则要困难许多。目前主要通过两种途径进行这项工作：使用 pointfreeco 的 SnapshotTesting 库进行快照测试或使用 ViewInspector 检查视图。作为 ViewInspector 的作者， Toomas Vahter 将通过本文向你展示如何为 SwiftUI 的视图构建单元测试。

6、[Ask Apple 2022 十月问答汇总](https://www.fatbobman.com/tags/ask-apple-2022/ "Ask Apple 2022 十月问答汇总") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): Ask Apple 为开发者与苹果工程师创造了在 WWDC 之外进行直接交流的机会。作者用四篇文章对 10 月份活动中与 SwiftUI 和 Core Data 有关的问答内容进行了整理。或许是受到开发者对本次活动正向反馈的鼓励，在本周苹果继续举办了 Ask Apple 活动，有逐步常态化的趋势。其中【集锦-简体中文】频道不仅会对英文问答进行汇总，同时也会用中文为开发者解答各类问题，希望广大开发者能够踊跃参与。

## 摸一下鱼

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #63 | Apple 企业家培训营已开放申请](https://mp.weixin.qq.com/s/nAMshUG4AjWLAAHOFPVqXg)

[iOS 摸鱼周报 #62 |  Live Activity 上线 Beta 版 ](https://mp.weixin.qq.com/s/HySX4Yaf3Zxy8Wn-LyUO0A)

[iOS 摸鱼周报 #61 |  Developer 设计开发加速器](https://mp.weixin.qq.com/s/WfwqRhC-9-isUanv8ZnvMQ)

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
