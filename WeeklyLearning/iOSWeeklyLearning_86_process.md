# iOS 摸鱼周报 #82

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：Apple 公布 iOS 16 的普及率已达 81%
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [Apple 公布 iOS 16 的普及率已达 81%](https://developer.apple.com/cn/support/app-store/ "Apple 公布 iOS 16 的普及率达 81%")

[@远恒之义](https://github.com/eternaljust)：Apple 官方数据来源于 App Store 上进行交易的设备统计，时间截止至 2023 年 2 月 14 日。在过去四年推出的设备中，iOS 16 的普及率达 81%。在所有的设备中，iOS 16 的普及率达 72%，加上 iOS 15 的 20%，iOS 15 系统及以上的普及率总计 92%。是时候修改 iOS 项目最低版本的限制了，开发者们要紧跟 Apple 的步伐，毕竟现在「小而美」的微信，也早已是 iOS 13 系统起步。

![](https://cdn.zhangferry.com/Images/85-ios16-ipados16.png)

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

继续推荐近期的一些优秀博文，涵盖 Swift 混编 Module、App Store 价格新政、内存优化、Xcode 命令行参数和构建配置等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[云音乐 Swift 混编 Module 化实践](https://juejin.cn/post/7207269389474037817 "云音乐 Swift 混编 Module 化实践") -- 来自：网易云音乐技术团队 冰川

[@东坡肘子](https://www.fatbobman.com/): 云音乐 iOS App 经历多年的迭代，积累了大量的 Objective-C（以下简称 OC）代码。在云音乐中集成的创新业务，因为依赖的历史基础库较少，已经投入使用 Swift。但主站业务迟迟没有投入，主要原因是由于大量的 OC 业务基础库和公共基础库不支持 Swift 混编。OC 组件库参与混编的前提是要完成 Module 化。本文主要介绍在支持云音乐 Swift 混编过程中，Module 化阶段的分析与实践。

2、[关于 App Store 苹果商店价格的那些事（历上最全版）](https://juejin.cn/post/7205562168358895671 "关于 App Store 苹果商店价格的那些事（历上最全版）") -- 来自：37 手游 iOS 技术运营团队

[@东坡肘子](https://www.fatbobman.com/): 自 2008 年苹果 iPhone 3G 和 App Store 推出，到如今 App Store 已经是世界最大的软件商店！苹果于 2022 年 12 月 6 日宣布对 App Store 定价机制作出重大升级，新增了 700 个价格点。本文是 37 手游 iOS 技术运营团队对当前 App Store 定价机制的总结和分析。本文在创作过程中使用了 ChatGPT 和 NotionAI 进行了辅助，也算是一项不错的尝试。

3、[SwiftUI + Core Data App 的内存占用优化之旅](https://www.fatbobman.com/posts/memory-usage-optimization/ "SwiftUI + Core Data App 的内存占用优化之旅") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 尽管 SwiftUI 的惰性容器以及 Core Data 都有各自的内存占用优化机制，但随着应用视图内容的复杂（ 图文混排 ），越来越多的开发者遇到了内存占用巨大甚至由此导致 App 崩溃的情况。本文将通过对一个演示 App 进行逐步内存优化的方式（ 由原先显示 100 条数据要占用 1.6 GB 内存，优化至显示数百条数据仅需 200 多 MB 内存 ），让读者对 SwiftUI 视图的存续期、惰性视图中子视图的生命周期、托管对象的惰值特性以及持久化存储协调器的行缓存等内容有更多的了解。

4、[将 Streaks Apple Watch App 转换为 SwiftUI](https://crunchybagel.com/converting-streaks-apple-watch-app-to-swiftui/ "将 Streaks Apple Watch App 转换为 SwiftUI") -- 来自：Quentin Zervaas

[@东坡肘子](https://www.fatbobman.com/): Streaks 是一款荣获 Apple 设计奖的代办事项列表应用。经过了 2 年的努力，开发团队将 Apple Watch 版本的开发框架转换成了 SwiftUI。本文讨论了实现这一里程碑改动的一些技术细节，以及本次转换过程的感受。

5、[在 SwiftUI 中设置不同的环境：命令行参数和构建配置](https://holyswift.app/best-ways-to-set-up-environment-in-swiftui/ "在 SwiftUI 中设置不同的环境：命令行参数和构建配置") -- 来自：Leonardo

[@东坡肘子](https://www.fatbobman.com/): 你是否厌倦了在你的 SwiftUI 应用中硬编码配置设置和数据？您想在运行时向你的应用程序传递值，而不需要手动更改代码吗？不妨看看 Xcode 环境变量和命令行参数吧。在这篇文章中，作者将探讨如何使用这些强大的功能来设置配置值，并在运行时向你的 SwiftUI 应用程序传递参数。Leonardo 将介绍如何在 Xcode 构建设置中设置环境变量，以及如何在 SwiftUI 代码中访问它们。并且还将深入探讨如何使用命令行参数，在你的应用程序从命令行启动时向其传递数值。



## 摸一下鱼

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
