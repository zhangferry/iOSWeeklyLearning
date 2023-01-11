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

> 本期将推荐近期的一些优秀博文，涵盖如何保护剪切板内容、SwiftUI 的视图风格、iOS 应用启动优化等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[如何防止复制和粘贴到其他 iOS 应用程序中](https://blog.eidinger.info/prevent-copy-paste-into-other-ios-apps "如何防止复制和粘贴到其他 iOS 应用程序中") -- 来自：Marco Edinger

[@东坡肘子](https://www.fatbobman.com/): 在企业应用程序中，经常需要通过防止最终用户将内容复制和粘贴到其他应用程序中来保护敏感信息。在这篇文章中，作者将向你展示为 iOS 应用程序引入这种高级剪贴板保护功能的多种方法。

2、[掌握 Swift Concurrency 的 AsyncStream](https://www.donnywals.com/understanding-swift-concurrencys-asyncstream/ "掌握 Swift Concurrency 的 AsyncStream") -- 来自：Donny wals

[@东坡肘子](https://www.fatbobman.com/): 创建自定义的异步序列的最好方法是什么？实现 AsyncSequence 协议并构建你的 AsyncIterator 确实可以解决一切问题，但实现起来很繁琐而且容易出错。在这篇文章中，作者将向你展示如何利用 Swift 的 AsyncStream 来构建自定义的异步序列，在你需要的时候产生数值。

3、[SwiftUI 视图的样式 —— 视图样式是如何工作的](https://peterfriese.dev/posts/swiftui-styling-views/ "SwiftUI 视图的样式 —— 视图样式是如何工作的") -- 来自：Peter Friese

[@东坡肘子](https://www.fatbobman.com/): SwiftUI 视图的样式是一个强大的概念，让开发者在设计应用程序时具有很大的灵活性，且不会丢失我们使用的视图的语义。支持此概念的 SwiftUI 视图列表令人印象深刻：按钮、选择器、菜单、切换、指示器、文本和标签、集合视图、导航视图、窗口和工具栏以及组等。因此，下次在你需要定制 UI 元素的特殊外观时，请先查看苹果的文档，看看是否已经有满足你需求的风格。如果没有，本文将告诉你如何创建自定义样式。

4、[Dependencies —— Point Free 发布了新的开源依赖库](https://www.pointfree.co/blog/posts/92-a-new-library-to-control-dependencies-and-avoid-letting-them-control-you "Dependencies —— Point Free 发布了新的开源依赖库") -- 来自：Point Free

[@东坡肘子](https://www.fatbobman.com/): 依赖性是指你的应用程序中需要与不受你控制的外部系统交互的类型和功能。典型的例子是向服务器发出网络请求的 API 客户端，但也有一些看似无害的东西，如 UUID 和日期初始化器、文件访问、用户默认值，甚至时钟和计时器，都可以被认为是依赖关系。Point Free 将 TCA 中广受好评的依赖功能分离出来构建成一个独立且开源的依赖管理系统，以便让更多的开发者受益。

5、[云音乐 iOS 启动性能优化「开荒篇」](https://juejin.cn/post/7145672412883845127 "云音乐 iOS 启动性能优化「开荒篇」") -- 来自：网易云音乐技术团队

[@东坡肘子](https://www.fatbobman.com/): App 启动作为用户使用应用的第一个体验点，直接决定着用户对 App 的第一印象。网易云音乐作为一个有着近 10 年发展历史的 App，随着各种业务不停的发展和复杂场景的堆叠，不同的业务和需求不停地往启动链路上增加代码，这给 App 的启动性能带来了极大的挑战。而随着云音乐用户基数的不断扩大和深度使用，越来越多的用户反馈启动速度慢，况且启动速度过慢更甚至会降低用户的留存意愿。因此，云音乐 iOS App 急需要进行一个专项针对启动性能进行优化。本文将介绍云音乐技术团队在 App 启动优化方面所做出的努力。（ 编者同大多数评论的想法一致，在不解决开屏广告的情况下，一切基于技术层面的优化都很难让用户有较大的感知 ）

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
