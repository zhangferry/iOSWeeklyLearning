# iOS 摸鱼周报 #64 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题



## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)


## 内容推荐

整理编辑：[@远恒之义](https://github.com/eternaljust)

1、[SwiftUI 与 Core Data —— 安全地响应数据](https://www.fatbobman.com/posts/modern-Core-Data-Respond-Data-safely/ "SwiftUI 与 Core Data —— 安全地响应数据") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：保证应用不因 Core Data 的原因导致意外崩溃是对开发者的起码要求。本文将介绍可能在视图中产生严重错误的原因，如何避免，以及在保证视图对数据变化实时响应的前提下如何为使用者提供更好、更准确的信息。

2、[如何使用 SwiftUI Grid API 创建网格布局](https://www.appcoda.com.tw/swiftui-grid-api/ "如何使用 SwiftUI Grid API 创建网格布局") -- 来自：Simon Ng

[@远恒之义](https://github.com/eternaljust)：Grid 视图是一种容器视图，它以二维布局排列其他视图，Grid 为开发人员提供了构建基于网格的布局的更多选项。你可以使用 HStack 和 VStack 来构建类似的布局，不过 Grid 视图可以为你节省大量代码并使你的代码可读性更高，你可以尝试使用 Grid 来构建一些有趣的布局。

3、[如何对 SwiftUI list 中的列表行进行重新排序](https://sarunw.com/posts/swiftui-list-onmove/ "如何对 SwiftUI list 中的列表行进行重新排序") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：想要启用 SwiftUI 列表行重新排序，你只需执行以下步骤即可：创建数据源（必须是可变的）、使用填充列表视图 `ForEach`、将 `onMove(perform:)` 修饰符应用于 `ForEach`、手动移动项目 `onMove` 的闭包，调用方法十分简单方便。

4、[如何创建 iOS 锁屏小部件？](https://swiftsenpai.com/development/create-lock-screen-widget/?utm_source=rss&utm_medium=rss&utm_campaign=create-lock-screen-widget "如何创建 iOS 锁屏小部件？") -- 来自：Lee Kah Seng

[@远恒之义](https://github.com/eternaljust)：在 iOS 16 中，Apple 新增了锁定屏幕，其中锁屏小组件带来 app 新的曝光入口。与桌面小组件类似，锁屏小组件主要用 WidgetKit 来实现功能。不同的是，Apple 引入了 3 个新的不同类型的锁屏小组件：`accessoryCircular`、`accessoryRectangular` 和 `accessoryInline`，前两个为小与中两种尺寸，后者为单行文本。

5、[用 SwiftUI 实现 AI 聊天对话 app - iChatGPT](https://juejin.cn/post/7175051294808211512 "用 SwiftUI 实现 AI 聊天对话 app - iChatGPT") -- 来自掘金：37手游iOS技术运营团队

[@远恒之义](https://github.com/eternaljust)：iChatGP 是一款用 SwiftUI 实现的开源 ChatGPT app，支持系统 iOS 14.0+、iPadOS 14.0+、macOS 11.0+，目前已实现 ChatGPT 基本聊天功能：直接与 ChatGPT 对话，并且保留上下文；复制问题和回答内容；快捷重复提问。

6、[EBPF 介绍](https://coolshell.cn/articles/22320.html "EBPF 介绍") -- 来自：酷壳

[@远恒之义](https://github.com/eternaljust)：eBPF（extened Berkeley Packet Filter）是一种内核技术，它允许开发人员在不修改内核代码的情况下运行特定的功能。eBPF 比起传统的 BPF 来说，传统的 BPF 只能用于网络过滤，而 eBPF 则可以用于更多的应用场景，包括网络监控、安全过滤和性能分析等。耗子叔在文末留了一个彩蛋，聊了聊他对大火的 ChatGPT 一些看法。


## 摸一下鱼

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

1、[A Tour in the Wonderland of Math with Python](https://github.com/neozhaoliang/pywonderland) 通过渲染高质量的图像、视频和动画来展示数学之美。

![](https://cdn.zhangferry.com/Images/125026787-dad59700-e0b7-11eb-889f-b0c737413b6a.png)

2、[MindForger](https://www.mindforger.com/#home)，是一款个人知识管理工具

![](https://cdn.zhangferry.com/Images/1-title-screen.jpg)

MindForger的目标是模仿人类的思维--学习、回忆、识别、联想、遗忘--以实现与你的思维的协同，使你的搜索、阅读和写作更有效率。

不仅如此，MindForger 尊重隐私，并确保知识安全。

不仅仅是一个markdown 编辑器，更是一个辅助的智能助手。

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #63 | Apple 企业家培训营已开放申请](https://mp.weixin.qq.com/s/nAMshUG4AjWLAAHOFPVqXg)

[iOS 摸鱼周报 #62 |  Live Activity 上线 Beta 版 ](https://mp.weixin.qq.com/s/HySX4Yaf3Zxy8Wn-LyUO0A)

[iOS 摸鱼周报 #61 |  Developer 设计开发加速器](https://mp.weixin.qq.com/s/WfwqRhC-9-isUanv8ZnvMQ)

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
