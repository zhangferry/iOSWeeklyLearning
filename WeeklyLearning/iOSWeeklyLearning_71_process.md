# iOS 摸鱼周报 #71 | One More Thing?

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：十月份 One More Thing? Apple 新增 QA 活动；Swift 和  SwiftUI 在 iOS 系统中的使用情况。 
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### One More Thing?

[@zhangferry](zhangferry.com)：虽然还没有官宣，但是网上已经讨论很多了，Apple 10 月还会有一场发布会。YouTube 博主 GregsGadgets 录了一期视频爆料新产品：[Apple October Event LEAKS!](https://www.youtube.com/watch?v=euUGv_Fz71o&list=RDCMUCoi3Uk6JtP9QgA5BRwnh6NQ "Apple October Event LEAKS!")。

![](https://cdn.zhangferry.com/Images/20221011224436.png)

新产品会有这些：New iPads、New M2 iPad Pros、M2 Mac mini、M2 MacBook Pro（14/16寸），M2 版本的 Mac Pro 和 Apple TV 也可能会一起发布。

### [Apple 提供 Ask People 服务](https://developer.apple.com/cn/events/ask-apple/ "Ask People")

![](https://cdn.zhangferry.com/Images/20221012233542.png)

[@zhangferry](zhangferry.com)：Apple 提供了 Ask People 服务让开发者能够通过 Slack 与 Apple 专家进行交流。Ask People 可以理解为一个 QA 环节，可以问代码级别的支持、设计建议、系统库使用等内容，Apple 指定了一段时间用于问答，从 10月 17 号开始到 21 号结束，这个期间会按照不同专题进行问答，这些专题对应 Slack 不同频道。活动注册，需要为开发者计划会员，具体日程和话题安排可以参照这个[日程表](https://developer.apple.com/cn/events/ask-apple/questions-and-answers/ "Ask People 日程表")。

Tech Talks 和 Meet with Apple Store Experts 项目在过去一年提供了 200 多个现场演示时长达数千小时。Apple 从这些活动中看到开发者对 Apple 专家交流的诉求，于是有了 Ask People。所以有理由相信后面还会有更多的 Ask People。

### [Swift 和 SwiftUI 在系统层面使用情况](https://blog.timac.org/2022/1005-state-of-swift-and-swiftui-ios16/ "Swift 和 SwiftUI 在系统层面使用情况")

[@zhangferry](zhangferry.com)：作者通过分析系统库的所有二进制文件来统计 Swift 和 SwiftUI 在系统版本上的占比情况：

![](https://cdn.zhangferry.com/Images/20221011222541.png)

统计方式是把系统中的所有二进制文件数量作为总数（不包含 XNU 和固件代码），如果该二进制文件中包含以上统计信息（语言或框架）就加一，按照比例划分做出上图。从这张图中可以得出以下结论：

* Objective-C 仍然是 iOS 系统的核心语言。
* Swift 在系统库中的使用越来越高，相对成熟；SwiftUI 开始崭露头角但仍处于早期阶段。
* C 语言在慢慢退出。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)


## 内容推荐

1、[StateObject 与 ObservedObject](https://www.fatbobman.com/posts/StateObject_and_ObservedObject/ "StateObject 与 ObservedObject") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：StateObject 和 ObservedObject 两者都是用来订阅可观察对象（ 符合 ObservableObject 协议的引用类型 ）的属性包装器。当被订阅的可观察对象通过内置的 Publisher 发送数据时（ 通过 @Published 或直接调用其 objectWillChange.send 方法 ），StateObject 和 ObservedObject 会驱动其所属的视图进行更新。StateObject 是在 SwiftUI 2.0 中才添加的属性包装器，它的出现解决了在某些情况下使用 ObservedObject 视图会出现超预期的问题。本文将介绍两者间的异同，原理以及注意事项。

2、[SwiftUI 开发之旅：适配深色模式](https://juejin.cn/post/7150553079060889614 "SwiftUI 开发之旅：适配深色模式") -- 来自：掘金 new_cheng

[@远恒之义](https://github.com/eternaljust)：从 iOS 13 开始，苹果支持了深色模式，在昏暗的环境中，我们打开深色模式可获得出色的视觉体验。SwiftUI 默认支持深色模式，对于基本视图的文字和背景都有默认的深色模式样式。本文作者介绍了 Color Set、overrideUserInterfaceStyle 等适配方法，还有如何支持用户手动切换颜色模式。对于深色模式的适配，推荐采用 Assets.xcassets 的方式去定义一个完整的颜色集来适配。

3、[How to dismiss sheet in SwiftUI](https://sarunw.com/posts/swiftui-dismiss-sheet/ "How to dismiss sheet in SwiftUI") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：模态或表单（.sheet）是 iOS 中的核心展示之一。在 SwiftUI 中有三种方法（`in the same view`、`with @Binding`、`with @Environment`）来关闭表单，具体的方式取决于你的视图结构以及支持的最低 iOS 版本。

4、[SwiftUI List Style examples](https://sarunw.com/posts/swiftui-list-style/ "SwiftUI List Style examples") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：SwiftUI 中的 list 列表有多种样式，基于不同的平台也支持许多不同的风格。本文中将专注于 iOS 平台，介绍六种不同的风格：`.automatic`、`.insetGrouped`、`.grouped`、`.inset`、`.plain`、`.sidebar`，每种样式都有简单的代码示例和展示配图。

5、[How to show badge on Tab Bar Item in SwiftUI](https://sarunw.com/posts/swiftui-tabbar-badge/ "How to show badge on Tab Bar Item in SwiftUI") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：tabItem 上的红点角标非常能吸引用户的注意，通常与应用程序图标上未读通知的数量相关联。在 SwiftUI 中，我们能非常方便的实现这个功能，使用 `badge(_:)` 来修饰选项卡栏项目（tabItem），支持设置整数（`.badge(3)`）和字符串（`.badge("99+")`）。

6、[How To Automatically Create .gifs From The iOS Simulator](https://digitalbunker.dev/automatically-create-gifs-from-the-ios-simulator/ "How To Automatically Create .gifs From The iOS Simulator")  -- 来自：digitalbunker

[@远恒之义](https://github.com/eternaljust)：如何在不需要任何第三方工具的情况下，直接从 iOS 模拟器录制视频并导出 .gif？首先，请按住 Option 键并将鼠标悬停在模拟器“保存屏幕”按钮上。按下该 Option 键，此设置将更改为“录制屏幕”。接着，你可以像往常一样继续录制你的应用程序。最后，停止录制，在视频预览消失之前，右键单击它并选择“另存为动画 GIF”。

![来自 digitalbunker 的演示操作 gif](https://cdn.zhangferry.com/Images/ios-simulator-gif.gif)

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
