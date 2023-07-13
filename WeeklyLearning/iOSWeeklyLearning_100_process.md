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

推荐近期的一些优秀博文，内容涵盖 String Catalogs、自定义字体加载、HTTP 类型、单向数据流、构建类 Facetime 应用等方面。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[与 String Catalogs 有关的常见问题解答](https://www.fline.dev/the-missing-string-catalogs-faq-for-xcode-15/ "与 String Catalogs 有关的常见问题解答") -- 作者：Cihat Gündüz

[@东坡肘子](https://www.fatbobman.com/): 在 WWDC23 上，苹果为 Xcode 推出了一个新功能：String Catalogs。该功能取代了传统的本地化文件，简化了本地化流程。本文作者同时为 [RemafoX](https://remafox.app/)（ 一个本地化工具）的开发者，他在 Slack activity 上与苹果的工程师进行了深入探讨。作者将通过问题解答的形式对 String Catalogs 进行说明，以帮助开发者了解为什么应该对 Xcode 15 中的这个强大工具感到兴奋。

2、[使用 Swift Package 插件将自定义字体加载到应用程序中](https://www.polpiella.dev/load-custom-fonts-with-no-code-using-swift-package-plugins/ "使用 Swift Package 插件将自定义字体加载到应用程序中") -- 作者：Pol Piella Abadia

[@东坡肘子](https://www.fatbobman.com/): 如果你发现自己一遍又一遍地使用相同的字体，那么就要考虑是否需要创建一个 Swift Package 来包含共享的字体文件和字体加载代码。这样可以更快地创建新的应用程序，通过一个单一的地方来更新所有应用程序的字体文件，并减少代码重复。本文作者将向你展示如何使用 [SwiftGen](https://github.com/SwiftGen/SwiftGen) 来实现这一点，让你的应用程序更加高效和可维护。

3、[介绍 Swift HTTP 类型](https://www.swift.org/blog/introducing-swift-http-types/ "介绍 Swift HTTP 类型") -- 作者：Guoye Zhang、Eric Kinnear、Cory Benfield

[@东坡肘子](https://www.fatbobman.com/): Swift 社区刚刚发布了一个名为 [Swift HTTP Types](https://github.com/apple/swift-http-types) 的开源软件包，通过 HTTPRequest 和 HTTPResponse 提供了 HTTP 消息的核心构建块的通用表示。在项目中采用这些类型，可以在客户端和服务器之间共享更多的代码，从而减少在类型之间进行转换的成本。Swift 社区的最终目标是使用 Swift HTTP Types 替换 SwiftNIO 的 HTTPRequestHead 和 HTTPResponseHead，以及 Foundation 的 URLRequest 和 URLResponse 中的 HTTP 消息信息。

4、[单向数据流](https://swiftwithmajid.com/2023/07/11/unidirectional-flow-in-swift/ "单向数据流") -- 作者：Majid

[@东坡肘子](https://www.fatbobman.com/): Majid 写过很多关于 SwiftUI 数据流的文章，分享了他在该领域的灵感和想法。这些想法经过多年应用程序构建的实践，最终产生了一个名为 [swift-unidirectional-flow](https://github.com/mecid/swift-unidirectional-flow) 的 Swift 软件包。该软件包实现了 Majid 所有的想法，并被用于他的项目中，支持并发以及构建实际应用所需的其他功能（如可预测、可预览、可调试、模块化）。但是，Majid 并不建议开发者直接使用该软件包。他认为，开发者不应该导入任何第三方库或框架来构建应用程序的核心功能。你可以使用它作为灵感，在应用程序中根据你的需求构建状态管理系统。

5、[流式视频通话：如何使用 SwiftUI 构建类似 FaceTime 的应用](https://getstream.io/blog/facetime-clone/ "流式视频通话：如何使用 SwiftUI 构建类似 FaceTime 的应用") -- 作者：Amos G

[@东坡肘子](https://www.fatbobman.com/): 无论通话参与者身在何处，使用苹果设备，都可以通过 FaceTime 创建一对一或群组的音频/视频通话。本文将演示如何使用 SwiftUI 和 iOS Video SDK from Stream 来构建一个类似 FaceTime 的应用，与朋友和家人进行面对面的聊天。构建的 iOS 语音和视频通话应用程序可以支持多种用例，例如 1-1 通话，群组会议，远程医疗，约会和会议等。


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
