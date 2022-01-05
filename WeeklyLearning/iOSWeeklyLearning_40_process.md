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

编译前端做的工作主要是词法分析、语法分析、语义分析，然后导出IR中间件供优化器使用。这一步 Swift 会比 Objc 多几个步骤，其中一个是 ClangImporter，这一步用于兼容 OC。它会导入 Clang Module，把 Objc 或者 C 的API 映射为 Swift API，导出结果能够被语义分析器使用。

另外一个不同是 Swift 会有几个 SIL 相关的步骤（蓝色标注），SIL 是 Swift Intermediate Language 的缩写，意为 Swift 中间语言，它不同于 IR，而是特定于 Swift 的中间语言，适合用于对 Swift 源码进行分析和优化。它这里又分三个步骤：

1、生成原始的 SIL

2、进行一些数据流诊断，转成标准 SIL

3、做一些特定于 Swift 的优化，包括 ARC、泛型等

#### 优化器

优化器接收 IR 中间件会做进一步的优化，如果开启了 Bitcode，还会转成 Bitcode格式。Bitcode 是 IR 的二进制形式。

#### 后端

经过汇编过程根据不同的 CPU 架构生成不同格式的目标文件。

[Swift.org - Swift Compiler](https://www.swift.org/swift-compiler/#compiler-architecture)

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
