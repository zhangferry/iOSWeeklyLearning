# iOS摸鱼周报 第四十七期

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：苹果多个产品线的更新介绍
> * 面试模块：动态库与静态库的区别
> * 优秀博客：关于该不该换工作以及如何准备面试
> * 见闻：一个新的、偏技术领域的博客推荐模块
> * 学习资料：Rust 数据结构与算法
> * 开发工具：Aria2GUI，一款支持多种协议的轻量级命令行下载工具

## 本期话题

[@zhangferry](https://zhangferry.com)：苹果的多个产品线带来了一波更新。

### [macOS Monterey 12.3](https://developer.apple.com/documentation/macos-release-notes/macos-12_3-release-notes "macOS Monterey 12.3")

* Python 2 被从系统中移出了，但新系统中也并没有预装 Python 3，需要开发者手动安装。
* Universal Control（通用控制）：键盘、鼠标和触摸板可以在 Mac 和 iPad (iPadOS 15.4) 端无缝衔接。
* M1 芯片的电脑可以搭配支持空间音频的 AirPods 使用头部追踪功能。

### [iOS 15.4](https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-15_4-release-notes "iOS 15.4")

* 支持戴口罩的 FaceID 功能，仅支持 iPhone 12 及之后的机型。
* 新增了 37 个 Emoji 表情。

### [Xcode 13.3](https://developer.apple.com/documentation/Xcode-Release-Notes/xcode-13_3-release-notes "Xcode 13.3")

* 新增了一项针对 Swift 的编译优化

```
defaults write com.apple.dt.XCBuild EnableSwiftBuildSystemIntegration 1
```

* Instruments 获得了多项提升，提高了 leaks 、memory graph debugger 扫描的准确性等。

问题收集：

* 反馈打包时有 pod 相关异常
* 反馈编译变慢

### [Swift 5.6 Released](https://www.swift.org/blog/swift-5.6-released/ "Swift 5.6 Released")

* 类型系统的提升。[Type Placeholders SE-0315](https://github.com/apple/swift-evolution/blob/main/proposals/0315-placeholder-types.md "Type Placeholders SE-0315")
* 改进了指针交互的功能
* SPM 增加了运行新插件的能力

还有一个小优化：[SE-0290: Unavailability Condition](https://github.com/apple/swift-evolution/blob/main/proposals/0290-negative-availability.md "SE-0290: Unavailability Condition") 

## 面试解析

整理编辑：[JY](https://juejin.cn/user/1574156380931144)

### 静态库和动态库的区别

#### 静态库（Static Library）

特点如下：

- 分发文件大

- 静态库默认仅将有用到的类文件 `link` 到 `Mach-O` 中 （以类文件为最小链接单位）

- ipa 包小（为了 App 瘦身，尽量将代码放静态库中）

    - 静态库中某个目标文件的代码没有被任何地方引用，则这个目标文件不会被链接到可执行文件中去（分类代码经常被优化掉，一般都使用 `-Objc` 和 `-all_load` 或者 `-force_load` 来处理静态库分类加载问题）

- App 冷启动速度快
	- 前提是不使用 `动态库拆分` 搭配 `动态库懒加载方案`
	- App 启动流程中有 `rebase` 和 `bind`，多个静态库只需要 `rebase` 和 `bind` 一次

- 存在符号冲突可能
- 共享 `TEXT 段`
	- iOS 9 以前单个 Mach-O 的 TEXT 限制 60M
	- iOS 9 以后单个 Mach-O 的 TEXT 限制 500M
- 不需要额外签名验证  
- 静态库符号的可见性可以在链接期间被修改 
- 文件格式多为 `fat` 格式的静态库文件
- 形式多为 `.a` 与 `.framework`
- 静态库不含 `bitcode` 时，引用静态库的目标部署时就不能包含 `bitcode`   

####  动态库（Dynamic Library）
特点如下：

- 分发文件小

- ipa 包大（前提是不考虑懒加载的情况）
	- 动态库会把整个 `lib` 复制进 `ipa` 中

- App 冷启动速度慢
	- App 启动流程中有 `rebase` 和 `bind`，多个动态库只需要多次 `rebase` 和 `bind`

- 需要设置合适的 `runpath` 

- 需要动态加载

- 需要签名且需要验证签名
	- 会检查 `framework` 的签名，签名中必须包含 `TeamIdentifier`，并且 `framework` 和 host App 的 `TeamIdentifier` 必须一致
	- Xcode 重签名，保证动态库签名一致性

- 需要导出符号

- 重复的 `arch` 结构

- App 与动态库中重复代码可以共存，不会发生符号冲突
	- 因为可执行文件在构建链接阶段，遇到静态库则吸附进来，遇到动态库则打个标记，彼此保持独立性。
	- 对于来自动态库的符号，编译器会打个标记，交给 `dyld` 去加载和链接符号，也就是把链接的过程推迟到了运行时执行。（比如 App 使用的是 3.0 版本 SDK，动态库使用的是 1.0 版本 SDK，能正常运行，但是会有风险）

- 链接后需要包含分发大小

- 冷启动过程中，默认会在 `main` 函数之前加载
	- 默认情况下，过多的动态库会拖慢冷启动速度
	- 如果采用懒加载动态库的形式，能够加快 App 的启动速度，可以使用 `dlopen` 和 `bundle` 懒加载优化

- 文件格式 `Mach-O`（一个没有 `main` 函数的可执行文件）

- 动态库不包含 `bitcode` 时，引用动态库的目标部署时可以包含 `bitcode`

- `CocoaPods` 从 `v0.36.0` 开始，可添加关键字 `use_frameworks!` 编译成类似 `Embedded Framework` 的结构（可以称之为 `umbrella framework`）
	- 缺点：默认把项目的依赖全部改为动态库（可使用 `use_modular_headers!`，也可以在 `podsepc` 添加 `s.static_framework = true` 规避）
	- `CocoaPods` 执行脚本把动态库嵌入到 `.app` 的 `Framework` 目录下（相当于在 `Embedded Binaries` 加入动态库）

## 优秀博客

整理编辑：皮拉夫大王在此

> 本期优秀博客主题相对轻松，聊聊面试相关和成长相关的事情。本来想借助本期内容整理下 `rebase` & ` bind ` 的相关技术细节，但是这周被某些自媒体散布的裁员消息给刷屏了，恰巧我本人也是在最近换了工作，因此借助这个机会和大家一起暂停下技术学习的脚步，抬头看看外面的情况。
>
> **阅读后你将获得什么？**
>
> - 如果你在犹豫自己是不是该换工作，那么可以从文章中找到部分答案；
> - 东野浪子和苍耳两位大佬是非常资深的大厂面试官，他们的建议是非常中肯的；
> - 我本人近期面试的一些细节；
> - 尽管不认同面试问八股文，但是还是给大家准备了八股集合，以供大家增强面试信心；


1、**如果你在犹豫期，请看下文**

1.1 [浅谈如何理性的判断自己是否应该换工作](https://mp.weixin.qq.com/s/h5G7LCCAPPh6GfwvRHhkOw) -- 来公众号：东野职场派

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：去年推荐过这篇文章，考虑到目前是金三银四，有些同学可能之前没有看过，因此再推荐一次。

2、**面试官篇：知己知彼，面试官的关注点**

2.1 [给面试者的一些建议](https://djs66256.github.io/2021/12/22/2021-12-22-%E7%BB%99%E9%9D%A2%E8%AF%95%E8%80%85%E7%9A%84%E4%B8%80%E4%BA%9B%E5%BB%BA%E8%AE%AE/#more "给面试者的一些建议") -- 来自：苍耳的技术博客

2.2 [面试过500+位候选人之后，想谈谈面试官视角的一些期待](https://mp.weixin.qq.com/s/kv-_oZObp7QRHeAbrkdfsA) -- 来公众号：东野职场派

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：以上两篇文章的观点本质上来说是一致的，面试官期望候选人是在平时工作中是有所思考和行动的人，而不是临时抱佛脚去应试。**因此用半年时间去刷题复习基础知识，不如用这个时间去认真打磨一个项目**。

3、**候选人篇：近期面试的一些细节**

3.1 [刚换工作，说点找工作相关的事情~](https://mp.weixin.qq.com/s/0BTRFr4m5FGH3fztIMkmVw) -- 来自公众号：皮拉夫大王在此

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：这是我本人近期的亲身经历，前段时间和几个朋友聊了聊换工作的事情。包括：该走该留？如何准备？如何写简历？如何投简历？面试中和面试后各有哪些问题？等等

4、**最全基础知识整理**

4.1 [《史上最全iOS八股文面试题》2022年](https://blog.51cto.com/u_15068388/5076104 "《史上最全iOS八股文面试题》2022年") -- 来自51CTO：宇夜iOS 

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：面试中多多少少会考察到部分基础知识，对基础不放心的同学可以看看。

## 见闻

整理编辑：[zhangferry](zhangferry.com)

> 这一周阅读或者观看到的有价值的讯息。

1、[深度学习撞墙了](https://www.jiqizhixin.com/articles/2022-03-11-4 "深度学习撞墙了") -- 来自：机器之心

[@zhangferry](zhangferry.com)：早在 2016 年，深度学习教父级人物 Hinton 就曾说过，我们不用再培养放射科医生了。但如今 AI 并没有取代任何一位放射科医生，问题出在哪呢？在 Robust.AI 创始人 Gary Marcus 看来深度学习可能就要撞墙了。整个 AI 领域需要寻找新的出路。

深度学习本质上是一种识别模式，当我们只需粗略结果时，它非常适合，但是对于需要精确性操作且风险很高的事情，像放射学和无人驾驶，就需要很谨慎了。人工智能确实没有我们想象的进化那么快，所以它的未来是悲观的吗？并不是，作者提出 Hinton 这样的先驱把深度学习的研究方向带偏了，应当将深度学习和符号处理结合起来，这种混合人工智能可能才是最好的方向。

2、[【译文】谷歌搜索正在消亡](https://sspai.com/post/72065 "【译文】谷歌搜索正在消亡") -- 来自少数派：赵喧典

作者认为 reddit 才是目前最受欢迎的搜索引擎，而谷歌搜索正在走向消亡。认为谷歌不再被认可的原因有这几个：

* 广告：谷歌的大部分收入来源于广告，但过多广告占据搜索词条会严重影响用户体验。
* SEO 优化：很多人的工作就是搜索引擎优化，这违背了公平也会导致搜索质量下降。
* 人工智能：人工智能在尝试帮你找到你想要的内容，但这种揣测经常让人不满意。

3、[领导，我想改善团队的分享氛围](https://mp.weixin.qq.com/s/qfWtn2E3UhssjcbTAqQUEg) -- 来自公众号：hockor

[@zhangferry](zhangferry.com)：大多数人都会在工作中遇到技术分享这个事情，作为 TL 应该如何打造良好的分享氛围呢？首先明确良好的分享氛围是有很大好处的，比如提升团队的技术视野、发现团队牛人、提升团队战斗力、扩大团队影响力等。分享形式较普遍的定期举行技术分享会，任何的分享行为都应该被鼓励。“分享本身是一种精神上自我实现的行为，所以无论分享内容如何，至少这种行为是慷慨的，我们应该及时的、积极的反馈，去鼓励他们往前更进一步”。

同时作为分享的参与者，我们应该抱着探索者的积极的心态去听，有参与感的学习形式是非常高效的。

4、[Usage statistics of content languages for websites](https://w3techs.com/technologies/overview/content_language "Usage statistics of content languages for websites") -- 来自网站：W3Techs

[@zhangferry](zhangferry.com)：当前世界上的网站按语言划分的话，英语最多，这个毋庸置疑。但第二多的竟然是俄语，更令人意外的是，作为使用人口非常多的汉语，其网站数量占比竟然排到了第 10 位。我能想到的原因是，俄语地区互联网发展比较早，催生了很多网站；汉语虽然使用人数多，但是相对集中，国内互联网的发展比较晚，近几年移动互联网浪潮催生了很多 App，但网站的创建则很少。

网站是目前人们获取信息最重要的途径之一，英语网站远超其他语种，也反应了当前英语世界的话语权是更大的。

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20220316231714.png)


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Rust 数据结构与算法

**地址**：https://github.com/QMHTMY/RustBook

一本 Rust 书籍，有简体和繁体版（英文版和日文版正在撰写中），内容包括算法分析，基本数据结构和算法，外加一些实战，共有九章。包含了大家常用的常见的数据结构的实现和讲解，配有详实的代码和清晰简明的图解。

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/%E6%88%AA%E5%B1%8F2022-03-17%20%E4%B8%8B%E5%8D%886.37.13.png)

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Aria2GUI 

**地址**：https://github.com/yangshun1029/aria2gui

**软件状态**：免费

**软件介绍**：

`Aria2GUI` 是一款支持多种协议的轻量级命令行下载工具，可以轻松的下载离线资源。

![Aria2GUI](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/687474703a2f2f692e696d6775722e636f6d2f4d455a7150397a2e706e67.png)


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第四十六期](https://mp.weixin.qq.com/s/8Wpfk9yxpjwaDXN7iXIcvQ)

[iOS摸鱼周报 第四十五期](https://mp.weixin.qq.com/s/_N98ADlfQCUkxYjmH0SvZw)

[iOS摸鱼周报 第四十四期](https://mp.weixin.qq.com/s/q__-veuaUZAK6xGQFxzsEg)

[iOS摸鱼周报 第四十三期](https://mp.weixin.qq.com/s/Ktk5wCMPZQ5E-UASwHD7uw)

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/WechatIMG384.jpeg)
