# iOS 摸鱼周报 #82

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：Apple 公布 iOS 16 的普及率已达 81%
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题



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

6、[Swift 5.8 的新功能](https://www.hackingwithswift.com/articles/256/whats-new-in-swift-5-8 "Swift 5.8 的新功能") -- 来自：Paul Hudson

[@东坡肘子](https://www.fatbobman.com/): 一如既往，Paul Hudson 又为我们带来了 Swift 新版本的功能介绍。他认为 Swift 5.8 本身更像是一个清理版本：有一些新增功能，但更多的是改进了已经被广泛使用的功能。在这篇文章中，作者将引导你了解这次最重要的变化，并提供代码示例和解释，以便你可以自己尝试这一切。


## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[roomgpt](https://www.roomgpt.io/ "roomgpt")：利用 AI 技术把你现有的房间生成一个 dream room，只需上传一张当前房间的图片即可。

![](https://cdn.zhangferry.com/Images/202303072231277.png)

2、[潮流周刊](https://weekly.tw93.fun/ "潮流周刊")：作者是妙言的开发者，一位前端工程师。潮流周刊已经发到 119 期了，看了下日期，真的是期期不落。周报里是这样定位这份周刊的：「记录每周看到的前端潮流技术，筛选后用接地气方式发布于此」。周报里保留了一定的生活气息，使得个人色彩相对浓厚。

这也为我对摸鱼周报如何设定基调起到了一定的参考意义，技术周报不一定就得是板板正正的，也可以有血有肉，有情绪，有个性。

3、[基于 ChatGPT 的 API 能做什么产品](https://decohack.zhubai.love/posts/2244447748458225664 "基于 ChatGPT 的 API 能做什么产品")：这是 DecoHack 周刊的第 50 期内容，ChatGPT 的 API 已经开放一周了，随之而来确实有很多基于此的产品出现，本期内容总结了很多有趣的产品。我关注到的产品有：

* [一键总结音视频内容](https://b.jimmylv.cn/ "一键总结音视频内容")：主要面向的是 B 站内容，可以自动总结视频信息。
* [roamaround.guide](https://roamaround.guide/ "roamaround.guide")：帮助制定旅游计划，我写了一个要去杭州游玩3天，这是它给的建议。

![](https://cdn.zhangferry.com/Images/202303072303406.png)

* [chatgpt-sidebar](https://chatgpt-sidebar.com/ "chatgpt-sidebar")：一个浏览器侧边栏插件，把一些常用的功能，像是文章总结，翻译，语法检查，代码解释等功能进行了一个聚合。

4、[ChatGPT Shortcut](https://newzone.top/chatgpt/ "ChatGPT Shortcut")：总结了 ChatGPT 的常见用法，并把一些使用的快捷指令进行了整理。prompts 是以英文来写的，因为 ChatGPT 语言处理能力非常强，换成中文处理也是可以的。

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
