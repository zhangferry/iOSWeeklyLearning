# iOS摸鱼周报 第四十二期

![](http://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * Tips：
> * 面试模块：Runtime 中的 **StripeMap<T>** 模板类
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)



## 面试解析

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### `StripeMap<T>` 模板类

`StripeMap<T>` 是 OC `Runtime` 中定义的一个类，用于引用计数表、`Synchroinzed`、以及属性设置时的 `lock`列表等。**该类可以理解成是一种特殊的 hashmap。**
特殊性体现在：一般的 hashmap key&value 是一一对应的，即使存在哈希冲突，也会通过其他方法解决该冲突，但是`StripeMap`是 key&value 多对一的。
我们去思考下 apple 为什么要将内存管理的表结构设计为 `StripeMap` 类型？先了解下简化后定义：

```cpp
enum { CacheLineSize = 64 };

template<typename T>
class StripedMap {
#if TARGET_OS_IPHONE && !TARGET_OS_SIMULATOR
    enum { StripeCount = 8 };
#else
    enum { StripeCount = 64 };
#endif
    struct PaddedT {
        T value alignas(CacheLineSize); // 对齐
    };

    PaddedT array[StripeCount];
};
```

**`StripeMap`存在的意义很显然就是优化访问性能 **. 优化高频访问 `<T>`产生的性能瓶颈，尤其是在多线程资源竞争场景下的。根据注释主要体现在以下方面

- 对象结构内部维护一个数组，根据设备的不同分成不同的页，移动设备是 8 页，其他是 64 页。
- 它使用对象的地址作为 key，进行哈希运算后获取一个 index，取得对应的 `<T>` value 。映射关系为 `void* -> <T>`
- 做内存对齐，提高cpu 缓存命中率

#### 分离锁优化

`StripeMap` 实质上是对分离锁概念的实现，简单概述下个人对分离锁的理解
我们都知道多线程场景下，如果多个变量都会被多线程访问和修改，最好的办法是针对不同的变量用不同的锁对象来实现资源管理。这样可以避免访问一个变量时，多线程访问其他不相关的变量时被阻塞等待。这其实是对分拆锁的应用。即避免对同一个锁访问等待。
而分离锁则是对上述思路的进一步优化，针对同一个高频访问的对象来说，分段管理可以解决线程之间的资源竞争。拿 `SideTables`举例来说：
将 `SideTables` 表结构分拆为 8 份，每一份维护一个锁对象。这样在高频访问时，在保证线程安全的同时最多可以支持访问所有的 8 页表数据。实现思路是数组 + 哈希函数（将地址指针转换为 index 索引）。 

```cpp
typedef unsigned long           uintptr_t;

static unsigned int indexForPointer(const void *p) {
        uintptr_t addr = reinterpret_cast<uintptr_t>(p);
        return ((addr >> 4) ^ (addr >> 9)) % StripeCount;
    }
```

将地址指针强制转换为 `uintptr_t` 无符号长整型，`uintptr_t` 定义为 8 字节，保证了指针（8 字节）的全量转换不会溢出。
然后通过位运算以及取模保证 index 落在 StripeCount 索引范围内。

#### CPU Cache Line

在上面优化方式第三条提到，在定义模板类型 `<T>` 时，使用 `CacheLineSize`做了内存对齐。
通常来讲，内存对齐的目的是为了加快 CPU 的访问，这里也不例外，

但是好奇的是 OC 中常见的内存对齐大小一般是对象的 16 字节对齐。而 StripedMap 定义了 64 字节对齐是出于什么考虑。

这里直接给出结论（理论部分不感兴趣的同学可以直接跳过）：**CacheLine 是 CPU Cache 缓存和主内存一次交换数据的大小，不同 CPU 上不同，Mac & iOS 上是 64 字节,这里是为了解决 `Cpu Cache`中的伪共享（False Sharing）问题。**

出于探索心理，搜索了一下关键字。因为笔者对操作系统了解不多，所以只是做一个概述：

1. CPU 和内存之间由于存在巨大的频率差距，影响数据访问速度从而诞生了 `CPU Cache` 的概念，`Cache Line` 是 `CPU Cache`之间数据传输和操作的最小单位。意味着每一次缓存之间的数据交换都是`Cache Line`的倍数。这是前置条件。

2. 另外一个重要的点是不同核心之间 L1 和 L2 缓存是不共享的，其他核心中的线程要访问当前核心缓存中的数据需要发送 `RFO 消息`，当前核心重置命中的的`Cache Line`状态，并经过一次 L1 / L2 => L3/主内存的数据写入，另外一个核心再次读取后才能访问。如果频繁的在两个核心线程中访问。会造成性能损耗。

我们假设一个场景， 两个不相关的变量 `var1` 和 `var2` 小于 64 字节，并且内存中紧邻，这时一个核心加载了包含 `var1 和 var2` 内存区域的`Cache Line` 并更新了 `var1`的值，此时处于另外一个核心需要访问 `var2`就会出现上面第二条的情况。
解决这类问题的思路就是空间换时间。也是 `StripedMap` 的做法。内存对齐，尽量保证不同页的 `SideTable`表结构会在不同的 `Cahce Line`上。这样不同的核心线程就可以做到同时处理两个变量值。

* [Objective-C runtime源码小记-StripedMap](https://juejin.cn/post/6869014441284141063 "Objective-C runtime源码小记-StripedMap")
* [【译】CPU 高速缓存原理和应用](https://segmentfault.com/a/1190000022785358 "【译】CPU 高速缓存原理和应用")


## 优秀博客

> 本期将整理一些有关最近发布的 Swift 5.6 和 Xcode 13.3 的新特性和新功能的博文。

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[Swift 5.6 新特性](https://juejin.cn/post/7077369199626027039 "Swift 5.6 新特性") -- 来自掘金：YungFan

[@东坡肘子](https://www.fatbobman.com/)：Swift 5.6 为该语言引入了一系列新的特性，同时为了协助开发者顺利地过渡至 Swift 6 而完善了部分其他功能。本文对 Swift 5.6 的新特性进行了介绍。另外，在 Swift 每次升级后，hackingwithswift.com 都会有专文介绍新添加的内容，感兴趣的朋友可以持续关注。

2、[Swift 5.6 SE-0335 Introduce existential any 的理解](https://juejin.cn/post/7078192732635676680 "Swift 5.6 SE-0335 Introduce existential any 的理解") -- 来自掘金：赤脊山的豺狼人

[@东坡肘子](https://www.fatbobman.com/)：在Swift 5.6 的新功能中，引入了一个新的关键字 any 来标记 existential type。这种变化有可能在未来破坏现有代码，使其在 Swift 6 中会出现兼容性问题。所有的 Swift 开发者都应及时对其有所了解。本文的作者将对 any 的用法和存在的理由进行介绍和探讨。

3、[在GitHub页面上将DocC文档作为静态网站发布](https://www.createwithswift.com/publishing-docc-documention-as-a-static-website-on-github-pages/ "Publishing DocC Documentation as a Static Website on GitHub Pages") -- 来自：Moritz Philip Recke

[@东坡肘子](https://www.fatbobman.com/)：Swift 5.6 为 Swift Package Manager 实现了可扩展的构建工具（SE-0303）及其扩展命令插件（SE-0332）等功能。本教程展示了如何利用新功能生成 DocC 文档，并将其处理为可静态托管的文档。

4、[Xcode 13.3 添加了在私有存储库中使用 SPM 二进制依赖项的能力](https://blog.eidinger.info/xcode-133-supports-spm-binary-dependency-in-private-github-release "Xcode 13.3 supports SPM binary dependency in private GitHub release") -- 来自：Marco Eidinger

[@东坡肘子](https://www.fatbobman.com/)：无法通过二进制发布库是阻碍开发者全面转向 Swift Package Manager 的一个重要因素。在 Xcode 12 中添加了XCFramework ，使得二进制发布得以可能。Xcode 13.3 再接再厉，增加了 XCFramework 对私有存储库的支持。开发者通过在开发私有的闭源库时将其代码作为二进制文件提供，以进一步保护其知识产权。

5、[Swift异步算法介绍](https://www.swift.org/blog/swift-async-algorithms/ "Introducing Swift Async Algorithms") -- 来自：Tony Parker

[@东坡肘子](https://www.fatbobman.com/)：Swift 5.5 为 Swift 带来了全新的异步开发体验。近日，苹果公开了跨平台开源项目 Swift Async Algorithms，为开发者提供了更加自然、高效地处理异步序列的能力。该库需要 Swift 5.6 的支持。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 即时教程

**地址**：https://js.design/courses

由[即使设计](https://js.design/)社区组织的精选设计课程，即时设计是一款可以在线实时协作的专业 UI 设计工具，类似 Figma。在即时教程中你可以找到来自各大视频网站平台创作者们的免费高质量课程。从零基础开始一步步到做案例，进阶技巧，应有尽有，非常适合想学一点 UI 知识的程序员们。

![jsdesign](http://cdn.zhangferry.com/Images/截屏2022-03-31 下午4.48.10.png)

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Decode

**地址**：https://microcodingapps.com/products/decode.html

**软件状态**：$8.99

**软件介绍**：

 将 `Xcode Interface Builder` 文件（`Xib` 和 `Storyboard` 文件）转换为 `Swift` 源代码。

![Decode](http://cdn.zhangferry.com/top-d338be7e-1200.png)


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](http://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
