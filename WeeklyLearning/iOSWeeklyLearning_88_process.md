# iOS 摸鱼周报 #82

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：Xcode 14.3 RC 版本发布
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [Xcode 14.3 RC 版本发布](https://developer.apple.com/documentation/xcode-release-notes/xcode-14_3-release-notes "Xcode 14.3 RC 版本发布")

[@远恒之义](https://github.com/eternaljust)：Apple 于 2023 年 3 月 21 日发布了 [Xcode 14.3 RC 版本](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_14.3_Release_Candidate/Xcode_14.3_Release_Candidate.xip "Xcode 14.3 RC 版本下载")，新版本要求 macOS Ventura 13.0 系统及以上，最低兼容：MacBook Pro 2017 款、MacBook Air 2018 款、iMac 2017 款以及 Mac mini 2018 款等 Mac 机型。Xcode 14.3 内置 [Swift 5.8](https://www.hackingwithswift.com/articles/256/whats-new-in-swift-5-8 "Swift 5.8 中的新功能")，新版带来了可向后的函数返回部署 API、隐式 self 进行弱自我捕获、改进的结果生成器等新功能，同时内含 iOS 16.4 SDKs。本周三我下载好 Xcode 14.3 解压，编译了一下日常开发的 Swift 项目，仅遇到一个单行隐式函数表达式中，包含两个三元运算符的数据类型相加无法正常推导的报错，声明两个变量类型来拆分三元运算符后即通过了编译，目前暂无遇到其他报错信息。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

推荐近期的一些优秀博文，涵盖 CreateML 使用、Runtime 探索、XCTest 性能测试等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[CreateML 使用](https://mp.weixin.qq.com/s/FGwv9cvf1lZDaYa9dh_kmQ "CreateML 使用") -- 作者：王德亮 搜狐技术产品

[@东坡肘子](https://www.fatbobman.com/): CoreML 框架允许将机器学习模型整合到苹果平台的应用程序中。有许多种方法来创建可用于 CoreML 的模型，其中一种方式便是使用 Xcode 附带的 CreateML 开发者应用程序。本文将展示使用 CreateML 来创建模型的流程。

2、[iOS 底层之 Runtime 探索](https://juejin.cn/post/7207330728698806309 "iOS 底层之 Runtime 探索") -- 作者：Joe天青色

[@东坡肘子](https://www.fatbobman.com/): Runtime 简称运行时，Objective-C 语言将尽可能多的决策从编译时和链接时推迟到运行时。只要可能，它都会动态地进行操作。这意味着该语言不仅需要编译器，还需要运行时系统来执行编译的代码。运行时系统充当 Objective-C 语言的一种操作系统。作者将通过三篇文章来梳理并分享自己对 Runtime 的探索过程。

3、[只在视图 Body 中生存的变量](https://www.fatbobman.com/posts/variables-that-only-survive-in-view-body/ "只在视图 Body 中生存的变量") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 相信不少开发者都会在视图中使用过 `let _ = print("update")`，但很少有人会在 body 中去使用 var 来定义变量，因为实在找不到使用 var 的理由和意义。本文将探讨在 SwiftUI 的视图 body 中用 var 来创建变量的意义和可能的场景。

4、[用结构体包裹函数](https://paul-samuels.com/blog/2023/03/18/wrapping-functions-in-structs/ "用结构体包裹函数") -- 作者：Paul Samuels

[@东坡肘子](https://www.fatbobman.com/): 我们可以在 Swift 中使用函数来捆绑行为，并在我们的应用程序中方便地传递它。使用函数时，当我们遇到一些特殊的可用性问题，可以尝试通过将函数包装在一个结构中来解决。这篇文章 100% 不是建议把每个函数都包装在一个结构中，而是研究一些可能有意义的情况。

5、[使用 XCTest 框架在 Swift 中进行性能测试](https://swiftwithmajid.com/2023/03/15/performance-testing-in-swift-using-xctest-framework/ "使用 XCTest 框架在 Swift 中进行性能测试") -- 作者：Majid

[@东坡肘子](https://www.fatbobman.com/): 在 Swift 中，我们可以使用 XCTest 框架进行性能测试，它是 Xcode 开发环境的一部分。 XCTest 提供了一套全面的工具，用于编写、运行和分析 Swift 应用程序的单元测试和性能测试。 本周我们将学习如何使用 XCTest 框架在 Swift 中进行性能测试。作者 Majid 善长进行系列创作，本文或许是他有关 XCTest 框架的又一系例作品的开篇，目前已经完成了两篇。


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
