# iOS 摸鱼周报 #97 | 智源大会线下参会体验

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：智源大会线下参会体验
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### 智源大会线下参会体验

![](https://cdn.zhangferry.com/Images/202306160815108.png)

北京智源大会是智源研究院主办的国际性人工智能高端专业交流活动，定位于"AI内行顶级省会"。看本期的参会人员，都是 AI 领域最顶级的大佬，我其实是被 Sam Altman 吸引的。结果现场并没有见到本人，只有视频连线。连线那一刻现场氛围一下热腾起来了，Sam Altman 的明星属性真的太强了。虽然我是 AI 小白去凑热闹，也涨了不少见识。

![](https://cdn.zhangferry.com/Images/202306160810986.png)

大会所有视频内容已同步到 B 站官号 [2023北京智源大会](https://www.bilibili.com/video/BV1PN411C7JX "2023北京智源大会")。会议涉及主题非常多，强化学习、多模态大模型、AI 开源、AI 系统、认知神经科学大模型、AI 安全 等等。简单说一下参会那天的几点感受：

* 会议学术性非常强，既有研究成果展示，也有具体技术方案的讨论
* AI 领域不只有大模型，像 AI 编译器、AI 芯片、模型优化、模型评估等有非常多研究方向
* 国内在 AI 领域的投入和产出都很高，不能只通过大模型的差距，来衡量 AI 领域整体的差异。很多 AI 环节涉及的关键技术，都有国内的替代产品。
* AI 领域的发力很多都在走开源路线，借助于社区的贡献和检验来完成 AI 产品本身
* 从事 AI 底层研究的主要还集中在这些研究机构和高校上，科技公司对于底层研究的投入还可以再多一点

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

苹果在 WWDC 2023 上发布了许多新产品与新技术，本期将推荐几篇相关博客文章。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[WWDC 23 新增的系统框架](https://juejin.cn/post/7243352406132981797 "WWDC 23 新增的系统框架") -- 作者：ZacJi

[@东坡肘子](https://www.fatbobman.com/): 每年的 WWDC 都会发布新的系统，其中包括新功能和之前未向开发者开放的功能。为了支持这些特性，新的系统框架通常也会随之发布。这使得开发者能够方便地使用新系统的特性来开发应用程序。在本文中，作者将介绍 WWDC 23 中新增的系统框架，并分享自己的看法。

2、[Metal for SwiftUI](https://alexanderlogan.co.uk/blog/wwdc23/09-metal "Metal for SwiftUI") -- 作者：Alex

[@东坡肘子](https://www.fatbobman.com/): 在本届 WWDC 上，SwiftUI 获得了很多新的 API，其中就包括可以直接在视图中使用 Shader（着色器）的能力。本文介绍了在 SwiftUI 中使用着色器的方法，涵盖了三种类型的效果：颜色效果、图层效果和扭曲效果。对于每种效果，都提供了示例，包括渐变效果、像素翻转效果和圆形加载器效果。

3、[使用 Swift 宏自动适配 RawRepresentable 协议](https://otbivnoe.ru/2023/06/13/Automating-RawRepresentable-Conformance-with-Swift-Macros.html "使用 Swift 宏自动适配 RawRepresentable 协议") -- 作者：Nikita Ermolenko

[@东坡肘子](https://www.fatbobman.com/): 宏是 Swift 5.9 版本中推出的最重要的新特性之一。WWDC 上很多新的 API 都是基于宏来实现的。本文将通过创建一个自动为枚举类型添加 RawRepresentable 协议的宏，来介绍自定义宏的方法。通过使用宏，可以使我们的代码更加优雅、简洁和可维护，让开发者能够专注于应用程序的核心逻辑。

4、[深入了解 SwiftUI 5 中 ScrollView 的新功能](https://www.fatbobman.com/posts/new-features-of-ScrollView-in-SwiftUI5/ "深入了解 SwiftUI 5 中 ScrollView 的新功能") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 在 SwiftUI 5.0 中，苹果大幅强化了 ScrollView 功能。新增了大量新颖、设计精巧的 API。包括：contentMargins、safeAreaPadding、scrollIndicatorsFlash、scrollClipDisable、scrollTargetLayout、scrollPosition、scrollTargetBehavior、scrollTransition 等。本文将对这些新功能进行介绍。

5、[WWDC2023 Session系列：探索 XCode15 新特性](https://juejin.cn/post/7244561312709558330 "WWDC2023 Session系列：探索 XCode15 新特性") -- 作者：京东云技术团队

[@东坡肘子](https://www.fatbobman.com/): 像往年一样，苹果在 WWDC 2023 上推出了全新的 Xcode 15。在本文中，京东云技术团队将逐一介绍 Xcode 15 引入的新功能。包括更简洁的宏、文档和日志功能，使开发者能够更高效地编写和维护代码。更智能的自动补全和测试分析功能大大提高了开发效率。更方便的包管理功能通过拆分下载和 Git 集成简化了开发流程。此外，Xcode 15 还增强了图片资产和框架的安全性管理，为应用提供更高级的安全保障。这些新功能为开发者带来了更高效、更方便和更安全的开发体验。



## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[OpenAI API 模型更新](https://openai.com/blog/function-calling-and-other-api-updates)：本次更新主要有这几点：

* 支持函数调用。它的目的是增加模型的灵活度，扩展模型的能力。以「获取 Boston 的天气」这个对话为例，先输入问题和需要的函数及参数类型，调用 `chat/completions` 的接口，这一步获取 Boston 这个地理信息。此时没结束，因为 OpenAI 的模型并不知道实时的天气信息。我们拿到提取的地理信息，请求天气 API 获取实时天气，把实时天气信息，作为函数参数拼接进 role 对应的内容，再调一次 `chat/completions`，就可以完成了整个流程了。这个能力可以突破模型本身的限制，它的能力非常强大，这样各类 AI 插件又有更多新玩法了。支持模型为：`gpt-4-0613`和 `gpt-3.5-turbo-0613`。
* gpt-3.5-turbo 发布了一个支持 16k tokens 的模型：`gpt-3.5-turbo-16k`，3.5-trubo支持的 tokens 数只有 4k。这里的 token 数是把 prompt 和 回复内容一起计算的。
* 因为系统层面的优化，`text-embedding-ada-002`价格下调 75%，`gpt-3.5-turbo` 下调 25%。

我把 [SummarAI](https://github.com/zhangferry/SummarAI "SummarAI") 可用的模型也同步扩展了 `gpt-3.5-turbo-16k`，用一篇长文进行分析，发现这个模型识别效果比 3.5-turbo 更好些，而且输出的回复也非常长。之前用 3.5-turbo 经常超过 600 个字符的回复就自动截断了。用 16k 这个模型测试对 OpenAI 这篇文章的总结回复长达 2500 个字符，非常夸张。

2、[API2D](https://api2d.com/r/187046 "API2D")：很多基于 AI 的开发工具，都需要提供 API Key 才能使用。但 OpenAI 的 API Key 一是充值麻烦，二是接口被墙无法直接访问。针对这类痛点催生了一批针对国内用户的 API Key 服务，它们即提供便利的充值，也代理了接口国内可以直接访问，API2D 就是这样一个产品。付费方式是按照 Token 数算的，价格上是官方的 1.5 倍。点数的好处是适用于个人，不会出现价格高，自己用不完，找人拼车的问题。而且它还支持 GPT-4 的调用。支持这些接口：

![](https://cdn.zhangferry.com/Images/202306160021450.png)

3、[《Design for spatial user interfaces》 总结](https://twitter.com/zuozizhen/status/1669313088674496514 "《Design for spatial user interfaces》 总结")：来自于博主 [@左子帧](https://twitter.com/zuozizhen) 对于 [Design for spatial user interfaces](https://developer.apple.com/videos/play/wwdc2023/10076/ "Design for spatial user interfaces") 这期 Session 的总结，可以注意到很多 visonOS 设计上的细节，苹果真的是设计怪，以下是其中几点：

* 在 visionOS 中设计 App 图标时，图标最多可以分为三层（一个背景层 + 两个前景层），每一层尺寸都是 1024*1024px，当使用时系统会自动再加一层玻璃层，给图标增加深度、高光和阴影效果，这样就可以产生官方视频中图标微妙的纵深感
* visionOS 中的窗口主题使用了新设计的玻璃材质，同时系统会自动在边缘处通过高光阴影（环境光的反射）来体现在空间中的位置
* visionOS 中没有明确的亮色和暗色模式，但系统会自动感应环境光线来调整窗口颜色对比度，让内容保证始终可见
* 强调色不要直接应用在前景元素上，同时尽量使用系统颜色（因为系统颜色可以跟随环境光动态适应调整）
* 左右转头要比上下转头更容易，所有不要把东西放太高或太低，界面也要往两边延伸而不是上下延伸
* 系统控件会自带焦点反馈效果（类比桌面端的 Hover 效果，在 visionOS 就是眼睛注视到控件时的效果 ）
* 在 visionOS 中弹出菜单不需要箭头，系统按钮会在选中时显示白色背景，所以需要注意的是尽量也不要设计白色背景的按钮，否则会和系统按钮的选中态混淆

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
