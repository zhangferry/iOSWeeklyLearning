# iOS 摸鱼周报 #67 | Xcode Cloud 已支持订阅

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：WWDC22 视频现已提供简体中文字幕；现已推出 Xcode Cloud 订阅
> * 本周学习：移动网络的优化方向；DNS 解析的相关问题
> * 内容推荐：SwiftUI 相关的一些文章推荐。
> * 摸一下鱼：Superhuman 3D 捏人；Swifty Compiler 是一个可以在 iPhone/iPad 上编写和运行 Swift 代码的 app；一款命令行版本的电脑状态管理器 iStats；一款极客范儿的浏览器主题 YuIndex。

## 本期话题

### [WWDC22 视频现已提供简体中文字幕](https://developer.apple.com/cn/news/?id=lw8dnr3l "WWDC22 视频现已提供简体中文字幕")

[@师大小海腾](https://juejin.cn/user/782508012091645/posts)：现在，主题演讲、Platforms State of the Union 以及今年 Apple 全球开发者大会的近 200 场主题演讲皆配有日语、韩语和简体中文字幕。相关视频可在开发者网站或 iPhone、iPad、Mac 和 Apple TV 中的 Apple Developer App 上观看。

![](https://cdn.zhangferry.com/Images/20220901232418.png)

### [Xcode Cloud 已支持订阅](https://developer.apple.com/cn/news/?id=5hlzzu3u " Xcode Cloud 已支持订阅")

[@师大小海腾](https://juejin.cn/user/782508012091645/posts)：Xcode Cloud 是一项内置于 Xcode 中的持续集成和交付服务，能有效地为高质量 App 的开发和交付提升速度。该功能为收费项目，从现在开始到 2023 年底之前注册开发者可以每月免费获取 25 个小时使用时长。如果需要更长时间使用，可以付费订阅这项功能，目前[订阅计划](https://developer.apple.com/xcode-cloud/get-started/ "开始使用 Xcode Cloud (英文))是这样的：

![](https://cdn.zhangferry.com/Images/20220901224059.png)

## 本周学习

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### 移动网络的优化方向

移动网络的优化方向一般从下面三个方面考量：

1. 速度：网络请求的速度怎样能进一步提升？
2. 弱网：移动端网络环境随时变化，经常出现网络连接很不稳定可用性差的情况，怎样在这种情况下最大限度最快地成功请求？
3. 安全：怎样防止被第三方窃听/篡改或冒充，防止运营商劫持，同时又不影响性能？

#### 如何提升速度

不考虑服务器响应时间及基于 TCP 协议，网络请求的流程可以简单分为下面 3 步：

1. DNS 解析，请求 DNS 服务器，获取域名对应的 IP 地址
2. 与服务端建立连接，包括 TCP 三次握手，安全协议同步流程
3. 连接建立完成，发送和接收数据，解码数据

我们可以通过下面三个方面来优化网络速度

1. 直接使用 IP 地址，去除 DNS 解析步骤（一般使用 `HTTPDNS`）
2. 不要每次请求都重新建立连接，复用连接或一直使用同一条连接（长连接）
3. 压缩数据，减小传输的数据大小

### DNS 解析的相关问题

DNS（Domain Name System，域名系统），DNS 服务用于在网络请求时，将域名转为 IP 地址。能够使用户更方便的访问互联网，而不用记住能够被机器直接读取的 IP。

> 域名到 IP 地址的映射，DNS 解析请求采用 UDP 数据报，且明文

DNS 解析的查询方式分为递归查询`和`迭代查询`

* 递归查询：如果主机所询问的本地域名服务器不知道被查询域名的 IP 地址，那么本地域名服务器就以 DNS 客户的身份，向其他根域名服务器继续发出查询请求报文，而不是让该主机自己进行下一步的查询。
* 迭代查询：当根域名服务器收到本地域名服务器发出的迭代查询请求报文时，要么给出所要查询的 IP 地址，要么告诉本地域名服务器：你下一步应当向哪一个域名服务器进行查询。然后让本地域名服务器进行后续的查询，而不是替本地域名服务器进行后续的查询。

#### DNS 解析存在哪些常见问题

DNS 完整的解析流程很长，会先从本地系统缓存取，若没有就到最近的 DNS 服务器取，若没有再到主域名服务器取，每一层都有缓存，但为了域名解析的实时性，每一层缓存都有过期时间，这种 DNS 解析机制有几个缺点：

##### 解析问题

DNS 解析过程不受控制，无法保证解析到最快的 IP。而且一次请求只能解析**一个**域名，大量请求会阻塞流程。

##### 时效问题

缓存时间设置得长，域名更新不及时，设置得短，大量 DNS 解析请求影响请求速度

##### 域名劫持

**域名劫持**，容易被中间人攻击，或被运营商劫持，把域名解析到第三方 IP 地址

#### HTTPDNS

为了解决 DNS 解析的问题，于是有了 HTTPDNS。

HTTPDNS 利用 HTTP 协议与 DNS 服务器交互，代替了传统的基于 UDP 协议的 DNS 交互，绕开了运营商的 Local DNS，有效防止了域名劫持，提高域名解析效率。另外，由于 DNS 服务器端获取的是真实客户端 IP 而非 Local DNS 的 IP，能够精确定位客户端地理位置、运营商信息，从而有效改进调度精确性。


## 内容推荐

1、[在 SwiftUI 中实现视图居中的若干种方法](https://www.fatbobman.com/posts/centering_the_View_in_SwiftUI/ "在 SwiftUI 中实现视图居中的若干种方法") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：将某个视图在父视图中居中显示是一个常见的需求，即使对于 SwiftUI 的初学者来说这也并非难事。在 SwiftUI 中，有很多手段可以达成此目的。本文将介绍其中的一些方法，并对每种方法背后的实现原理、适用场景以及注意事项做以说明。

2、[SwiftUI Navigation 框架的新功能](https://www.appcoda.com.tw/swiftui-navigation/ "SwiftUI Navigation 框架的新功能") -- 来自：AppCoda 编辑团队

[@远恒之义](https://github.com/eternaljust)：自推出以来，NavigationView 一直都是 SwiftUI Navigation 框架的致命弱点。它之前不支持 NavigationLink 中延迟载入目标视图，无法以编程方式导航 Deep Link。在 iOS 16 中，Apple 推出了一个以数据驱动的新导航结构 NavigationStack，让开发者可以从堆栈中推入和弹出视图，NavigationPath 用于管理 routing 堆栈，同时使用 navigationDestination 修饰符来有效率地导航视图。

3、[ContextMenu in SwiftUI](https://www.swiftanytime.com/contextmenu-in-swiftui/ "ContextMenu in SwiftUI") -- 来自：Team SA

[@远恒之义](https://github.com/eternaljust)：在 UiKit 中，使用 3D Touch 按压可实现 Peek 和 Pop 快速预览内容并提供上下文菜单操作，这是一个非常棒的交互体验。在 SwiftUI 中，我们可以用 Menu 弹出菜单进行交互，使用 ContextMenu 则能达到和 UiKit 类似的体验。本文将介绍使用 .contextMenu 修饰符来长按触发上下文菜单，并结合 Menu 和 Button 来添加子菜单。

4、[SwiftUI Gauge](https://sarunw.com/posts/swiftui-gauge/ "SwiftUI Gauge") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：仪表 Gauge 在 iOS 16 (SwiftUI 4) 中引入，是一种能显示范围内值的视图。在现实世界中，仪表是用于测量某物的大小、数量或内容，比如燃油表、温度表、转速表和速度表等仪器设备。Gauge 和 Slider 有些类似，你可以将 Gauge 视为 ProgressView 和 Slider 的结合。本文将介绍 Gauge 的使用方法，几种样式标签显示，以及如何进行自定义仪表视图。

5、[Lock screen widgets in SwiftUI](https://swiftwithmajid.com/2022/08/30/lock-screen-widgets-in-swiftui/ "Lock screen widgets in SwiftUI") -- 来自：Majid

[@远恒之义](https://github.com/eternaljust)：锁屏小组件是 iOS 16 最重磅的功能更新，作为 iPhone 设备上最顶级的访问入口，我们需要把握住用户使用自家 App 的曝光机会。实现锁屏小部件非常简单，因为它的 API 能与主屏幕小部件共享相同的代码。本文将介绍如何为我们的应用程序实现锁屏小部件。


## 摸一下鱼

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

1、[Superhuman 3D 捏人](https://superhuman.fun/ "3D 捏人")：Superhuman 3D character builder for your interfaces。

![](https://cdn.zhangferry.com/Images/20220901232647.png)

2、[cnchar](https://theajack.github.io/cnchar/ "cnchar")：功能全面、多端支持的汉字拼音笔画 js 库。

![](https://cdn.zhangferry.com/Images/20220901233322.png)

3、[Swifty Compiler](https://apps.apple.com/cn/app/swifty-compiler/id1544749600 "Swifty Compiler")：一个可以在 iPhone/iPad 上编写和运行 Swift 代码的 app。

![](https://cdn.zhangferry.com/Images/20220901233246.png)

4、[iStats](https://github.com/Chris911/iStats "iStats")：iStats 是一款命令行版的电脑运行状态记录工具，使用 Ruby 开发。安装和使用方式非常简单：

```
gem install iStats
```
![](https://cdn.zhangferry.com/Images/20220901225407.png)

5、[YuIndex](https://github.com/liyupi/yuindex)：一款极客范儿的浏览器主题，你可以在一个网页版的终端中完成多数需求。目前支持搜索、书签管理、音乐、todo 等功能，可以在这里体验：https://www.yuindex.com/ ：

![](https://cdn.zhangferry.com/Images/20220901230609.png)

## 岗位推荐

公司名：Espressif（乐鑫科技）

城市：上海

**Senior QA Engineer**

Successful candidate will:

* Work closely with users to understand their needs
* Lead the quality assurance for multiple web/mobile projects of the team 
* Create and execute functional and non-functional tests
* Perform testing using a variety of test methodologies, including manual and automated testing for both frontend and backend
* Report, track, and help determine priorities for enhancements and defects utilizing tools likes Jira
* Capture detailed documentation of test execution
* Collaborate across boundaries with peers and business partners in an agile way
* Contribute to a culture of innovation and teamwork


Skills Required

* Bachelor's degree in Computer Science, Information Technology or related area
* Experienced with API, functional, regression, compatibility and acceptance/smoke testing, 
* Experienced with Selenium for web automated testing
* Experienced with at least one major programming language such as Java or Python for backend automated testing
* A strong sense of ownership and ability to collaborate with others as a great team player
* Desire to learn new skills
* Mindset of understanding the real business needs, generating designs to satisfy current and future customer needs

联系方式：简历发送到邮箱：fanbaoying@espressif.com 或加微信：fzhanfei（备注：摸鱼周报）。

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #66 | Shazam 迎来问世 20 周年](https://mp.weixin.qq.com/s/LP1qNAgjzEiDwrR7I32kuA)

[iOS 摸鱼周报 #65 | 什么是精准测试](https://mp.weixin.qq.com/s/lvMHf5qQHpnDGLz1KY-2dg)

[iOS 摸鱼周报 #64 | 与 App Store 专家会面交流](https://mp.weixin.qq.com/s/Bd9MZDqmvmgp1UTr5WKPig)

[iOS 摸鱼周报 #63 | Apple 企业家培训营已开放申请](https://mp.weixin.qq.com/s/nAMshUG4AjWLAAHOFPVqXg)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
