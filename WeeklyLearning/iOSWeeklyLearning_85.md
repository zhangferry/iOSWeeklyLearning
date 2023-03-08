# iOS 摸鱼周报 #85 | ChatGPT 的 API 开放使用

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：在线讲座：与 App Store 专家会面交流；加速器线上活动：设计挑战（亚太）
> * 内容推荐：本期将推荐近期的一些优秀博文，涵盖基于文本生成图像、SwiftUI 布局、Swift 静态代码检测、原生的 SwiftUI Markdown 渲染包等方面的内容
> * 摸一下鱼：ChatGPT 的 API 开发使用；Notion AI 体验；new bing 体验；针对程序员的智能搜索引擎 phind

## 本期话题

### [在线讲座：与 App Store 专家会面交流](https://developer.apple.com/cn/news/?id=tfb0r2ql "在线讲座：与 App Store 专家会面交流")

[@远恒之义](https://github.com/eternaljust)：Apple 会在 2 月 28 日至 4 月 13 日举行「与 App Store 专家会面交流」在线讲座，探索如何吸引新顾客、测试营销策略、优化订阅等多个主题。感兴趣的 Apple Developer Program 开发者，可登录关联的 Apple ID，查看日程表并注册。

### [加速器线上活动：设计挑战（亚太）](https://developer.apple.com/events/view/R67PUKP9H9/dashboard "加速器线上活动：设计挑战（亚太）")

[@远恒之义](https://github.com/eternaljust)：新一期的线上讲座开启，优秀的 App 少不了卓越的设计，与 Apple 设计布道师一起学习重要设计原理的实践方式，并在两项设计挑战当中展示你的设计技能。

![](https://cdn.zhangferry.com/Images/85-developer-design.jpeg)

## 内容推荐

本期将推荐近期的一些优秀博文，涵盖基于文本生成图像、SwiftUI 布局、Swift 静态代码检测、原生的 SwiftUI Markdown 渲染包等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[MarkdownView 从 0 到 1 —— 回顾整条时间线”](https://liyanan2004.github.io/the-road-of-markdown-view/ "MarkdownView 从 0 到 1 —— 回顾整条时间线") -- 来自：LiYanan2004

[@东坡肘子](https://www.fatbobman.com/): [MarkdownView](https://github.com/LiYanan2004/MarkdownView) 是一个用于在 SwiftUI 中原生渲染 Markdown 的 Swift 软件包，不久前刚刚正式发布了 1.0 版本。该包的作者 LiYanan2004 通过本文回顾了开发的动机、历程，并分享了主要的技术点和一些解决方案。

2、[Swift 静态代码检测工程实践](https://kingnight.github.io/programming/2023/02/20/Swift静态代码检测工程实践.html "Swift静态代码检测工程实践") -- 来自：Kingnight

[@东坡肘子](https://www.fatbobman.com/): 随着 App 功能不断增加，工程代码量也随之快速增加，依靠人工 CodeReview 来保证项目的质量，越来越不现实，这时就有必要借助于自动化的代码审查工具，进行程序静态代码分析；提升自动化水平，提高团队研发效率。本篇文章将介绍 SwiftLint 的工作原理，配置文件的参数含义，同时还介绍了 SwiftLint 内置规则的分类、如何读懂规则说明、如何禁用规则；另外从工程实践角度出发，给出了一些切实可行的建议，并详解了如何添加自定义规则；最后在大项目改进耗时方面给出了解决方案。

3、[一段因 @State 注入机制所产生的‘灵异代码’](https://www.fatbobman.com/posts/bug-code-by-state-inject/ "一段因 @State 注入机制所产生的‘灵异代码’") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 本文将通过一段可复现的“灵异代码”，对 State 注入优化机制、模态视图（ Sheet、FullScreenCover ）内容的生成时机以及不同上下文（ 相互独立的视图树 ）之间的数据协调等问题进行探讨。

4、[用 SwiftUI 的方式进行布局](https://www.fatbobman.com/posts/layout-in-SwiftUI-way/ "用 SwiftUI 的方式进行布局") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 最近时常有朋友反映，尽管 SwiftUI 的布局系统学习门槛很低，但当真正面对要求较高的设计需求时，好像又无从下手。SwiftUI 真的具备创建复杂用户界面的能力吗？本文将通过用多种手段完成同一需求的方式，展示 SwiftUI 布局系统的强大与灵活，并通过这些示例让开发者对 SwiftUI 的布局逻辑有更多的认识和理解。

5、[swift -e 直接从命令行运行代码](https://blog.eidinger.info/swift-e-runs-code-directly-from-the-command-line "swift -e 直接从命令行运行代码") -- 来自：Marco Eidinger

[@东坡肘子](https://www.fatbobman.com/): 在 Swift 5.8 / Xcode 14.3 Beta 1 中引入的一个新的命令行选项，允许 Swift 执行单行代码。在这篇文章中，作者解释了这个可以为执行小型一次性任务或操作数据带来便利的 swift -e 的用法。

6、[使用 Core ML 在 Apple Silicon 上生成 Stable Diffusion 图像](https://www.createwithswift.com/generating-images-with-stable-diffusion-on-apple-silicon-with-core-ml/ "使用 Core ML 在 Apple Silicon 上生成 Stable Diffusion 图像") -- 来自：Moritz Philip Recke

[@东坡肘子](https://www.fatbobman.com/): Stable Diffusion 是 2022 年发布的基于深度学习的文本到图像模型，也是热门的人工智能工具之一。 它可用于根据文本描述生成图像。本文将介绍如何使用 Apple 的 Core ML Stable Diffusion Package 通过 Swift 在 Apple Silicon 上使用 Stable Diffusion 生成图像。

## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[ChatGPT 和 Whisper 模型 API 开放](https://openai.com/blog/introducing-chatgpt-and-whisper-apis "ChatGPT 和 Whisper 模型 API 开放")：在 OpenAI 团队一些列的优化下，ChatGPT 的成本降低了 90%，他们要把这部分节省的钱回报开发者，现在开发者可以用相当于 GPT 3.5 十分之一的价格来使用 ChatGPT 的API。之前很多基于 OpenAI API 开发的对话功能将模型从`text-davinci-003`切到`gpt-3.5-turbo`，即完成了切换。作为开发者可以关注这些事项：

* 除非机构选择加入，否则通过 API 提交的数据不再用于服务改进（包括模型训练）。
* 为API用户实施默认的 30 天数据保留政策，并根据用户需求提供更严格的保留选项。
* 移除我们的预发布审核（通过改进自动监控而解锁）。
* 改进开发人员文档。
* 简化我们的服务条款和使用政策，包括关于数据所有权的条款：用户拥有模型的输入和输出。

同时 OpenAI CEO 在推特上发表了一则信息：

> a new version of moore’s law that could start soon: the amount of intelligence in the universe doubles every 18 months

即人工智能领域的摩尔定律，宇宙中的智能数量每 18 个月会翻一倍。

伴随 ChatGPT 这个风口，相信会有越来越多的基于这个模型的应用场景诞生出来，而更多应用场景更有助于推进 AI 相关技术的快速发展，或许一个新的时代已经到来。

2、[Notion AI 上线](https://www.notion.so/product/ai "Notion AI 上线")：在 Notion AI 的 whitelist 里排了两周多时间都没有获得资格，竟然正式上线了。免费用户有 20 次的使用额度，之后就需要付费，每月 $10。体验了一下 Notion AI 的写作方式，我让它写一篇介绍 NotionAI 和 ChatGPT 这类 AIGC 工具的文章。

![](https://cdn.zhangferry.com/Images/202302261414807.png)

文章思路和内容都很强，关键还非常快。

3、等了两周 new bing whitelist，都没有回音。给 bing 团队回了一封邮件，隔了一天测试资格就下来了。需要使用 Edge 浏览器才能体验，我问了它：作为计算机专业学生，可以帮我选一款笔记本电脑吗：

![](https://cdn.zhangferry.com/Images/202302261723153.png)

相比 ChatGPT，它的速度更快，且检索不再有训练模型的限制，不能回答2021年之后的问题，而是可以回答任何实时性的问题；为了让 Chat 过程更人性化，回答内容还会包含一些 emoji 和原文链接内容。当然不只是内容检索，内容创作也完全可以。

相比搜索引擎它可以理解自然语言，且有上下文能力。它的工作流程可以看出来是先把自然语言转成搜索引擎识别的关键字，然后检索结果，并用自然语言生成。当这种自然的检索能力跟商业化结合起来，比如测试的电商场景，如何定义性能强劲、如何定义性价比，谁排名靠前，让算法做决定，它选择哪一个。这些原本人为判断的过程，都可以作为 AI 的选择路径之一，细想一下真的不要太强大。

4、[phind](https://phind.com/ "phind")：一个针对研发者的 AI 搜索引擎，我试了几个问题，跟 ChatGPT 回答的差不多，感觉还要更详细一些。同时它还会把参考文档一起列出来，可以选择时效时间。

![](https://cdn.zhangferry.com/Images/202302261834156.png)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #84 | 开箱即用的云服务 AirCode](https://mp.weixin.qq.com/s/fKutqWAHfzkbbFgYCvPfIA)

[iOS 摸鱼周报 #83 | ChatGPT 的风又起来了](https://mp.weixin.qq.com/s/Ty95hGBIevHaJQ5TU774aQ)

[iOS 摸鱼周报 #82 | 去中心化社交软件 Damus](https://mp.weixin.qq.com/s/ck4Jn4Cq-yOs_mjAO-WacA)

[iOS 摸鱼周报 #81 | Apple 推出 Apple Business Connect](https://mp.weixin.qq.com/s/Ek6W0MTBDP6PN1uxWQ5M_A)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
