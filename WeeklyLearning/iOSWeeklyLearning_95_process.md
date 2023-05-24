# iOS 摸鱼周报 #90

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [Xcode 14.3.1 RC 版本已修复打包导致的奔溃问题](https://developer.apple.com/forums/thread/727680#753414022 "Xcode 14.3.1 RC 版本已修复打包导致的奔溃问题")

[@远恒之义](https://github.com/eternaljust)：Apple 于 2023 年 5 月 17 日发布 Xcode 14.3.1 RC 版本，修复了在 Xcode 14.3 打包导致 iOS 13 系统上的奔溃问题。根据最新的版本发行说明，该问题表现为：用 Xcode 14.3 打包 Swift 项目混编 OC 协议，会导致在 iOS 13 系统出现启动奔溃 (When targeting devices running iOS 13, apps built with Xcode 14.3 and using Objective-C protocols from Swift, sometimes crash at launch)。Apple 已从 2023 年 4 月 25 日起，限制了最新提交至 App Store 的 App 必须使用 Xcode 14.1 或更高版本构建，还在使用低版本 Xcode 的同学，建议下载最新的 [Xcode 14.3.1 RC 版本](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_14.3.1_Release_Candidate/Xcode_14.3.1_Release_Candidate.xip "Xcode 14.3.1 RC 版本")来打包。

## 本周学习

整理编辑：[zhangferry](https://zhangferry.com)

这是学习 Glarity 项目的第二期，本期会更多的学习。

### 产品核心功能

**搜索引擎的结果**



**视频字幕**



**文章概要**



### 产品规划





## 内容推荐

推荐近期的一些优秀博文，涵盖：在 App Store 推广应用的技巧、SwiftUI 预览的工作原理、离屏渲染等方面的内容。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[在 App Store 中推广你的应用的 10 个技巧](https://www.avanderlee.com/optimization/getting-app-featured-app-store/ "在 App Store 推广你的应用的 10 个技巧") -- 作者：Antoine Van Der Lee

[@东坡肘子](https://www.fatbobman.com/): Antoine Van Der Lee 是一位知名博主，同时也开发了大量应用程序。在这篇文章中，他分享了一些获得苹果推荐的技巧和诀窍，有助于提高你的应用在 App Store 特色推荐中的曝光率。主要建议包括：告知苹果你的应用的存在、从苹果编辑团队的角度思考、优化你的 App Store 页面、本地化你的应用、获取更多评分、成为一个好的应用公民、让你的应用更无障碍、降低崩溃率、创新和采用最新功能、让你的应用更独特。提高应用的整体质量、经常填写推广表格告知苹果应用的新功能，可以增加推荐机会。

2、[在 CI/CD 中使用私有 Swift 包](https://www.polpiella.dev/private-swift-packages-on-ci-cd/ "在 CI/CD 中使用私有 Swift 包") -- 作者：Pol Piella Abadia

[@东坡肘子](https://www.fatbobman.com/): 这篇文章探讨了如何在持续集成环境下安全使用私有代码包,特别是 Swift 包。通过配置 Git 和访问令牌管理，作者设计了一种机制，可以在构建流程中临时获取访问权限，并在流程结束后立即撤销，保证私有包的安全与隐私。这种方法不但可以在本地开发环境和 CI、CD 环境保持一致的包依赖配置，还可以根据需要灵活地控制私有包的访问时长，值得 iOS 开发者学习和运用。除 Swift 包外，该方法也可以应用于其他语言和构建工具，对保护私有代码仓库安全至关重要。

3、[构建稳定的预览视图 —— SwiftUI 预览的工作原理](https://www.fatbobman.com/posts/how-SwiftUI-Preview-works/ "构建稳定的预览视图 —— SwiftUI 预览的工作原理") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 在这篇文章中，作者通过分析一段会导致预览视图崩溃的代码，向读者揭示了 SwiftUI 预览的工作原理和流程，包括生成衍生代码、准备项目资源、启动预览线程、加载衍生代码库、通过 XPC 进行通讯等操作。通过对原理的探讨，让读者认识到预览功能客观存在的局限性：虽然 Xcode 预览功能在视图开发流程中极为方便，但它仍处在一个功能受限的环境中。开发者使用预览时需要清醒地认识到其局限性，并避免在预览中实现超出其能力范围的功能。在下一篇文章中，作者还将会从开发者的角度来审视预览功能：它的设计目的、最适宜的使用场景以及如何构建稳定高效的预览。

4、[​一文学会 iOS 画中画浮窗](https://mp.weixin.qq.com/s/SDasEZ2cYmm9Kim0KlHicw "​一文学会 iOS 画中画浮窗") -- 作者：王德亮 搜狐技术产品

[@东坡肘子](https://www.fatbobman.com/): 在这篇文章中，作者详细介绍了两种实现 iOS 画中画浮动窗口的方法：将视图转换为视频并播放，以及播放空白视频并在窗口中显示视图。这两种方法都可以实现自定义画中画显示的效果。第一种方法提供了更多自定义显示的灵活性，但消耗更多 CPU 资源；第二种方法更轻量级，但需要依赖空白视频文件。因此，开发者应根据具体需求，选择方法时应考虑灵活性和资源消耗之间的平衡。

5、[离屏渲染](https://juejin.cn/post/7214018170833928250 "离屏渲染") -- 作者：Jony唐

[@东坡肘子](https://www.fatbobman.com/): 在 iOS 开发中，避免离屏渲染是提高应用性能的重要方法之一。离屏渲染会增加 GPU 的工作量和内存消耗，甚至可能降低性能。因此，重要的是要理解什么是离屏渲染及其影响因素。本文作者通过两篇文章深入探讨了离屏渲染，以及 UIKit 下常见的触发离屏渲染的操作。同时，作者也介绍了对应的优化技巧，以帮助开发者避免这些潜在的性能陷阱。这些知识不仅适用于 UIKit，也同样适用于 SwiftUI 开发。掌握它们可以更高效地开发出性能卓越的 iOS 应用。



## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、微软build大会



2、

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
