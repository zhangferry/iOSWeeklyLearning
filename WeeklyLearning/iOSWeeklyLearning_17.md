# iOS摸鱼周报 第十七期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 这期的 `本期话题` 从一个同学的问题入手，谈了些关于习惯的理解。
> * Tips 部分围绕一个问题展开：String.count 和 NSString.length 结果是一样的吗？他们之间有什么差别？后面的阅读可以帮你回答这个问题。
> * 面试专题带来网络部分的第二弹，关于 TCP 连接，关于三次握手，四次挥手。
> * 博客部分整理了一些网络优化的文章，网络请求分为：请求前阶段，连接阶段，数据处理阶段，各个阶段都是可以进行优化的。
> * 如何用 Swift 实现常用的数据结构？来看 Swift Algorithm Club 吧。
> * 桌面版 Homebrew：Cakebrew，一个好用的剪切板工具：Paste - Clipboard Manager。

## 本期话题

[@zhangferry](https://zhangferry.com)：本期话题来源于一个同学的提问：普通人如何摆脱娱乐的诱惑，让自己可以每天，或者每周有固定的学习时间。

这个问题比较难回答，因为娱乐是人的本能，真正做到摆脱诱惑是非常难的。不光是学习，其实有很多事情我们都是知道应该要做什么的，但就是无法做到，那到底是为什么呢？《Synaptic Self》这本书从脑科学的角度解释了这个现象：

> 大脑中的新皮层（neocortex，所谓“理性”居住的地方，尤其是前额叶）在进化历史上是较为新近的年代才进化出来的，跟底层较原始的模块（如主管情绪的杏仁核）之间的神经网络沟通并不是合作无间，这就解释了为什么有些事情我们明明知道是对的，但就是不能说服自己，情绪还是在那里不依不挠的驱使你去做另一样事情。

显然来自大脑的本能我们无法克服，但我们可以换个角度考虑这个问题，不再是考虑如何摆脱诱惑，而是如何培养一个定期学习的习惯。它们能达到一样的效果，而且相对来说，习惯养成比对抗本能显得更容易一些。

关于习惯有很多书专门去讲了，像是《习惯的力量》、《微习惯》等，这里不展开太多，仅说下我个人认为有用的几个小技巧：

* **拆分目标**：即微习惯，把定时学习拆分成每天 5-10 分钟的固定学习，目标越小，我们在准备实施的时候遇到的阻力就会越小。比如我自己的学习习惯，每天在群里分享一点自己学习的知识，平均准备时长在 10 分钟左右，偶有断开连接，但毕竟负担不大，多数时间都在坚持输出，已经差不多有一年时间了。其实类似的还可以是每天弄懂一个开发概念，每天读两页书等。**这一步是最关键，最重要的，因为大部分情况我们没能采取行动都是因为`杏仁核`的阻挠，微习惯的核心作用就是为了避开情绪的负担，先能够行动起来**。
* **找到监督环境**：即使习惯微小，要完全自觉可能还是有些困难的，可以附带施加一些外部监督力量。想象下在公司的一天和在家的一天，同样的时间，大部分人的工作效果都是在公司更好一些，因为公司相当于外部的监督力量，能提供更好的工作氛围。还是我那个例子，我是用交流群充当监督作用，因为知道有人在期待这个，所以我有不得不做的理由；类似的还有付费群，交钱入群，完成目标退钱，甚至还能挣钱；网络自习室，打开摄像头互相监督等。
* **提供奖励**：每完成一次目标都可以提供适当的奖励给自己，奖励的目的是让下次行动时能更容易一些，以此来形成一个良性循环。对我那个每日分享的微习惯来说，因为那些总结的内容，后期写文章都是有用到的，所以对我来说奖励就是提前启动准备工作了，后期写东西会更容易一些。当然大家可以根据自己的情况设置适当的奖励，比如增加一点娱乐的时间等。

这几点是按顺序来说的，也可以当做一个培养习惯的简单模型，实际场景大家可以根据自身情况适当调整。习惯的培养是一个持久战，不是坚持 21 天就算养成了，也不是中断了几次就是失败了，只管一点点持续下去，它总会反馈给我们好的结果。

如果对该话题有兴趣的小伙伴还可以评论区继续跟我们交流。

## 开发Tips

内容贡献：[HansZhang](https://github.com/HansZhang)，校验整理：[夏天](https://juejin.cn/user/3298190611456638)

###  关于 String.count 和 NSString.length 的探究

在开发过程中使用 Swift 的 `String.count` 创建 `NSRange` 时，发现在某些语言下（印度语言，韩语）对应位置的文字没有应用预期的显示效果。通过打印同一个字符串在 NSString 类型下的 `length` 和在 Swift 的 String 类型下的 `count` 发现二者的值并不相等，`length` 比 `count` 要大一些。也就是说，在创建 NSRange 时，Swift 的 `String.count` 并不可靠，我们可以使用 `NSString.length` 解决这个问题。

#### `length` 和 `count` 的不同

那么，为什么同一个字符串的 `长度` 在 String 与 NSString 中会得到不同的值呢？我们来看一下 `String.count` 与 `NSString.length` 各自的官方定义：

> * String.count: The number of characters in a string.
> * NSString.length: The length property of an NSString returns the number of UTF-16 code units in an NSString

通过上述官方文字，我们隐约能察觉到一丝不同而继续发出疑问🤔️：

- 这个 `characters` 与 `UTF-16 code units` 是一回事么？
- 如果不是的话那各自的定义又是什么呢？

在 [Swift doc](https://docs.swift.org/swift-book/LanguageGuide/StringsAndCharacters.html#ID290 "Swift doc") 中对 Swift 中的 Character 有如下说明：

> Every instance of Swift’s Character type represents a single **extended grapheme cluster**. An extended grapheme cluster is a sequence of one or more Unicode scalars that (when combined) produce a single human-readable character.

在 Swift 1.0 版本的 [Swift String Design](https://github.com/apple/swift/blob/7123d2614b5f222d03b3762cb110d27a9dd98e24/docs/StringDesign.rst#id35 "Swift String Design") 中，也找到了相关描述：

> `Character`, the element type of `String`, represents a **grapheme cluster**, as specified by a default or tailored Unicode segmentation algorithm. This term is [precisely defined](http://www.unicode.org/glossary/#grapheme_cluster) by the Unicode specification, but it roughly means [what the user thinks of when she hears "character"](http://useless-factor.blogspot.com/2007/08/unicode-implementers-guide-part-4.html). For example, the pair of code points "LATIN SMALL LETTER N, COMBINING TILDE" forms a single grapheme cluster, "ñ".

所以我们可以粗略的理解为一个 Character 表示一个人类可读的字符，举个例子：

```swift
let eAcute: Character = "\u{E9}"                         // é
let combinedEAcute: Character = "\u{65}\u{301}"          // e followed by ́
// eAcute is é, combinedEAcute is é

let eAcute: String = "\u{E9}"
let combinedEAcute: String = "\u{65}\u{301}"
// eAcute is é, combinedEAcute is é
print(eAcute.count) // 1
print(combinedEAcute.count) // 1
print((eAcute as NSString).length) // 1
print((combinedEAcute as NSString).length) // 2
```

`é` 在 unicode 中由一个标量（unicode scalar value）表示，也有由两个标量组合起来表示的，不论哪种在 Swift 的 String 中都表示为**一个** Character。

那我们再返回来看 Swift `String.count` 的定义就好理解了，**count** 表示的是 Character 的数量，而 NSString 的 **length** 表示的是实际 unicode 标量（code point）的数量。所以在某些有很多组合标量字符的语言中（或者 emoji 表情）一个 `Character` 与一个 unicode 标量并不是一一对应的，也就造成了同一个字符 `NSString.length` 与 `String.count` 值可能不相等的问题，其实这个问题在 [Swift doc](https://docs.swift.org/swift-book/LanguageGuide/StringsAndCharacters.html#ID290) 中早有提示：

> The count of the characters returned by the **count** property isn’t always the same as the **length** property of an **NSString** that contains the same characters. The length of an NSString is based on the number of 16-bit code units within the string’s UTF-16 representation and not the number of Unicode extended grapheme clusters within the string.

我们可以看到对于字符串 Character 这样 **grapheme cluster** 式的分割字符的方式，更符合我们人类看到文字时的预期的，可以很方便的遍历真实字符，且包容多种多样的语言。但在带来便利的同时也增加了实现上的复杂度。由于每个 `Character` 长度不尽相同，`String.count` 无法像 `NSString.length` 那样使用 `O(1)` 复杂度的情况简单计算固定长度的个数，而是需要遍历每一个字符，在确定每个 Character 的边界和长度后才能推算出总个数。所以当你使用 `String.count` 时，也许要注意一下这是一个 `O(n)` 的调用。


## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。计算机网络是面试必考的知识点，最好比较系统的去学习了解，推荐书籍：《图解 TCP/IP》、《网络是怎样连接的》；推荐付费课程：[计算机网络通关 29 讲](https://t7.lagounews.com/RR7FRYRDsi3B1 "计算机网络通关 29 讲")，大家可以根据自己喜欢的学习方式进行选择。


### 什么是 TCP 的三次握手和四次挥手？

我们先来看一下 TCP 报文头部结构：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210704165732.png)

握手阶段主要依靠以下几个标志位：
* SYN：在建立连接时使用，用来同步序号。SYN=1 代表这是一个请求建立连接或同意建立连接的报文，只有前两次握手中 SYN 才为 1，带 SYN 标志的 TCP 报文段称为同步报文段；
  * 当 SYN=1，ACK=0 时，表示这是一个请求建立连接的报文段
  * 当 SYN=1，ACK=1 时，表示对方同意建立连接
* ACK：表示前面确认号字段是否有效。ACK=1 代表有效。带 ACK 标志的 TCP 报文段称为确认报文段；
* FIN：表示通知对方本端数据已发送完毕，要关闭连接了。带 FIN 标志的 TCP 报文段称为终止报文段。

**三次握手是指建立一个 TCP 连接时，需要客户端和服务端总共发送 3 个包，需要三次握手才能确认双方的接收与发送能力是否正常。**

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210703051424.png)

1. 客户端向服务端发起连接请求，需要发送一个 SYN 报文到服务端。
2. 当服务端收到客户端发过来的 SYN 报文后，返回给客户端 SYN、ACK 报文。`这时候服务端可以确认客户端的发送能力和自己的接收能力正常`。
3. 客户端收到该报文。`这时候客户端可以确认双方的发送和接收能力都正常`。然后客户端再回复 ACK 报文给服务端，服务端收到该报文。`这时候服务端可以确认客户端的接收能力和自己的发送能力正常。所以这时候双方都可以确认自己和对方的接收与发送能力都正常`。就这样客户端和服务端通过 TCP 建立了连接。

**四次挥手的目的是关闭一个 TCP 连接。**

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210703051443.png)

1. 客户端主动发起连接断开，发送一个 FIN 报文到服务端；
2. 服务端返回给客户端 ACK 报文。此时服务端处于关闭等待状态，而不是立马给客户端发 FIN 报文，这个状态还要持续一段时间，因为服务端可能还有数据没发完。`此时客户端到服务端的连接已经断开。但客户端和服务端之间所建立的 TCP 连接通道是全双工的，此时只是处于半关闭状态，所以服务端到客户端可能还会传递数据`；
3. 当服务端的数据都发送完毕后，给客户端发送一个 FIN，ACK 报文；
4. 客户端回应一个 ACK 报文。注意客户端发出 ACK 报文后不是立马释放 TCP 连接，而是要经过 2MSL（最长报文段寿命的 2 倍时长）后才释放 TCP 连接。而服务端一旦收到客户端发出的确认报文就会立马释放 TCP 连接，所以服务端结束 TCP 连接的时间要比客户端早一些。`此时服务端到客户端的连接也已经断开，整个 TCP 连接关闭`。


### 为什么 TCP 连接是三次握手？两次不可以吗？

TCP 是一个全双工协议，它要保证双方都具有接收与发送的能力。

因为需要考虑连接时丢包的问题，如果只握手两次，第二次握手时如果服务端发给客户端的确认报文段丢失，此时服务端已经准备好了收发数据（可以理解为服务端已经连接成功），而客户端一直没收到服务端的确认报文，所以客户端就不知道服务端是否已经准备好了（可以理解为客户端未连接成功），这种情况下客户端不会给服务端发数据，也会忽略服务端发过来的数据。

如果是三次握手，即便发生丢包也不会有问题，比如如果第三次握手客户端发的确认报文丢失，服务端在一段时间内没有收到确认报文的话就会重新进行第二次握手，也就是服务端会重发 SYN 报文段，客户端收到重发的报文段后会再次给服务端发送确认报文。


### 为什么 TCP 连接是三次握手，关闭的时候却要四次挥手？

主要是建立连接时接收者的 SYN-ACK 一同发送了，而关闭时 FIN 和 ACK 却不能同时发送，因为断开连接要处理的情况比较多，比如服务器端可能还有发送出的消息没有得到 ACK，也可能服务器资源需要释放等。所以先发一个 ACK 表示已经收到了发送方的请求，等上述情况都有了确定的处理，再发 FIN 表示接收方已经完成了后续工作。

类比现实世界中，你收到了一个 Offer，出于礼貌你先回复一下，然后思考一段时间再回复 HR 最终的结果。


### 为什么客户端发出第四次挥手的确认报文后要等 2MSL 的时间才能释放 TCP 连接？

这里同样是要考虑丢包的问题，如果第四次挥手的报文丢失，服务端没收到确认报文就会重发第三次挥手的报文，这样报文一去一回最长时间就是 2MSL，所以需要等这么长时间来确认服务端确实已经收到了。

参考：[https://zhuanlan.zhihu.com/p/141396896](https://zhuanlan.zhihu.com/p/141396896 "https://zhuanlan.zhihu.com/p/141396896")

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`网络优化`

网络优化大致可分为三个阶段：
1、请求前阶段：接口冷却，优先级调整、接口依赖、数据压缩、请求拦截

2、连接阶段：IP 直连、HTTPDNS、重试、不同网络环境的超时处理

3、数据处理阶段：数据解析、缓存

一、[全面理解DNS及HTTPDNS](https://juejin.cn/post/6844903987796246542 "全面理解DNS及HTTPDNS") -- 来自掘金：iosmedia

你有没有遇到过，某些地区的连接成功率很低，有时连接成功，有时连接不成功呢？如果你遇到这种情况那可能是 DNS 解析出现了问题。本文全面解析了 DNS 是什么，为什么会被劫持，为什么 HTTPDNS 可以解决这种问题，如果你有类似困惑，建议阅读本文，相信一定能收获满满。

二、[iOS IP 直连原理剖析](https://juejin.cn/post/6844903564960088071 "iOS IP 直连原理剖析") -- 来自掘金：joy_xx

HTTPDNS 是自研还是使用第三方的？如果自研的话会不会成本比较高呢？IP 直连可能适合，遇到 DNS 问题，但又不希望花费大量时间精力的解决方案。其本质就是服务器有多个 IP，app 内置多个 IP，如果连接成功，每次启动就去请求更新新的 IP 列表。

三、[网络请求优化之取消请求](https://juejin.cn/post/6844903736968478727 "网络请求优化之取消请求") -- 来自掘金：阿南

本文介绍了，我们在开发中一定会遇到的场景：销毁页面时，取消网络请求；同一接口短时间请求多次，做忽略处理；请求重试，防止网络抖动造成连接失败。


四、[iOS网络缓存扫盲篇](https://www.jianshu.com/p/fb5aaeac06ef "iOS网络缓存扫盲篇") -- 来自简书：iOS程序猿

iOS 系统会自动对 GET 请求进行缓存；同时提供了`NSURLCache`支持我们设置缓存路径和缓存大小，文中就如何控制缓存的有效性展开进行了讨论。

五、[移动端IM开发者必读(二)：史上最全移动弱网络优化方法总结](http://www.52im.net/thread-1588-1-1.html "移动端IM开发者必读(二)：史上最全移动弱网络优化方法总结") -- 来自即时通讯网

作者针对 IM 场景下弱网进行的一系列总结，文中提到了很多理论基础，提出自动重试时导致后台雪崩的重要因素的观点。本文篇幅较长，适合有一定网络底层基础的人阅读。

六、[iOS中的网络调试](https://juejin.cn/post/6844904185268273159 "iOS中的网络调试") -- 来自掘金：即刻团队

"开发 iOS 的过程中，有一件非常令人头疼的事，那就是网络请求的调试，无论是后端接口的问题，或是参数结构问题，你总需要一个网络调试的工具来简化调试步骤。" 本文是即刻团队进行网络调试的解决方案。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Swift Algorithm Club

地址：https://github.com/raywenderlich/swift-algorithm-club

由 [raywenderlich](https://www.raywenderlich.com/whats-new) 创立的 Swift 算法俱乐部，在这里会用 Swift 来解释和实现大部分常见的数据结构和算法，例如栈、队列、快速排序、BFS、KMP 等等，如果按照他的学习路线来学习的话，难度由浅入深，循序渐进，很适合入门选手。另外你也可以自己选择感兴趣的内容来查看，适合想要温习算法和数据结构或者温习 Swift 语法的朋友👍。

## 工具推荐

整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)，[zhangferry](https://zhangferry.com)

### Cakebrew

**地址**：https://www.cakebrew.com/

**软件状态**：免费，[开源](https://github.com/brunophilipe/Cakebrew)

**软件介绍**：

Homebrew 是 Mac 端常用的包管理工具，但其仅能通过命令行操作，对那些不擅长使用命令行的开发来说会是一种苦恼，而且命令行确实不够直观。Cakebrew 是一款桌面端的 Homebrew 管理工具，它包含常用的 Homebrew 功能，并将其可视化，像是已安装工具，可升级工具以及工具库等功能。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210704205546.png)

### Paste - Clipboard Manager

**地址**: https://apps.apple.com/us/app/paste-clipboard-manager/id967805235

**软件状态**: 收费 ¥98/年 

**软件介绍**：

Paste for Mac 是 Mac 平台上一款专业的剪切板记录增强工具，它能够为您储存您在设备上复制的所有内容，并将其储存在 Paste for Mac 的历史记录中。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210703184817.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期内容

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

[iOS摸鱼周报 第十三期](https://mp.weixin.qq.com/s/qJG74OQsJ1VV1cB6fDX8TA)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)