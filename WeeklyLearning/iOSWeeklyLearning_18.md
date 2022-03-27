# iOS摸鱼周报 第十八期

![](http://cdn.zhangferry.com/Images/iOS摸鱼周报模板.png)

### 本期概要

> * 本期话题：什么是暗时间。
> * Tips 带来了多个内容：Fastlane 用法总结、minimumLineSpacing 与 minimumInteritemSpacing 的区别以及一个定位 RN 发热问题的过程。
> * 面试解析：本期围绕 block 的变量捕获机制展开说明。
> * 优秀博客带来了几篇编译优化的文章。
> * 学习资料带来了一个从 0 设计计算机的视频教程，还有 Git 和正则表达式的文字教程。
> * 开发工具介绍了两个代码片段整理的相关工具。

## 本期话题

[@zhangferry](https://zhangferry.com)：最近在看一本书：《暗时间》，初听书名可能有些不知所云，因为这个词是作者发明的，我们来看[文中](http://mindhacks.cn/2009/12/20/dark-time/ "暗时间")对“暗时间”的解释：

> 看书并记住书中的东西只是记忆，并没有涉及推理，只有靠推理才能深入理解一个事物，看到别人看不到的地方，这部分推理的过程就是你的思维时间，也是人一生中占据一个显著比例的“暗时间”。你走路、买菜、洗脸洗手、坐公交、逛街、出游、吃饭、睡觉，所有这些时间都可以成为暗时间，你可以充分利用这些时间进行思考，反刍和消化平时看和读的东西，这些时间看起来微不足道，但日积月累会产生巨大的效应。

这里对于暗时间的解释是思维时间，因为思维是人的”后台线程“，我们通常注意不到它，可它却实际存在且非常重要。但按思维时间来说其适用的范围就有点窄了，大多数情况我们并不会一直保持思考。我尝试把刘未鹏关于暗时间的概念进行扩展，除思维时间外，还包括那些零碎的，可以被利用但未被利用起来的时间。“明时间”，暗时间倘若都能利用起来，那定是极佳的。

目前我有两个关于暗时间应用的实践：

1、在上下班走路过程中是思考时间。我现在换了一条上下班路线，使得步行时间更长，一趟在 15 分钟左右。这段时间，我会尝试想下今天的工作内容，规划日常任务；或者回忆最近在看的某篇文章，脑海里进行推演然后尝试复述其过程；或者仅仅观察路过的行人，想象下如果我是他们，我在另一个视角观察到的自己是什么样子。总之，让大脑活跃起来。

2、等待的过程是运动时间。等人或者等红绿灯的时候，我会尝试让自己运动起来，比如小动作像垫垫脚，大一点的动作像跳一跳、跑一跑。运动是一项反人性的事情，所以它不能规划，一规划就要跟懒惰做斗争，所以干脆就随时有空就动两下。通常这种小型的运动体验，如果突然因为要开始干正事被打断了，还会有种意犹未尽的感觉。

当然还可以有别的尝试，重要的是我们要明白和感受到暗时间这个东西，然后再想办法怎么利用它。至少在我的一些尝试中会让一些本该枯燥的时间变得更有趣了些。

## 开发Tips

整理编辑：[zhangferry](https://juejin.cn/user/3298190611456638)

### Fastlane 用法总结

图片来源：[iOS-Tips](https://github.com/awesome-tips/iOS-Tips/blob/master/resources/fastlane.png)

![](http://cdn.zhangferry.com/Images/fastlane.png)

### React Native 0.59.9 引发手机发烫问题解决思路

内容贡献：[yyhinbeijing](https://github.com/yyhinbeijing)

问题出现的现象是：RN 页面放置久了，或者反复操作不同的 RN 页面，手机会变得很烫，并且不会自动降温，要杀掉进程才会降温，版本是 0.59.9，几乎不同手机不同手机系统版本均遇到了这个问题，可以确定是 RN 导致的，但具体哪里导致的呢，以下是通过代码注释定位问题的步骤，后面数值为 CPU 占用率：

1、原生：7.2%

2、无网络无 Flatlist：7.2%

3、网络 + FlatList ：100%+

4、网络 + 无 FlatList：100%+

5、去掉 loading：2.6% — 30%，会降低

6、网络和 FlatList 全部放开，只关闭 loading 最低 7.2%，能降低，最高 63%

首先是发现网络导致 CPU 占用率很高，然后网络注释掉 RNLoading （我们自写的 loading 动画），发现内存占用不高了。就断定是 RNLoading 问题，查询发现：我们每次点击 tab 都会加载 loading，而 loading 又是动画，这样大量的动画引发内存问题。虽不是特例问题，但发现、定位、解决问题的过程仍然是有借鉴意义的，即确定范围，然后不断缩小范围。


## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析会按照主题讲解一些高频面试题，本期面试题是 **block 的变量捕获机制**。

### block 的变量捕获机制

block 的变量捕获机制，是为了保证 block 内部能够正常访问外部的变量。

1、对于全局变量，不会捕获到 block 内部，访问方式为`直接访问`；作用域的原因，全局变量哪里都可以直接访问，所以不用捕获。

2、对于局部变量，外部不能直接访问，所以需要捕获。

* auto 类型的局部变量（我们定义出来的变量，默认都是 auto 类型，只是省略了），block 内部会自动生成一个同类型成员变量，用来存储这个变量的值，访问方式为`值传递`。**auto 类型的局部变量可能会销毁，其内存会消失，block 将来执行代码的时候不可能再去访问那块内存，所以捕获其值**。由于是值传递，我们修改 block 外部被捕获变量的值，不会影响到 block 内部捕获的变量值。
* static 类型的局部变量，block 内部会自动生成一个同类型成员变量，用来存储这个变量的地址，访问方式为`指针传递`。static 变量会一直保存在内存中， 所以捕获其地址即可。相反，由于是指针传递，我们修改 block 外部被捕获变量的值，会影响到 block 内部捕获的变量值。    
* 对于对象类型的局部变量，block 会连同它的所有权修饰符一起捕获。
    * 如果 block 是在栈上，将不会对对象产生强引用
    * 如果 block 被拷贝到堆上，将会调用 block 内部的 `copy(__funcName_block_copy_num)`函数，copy 函数内部又会调用 `assign(_Block_object_assign)`函数，assign 函数将会根据变量的所有权修饰符做出相应的操作，形成强引用（retain）或者弱引用。
    * 如果 block 从堆上移除，也就是被释放的时候，会调用 block 内部的 `dispose(_Block_object_dispose)`函数，dispose 函数会自动释放引用的变量（release）。
* 对于 `__block`（可用于解决 block 内部无法修改 auto 变量值的问题） 修饰的变量，编译器会将 `__block` 变量包装成一个 `__Block_byref_varName_num` 对象。它的内存管理几乎等同于访问对象类型的 auto 变量，但还是有差异。
    * 如果 block 是在栈上，将不会对 `__block` 变量产生强引用
    * 如果 block 被拷贝到堆上，将会调用 block 内部的 copy
    函数，copy 函数内部又会调用 assign 函数，assign 函数将会直接对 `__block` 变量形成强引用（retain）。
    * 如果 block 从堆上移除，也就是被释放的时候，会调用 block 内部的 dispose 函数，dispose 函数会自动释放引用的 `__block` 变量（release）。
    ![](https://user-gold-cdn.xitu.io/2020/2/23/170724cf4ff4b2bd?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
* 被 `__block `修饰的对象类型的内存管理：
    * 如果 `__block` 变量是在栈上，将不会对指向的对象产生强引用
    * 如果 `__block` 变量被拷贝到堆上，将会调用 `__block` 变量内部的 `copy(__Block_byref_id_object_copy)`函数，copy 函数内部会调用 assign 函数，assign 函数又会根据变量的所有权修饰符做出相应的操作，形成强引用（retain）或者弱引用。（注意：这里仅限于 ARC 下会 retain，MRC 下不会 retain，所以在 MRC 下还可以通过 `__block` 解决循环引用的问题）
    * 如果 `__block` 变量从堆上移除，会调用 `__block` 变量内部的 dispose 函数，dispose 函数会自动释放指向的对象（release）。
    
    

掌握了 block 的变量捕获机制，我们就能更好的应对内存管理，避免因使用不当造成内存泄漏。

常见的 block 循环引用为：`self(obj) -> block -> self(obj)`。这里 block 强引用了 self 是因为对于对象类型的局部变量，block 会连同它的所有权修饰符一起捕获，而对象的默认所有权修饰符为 __strong。

```objectivec
self.block = ^{
    NSLog(@"%@", self);
};
```

> 为什么这里说 self 是局部变量？因为 self 是 OC 方法的一个隐式参数。

为了避免循环引用，我们可以使用 `__weak` 解决，这里 block 将不再持有 self。

```objectivec
__weak typeof(self) weakSelf = self;
self.block = ^{
    NSLog(@"%@", weakSelf);
};
```

为了避免在 block 调用过程中 self 提前释放，我们可以使用 `__strong` 在 block 执行过程中持有 self，这就是所谓的 Weak-Strong-Dance。

```objectivec
__weak typeof(self) weakSelf = self;
self.block = ^{
    __strong typeof(self) strongSelf = weakSelf;
    NSLog(@"%@", strongSelf);
};
```

当然，我们平常用的比较多的还是 `@weakify(self)` 和 `@strongify(self)` 啦。

```objectivec
@weakify(self);
self.block = ^{
    @strongify(self);
    NSLog(@"%@", self);
};
```

如果你使用的是 RAC 的 Weak-Strong-Dance，你还可以这样：

```objectivec
@weakify(self, obj1, obj2);
self.block = ^{
    @strongify(self, obj1, obj2);
    NSLog(@"%@", self);
};
```

如果是嵌套的 block：

```objectivec
@weakify(self);
self.block = ^{
    @strongify(self);
    self.block2 = ^{
        @strongify(self);
        NSLog(@"%@", self);
    }
};
```

你是否会疑问，为什么内部不需要再写 @weakify(self) ？这个问题就留给你自己去思考和解决吧！

相比于简单的相互循环引用，block 造成的大环引用更需要你足够细心以及敏锐的洞察力，比如：

```objectivec
TYAlertView *alertView = [TYAlertView alertViewWithTitle:@"TYAlertView" message:@"This is a message, the alert view containt text and textfiled. "];
[alertView addAction:[TYAlertAction actionWithTitle:@"取消" style:TYAlertActionStyleCancle handler:^(TYAlertAction *action) {
    NSLog(@"%@-%@", self, alertView);
}]];
self.alertController = [TYAlertController alertControllerWithAlertView:alertView preferredStyle:TYAlertControllerStyleAlert];
[self presentViewController:alertController animated:YES completion:nil];
```

这里循环引用有两处：

1. `self -> alertController -> alertView -> handlerBlock -> self`
2. `alertView -> handlerBlock -> alertView`

避免循环引用：

```objectivec
TYAlertView *alertView = [TYAlertView alertViewWithTitle:@"TYAlertView" message:@"This is a message, the alert view containt text and textfiled. "];
@weakify(self, alertView);
[alertView addAction:[TYAlertAction actionWithTitle:@"取消" style:TYAlertActionStyleCancle handler:^(TYAlertAction *action) {
    @strongify(self, alertView);
    NSLog(@"%@-%@", self, alertView);
}]];
self.alertController = [TYAlertController alertControllerWithAlertView:alertView preferredStyle:TYAlertControllerStyleAlert];
[self presentViewController:alertController animated:YES completion:nil];
```

> 另外再和你提一个小知识点，当我们在 block 内部直接使用 _variable 时，编译器会给我们警告：`Block implicitly retains self; explicitly mention 'self' to indicate this is intended behavior`。
>
> 原因是 block 中直接使用 `_variable` 会导致 block 隐式的强引用 self。Xcode 认为这可能会隐式的导致循环引用，从而给开发者带来困扰，而且如果不仔细看的话真的不太好排查，笔者之前就因为这个循环引用找了半天，还拉上了我导师一起查找原因。所以警告我们要显式的在 block 中使用 self，以达到 block 显式 retain 住 self 的目的。改用 `self->_variable` 或者 `self.variable`。
> 
> 你可能会觉得这种困扰没什么，如果你使用 `@weakify` 和 `@strongify` 那确实不会造成循环引用，因为 `@strongify` 声明的变量名就是 self。那如果你使用 `weak typeof(self) weak_self = self;` 和 `strong typeof(weak_self) strong_self = weak_self` 呢？

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`编译优化`

1、[iOS编译过程的原理和应用](https://blog.csdn.net/Hello_Hwc/article/details/53557308 "iOS编译过程的原理和应用") -- 来自 CSDN：黄文臣

做编译优化前，先了解下编译原理吧！该作者通过 iOS 的视角，白话了编译原理，通俗易懂。

2、[Xcode编译疾如风系列 - 分析编译耗时](https://cloud.tencent.com/developer/article/1817236 "Xcode编译疾如风系列 - 分析编译耗时") -- 来自腾讯社区：小菜与老鸟

在进行编译速度优化前，一个合适的分析工具是必要的，它能告诉你哪部分编译时间较长，让你发现问题，从而解决问题，本文介绍了几种分析编译耗时的方式，助你分析构建时间。该作者还有其他相关姊妹篇，建议前往阅读。

3、[iOS 微信编译速度优化分享](https://cloud.tencent.com/developer/article/1564372 "iOS 微信编译速度优化分享") -- 来自云+社区：微信终端开发团队

文章对编译优化由浅入深做了介绍。作者首先介绍了常见的现有方案，利用现有方案以及精简代码、将模板基类改为虚基类、使用 PCH 等方案做了部分优化。文章精彩的部分在于作者并没有止步于此，而是从编译原理入手，结合量化手段，分析出编译耗时的瓶颈。在找到问题的瓶颈后，作者尝试人工进行优化，但是效率较低。最终在 IWYU 基础上，增加了 ObjC 语言的支持，高效地处理了一部分多余的头文件。

4、[iOS编译速度如何稳定提高10倍以上之一](https://juejin.cn/post/6903407900006449160 "iOS编译速度如何稳定提高10倍以上之一") -- 来自掘金：Mr_Coder

美柚 iOS 的编译提效历程。作者对常见的优化做了分析，列举了各自的优缺点。有想做编译优化的可以参考这篇文章了解一下。对于业界的主流技术方案，别的技术文章往往只介绍优点，对方案的缺点谈的不够彻底。这篇文章从实践者的角度阐述了常见方案的优缺点，很有参考价值。文章介绍了双私有源二进制组件并与 ccache 做了对比，最后列出了方案支持的功能点。

5、[iOS编译速度如何稳定提高10倍以上之二](https://juejin.cn/post/6903408514778497031 "iOS编译速度如何稳定提高10倍以上之二") -- 来自掘金：Mr_Coder

作为上文的姊妹篇，本文详细介绍了双私有源二进制组件的方案细节以及使用方法。对该方案感兴趣的可以关注下。

6、[一款可以让大型iOS工程编译速度提升50%的工具](https://tech.meituan.com/2021/02/25/cocoapods-hmap-prebuilt.html "一款可以让大型iOS工程编译速度提升50%的工具") -- 来自美团技术团队：思琦 旭陶 霜叶

本文主要介绍了如何通过优化头文件搜索机制来实现编译提速，全源码编译效率提升 45%。文中涉及很多知识点，比如 hmap 文件的作用、Build Phases - Headers 中的 Public，Private，Project 各自是什么作用。文中详细分析了 podspec 创建头文件产物的逻辑以及 Use Header Map 失效的原因。干货比较多，可能得多读几遍。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 从 0 到 1 设计一台计算机

地址：https://www.bilibili.com/video/BV1wi4y157D3

来自 [Ele实验室](https://space.bilibili.com/481434238) 的计算机组成原理课程，该系列视频主要目的是让大家对「计算机是如何工作的」有个较直观的认识，做为深入学习计算机科学的一个启蒙。观看该系列视频最好有一些数字电路和模拟电路的基础知识，Ele 实验室同时也有关于 [数电](https://www.bilibili.com/video/BV1Hi4y1t7zY "Ele实验室 数电") 和 [模电](https://www.bilibili.com/video/BV1774114798 "Ele实验室 模电") 的基础知识介绍供大家参考。

### Git Cheat Sheet 中文版

地址：https://github.com/flyhigher139/Git-Cheat-Sheet

Git Cheat Sheet 让你不用再去记所有的 git 命令！对新手友好，可以用于查阅简单的 git 命令。

### 正则表达式 30 分钟入门教程

地址：https://deerchao.cn/tutorials/regex/regex.htm

30 分钟内让你明白正则表达式是什么，并对它有一些基本的了解。别被那些复杂的表达式吓倒，只要跟着我一步一步来，你会发现正则表达式其实并没有想象中的那么困难。除了作为入门教程之外，本文还试图成为可以在日常工作中使用的正则表达式语法参考手册。

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

### SnippetsLab

**地址**：http://www.renfei.org/snippets-lab/

**软件状态**：$9.99

**软件介绍**：

一款强大的代码片段管理工具，从此告别手动复制粘贴，SnippetsLab 的设计更符合 Apple 的交互习惯，支持导航栏快速操作。另外还可以同步 Github Gist 内容，使用 iCloud 备份。

![](http://cdn.zhangferry.com/Images/20210710232333.png)

### CodeExpander

**地址**：https://codeexpander.com/

**软件状态**：普通版免费，高级版付费

**软件介绍**：

专为开发者开发的一个集输入增强、代码片段管理工具，支持跨平台，支持云同步（Github/码云）。免费版包含 90% 左右功能，相对 SnippetsLab 来说其适用范围更广泛，甚至包括一些日常文本的片段处理。

![](http://cdn.zhangferry.com/Images/20210710231521.png)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期内容

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](http://cdn.zhangferry.com/Images/wechat_official.png)
