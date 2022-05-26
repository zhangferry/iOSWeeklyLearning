# iOS 摸鱼周报 55 | WWDC 码上就位

![](http://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：WWDC22 码上就位
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

### [WWDC22 码上就位](https://developer.apple.com/wwdc22/ "WWDC22 码上就位")

![](http://cdn.zhangferry.com/Images/20220526003950.png)

[@zhangferry](zhangferry.com)：WWDC22 已经快到了，Apple 放出了一些开发者大会的活动安排，我们可以根据这些安排了解WWDC 的整个过程。

#### Apple Keynote and Platforms State of the Union

北京时间：6 月 7 号凌晨 1 点和 凌晨 4 点。

这是 WWDC 的开场，介绍 Apple 各平台的新版创新，有时也会公布一些硬件产品。

#### Sessions

北京时间：6 月 8 号至 11 号

这是 WWDC 的核心环节，由 Apple 开发工程师介绍 Apple 全平台最近做的一些升级、创新或者最佳实践。这4天时间里会有 100+ Session 放出。

#### Labs

需要申请，条件是：需要具备开发者会员身份或者是 Swift Student Challenge 的获奖者。

申请开始时间：6月 6 号（美国时区）

是一个跟 Apple 内部员工一对一交流的活动，可以问设计或者开发相关的各种问题，包括一些类似优化、调试等。

#### Digital Lounges

需要注册，条件是：需要具备开发者会员身份或者是 Swift Student Challenge 的获奖者。

注册开始时间：5 月 31号（美国时区）

WWDC 在线休息室也是一个跟 Apple 内部员工交流的活动，相比于 Labs 它对应场景更广泛，会分一些主题开展，像是 WWDC21 就有 SwiftUI、Accessibilty、DevTools 主题。这有一个[网站](https://roblack.github.io/WWDC21Lounges/ "WWDC21 Digital Lounges")还记录了 WWDC21 Digital Lounges 的问答内容。

#### Apple Design Awards

北京时间：6 月 7 号早上 8 点

苹果设计奖表彰那些在包容性、愉悦和乐趣、互动、社会影响、视觉和图形以及创新等方面表现突出的应用程序和游戏。

#### Forums

需要注册：条件是要有 Apple ID

北京时间：6 月 7 号

Forums 是一个更广泛的 Apple 跟开发者之间交流的形式，你可以在这里询问跟 WWDC 22 相关的任何问题。记得把问题标签标记为 WWDC22 或者对应 Session 的主题。

## 面试解析

整理编辑：[JY](https://juejin.cn/user/1574156380931144)



## 优秀博客

> 在 Swift 中有两种特性（ Attributes ），分别用于修饰声明和类型。特性提供了有关声明和类型的更多信息。本期将汇总一些介绍声明特性的文章以帮助大家更好的掌握和使用特性这个强大的工具。

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[@available 与调用方进行沟通](https://mp.weixin.qq.com/s/e2_mWNx4HduM57LF0xTvqA "@available 与调用方进行沟通") -- 来自：OldBirds

[@东坡肘子](https://www.fatbobman.com/)：保持代码不变很难，因为需求不断在变化，系统、框架不断在更新。那么项目实践中，往往会废弃掉一些类或方法。如果是自己独立维护代码，且不需要将代码给他人使用，废弃 API 对你来说是非常简单的，直接改动源码即可。但是对于多人合作的项目，特别是开源的库，废弃一个公开的 API 不是简单地改动下代码就可以，因为你的改动将会影响使用你这个库的所有代码。公开的 API 的更新换代，就相当于你改动了和别人约定的契约一样，这也侧面反映了作者的专业水平。那么如果要废弃一个 API，在 Swift 中我们该如何做？

2、[了解 Swift 中的 @inlinable](https://swiftrocks.com/understanding-inlinable-in-swift.html "了解 Swift 中的 @inlinable") -- 来自：Bruno Rocha

[@东坡肘子](https://www.fatbobman.com/)：@inlinable 特性是 Swift 中较少为人所知的属性之一。和其他同类特性一样，它的目的是启用一组特定的微优化，开发者可以用它来提高应用程序的性能。本文将介绍这个属性是如何工作的，并分析使用它的利弊。

3、[ViewBuilder 研究 —— 掌握 Result builders](https://mp.weixin.qq.com/s/4TwfyhWHVjm3Dv-Vz7MYvg "ViewBuilder 研究 —— 掌握 Result builders") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：结果构造器能按顺序构造一组嵌套的数据结构。利用它，可以以一种自然的声明式语法为嵌套数据结构实现一套领域专门语言（ DSL ），SwiftUI 的声明式特性即来源于此。本文将探讨结果构造器的实现原理，以及如何使用它来创建自己的 DSL 。

4、[@testable 的隐藏成本](https://paul-samuels.com/blog/2021/03/29/thoughts-on-testable-import/ "@testable 的隐藏成本") -- 来自：Paul Samuels

[@东坡肘子](https://www.fatbobman.com/)：在单元测试中，开发者通过为 import 添加 @testable 特性以改变代码的可见性。在需要的时候，这当然是有用的，但它常常被过于急切地使用而没有考虑到可能导致的一些问题。本文将探讨一下使用 @testable 可能导致的一些潜在的设计问题。本文的作者并不是说使用 @testable 是错误的，而是开发者需要为此做的一些设计权衡。

5、[Swift 中的 @objc、@objcMembers 关键字探讨](https://mp.weixin.qq.com/s?__biz=MzkwMDIxNDA3NA==&mid=2247483745&idx=1&sn=8f1db6e0a109754ed73bd3438f64285e&chksm=c0463d34f731b4222e8c238448d19e71f801b25d459b57be673305bcee2ae9cd5aa09a120f01&token=912344454&lang=zh_CN#rd "Swift 中的 @objc、@objcMembers 关键字探讨") -- 来自：剑老师

[@东坡肘子](https://www.fatbobman.com/)：我们说 Objective-c 是一门动态语言，决策会尽可能地推迟到运行时。而 Swit 是一门静态语言，也就是说 Swift 的对象类型、调用的方法都是在编译期就确定的，这也是为什么 Swift 比 oc 性能高的原因。但是在 Swift 中所有继承自 NSObject 的类，仍然保留了 Objective-c 的动态性。如果想要使用它的动态性就需要加上 @objc 关键字，本篇文章就来讲一下，哪些情况需要用到@objc。

6、[为自定义属性包装类型添加类 @Published 的能力](https://mp.weixin.qq.com/s/USGJbLnR-l8Ajgcj8Vb7_A "为自定义属性包装类型添加类 @Published 的能力") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：属性包装器允许你在一个独特的包装器对象中提取通用逻辑。你可以把属性包装器看作是一个额外的层，它定义了一个属性是如何在读取时存储或计算的。它有利于改善 getters 和 setters 中发现重复性代码的几率。本文介绍了 Swift 编译器如何将属性包装类型转译为标准的 Swift 代码，并通过几个实例让读者对属性包装器的用法有更深的了解。

## 见闻

> 这一周阅读/浏览到的有趣的资讯。

1、[谷歌夺回 AI 画语权，机器的想象力达到全新高度，网友：DALL·E 2 诞生一个月就过时了？](https://mp.weixin.qq.com/s/8S5TvFZgRp_N0APKKmrYwA) -- 来自公众号：量子位

[@远恒之义](https://github.com/eternaljust)：前段时间外网爆火的 [Disco Diffusion](https://github.com/alembics/disco-diffusion "Disco Diffusion Github 地址") AI 画画刷屏出圈，DALL·E 2 也紧随其后，不到六周的时间，谷歌立马派出 [Imagen](https://imagen.research.google/ "谷歌 Imagen") 来强势应战。谷歌 Imagen 的创作提升，在于使用自家纯语言模型 T5-XXL 负责编码文本特征，把文本到图像转换的工作丢给了图像生成模型。同时扩大语言模型的规模，优化扩算模型，增加无分类器引导，每一步采样时使用动态阈值，防止图像过饱和。使用高引导权重的同时在低分辨率图像上增加噪声。新的 Efficient U-Net 结构改进，改善了内存使用效率、收敛速度和推理时间。对此，网友们调侃道：以后可能没图库网站什么事儿了。

2、[人体系统调优不完全指南](https://github.com/zijie0/HumanSystemOptimization "人体系统调优不完全指南") -- 来自 Github: zijie0

[@远恒之义](https://github.com/eternaljust)：之前有推荐过[程序员延寿指南](https://github.com/geekan/HowToLiveLonger "程序员延寿指南")，延寿的关键在于降低 ACM: All-Cause Mortality / 全因死亡率。最近又在 V2EX 上刷到类似的话题：[不可不看的程序员续命科技](https://www.v2ex.com/t/855113 "V 站原帖：不可不看的程序员续命科技")，作者提出通过调优人体系统来延长寿命。对于程序员来说，降低全因死亡率就好比降低软件程序 bug 奔溃率，只要解决了项目中的疑难杂症，奔溃减少了，系统自然就能长期稳定运行。我们通过学习了解自身的人体系统（类比计算机组成原理），从机体工作原理出发，像调优软件程序那样来“调优”自身的人体系统，这也是一个不错的延寿方案。如果能把两者结合起来，相辅相成，那么长寿指日可待。

3、[Beautify Github Profile](https://github.com/rzashakeri/beautify-github-profile) -- 来自 Github

![](http://cdn.zhangferry.com/Images/20220525231909.png)

[@zhangferry](zhangferry.com)：Github 自定义 Profile 是一个很棒的功能，我们可以用它定制自己的个人介绍页面。它的使用非常简单，建一个跟用户名同名的仓库，该仓库的 README.md 即是 Profile 的展示页面。Github 有很多做的很漂亮的样式都有对应的开源配置链接，该仓库对这类配置进行了收录整理。

4、[我的移动开发程序人生：写在创业十周年](https://blog.devtang.com/2022/05/22/startup-10th-year-summary/ "我的移动开发程序人生：写在创业十周年") -- 来自唐巧的博客

[@zhangferry](zhangferry.com)：巧哥是国内 iOS 圈最著名的开发者之一，这篇文章是对他移动开发程序人生的总结。我发现很多非常优秀的开发者都是有着一个跟计算机紧密联系的童年，他们一个偶然的机会接触到计算机，被这个神奇的机器所吸引，然后寻找当下可以获取的所有资料去探索它，最终从事计算机行业，凭借时代红利和个人努力，最终成长为某一领域的翘楚。这一切的起点都来源于热爱，有了那股一心钻研去满足好奇心的劲，才将这份热爱开花结果。

5、[移动应用出海趋势洞察白皮书](https://report.iresearch.cn/report_pdf.aspx?id=3999) -- 来自艾瑞网

[@zhangferry](zhangferry.com)：2022 年移动应用出海趋势愈发明显，那出海的环境怎么样，机会还有多大呢？艾瑞网的这份白皮书正是基于这个背景下产出的。根据对仅百位移动开发者的调研，得出以下观点：

* 国内移动应用多个领域增长放缓，部分分类已到天花板。海外市场仅2021年网民数量扩展了6亿，中东、拉美渗透率增长较快。
* 隐私安全、数据保护在国外的重视程度趋严，应用合规性需要给予重视。
* 游戏类和娱乐类应用收入增长强劲。非游戏类视频&照片类应用更吸引全球用户。
* 由于印度 App 的封禁措施，东南亚取而代之成为下载量最多的区域，非洲下载增速最明显。北美、日韩、欧洲仍是收入主要来源地。
* 出海遇到的困难有对海外市场的陌生感、本地化难开展、推广困难、海外政策不熟悉等。针对这些问题华为提供了一些解决方案，[AppTouch](https://developer.huawei.com/consumer/cn/AppTouch "AppTouch") 和 [AppGallery Connect](https://developer.huawei.com/consumer/cn/service/josp/agc/index.html#/ "AppGallery Conenct")，他们可以在本地化、投放、运营和技术等多方面提供出海支持。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### TypeScript 入门教程

**地址**：https://ts.xcatliu.com/

这是一份 TypeScript 的入门教程，与官方手册不同，这份 TypeScript 入门教程着重于从 JavaScript 程序员的角度总结思考，循序渐进的理解 TypeScript，示例丰富，比官方文档更易读。同时作者也指出，本书比较适合已经熟悉 JavaScript 的开发者，不适合没有学习过 JavaScript 的人群。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #54 | Apple 辅助功能持续创新](https://mp.weixin.qq.com/s/6jdqa143Y5yr6lbjCuzlqA)

[iOS 摸鱼周报 #53 | 远程办公正在成为趋势](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

[iOS 摸鱼周报 #52 | 如何规划个人发展](https://mp.weixin.qq.com/s/45ftt4AC2C5Ts8Zt3sWvJA)

[iOS 摸鱼周报 #51 | 游戏版号恢复发放](https://mp.weixin.qq.com/s/ogjhELipiVFRaYJkT2NQwA)

[iOS 摸鱼周报 第五十期](https://mp.weixin.qq.com/s/6IS0RlytWxjeRHyh0f2fXA)

![](http://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
