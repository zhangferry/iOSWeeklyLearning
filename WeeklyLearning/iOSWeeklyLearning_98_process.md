# iOS 摸鱼周报 #90

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

![](https://cdn.zhangferry.com/Images/85-ios16-ipados16.png)

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

推荐近期的一些优秀博文，内容涵盖可合并库、Swift on Server、Observation 框架、通过 ReviewKit 获得更多好评、Apple AR 技术全景等方面。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[了解可合并库](https://www.polpiella.dev/understanding-mergeable-libraries/ "了解可合并库") -- 作者：Pol Piella Abadia

[@东坡肘子](https://www.fatbobman.com/): 在 WWDC 2023 中，苹果推出了可合并的库。在此之前，开发者必须选择是将框架设置为静态库还是动态库。选择其中一种库类型可能会对应用程序的构建和启动时间性能产生连锁反应。但从 Xcode 15 开始，我们可以使用可合并的库，这是一种新类型的库，结合了动态库和静态库的优点，并且针对构建和启动时间性能进行了优化。在本文中，作者将向你展示可合并的库如何解决模块化代码库中的问题，以及使用方法。

2、[Swift on Server Tour](https://blog.kevinzhow.com/posts/why-swift-on-server/zh "Swift on Server Tour") -- 作者：Kevin

[@东坡肘子](https://www.fatbobman.com/): 作者将通过一系列文章，带领读者畅游 Swift on Server 的世界。这个系列主要面向服务器开发的初学者，因此除了功能实现外，还会写一些相关概念的内容。主题涉及：什么是 Server App、HTTP 请求的相关内容、选择你的框架 - Vapor、设计你的数据模型、设计你的 API、用户权限验证、测试你的 API、部署你的服务器、和其他语言一起工作等内容。目前已完成两章，敬请期待后续更新。

3、[深度解读 Observation —— SwiftUI 性能提升的新途径](https://www.fatbobman.com/posts/mastering-Observation/ "深度解读 Observation —— SwiftUI 性能提升的新途径") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 在 WWDC 2023 中，苹果介绍了 Swift 标准库中的新成员：Observation 框架。它的出现有望缓解开发者长期面临的 SwiftUI 视图无效更新问题。作者在文章中采取了问答的方式，全面而详尽地探讨了 Observation 框架，内容涉及其产生的原因、使用方法、工作原理以及注意事项等内容。

4、[ReviewKit：帮你的应用获得更多的 App Store 好评](https://www.fline.dev/introducing-reviewkit/ "ReviewKit：帮你的应用获得更多的 App Store 好评") -- 作者：Cihat Gündüz

[@东坡肘子](https://www.fatbobman.com/): 作为一名应用程序开发者，你应该知道用户评论对应用程序的成功和可信度有多重要。积极的评论不仅可以吸引更多用户，还可以帮助应用在 App Store 中获得更高的排名。然而，在不合适的时间或者向没有充分体验应用的用户要求评论可能会导致用户失望并获得负面反馈。ReviewKit 提供了一个简单而有效的解决方案，通过根据最近的使用记录智能地决定何时向用户请求应用程序评论。在本文中，作者介绍了如何使用 ReviewKit。

5、[掌握 Transaction，实现 SwiftUI 动画的精准控制](https://www.fatbobman.com/posts/mastering-transaction/ "掌握 Transaction，实现 SwiftUI 动画的精准控制") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): SwiftUI 因其简便的动画 API 与极低的动画设计门槛而广受欢迎。但是，随着应用程序复杂性的增加，开发者逐渐发现，尽管动画设计十分简单，但要实现精确细致的动画控制并非易事。同时，在 SwiftUI 的动画系统中，有关 Transaction 的解释很少，无论是官方资料还是第三方文章，都没有对其运作机制进行系统的阐述。文章将通过探讨 Transaction 的原理、作用、创建和分发逻辑等内容，告诉读者如何在 SwiftUI 中实现更加精准的动画控制，以及需要注意的其他问题。

6、[开发 visionOS 前，你需要了解的 Apple AR 技术全景](https://mp.weixin.qq.com/s/LTR9C2TmKVhuYgFpD5Bw1A "开发 visionOS 前，你需要了解的 Apple AR 技术全景") -- 作者：XR基地 XR 基地的小老弟

[@东坡肘子](https://www.fatbobman.com/): 自从 2017 年 Apple 推出 ARKit 以来，Apple AR 相关的技术已经发展了 6 年多了。在这个过程中，每年的 WWDC 都会有关于 AR 技术的 Sessions。然而，由于使用场景的限制，大多数开发者可能仅仅是知道 Apple 有 AR 相关的技术，但对这项技术并没有实际的上手或深入了解。因此，对于 iOS 开发者来说，它可能是一个“熟悉的陌生人”。本文作者将从以下方面出发，帮助读者对 Apple AR 技术有一个大致的了解：2017~2022 年 WWDC 的进展、从官方 30+ 个 Sample Code 中总结出的 AR 整体框架、所有 AR App 都会用到的最基础的代码和编程概念、精进 Apple AR 必须了解的其他技术，以及入门 Apple AR 的推荐资料。作者希望读者在阅读本文后能够更好地理解 Apple AR 技术，并成为与之可以进一步合作的同事。


## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
