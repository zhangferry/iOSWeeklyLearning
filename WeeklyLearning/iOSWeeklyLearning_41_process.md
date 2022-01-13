1# iOS 摸鱼周报 第四十一期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * Tips：在 Objective-C 中标记构造器为指定构造器。
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

### In-App Events 数据分析可以查看了

In-App Events 的展示效果数据可以在 App Store Connect 中的应用分析查看了。应用分析还包括事件的页面展示，提醒和通知数据，以及由你的 In-App Events 触发的下载和重新下载的数量。每个指标都可以根据区域、资源类型、设备等进行查看，这样你就可以了解 In-App Events 是如何影响应用的发展和成功的了。

[Analytics now available for in-app events](https://developer.apple.com/news/?id=pa0x2dzk "Analytics now available for in-app events")

### 线上直播沙龙 - 抖音 iOS 基础技术大揭秘

**内容介绍**：如何保证抖音 App 的稳定性？如何给用户带来如丝般柔滑的流畅体验？如何在用户弱感知甚至无感知的情况下，推进抖音 App 的架构演进？如何利用容器等技术推进自动化测试？字节自研的 iOS 构建系统 JOJO 又是如何实现超级 App 构建效能提升 40% 的？本期字节跳动技术沙龙将以《抖音 iOS 基础技术大揭秘》为主题，为你全面揭开抖音 iOS 基础技术背后的技术能力！

**沙龙时间**：2022 年 1 月 22 日 14:00-17:25

**报名地址**：[百格活动](https://www.bagevent.com/event/sales/i843tlja9we9xhc7ujim43jiaxn15sdl?code=0617daGa1vyXqC0aiPGa1cZLRM07daGm&state=STATE "线上直播沙龙-抖音iOS基础技术大揭秘")

## 开发 Tips

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

### 在 Objective-C 中标记构造器为指定构造器

这是一个开发 tip，一个编码规范，也是快手的一道面试真题。

指定构造器模式有助于确保继承的构造器正确地初始化所有实例变量。指定构造器通常为类中接收全部初始化参数的全能构造器，是类中最重要的构造器；便利构造器通常为接收部分初始化参数的构造器，它们调用当前类的其它构造器，并为一些参数赋默认值。便利构造器是类中比较次要的、辅助型的构造器。

Objective-C 类的指定构造器模式和 Swift 的略有不同。在 Objective-C 中，为了明确区分指定构造器和便利构造器，可以使用宏 `NS_DESIGNATED_INITIALIZER` 标记构造器为指定构造器，其它未添加该宏的构造器都成为了便利构造器。

```objectivec
- (instancetype)init NS_DESIGNATED_INITIALIZER;
```

使用这个宏会引入一些规则：

1. 指定构造器的实现只能且必须`向上代理`到父类的一个指定构造器（with `[super init...]`）；
2. 便利构造器的实现只能且必须`横向代理`到当前类的另一个构造器（with `[self init...]`），最终需要在当前类的指定构造器处终止链；
3. 如果一个类提供了一个或多个指定构造器，它必须覆写其父类的所有指定构造器作为（退化为）该类的便利构造器，并让其满足条件 2。这样才能保证子类新增的实例变量得到正确的初始化。

如果违反了以上任何规则，将会得到编译器的警告。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220112232618.png)

简单来说，指定构造器必须总是`向上代理`，便利构造器必须总是`横向代理`。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220112232822.png)

另外，在 Objective-C 中，你还必须覆写父类的所有指定构造器退化为子类的便利构造器，并且要遵循便利构造器的实现规则；而 Swift 则不用，因为 Swift 中的子类默认情况下不会继承父类的构造器，仅会在安全和适当的某些情况下被继承。Swift 的这种机制可以防止一个父类的简单构造器被一个更精细的子类继承，而在用来创建子类时的新实例时没有完全或错误被初始化。

在 Objective-C 中，使用宏 `NS_DESIGNATED_INITIALIZER` 标记构造器为指定构造器，可以充分发挥编译器的特性帮我们找出初始化过程中可能存在的漏洞（通过警告），有助于确保继承的构造器正确地初始化所有实例变量，让构造过程更完整，增强代码的健壮性。

示例代码：

```objective-c
@interface MyClass : NSObject
- (instancetype)initWithTitle:(nullable NSString *)title subtitle:(nullable NSString *)subtitle NS_DESIGNATED_INITIALIZER;
- (instancetype)initWithTitle:(nullable NSString *)title;
- (instancetype)init;
@end
  
@implementation MyClass
  
- (instancetype)initWithTitle:(nullable NSString *)title subtitle:(nullable NSString *)subtitle {
    self = [super init]; // [规则1] 指定构造器只能向上代理到父类指定构造器，否则会得到编译器警告：Designated initializer should only invoke a designated initializer on 'super'
    if (self) {
        _title = [title copy];
        _subtitle = [subtitle copy];
    }
    return self;
}

- (instancetype)initWithTitle:(nullable NSString *)title {
/* 
    return [super init]; 
    [规则2] 当该类设定了指定构造器也就是使用了 NS_DESIGNATED_INITIALIZER 后，其它非指定构造器都变成了便利构造器。
    便利构造器只能横向代理到该类的指定构造器，或者通过横向代理到其它便利构造器最后间接代理到该类的指定构造器。
    这里调用 [super init] 的话会得到编译器警告：
    	- Convenience initializer missing a 'self' call to another initializer
    	- Convenience initializer should not invoke an initializer on 'super'
 */
    return [self initWithTitle:title subtitle:nil];
}

// [规则3] 如果子类提供了指定构造器，那么需要重写所有父类的指定构造器为子类的便利构造器，保证子类新增的实例变量能够被正确初始化，以让构造过程更完整。
// 这里需要重写 -init，否则会得到编译器警告：Method override for the designated initializer of the superclass '-init' not found
- (instancetype)init {
    return [self initWithTitle:nil];
}

@end
```

## 面试解析

整理编辑：[张飞](https://juejin.cn/user/782508012091645/posts)

### 如何检测内存泄露

检测内存泄露有多种方案，大体可以分为两类：工具和代码。

#### 工具类

工具类比较多：

* Instruments 里的 Leaks

* Memory Graph Debugger

* Schems 里的 Memory Management

* XCTest 中的 XCTMemoryMetric

前两种方式比较常见，后两种内存泄露还需要借助于 Xcode 导出的 memgraph 文件，结合 `leaks`、`malloc_history` 等命令行工具进行分析。工具类检测方案都有一个缺点就是比较繁琐，开发阶段很容易遗漏，所以基于代码的自动化内存泄露检测方案更适合使用。

#### 代码类

代码类检测泄露方式有三个典型的库。

**MLeaksFinder**

地址：https://github.com/Tencent/MLeaksFinder

它的基本原理是这样的，当一个 ViewController 被 pop 或 dismiss 之后，我们认为该 ViewController，包括它上面的子 ViewController，以及它的 View，View 的 subView 等等，都很快会被释放，如果某个 View 或者 ViewController 没释放，我们就认为该对象泄漏了。

它是基于 Method Swizzled 方式，需要 Hook ViewController 的 `viewDidDisappear` ，`viewWillAppear` 等方法。所以仅适用于 Objective-C 项目。

**LifetimeTracker**

地址：https://github.com/krzysztofzablocki/LifetimeTracker

LifetimeTracker 是使用 Swift 实现的，可以同时支持 OC 和 Swift 项目。它的原理是用一个协议表达监听泄露能力，我们提前设置监听入口和允许存在的对象个数。内部维护一个类似引用计数一样的数值，进入监听会进行一个 +1 操作，还会监听该对象的 `deinit` 方法，如果调用执行 `-1`。如果该「引用计数」大于我们设置的最大对象个数，就触发可视化的泄露警告。

简化一些流程之后的代码：

```swift
internal func track(_ instance: Any, configuration: LifetimeConfiguration, file: String = #file) {
    let instanceType = type(of: instance)
    let configuration = configuration
    configuration.instanceName = String(reflecting: instanceType)

    func update(_ configuration: LifetimeConfiguration, with countDelta: Int) {
        let groupName = configuration.groupName ?? Constants.Identifier.EntryGroup.none
        let group = self.trackedGroups[groupName] ?? EntriesGroup(name: groupName)
        group.updateEntry(configuration, with: countDelta)
        // 检测当前计数是否大于最大引用数
        if let entry = group.entries[configuration.instanceName], entry.count > entry.maxCount {
            self.onLeakDetected?(entry, group)
        }
        self.trackedGroups[groupName] = group
    }
    // 开始检测，计数+1
    update(configuration, with: +1)

    onDealloc(of: instance) {
        // 执行deinit，计数-1
        update(configuration, with: -1)
    }
}
```

**FBRetainCycleDetector**

地址：https://github.com/facebook/FBRetainCycleDetector

上面两种方案都是粗略的检测，是 ViewController 或者 View 级别的，要想知道更具体的信息，到底哪里导致的循环应用就无能为力了。而 FBRetainCycleDetector 就是用于解决这类问题，因为需要借助 OC 的动态特性，所以该库无法在 Swift 项目中发挥作用。

它的实现相对上面两个方案更复杂一些，大致原理是基于`DFS`算法，把整个对象之间的强引用关系当做图进行处理，查找其中的环，就找到了循环引用。

核心是寻找对象之间的强引用关系，在 OC 语言中，强引用关系主要发生在这三种场景里，针对这三种场景也有不同的处理方案：

**类的成员变量**

通过`runtime`的`class_getIvarLayout`获取描述该类成员变量的布局信息，然后通过`ivar_getOffset`遍历获取成员变量在类结构中的偏移地址，然后获取强引用变量的集合。

**关联对象**

利用 fishhook hook `objc_setAssociatedObject` 和 `objc_removeAssociatedObjects` 这两个方法，对通过`OBJC_ASSOCIATION_RETAIN`和`OBJC_ASSOCIATION_RETAIN_NONATOMIC`策略进行关联的对象进行保存。

**block持有**

理解这个原理还需要再回顾下 block 的内存布局，FBRetainCycleDetector 对 block 结构体进行了等价的封装：

```c
struct BlockLiteral {
    void *isa;
    int flags;
    int reserved;
    void (*invoke)(void *, ...);
    struct BlockDescriptor *descriptor;
    // imported variables
};

struct BlockDescriptor {
  unsigned long int reserved;                // NULL
  unsigned long int size;
  // optional helper functions
  void (*copy_helper)(void *dst, void *src); // IFF (1<<25)
  void (*dispose_helper)(void *src);         // IFF (1<<25)
  const char *signature;                     // IFF (1<<30)
};
```

在 `BlockLiteral` 结构体的 descriptor 字段之后的位置会存放 block 持有的对象，但是并非所有对象都是我们需要的，我们只需要处理强引用对象即可。而恰恰 block 的引用对象排列基于寻址长度对齐，较大地址放在前面，且强引用对象会排在弱引用之前，所以从 descriptor 之后的成员变量，可以按固定的指针长度依次取出对象。这之后的对象用 `FBBlockStrongRelationDetector` 封装，但这有可能会多取对象，比如 weak 类型的引用其实是不需要捕捉的。

该库的做法是重写 `FBBlockStrongRelationDetector` 对象的 release 方法，仅设置标记位，然后外部调用它的 dispose 方法，这样其强引用对象都会调用 release，被调用这部分都是强引用对象。

```objectivec
static NSIndexSet *_GetBlockStrongLayout(void *block) {
	...
	void (*dispose_helper)(void *src) = blockLiteral->descriptor->dispose_helper;
	const size_t ptrSize = sizeof(void *);	
	const size_t elements = (blockLiteral->descriptor->size + ptrSize - 1) / ptrSize;
	
	void *obj[elements];
	void *detectors[elements];
	
	for (size_t i = 0; i < elements; ++i) {
		FBBlockStrongRelationDetector *detector = [FBBlockStrongRelationDetector new];
		obj[i] = detectors[i] = detector;
	}
	
	@autoreleasepool {
		dispose_helper(obj);
	}
	...
}
```

当拿到以上所有强引用关系时就可以利用 DFS 深度优先搜索遍历引用树，查找是否有环形引用了。

FBRetainCycleDetector 的检测方案明显更复杂、更耗时，所以几乎不可能针对所有对象都进行检测，所以更好的方案是配合 MLeaksFinder 或者 facebook 自己的 [FBAllocationTracker](https://github.com/facebookarchive/FBAllocationTracker "FBAllocationTracker")，先找到潜在泄露对象，然后分析这些对象的强引用关系，查找是否存在循环引用。

**其他方案**

在资料查找过程中还发现了另一个库 [BlockStrongReferenceObject](https://github.com/tripleCC/Laboratory/tree/master/BlockStrongReferenceObject ""BlockStrongReferenceObject) ，它只检测 Block 导致的循环引用问题，跟 FBRetainCycleDetector 类似，也是要分析 block 内存布局。但不同的是，它可以完全根据内存布局，来定位到强引用对象，主要是依据 block 和 clang 源码进行分析得出，这里真的非常强👍🏻，如果对实现细节感兴趣可以阅读这篇文章：[聊聊循环引用的检测](https://triplecc.github.io/2019/08/15/%E8%81%8A%E8%81%8A%E5%BE%AA%E7%8E%AF%E5%BC%95%E7%94%A8%E7%9A%84%E6%A3%80%E6%B5%8B/ "聊聊循环引用的检测")。

参考：

[检测和诊断 App 内存问题](https://mp.weixin.qq.com/s/E80VEIJma66fj7BZy1cCeQ)

[draveness的源码分析 - FBRetainCycleDetector](https://github.com/draveness/analyze/tree/master/contents/FBRetainCycleDetector "draveness的源码分析 - FBRetainCycleDetector")

## 优秀博客

整理编辑：[皮拉夫大王在此](https://juejin.cn/user/281104094332653)

1、[大白健康系统--iOS APP运行时Crash自动修复系统](https://neyoufan.github.io/2017/01/13/ios/BayMax_HTSafetyGuard/)

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：整个文章是非常经典的，作者介绍通过method swizzling替换NSObject的allocWithZone方法和dealloc方法实现野指针拦截。

2、[JJException](https://github.com/jezzmemo/JJException)

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：这个库需要自己指定探测哪些类对应的野指针。换句话说，就是我们自己指定10个类，那么这10个类的对象发生野指针时我们才能发现。如果在此之外，野指针监控不到。

3、[iOS 野指针定位:野指针嗅探器](https://www.jianshu.com/p/9fd4dc046046)
[@皮拉夫大王](https://juejin.cn/user/281104094332653)：文章介绍了2个方案：（1）在开发阶段破坏内存，使野指针必现崩溃(野指针可能由于内存释放但未被写入导致崩溃不必现)。在free时，并不释放内存，保留内存，判断是否为objc对象，如果是objc对象则将对象setclass为自定义类，借助消息转发得到堆栈和类信息。监听系统内存警告，收到警告后释放。（2）hook objc的dealloc 方法，在dealloc时判断是否需要开启野指针探测，如果不需要则直接释放，否则将对象修改isa后保留并加入到内存池中，再次调用对象时会触发消息转发拦截到堆栈及对象类名信息。

4、[iOS野指针定位总结](https://juejin.cn/post/6844903747538141191)

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：文章介绍方案如下：分类覆盖dealloc函数，并在dealloc 中重新设置isa并不释放obj，其中重新指向的isa是动态创建的。也就是说dealloc是10000个类，也会同步动态创建10000个类。

5、[浅谈 iOS 中的 Crash 捕获与防护](http://shevakuilin.com/ios-crashprotection/)

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：推荐阅读的文章，文章不仅仅介绍了野指针相关内容，还介绍了崩溃相关的基础知识。

6、[xiejunyi'Blog](https://junyixie.github.io/categories/APM/)

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：坦白讲我并没有看完的文章，在做技术调研时发现的博客，文章内容比较深入并且能看出作者是有大量实战经验的开发者，因此推荐给大家。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Visual Web Skills

地址：https://andreasbm.github.io/web-skills/

这是一份可视化的 Web 技能列表，它对刚开始学习 Web 或已经工作多年并想学习新东西的人都很有用，你可以从中了解 Web 开发的大概路径和图谱，按顺序或者选择自己感兴趣的部分来看。除此之外最吸引人的是这个列表可视化的非常棒，每个图标符号都很大方美观形象，快来看一下！

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Web%20Skills.png)

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### SwiftInfo

**地址**：https://github.com/rockbruno/SwiftInfo

**软件状态**：开源、免费

**软件介绍**：

`SwiftInfo` 是一个 `CLI` 工具，用于提取、跟踪和分析对 `Swift` 应用程序有用的指标。除了该工具附带的默认跟踪选项外，还支持自定义编写`.Swift`脚本来实现额外的功能。

默认支持的工具包括：

- IPASizeProvider
- WarningCountProvider
- LinesOfCodeProvider
- ...

更多细节请直接前往 repo homepage 查看。

![SwiftInfo](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220112183759.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS 成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
