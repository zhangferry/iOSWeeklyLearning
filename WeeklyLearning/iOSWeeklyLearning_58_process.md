# iOS 摸鱼周报 #58 | 极客风听歌网站，纯文字音乐播放器

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：在您的 App 中提供帐户删除选项
> * 本周学习：如何配置合适的 ATS
> * 内容推荐：WWDC22 推出的新技术和新内容（二番）
> * 摸一下鱼：开启真·摸鱼模式，在线养金鱼；极客风的听歌网站，纯文字的音乐播放器。
## 本期话题

### [在您的 App 中提供帐户删除选项](https://developer.apple.com/cn/support/offering-account-deletion-in-your-app "在您的 App 中提供帐户删除选项")

[@远恒之义](https://github.com/eternaljust)：苹果要求，自 2022 年 6 月 30 日起，如果您的 App 支持帐户创建，提交到 App Store 审核，必须支持用户在 App 中发起帐户删除，以避免审核延迟。

⚠️ 注意事项：
* 支持“通过 Apple 登录”的 App 应使用 Sign in with Apple REST API 来[撤销用户令牌](https://www.yuque.com/eternaljust/rpmt31/bxmc3d#khpAl "撤销用户令牌")。
* 如果 App 帐户删除流程是手动的（如在应用内申请删除账号，需要管理员后台审核），请告知用户删除帐户需要多长时间，并在删除完成时提供一条确认信息。
* 如何避免拥有自动续期订阅的用户在删除帐户后意外被 Apple 继续扣款？可提供[链接](https://apps.apple.com/account/subscriptions "打开用户管理订阅链接")来让用户管理取消自己的订阅。

## 本周学习

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) 
### 如何配置合适的 ATS（App Transport Security）配置

为了增强应用与网络交互的安全，从 **iOS 9** 开始，苹果开启了称为应用传输安全 (ATS) 的网络功能用于提高所有应用和应用扩展的隐私和数据完整性。

**ATS 会阻止不符合最低安全规范的连接**

![Apps-Transport-Security~dark@2x](http://cdn.zhangferry.com/Images/Apps-Transport-Security_dark@2x.png)

<center> 图片来源于开发者官网</center>

#### 为什么需要进行 ATS 配置

ATS 为我们的应用安全增加了保护，但是由于某些原因，我们不得不需要某些手段来*规避* ATS 规则

在 `info.plist` 中提供了 ATS 配置信息允许用户自定义规则

**最新完整**的 ATS 配置键值如下：

```
NSAppTransportSecurity : Dictionary {
    NSAllowsArbitraryLoads : Boolean
    NSAllowsArbitraryLoadsForMedia : Boolean
    NSAllowsArbitraryLoadsInWebContent : Boolean
    NSAllowsLocalNetworking : Boolean
    NSExceptionDomains : Dictionary {
    	<domain-name-string> : Dictionary {
      	  NSIncludesSubdomains : Boolean
        	NSExceptionAllowsInsecureHTTPLoads : Boolean
        	NSExceptionMinimumTLSVersion : String
        	NSExceptionRequiresForwardSecrecy : Boolean
    	}
		}
}
```
> 如果你现有的ATS 配置存在冗余的键值，证明其已被摒弃。你可以查看[Document Revision History](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/RevisionHistory.html#//apple_ref/doc/uid/TP40016535-SW1 "Document Revision History") 明确相关键值的信息 

#### 如何挑选合适的 ATS 配置

但是由于各种键值的组合分类繁杂，为了确保连通性，我们需要一个简单的方法，来寻找到我们最适合的 ATS 配置

>  `nscurl --ats-diagnostics --verbose https://developer.apple.com`

上述命令会模拟我们 ATS 中配置规则对项目中使用`URLSession:task:didCompleteWithError:`是否能够请求成功，也就是我们发起网络请求的结果。

>  受限于篇幅，我们就不展示命令运行的结果

从 ATS 默认的空字典开始，共计 16 种组合

* `Result : PASS` 说明该配置可以连接到域名服务器成功

* `Result : FAIL` 说明请求域名服务器失败，当前配置无法组合成功

> **注：**虽然其列举的结果不包括    `NSAllowsArbitraryLoadsForMedia` ,`NSAllowsArbitraryLoadsInWebContent `, `NSAllowsLocalNetworking` ，但是这三个是针对特定的文件的，所以不会影响配置

基于**最小最适用**原则选择对应的 ATS 配置。

#### 参考资料

[NSAppTransportSecurity](https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity?language=objc "NSAppTransportSecurity")

[NSExceptionDomains](https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity/nsexceptiondomains?language=objc "NSExceptionDomains")

[Preventing Insecure Network Connections](https://developer.apple.com/documentation/security/preventing_insecure_network_connections?language=objc "Preventing Insecure Network Connections") 


## 内容推荐

> 每年一度的苹果开发者盛会在不久前落幕了。今年的 WWDC 一如既往地精彩。我们将分几期将一些有关 WWDC 2022 上推出的新内容、新技术介绍给大家。

整理编辑：[远恒之义](https://github.com/eternaljust)，[Mimosa](https://juejin.cn/user/1433418892590136)

1、[WWDC22: Wrap up and recommended talks](https://www.hackingwithswift.com/articles/254/wwdc22-wrap-up-and-recommended-talks "WWDC22: Wrap up and recommended talks") -- 来自：hackingwithswift

[@远恒之义](https://github.com/eternaljust)：WWDC22 精彩纷呈，本文作者回顾了他参与本次活动的过程，一些现场有趣的故事，10 个最喜欢的演讲主题，6 个推荐视频来了解刚推出的新内容，还有几个丰富的 WWDC22 周边社区活动。

2、[在 SwiftUI 利用 Live Text API 從圖片中擷取文本](https://www.appcoda.com.tw/live-text-api/ "在 SwiftUI 利用 Live Text API 從圖片中擷取文本") -- 来自：appcoda

[@远恒之义](https://github.com/eternaljust)：在新的 iOS 16，Apple 发布了 Live Text API，可以将图像转换为机器可读的文本格式。我们只需使用 VisionKit 中的一个新类别 DataScannerViewController，来启用有 Live Text 功能的相机，就能提取出图像中的文本。本文同时为你提供了一个 demo 来快速上手体验。

3、[iOS CarPlay｜WWDC22 - 通过 CarPlay 让你的 App 发挥更大的作用](https://juejin.cn/post/7114239495360233479 "iOS CarPlay｜WWDC22 - 通过 CarPlay 让你的 App 发挥更大的作用") -- 来自：师大小海腾

[@远恒之义](https://github.com/eternaljust)：时隔 2 年，CarPlay 迎来了大更新。在 iOS16 中新增的两种支持 CarPlay 的 App 类型：Fueling App 和 Driving Task App。感兴趣的话，和作者一起来探索 Navigation App 如何在受支持车辆中的数字仪表盘上实时绘制地图。

此外，Apple 今年给我们带来了 CarPlay Simulator，它是一个 Mac App，可以帮助你在不离开办公桌的情况下连接 iPhone Device 来开发和测试 CarPlay App，模拟真实环境，而无需经常来回跑到你的车上或购买售后市场主机进行测试。这大幅度提升了开发者的开发测试体验。

4、[用 Table 在 SwiftUI 下创建表格](https://www.fatbobman.com/posts/table_in_SwiftUI/ "用 Table 在 SwiftUI 下创建表格") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：Table 是 SwiftUI 3.0 中为 macOS 平台提供的表格控件，开发者通过它可以快捷地创建可交互的多列表格。在 WWDC 2022 中，Table 被拓展到 iPadOS 平台，让其拥有了更大的施展空间。本文将介绍 Table 的用法、分析 Table 的特点以及如何在其他的平台上实现类似的功能。

5、[What’s the difference between any and some in Swift 5.7?](https://www.donnywals.com/whats-the-difference-between-any-and-some-in-swift-5-7/ "What’s the difference between any and some in Swift 5.7?") -- 来自：Donny Wals

[@Mimosa](https://juejin.cn/user/1433418892590136)：作者通过举例来说明了在 Swift 5.7 中你该如何选择 some 还是 any 关键词，阐述了他们之间的不同，同时谈了一下该如何正确的使用它们，以及未来可能在 Swift 6 中的表现。在作者的另一篇文章 [What are primary associated types in Swift 5.7?](https://www.donnywals.com/what-are-primary-associated-types-in-swift-5-7/) 中它也谈到了，在实际使用场景，例如关联类型的使用中，some 和 any 关键词对程序的影响。

6、[深入理解 Git 底层实现原理](http://chuquan.me/2022/05/21/understand-principle-of-git/ "深入理解 Git 底层实现原理") -- 来自：楚权

[@Mimosa](https://juejin.cn/user/1433418892590136)：大家平时都在使用 Git，但是其中的底层实现原理大家了解么？该文章作者从 Git 整体的架构出发，分层讲解了各层作用，主要谈了对象数据库的设计等。同时也给出了基于其原理的一个设计案例 —— CocoaPods Source 管理机制。文章整体写的通俗易懂，配图也简洁大方。

## 摸一下鱼

整理编辑：[东坡肘子](https://www.fatbobman.com)、[师大小海腾](https://juejin.cn/user/782508012091645/posts)

1、[Goldfishies](https://goldfishies.com "Goldfishies")：开启真·摸鱼模式，在线养金鱼，有 5 种皮肤的鱼可选。对程序员来说刚刚好，不幼稚。

![](http://cdn.zhangferry.com//Images/20220630214456.png)

2、[MusicForProgramming](https://musicforprogramming.net/fortyone "MusicForProgramming")：极客风的听歌网站，纯文字的音乐播放器，作者说里面都是适合编程的音乐。

![](http://cdn.zhangferry.com//Images/20220630213027.png)


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #57 | 周报改版，WWDC22 讲座集锦](https://mp.weixin.qq.com/s/e4ZbFBPqclgy7KyfxVyQZA)

[iOS 摸鱼周报 #56 | WWDC 进行时](https://mp.weixin.qq.com/s/ZyGV6WlFsZOX6Aqgrf1QRQ)

[iOS 摸鱼周报 #55 | WWDC 码上就位](https://mp.weixin.qq.com/s/zDhnOwOiLGJ_Nwxy5NBePw)

[iOS 摸鱼周报 #54 | Apple 辅助功能持续创新](https://mp.weixin.qq.com/s/6jdqa143Y5yr6lbjCuzlqA)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
