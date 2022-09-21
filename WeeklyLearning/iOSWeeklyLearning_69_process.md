# iOS 摸鱼周报 #64 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：使用 iOS 16.1 Beta 版和 Xcode 14.1 Beta 版，准备登陆灵动岛
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [使用 iOS 16.1 Beta 版和 Xcode 14.1 Beta 版，开发实时活动功能](https://developer.apple.com/cn/news/?id=ttuz9vwq "使用 iOS 16.1 Beta 版和 Xcode 14.1 Beta 版，开发实时活动功能")

[@远恒之义](https://github.com/eternaljust)：从 iOS 16.1 Beta 版和 Xcode 14.1 Beta 版开始，我们可以在灵动岛和锁定屏幕上共享应用程序的实时更新作为实时活动。借助于新 ActivityKit 框架的实时更新功能，实时活动能帮助用户跟踪 App 内容状态的变化。

灵动岛作为 iPhone 14 Pro 系列最惊艳的设计，App 的实时活动会显示在锁定屏幕和灵动岛中，可以让用户非常直观、愉悦地体验到实时更新的内容。实时活动功能和 ActivityKit 将在今年晚些时候 iOS 16.1 正式版中上线。

推荐观看 [Dynamic Island API - iOS 16.1 Beta - Xcode 14.1](https://www.youtube.com/watch?v=gEWvV-TmjqE&t=25s "Dynamic Island API - iOS 16.1 Beta - Xcode 14.1 - SwiftUI Tutorials") 课程介绍，开始登陆灵动岛。

![Kavsoft SwiftUI Tutorials](https://cdn.zhangferry.com/Images/dynamic-island-api.jpeg)

### [App 和 App 内购买项目即将实行价格和税率调整](https://developer.apple.com/cn/news/?id=e1b1hcmv "App 和 App 内购买项目即将实行价格和税率调整")

[@远恒之义](https://github.com/eternaljust)：最早于 2022 年 10 月 5 日起，智利、埃及、日本、马来西亚、巴基斯坦、波兰、韩国、瑞典、越南和所有使用欧元货币的地区的 App Store 上的 App 及 App 内购买项目 (自动续期订阅除外) 价格将有所提高。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)


## 内容推荐

整理编辑：[东坡肘子](https://www.fatbobman.com)

> 本期将介绍近期的几篇优秀博文

1、[SwiftUI布局协议](https://swiftui-lab.com/layout-protocol-part-1/ "SwiftUI布局协议") -- 来自：Javier

[@东坡肘子](https://www.fatbobman.com/)：在 SwiftUI 诞生初期，SwiftUI-Lab 的 Javier 便对 SwiftUI 进行了深入地研究，可以说很多 SwiftUI 的使用者都是通过阅读他的文章才开始了解 SwiftUI 的布局机制。针对今年 SwiftUI 新增的 Layout 协议，Javier 也贡献出了精彩研究文章。文章共分上下两部分，上篇着重介绍理论，下篇提供了许多有趣的案例演示。

2、[iPhone 14 屏幕尺寸](https://useyourloaf.com/blog/iphone-14-screen-sizes/ "iPhone 14 屏幕尺寸") -- 来自：Keith Harrison

[@东坡肘子](https://www.fatbobman.com/)：iPhone 14 Pro 和 iPhone 14 Pro Max 用灵动岛替换了刘海，这导致了屏幕的分辨率也发生了变化。本文对 2022 年 iPhone 14 系列机型的屏幕尺寸的变化做了总结。

3、[如何判断 ScrollView、List 是否正在滚动中](https://www.fatbobman.com/posts/how_to_judge_ScrollView_is_scrolling/ "如何判断 ScrollView、List 是否正在滚动中") -- 来自：Holly Borla

[@东坡肘子](https://www.fatbobman.com/)：SwiftUI 4 重写了 ScrollView 和 List 的底层实现，这意味着以前通过 Hack 的方式获取滚动状态的手段将不再有效。本文将介绍几种在 SwiftUI 中获取当前滚动状态的方法，每种方法都有各自的优势和局限性。

4、[Swift 5.7 正式发布](https://www.swift.org/blog/swift-5.7-released/ "Swift 5.7 正式发布") -- 来自：Holly Borla

[@东坡肘子](https://www.fatbobman.com/)：Swift 5.7 现已正式发布! Swift 5.7包括对语言和标准库的重大补充，对编译器的增强以获得更好的开发者体验，对Swift生态系统中的工具的改进，包括SourceKit-LSP和Swift Package Manager，完善的Windows支持等等。

5、[Combine中的内存管理](https://tanaschita.com/20220912-memory-management-in-combine/ "Combine中的内存管理") -- 来自：Holly Borla

[@东坡肘子](https://www.fatbobman.com/)：就像其他异步操作一样，内存管理是 Combine 的一个重要部分。一个订阅者只要想接收值就需要保留一个订阅，然而，一旦不再需要订阅，所有的引用应该被正确地释放。在这种情况下，一个常见的问题是我们是否应该使用弱引用。本文将通过一些例子来帮助读者更好地理解 Combine 中的内存管理。

6、[Apple Watch 应用开发系列](https://juejin.cn/post/7136115417323405325 "Apple Watch 应用开发系列") -- 来自：Layer

[@东坡肘子](https://www.fatbobman.com/)：2015 年 4 月 24 日，Apple 发布了第一代 Apple Watch。 无论我们对 Apple Watch 看法如何，watchOS 肯定是我们要支持的 Apple 生态系统的一部分，确保我们的应用获得更大的曝光率。作者将通过创建一个 watchOS 应用程序，来展示如何将我们现有的 iOS 开发知识转移到 watchOS 上来。

7、[灵动岛开发演示](https://www.youtube.com/watch?v=gEWvV-TmjqE&t=65s "灵动岛开发演示") -- 来自：
Kavsoft

[@东坡肘子](https://www.fatbobman.com/)：Kavsoft 将在本视频中演示如何使用 SwiftUI 开发可用于 Apple iPhone 14 Pro 灵动岛的 Live Actitivy。

## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)




## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #63 | Apple 企业家培训营已开放申请](https://mp.weixin.qq.com/s/nAMshUG4AjWLAAHOFPVqXg)

[iOS 摸鱼周报 #62 |  Live Activity 上线 Beta 版 ](https://mp.weixin.qq.com/s/HySX4Yaf3Zxy8Wn-LyUO0A)

[iOS 摸鱼周报 #61 |  Developer 设计开发加速器](https://mp.weixin.qq.com/s/WfwqRhC-9-isUanv8ZnvMQ)

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
