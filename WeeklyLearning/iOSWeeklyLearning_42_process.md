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

OOM（Out Of Memory）指的是应用内存占用过高被系统强制杀死的情况，通常还会再分为 FOOM 前台 OOM 和 BOOM 后台 OOM 两种。其中 FOOM 是对用户体验影响比较大，急需治理的。

导致 OOM 的原因是应用内存占用过高，所以治理方法就可以分两方面进行：

1、现存代码，查找导致 OOM 的问题进行解决

2、以后代码，对内存使用进行合理的规范

第 2 部分属于防劣化，这个跟业务关联比较大，这里只考虑现存代码的治理。OOM与其他 Crash 不同的一点是它的触发是通过 SIGKILL 信号进行的，常规的 Crash 捕获方案无法捕获这类异常。那么该如何定位呢，目前主流的有以下几个方案：

#### FBAllocationTracker

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

#### OOMDetector

通过Hook iOS系统底层内存分配的相关方法（包括malloc_zone相关的堆内存分配以及vm_allocate对应的VM内存分配方法），跟踪并记录进程中每个对象内存的分配信息，包括分配堆栈、累计分配次数、累计分配内存等，这些信息也会被缓存到进程内存中。在内存触顶的时候，组件会定时Dump这些堆栈信息到本地磁盘，这样如果程序爆内存了，就可以将爆内存前Dump的堆栈数据上报到后台服务器进行分析。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220119232138.png)



[【腾讯开源】iOS爆内存问题解决方案-OOMDetector组件 - 掘金](https://juejin.cn/post/6844903550187733000)



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
