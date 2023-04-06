# iOS 摸鱼周报 #82

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：WWDC 23 全球开发者大会日期公布
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [WWDC 23 全球开发者大会日期公布](https://developer.apple.com/cn/wwdc23/ "WWDC 23 全球开发者大会日期公布")

![](https://cdn.zhangferry.com/Images/89-wwdc23.jpeg)

Apple 宣布 WWDC 23 将在北京时间 6 月 6 日至 10 日举行，主要内容是为期一周丰富多彩的技术和社区活动，大会仍采用线上播放形式。通过邀请函图片猜测，本次大会 Apple 可能会带来新的 MR 头显硬件。除了 iOS、iPadOS、macOS、watchOS 和 tvOS 等系统新功能的更新，大会上是否会有 xrOS 新系统的推出也值得关注。

Apple 同时会在 Apple Park 举办面向开发者和学生的全天特别活动，[Swift Student Challenge](https://developer.apple.com/cn/wwdc23/swift-student-challenge/ "Swift Student Challenge ") 也将继续举行，全世界满足条件的学生可以构建自己的 App Playground。完成作品提交截止日期为太平洋夏令时间 2023 年 4 月 19 日，获奖者将会得到 WWDC23 专属夹克、AirPods Pro、定制徽章套装，以及一年开发者会员资格。此外，获奖者还有一次专属的随机抽取出席 Apple Park 特别活动的机会。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

推荐近期的一些优秀博文，涵盖：通过 ReplayKit 录制屏幕、在 SwiftUI 中使用相对比例进行布局、保护小组件中的用户隐私等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[当 matchGeometryEffect 不起作用时](https://chris.eidhof.nl/post/matched-geometry-effect/ "当 matchGeometryEffect 不起作用时") -- 作者：Chris Eidhof

[@东坡肘子](https://www.fatbobman.com/): 在 SwiftUI 中，视图的 modifier 顺序十分重要，不同的顺序可能会产生完全不一样的结果。作者通过分析一段 matchGeometryEffect 不起作用的代码，从另一个角度阐述了视图的布局逻辑以及 modifier 顺序的重要性。

2、[iOS ReplayKit 与 屏幕录制](https://juejin.cn/post/7217692600647254071 "iOS ReplayKit 与 屏幕录制") -- 作者：网易云音乐技术团队

[@东坡肘子](https://www.fatbobman.com/): 在客户端开发过程中，有时会遇到这样一些场景，需要对用户在应用内的操作做进行屏幕录制，甚至是系统层级的跨应用屏幕录制来实现某种特殊需求，例如在线监考、应用问题反馈、游戏直播等。网易云音乐技术团队在本文中介绍了云音乐 LOOK 直播客户端如何通过 ReplayKit Framework 实现了上述需求。

3、[在 SwiftUI 布局中使用百分比](https://oleb.net/2023/swiftui-relative-size/ "在 SwiftUI 布局中使用百分比") -- 作者：Ole Begemann

[@东坡肘子](https://www.fatbobman.com/): SwiftUI 没有提供使用相对大小进行布局的工具，例如“使此视图是其容器宽度的 50% ”。Ole Begemann 通过 Layout 协议实现了上述的想法，本文提供了思路以及完整代码。有趣的是，在 SwiftUI 1.0 的测试版本中，曾经出现过官方提供的使用相对比例进行布局的 modifier，不过在最终版本中取消了，并且也再没有出现过。

4、[onAppear 的调用时机](https://www.fatbobman.com/posts/onAppear-call-timing/ "onAppear 的调用时机") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): onAppear 是 SwiftUI 开发者经常使用的一个修饰符，但一直没有权威的文档明确它的闭包被调用的时机。本文将通过 SwiftUI 4 提供的新 API ，证明 onAppear 的调用时机是在布局之后、渲染之前。

5、[深入了解 NotificationCenter 的实现原理](https://juejin.cn/post/7216340356949459004 "深入了解 NotificationCenter 的实现原理") -- 作者：向辉_

[@东坡肘子](https://www.fatbobman.com/): NotificationCenter 是一个系统组件，它负责协调和管理事件的通知和响应。它的基本原理是基于观察者模式。由于 Apple 对其是闭源的，因此无法查看 NotificationCenter 的源码。作者采用了曲线救国的方式，通过分析开源的 Swift 来理解 NotificationCenter 的实现。

6、[设备锁定时如何隐藏敏感的小组件数据](https://swiftsenpai.com/development/hide-sensitive-widget-data/?utm_source=rss&utm_medium=rss&utm_campaign=hide-sensitive-widget-data "设备锁定时如何隐藏敏感的小组件数据") -- 作者：Lee Kah Seng

[@东坡肘子](https://www.fatbobman.com/): 随着 iOS 引入小组件，用户现在可以在锁屏和今日视图中轻松访问他们喜爱的应用程序的信息。尽管看起来不错，但这确实带来了隐私问题 —— 即使设备被锁定，敏感数据也可以被访问。在本文中，作者将介绍如何在小组件上隐藏敏感数据，保护用户隐私。


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
