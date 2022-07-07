# iOS 摸鱼周报 #59 | DevOps 再理解 

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：DevOps 再理解
> * 本周学习：OC 类信息解析
> * 内容推荐： WWDC 2022 上推出的新技术（三番）
> * 摸一下鱼：一款跨平台摸鱼神器 Thief，一款用来生成骚话生成器的生成器 sao-gen-gen

## 本期话题

### DevOps 再理解

CI/CD 和 DevOps 有什么区别？如果不能准确回答的话，这篇介绍就值得读一下。文章介绍主要参考于[《软件研发效能提升之美》](https://book.douban.com/subject/35631505/ "软件研发效能提升之美")。

DevOps 是 Development和 Operations 的组合，即开发和运维，再加上保证质量的测试，就构成了完整的 DevOps。

![](https://cdn.zhangferry.com/Images/20220705233157.png)

可以注意到 DevOps 是一个环形结构，它需要同时触达开发、测试、运维三方。DevOps 还可以理解为是敏捷的一种延续，到此可以总结出 DevOps 的目的：拉通职能、快速迭代，以达到提升能效的作用。如何更好的达到这个目的，由此会引出一系列工程实践和技术方案。DevOps 不是具体的开发工具，而是一种软件研发管理模式和思想，是一种文化实践，并不是具体的工具或技术，所有在保证质量的前提下提升效能的方法都属于 DevOps 的范畴。

根据业界主流观点，DevOps 的生命周期可以化为这 7 个阶段：持续开发、持续集成、持续测试、持续监控、持续反馈、持续部署和持续运营。持续开发对应于编码工作，这个阶段需要用到代码仓库、版本控制工具、包管理工具等。持续集成是频繁的提交代码、编译代码、执行单测等，尽可能早的发现问题。持续测试是保证代码的每次提交都能够被及时验证。持续部署是指频繁的把构建出的产品发布到测试环境、生产环境的流程，以尽早接收检验。CI/CD 对应的是持续集成和持续部署，它是 DevOps 生命周期里最重要也是最基本的两个阶段，也可以说它们是 DevOps 概念的实践方式。

DevOps 的 7 个阶段都用到了持续一词，为了实现持续，需要串联开发中的各项任务，由此引出了流水线的概念。流水线是讲究顺序的，任何一个节点出错都会导致任务的失败，这一方面加快了周转速度，也利于尽早暴露问题。像是 Jenkins、GitLab、Github 都会 CI/CD 提供了便捷的流水线配置方案。

DevOps 还常会跟容器技术同时出现，无容积化流程通常是这样的：

![](https://cdn.zhangferry.com/Images/20220706231712.png)

任务量小时这样没问题，但当面对大规模的提交时多场景的提交时，机器的执行效率就显得尤为重要。除了增加机器外，还可以利用容积化技术最大化机器的利用效率。Kubernetes 是一个比较成熟的管理容积化负载均衡、弹性伸缩的服务。

![](https://cdn.zhangferry.com/Images/20220706231848.png)

在 DevOps 之后又演化出了其他开发实践。

* DevSecOps：Sec 表示 Secure，就是将安全防护与 DevOps 结合起来。需要监控 DevOps 各个阶段的安全问题，通常会通过扫描代码、交互式安全扫描、模拟攻击等方式来保证安全性，这些都有对应的开发工具。
* DevPerfOps：Perf 表示 Performance，就是将性能保障与 DevOps 结合起来。需要监控各个阶段的性能指标，开发阶段有：代码静态性能问题、算法时间复杂度、接口级并发测试、性能基线比较等。持续集成阶段有模块级扩缩容测试、压力测试等。持续发布有系统级别的性能基准测试、故障迁移测试、全链路压力测试等。
* BizDevOps：Biz 表示 Business，就是将业务与 DevOps 结合起来。BizDevOps 的概念是将不写代码的业务团队，像是产品和运行也参与进来。它要解决的问题源于[三个不等式](https://developer.aliyun.com/article/839569 "深度 | 从DevOps到BizDevOps, 研发效能提升的系统方法")：局部效率不等于高效交付，高效交付不等于持续高效，高效交付不等于业务成功。为了起到真正助力业务的目标，需要落地产品导向的交付，建设标准化基础设施，不断积累技术资产，同时还需要与业务之间建立快速的反馈闭环。
* AIOps：人工智能 Ops，在原有 DevOps 的各个阶段都融入 AI 能力，通过不断的数据采集和分析，能够根据算法自动的下发执行规则。更进一步，通过自动化测试，不断的分析测试结果，还可以用于异常检测、瓶颈分析、故障预测甚至于故障自愈。

### [Apple 计划推出 Lockdown 模式，保护用户免遭间谍软件侵害](https://www.apple.com.cn/newsroom/2022/07/apple-expands-commitment-to-protect-users-from-mercenary-spyware/ "Apple 计划推出 Lockdown 模式，保护用户免遭间谍软件侵害")

Apple 宣布将发布突破性的安全功能，为可能成为高度针对性网络攻击目标的用户提供特别的额外保护。这些网络攻击来自唯利是图、受国家支持开发间谍软件的私人企业。在 iOS 16、iPadOS 16 和 macOS Ventura 中开启 Lockdown 模式将进一步加强设备防护，严格限制部分功能，大幅减少受攻击面，以免给具高度针对性的间谍软件可乘之机。

## 本周学习

整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)
### OC所使用的类信息存储在哪？ 如何从Macho中找到？

首先我们需要读取到 `__DATA,__objc_classlist` 的信息，存储结构是8个字节指针，读取到对应的指针数据 `data`  

`data` 数据是 `VM Address` 地址，我们需要通过转换拿到对应的 `offset`


* 需要判断是否在对应的 `segmentCommand` 当中

`offset = address - (segmentCommand.vmaddr - segmentCommand.fileoff)`


拿到偏移地址之后，我们就可以根据 `Class64` 的数据结构，在 `machoData` 当中找到对应的数据 `Class` 数据，其中的 `data` 数据才是真正 `Class` 信息的数据

```C++
struct Class64 {
    let isa: UInt64
    let superClass: UInt64
    let cache: UInt64
    let vtable: UInt64
    let data: UInt64
}
```

---

`Class64.data` 数据是 `VM Address` 地址，我们需要通过转换后拿到 `offset` ，在 `machData` 当中找到对应的 `ClassInfo64` 数据，然后其中 `name` 就是对应的 `className`

```C++
struct Class64Info
{
    let flags: Int32 //objc-runtime-new.h line:379~460
    let instanceStart: Int32
    let instanceSize: Int32
    let reserved: Int32
    let instanceVarLayout: UInt64
    let name: UInt64
    let baseMethods: UInt64
    let baseProtocols: UInt64
    let instanceVariables: UInt64
    let weakInstanceVariables: UInt64
    let baseProperties: UInt64
};

```
![](http://cdn.zhangferry.com/Images/20220707210722.png)

如果想要了解具体源码实现，可以通过另一位主编皮拉夫大王的开源项目 [WBBlades](https://github.com/wuba/WBBlades) 学习


## 内容推荐

> 本期内容仍以介绍 WWDC 2022 上推出的新技术为主

1、[Grid 格狀排版](https://youtu.be/N2pXtupyblI "Grid 格狀排版") -- 来自：Jane

[@东坡肘子](https://www.fatbobman.com/)：这个视频会介绍 iOS16 新推出的 Grid —— 网格排版 View 。Grid 是一个十分强大的网格排版工具，极大地改善了 SwiftUI 的版式控制能力。视频会从经典的网格解决方案 GeometryReader 写法讲起，更具体地呈现 Grid 所解决的问题。接着会介绍与 Grid 相关的四个 modifier。

2、[SwiftUI 布局 —— 对齐](https://www.fatbobman.com/posts/layout-alignment/ "SwiftUI 布局 —— 对齐") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：“对齐”是 SwiftUI 中极为重要的概念，然而相当多的开发者并不能很好地驾驭这个布局利器。在 WWDC 2022 中，苹果为 SwiftUI 增添了 Layout 协议，让我们有了更多的机会了解和验证 SwiftUI 的布局原理。本文将结合 Layout 协议的内容对 SwiftUI 的“对齐”进行梳理，希望能让读者对“对齐”有更加清晰地认识和掌握。

3、[Swift Protocol 背后的故事 —— Swift 5.6/5.7](http://zxfcumtcs.github.io/2022/06/30/SwiftProtocol3/ "Swift Protocol 背后的故事 —— Swift 5.6/5.7") -- 来自：雪峰

[@东坡肘子](https://www.fatbobman.com/)：本文是系列文章的第三篇（ 前两篇为 Swift Protocol 背后的故事 —— 实践、Protocol 背后的故事 —— 理论 ），介绍了 Swift 5.6/5.7 在 Protocol 上的相关扩展和优化，主要包括：any、Opaque Parameter、Unlock existentials for all protocols 以及 Primary Associated Types 等内容。

4、[利用 SwiftUI 的新 Charts API 輕鬆建立漂亮的折線圖](https://www.appcoda.com.tw/swiftui-line-charts/ "利用 SwiftUI 的新 Charts API　輕鬆建立漂亮的折線圖") -- 来自：Simon Ng

[@远恒之义](https://github.com/eternaljust)：在 iOS 16 的新版 SwiftUI 中，Apple 重磅更新带来了 Charts 框架。在此之前，我们需要自定义构建图表，或者是依靠第三方库来建立图表。等到现在，我们简单使用 Charts API，就能轻松上手构建折线图。除此之外，开发者还可以更方便地创建动画化和互动的其他图表。

5、[How to Use ShareLink for Sharing Data Like Text and Photos](https://www.appcoda.com/swiftui-sharelink/ "How to Use ShareLink for Sharing Data Like Text and Photos") -- 来自：Simon Ng

[@远恒之义](https://github.com/eternaljust)：当前在 SwiftUI 项目中，我们如果需要调用系统分享数据，必须通过桥接 UIActivityViewController 来实现。在 iOS 16 中，SwiftUI 推出一个名为 ShareLink 的视图控件，当用户点击分享链接时，它会弹出显示系统分享列表，让用户将内容共享到其他应用程序或复制数据以供以后使用。本文将向你展示如何使用 ShareLink 来分享文本、URL 链接和图像等数据。

6、[Implementing a custom native calendar using UICalendarView in iOS16 and Swift](https://ohmyswift.com/blog/2022/06/12/implementing-a-custom-native-calendar-using-uicalendarview-in-ios16-and-swift/ "Implementing a custom native calendar using UICalendarView in iOS16 and Swift") -- 来自：Rizwan Ahmed

[@远恒之义](https://github.com/eternaljust)：以前，面对复杂的日历显示交互需求，我们通常选择第三方日历组件或者自定义日历视图来实现。今年，Apple 引入了原生 UICalendarView，支持在 iOS 16 创建自定义日历视图。本文将介绍如何使用 UICalendarView 来实现自定义原生日历，并支持单选与多选日期。

7、[How to change status bar color in SwiftUI](https://sarunw.com/posts/swiftui-status-bar-color/ "How to change status bar color in SwiftUI") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：在 UIKit 中，我们有很多方法可以[改变状态栏的样式](https://sarunw.com/posts/how-to-set-status-bar-style/ "改变状态栏的样式")。
然而在 SwiftUI 中，我们无法直接更改状态栏样式，需要通过视图修饰符 .preferredColorScheme 来间接修改。这种方式将影响应用程序中的每个视图，相当于手动设置了浅色与深色模式。在 iOS 16 中，我们使用新的修饰符 .toolbarColorScheme 来影响特定导航堆栈上的状态栏，也可以单独在目标视图中再次设置来覆盖此值。

## 摸一下鱼

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

1、[iOS Icon Gallery](https://www.iosicongallery.com/ "iOS Icon Gallery")：一个收录 App Store 上精美的 iOS/macOS/watchOS icon 的网站，可以为作为设计师的你在设计 icon 时提供良好的设计灵感。

![](https://cdn.zhangferry.com/Images/20220707204618.png)

![](https://cdn.zhangferry.com/Images/20220707204501.png)

2、[Thief](https://thief.im/ "Thief")：`Thief` 是一款基于 `Electron`开发的跨平台多功能(`真正创新的`)摸鱼软件，为了上班族打造的`上班必备神器`，使用此软件可以让上班`倍感轻松`，远离 `ICU`。

- **多功能** 不仅仅支持 `小说摸鱼` ，还支持 `股票`、`基金`、`网页`、`视频`、`直播`、`PDF`、`游戏 `等摸鱼模式
- **隐蔽性** 每种摸鱼模式都提供了不同的摸鱼 **技巧**，可以很隐秘地进行摸鱼
- **跨平台** 支持 `Win` + `Mac` + `Linux` , 不管你用什么系统，`Thief` 都让你无缝隙摸鱼

![](https://cdn.zhangferry.com/Images/20220707205920.png)

![](https://cdn.zhangferry.com/Images/20220707210020.png)

3、[Objective-See's Tools](https://objective-see.org/tools.html "Objective-See's Tools")：提供了一系列保护 Mac 的免费、开源的工具。

![](https://cdn.zhangferry.com/Images/20220707211351.png)

4、[sao-gen-gen 骚话生成器生成器](https://github.com/disksing/sao-gen-gen "sao-gen-gen 骚话生成器生成器")：一款用来生成骚话生成器的生成器，你可以通过提交 GitHub Issue 来创建你的生成器！

![](https://cdn.zhangferry.com/Images/20220707212753.png)

![](https://cdn.zhangferry.com/Images/20220707213902.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #58 | 极客风听歌网站，纯文字音乐播放器](https://mp.weixin.qq.com/s/KwqFraJk40f9bEy0eKa8Kw)

[iOS 摸鱼周报 #57 | 周报改版，WWDC22 讲座集锦](https://mp.weixin.qq.com/s/e4ZbFBPqclgy7KyfxVyQZA)

[iOS 摸鱼周报 #56 | WWDC 进行时](https://mp.weixin.qq.com/s/ZyGV6WlFsZOX6Aqgrf1QRQ)

[iOS 摸鱼周报 #55 | WWDC 码上就位](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
