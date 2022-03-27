# iOS摸鱼周报 第十三期

![](http://cdn.zhangferry.com/Images/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 开发Tips

整理编辑：[人魔七七](https://github.com/renmoqiqi)

### CocoaPods 常见操作

#### pod install

当我们的工程首次使用 Cocoapods 管理第三方库的时候或者当我们每次编辑 Podfile 文件的时候比如：添加，删除或者编辑一个 pod 库的时候，都需要执行该命令。

* 首次执行 `pod install` 命令，会下载安装新的 pod，并把每个 pod 的版本写到 Podfile.lock 文件里。这个文件跟踪所有的 pod 库及其依赖的版本并锁定他们的版本号。
* 在存在 Podfile.lock 的情况下执行 `pod install` 的时候，只解析 Podfile.lock 中没有列出的pod依赖项。1. 对于Podfile.lock 列出的版本，不需要检查 pods 是否有更新直接使用既有的版本安装。2. 对于Podfile.lock 未列出的版本，会根据Podfile 描述的版本安装。

Podfile 文件是 pod 执行的核心文件，它的解析逻辑推荐看这篇：[Podfile 的解析逻辑](https://www.desgard.com/2020/09/16/cocoapods-story-4.html "Podfile 的解析逻辑")。

#### pod update

pod update 可以全局升级，也可以指定 podName 单个升级。当我们执行 `pod update podName` 的时候，会忽略 Podfile.lock 文件的版本，根据 Podfile 的定义尽可能更新到最新的版本，并更新 Podfile.lock 文件。该命令会同样适配于 pod 库 podspec文件内部定义的依赖。 可以通过`pod outdated` 检测出过期的依赖版本和可升级版本。

对于 install 和 update 有两个常用参数：

* --repo-update：该参数会更新所有的 repo，例如该更新了一个私有库版本，直接 install 是找不到对应版本的，我们不想更新所有的依赖库，只想更新 对应的 repo，就可以使用该指令。该参数还对应一个特有命令：`pod repo update`。
* --no-repo-update：update 操作会默认更新所有 repo，有时这并不是必须的，且该步骤会同步 pod 公有 repo，导致比较耗时，这时就可以增加该参数，用于关闭该更新操作。

### CocoaPods 使用建议

* 推荐使用 Gemfile 管理 pod 版本，每次执行 pod 通过 bundle 进行，例如： `bundle exec pod install` 。

* 工程持有管理者对项目进行 CocoaPods 初始化的时候会有一个 Podfile.lock 这个文件我们需要纳入版本控制里。

* 如果需要更新某个库到某一个版本，由项目持有管理者采用 `pod update podName` 的方式更新某个库到一定的版本。然后提交 Podfile.lock 和 Podfile 文件。


## 那些Bug

整理编辑：[zhangferry](https://zhangferry.com)

### module compiled with Swift 5.3.2 cannot be imported by the Swift 5.3 compiler: **.swiftmodule

**问题背景**

通过某个版本的 Xcode 生成的 Swift 库（Framework），在另一台机器（不同版本 Xcode）无法识别，报上述错误。

**问题分析**

该错误是由于编译器不兼容导致的，错误含义是由 Swift 5.3.2 编译器（编译器版本可以通过 `swift --version`查看）编译的module，特指 `swiftmodule` 文件，无法被 Swift 5.3 的编译器所识别。`swiftmodule`文件用于描述Swift内部的方法声明，它是二进制格式的，会根据不同的架构生成不同的版本。但也正因为其二进制格式的特性，无法跟随编译器的升级进行调整。这个问题对应的就是 ABI 稳定中的 module stability。这里引用喵神的一段[博客](https://onevcat.com/2019/02/swift-abi/ "Swift ABI 稳定对我们到底意味着什么")内容：

> ABI 稳定是使用 binary 发布框架的必要非充分条件。框架的 binary 在不同的 runtime 是兼容了，但是作为框架，现在是依靠一个 `.swiftmodule` 的二进制文件来描述 API Interface 的，这个二进制文件中包含了序列化后的 AST (更准确说，是 interface 的 SIL)，以及编译这个 module 时的平台环境 (Swift 编译器版本等)。
>
> ABI 稳定并不意味着编译工具链的稳定，对于框架来说，想要用 binary 的方式提供框架，除了 binary 本身稳定以外，还需要描述 binary 的方式 (也就是现在的 swiftmodule) 也稳定，而这正在开发中。将来，Swift 将为 module 提供文本形式的 `.swiftinterface` 作为框架 API 描述，然后让未来的编译器根据这个描述去“编译”出对应的 `.swiftmodule` 作为缓存并使用。
>
> 这一目标被称为 module stability，当达到 module stability 后，你就可以使用 binary 来发布框架了。

**问题解决**

上面说的 module stability 已经实现了，就是可以通过 `.swiftinterface` 文件描述二进制包。它的实现对应一个编译参数`-enable-library-evolution`，在 Build Setting 里就是 `Build Libraries for Distribution`，我们将其设置为 YES ，生成的 Framework 里就会包含对应的 `.swiftinterface` 文件，就能实现不同版本编译器之间的兼容问题。

但到这里还没完全结束，遇到了另一个问题：

```
/*.framework/Modules/*.swiftmodule/arm64-apple-ios.swiftinterface:5:8: cannot load underlying module for 'SnapKit'

failed to build module '*' from its module interface; the compiler that produced it, 'Apple Swift version 5.3.2 (swiftlang-1200.0.45 clang-1200.0.32.28)', may have used features that aren't supported by this compiler, 'Apple Swift version 5.3 (swiftlang-1200.0.29.2 clang-1200.0.30.1)
```

按理说有了 `swiftinterface` 应该不会出现编译不兼容问题了，但还是出现了，虽然提示内容有些不太一样，这里会多出一个内部依赖库的问题。这里查看对应版本的 `swiftinterface` 文件：

```
// swift-interface-format-version: 1.0
// swift-compiler-version: Apple Swift version 5.3.2 (swiftlang-1200.0.45 clang-1200.0.32.28)
// swift-module-flags: -target arm64-apple-ios10.0 -enable-objc-interop -enable-library-evolution -swift-version 5 -enforce-exclusivity=checked -Onone -module-name ZYModule
import Foundation
import SnapKit
import Swift
import UIKit
```

这里除了声明编译器信息外，还把依赖库 SnapKit 也写入了进去，所以这里猜测的隐含逻辑就是二进制库做了 `Build Libraries for Distribution` ，其依赖的其他库也绑定了对应的编译器版本信息，在工程里使用源码编译的 SnapKit 对于了其当前编译版本（5.3），与二进制库所生成的版本（5.3.2）不一致，所以才导致了该问题。我尝试修改项目里 Pod库 的 `Build Libraries for Distribution` 选项：

```ruby
post_install do |installer|
  installer.pods_project.targets.each do |target|
   target.build_configurations.each do |config|
    config.build_settings['BUILD_LIBRARY_FOR_DISTRIBUTION'] = 'YES'
   end
  end
end
```

问题得到解决，编译通过！

## 编程概念

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)


### 什么是 BIOS

BIOS 全称为 Basic Input Output System，即基本输入输出系统。BIOS 是预先内置在计算机主机内部的程序，也是计算机开机后加载的第一个程序。BIOS 保存着计算机最重要的基本输入输出的程序、开机后自检程序和系统自启动程序，它可从 CMOS（是电脑主板上的一块可读写的 RAM 芯片）中读写系统设置的具体信息。

BIOS 除了键盘，磁盘，显卡等基本控制程序外，还有`引导程序`的功能。引导程序是存储在启动驱动器起始区域的小程序，操作系统的启动驱动器一般是硬盘。不过有时也可能是 CD-ROM 或软盘。

电脑开机后，BIOS 会确认硬件是否正常运行，没有异常的话就会直接启动引导程序，引导程序的功能就是把在硬盘等记录的 OS 加载到内存中运行，虽然启动应用是 OS 的功能，但 OS 不可以自己启动自己，而是通过引导程序来启动。

制作黑苹果的时候安装的 Clover 就是一个启动程序，它通过修改 BIOS 配置，让 BIOS 首先执行它，然后由它来引导至 MacOS 的启动。

![](http://cdn.zhangferry.com/Images/20210527232231.png)

严格意义来说 BIOS 是 IBM PC架构上的一种设计规范，Mac电脑，包括一些新型的主板都没有 BIOS 这一概念，取而代之的是 EFI/UEFI。


### 什么是汇编

汇编语言（Assembly Language）是任何一种用于电子计算机、微处理器、微控制器或其他可编程器件的低级语言，亦称为符号语言。在汇编语言中，用助记符代替机器指令的操作码，用地址符号或标号代替指令或操作数的地址。在不同的设备中，汇编语言对应着不同的机器语言指令集，通过汇编过程转换成机器指令。特定的汇编语言和特定的机器语言指令集是一一对应的，不同平台之间不可直接移植。

汇编语言比机器语言的可读性要好，但跟高级语言比较而言，可读性还是较差。不过采用它编写的程序具有存储空间占用少、执行速度快的特点，这些是高级语言所无法取代的。在实际应用中，是否使用汇编语言，取决于具体应用要求、开发时间和质量等方面作权衡。汇编常用的指令如下：

| 操作码 | 操作数 | 功能                          |
| ------ | ------ | ----------------------------- |
| mov    | A, B   | 把B的值赋给A                  |
| and    | A, B   | 把A和B同时相加，并把结果赋给A |
| push   | A      | 把A的值存储在栈中             |
| pop    | A      | 从栈中读出值，并将其赋值给A   |
| call   | A      | 调用函数A                     |
| ret    | 无     | 处理返回给调用源函数          |


### 什么是虚拟机

虚拟机（Virtual Machine）是指通过软件模拟的具有完整硬件系统功能的、运行在一个完全隔离环境中的完整计算机系统。在实体计算机中能够完成的工作在虚拟机中都能够实现。在计算机中创建虚拟机时，需要将实体机的部分硬盘和内存容量作为虚拟机的硬盘和内存容量。每个虚拟机都有独立的 CMOS、硬盘和操作系统，可以像使用实体机一样对虚拟机进行操作。

虚拟机的主要用处有：

1. 演示环境，可以安装各种演示环境，便于做各种例子
2. 保证主机的快速运行，减少不必要的垃圾安装程序，偶尔使用的程序，或者测试用的程序在虚拟机上运行
3. 避免每次重新安装，银行等常用工具，不经常使用，而且要求保密比较好的，单独在一个环境下面运行
4. 想测试一下不熟悉或者有风险的应用，在虚拟机中随便安装和彻底删除
5. 体验不同版本的操作系统，如 Linux、Mac 等。

虚拟机目前可分为三类：

* 系统虚拟机，例如：VMware
* 程序虚拟机，例如：JVM（Java Virtual Machine）
* 操作系统层虚拟化，例如：Docker


### 什么是外围中断

IRQ（Interrupt Request）代表的就是中断请求。IRQ 是用来暂停当前正在运行的程序，并跳转到其他程序运行的必要机制。该机制被称为处理中断。中断处理在硬件控制中担当着重要的角色。因为如果没有中断处理，就有可能无法顺畅进行处理的情况。

从中断处理开始到请求中断的程序（中断处理程序）运行结束之前，被中断的程序（主程序）的处理是停止的。这种情况就类似于在处理文档的过程中有电话打进来，电话就相当于是中断处理。假如没有中断处理的发生，就必须等到文档处理完成后才能够接听电话。由此可见，中断处理有着巨大的价值，就像是接听完电话后会返回原来的文档作业一样，中断程序处理完成后，也会返回到主程序中继续。

![中断请求示意图](http://cdn.zhangferry.com/Images/20210526233248.png)

**实施中断请求的是连接外围设备的 I/O 控制器，负责实施中断处理的是 CPU。**

假如有多个外围设备进行中断请求的话， CPU 需要做出选择进行处理，为此，我们可以在 I/O 控制器和 CPU 中间加入名为中断控制器的 IC 来进行缓冲。中断控制器会把从多个外围设备发出的中断请求有序的传递给 CPU。中断控制器的功能相当于就是缓冲。下面是中断控制器功能的示意图

![中断控制器的功能](http://cdn.zhangferry.com/Images/20210526233322.png)


### 什么是 DMA

DMA 全称为 Direct Memory Access，即直接存储器访问。DMA 是一种内存访问机制，它是指在不通过 CPU 的情况下，外围设备直接和主存进行数据传输。磁盘等硬件设备都用到了 DMA 机制，通过 DMA，大量数据就可以在短时间内实现传输，之所以这么快，是因为 CPU 作为中介的时间被节省了，下面是 DMA 的传输过程


![使用 DMA 的外部设备和不使用 DMA 的外部设备](http://cdn.zhangferry.com/Images/20210527220519.png)


I/O 端口号、IRQ、DMA 通道可以说是识别外围设备的 3 点组合。不过，IRQ、DMA 通道并不是所有外围设备都具备的。计算机主机通过软件控制硬件时所需要的信息的最低限，是外围设备的 I/O 端口号。IRQ 只对需要中断处理的外围设备来说是必须的，DMA 通道则只对需要 DMA 机制的外围设备来说必须的。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)


本期博客汇总的主题是 `watchdog`

1、[iOS watchdog (看门狗机制)](https://www.jianshu.com/p/6cf4aeced795 "iOS watchdog (看门狗机制)") -- 来自简书：Mr_Xie


先来简单了解什么是 watchdog。

2、[iOS App 后台任务的坑](http://www.cocoachina.com/articles/27303 "iOS App 后台任务的坑") -- 来自cocoachina ：米米狗


后台任务泄漏是导致触发 watchdog 常见情况之一，还有一种情况就是主线程卡死，文章中有介绍如何区分。


3、[Addressing Watchdog Terminations](https://developer.apple.com/documentation/xcode/addressing-watchdog-terminations "Addressing Watchdog Terminations")


苹果的官方文档。对我个人而言，了解 scene-create 和 scene-update 的含义在排查问题过程中起到了一定的作用。


4、[你的 App 在 iOS 13 上被卡死了吗](https://zhuanlan.zhihu.com/p/99232749 "你的 App 在 iOS 13 上被卡死了吗")


进入实践阶段，其实我们很少真的在主线程做大量耗时操作如网络请求等。触发 watchdog 往往是不经意的，甚至你不会怀疑你的代码有任何问题。这篇文章介绍的是 58 同城团队如何定位到剪切板造成的启动卡死。


5、[iOS 稳定性问题治理：卡死崩溃监控原理及最佳实践](https://juejin.cn/post/6937091641656721438 "iOS 稳定性问题治理：卡死崩溃监控原理及最佳实践")


这篇文章是字节跳动 APM 团队早些时候发表的，是业界少有的公开介绍卡死崩溃的原因的文章，具有很强的借鉴意义。我们在做启动卡死优化的过程中，文中提到的相关问题基本都有遇到，只不过在此之前并不知道什么原因以及如何解决。所以说如果你想做卡死治理，可以参考下这篇文章。

6、[面试过 500+ 位候选人之后，想谈谈面试官视角的一些期待](https://mp.weixin.qq.com/s/kv-_oZObp7QRHeAbrkdfsA "面试过500+位候选人之后，想谈谈面试官视角的一些期待")

《iOS 稳定性问题治理：卡死崩溃监控原理及最佳实践》的作者在面试了 500+ 候选人后写的文章，有需要的同学可以针对性的做些准备。

7、[论证：iOS安全性，为什么需要审核？](https://juejin.cn/post/6967199105541996575 "论证：iOS安全性，为什么需要审核？")

[@iHTCboy](https://github.com/iHTCboy)：从辩论的视角分析 iOS 安全性，同时与 macOS 安全性进行对比，提出了让 iOS 更加安全的建议，文中同时也总结了非常多 iOS 和 macOS 安全技术小知识，可以让大家在短时间里快速入门和重温 Apple OS 安全性知识点。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 喵神预告：新书，开工！

[喵神](https://weibo.com/onevcat)关于 `async-swift` 的书开工了。是关于Swift5.5的新特性**协程**，待书籍完工的第一时间我们会通过周报再通知到大家。

![New Book! Go!](http://cdn.zhangferry.com/Images/11661621992188_.pic.jpg)

### 30 seconds of code

地址：https://www.30secondsofcode.org/

该网站的口号是：「能找到满足你所有开发需求的代码片段！」，他有许多语言的常用代码片段（Code Snippets），例如排序算法、hex 转 rgb、时间转换等等，能让你轻松地找到各个语言的这些常用代码，让你的开发效率大大提升！（可惜目前还没有 `Swift` 的板块🥲

![](http://cdn.zhangferry.com/Images/20210529183606.png)

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

### Whatpulse

**地址**：https://whatpulse.org/

**软件状态**：基础功能免费，高级功能付费

**使用介绍**

Whatpulse是一个电脑使用检测统计软件，它可以统计你每天的键盘、鼠标、网络等情况的使用详情并将其做成简单的统计表格，用于分析每天的电脑使用情况。

翻到一张之前公司电脑使用该软件将近一年的留存成果，100万+ 按键次数，使用最多的竟然是删除键。。

![](http://cdn.zhangferry.com/Images/20210529185605.png)

# OctoMouse

**地址**：https://konsomejona.github.io/OctoMouse/index.html

**软件状态**：免费，[开源](https://github.com/KonsomeJona/OctoMouse)

**使用介绍**

该软件主要用于统计键盘及鼠标的行为信息，比较有意思的是，它对鼠标的统计会包含移动距离参数。可以试试看多久才能让鼠标移动 5km。

![](http://cdn.zhangferry.com/Images/20210529191107.png)

## 联系我们

[iOS摸鱼周报 第八期](https://zhangferry.com/2021/04/11/iOSWeeklyLearning_8/)

[iOS摸鱼周报 第九期](https://zhangferry.com/2021/04/24/iOSWeeklyLearning_9/)

[iOS摸鱼周报 第十期](https://zhangferry.com/2021/05/05/iOSWeeklyLearning_10/)

[iOS摸鱼周报 第十一期](https://zhangferry.com/2021/05/16/iOSWeeklyLearning_11/)

[iOS摸鱼周报 第十二期](https://zhangferry.com/2021/05/22/iOSWeeklyLearning_12/)

![](http://cdn.zhangferry.com/Images/wechat_official.png)