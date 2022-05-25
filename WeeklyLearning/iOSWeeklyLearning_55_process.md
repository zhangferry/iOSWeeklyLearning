iOS 摸鱼周报 52 | 如何规划个人发展

![](http://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题



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

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #51 | 游戏版号恢复发放](https://mp.weixin.qq.com/s/ogjhELipiVFRaYJkT2NQwA)

[iOS 摸鱼周报 第五十期](https://mp.weixin.qq.com/s/6IS0RlytWxjeRHyh0f2fXA)

[iOS 摸鱼周报 第四十九期](https://mp.weixin.qq.com/s/6GvVh8_CJmsm1dp-CfIRvw)

[iOS摸鱼周报 第四十八期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](http://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
