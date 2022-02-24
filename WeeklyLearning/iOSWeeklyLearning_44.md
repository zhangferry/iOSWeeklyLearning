# iOS摸鱼周报 第四十四期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：Apple 将推出 Tap to Pay 功能
> * Tips：解决 iOS 15 上 APP 莫名其妙地退出登录
> * 面试模块：Dealloc 使用注意事项及解析
> * 优秀博客：ARM64 汇编入门及应用
> * 学习资料：Github: How to Cook
> * 开发工具：文件搜索应用：EasyFind

## 本期话题

[@zhangferry](https://zhangferry.com)：Apple 将在 iPhone 上推出 Tap to Pay 功能，即可以通过简单的操作行为 -- 轻触，完成在商户端的付款过程。该功能通过 NFC 实现，非常安全，支持 Apple Pay、非接触式信用卡、借记卡以及其他数字钱包，这意味着 iPhone 将具备类似 POS 的功能，客户可以直接在商户的 iPhone 上刷信用卡进行消费。该功能仅 iPhone XS 及之后的机型支持。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Apple_Apple-Pay_Payment_inline.jpg.large_2x.jpg)

Stripe 将成为第一个在 iPhone 上向其商业客户提供 Tap to Pay 的支付平台。其他支付平台和应用程序将在今年晚些时候推出。

[Apple empowers businesses to accept contactless payments through Tap to Pay on iPhone](https://www.apple.com/newsroom/2022/02/apple-unveils-contactless-payments-via-tap-to-pay-on-iphone/ "Apple empowers businesses to accept contactless payments through Tap to Pay on iPhone")

## 开发Tips

整理编辑：[FBY展菲](https://github.com/fanbaoying)

### 解决 iOS 15 上 APP 莫名其妙地退出登录

#### 复现问题

在 iOS 15 正式版推出后， 我们开始收到用户的反馈：在打开我们的App (Cookpad) 时，用户莫名其妙地被强制退出帐号并返回到登录页。非常令人惊讶的是，我们在测试 iOS 15 beta 版的时候并没有发现这个问题。

我们没有视频，也没有具体的步骤来重现这个问题，所以我努力尝试以各种方式启动应用程序，希望能亲手重现它。我试着重新安装应用程序，我试着在有网络连接和没有网络连接的情况下启动，我试着强制退出，经过 30 分钟的努力，我放弃了，我开始回复用户说我没找到具体问题。

直到我再次解锁手机，没有做任何操作，就启动了 Cookpad，我发现 APP 就像我们的用户所反馈的那样，直接退出到了登录界面！

在那之后，我无法准确的复现该问题，但似乎与暂停使用手机一段时间后再次使用它有关。

#### 缩小问题范围
我担心从 Xcode 重新安装应用程序可能会影响问题的复现，所以我首先检查代码并试图缩小问题的范围。根据我们的实现，我想出了三个怀疑的原因。

- 1、`UserDefaults` 中的数据被清除。
- 2、一个意外的 API 调用返回 HTTP 401 并触发退出登录。
- 3、`Keychain` 抛出了一个错误。

我能够排除前两个潜在的原因，这要归功于我在自己重现该问题后观察到的一些微妙行为。

- 登录界面没有要求我选择地区 —— 这表明 `UserDefaults` 中的数据没有问题，因为我们的 "已显示地区选择 "偏好设置仍然生效。
- 主用户界面没有显示，即使是短暂的也没有 —— 这表明没有尝试进行网络请求，所以 API 是问题原因可能还为时过早。

这就把`Keychain`留给了我们，指引我进入下一个问题。是什么发生了改变以及为什么它如此难以复现？

#### 寻找根本原因
我的调试界面很有用，但它缺少了一些有助于回答所有问题的重要信息：**时间**。

我知道在 `AppDelegate.application(_:didFinishLaunchingWithOptions:)` 之前，“受保护的数据” 是不可用的，但它仍然没有意义，因为为了重现这个问题，我正在执行以下操作：

1、启动应用程序
2、简单使用
3、强制退出应用
4、锁定我的设备并将其放置约  30 分钟
5、解锁设备
6、再次启动应用

每当我在第 6 步中再次启动应用程序时，我 100% 确定设备已解锁，因此我坚信我应该能够从 `AppDelegate.init() ` 中的 `Keychain ` 读取数据。

直到我看了所有这些步骤的时间，事情才开始变得有点意义。

![](https://images.xiaozhuanlan.com/photo/2021/ffa4e4a3730d3fd5ed1891fa73539f24.png)

再次仔细查看时间戳：
- `main.swift` — 11:38:47
- `AppDelegate.init()` — 11:38:47
- `AppDelegate.application(_:didFinishLaunchingWithOptions:)` — 12:03:04
- `ViewController.viewDidAppear(_:)` — 12:03:04

在我真正解锁手机并点击应用图标之前的 25 分钟，应用程序本身就已经启动了！

现在，我实际上从未想过有这么大的延迟，实际上是 [@_saagarjha](https://twitter.com/_saagarjha) 建议我检查时间戳，之后，他指给我看这条推特。

![](https://images.xiaozhuanlan.com/photo/2021/6ea72a16b7326fe97fcdfd33c4758f6d.png)

> 推特翻译：
> 有趣的 iOS 15 优化。Duet 现在试图先发制人地 "预热" 第三方应用程序，在你点击一个应用程序图标前几分钟，通过 dyld 和预主静态初始化器运行它们。然后，该应用程序被暂停，随后的 "启动" 似乎更快。

现在一切都说得通了。我们最初没有测试到它，因为我们很可能没有给 iOS 15 beta 版足够的时间来 "学习" 我们的使用习惯，所以这个问题只在现实世界的场景中再现，即设备认为我很快就要启动应用程序。我仍然不知道这种预测是如何形成的，但我只想把它归结为 "Siri 智能"，然后就到此为止了。

#### 结论

从 iOS 15 开始，系统可能决定在用户实际尝试打开你的应用程序之前对其进行 "预热"，这可能会增加受保护的数据在你认为应该无法使用的时候的被访问概率。

通过等待 `application(_:didFinishLaunchingWithOptions:)` 委托回调来保护自己，如果可能的话，留意 `UIApplication.isProtectedDataAvailable`（或对应委托的回调/通知）并相应处理。

我们仍然发现了非常少的非致命问题，在 `application(_:didFinishLaunchingWithOptions:)` 中报告 `isProtectedDataAvailable`为 `false`，在我们可以推迟从钥匙串阅读的访问令牌之外，这将是一个大规模的任务，现在它不值得进行进一步调查。

参考：[解决 iOS 15 上 APP 莫名其妙地退出登录 - Swift社区](https://mp.weixin.qq.com/s/_a5DddYgQHKREi5VoEeJyg)


## 面试解析

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Dealloc 使用注意事项及解析

关于 Dealloc 的相关面试题以及应用， 周报里已经有所提及。例如 [三十八期：dealloc 在哪个线程执行](https://mp.weixin.qq.com/s/a1aOOn1sFh5EaxISz5tAxA) 和 [四十二期：OOM 治理 FBAllocationTracker 实现原理](https://mp.weixin.qq.com/s/ybANWeLNHPOTkr5_alha9g)，可以结合今天的使用注意事项一起学习。

#### 避免在 dealloc 中使用属性访问

在很多资料中，都明确指出，应该尽量避免在 dealloc 中通过属性访问，而是用成员变量替代。

> 在初始化方法和 dealloc 方法中，总是应该直接通过实例变量来读写数据。- 《Effective Objective-C 2.0》第七条
>
> Always use accessor methods. Except in initializer methods and dealloc. -  WWDC 2012 Session 413 - Migrating to Modern Objective-C
>
> The only places you shouldn’t use accessor methods to set an instance variable are in initializer methods and dealloc. - [Practical Memory Management](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/mmPractical.html#//apple_ref/doc/uid/TP40004447-SW4)

除了可以提升访问效率，也可以防止发生 crash。有文章介绍 crash 的原因是：析构过程中，类结构不再完整，当使用 `accessor` 时，实际是向当前实例发送消息，此时可能会存在 crash。

> 笔者对这里也不是很理解，根据 `debug`  分析析构过程实际是优先调用了实例覆写的 `dealloc`  后，才依次处理 `superclass 的 dealloc`、 `cxx_destruct` 、`Associated`、`Weak Reference`、`Side Table`等结构的，最后执行 `free`，所以不应该发生结构破坏导致的 crash，希望有了解的同学指教一下

笔者个人的理解是：Apple 做这种要求的原因是不想让子类影响父类的构造和析构过程。例如以下代码，子类通过覆写了 `Associated`方 法， 会影响到父类的 `dealloc` 过程。

```objective-c
@interface HWObject : NSObject
@property(nonatomic) NSString* info;
@end
    
@implementation HWObject
- (void)dealloc
{
    self.info = nil;
}
- (void)setInfo:(NSString *)info {
    if (info)
    {
        _info = info;
        NSLog(@"%@",[NSString stringWithString:info]);
    }
}
@end

@interface HWSubObject : HWObject
@property (nonatomic) NSString* debugInfo;
@end

@implementation HWSubObject
- (void)setInfo:(NSString *)info {
    NSLog(@"%@",[NSString stringWithString:self.debugInfo]);
}
- (void)dealloc {
    _debugInfo = nil;
}
- (instancetype)init {
    if (self = [super init]) {
        _debugInfo = @"This is SubClass";
    }
    return self;
}
@end
```

造成 crash 的原因是 `HWSubObject:dealloc()` 中释放了变量 `debugInfo`，然后调用 `HWObject:dealloc()` ，该函数使用 `Associated` 设置 `info` ，由于子类覆写了 `setInfo`，所以执行子类 `setInfo`。该函数内使用了已经被释放的变量 `debugInfo`。**正如上面说的， 子类通过重写 Associated，最终影响到了父类的析构过程。**

#### dealloc 是什么时候释放变量的

其实在 `dealloc` 中无需开发处理成员变量， 当系统调用 `dealloc`时会自动调用析构函数（`.cxx_destruct`）释放变量，参考源码调用链：`[NSObject dealloc] => _objc_rootDealloc => rootDealloc => object_dispose => objc_destructInstance => object_cxxDestruct => object_cxxDestructFromClass `

```cpp
static void object_cxxDestructFromClass(id obj, Class cls)
{
    // 遍历 self & superclass
        // SEL_cxx_destruct 是在 map_images 时在 Sel_init 中赋值的， 其实就是 .cxx_destruct 函数
        dtor = (void(*)(id))
            lookupMethodInClassAndLoadCache(cls, SEL_cxx_destruct);
            // 执行
            (*dtor)(obj);
        }
    }
}
```

沿着 superClass 链通过 `lookupMethodInClassAndLoadCache `去查询 `SEL_cxx_destruct`函数，查找到调用。`SEL_cxx_destruct` 是 `objc` 在初始化调用 `map_images` 时，在 `Sel_init` 中赋值的，值就是 `.cxx_destruct`。

而 `cxx_destruct` 就是用于释放变量的，当类中新增了变量后，会自动插入该函数，这里可以通过 `LLDB watchpoint ` 监听实例的属性值变化， 然后查看堆栈信息验证。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/weekly_44_interview_02.jpg)

#### 避免在 dealloc 中使用 __weak

```objective-c
- (void)dealloc {
    __weak typeof(self) weakSelf = self;
}
```

当在 `dealloc`中使用了 `__weak` 后会直接 crash，报错信息为：`Cannot form weak reference to instance (0x2813c4d90) of class xxx. It is possible that this object was over-released, or is in the process of deallocation.` 报错原因是 `runtime` 在存储弱引用计数过程中判断了当前对象是否正在析构中， 如果正在析构则抛出异常

核心源码如下：

```cpp
id  weak_register_no_lock(weak_table_t *weak_table, id referent_id,   id *referrer_id, WeakRegisterDeallocatingOptions deallocatingOptions) {
    // ... 省略
        if (deallocating) {
            if (deallocatingOptions == CrashIfDeallocating) {
                _objc_fatal("Cannot form weak reference to instance (%p) of " "class %s. It is possible that this object was " "over-released, or is in the process of deallocation.", (void*)referent, object_getClassName((id)referent));
            } 
    // ... 省略
}

```

#### 避免在 dealloc 中使用 GCD

例如一个经常在子线程中使用的类，内部需要使用 `NSTimer` 定时器，定时器由于需要加到 NSRunloop 中，为了简单，这里加到了主线程， 而定时器有一个特殊性：**定时器的释放和创建必须在同一个线程**，所以释放也需要在主线程，示例代码如下（*以上代码仅作为示例代码，并非实际开发使用*）：

```objective-c
- (void)dealloc {
		[self invalidateTimer];
}

- (void)fireTimer {
    __weak typeof(self) weakSelf = self;
    dispatch_async(dispatch_get_main_queue(), ^{
        if (!weakSelf.timer) {
            weakSelf.timer = [NSTimer scheduledTimerWithTimeInterval:1.0 repeats:YES block:^(NSTimer * _Nonnull timer) {
                NSLog(@"TestDeallocModel timer:%p", timer);
            }];
            [[NSRunLoop currentRunLoop] addTimer:weakSelf.timer forMode:NSRunLoopCommonModes];
        }
    });
}

- (void)invalidateTimer {
    dispatch_async(dispatch_get_main_queue(), ^{
        //  crash 位置
        if (self.timer) {
            NSLog(@"TestDeallocModel invalidateTimer:%p model:%p", self->_timer, self);
            [self.timer invalidate];
            self.timer = nil;
        }
    });
}
- (vodi)main {
    dispatch_async(dispatch_get_global_queue(0, 0), ^{
        HWSubObject *obj = [[HWSubObject alloc] init];
        [obj fireTimer];
    });
}
```

代码会在`invalidateTimer::if (self.timer)` 处发生 crash， 报错为 `EXC_BAD_ACCESS`。原因很简单，因为 `dealloc`最终会调用 `free()`释放内存空间，而后 `GCD`再访问到 `self` 时已经是野指针，所以报错。

>  可以使用 `performSelector`代替 `GCD`实现， 确保线程操作先于 dealloc 完成。

总结：面试中对于内存管理和 dealloc 相关的考察应该不会很复杂，建议熟读一次源码，了解 `dealloc` 的调用时机以及整个释放流程，然后理解注意事项，基本可以一次性解决 `dealloc` 的相关面试题。

* [为什么不能在init和dealloc函数中使用accessor方法](https://cloud.tencent.com/developer/article/1143323 "为什么不能在init和dealloc函数中使用accessor方法")
* [ARC下，Dealloc还需要注意什么？](https://gitkong.github.io/2019/10/24/ARC%E4%B8%8B-Dealloc%E8%BF%98%E9%9C%80%E8%A6%81%E6%B3%A8%E6%84%8F%E4%BB%80%E4%B9%88/ "ARC下，Dealloc还需要注意什么？")
* [Practical Memory Management](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/mmPractical.html#//apple_ref/doc/uid/TP40004447-SW4 "Practical Memory Management")


## 优秀博客
整理编辑：[皮拉夫大王在此](https://juejin.cn/user/281104094332653)

> 本期优秀博客的主题为：ARM64 汇编入门及应用。汇编代码对于我们大多数开发者来说是既熟悉又陌生的领域，在日常开发过程中我们经常会遇到汇编，所以很熟悉。但是我们遇到汇编后，大多数人可能并不了解汇编代码做了什么，也不知道能利用汇编代码解决什么问题而常常选择忽略，因此汇编代码又是陌生的。本期博客我搜集了 3 套汇编系列教程，跟大家一道进入 ARM64 的汇编世界。
>
> **阅读学习后我将获得什么？**
>
> 完整阅读三套学习教程后，我们可以阅读一些逻辑简单的汇编代码，更重要的是多了一种针对疑难 bug 的排查手段。
>
> **需要基础吗？**
>
> 我对汇编掌握的并不多，在阅读和学期过程期间发现那些需要思考和理解的东西作者们都介绍的很好。

1、[[C in ASM(ARM64)]](https://zhuanlan.zhihu.com/p/31168062 "[C in ASM(ARM64)]") -- 来自知乎：知兵

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：推荐先阅读此系列文章。作者从语法角度解释源码与汇编的关系，例如数组相关的汇编代码是什么样子？结构体相关的汇编代码又是什么样子。阅读后我们可以对栈有一定的理解，并且能够阅读不太复杂的汇编代码，并能结合指令集说明将一些人工源码翻译成汇编代码。

2、[iOS汇编入门教程](https://juejin.cn/post/6844903576855117831 "iOS汇编入门教程") -- 来自掘金：Soulghost

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：页师傅出品经典教程。相对前一系列文章来说，更多地从 iOS 开发者的角度去看到和应用汇编，例如如何利用汇编代码分析 NSClassFromString 的实现。文章整体的深度也有所加深，如果读者有一定的汇编基础，可以从该系列文章开始阅读。

3、[深入iOS系统底层系列文章目录](https://juejin.cn/post/6844903847027015694 "深入iOS系统底层系列文章目录") -- 来自掘金：欧阳大哥2013

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：非常全面且深入的底层相关文章集合。有了前两篇文章的铺垫，可以阅读该系列文章做下拓展。另外作者还在 [深入iOS系统底层之crash解决方法](https://juejin.cn/post/6844903670404874254 "深入iOS系统底层之crash解决方法") 文章中一步步带领我们利用汇编代码排查野指针问题。作为初学者我们可以快速感受到收益。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 程序员做饭指南

**地址**：https://github.com/Anduin2017/HowToCook

一个由社区驱动和维护的做饭指南。在这里你可以学习到各色菜式是如何制作的，以及一些厨房的使用常识和知识。比较有意思的是，该仓库里的菜谱大都对制作过程中的细节和用量描述准确，比如菜谱中有 `不允许使用不精准描述的词汇，例如：适量、少量、中量、适当。` 等非常严格准确的要求，对几乎每个菜谱都做到了简洁准确，非常有意思，也非常欢迎大家贡献它~

## 工具推荐


整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### EasyFind 

**地址**：https://easyfind.en.softonic.com/mac

**软件状态**：免费

**软件介绍**：

小而强大的文件搜索应用，媲美 `windows` 下的 `Everything`。

![EasyFind](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/easyfind-easyfind.png)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第四十三期](https://mp.weixin.qq.com/s/Ktk5wCMPZQ5E-UASwHD7uw)

[iOS摸鱼周报 第四十二期](https://mp.weixin.qq.com/s/ybANWeLNHPOTkr5_alha9g)

[iOS摸鱼周报 第四十一期](https://mp.weixin.qq.com/s/DNXrfZgx0JaXyvfVZ4sYVA)

[iOS摸鱼周报 第四十期](https://mp.weixin.qq.com/s/y4229I_l8aLILR7WA7y01Q)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
