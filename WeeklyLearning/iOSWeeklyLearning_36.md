# iOS摸鱼周报 第三十五期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：Typora 开启收费模式，支持！
> * Tips：混编｜为 Objective-C 添加枚举宏，改善混编体验。
> * 面试模块：事件传递及响应链。
> * 优秀博客：几篇关于 Swift 字符串的优秀博客。
> * 学习资料：独立开发者经验分享。
> * 开发工具：思源笔记，一款本地优先的个人知识管理系统， 支持细粒度块级引用和 Markdown 所见即所得。

## 本期话题

[@zhangferry](https://zhangferry.com)：软件本身做的很好，是很轻巧的MD编辑软件，在这之前我试过很多款，最后还是这个陪我走的最久。软件收费真无可厚非，一般都是付费软件才能提供更优质的服务。软件开发也都是需要挣钱的，更不用说，还是常用且质量很高的软件。

知名 Markdown 编辑软件 Typora ，最近迎来了最新的 1.0 版本（正式版）。这次更新功能上没啥大变化，最大的变化是从之前的免费变为了付费。这个变化在官方 Github 的 [Issus](https://github.com/typora/typora-issues "typora-issue") 里早有说明：

> Typora is a minimal markdown editor, providing new ways for reading and writing markdown. It is currently in beta.
> Typora is commercial software (not open source), but is free during beta. Typora on GitHub supports collaboration between its developer, and its user community, providing a place to transparently report issues, collect feedback and discuss future direction. It also provides open source resources for user customization of themes.

Typora 的口碑一直很好，在各类 Markdown 软件的推荐中基本都是排名首位。我也是 Typora 的重度用户，借助于 Typora 精巧的单栏设置，配合 Orangheart 主题，PicGo 图床插件，可以很方便的输出和排版每篇公众号文章。

面对这次由免费转付费的事情，网上有不少文章都在宣传各种 Typroa 平替方案，却少有人站出来说应该支持开发者，多少有一点让人感觉遗憾。

看下 Typora 的收费标准：89 元（可支付宝）、买断制（终身）、最多三台设备（可以重置）。这相比很多按年续订，动辄上百的产品，价格上算是良心了。

说回付费本身，好的软件就应该是有收益的，有了收益作者能更专注地开发设计产品，更好的产品能给我们带来更多便利，最终还是回馈到用户自身，这是正向循环。单纯为爱发电的事也能持续，但肯定持续不久。所以如果你感觉它好，你喜欢它，那就支持一下吧。


同时我也理解大家并非都是 Typora 重度用户，我找到了收费前的那个版本（v0.11.18）并做了保存，大家如果不小心安装了最新版还想继续白嫖的话可以在公众号后台回复：Typora，下载旧版本。

再来说说 Typora 这个软件吧，其创建于 2014 年，作者 Abner Lee 还是一位国人，为人非常低调，但很有设计天赋。只找到其 2015 年在 Medium 里发的一篇介绍 Typora 设计原由的文章：[Introduce Typora — Why another markdown editor](https://medium.com/@LeeAbner/introduce-typora-why-another-markdown-editor-c86e679828d5 "Introduce Typora — Why another markdown editor") 。其对当时 Markdown 工具的分析可谓句句精准，在 Typora 之前的 Markdown 编辑器都是双栏的，而在这之后越来越多 Markdown 工具尝试单栏的编辑模式。好的产品就是能发现痛点，解决痛点。Abner Lee 一定程度做了不少创新，厉害，确实厉害。

## 开发Tips

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

### 混编｜为 Objective-C 添加枚举宏，改善混编体验

* `NS_ENUM`。用于声明简单枚举，将作为 `enum` 导入到 Swift 中。建议将使用其它方式来声明的 Objective-C 简单枚举进行改造，使用 `NS_ENUM` 来声明，以更好地在 Swift 中使用。
* `NS_CLOSED_ENUM`。用于声明不会变更枚举成员的简单枚举（简称 “冻结枚举” ），例如 NSComparisonResult，将作为 `@frozen enum` 导入到 Swift 中。冻结枚举以降低灵活性的代价，换取了性能上的提升。
* `NS_OPTIONS`。用于声明选项枚举，将作为 `struct` 导入到 Swift 中。
* `NS_TYPED_ENUM`。用于声明类型常量枚举，将作为 `struct` 导入到 Swift 中。可大大改善 Objective-C 类型常量在 Swift 中的使用方式。
* `NS_TYPED_EXTENSIBLE_ENUM`。用于声明可扩展的类型常量枚举。与 `NS_TYPED_ENUM` 的区别是生成的 `struct` 多了一个忽略参数标签的构造器。
* `NS_STRING_ENUM` / `NS_EXTENSIBLE_STRING_ENUM`。用于声明字符串常量枚举，建议弃用，使用 `NS_TYPED_ENUM` / `NS_TYPED_EXTENSIBLE_ENUM` 替代。在 Xcode 13 中，Apple 已经将原先使用 `NS_EXTENSIBLE_STRING_ENUM` 声明的 NSNotificationName 等常量类型改为使用 `NS_TYPED_EXTENSIBLE_ENUM` 来声明。

可以看看：[@师大小海腾：iOS 混编｜为 Objective-C 添加枚举宏，改善混编体验](https://juejin.cn/post/6999460035508043807 "@师大小海腾：iOS 混编｜为 Objective-C 添加枚举宏，改善混编体验")

官方文档：[@Apple：Grouping Related Objective-C Constants](https://developer.apple.com/documentation/swift/objective-c_and_c_code_customization/grouping_related_objective-c_constants "@Apple：Grouping Related Objective-C Constants")

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

### 事件传递及响应链

对于 iOS 的事件传递及响应链，你是否还掌握得不够好，推荐阅读我们编辑 @Mim0sa 和 @CoderStar 的这几篇文章以及 Apple 的文档，相信你一定能在面试中所向披靡。

* [@Mim0sa：iOS | 事件传递及响应链](https://juejin.cn/post/6894518925514997767 "@Mim0sa：iOS | 事件传递及响应链")
* [@Mim0sa：iOS | 响应链及手势识别](https://juejin.cn/post/6905914367171100680 "@Mim0sa：iOS | 响应链及手势识别")
* [@CoderStar：iOS 中的事件响应](https://mp.weixin.qq.com/s/OFwC7Z3iir2wKPJoRpLhFw "@CoderStar：iOS 中的事件响应")
* [@Apple：Event Handling Guide for iOS](https://github.com/zhangferry/iOSWeeklyLearning/blob/main/Resources/Books/Event%20Handling%20Guide%20for%20iOS%20官方文档.pdf "@Apple：Event Handling Guide for iOS")
* [Event Handling Guide for iOS 中文翻译版](https://github.com/zhangferry/iOSWeeklyLearning/blob/main/Resources/Books/Event%20Handling%20Guide%20for%20iOS%20中文翻译版.pdf "Event Handling Guide for iOS 中文翻译版")


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

1、[Swift 字符串性能问题](https://blog.jerrychu.top/2020/11/29/Swift字符串/ "@JerryChu：Swift 字符串性能问题") -- 来自：JerryChu

[@东坡肘子](https://www.fatbobman.com/)：本文的作者在处理一道 LeetCode 算法题时碰到了 Swift 字符串遍历超时的状况，通过分析 Array 同 String 之间遍历机制的不同，最终获得了优化 String 遍历效率的方法。

2、[Swift 的字符串为什么这么难用？](https://juejin.cn/post/6844903962450067469 "@四娘：Swift 的字符串为什么这么难用？") -- 来自掘金：四娘

[@东坡肘子](https://www.fatbobman.com/)：在其它语言里一个语句就能解决的字符串操作在 Swift 中需要多个，但这些其实都是 Swift 有意而为之的设计。本文通过对 SE-0265 Offset-Based Access to Indices, Elements, and Slices 提案的讲解，让开发者了解 Swift 字符串背后的部分设计思路。

3、[WWDC 2021 新 Formatter API：新老比较及如何自定义](https://www.fatbobman.com/posts/newFormatter/ "@东坡肘子：WWDC 2021 新 Formatter API：新老比较及如何自定义") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：在 Swift 中开发者通过使用 Formatter ，可以让很多常用类型的数据都转换成可格式化字符串。在 WWDC 2021 中，苹果推出了使用 Swift 编写的全新 Formatter API。本文通过介绍如何创建符合新 API 的 Formatter，让读者从另一个角度了解新 Formatter API 的设计机制；并对新旧两款 API 进行比较。

4、[Swift 正则表达式完整教程](https://juejin.cn/post/6844903894066151431 "@SunshineBrother：Swift 正则表达式完整教程") -- 来自掘金：SunshineBrother

[@我是熊大](https://github.com/Tliens)：如何在 Swift 中使用正则表达式，本文做了详细描述，操作字符串时应该会用得到。

5、[SwiftString](https://github.com/amayne/SwiftString "GitHub：SwiftString") -- 来自：GitHub

[@我是熊大](https://github.com/Tliens)：SwiftString 是一个轻量级的字符串扩展，功能丰富且强大，GitHub star 1.6k+。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 独立开发者经验分享

**地址**：https://github.com/loonggg/DevMoneySharing

全职独立开发者是一群相对比较自由的开发者，但自由的背后也有赚不到钱、产品没人用的焦虑，在这个仓库中你可以看到很多国内国外的独立开发者赚钱的经验。

## 工具推荐

### 思源笔记

**地址**：https://github.com/siyuan-note/siyuan

**软件状态**：开源、免费

**软件介绍**：

思源笔记是一款本地优先的个人知识管理系统， 支持细粒度块级引用和 Markdown 所见即所得。

![siyuan-note](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/68747470733a2f2f63646e2e6a7364656c6976722e6e65742f67682f73697975616e2d6e6f74652f73697975616e40383438393339373430316366353032356561623834376466623236613466333839366265353336332f73637265656e73686f74732f66656174757265302e706e67.png)


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第三十五期](https://mp.weixin.qq.com/s/fCEbYkAPlK0nm7UtLKFx5A)

[iOS摸鱼周报 第三十四期](https://mp.weixin.qq.com/s/P0HjLDCIM3T-hAgQFjO1mg)

[iOS摸鱼周报 第三十三期](https://mp.weixin.qq.com/s/nznnGmBsqsrWcvZ4XFMttg)

[iOS摸鱼周报 第三十二期](https://mp.weixin.qq.com/s/6CyL0B6Zkf6KXRrfocohoQ)https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
