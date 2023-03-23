# iOS 摸鱼周报 #88 | 把 AI 集成到研发流程 

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：Xcode 14.3 RC 版本发布
> * 内容推荐：推荐近期的一些优秀博文，涵盖 CreateML 使用、Runtime 探索、XCTest 性能测试等方面的内容
> * 摸一下鱼：集成 GPT-4 的 Cursor；CopilotX；AI 工具使用提效，Prompt 编写模式

## 本期话题

### [Xcode 14.3 RC 版本发布](https://developer.apple.com/documentation/xcode-release-notes/xcode-14_3-release-notes "Xcode 14.3 RC 版本发布")

[@远恒之义](https://github.com/eternaljust)：Apple 于 2023 年 3 月 21 日发布了 [Xcode 14.3 RC 版本](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_14.3_Release_Candidate/Xcode_14.3_Release_Candidate.xip "Xcode 14.3 RC 版本下载")，新版本要求 macOS Ventura 13.0 系统及以上，最低兼容：MacBook Pro 2017 款、MacBook Air 2018 款、iMac 2017 款以及 Mac mini 2018 款等 Mac 机型。

Xcode 14.3 内置 [Swift 5.8](https://www.hackingwithswift.com/articles/256/whats-new-in-swift-5-8 "Swift 5.8 中的新功能")，新版带来了可向后的函数返回部署 API、隐式 self 进行弱自我捕获、改进的结果生成器等新功能，同时内含 iOS 16.4 SDK。

本周三我下载好 Xcode 14.3 解压，编译了一下日常开发的 Swift 项目，仅遇到一个单行隐式函数表达式中，包含两个三元运算符的数据类型相加无法正常推导的报错，声明两个变量类型来拆分三元运算符后即通过了编译，目前暂无遇到其他报错信息。

## 内容推荐

推荐近期的一些优秀博文，涵盖 CreateML 使用、Runtime 探索、XCTest 性能测试等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[CreateML 使用](https://mp.weixin.qq.com/s/FGwv9cvf1lZDaYa9dh_kmQ) -- 作者：王德亮 搜狐技术产品

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

本周 AI 领域又迎来新一轮功能迭代：微软将 GPT-4 引入 Office 和 Copilot，将 DALLE2 引入 new bing；Google Bard 上线测试；Midjourney 上线了 V5 版本；多位国内科技圈大佬投身 AI 创业。AI 科技这一轮变化真的太快，还没完全适应，多种全新能力就诞生出来了。

1、[Cursor](https://www.cursor.so/ "Cursor")：集成 GPT-4 的代码编辑器，不需要 OpenAI Key，免费使用。体验了一下，感觉真的改变了很多编程习惯。它主要有这几个功能：

* Generate：用于生成内容，在空白区域键入 Commond + K，输入指令即可。这里即可以生成模版代码，也可以通过提问题的方式，让它给出答案。

* Edit：代码编辑，这里需要选中代码才能执行编辑操作。我在上一步问了 IDE 一个问题，如果在 Swift 中调用 C 函数，它给了我一个示例。然后我选中这段代码，执行Edit，输入指令：把示例中的 int 参数转成 char 参数。它逐行扫描，还显示出了修改之后的 Diff 信息，点击 Accept 即可以实现替换。

  ![](https://cdn.zhangferry.com/Images/202303212355300.png)

* Chat：这个也是针对内容选中的功能，它可以支持长段对话。我让它帮我介绍整个文件的含义，有时中文输入的问题，结果还是英文。然后问他代码有没有什么优化的空间，它也很快给了一些建议，也挺符合编程规范的。

![](https://cdn.zhangferry.com/Images/202303212334574.png)

基于GPT4协作编程这件事，有人总结了一些[可以遵循的要点](https://twitter.com/goldengrape/status/1638049866604777472 "GPT4协作编程要点-Twitter")：

> 0.建立一个markdown文件记录prompt 
>
> 1.写明程序目的 
>
> 2.写明程序实现目的的方法/流程 
>
> 3.注明编程风格，要求GPT4写出函数的作用描述、输入、输出，但不必列出函数的具体实现。 
>
> 4.由GPT4生成函数设计 
>
> 5.注明需要使用的库，列出库中的几个典型示例，复制之上所有部分交GPT4生成代码
>
> 6.debug，将代码和报错一起交给GPT4，询问错误出现的原因，并修改。注意GPT4的知识过时，有可能引用不存在的库中的函数方法，可能需要以ChatPDF或者Bing Chat协助或者手动找到对应的函数，并找到说明或者示例，一同交给GPT4生成新代码。 
>
> 7.记录debug要点于文件中。

2、[CopilotX](https://github.com/features/preview/copilot-x "GopilotX")：之前的 Github Copilot 是基于 GPT-3 实现的，随着 GPT-4 的到来，Github Copilot 随之升级，就是 CopilotX。Github 对于 CopilotX 的定位并非只是代码补全，而是希望它能成为一个为开发全流程赋能的工具。CopilotX 能够在 pull request、终端才做、开发文档等多个常用流程提供帮助。目前 [CopilotX for docs](https://githubnext.com/projects/copilot-for-docs "https://githubnext.com/projects/copilot-for-docs") 和 [Copilot for CLI](https://githubnext.com/projects/copilot-cli "Copilot for CLI") 目前可以加入 waitlist 等待内测。

随着 GPT-4 使用成本的降低，借由 CopilotX 的思路，相信会有更多 AI 工具填充到我们的产研链路中。

![](https://cdn.zhangferry.com/Images/202303232250503.png)

3、[Prompt 编写模式](https://prompt-patterns.phodal.com/ "Prompt 编写模式")：像 ChatGPT、MidJourney 这类 AI 工具，正在一步步颠覆我们之前对工具的使用方式。如何使用 AI，就像是电脑刚出现时，如何使用电脑一样，它很强大，但如何发挥它的强大，如何借助于 AI 让自己的做事效率提升，这是一件差异很大的事情。

目前我们跟 AI 的交互基本都是通过 Prompt 进行的，如何编写 Prompt，如果高效的获取我们希望的结果，正是这篇文章想要解答的问题。作者并非按各个用途总结 Prompt 使用方式，而是按照设计模式的形式把跟AI对话的 Prompt 进行了抽象，正如它的目标：**如何将思维框架赋予机器，以设计模式的形式来思考 prompt**。

![](https://cdn.zhangferry.com/Images/202303222234824.png)

## 岗位推荐：小红书-直播-iOS

### 岗位要求

* 参与小红书直播生态业务建设
* 负责视频录制开播推流，IM交互，礼物打赏，直播带货等完整直播场景的功能研发迭代
* 能够在数据分析的支持下提升直播相关功能的性能，主播开播体验，以及观看，购买和互动体验
* 3年以上工作经验；扎实的编程和数据结构算法基础；有直播项目经验者优先

### 岗位介绍

* 绝对的上升部门，前景光明，机会多多。[晚点独家丨小红书调整组织架构，押注直播电商，结束社区和商业化之争](https://mp.weixin.qq.com/s/O2XYOoYnE7gBJJDkG2DYzw)
* 团队成员多样化，有抖快来的资深大神也有刚毕业的00后应届生，团队氛围轻松愉悦
* 免费三餐 + 免费零食饮料，节日生日周年日各种福利，团建费多多（200/人月+额外奖励）
* 大小周，周六双倍，其他节假日极少加班，如有则三/双倍

工作地点：北京 地铁10号线 安贞门站 中海国际中心A座（地下直通）

联系方式：hulong1@xiaohongshu.com

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #87 | Planning for AGI](https://mp.weixin.qq.com/s/TwugmMEiGoFKYQY9euhg6Q)

[iOS 摸鱼周报 #86 | 更多基于 ChatGPT API 的产品诞生了](https://mp.weixin.qq.com/s/y1_V0WKfdwsUL2WjP2zPyA)

[iOS 摸鱼周报 #85 | ChatGPT 的 API 开放使用](https://mp.weixin.qq.com/s/Hhb7ZCDDqEcpIRTlUKiGTQ)

[iOS 摸鱼周报 #84 | 开箱即用的云服务 AirCode](https://mp.weixin.qq.com/s/fKutqWAHfzkbbFgYCvPfIA)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
