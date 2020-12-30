# iOS摸鱼周报 第二期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享大家开发过程遇到的经验教训及学习内容。成立的目的一个是开发知识碎片化，需要有一个地方去总结并用于回顾；另一个是为了提醒自己不断学习，内卷日益严重的开发环境下，不进则退。

虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug遭遇。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips

开发小技巧收录。

## 那些bug



## 编程概念

### 什么是Clang

![image.png](https://cdn.nlark.com/yuque/0/2020/png/2215058/1605605435472-f4f3bd90-9332-4eac-b8f0-f042248555c1.png?x-oss-process=image%2Fresize%2Cw_300)

Clang 是一个C、C++、Objective-C和Objective-C++编程语言的编译器前端。它的目标是提供一个GNU编译器套装（GCC）的替代品，支持了GNU编译器大多数的编译设置以及非官方语言的扩展。作者是克里斯·拉特纳（Chris Lattner）。

clang项目包括clang前端和clang静态分析器。编译器前端的含义是clang不能直接将源码编译成机器码，clange能输出源码的抽象语法树，并将代码编译成LLVM bitcode。

Clang本身性能优异，其生成的AST所耗用掉的内存仅仅是GCC的20%左右，Clang编译Objective-C代码时速度为GCC的3倍，还能针对用户发生的编译错误准确地给出建议。

### 什么是LLVM

LLVM（Low Level Virtual Machine）是一个自由软件项目，它是一种编译器基础设施，以C++写成，包含一系列模块化的编译器组件和工具链，用来开发编译器前端和后端。它是为了任意一种编程语言而写成的程序，利用虚拟技术创造出编译时期、链接时期、运行时期以及“闲置时期”的最优化。

LLVM有两层含义，广义的LLVM是指一个完整的编译器架构，包括前端、后端、优化器等。

狭义的LLVM仅指编译器后端功能的一些列模块和库，由Clange编译出的中间件经过LLVM后端处理变成对应机器码。

![img](https://cdn.nlark.com/yuque/0/2020/png/2215058/1605605278765-f1534ab7-af3d-4f43-b871-d7cf1b70497c.png?x-oss-process=image%2Fresize%2Cw_515)

### 什么是ld

链接器（Linker）是一个程序，它可以将一个或多个由编译器或汇编器生成的目标文件外加库链接为一个可执行文件。

ld是GNU的链接器，llvm4中有了自己的链接器lld，但是lld在macOS上运行还有问题 (http://lists.llvm.org/pipermail/cfe-dev/2019-March/061666.html)，所以当前xcode使用的链接器仍是ld。

Build Setting里的Other Linker Flags就是制定ld命令的参数。

在xcode中，它有三个常用的参数：

`-Objc`:链接器就会把静态库中所有的 Objective-C Class 和 Category 都加载到最后的可执行文件中

`-all_load`:会让链接器把所有找到的目标文件都加载到可执行文件中，但有可能会遇到duplicate symbol错误

`-fore_load`:需要指定加载库文件的路径，然后将目标文件全部加载到可执行文件中。

### 什么是dyld

通常说的动态库是指共享库，即可以被多个应用共用。动态库只会在系统中内置一份，应用端加入引用会在启动时由dyld链接。系统动态库还会被缓存起来，第二次使用该动态库的应用会比第一次使用的加载速度更快。

在iOS中动态库的格式为framework、dylib或者tbd。Linux（安卓）里的动态库为so，windows中的动态库为dll。

通常大家说的，只有系统库才是动态的，开发者创建的都是静态库，这种说法其实是不严谨的。Xcode允许开发者创建framework，并且提供了动态和静态的选择，但这里的动态是受限制的，通常叫做伪动态。自建的动态库仅可在主应用和Extension之间共享，无法在APP之间共享。

### 什么是bitcode

bitcode是编译后的程序的中间表现，在xcode中bitcode对应的是一个配置，意为是否开启bitcode。

包含bitcode并上传到App Store Connect的Apps会在App Store Connect上编译和链接。包含bitcode可以在不提交新版本App的情况下，允许Apple在将来的时候再次优化你的App 二进制文件。 对于iOS Apps，Enable bitcode 默认为YES，是可选的（可以改为NO）。对于WatchOS和tvOS，bitcode是强制的。如果你的App支持bitcode，App Bundle（项目中所有的target）中的所有的Apps和frameworks都需要包含bitcode。

苹果推荐iOS项目开启bitcode，且强制watchOS必须开启bitcode。

因为包含bitcode的项目会在App Store Connect重新编译，所以其符号表文件依赖编译后的结果，这时就需要从app store connect下载对应dSYM文件。

## 优秀博客



## 学习资料



## 开发利器

推荐好用的开发工具。

**A Companion for SwiftUI**

作者的 [SwiftUI 实验室](https://swiftui-lab.com)

A Companion for SwiftUI 是一款可以记录 iOS 和 macOS 平台的 SwiftUI 视图，形状，协议，场景和属性包装的应用程序。该应用程序还包含每种方法的示例，其中有许多都是交互式的，并且嵌入在应用程序中运行。通过使用关联的控件，你可以看到它们对视图的直接影响，以及如何修改你的代码以产生这样的效果。

下载地址：[Mac App Store](https://apps.apple.com/cn/app/a-companion-for-swiftui/id1485436674?mt=12)

![A Companion for SwiftUI](https://raw.githubusercontent.com/AlleniCode/MyPics/main/BlogPics/A%20Companion%20SwiftUI.png)



