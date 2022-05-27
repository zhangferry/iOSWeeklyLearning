# iOS 摸鱼周报 #55 | WWDC 码上就位

![](http://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：WWDC22 码上就位
> * 面试模块：iOS WebView 中的 User-Agent
> * 优秀博客：Swift 中修饰声明和类型的两种特性
> * 学习资料：TypeScript 入门教程
> * 开发工具：一款适用于 mac 的简洁日历软件 itsycal 

## 本期话题

### [WWDC22 码上就位](https://developer.apple.com/wwdc22/ "WWDC22 码上就位")

![](http://cdn.zhangferry.com/Images/20220526003950.png)

[@zhangferry](zhangferry.com)：WWDC22 已经快到了，Apple 放出了一些开发者大会的活动安排，我们可以根据这些安排了解 WWDC 的整个过程。

#### Apple Keynote and Platforms State of the Union

北京时间：6 月 7 号凌晨 1 点和 凌晨 4 点。

这是 WWDC 的开场，介绍 Apple 各平台的新版创新，有时也会公布一些硬件产品。

#### Sessions

北京时间：6 月 8 号至 11 号

这是 WWDC 的核心环节，由 Apple 开发工程师介绍 Apple 全平台最近做的一些升级、创新或者最佳实践。这 4 天时间里会有 100+ Session 放出。

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

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### iOS WebView 中的 User-Agent

User-Agent 中文名为用户代理，简称 UA（后文中的 User-Agent 统一用 UA 表示），它是一个特殊的字符串头，内容涵盖客户端的操作系统类型及版本、CPU 类型、浏览器及版本、浏览器语言等；`WebView` 会在每个 URL 请求头中携带该信息。

UA 在项目中的常见应用：

1. 区分访问客户端是移动端还是 PC，如果是移动端还可以区分是 iOS 或者 Android。
2. 收集有关访问者的统计信息，例如渠道信息等。
3. 传递一些基础数据，例如站点、协议版本号、app 名称等等和业务相关的基础信息。

#### UA 字符串格式 

**UA 字符串格式：**Mozilla/[version] ([system and browser information]) [platform] ([platform details]) [extensions]

由于浏览器厂商的历史兼容性问题，很多字段值都没有严格按照格式排布，有些字段值和最初的定义也不具有对应价值。各部分描述参考如下：

- Mozilla/[version]：设计目的是描述浏览器名称以及版本，但是由于浏览器兼容性问题，已经没有实际意义，一般值为 `"Mozilla/5.0"`。
- ([system and browser information])：CPU 操作系统以及浏览器信息，值是以 `;`分割的。例如 `"Macintosh; Intel Mac OS X 10_13_6"` Macintosh 指的是 Mac 平台、CPU 类型是 intel、 操作系统为 10.13.6 MacOS。
- [platform]： 浏览器渲染引擎，chrome/safari浏览器的值一般为 `"AppleWebKit/xxx"` 表示内核为`webkit/blink`。
- ([platform details])： 浏览器渲染其他补充信息，同样由于兼容性问题，值不具有代表意义，例如 iOS 上是 `(KHTML, like Gecko)`
- [extensions]：扩展字段，主要描述了浏览器信息以及自定义字段，自定义字段是 key/value 形式，例如 `protocol/1.0.0` 传递协议版本等内容。扩展字段中一些字段描述：
    - Chrome：Chrome/版本号
    - Safari：Safari/版本号 （chrome 浏览器后面也会带 Safari 字段）
    - Version：Version/版本号
    - Mobile：移动设备标识，一般指内部版本号，苹果设备会带版本号，安卓设备不含版本号

iPhone 上的示例格式如下:

```cpp
Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X)  AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148
```

其他数据值类型参考[解析Navigator.userAgent的迷惑行为](https://juejin.cn/post/6908647211945590791 "解析Navigator.userAgent的迷惑行为")

#### 获取系统的 UA

iOS 获取 UA 的方式是相似的，都是直接调用 js  查询 `navigator.userAgent`；区别在于执行 js 的 api 不同。iOS 已经淘汰了 `UIWebView` 所以这里只做对比了解就可以。

```objectivec
// UIWebView
UIWebView *webView = [[UIWebView alloc] initWithFrame:CGRectZero];
self.userAgent = [webView stringByEvaluatingJavaScriptFromString:@"navigator.userAgent"] ?:@"";

// WkWebView
WKWebViewConfiguration *config = [[WKWebViewConfiguration alloc] init];
if (@available(iOS 13.0, *)) {
   config.defaultWebpagePreferences.preferredContentMode = WKContentModeMobile;
}
WKWebView *webView = [[WKWebView alloc] initWithFrame:CGRectZero configuration:config];
[webView evaluateJavaScript:@"navigator.userAgent" completionHandler:^(id _Nullable response, NSError *_Nullable error) {
        self.userAgent = (NSString *)response;
}];
```

`UIWebView` 是同步方式， `WKWebView` 是异步方式，所以要注意如果是使用 `WKWebView`，确保 user-agent 已经设置完成后再创建 web 页面，否则会造成自定义信息的丢失。

#### 修改 UA

一般场景因为业务需求，经常需要在 UA 里添加自定义值，有三种方式来修改默认的 UA 值。

1. 修改系统 UA，程序一旦杀死更改的 UA 也会随即失效，如果希望保持更改 UA，则需要在每次应用启动时重新更改系统User-Agent。修改后使用 `NSUserDefaults` 进行缓存，APP 内所有的 H5 页面共享使用。

```objectivec
- (void)updateSystemUserAgent:(NSString *)userAgent {
    [[NSUserDefaults standardUserDefaults] registerDefaults:@{@"UserAgent":userAgent}];
    [[NSUserDefaults standardUserDefaults] synchronize];
}
```

2. iOS 12支持修改局部的 UA，此时 UA 仅在当前的 `WebView`的生命周期内生效，随着 `WebView` 销毁，更改的 UA 信息就会随机失效。作用域是针对 `WebView` 实例的。

```objectivec
- (void)updateCustomUserAgent:(NSString *)userAgent {
    [self.wkWebView setCustomUserAgent:userAgent];
}
```


3. 通过 `applicationNameForUserAgent` 设置，该方式非直接覆盖，而是将设置的值追加到默认值的后面。也是仅针对当前 config 生效的。

```objectivec
let config = WKWebViewConfiguration()
config.applicationNameForUserAgent = "Custom User Agent"
let webview = WKWebView(frame: .zero, configuration: config)
    
// 修改后的UA 值为：`Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Custom UserAgent`。
```

`applicationNameForUserAgent`在客户端获取默认值仅有 `Mobile/16A404`，实际上 web 页面获取到的是完整的值。

> **三种方式的优先级：**`customUserAgent > UserDefault > applicationNameForUserAgent`

#### 注意事项

1. `WKWebView` 获取系统 UA 为异步方式，如果需要多次设置 UA，则需要依次进行，否则会造成覆盖问题。

2. 修改自定义 UA，需要在创建加载页面的 `WKWebView` 前设置好。所以一般情况是在 `AppDelegate中`使用临时对象调用 `evaluateJavaScript:@"navigator.userAgent"`，否则会造成加载页面的 `WKWebView`首次使用 UA 失效。需要重新 reload webview 才生效。

3. 由于第一种经常造成莫名失效问题， 建议使用 2、3 设置方式。

- [iOS - User Agent 的应用和设置](https://www.cnblogs.com/lxlx1798/p/10819610.html "iOS - User Agent 的应用和设置")
- [WKWebView 设置自定义UserAgent正确姿势](https://juejin.cn/post/6844903632152821773 "WKWebView 设置自定义UserAgent正确姿势")
- [记使用WKWebView修改user-agent在iOS 12踩的一个坑](https://cloud.tencent.com/developer/article/1158832 "记使用WKWebView修改user-agent在iOS 12踩的一个坑")

## 优秀博客

> 在 Swift 中有两种特性（ Attributes ），分别用于修饰声明和类型。特性提供了有关声明和类型的更多信息。本期将汇总一些介绍声明特性的文章以帮助大家更好的掌握和使用特性这个强大的工具。

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[@available 与调用方进行沟通](https://mp.weixin.qq.com/s/e2_mWNx4HduM57LF0xTvqA) -- 来自：OldBirds

[@东坡肘子](https://www.fatbobman.com/)：保持代码不变很难，因为需求不断在变化，系统、框架不断在更新。那么项目实践中，往往会废弃掉一些类或方法。如果是自己独立维护代码，且不需要将代码给他人使用，废弃 API 对你来说是非常简单的，直接改动源码即可。但是对于多人合作的项目，特别是开源的库，废弃一个公开的 API 不是简单地改动下代码就可以，因为你的改动将会影响使用你这个库的所有代码。公开的 API 的更新换代，就相当于你改动了和别人约定的契约一样，这也侧面反映了作者的专业水平。那么如果要废弃一个 API，在 Swift 中我们该如何做？

2、[了解 Swift 中的 @inlinable](https://swiftrocks.com/understanding-inlinable-in-swift.html "了解 Swift 中的 @inlinable") -- 来自：Bruno Rocha

[@东坡肘子](https://www.fatbobman.com/)：@inlinable 特性是 Swift 中较少为人所知的属性之一。和其他同类特性一样，它的目的是启用一组特定的微优化，开发者可以用它来提高应用程序的性能。本文将介绍这个属性是如何工作的，并分析使用它的利弊。

3、[ViewBuilder 研究 —— 掌握 Result builders](https://mp.weixin.qq.com/s/4TwfyhWHVjm3Dv-Vz7MYvg) -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：结果构造器能按顺序构造一组嵌套的数据结构。利用它，可以以一种自然的声明式语法为嵌套数据结构实现一套领域专门语言（ DSL ），SwiftUI 的声明式特性即来源于此。本文将探讨结果构造器的实现原理，以及如何使用它来创建自己的 DSL 。

4、[@testable 的隐藏成本](https://paul-samuels.com/blog/2021/03/29/thoughts-on-testable-import/ "@testable 的隐藏成本") -- 来自：Paul Samuels

[@东坡肘子](https://www.fatbobman.com/)：在单元测试中，开发者通过为 import 添加 @testable 特性以改变代码的可见性。在需要的时候，这当然是有用的，但它常常被过于急切地使用而没有考虑到可能导致的一些问题。本文将探讨一下使用 @testable 可能导致的一些潜在的设计问题。本文的作者并不是说使用 @testable 是错误的，而是开发者需要为此做的一些设计权衡。

5、[Swift 中的 @objc、@objcMembers 关键字探讨](https://mp.weixin.qq.com/s?__biz=MzkwMDIxNDA3NA==&mid=2247483745&idx=1&sn=8f1db6e0a109754ed73bd3438f64285e&chksm=c0463d34f731b4222e8c238448d19e71f801b25d459b57be673305bcee2ae9cd5aa09a120f01&token=912344454&lang=zh_CN#rd) -- 来自：剑老师

[@东坡肘子](https://www.fatbobman.com/)：我们说 Objective-C 是一门动态语言，决策会尽可能地推迟到运行时。而 Swit 是一门静态语言，也就是说 Swift 的对象类型、调用的方法都是在编译期就确定的，这也是为什么 Swift 比 OC 性能高的原因。但是在 Swift 中所有继承自 NSObject 的类，仍然保留了 Objective-C 的动态性。如果想要使用它的动态性就需要加上 @objc 关键字，本篇文章就来讲一下，哪些情况需要用到 @objc。

6、[为自定义属性包装类型添加类 @Published 的能力](https://mp.weixin.qq.com/s/USGJbLnR-l8Ajgcj8Vb7_A) -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：属性包装器允许你在一个独特的包装器对象中提取通用逻辑。你可以把属性包装器看作是一个额外的层，它定义了一个属性是如何在读取时存储或计算的。它有利于改善 getters 和 setters 中发现重复性代码的几率。本文介绍了 Swift 编译器如何将属性包装类型转译为标准的 Swift 代码，并通过几个实例让读者对属性包装器的用法有更深的了解。

## 见闻

> 这一周阅读/浏览到的有趣的资讯。

1、[谷歌夺回 AI 画语权，机器的想象力达到全新高度，网友：DALL·E 2 诞生一个月就过时了？](https://mp.weixin.qq.com/s/8S5TvFZgRp_N0APKKmrYwA) -- 来自公众号：量子位

[@远恒之义](https://github.com/eternaljust)：前段时间外网爆火的 [Disco Diffusion](https://github.com/alembics/disco-diffusion "Disco Diffusion Github 地址") AI 画画刷屏出圈，DALL·E 2 也紧随其后，不到六周的时间，谷歌立马派出 [Imagen](https://imagen.research.google/ "谷歌 Imagen") 来强势应战。谷歌 Imagen 的创作提升，在于使用自家纯语言模型 T5-XXL 负责编码文本特征，把文本到图像转换的工作丢给了图像生成模型。同时扩大语言模型的规模，优化扩算模型，增加无分类器引导，每一步采样时使用动态阈值，防止图像过饱和。使用高引导权重的同时在低分辨率图像上增加噪声。新的 Efficient U-Net 结构改进，改善了内存使用效率、收敛速度和推理时间。对此，网友们调侃道：以后可能没图库网站什么事儿了。

2、[人体系统调优不完全指南](https://github.com/zijie0/HumanSystemOptimization "人体系统调优不完全指南") -- 来自 Github: zijie0

[@远恒之义](https://github.com/eternaljust)：之前有推荐过[程序员延寿指南](https://github.com/geekan/HowToLiveLonger "程序员延寿指南")，延寿的关键在于降低 ACM: All-Cause Mortality / 全因死亡率。最近又在 V2EX 上刷到类似的话题：[不可不看的程序员续命科技](https://www.v2ex.com/t/855113 "V 站原帖：不可不看的程序员续命科技")，作者提出通过调优人体系统来延长寿命。对于程序员来说，降低全因死亡率就好比降低软件程序 bug 奔溃率，只要解决了项目中的疑难杂症，奔溃减少了，系统自然就能长期稳定运行。我们通过学习了解自身的人体系统（类比计算机组成原理），从机体工作原理出发，像调优软件程序那样来“调优”自身的人体系统，这也是一个不错的延寿方案。如果能把两者结合起来，相辅相成，那么长寿指日可待。

3、[Beautify Github Profile](https://github.com/rzashakeri/beautify-github-profile "Beautify Github Profile") -- 来自 Github

![](http://cdn.zhangferry.com/Images/20220525231909.png)

[@zhangferry](zhangferry.com)：Github 自定义 Profile 是一个很棒的功能，我们可以用它定制自己的个人介绍页面。它的使用非常简单，建一个跟用户名同名的仓库，该仓库的 README.md 即是 Profile 的展示页面。Github 有很多做的很漂亮的样式都有对应的开源配置链接，该仓库对这类配置进行了收录整理。

4、[我的移动开发程序人生：写在创业十周年](https://blog.devtang.com/2022/05/22/startup-10th-year-summary/ "我的移动开发程序人生：写在创业十周年") -- 来自唐巧的博客

[@zhangferry](zhangferry.com)：巧哥是国内 iOS 圈最著名的开发者之一，这篇文章是对他移动开发程序人生的总结。我发现很多非常优秀的开发者都是有着一个跟计算机紧密联系的童年，他们一个偶然的机会接触到计算机，被这个神奇的机器所吸引，然后寻找当下可以获取的所有资料去探索它，最终从事计算机行业，凭借时代红利和个人努力，最终成长为某一领域的翘楚。这一切的起点都来源于热爱，有了那股一心钻研去满足好奇心的劲，才将这份热爱开花结果。

5、[移动应用出海趋势洞察白皮书](https://report.iresearch.cn/report_pdf.aspx?id=3999 "移动应用出海趋势洞察白皮书") -- 来自艾瑞网

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

### itsycal

**地址**：https://www.mowglii.com/itsycal/

**软件状态**：免费

**软件介绍**：

一款简洁的适用于`mac`的日历软件。

![itsycal](http://cdn.zhangferry.com/20220526142405.png)


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #54 | Apple 辅助功能持续创新](https://mp.weixin.qq.com/s/6jdqa143Y5yr6lbjCuzlqA)

[iOS 摸鱼周报 #53 | 远程办公正在成为趋势](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

[iOS 摸鱼周报 #52 | 如何规划个人发展](https://mp.weixin.qq.com/s/45ftt4AC2C5Ts8Zt3sWvJA)

[iOS 摸鱼周报 #51 | 游戏版号恢复发放](https://mp.weixin.qq.com/s/ogjhELipiVFRaYJkT2NQwA)

![](http://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
