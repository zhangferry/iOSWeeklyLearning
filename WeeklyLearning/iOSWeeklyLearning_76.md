# iOS 摸鱼周报 #76 | 如何智慧提问？

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本周学习：如何智慧提问？
> * 内容推荐：SwiftUI 相关的一些博客推荐
> * 摸一下鱼：Combine 操作符；Token，Session，JWT 这些鉴权技术有哪些区别？Mac 版微信为何不断往电脑中写日志？；Github 开源两款字体；一个摸鱼小网站。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### 面向程序员，如何智慧提问？

在平时的工作中，相信很多的程序员小伙伴都面临两个问题：

- 经常不知道如何提出自己的问题
- 经常被其他同学打断自己的编码思路

这两个问题曾也久久困扰着小编。那么如何提升提问和被提问的能力？我们今天就聊聊**智慧的提问**这个很虚但很实用的话题，它适用于开发，产品，运营等同学

#### 提问前需要做什么？

在你准备提问时，你应该是有做过思考和前期准备的。对于程序员来说，当你遇到业务问题或者是技术问题。那么你应该有如下几点需要做到：

>尝试在旧的问题列表找到答案。
>
>尝试上网搜索以找到答案。
>
>尝试阅读手册以找到答案。
>
>尝试阅读常见问题文件（FAQ）以找到答案。
>
>尝试自己检查或试验以找到答案。
>
>尝试阅读源码找到答案。

当你提出问题的时候，请先表明你已经做了上述的努力；这将有助于树立你并不是一个不劳而获且浪费别人的时间的提问者。如果你能一并表达在做了上述努力的过程中所**学到**的东西会更好，因为我们更乐于回答那些表现出能从答案中学习的人的问题。

**准备好你的问题，再将问题仔细的思考过一遍，然后开始提问**

#### 提问时如何描述问题？

如何很好的提问，这也是我们常见的一些问题。下面是常用的一些手段：

> 使用有意义且描述明确的标题
>
> 精确地描述问题并言之有物
>
> 话不在多而在精
>
> 别动不动就说自己找到了 Bug
>
> 描述实质问题而不是你的猜测问题
>
> 按发生时间先后列出问题症状
>
> 询问有关代码的问题时，不要直接粘贴几百行代码
>
> 去掉无意义的提问句，减少无效内容
>
> 即使你很急也不要在标题写`紧急`，你可能直接都不知道是否紧急

#### Bad Question（蠢问题）

以下是几个经典蠢问题：

问题：我能在哪找到 X 程序或 X 资源？

问题：我怎样用 X 做 Y?

问题：我的程序/设定/SQL 语句没有用?

问题：我的 Mac 电脑有问题，你能帮我吗?

问题：我的程序不会动了，我认为系统工具 X 有问题

问题：我在安装 Linux（或者 X ）时有问题，你能帮我吗？

问题：你的程序有Bug，能帮我解决吗？

来源：[How To Ask Questions The Smart Way](http://www.catb.org/~esr/faqs/smart-questions.html "How To Ask Questions The Smart Way")和[提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md "提问的智慧")

## 内容推荐

整理编辑：[远恒之义](https://github.com/eternaljust)

1、[在 SwiftUI 中创建自适应的程序化导航方案](https://www.fatbobman.com/posts/adaptive-navigation-scheme/ "在 SwiftUI 中创建自适应的程序化导航方案") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：随着苹果对 iPadOS 的不断投入，越来越多的开发者都希望自己的应用能够在 iPad 中有更好的表现。尤其当用户开启了台前调度（ Stage Manager ）功能后，应用对不同视觉大小模式的兼容能力就越发显得重要。本文将就如何创建可自适应不同尺寸模式的程序化导航方案这一内容进行探讨。

2、[简介 iOS 16 新的 Layout 协议](https://www.appcoda.com.tw/ios16-layout-protocol/ "简介 iOS 16 新的 Layout 协议") -- 来自：appcoda

[@远恒之义](https://github.com/eternaljust)：在 iOS 16 中，Apple 推出了 Layout 协议，希望进一步简化在 SwiftUI 构建 UI Layout 的步骤。本文将介绍这个新协议的用途和使用方法，并用它们的 Layout 规则创建属于自己的容器。

3、[Swift project in 2023](https://www.swift.org/blog/focus-areas-2023/ "Swift project in 2023") -- 来自：swift.org

[@远恒之义](https://github.com/eternaljust)：来自 Swift 官网博客的消息，Swift 核心团队收集并整理了社区和论坛所关注的信息，列出了他们明年的工作计划和内容。其中核心团队会更新重组，将创建更多工作组，包括一个致力于提高 Swift 跨平台可用性的工作组。语言工作组专注于在五个主要语言领域：Concurrency（并发）、Generics（泛型）、Ownership（内存所有权）、Macros（宏）和 C++ interoperability（C++ 互操作性）。同时编译器开发团队将改进编译器与构建系统和自身其他调用的交互方式。其他还包括对 Swift 包管理器的优化，文档工作组将开发工具来解决文档需求，网站工作组专注于通过多种方式增强 swift.org 网站，服务器工作组专注于提升服务器和 Linux 上的 Swift 状态等。

4、[如何在 SwiftUI 中使用手势](https://www.swiftanytime.com/gestures-in-swiftui/ "如何在 SwiftUI 中使用手势") -- 来自：swiftanytime

[@远恒之义](https://github.com/eternaljust)：在如今的触摸屏手机中，实体按键快消失殆尽了，几乎所有的操作都基于手指手势。现代手机可以识别多种手势感应：点击、拖动、滑动、捏合、双击、旋转、摇动、触摸和长按等等，本文将介绍 SwiftUI 中一些基本且最常用的手势使用。

5、[SwiftUI 按钮的基本用法](https://sarunw.com/posts/swiftui-button-basic/ "SwiftUI 按钮的基本用法") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：SwiftUI 中的按钮十分方便使用和自定义。按钮界面很简单，只需要做两件事：动作和标签。动作是一种方法或闭包，当用户单击或点击按钮时会调用它，标签是描述按钮用途的视图，可以是文本、图标图像或任何自定义视图。使用自定义按钮也非常容易，任选 `buttonStyle(_:)` 内置五种按钮样式之一即可。

6、[如何在 SwiftUI 中使用自定义字体](https://sarunw.com/posts/swiftui-custom-font/ "如何在 SwiftUI 中使用自定义字体") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：要在 SwiftUI 中使用自定义字体，你需要执行以下步骤：查找在你的应用中能免费使用的自定义字体；将字体文件添加到你的 Xcode 项目，同时在 Info.plist 中引入注册；最后使用 `custom(_:size:)` 方法来初始化字体。

## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[Combine operators cheat sheet](https://tanaschita.com/20221121-cheatsheet-combine-operators/ "Combine operators cheat sheet")：Combine 里有很多操作符，这些操作符很多并不能通过命名就完全区分出来，那该如何记忆和理解这些操作符的含义呢，tanaschita 用 SwiftUI 实现了这些操作符的可视化表达。如果你看过 RxSwift 的文档应该对这些图标非常亲切。

![](https://cdn.zhangferry.com/Images/20221124201158.png)

2、[Session, cookie, token, JWT, SSO 和 OAuth 2.0 是什么](https://twitter.com/alexxubyte/status/1595455518583029764 "Session, cookie, token, JWT, SSO 和 OAuth 2.0 是什么")：这几种常用的身份校验技术有什么区别呢， Alex Xu 做了这样一张图用于解释它们的区别以及用于解决的问题。

![](https://cdn.zhangferry.com/Images/20221124205007.png)

3、[电脑端微信不断写日志](https://v.douyin.com/rVWRmUG/ "微信在电脑不断写日志")：来源于抖音一位技术博主的视频，详细描述了微信在电脑端不断写日志的过程。利用 Xcode 的 Instruments 里的 File Activity，采集微信在后台的文件读取记录。会发现很多 xlog 日志的生成，但因为文件是加密的，我们并不能解析里面是什么内容。我看了我电脑里的日志，有三天我的电脑都是没有打开的，但是却能找到这几天的 xlog 日志，也就是说即使是休眠状态，微信依然在尝试写东西。该日志并非完全本地，还会通过网络进行上传。目前关于这些数据是做什么的还没有查到任何相关资料。

如果你感觉不放心，可以通过这种方式，关闭日志写权限：

```bash
$ sudo chmod 400 ~/Library/Containers/com.tencent.xinWeChat/Data/Library/Caches/com.tencent.xinWeChat/2.0b4.0.9/log
```

4、对于新技术很多开发都会抑制不住想去尝试，比如 SwiftUI，当你有这种想法时你可能会理解这张图的含义。

![](https://cdn.zhangferry.com/Images/20221124205551.png)

5、[Github 推出的两种开源字体 mona & hubot sans](https://github.com/mona-sans "Github 推出的两种开源字体 mona & hubot sans")：这是一种强大而通用的字体，以Degarism风格设计，灵感来源于工业时代的怪诞风格。Mona Sans在产品、网络和印刷领域都很有效。Hubot Sans 字体更修长，有一种独特的技术感。

![](https://cdn.zhangferry.com/Images/20221124211158.png)

6、[Moyu.Games](https://moyu.games/ "摸鱼游戏")：一个站点聚合网站，一直工作也挺累的，偶尔摸摸鱼吧。

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #75 | 远程工作推行之难](https://mp.weixin.qq.com/s/nguqKvkuzDBR9o-Yw6y3KQ)

[iOS 摸鱼周报 #74 | 抖音 iOS 基础技术大揭秘 Vol.02 周六见](https://mp.weixin.qq.com/s/lhhV0Qlc9NtFoM6nF7gZbA)

[iOS 摸鱼周报 #73 | macOS Ventura 初体验](https://mp.weixin.qq.com/s/Om_1TOGKWkMiNneB6Ittrw)

[iOS 摸鱼周报 #72 | 1024 开始预热](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
