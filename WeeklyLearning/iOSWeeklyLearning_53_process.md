iOS 摸鱼周报 52 | 如何规划个人发展

![](http://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * 面试模块：
> * 优秀博客：App Extension
> * 学习资料：
> * 开发工具：

## 本期话题



## 阅读

> 本期阅读的书籍是《深入解析 MacOS X & iOS》

### 达尔文主义：OS X 的进化史

有些人可能会注意到我们在说 MacOS 时通常会带上 X，将其叫做 MacOS X，本篇主要内容是让大家理解「X」 是如何发展出来的。

在 X 之前的版本叫做 Mac OS Classic，它是一个相对粗糙且很不成熟的操作系统。苹果创始人乔布斯离开苹果时创办了 NeXT，NeXT 也有自己专门的操作系统 NeXTSTEP。NeXTSTEP 有一些前卫的特性：

* 采用 Mach 微内核
* 使用Objective-C作为开发语言
* 面向对象思想贯穿整个操作系统

后来乔布斯回归苹果，将 NeXTSTEP 带回了苹果。于是自然而然的，Mac OS Classic 和 NeXTSTEP 两个非常小众的操作系统进行了融合。他们一个拥有伟大的 GUI 但设计糟糕，一个设计很棒但GUI平淡，融合之后的 Mac OS X 则吸收两者的优点成为了一个流行的多的操作系统。此时的几个核心组件：Cocoa、Mach、IOKit、Xcode的Interface Builder 都来自于 NeXTSTEP。这个操作系统内核就是我们熟知的 Darwin（中译为达尔文）。

Darwin 是开源的，以它为核心诞生了 iOS、tvOS、watchOS、BridgeOS 等一系列变体操作系统。除 MacOS 中的Darwin 外，其他 Darwin 版本都是不开源的。有一个命令可以查看系统的架构信息：uname。

```bash
$ uname -v
Darwin Kernel Version 21.2.0: Sun Nov 28 20:28:54 PST 2021; root:xnu-8019.61.5~1/RELEASE_X86_64
```

Darwin 和 Darwin变体的一些列 OS 版本是同步更新的。它们之间的版本遵循这个关系：

> Darwinver = 10.(MacOSVer + 4)  = (iOSVer + 6) = (TvOSVer + 6) = (WatchOSVer + 13)

后来 MacOS 的主版本号从 10 升级为 11，上面MacOS的版本对应关系发生了一些变化。另外就是名称这里，如果继续叫做 「X」，是有些不恰当了，但很多时候人们还是将Classic之后的 MacOS 叫做 MacOS X。

### Darwin 操作系统的演变历史。

![](http://cdn.zhangferry.com/Images/20220504081928.png)

图片来自（*OS Volum 1）

可以再一个iOS的小故事，iOS1.x 版本最初的代号是 Alpine，这是i系列设备的默认root密码。但最后发布的版本代号是 Heavenly，因为这个版本的操作系统拥有完整的调试符号、未加密还容易反汇编，很多越狱者都依赖从这个版本中提取的符号和函数调用关系寻找破解灵感，从越狱者角度来看确实如天堂般美好。

### Darwin 的内部组成

Darwin 是一个类UNIX的操作系统核心。它的内部可以近似看做，Darwin = kernel + XNU + 运行时。XNU 是一个占据关键作用的 Darwin 核心，XNU = Mach + BSD + 其他组件。

初版的 XNU 是 NeXTSTEP 的核心，它包括由卡耐基梅隆大学发展的 Mach2.5 版本和 4.3 版本的BSD。NeXTSTEP 合入苹果后，Mach被升级为 3.0，BSD 升级为 FreeBSD。

Mach 和 BSD 一个是微内核一个是宏内核，所以 XNU 也是一个混合架构。

![](http://cdn.zhangferry.com/Images/20220504000309.png)

#### Mach

Mach（微内核）的特点是相对灵活，它可以把操作系统的核心部分作为独立的进程运行，它跟 kernel 分属不同的内存空间。但因为内部会有更频繁的内核态/用户态上下文切换，这会额外消耗时间，同时内核与服务进程之间的消息传递也会降低运行效率，所以这种设计通常会降低性能。它的优点是服务进程容易扩展，我们熟知的 MachO 能同时支持多架构文件，就得益于Mach架构的灵活性。以此为基础 MacOS 顺利的从 PowerPC 过渡到 Intel 再到 M1。

#### BSD

BSD （**B**erkeley **S**oftware **D**istribution 伯克利软件包）是一个派生自 Unix 的操作系统。宏内核的特点是用户服务和内核服务都运行在同一内存空间，这有效降低了内核态/用户态之间的频繁切换，执行效率会更高。除了执行效率 BSD 同时还带来了 POSIX、安全策略、加密框架、用户和用户组、IPC、审计机制等操作系统能力。但是宏内核的代价是什么呢，就是扩展性较差，有一个服务崩溃，整个操作系统就会崩溃。

既然没有完美的内核模式，于是苹果就将两者混合，它同时兼顾微内核和宏内核各自的优点，就是现在的 Hybrid kernel 了。

### 关于吉祥物的故事

操作系统发展的早期人们热衷于为受欢迎的操作系统设置吉祥物，就像Linux的吉祥物是一只企鹅。

![](http://cdn.zhangferry.com/Images/20220504082713.png)

它叫Tux，大多数人认为这个名字来源于**T**orvalds **U**ni**X**。

BSD的吉祥物是一只小恶魔😈，叫做Beastie，它的发音跟BSD很像。

![](http://cdn.zhangferry.com/Images/20220504083150.png)



[BSD](https://zh.wikipedia.org/wiki/BSD%E5%B0%8F%E6%83%A1%E9%AD%94)

Darwin这里，吉祥物是**Hexley**，它是一个卡通的鸭嘴兽，带着BSD小恶魔的帽子，拿着三叉戟。

![](http://cdn.zhangferry.com/Images/20220504083800.png)

这也是 「*OS Internal 三部曲」的书籍封面人物。

### 走向移动端的 iOS

iOS1.x 版本最初的代号是 Alpine （这是i系列设备的默认root密码），但最后发布的版本代号是 Heavenly。

### 未来的一些展望

1、根除Mach。

内核中的 Mach API 是 NeXTSTEP 时代的产物，运行效率较低，可以完全由BSD代替。但这需要巨大的工作量。直到现在也没有达成，以后应该也不会了。

2、兼容 ELF 格式。MacOS无法融入UN*X的世界最大的一个困难就是坚持使用Mach-O二进制格式。当然这个想法也需要依赖上面的根除Mach，这样Linux、BSD中的程序就可以不经修改直接迁移到OS X上了。这是很美好的想象，但苹果更重视的是可控，而非兼容。

3、和iOS合并。这个是容易达到的，特别是M1芯片的发布，现在MacOS和iOS已经都运行在arm64架构的芯片上了。但还是那句话，技术要为公司策略让路，不同的操作系统应具有不同的用途，即使是iPadOS，苹果也不希望其能够代替MacOS，融合是技术上的完美而非效益的最佳方案。





## 面试解析

整理编辑：[JY](https://juejin.cn/user/1574156380931144)



## 优秀博客
> 本期优秀博客的主题为：App Extension。

1、[iOS - App Extension 整体总结](https://www.cnblogs.com/junhuawang/p/8178276.html "iOS - App Extension 整体总结") -- 来自博客园：俊华

[@我是熊大](https://github.com/Tliens)：本文比较全面的介绍了App Extension的种类以及使用方法，平时不怎么使用的extension竟然有十几种。通过此文应该能对extension有个整体的了解。

2、[App与Extensions间通信共享数据](http://yulingtianxia.com/blog/2015/04/06/Communication-between-your-App-and-Extensions/ "App与Extensions间通信共享数据") -- 来自博客：杨萧玉

[@我是熊大](https://github.com/Tliens)：本文利用WatchKit Extension实现了app与watch之间的通信，介绍了containing app与app extension之间如何进行通信和数据共享。

3、[Photo Editing Extension 详解](https://colin1994.github.io/2016/03/12/Photo-Editing-Extension/ "Photo Editing Extension 详解") -- 来自博客：colin

[@我是熊大](https://github.com/Tliens)：本文通过一个Demo演示，介绍了Photo Editing Extension如何开发。

4、[iOS14 Widget小组件开发(Widget Extension)](https://www.jianshu.com/p/94a98c203763 "iOS14 Widget小组件开发(Widget Extension)") -- 来自简书：Singularity_Lee

[@我是熊大](https://github.com/Tliens)：iOS14之后出现了非常重要的extension，这就是Widget，桌面小组件，本文十分详细的介绍了如何开发Widget，如果你也有开发需求，推荐阅读。

5、[揭秘 iOS App Extension 开发 —— Today 篇](https://www.jianshu.com/p/bbc6a95d9c54 "揭秘 iOS App Extension 开发 —— Today 篇") -- 来自简书：Cyandev

[@我是熊大](https://github.com/Tliens)：在iOS14之前，是没有桌面组件的，那时候叫做Today Extension，但在iOS14之后，这个extension已经被widget代替。本文借助一个todo的demo，介绍了Today Extension。



## 见闻

> 这一周阅读/浏览到的有趣的资讯。

1、[985 毕业后，我成了天光墟里收破烂的“无冕之王”](https://mp.weixin.qq.com/s/LeC_aOiYVcs3MA8jkDYc7Q) -- 来自公众号：显微故事

[@远恒之义](https://github.com/eternaljust/)：985 毕业的武楷斯开设了一家名为“永续旧物”的店铺，一个属于他一个人的跳蚤市场。受父母工作的影响，他从小辗转于多地，在不同的城市读书和生活，倍感孤独的他却与旧物结下了不解之缘。15 年他凭借自己捡破烂的本事在美国走南闯北，穷游了美国 16 个城市。与旧物对话，他从此不再孤独。面对采访，他表示他的生活不曾焦虑。

2、[告别华尔街十年，我在非洲做起 WiFi 生意](https://mp.weixin.qq.com/s/fote_47nG8AQW-lrkQy9Hw) -- 来自公众号：志象网

[@远恒之义](https://github.com/eternaljust/)：拥有传奇经历的周涛定居在非洲这片“最后十亿人”（last billion）的土地，目前正在肯尼亚创业，做“社区 WiFi”。他在国内做云计算的过程中结实了肯尼亚外交官 David，现在的合伙创始人。David 对肯尼亚目前绝大多数的用户不能廉价上网这件事情耿耿于怀，想要在肯尼亚发展互联网，必须先搞定昂贵的上网资费。周涛提供的公共 WiFi 网费非常低，做到了本土市场价格的 1/10。因地制宜，周涛大量雇佣当地社区青年来服务社区用户，打破了大家对非洲青年的固有印象。通过本地化的管理，公司的规模达到了 200 多人，其中大概只有五六个中国人。

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
