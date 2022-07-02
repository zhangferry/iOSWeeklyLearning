# macOS 进化史

macOS 最为 iOS 开发的钦定操作系统，且 iOS 本身就是通过它衍生出来的，所以我们跟它之间会经常打交道。为了验证你对它的熟悉程度，看下能否回答这几个问题：

* 我们在说 MacOS 时通常会带上「X」，将其叫做 MacOS X 或者 OS X，这是为什么呢？「X」 有什么含义？
* Darwin、XNU、Mach、BSD 分别代表什么，之间又有什么关系？
* Mac OS 与 Unix 是什么关系？
* Apple 开源了 Darwin，对应的开源社区为什么发展不起来？

本篇文章致力于帮助解答这些问题，也会顺道讲些 Apple 相关的背景小故事。

文章内容主要参考《Mac OS X And iOS Internals》（中译本叫《深入解析Mac OS & iOS》）和 《*OS Internal Volume I -- User Mode》，作者都是 Jonathan Levin。前者完书于 2012年，后者第二版本完书于 2019 年，后者不仅是前者的完善版本，还是一个全新版本，大量图文都进行了重写。随着时间的推进，后者对最新的技术有了更多讨论。

![](https://cdn.zhangferry.com/Images/julian-hochgesang-dc-I7GCibzs-unsplash.jpg)

## MacOS 发展背景

### 背景

MacOS 的早期版本叫做 Mac OS Classic，它诞生于苹果，拥有伟大的 GUI 却是一个相对粗糙且很不成熟的操作系统。

在这期间苹果创始人乔布斯离开苹果创办了 NeXT，NeXT 公司生产 NeXT 计算机和NeXTstation，它们运行在叫做 NeXTSTEP 的操作系统之上。NeXTSTEP 有这些比较前卫的特性：

* 采用 Mach 微内核
* 使用 Objective-C 作为开发语言
* 面向对象思想贯穿整个操作系统
* 设备驱动开发是一个面向对象的框架，叫做 DriverKit

### MacOS X 诞生

后来乔布斯回归苹果，也将 NeXTSTEP 带回了苹果。于是自然而然的，Mac OS Classic 和 NeXTSTEP 两个非常小众的操作系统进行了融合。他们一个拥有伟大的 GUI 但设计糟糕，一个设计很棒但 GUI 平淡，融合之后起到了 1+1 大于 2 的效果，诞生了一个流行的多的操作系统，这就是 MacOS X。「X」的含义是罗马数字 「10」，对应了此时 MacOS 的版本号 10.x，这个版本之后又发展了很长时间。

MacOS X 此时的几个核心组件：Cocoa、Mach、IOKit、Xcode 的 Interface Builder 都来自于 NeXTSTEP。这个操作系统的内核就是 Darwin（中译为达尔文）。

Darwin 是开源的，以它为核心诞生了 iOS、tvOS、watchOS、BridgeOS（用于 Macbook Touch Bar 的 OS） 等一系列变体操作系统。有一个命令可以查看系统所使用的 Darwin 版本信息：uname。

```bash
$ uname -v
Darwin Kernel Version 21.2.0: Sun Nov 28 20:28:54 PST 2021; root:xnu-8019.61.5~1/RELEASE_X86_64
```

Darwin 和 Darwin 变体的一系列 OS 版本是同步更新的。它们之间的版本遵循这个关系：

> Darwinver = 10.(MacOSVer + 4)  = (iOSVer + 6) = (TvOSVer + 6) = (WatchOSVer + 13)

后来 MacOS 的主版本号从 10 升级为 11，上面 MacOS 的版本对应关系发生了一些变化。到了这里有必要再理一遍 MacOS 的名称变化情况，确实很少有人能准确的称呼它，因为它的命名发生过不少[变化](https://zh.wikipedia.org/wiki/MacOS "MacOS - Wiki")。

| 时间段            | MacOS 名称     | 说明                                                         |
| ----------------- | -------------- | ------------------------------------------------------------ |
| 创建 ~ 2001 年    | MachOS Classic | 古典 MacOS                                                   |
| 2001年 ~ 2011 年  | Mach OS X      | NeXTSTEP 与 MacOS Classic 合并之后的版本                     |
| 2012 年 ~ 2015 年 | OS X           | 这是最后一个以猫科动物命名的 OS 版本，此后开始以加州地标命名 |
| 2016 年至今       | macOS          | 便于与iOS、tvOS、watchOS 命名统一                            |

为了便于混乱，从这开始的下文在讲到 MacOS 统称时均以 macOS 代替。

### Darwin 操作系统的演变历史。

![](https://cdn.zhangferry.com/Images/20220504081928.png)

图片来自（*OS Volume 1）

> 结合上面图片可以再讲一个 iOS 的小故事，iOS1.x 版本最初的代号是 Alpine，这是 i 系列设备的默认 root 密码。但最后发布的版本代号是 Heavenly，因为这个版本的操作系统拥有完整的调试符号、未加密还容易反汇编，很多越狱者都依赖从这个版本中提取的符号和函数调用关系寻找破解灵感，从越狱者角度来看确实如天堂般美好。

## Darwin 的内部组成

Darwin 是一个类 UNIX 的操作系统核心，它的组成可以近似看做：Darwin = kernel + XNU + 运行时。macOS 从Leopard(10.5) 开始已经是一个经过认证的 UNIX 实现。

XNU 是一个占据关键作用的 Darwin 核心，XNU = Mach + BSD + libkern + I/OKit。

初版的 XNU 是 NeXTSTEP 的核心，它包括 Mach 2.5 版本和 4.3 版本的 BSD。NeXTSTEP 合入苹果后，Mach被升级为 3.0，BSD 升级为 FreeBSD。

Mach 和 BSD 一个是微内核（Microkernel）一个是宏内核（Monolithic Kernel），所以 XNU 是一个混合架构（Hybrid kernel）。理解这几种内核的关键是需要注意内核模式和用户模式占据的范围。

![](https://cdn.zhangferry.com/Images/20220504000309.png)

#### Mach

Mach（微内核）由卡耐基梅隆大学开发，它的目标是取代 BSD 的 UNIX 核心。这个微内核仅能处理最基本的操作系统职责：

* 进程和线程抽象
* 虚拟内存管理
* 任务调度
* 进程间通信和消息传递机制

由上图可以看出微内核的功能本来就少，其他 OS 功能是作为基础服务建设在用户模式下的。因为这个特性其内部任务的调用会有更频繁的内核态/用户态上下文切换，这会额外消耗时间。同时内核与服务进程之间的消息传递也会降低运行效率，所以这种设计通常会降低性能。

但它也有优点，就是服务进程容易扩展，服务进程出问题不会危及到 kernel 。得益于这种扩展性 MachO 能支持多架构文件，以此为基础 macOS 能顺利的从 PowerPC 过渡到 Intel 再到 M1。

#### BSD

BSD（宏内核），它是 **B**erkeley **S**oftware **D**istribution （伯克利软件包）的缩写，这是一个派生自 Unix 的操作系统。BSD 是作为完善 Mach 的一个存在，它建立在 Mach 之上，并提供了一层更可靠更现代的 API。它主要包括这些：

* UNIX 进程模型
* POSIX 线程模型
* UNIX 用户和组
* 网络协议栈（BSD Socket API）

宏内核的特点是用户服务和内核服务都运行在同一内存空间，这还有效降低了内核态/用户态之间的频繁切换，执行效率会更高。但是宏内核也并非没有缺点，就是扩展性较差，另外如果内核有一个服务崩溃，整个操作系统就会崩溃。

### Darwin 架构

既然没有完美的内核模式，于是苹果就将两者混合，它同时兼顾微内核和宏内核各自的优点，这就是 Darwin了。

![](https://cdn.zhangferry.com/Images/20220504122023.png)

图片来自（Mac OS X And iOS Internals）

这里没有表示出 XNU，它的边界可以看做是 Kernel/User Transition 这里，其下包括 BSD 和 Mach 的层级就是 XNU。在 macOS 的体系里，Darwin 之上的层次基本都是不开源的，他们是 Apple 的私有财产。

XNU 中还有另外两种重要组件：

* libkern：这是一个内建的 C++ 库，用于支持 C++ 运行时。有了它内核的很多高级功能都可以使用 C++ 编写。
* I/OKit：这是一个设备驱动框架，凭借 libkern 提供的底层支持，驱动程序可以使用 C++ 实现。借助于 C++ 的面向对象特性，外部在创建驱动程序时会节省很多成本。

## Darwin 的开源之路

既然 Darwin 开源了，那为什么没有出现非 Apple 系的 Darwin 发行版操作系统呢？虽说开源，但 XNU 主要依赖的 Mach 和 BSD 本来就是开源的；Apple 还把对 ARMv7/8 的支持单独闭源；原本来源的 launchd，在 Mac OS 10.10 的版本之后也变成闭源项目合入到 libxpc 项目里了。这还不算，Darwin 的开源版本并没有剥离干净，里面还包含了一些 Apple 的私有 API，导致其并不能完整编译，还需要做一些额外改造。

围绕 Darwin 有两个重要的开源版本，OpenDarwin 和 [PureDarwin](http://www.puredarwin.org/ "PureDarwin") ，可以看下他们当前的发展状况。

### OpenDarwin

它由 Apple 牵头于 2002 年 4 月成立，其目标是加强苹果开发人员与自由软件社区之间的协作且将 Darwin 发展出另一独立版本。理想情况是苹果可以将 OpenDarwin 中的改进应用到 Darwin 中，而开源设计又可以完全控制该系统，将其用于 GNU-Darwin 等自由软件的发行版中。然而仅仅过了 4 年，OpenDarwin 就宣布关闭。以下是 OpenDarwin 项目组的[陈述](https://web.archive.org/web/20060804104416/http://opendarwin.org/ "OpenDarwin Shutting Down")：

> Over the past few years, OpenDarwin has become a mere hosting facility for Mac OS X related projects. The original notions of developing the Mac OS X and Darwin sources has not panned out. Availability of sources, interaction with Apple representatives, difficulty building and tracking sources, and a lack of interest from the community have all contributed to this. Administering a system to host other people's projects is not what the remaining OpenDarwin contributors had signed up for and have been doing this thankless task far longer than they expected. It is time for OpenDarwin to go dark.

主要因素有两个：

* 苹果的 macOS X 对 OpenDarwin 掌控过强，未推进 OpenDarwin 的独立发展
* 开源社区的兴趣减淡。也可以说是前者导致了后者

现在 OpenDarwin 的官网 http://opendarwin.org/ 仅剩一行字：Opendarwin memorial page。

### PureDarwin

PureDarwin 通常被认为是 OpenDarwin 的继承者。它的代码托管在 [Github](https://github.com/PureDarwin/PureDarwin "Github - PureDarwin")上，且仍在维护。Pure 的含义是更纯净，PureDarwin 仅使用苹果为 Darwin 发布的组件而不用 macOS 的其他组件。它的目标是通过提供文档，使开放源码爱好者和开发人员能够检索、理解、修改、构建和分发 Darwin，从而使Darwin 更易于使用。

因为缺少官方的支持，它当前在 Github 上的 star 数仅有 1.7k，由此可见它的关注度和发展都不算太好。但是当有人问为什么要花费时间维护 PureDarwin 时，他们的答案是：

> For learning and for fun.

简短却让人振奋，与此同时还有那么一丝丝凄凉。

所以回归上面的问题为什么开源的 Darwin 没有发展起来，因为它是为 macOS 创建的操作系统，它依赖于 macOS 的特性，也依赖于 Apple 的支持，脱离这两者尝试走「 Pure」Darwin 开源路线是非常困难的。

### Hackintosh

OpenDarwin 和 PureDarwin 的发展仍带来了一些有益的事情，其基于开源的 Darwin 制作成一个可以完整引导并且安装的 ISO 镜像。之后 OSX86（一个致力于把苹果电脑出品的 macOS 操作系统移植到非苹果电脑上的计划）项目在此基础上继续发扬光大，努力将 macOS 完整移植到 PC、笔记本等设备，该行为被称为 Hackintosh，也叫黑苹果。

通常的黑苹果方案是借助于引导程序实现的，因为它不会修改 macOS 源文件，被称为最佳的合法途径。苹果曾经开源过 Boot-132，一个用于加载 XNU 内核的引导程序。Voodoo 团队基于该程序开发出 Chameleon（变色龙）引导程序，再后来 Clover 出现，可以让不支持 EFI 的电脑进入模拟的 EFI 环境。现在又有了 OpenCore，它在配置文件时比较复杂，但因其受到较多 kexts 作者的兼容和本身的易用性而得到相当数目使用者的追捧。

关于合规的问题，虽然引导的方式没有修改 macOS 的源码，但苹果的最终用户许可证协议（EULA）里并不允许将 macOS 安装在一台没有苹果商标的硬体上。苹果曾起诉并多起黑苹果相关的商业行为并获得胜诉，对于非盈利的个人 Hackintosh 行为，苹果并没有过多理睬。

## 吉祥物的故事

人们热衷于为受欢迎的操作系统或者框架设置吉祥物，Linux 的吉祥物是一只企鹅（名叫 Tux，Torvalds UniX的缩写）、安卓的吉祥物是一只绿色小机器人（无正式名称，被开发人员称为 Bugdroid）。再看下跟 macOS 相关的两个操作系统的吉祥物。

### BSD

BSD 的吉祥物是一只小恶魔😈，叫做 [Beastie](https://zh.wikipedia.org/wiki/BSD%E5%B0%8F%E6%83%A1%E9%AD%94 "BSD 小恶魔")，它的发音跟 BSD 很像。它通常带支三叉戟，代表行程的分岔。

![](https://cdn.zhangferry.com/Images/20220504083150.png)

### Darwin

Darwin 的吉祥物是 [Hexley](http://www.hexley.com/ "Hexley")，它是一个卡通的鸭嘴兽，戴着 BSD 小恶魔的帽子，也拿着三叉戟。Hexley 是由 Jon Hooper 所设计的，版权也为他所有。但 Hexley 并不附属于 苹果电脑。本来这个吉祥物的名称应该是 Huxley，源由是捍卫[达尔文](https://baike.baidu.com/item/达尔文/6914335)(Darwin)进化理论的英国生物学家 Thomas Henry Huxley，而原先提议的人误以为是达尔文的助理，并错用了 Hexley。而发现错误时，要改名已经太晚，因此沿用了 Hexley 这个名称。

这个形象并不属于 Apple，而属于开源社区，所以开源版本的 Darwin 均有该图案的展示。

![](https://cdn.zhangferry.com/Images/20220504083800.png)

「*OS Internal 三部曲」的书籍封面就是用的 Hexley 形象。

## 未来展望

对于 macOS 未来的展望这部分内容摘自《Mac OS X And iOS Internals》（注意其完成时间是 2012 年），站在 10 年后的今天我们可以再去看下这几个预测的实现情况。

### 根除 Mach

内核中的 Mach API 是 NeXTSTEP 时代的产物，运行速度慢，执行效率上很难赶得上 BSD。而且 XNU 本身更趋向于宏内核架构，如果移除 Mach 将内核建设为完整的 BSD，将会有很大收益，但这确实需要巨大的工作量。

该想法并没有达成，且 Apple 根本没有这么做的打算，混合内核并没有看上去那么遭，Mach 将在很长一段时间继续存在着。

### 兼容 ELF 格式

macOS 无法融入 UN*X 的世界最大的一个困难就是坚持使用 Mach-O 二进制格式。当然这个想法也需要依赖上一步的根除 Mach，这样 Linux、BSD 中的程序就可以不经修改直接迁移到 macOS 上了。

这是很美好的想象，考虑 Apple 对 Hackintosh 的打压，其商业策略是独占、完全掌控而非扩大市场占有率。

### 使用 ZFS

macOS 早期使用的文件系统是 HFS+，但该文件系统遭受过大量批评 Linus 曾这样评价 HFS+：

> Quite frankly, HFS+ is probably the worst filesystem ever. Christ what shit it is.

HFS+ 确实有很多不完善的地方，它大小写不敏感、不支持对数据内容进行 checksum 校验、timestamp 只支持到秒级。彼时 Sun 公司开发出 ZFS，号称是「宇宙无敌最强」文件系统，有传闻 Apple 将使用这一文件系统，但后来 Sun 被 Oracle 收购，这一想法最终无法实现。

2017 年， 伴随着 Mac OS High Sierra 版本，Apple 正式发布了 Apple File System（APFS）。该文件系统是 Apple 从零开发的，耗时三年，对于完整的文件系统来说，这个效率已经非常高了。其支持更多的功能，且宣称针对 SSD 做了很多优化。但让人遗憾的是 APFS 在多个方面的性能还[没有超过 HFS+](https://zhuanlan.zhihu.com/p/33656976 "谈谈 Mac OS 的文件系统")。

### 和 iOS 合并

在 macOS 和 iOS 的发展过程中，有不少功能都是在一个平台成熟之后移植到另一个平台上的。即使在 M1 芯片出现之前，这一想法也是有可能的，Apple 在很早之前就实现过硬件架构翻译机制 -- Rosetta。

当 M1 芯片发布之后，macOS 和 iOS 都已经可以运行在 arm64 架构的芯片上了，这个想法似乎顺其自然要实现了。但现实并非如此，相对于统一，Apple 更想要的是各司其职，每个产品线 macOS、iPadOS、iOS 都有其各自适用的场景，Apple 也极力往这方面宣传，这有助于产品的销售。

## 总结

再次列出开头提到的几个问题便于大家回顾这篇文章的内容：

1、我们在说 MacOS 时通常会带上「X」，将其叫做 MacOS X 或者 OS X，这是为什么呢？「X」 有什么含义？

2、Darwin、XNU、Mach、BSD 分别代表什么，之间又有什么关系？

3、Mac OS 与 Unix 是什么关系？

4、Apple 开源了 Darwin，对应的开源社区为什么发展不起来？

