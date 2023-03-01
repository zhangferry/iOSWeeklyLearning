# iOS 摸鱼周报 #82

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [在线讲座：与 App Store 专家会面交流](https://developer.apple.com/cn/news/?id=tfb0r2ql "在线讲座：与 App Store 专家会面交流")

[@远恒之义](https://github.com/eternaljust)：Apple 将于 2 月 28 日至 4 月 13 日举行「与 App Store 专家会面交流」在线讲座，探索如何吸引新顾客、测试营销策略、优化订阅等多个主题。感兴趣的 Apple Developer Program 开发者，可登录关联的 Apple ID，查看日程表并注册。

![](https://cdn.zhangferry.com/Images/85-event-appstore.jpeg)

### [Apple 公布 iOS 16 的普及率已达 81%](https://developer.apple.com/cn/support/app-store/ "Apple 公布 iOS 16 的普及率达 81%")

[@远恒之义](https://github.com/eternaljust)：Apple 官方数据来源于 App Store 上进行交易的设备统计，时间截止至 2023 年 2 月 14 日。在过去四年推出的设备中，iOS 16 的普及率达 81%。在所有的设备中，iOS 16 的普及率达 72%，加上 iOS 15 的 20%，iOS 15 系统及以上的普及率总计 92%。是时候修改 iOS 项目最低版本的限制了，开发者们要紧跟 Apple 的步伐，毕竟现在「小而美」的微信，也早已是 iOS 13 系统起步。

![](https://cdn.zhangferry.com/Images/85-ios16-ipados16.png)

## 内容推荐

本期将推荐近期的一些优秀博文，涵盖基于文本生成图像、SwiftUI 布局、Swift 静态代码检测、原生的 SwiftUI Markdown 渲染包等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[MarkdownView 从 0 到 1 —— 回顾整条时间线”](https://liyanan2004.github.io/the-road-of-markdown-view/ "MarkdownView 从 0 到 1 —— 回顾整条时间线") -- 来自：LiYanan2004

[@东坡肘子](https://www.fatbobman.com/): [MarkdownView](https://github.com/LiYanan2004/MarkdownView) 是一个用于在 SwiftUI 中原生渲染 Markdown 的 Swift 软件包，不久前刚刚正式发布了 1.0 版本。该包的作者 LiYanan2004 通过本文回顾了开发的动机、历程，并分享了主要的技术点和一些解决方案。

2、[Swift 静态代码检测工程实践](https://kingnight.github.io/programming/2023/02/20/Swift静态代码检测工程实践.html "Swift静态代码检测工程实践") -- 来自：Kingnight

[@东坡肘子](https://www.fatbobman.com/): 随着 App 功能不断增加，工程代码量也随之快速增加，依靠人工 CodeReview 来保证项目的质量，越来越不现实，这时就有必要借助于自动化的代码审查工具，进行程序静态代码分析；提升自动化水平，提高团队研发效率。本篇文章将介绍 SwiftLint 的工作原理，配置文件的参数含义，同时还介绍了 SwiftLint 内置规则的分类、如何读懂规则说明、如何禁用规则；另外从工程实践角度出发，给出了一些切实可行的建议，并详解了如何添加自定义规则；最后在大项目改进耗时方面给出了解决方案。

3、[一段因 @State 注入机制所产生的‘灵异代码’](https://www.fatbobman.com/posts/bug-code-by-state-inject/ "一段因 @State 注入机制所产生的‘灵异代码’") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 本文将通过一段可复现的“灵异代码”，对 State 注入优化机制、模态视图（ Sheet、FullScreenCover ）内容的生成时机以及不同上下文（ 相互独立的视图树 ）之间的数据协调等问题进行探讨。

4、[用 SwiftUI 的方式进行布局](https://www.fatbobman.com/posts/bug-code-by-state-inject/ "用 SwiftUI 的方式进行布局") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 最近时常有朋友反映，尽管 SwiftUI 的布局系统学习门槛很低，但当真正面对要求较高的设计需求时，好像又无从下手。SwiftUI 真的具备创建复杂用户界面的能力吗？本文将通过用多种手段完成同一需求的方式，展示 SwiftUI 布局系统的强大与灵活，并通过这些示例让开发者对 SwiftUI 的布局逻辑有更多的认识和理解。

5、[swift -e 直接从命令行运行代码](https://blog.eidinger.info/swift-e-runs-code-directly-from-the-command-line "swift -e 直接从命令行运行代码") -- 来自：Marco Eidinger

[@东坡肘子](https://www.fatbobman.com/): 在 Swift 5.8 / Xcode 14.3 Beta 1 中引入的一个新的命令行选项，允许 Swift 执行单行代码。在这篇文章中，作者解释了这个可以为执行小型一次性任务或操作数据带来便利的 swift -e 的用法。

6、[使用 Core ML 在 Apple Silicon 上生成 Stable Diffusion 图像](https://www.createwithswift.com/generating-images-with-stable-diffusion-on-apple-silicon-with-core-ml/ "使用 Core ML 在 Apple Silicon 上生成 Stable Diffusion 图像") -- 来自：Moritz Philip Recke

[@东坡肘子](https://www.fatbobman.com/): Stable Diffusion 是 2022 年发布的基于深度学习的文本到图像模型，也是热门的人工智能工具之一。 它可用于根据文本描述生成图像。本文将介绍如何使用 Apple 的 Core ML Stable Diffusion Package 通过 Swift 在 Apple Silicon 上使用 Stable Diffusion 生成图像。

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
