# iOS摸鱼周报 第四十期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * Tips：
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：从本期开始我们换了新的封面。

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)

## 面试解析

整理编辑：[zhangferry](https://zhangferry.com)

### dyld 2 和 dyld 3 有哪些区别

dyld 是动态加载器，它主要用于动态库的链接和程序启动加载工作，它目前有两个主要版本：dyld 2 和 dyld 3。

**dyld 2**

[dyld2 ](https://github.com/opensource-apple/dyld/tree/master/src "dyld开源地址")从 iOS 3.1开始引入，一直到 iOS12 被 dyld 3 全面代替。它经过了很多次版本迭代，我们现在常见的特性比如 ASLR，Code Sign，Shared Cache等技术，都是在 dyld 2 中引入的。dyld 2 的执行流程是这样的：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220104235847.png)

- 解析`mach-o`头文件，找到依赖库，依赖库又可能有别的依赖，这里会进行递归分析，直到获得所有 dylib 的完整图。这里数据庞大，需要进行大量的处理；
- 映射所有`mach-o`文件，将它们放入地址空间；
- 执行符号查找，若你的程序使用 `printf` 函数，将会查找`printf`是否在库系统中，然后我们找到它的地址，将它复制到你的程序中的函数指针上；
- 进行 bind 和 rebase，修复内部和外部指针；
- 运行一些初始化任务，像是 加载 category、load 方法等；
- 执行main；

**dyld 3**

dyld 3 在 2017 年就被引入至 iOS 11，当时主要用来优化系统库。现在，在 iOS 13 中它也将用于启动第三方APP，完全替代 dyld 2。

dyld 3 最大的特点就是引入了启动闭包，闭包里包含了启动所需要的缓存信息，而且这个闭包在进程外就完成了。在打开 APP 时，实际上已经有不少工作都完成了，这会使 dyld 的执行更快。

最重要的特性就是启动闭包，闭包里包含了启动所需要的缓存信息，从而提高启动速度。下图是 dyld 2 和 dyld 3 的执行步骤对比：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220105001119.png)

dyld 3 的执行步骤分两大步，以图中虚线隔开，虚线以上进程外执行，以下进程创建时执行：

* 前 3 步查找依赖和符号相对耗时，且涉及一些安全问题，所以将这些信息做成缓存闭包写入磁盘里，对应地址：`tmp/com.apple.dyld`。闭包会在重启手机/更新/下载 App 的首启等时机创建。

* 进程启动时，读取闭包并验证闭包有效性。

* 后面步骤同 dyld 2 

[iOS 13中dyld 3的改进和优化](https://easeapi.com/blog/blog/83-ios13-dyld3.html)

[iOS dyld 前世今生](https://www.yotrolz.com/posts/c2aae680/)

### 编译流程

一般的编译器架构，比如 LLVM 采用的都是三段式，也即从源码到机器码需要经过三个步骤：

前端 Frontend -> 优化器 Optimizer -> 后端 Backend

这么设计的好处就是将编译职责进行分离，当新增语言或者新增CPU架构是只需修改前端和后端就行了。

其中前端受语言影响，Objective-C 和 Swift 对应的前端分别是 clang 和 swiftc。下图整理了两种语言的编译流程：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/ios_compiler.png)

#### 前端

编译前端做的工作主要是：

1、词法分析：将源码进行分割，生成一系列记号（token）。

2、语法分析：扫描上一步生成的记号生成语法树，该分析过程采用上下文无关的语法分析手段。

3、语义分析：语义分析分为静态语义分析和动态语义分析两种，编译期间确认的都是静态语义分析，动态语义需运行时期间才能确定。该步骤包括类型匹配和类型转换，会确认语法树中各表达式的类型。

之后导出 IR 中间件供优化器使用。这一步 Swift 会比 Objc 多几个步骤，其中一个是 ClangImporter，这一步用于兼容 OC。它会导入 Clang Module，把 Objc 或者 C 的API 映射为 Swift API，导出结果能够被语义分析器使用。

另外一个不同是 Swift 会有几个 SIL 相关的步骤（蓝色标注），SIL 是 Swift Intermediate Language 的缩写，意为 Swift 中间语言，它不同于 IR，而是特定于 Swift 的中间语言，适合用于对 Swift 源码进行分析和优化。它这里又分三个步骤：

1、生成原始的 SIL

2、进行一些数据流诊断，转成标准 SIL

3、做一些特定于 Swift 的优化，包括 ARC、泛型等

#### 优化器

编译前端会生成统一的 IR (Intermediate Representation)文件传入到优化器，它是一种强类型的精简指令及，对目标指令进行了抽象。Xcode 中的Optimization Level 的几个优化等级，: `-O0` , `-O1` , `-O2` , `-O3` , `-Os`，即是这个步骤处理的。

如果开启了 Bitcode，还会转成 Bitcode 格式，它是 IR 的二进制形式。

#### 后端

这个步骤相对简单会根据不同的 CPU 架构生成汇编和目标文件。

[Swift.org - Swift Compiler](https://www.swift.org/swift-compiler/#compiler-architecture "Swift.org - Swift Compiler")

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

1、[iOS包依赖管理工具](https://juejin.cn/post/6932739864613879821 "iOS包依赖管理工具") -- 来自掘金：小小青叶

[@东坡肘子](https://www.fatbobman.com/)：本系列一共六篇文章，不仅从原理、使用、创建自定义库等方面，对 CocoaPods 和 Swift Package Manager 进行了介绍，并且对两种包管理工具进行了比较。

2、[CocoaPods Podspec 解析原理](http://chuquan.me/2022/01/03/podspec-analyze-principle/ "CocoaPods Podspec 解析原理") -- 来自楚权的世界：楚权

[@东坡肘子](https://www.fatbobman.com/)：在 CocoaPods 中，podspec 文件主要用于描述一个 pod 库的基本信息，包括：名称、版本、源、依赖等等。本文介绍了如何通过 DSL 方法将配置的属性保存在一个对象的哈希表中，通过构建一棵保存所有配置信息的树从而建立相互之间的依赖关系。

3、[关于 Swift Package Manager 的一些经验分享](https://juejin.cn/post/7007987863954391054 "关于 Swift Package Manager 的一些经验分享") -- 来自：字节跳动技术团队

[@东坡肘子](https://www.fatbobman.com/)：Swift Package Manager 是 Apple 为了弥补当前 iOS 开发中缺少官方组件库管理工具的产物。相较于其他组件管理控件，他的定义文件更加轻松易懂，使用起来也很 Magic，只需将源码放入对应的文件夹内，Xcode 就会自动生成工程文件，并生成编译目标产物所需要的相关配置。同时，SPM 与 Cocoapods 相互兼容，可以在特性上提供互补。本文除了介绍 Swift Package Manager 的现状、常见使用方法外，还阐述了作者对于 SPM 未来的一些思考。

4、[解决swift package manager fetch慢的问题](https://juejin.cn/post/7007987863954391054 "解决swift package manager fetch慢的问题") -- 来自简书：chocoford

[@东坡肘子](https://www.fatbobman.com/)：由于网络的某些限制，在 Xcode 中直接 fetch Github 上的 SPM 库并不容易。本文中给出了几种提高 fetch 成功率的解决方案。（编辑特别提示：Xcode 程序包中内置了终端、命令行工具等应用，任何在系统终端下的代理设定对其都不会产生作用。使用 SS + Proxifier 的方式可以实现让 Xcode 中的网络数据从指定代理通过）

5、[Swift Package Manager 添加资源文件](https://juejin.cn/post/6854573220784242702 "Swift Package Manager 添加资源文件") -- 来自掘金：moxacist

[@东坡肘子](https://www.fatbobman.com/)：从  swift-tool-version 5.3 版本开始，Swift Package Manager 提供了在包中添加资源文件的能力。本文是 WWDC 2020 —— 【Swift 软件包资源和本地化】 专题演讲的中文整理。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第三十九期](https://mp.weixin.qq.com/s/DolkTjL6d-KkvFftd2RLUQ)

[iOS摸鱼周报 第三十八期](https://mp.weixin.qq.com/s/a1aOOn1sFh5EaxISz5tAxA)

[iOS摸鱼周报 第三十七期](https://mp.weixin.qq.com/s/PwZ2nIHRo0GDsjMx7lSFLg)

[iOS摸鱼周报 第三十六期](https://mp.weixin.qq.com/s/K_JHs1EoEn222huWIoJRmA)

[iOS摸鱼周报 第三十五期](https://mp.weixin.qq.com/s/fCEbYkAPlK0nm7UtLKFx5A)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
