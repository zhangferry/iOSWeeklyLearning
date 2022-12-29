# iOS 摸鱼周报 #80 |Developer 设计开发加速器话题，SwiftUI 中管理数据模型

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题： Developer 设计开发加速器｜在 SwiftUI 中管理数据模型
> * 本周学习：iOS 堆栈调用理论回顾
> * 内容推荐：SwiftUI 好文推荐
> * 摸一下鱼：一款个人知识管理工具 MindForger，通过渲染高质量的图像、视频和动画展示数学之美。

## 本期话题

###  Developer 设计开发加速器｜在 SwiftUI 中管理数据模型

[@师大小海腾](https://juejin.cn/user/782508012091645/posts)：SwiftUI 以一种声明式的编程方式来定义用户界面，而这需要由您来定义数据与视图之间的依赖关系，以便能让 SwiftUI 正确工作。通过本次活动，您将了解 SwiftUI 提供的各种工具，用于将 App 的数据连接到用户界面。您还可以深入了解 SwiftUI 框架驱动的原理，以便能让您的 App 正确运作并且拥有良好性能。

活动将于 2023 年 1 月 10 日（周二）举办。名额有限。请在 2023 年 1 月 9 日前报名参加。**报名地址：** [https://developer.apple.com/events/view/D793NQ6482/dashboard](https://developer.apple.com/events/view/D793NQ6482/dashboard "Developer 设计开发加速器｜在 SwiftUI 中管理数据模型")。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### iOS 堆栈调用理论回顾

我们都知道程序的函数调用利用的是栈结构，每嵌套调用一次函数，就执行一次压栈操作，函数执行完毕后，执行出栈操作回到栈底(也就是函数调用处)，继续执行后续指令。
大部分操作系统栈的增长方向都是从高往低(包括 iOS / Mac OS)，意味着每次函数调用栈开辟都是在做内存地址的减法，`Stack Pointer` 指向栈顶，`Frame Pointer` 指向上一个栈帧的 `Stack Pointer`的地址值，通过 `Frame Pointer` 就可以递归回溯获取整个调用栈。 
每一次压栈时的数据结构被称为**栈帧**(Stack Frame)，里面存储了当前函数的栈顶指针以及栈底指针，如果我们能拿到每一次压栈的数据结构, 则可以根据这两个指针来递归回溯整个调用栈。

对于 x86_64或者 arm64 架构, 函数调用的汇编指令 `call/bl` 做法都是类似的：

1. 先将函数调用的下一条指令地址入栈，这一条指令是被调用函数执行结束后需要跳转执行的指令，一般存储到 `LR`寄存器中。如果后续还有其他函数调用，则会把`LR`存入栈帧进行保存。
2. 然后保存调用函数 `caller` 的 `FP` 指针，保存位置紧邻 `LR` 存储的内存地址。
3. 开辟新的栈空间，重新赋值 `FP` 指向新的栈的栈底，即被调用函数的栈帧的栈底。

![](https://cdn.zhangferry.com/Images/weekly_80_study_01.png)

通过上面的操作，我们已经可以实现串起整个函数调用链。但是由于我们只获取到 `LR`的值，它记录的是 `caller` 函数中的某一条指令地址，而我们的二进制文件存储的都是函数调用的首地址，所以要如何通过 `LR` 对应到具体的函数是下一步要做的事情。采用的方法也很好理解，即通过遍历 `MachO`的符号表，找到每个栈帧中存储的 `LR`的值最相近的高地址的函数，认为该函数是 `Caller`调用函数。

上面针对的是普通的函数调用，在实际情况下会有一些特殊的函数调用，例如内联或者尾调用等。这些都是没有办法通过上面的方式获取到调用栈的。

另外 x86_64 和 arm64 还有一些不同之处在于，arm64 下编译器可能会做一个优化：即针对叶子节点函数会优化栈帧结构，不再入栈保存 `FP`，这时读取到的 `FP`指针实际是 `Caller` 函数的 `FP`。

这个优化只针对 `FP`指针，叶子节点函数的`LR`指针还是会保存的（因为需要出栈继续执行下条指令）。所以我们可以通过线程上下文获取当前的 `LR` 对比`FP`计算得到的`LR` 是否是同一个地址，来判断最后一次的 `FP`是叶子节点函数的 `FP` 还是它的调用方的 `FP`。相同表示未优化 `FP`，不同表示已优化，则需要记录本次的 `LR`。

具体实现代码可以参考 [BSBacktraceLogger](https://github.com/bestswifter/BSBacktraceLogger "BSBacktraceLogger")，简化的核心代码如下：

```objective-c
NSString *_bs_backtraceOfThread(thread_t thread) {
  // 初始化50长度的指针数组
  uintptr_t backtraceBuffer[50];
  int i = 0;
// ...
  const uintptr_t instructionAddress = bs_mach_instructionAddress(&machineContext);
  backtraceBuffer[i] = instructionAddress;
  ++i;
  // 通过线程上下文获取 LR 地址 
  uintptr_t linkRegister = bs_mach_linkRegister(&machineContext);
  if(instructionAddress == 0) {
​    return @"Fail to get instruction address";
  }
  // 自定义的帧实体链表, 存储上一个调用栈以及返回地址(lr)
  BSStackFrameEntry frame = {0};
    
  // fp指针
  const uintptr_t framePtr = bs_mach_framePointer(&machineContext);
  if(framePtr == 0 ||
​    // 将fp存储的内容 (pre fp指针)存储到previous, fp+1 存储的内容(lr)存储到return_address
​    bs_mach_copyMem((void *)framePtr, &frame, sizeof(frame)) != KERN_SUCCESS) {
​    return @"Fail to get frame pointer";
  }
  // lr和fp读取的数据不相等, 是因为arm64下 编译器做的优化处理,即叶子函数复用调用函数的调用栈fp, 但是lr和sp是没有复用的, 所以为了避免丢帧,使用lr填充
  if (linkRegister != 0 && frame.return_address != linkRegister)  {
​    backtraceBuffer[i] = linkRegister;
​    i++;
  }
    
  // 原理就是通过当前栈帧的fp读取下一个指针数据,记录的是上一个栈帧的fp数据, fp + 2,存储的是lr数据, 即当前栈退栈后的返回地址(bl的下一条指令地址)
  for(; i < 50; i++) {
​    backtraceBuffer[i] = frame.return_address;
      // ... 容错处理
  }
  // 开始符号化，这里就是文中说的通过 lr 获取最近的函数首地址进行符号化
  int backtraceLength = i;
  Dl_info symbolicated[backtraceLength]；
  bs_symbolicate(backtraceBuffer, symbolicated, backtraceLength, 0);
    // ... 打印结果
  return [resultString copy];
}
```

代码中的 ` if (linkRegister != 0 && frame.return_address != linkRegister) ` 片段 `BSBacktraceLogger` 中是没有的，当根据打印堆栈将调用栈数调整到恰好 50 个时，会发现最后一个叶子节点函数栈帧丢失，也就是文中说的针对 arm64的优化。

以上代码仅是 `FP`和 `LR`的递归回溯的实现，符号化部分参考函数 `bs_symbolicate()`。

也可以查看 `BSBacktraceLogger` 的 [fork](https://github.com/talka123456/BSBacktraceLogger "BSBacktraceLogger fork") 版本代码，增加了核心代码逻辑注释方便学习。


## 内容推荐

整理编辑：[@远恒之义](https://github.com/eternaljust)

1、[SwiftUI 与 Core Data —— 安全地响应数据](https://www.fatbobman.com/posts/modern-Core-Data-Respond-Data-safely/ "SwiftUI 与 Core Data —— 安全地响应数据") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：保证应用不因 Core Data 的原因导致意外崩溃是对开发者的起码要求。本文将介绍可能在视图中产生严重错误的原因，如何避免，以及在保证视图对数据变化实时响应的前提下如何为使用者提供更好、更准确的信息。

2、[如何使用 SwiftUI Grid API 创建网格布局](https://www.appcoda.com.tw/swiftui-grid-api/ "如何使用 SwiftUI Grid API 创建网格布局") -- 来自：Simon Ng

[@远恒之义](https://github.com/eternaljust)：Grid 视图是一种容器视图，它以二维布局排列其他视图，Grid 为开发人员提供了构建基于网格的布局的更多选项。你可以使用 HStack 和 VStack 来构建类似的布局，不过 Grid 视图可以为你节省大量代码并使你的代码可读性更高，你可以尝试使用 Grid 来构建一些有趣的布局。

3、[如何对 SwiftUI list 中的列表行进行重新排序](https://sarunw.com/posts/swiftui-list-onmove/ "如何对 SwiftUI list 中的列表行进行重新排序") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：想要启用 SwiftUI 列表行重新排序，你只需执行以下步骤即可：创建数据源（必须是可变的）、使用填充列表视图 `ForEach`、将 `onMove(perform:)` 修饰符应用于 `ForEach`、手动移动项目 `onMove` 的闭包，调用方法十分简单方便。

4、[如何创建 iOS 锁屏小部件？](https://swiftsenpai.com/development/create-lock-screen-widget/?utm_source=rss&utm_medium=rss&utm_campaign=create-lock-screen-widget "如何创建 iOS 锁屏小部件？") -- 来自：Lee Kah Seng

[@远恒之义](https://github.com/eternaljust)：在 iOS 16 中，Apple 新增了锁定屏幕，其中锁屏小组件带来 app 新的曝光入口。与桌面小组件类似，锁屏小组件主要用 WidgetKit 来实现功能。不同的是，Apple 引入了 3 个新的不同类型的锁屏小组件：`accessoryCircular`、`accessoryRectangular` 和 `accessoryInline`，前两个为小与中两种尺寸，后者为单行文本。

5、[用 SwiftUI 实现 AI 聊天对话 app - iChatGPT](https://juejin.cn/post/7175051294808211512 "用 SwiftUI 实现 AI 聊天对话 app - iChatGPT") -- 来自掘金：37手游iOS技术运营团队

[@远恒之义](https://github.com/eternaljust)：iChatGP 是一款用 SwiftUI 实现的开源 ChatGPT app，支持系统 iOS 14.0+、iPadOS 14.0+、macOS 11.0+，目前已实现 ChatGPT 基本聊天功能：直接与 ChatGPT 对话，并且保留上下文；复制问题和回答内容；快捷重复提问。

6、[EBPF 介绍](https://coolshell.cn/articles/22320.html "EBPF 介绍") -- 来自：酷壳

[@远恒之义](https://github.com/eternaljust)：eBPF（extened Berkeley Packet Filter）是一种内核技术，它允许开发人员在不修改内核代码的情况下运行特定的功能。eBPF 比起传统的 BPF 来说，传统的 BPF 只能用于网络过滤，而 eBPF 则可以用于更多的应用场景，包括网络监控、安全过滤和性能分析等。耗子叔在文末留了一个彩蛋，聊了聊他对大火的 ChatGPT 一些看法。


## 摸一下鱼

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

1、[A Tour in the Wonderland of Math with Python](https://github.com/neozhaoliang/pywonderland "A Tour in the Wonderland of Math with Python") 通过渲染高质量的图像、视频和动画来展示数学之美。

![](https://cdn.zhangferry.com/Images/125026787-dad59700-e0b7-11eb-889f-b0c737413b6a.png)

2、[MindForger](https://www.mindforger.com/#home "MindForger")，是一款个人知识管理工具

![](https://cdn.zhangferry.com/Images/1-title-screen.jpg)

MindForger的目标是模仿人类的思维--学习、回忆、识别、联想、遗忘--以实现与你的思维的协同，使你的搜索、阅读和写作更有效率。

不仅如此，MindForger 尊重隐私，并确保知识安全。

不仅仅是一个markdown 编辑器，更是一个辅助的智能助手。

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
