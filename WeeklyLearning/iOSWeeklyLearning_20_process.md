# iOS摸鱼周报 第二十期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> 

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)



## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**对深浅拷贝的理解**。

### 对深浅拷贝的理解

我们先要理解拷贝的目的是：产生一个副本对象，跟源对象互不影响。

深拷贝和浅拷贝：

拷贝类型|拷贝方式|特点
--|--|--
深拷贝|内存拷贝，让目标对象指针和源对象指针指向 `两片` 内容相同的内存空间。|1. 不会增加被拷贝对象的引用计数；<br>2. 产生了一个内存分配，出现了两块内存。
浅拷贝|指针拷贝，对内存地址的复制，让目标对象指针和源对象指针指向 `同一片` 内存空间。|1. 会增加被拷贝对象的引用计数；<br>2. 没有进行新的内存分配。<br>注意：如果是小对象如 NSString，可能通过 Tagged Pointer 来存储，没有引用计数。

简而言之：

* 深拷贝：内容拷贝，产生新对象，不增加对象引用计数
* 浅拷贝：指针拷贝，不产生新对象，增加对象引用计数
* 区别：1. 是否影响了引用计数；2. 是否开辟了新的内存空间

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210724043958.png)


iOS 提供了 2 个拷贝方法：

* copy：不可变拷贝，产生不可变副本
* mutableCopy：可变拷贝，产生可变副本

对 mutable 对象与 immutable 对象 进行 copy 与 mutableCopy 的结果：

源对象类型|拷贝方式|目标对象类型|拷贝类型（深/浅）
:--:|:--:|:--:|:--:
mutable 对象|copy|不可变|深拷贝
mutable 对象|mutableCopy|可变|深拷贝
immutable 对象|copy|不可变|`浅拷贝`
immutable 对象|mutableCopy|可变|深拷贝

>注：这里的 immutable 对象与 mutable 对象指的是系统类 NSArray、NSDictionary、NSSet、NSString、NSData 与它们的可变版本如 NSMutableArray 等。

一个记忆技巧就是：对 immutable 对象进行 copy 操作是 `浅拷贝`，其它情况都是 `深拷贝`。

我们还根据拷贝的目的加深理解：

* 对 immutable 对象进行 copy 操作，产生 immutable 对象，因为源对象和目标对象都不可变，所以进行指针拷贝即可，节省内存
* 对 immutable 对象进行 mutableCopy 操作，产生 mutable 对象，对象类型不同，所以需要深拷贝
* 对 mutable 对象进行 copy 操作，产生 immutable 对象，对象类型不同，所以需要深拷贝
* 对 mutable 对象进行 mutableCopy 操作，产生 mutable 对象，为达到修改源对象或目标对象互不影响的目的，需要深拷贝

#### 使用 copy、mutableCopy 对集合对象进行的深浅拷贝是针对集合对象本身的

使用 copy、mutableCopy 对集合对象（Array、Dictionary、Set）进行的深浅拷贝是针对集合对象本身的，对集合中的对象执行的默认都是浅拷贝。也就是说只拷贝集合对象本身，而不复制其中的数据。主要原因是，集合内的对象未必都能拷贝，而且调用者也未必想在拷贝集合时一并拷贝其中的每个对象。

如果想要深拷贝集合对象本身的同时，也对集合内容进行 copy 操作，可使用类似以下的方法，copyItems 传 YES。但需要注意的是集合中的对象必须都符合 NSCopying 协议，否则会导致 Crash。

```objectivec
NSArray *deepCopyArray = [[NSArray alloc]initWithArray:someArray copyItems:YES];
```

但是，如果集合中的对象的 copy 操作是浅拷贝，那么对于集合来说还不是真正意义上的深拷贝。比如，你需要对一个 `NSArray<NSArray *>` 对象进行真正的深拷贝，那么内层数组及其内容也应该执行深拷贝，可以对该集合对象进行 `归档` 然后 `解档`，只要集合中的对象都符合 NSCoding 协议。而且，使用这种方式，无论集合中存储的模型对象嵌套多少层，都可以实现深拷贝，但前提是嵌套的子模型也需要符合 NSCoding 协议才行，否则会导致 Crash。

```objectivec
NSArray *trueDeepCopyArray = [NSKeyedUnarchiver unarchiveObjectWithData:[NSKeyedArchiver archivedDataWithRootObject:oldArray]];
```

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210724054744.png)


需要注意的是，使用 initWithArray:copyItems: 并将 copyItems 传 YES 时，需要注意生成的副本集合对象中的对象（下一个级别）是不可变的，所有更深的级别都具有它们以前的可变性。比如以下代码将 Crash。

```objectivec
NSArray *oldArray = @[@[].mutableCopy];
NSArray *deepCopyArray = [[NSArray alloc] initWithArray:oldArray copyItems:YES];
NSMutableArray *mArray = deepCopyArray[0]; // deepCopyArray[0] 已经被深拷贝为 NSArray 对象
[mArray addObject:@""]; // Crash
```
而 `归档解档集合` 的方式会保留所有级别的可变性，就像以前一样。

#### 实现对自定义对象的拷贝

如果想要实现对自定义对象的拷贝，需要遵守 `NSCopying` 协议，并实现 `copyWithZone:` 方法。

* 如果要浅拷贝，`copyWithZone:` 方法就返回当前对象：return self；
* 如果要深拷贝，`copyWithZone:` 方法中就创建新对象，并给希望拷贝的属性赋值，然后将其返回。如果有嵌套的子模型也需要深拷贝，那么子模型也需符合 NSCopying 协议，且在属性赋值时调用子模型的 copy 方法，以此类推。

如果自定义对象支持可变拷贝和不可变拷贝，那么还需要遵守 `NSMutableCopying` 协议，并实现 `mutableCopyWithZone:` 方法，返回可变副本。而 `copyWithZone:` 方法返回不可变副本。使用方可根据需要调用该对象的 copy 或 mutableCopy 方法来进行不可变拷贝或可变拷贝。

#### 以下代码会出现什么问题？

```objectivec
@property (nonatomic, copy) NSMutableArray *array;
```

不论赋值过来的是 NSMutableArray 还是 NSArray 对象，进行 copy 操作后都是 NSArray 对象（深拷贝）。由于属性被声明为 NSMutableArray 类型，就不可避免的会有调用方去调用它的添加对象、移除对象等一些方法，此时由于 copy 的结果是 NSArray 对象，所以就会导致 Crash。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`包大小优化`

1、[今日头条 iOS 安装包大小优化—— 新阶段、新实践](https://www.infoq.cn/article/iowjwhbirqeobzf5m2o8) -- 来自InfoQ：字节跳动技术团队


在多个渠道多次推荐的老文章了，再次推荐还是希望能跟大家一块打开思路，尤其在二进制文件的控制上，目前还有很多比较深入的手段去优化，资源的优化可能并不是全部的手段。


2、[今日头条优化实践： iOS 包大小二进制优化，一行代码减少 60 MB 下载大小](https://www.infoq.cn/article/XUJL32hTDKYqAKz0hkMM) -- 来自InfoQ：字节跳动技术团队


上篇文章的姊妹篇，也是大家比较熟悉的文章了。总而言之段迁移技术效果很明显，但是段迁移会带来一些其他的问题，比如文中提到的日志解析问题。我们在实践过程中也遇到了各种各样的小问题，一些二进制分析工具会失效，需要针对段迁移的ipa做适配。


3、[基于mach-o+反汇编的无用类检测](https://www.jianshu.com/p/c41ad330e81c) -- 来自简书：皮拉夫大王


很少在周报中推荐自己的文章，尤其是自己2年前的老文章。推荐这篇文章的原因是我在文中列举了58各个业务线的包大小占比分析。从数据中可以看出我们经过多年包大小治理后，资源的优化空间并不大，只能从二进制文件的瘦身上入手。可能很多公司的APP也有同样的问题，就是资源瘦身已经没有太大的空间了，这时我们就应该从二进制层面寻找突破口。文中工具地址：[Github WBBlades](https://github.com/wuba/WBBlades)


4、[Flutter包大小治理上的探索与实践](https://tech.meituan.com/2020/09/18/flutter-in-meituan.html) -- 来自美团技术团队：艳东 宗文 会超


谈点新鲜的内容。作者首先对Flutter的包大小进行了细致的分析，并在双平台选择了不同的优化方案。在Android平台选择动态下发，而iOS平台则将部分非指令数据进行动态下发。通过修改Flutter的编译后端将data重定向输入到文件，从而实现了数据段与文本段的拆分。使用Flutter的团队可以关注下这个方案。

5、[iOS 优化 - 瘦身](https://mp.weixin.qq.com/s/wDcYvea5dTq0dh0PBwRu4A) -- 来自微信公众号：CoderStar


文章详细介绍了APP瘦身的技巧与方案，包括资源和代码层面。对图片压缩与代码的编译选项有深入的解释。方案比较全面，可以通过此文章检查APP瘦身是否还有哪些方案没有应用。


6、[科普：为什么iOS的APP比安卓大好几倍？](https://www.jianshu.com/p/6f2adc5aeb9a) -- 来自简书：春暖花已开


前几篇文章已经将瘦身的技术介绍的比较完善了。接下来通过这篇文章回答下老板们经常会问道的问题：为什么iOS的包比安卓的大？是因为iOS的技术不如安卓吗？建议iOS程序员都看看这个问题，至少可以满足我们自己的好奇心。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Better Explaine

地址：https://betterexplained.com/

Better Explaine 是一个帮助你真正理解数学概念、使数学概念变得有趣的网站，在这个网站你可以看到很多复杂的概念被分解成图形、公式和通俗易懂的解释。网站的指导思想是爱因斯坦的这句话：“如果你不能简单地解释它，你就没有充分地理解它”，这里没有装腔作势，没有古板老师，只是一个兴奋的朋友在分享究竟是什么让一个想法变成了现实！

### 程序员可能必读书单推荐

地址：https://draveness.me//books-1

来自 [Draveness](https://draveness.me/) 的程序员书单，这是书单的系列一，后面应该还会有后续的推荐。这次的推荐中推荐了三本「大部头」：SICP、CTMCP 和 DDIA。即使你和小编一样对感觉这些书晦涩难懂（苦笑），并不准备阅读，也可以从 Draveness 的这篇书单推荐中窥探一眼别人的编程世界是什么样的😉。

## 工具推荐

整理编辑：[CoderStar](https://juejin.cn/user/588993964541288/posts)
### Snipaste
**地址**： https://zh.snipaste.com/

**软件状态**： 普通版免费，专业版收费，有Mac、Windows两个版本

**软件介绍**

Snipaste 是一个简单但强大的截图工具，也可以让你将截图贴回到屏幕上！普通版的功能已经足够使用，笔者认为是最好用的截图软件了！（下图是官方图）
![Snipaste](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/N3QEb3VA.png)
### LSUnusedResources
**地址**： https://github.com/tinymind/LSUnusedResources

**软件状态**： 免费

**软件介绍**

一个 Mac 应用程序，用于在 Xcode 项目中查找未使用的图像和资源，可以辅助我们优化包体积大小。

![LSUnusedResources](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/LSUnusedResourcesExample.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
