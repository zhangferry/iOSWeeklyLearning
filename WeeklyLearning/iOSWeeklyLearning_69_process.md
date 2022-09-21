# iOS 摸鱼周报 #69 | 准备登陆灵动岛

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：使用 iOS 16.1 Beta 版和 Xcode 14.1 Beta 版，准备登陆灵动岛
> * 本周学习：了解符号 Symbol 
> * 内容推荐：Swift、SwiftUI 相关好文推荐
> * 摸一下鱼：

## 本期话题

### [使用 iOS 16.1 Beta 版和 Xcode 14.1 Beta 版，开发实时活动功能](https://developer.apple.com/cn/news/?id=ttuz9vwq "使用 iOS 16.1 Beta 版和 Xcode 14.1 Beta 版，开发实时活动功能")

[@远恒之义](https://github.com/eternaljust)：从 iOS 16.1 Beta 版和 Xcode 14.1 Beta 版开始，我们可以在灵动岛和锁定屏幕上共享应用程序的实时更新作为实时活动。借助于新 ActivityKit 框架的实时更新功能，实时活动能帮助用户跟踪 App 内容状态的变化。

灵动岛作为 iPhone 14 Pro 系列最惊艳的设计，App 的实时活动会显示在锁定屏幕和灵动岛中，可以让用户非常直观、愉悦地体验到实时更新的内容。实时活动功能和 ActivityKit 将在今年晚些时候 iOS 16.1 正式版中上线。

推荐观看 [Dynamic Island API - iOS 16.1 Beta - Xcode 14.1](https://www.youtube.com/watch?v=gEWvV-TmjqE&t=25s "Dynamic Island API - iOS 16.1 Beta - Xcode 14.1 - SwiftUI Tutorials") 课程介绍，开始登陆灵动岛。

![Kavsoft SwiftUI Tutorials](https://cdn.zhangferry.com/Images/dynamic-island-api.jpeg)

### [App 和 App 内购买项目即将实行价格和税率调整](https://developer.apple.com/cn/news/?id=e1b1hcmv "App 和 App 内购买项目即将实行价格和税率调整")

[@远恒之义](https://github.com/eternaljust)：最早于 2022 年 10 月 5 日起，智利、埃及、日本、马来西亚、巴基斯坦、波兰、韩国、瑞典、越南和所有使用欧元货币的地区的 App Store 上的 App 及 App 内购买项目 (自动续期订阅除外) 价格将有所提高。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### 符号 Symbol 了解

#### 符号定义

开发过程中经常遇到一类 error 提示： `Symbol not found:xxx`， 我们都知道这是存在未定义的类、变量、方法等。这里的  `Symbol`可以理解为一种数据结构，包含类型和名称等数据信息。对应一个类或者方法的地址。编译过程中不同文之间接就是靠 `Symbol`正确的拼合到一起的。它可以是方法定义、类型定义或者数据定义。二进制文件中会存在特定的区间用于存储符号，称为符号表，根据作用的不同分为符号表和间接符号表。

#### 符号的分类

符号可以简单的分为全局符号（Global）、本地符号（Local）和调试符号。

- 全局符号： 目标文件外可见的符号，可以被其他目标文件引用，或者自己使用但是需要在其他目标文件定义的符号。
- 本地符号： 只有目标文件内可见的符号，一般只在目标文件内部引用，例如私有的方法等。
- 调试符号： 调试符号不涉及引用权限概念，它是为了做 `debug` 存在的符号，包括行号信息等调试阶段需要的数据。行号信息记录了函数或者变量的所在文件以及对应行号。一般调试符号会在 `release`阶段被移除，也就是常说的 `Strip` 符号裁剪。可以在 `Xcode Build Setting`中找到相关配置。

> 可以通过 `LLVM` 的 `nm`工具直观的查看二进制文件中的符号信息。具体可以通过 `man nm` 来查看相关指令

通过 `nm` 直观的看到符号信息中，例如图片所示

![](https://cdn.zhangferry.com/Images/weekly_69_study_01.jpg)

第一列为符号地址，第二列为符号类型，第三列为符号名称。第二列符号类型中大写字母代表是全局符号，小写字母代表本地符号。又根据不同的类型，使用不同的字母表示，这里列出常见的几种：

- U: undefined（未定义符号）
- A: absolute（绝对符号）
- T: text section symbol(\__Text.__text)
- D: data section symbol（\__DATA.__data）
- B: bss section symbol（\__DATA.__bss）
- C: common symbol（只能出现在MH_OBJECT类型的Mach-O⽂件中）
- S: 除了上⾯所述的，存放在其他section的内容，例如未初始化的全局变量存放在（\__DATA,__common）中
- -: debugger symbol table

上面提到了全局符号和本地符号的不同点，可能会好奇有没有办法在开发阶段人工干预呢。

其实是可以的。实际开发过程中，可以通过 `__attribute__((visibility("default")))` 和 `__attribute__((visibility("hidden")))`分别修饰符号，达到控制符号类型的目的。例如

```c++
__attribute__((visibility("default"))) void MyFunction1() {} 
__attribute__((visibility("hidden"))) void MyFunction2() {}
```

`default`默认可见，`hidden`则不可见。

Xcode 中 `Build Setting -> Symbols Hidden by Default`也可以设置默认配置。

另外在针对动态库还可以通过编译参数 `-exported_symbols_list`和 `-unexported_symbols_list` 设置导出符号文件和非导出符号文件。

`exported_symbols_list`设置的导出符号可以理解为全局符号，未指定的符号默认是本地符号不可访问。`unexported_symbols_list`同理。

#### 符号生成规则

- C 语言： 比较简单，一般就是在函数或者变量的前面加下划线`_`

- C++: 因为支持 namespace、函数重载等高级特性，所以采用了 `Symbol Mangling`，不同编译器可能规则不同。

    例如

    ```c++
    namespace MyNameSpace {
        class MyClass{
        public:
            static int myFunc(int);
            static double myFunc(double);
        };
    }
    
    // 0000000000000008 T __ZN11MyNameSpace7MyClass6myFuncEd
    // 0000000000000000 T __ZN11MyNameSpace7MyClass6myFuncEi
    ```

    - 以_Z开头
    - C语言的保留字符串N
    - 对于 `namespace` 等嵌套的名称，接下依次拼接名称长度，名称
    - 然后是结束字符E
    - 最后是参数的类型，比如int是i，double是d

- OC: 格式一般是 `+/-[Class_name(category_name) method:name:]`。`+/-`表示类方法或者实例方法。然后依次是类名（分类名），方法名。

- Swift: 采用了类似于 `c++`的 `name mangling`, 暂时不太了解 Swift实际规则，但是可以使用 `xcrun swift-demangle `来反解析一个符号到对应的信息。

篇幅原因， Symbol 的一些应用场景以及存储相关信息后续更新。

- [iOS强化 : 符号 Symbol](https://www.jianshu.com/p/4493ab03d5b2 "iOS强化 : 符号 Symbol")
- [深入理解 Symbol](https://mp.weixin.qq.com/s/uss-RFgWhIIPc6JPqymsNg "深入理解 Symbol")


## 内容推荐

整理编辑：[东坡肘子](https://www.fatbobman.com)

> 本期将介绍近期的几篇优秀博文

1、[SwiftUI布局协议](https://swiftui-lab.com/layout-protocol-part-1/ "SwiftUI布局协议") -- 来自：Javier

[@东坡肘子](https://www.fatbobman.com/)：在 SwiftUI 诞生初期，SwiftUI-Lab 的 Javier 便对 SwiftUI 进行了深入地研究，可以说很多 SwiftUI 的使用者都是通过阅读他的文章才开始了解 SwiftUI 的布局机制。针对今年 SwiftUI 新增的 Layout 协议，Javier 也贡献出了精彩研究文章。文章共分上下两部分，上篇着重介绍理论，下篇提供了许多有趣的案例演示。

2、[iPhone 14 屏幕尺寸](https://useyourloaf.com/blog/iphone-14-screen-sizes/ "iPhone 14 屏幕尺寸") -- 来自：Keith Harrison

[@东坡肘子](https://www.fatbobman.com/)：iPhone 14 Pro 和 iPhone 14 Pro Max 用灵动岛替换了刘海，这导致了屏幕的分辨率也发生了变化。本文对 2022 年 iPhone 14 系列机型的屏幕尺寸的变化做了总结。

3、[如何判断 ScrollView、List 是否正在滚动中](https://www.fatbobman.com/posts/how_to_judge_ScrollView_is_scrolling/ "如何判断 ScrollView、List 是否正在滚动中") -- 来自：Holly Borla

[@东坡肘子](https://www.fatbobman.com/)：SwiftUI 4 重写了 ScrollView 和 List 的底层实现，这意味着以前通过 Hack 的方式获取滚动状态的手段将不再有效。本文将介绍几种在 SwiftUI 中获取当前滚动状态的方法，每种方法都有各自的优势和局限性。

4、[Swift 5.7 正式发布](https://www.swift.org/blog/swift-5.7-released/ "Swift 5.7 正式发布") -- 来自：Holly Borla

[@东坡肘子](https://www.fatbobman.com/)：Swift 5.7 现已正式发布! Swift 5.7包括对语言和标准库的重大补充，对编译器的增强以获得更好的开发者体验，对Swift生态系统中的工具的改进，包括SourceKit-LSP和Swift Package Manager，完善的Windows支持等等。

5、[Combine中的内存管理](https://tanaschita.com/20220912-memory-management-in-combine/ "Combine中的内存管理") -- 来自：Holly Borla

[@东坡肘子](https://www.fatbobman.com/)：就像其他异步操作一样，内存管理是 Combine 的一个重要部分。一个订阅者只要想接收值就需要保留一个订阅，然而，一旦不再需要订阅，所有的引用应该被正确地释放。在这种情况下，一个常见的问题是我们是否应该使用弱引用。本文将通过一些例子来帮助读者更好地理解 Combine 中的内存管理。

6、[Apple Watch 应用开发系列](https://juejin.cn/post/7136115417323405325 "Apple Watch 应用开发系列") -- 来自：Layer

[@东坡肘子](https://www.fatbobman.com/)：2015 年 4 月 24 日，Apple 发布了第一代 Apple Watch。 无论我们对 Apple Watch 看法如何，watchOS 肯定是我们要支持的 Apple 生态系统的一部分，确保我们的应用获得更大的曝光率。作者将通过创建一个 watchOS 应用程序，来展示如何将我们现有的 iOS 开发知识转移到 watchOS 上来。

## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)




## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #68 |  iPhone14 灵动岛创意](https://mp.weixin.qq.com/s/YNukagI-VTOsIkhlYM6dEQ)

[iOS 摸鱼周报 #67 | Xcode Cloud 已支持订阅](https://mp.weixin.qq.com/s/8H7YnrVTubKvVnYJBXcF_A)

[iOS 摸鱼周报 #66 | Shazam 迎来问世 20 周年](https://mp.weixin.qq.com/s/LP1qNAgjzEiDwrR7I32kuA)

[iOS 摸鱼周报 #65 | 什么是精准测试](https://mp.weixin.qq.com/s/lvMHf5qQHpnDGLz1KY-2dg)https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
