# iOS摸鱼周报 第四十二期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * Tips：
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：

### 2022年1月31号之后提交的引用需提供账号删除功能

内容如题，该项要求是 2021 年 10 月 6 号提出的，主要目的是加强苹果生态的隐私保护。在 App Store 审核指南的 5.1.1 条款第 v 条更新了这句话：

> If your app supports account creation, you must also offer account deletion within the app.

但对于如何设置该功能，苹果并没有明确的要求。如果删除用户账号，应用端可以根据相关法律继续保留用户信息，但这需要在隐私政策中进行说明所采集用户数据的内容和保留策略。

[Account deletion within apps required starting January 31](https://developer.apple.com/news/?id=mdkbobfo "Account deletion within apps required starting January 31")

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)

## 面试解析

整理编辑：[zhangferry](https://zhangferry.com)

### 如何治理 OOM

OOM（Out Of Memory）指的是应用内存占用过高被系统强制杀死的情况，通常还会再分为 FOOM （前台 OOM） 和 BOOM （后台 OOM）两种。其中 FOOM 现象跟常规 Crash 一样，对用户体验影响比较大。

OOM 产生的原因是应用内存占用过高，治理方法就是降低内存占用，这可以分两部分进行：

1、现存代码：问题检测，查找内存占用较大的情况进行治理。

2、未来代码：防裂化，对内存使用进行合理的规范。

#### 问题检测

OOM 与其他 Crash 不同的一点是它的触发是通过 `SIGKILL` 信号进行的，常规的 Crash 捕获方案无法捕获这类异常。那么该如何定位呢，线下我们可以通过 Schems 里的 Memory Management，生成 memgraph 文件进行内存分析，但这无法应用到线上环境。目前主流的线上检测 OOM 方案有以下几个：

**FBAllocationTracker**

由 Facebook 提出，它会 hook OC 中的 `+alloc` 和 `+ dealloc` 方法，分别在分配和释放内存时增加和减少实例计数。

```objectivec
@implementation NSObject (AllocationTracker)

+ (id)fb_newAlloc
{
 id object = [self fb_originalAlloc];
 AllocationTracker::tracker()->incrementInstanceCountForClass([object class]);
 return object;
}

- (void)fb_newDealloc
{
 AllocationTracker::tracker()->decrementInstanceCountForClass([object class]);
 [self fb_originalDealloc];
}
@end
```

然后，当应用程序运行时，可以定期调用快照方法来记录当前活动的实例数。通过实例数量的异常变化来定位发生OOM的问题。

该方案的问题是无法检测非 OC 对象的内存占用，且没有堆栈信息。

[Reducing FOOMs in the Facebook iOS app](https://engineering.fb.com/2015/08/24/ios/reducing-fooms-in-the-facebook-ios-app/ "Reducing FOOMs in the Facebook iOS app")

**OOMDetector**

这个是腾讯采用的方案。

通过 Hook iOS 系统底层内存分配的相关方法（包括 `malloc_*zone`相关的堆内存分配以及 `vm*_allocate` 对应的 VM 内存分配方法），跟踪并记录进程中每个对象内存的分配信息，包括分配堆栈、累计分配次数、累计分配内存等，这些信息也会被缓存到进程内存中。在内存触顶的时候，组件会定时 Dump 这些堆栈信息到本地磁盘，这样如果程序爆内存了，就可以将爆内存前 Dump 的堆栈数据上报到后台服务器进行分析。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220119232138.png)

[【腾讯开源】iOS爆内存问题解决方案-OOMDetector组件 - 掘金](https://juejin.cn/post/6844903550187733000)

**Memory Graph**

这个是字节采用的方案，基于内存快照生成内存分布情况。线上 Memory Graph 核心的原理是扫描进程中所有 Dirty 内存，通过内存节点中保存的其他内存节点的地址值建立起内存节点之间的引用关系的有向图，用于内存问题的分析定位，整个过程不使用任何私有 API。该方案实现细节未开源，目前已搭载在字节跳动火山引擎旗下应用性能管理平台（[APMInsight](https://www.volcengine.com/product/apminsight "APMInsight")）上，供开发者注册使用。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220120225034.png)

[有一篇文章](https://juejin.cn/post/6895583288451465230 "分析字节跳动解决OOM的在线Memory Graph技术实现")分析了这个方案的实现原理：通过 mach 内核的 `vm_*region_recurse/vm_region_recurse64` 函数遍历进程内所有 VM Region。这里包括二进制，动态库等内存，我们需要的是 Malloc Zone，然后通过 `malloc*_get_all_zones` 获取 libmalloc 内部所有的 zone，并遍历每个 zone 中管理的内存节点，获取 libmalloc 管理的存活的所有内存节点的指针和大小。再根据指针判断是 OC/Swift 对象，还是 C++ 对象，还是普通的 Buffer。

参考：[iOS 性能优化实践：头条抖音如何实现 OOM 崩溃率下降50%+](https://juejin.cn/post/6885144933997494280 "iOS 性能优化实践：头条抖音如何实现 OOM 崩溃率下降50%+")

#### 防劣化

防劣化即防止出现 OOM 的一些手段，可以从以下方面入手：

* 内存泄漏：关于内存泄漏的检测可以见[上期内容](https://mp.weixin.qq.com/s/DNXrfZgx0JaXyvfVZ4sYVA)。

* autoreleasepool：在循环里产生大量临时对象，内存峰值会猛涨，甚至出现 OOM。适当的添加 autoreleasepool 能及时释放内存，降低峰值。

* 大图压缩：可以降低图片采样率。

* 前后台切换：后台更容易发生 OOM，因为后台可利用的内存更小，我们可以在进入后台时考虑释放一些内存。

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
