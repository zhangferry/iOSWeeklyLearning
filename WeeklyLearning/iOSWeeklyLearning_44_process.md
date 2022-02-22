# iOS摸鱼周报 第四十二期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * Tips：
> * 面试模块：Dealloc 使用注意事项及解析
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：Apple 将在 iPhone 上推出 Tap to Pay 功能，即可以通过简单的操作行为 -- 轻触，完成在商户端的付款过程。该功能通过 NFC 实现，非常安全，支持 Apple Pay、非接触式信用卡、借记卡以及其他数子钱包，这意味着 iPhone 将具备类似 POS 的功能，客户可以直接在商户的 iPhone 上刷信用卡进行消费。该功能仅 iPhone XS 及之后的机型支持。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Apple_Apple-Pay_Payment_inline.jpg.large_2x.jpg)

Stripe 将成为第一个在 iPhone 上向其商业客户提供 Tap to Pay 的支付平台。其他支付平台和应用程序将在今年晚些时候推出。

## 开发Tips

整理编辑：[zhangferry](https://zhangferry.com)

### 获取 Build Setting 对应的环境变量 Key

Xcode 的 build setting 里有很多配置项，这些配置项都有对应的环境变量，当我们要用脚本自定义的话就需要知道对应的环境变量 Key是哪个才好设置。比如下面这个 Header Search Paths

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220220215645.png)

其对应的 Key 是 `HEADER_SEARCH_PATHS`。那如何或者这个 Key 呢，除了网上查相关资料我们还可以通过 Xcode 获取。

#### 方法一（由@CodeStar提供）

选中该配置项，展开右部侧边栏，选中点击帮助按钮就能够看到这个配置的说明和对应的环境变量名称。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220220220200.png)

#### 方法二

选中该配置，按住 Option 键，双击该配置，会出现一个描述该选项的帮助卡片，这个内容与上面的帮助侧边栏内容一致。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220220220534.png)

## 面试解析

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Dealloc 使用注意事项及解析

关于 Dealloc 的相关面试题以及应用， 周报里已经有所提及。例如 [三十八期：dealloc 在哪个线程执行](https://mp.weixin.qq.com/s/a1aOOn1sFh5EaxISz5tAxA) 和 [四十二期：OOM 治理 FBAllocationTracker 实现原理](https://mp.weixin.qq.com/s/ybANWeLNHPOTkr5_alha9g)， 可以结合今天的使用注意事项一起学习。

#### 避免在 dealloc 中使用属性访问

在很多资料中，都明确指出，应该尽量避免在 dealloc 中通过属性访问，而是用成员变量替代。

> 在初始化方法和dealloc方法中，总是应该直接通过实例变量来读写数据。- 《Effective Objective-C 2.0》第七条
>
> Always use accessor methods. Except in initializer methods and dealloc. -  WWDC 2012 Session 413 - Migrating to Modern Objective-C
>
> The only places you shouldn’t use accessor methods to set an instance variable are in initializer methods and dealloc. - [Practical Memory Management](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/mmPractical.html#//apple_ref/doc/uid/TP40004447-SW4)

除了可以提升访问效率，也可以防止发生 crash。有文章介绍 crash 的原因是：析构过程中，类结构不再完整，当使用 `accessor` 时，实际是向当前实例发送消息，此时可能会存在 crash。

> 笔者对这里也不是很理解，根据 `debug`  分析析构过程实际是优先调用了实例覆写的 `dealloc`  后，才依次处理 `superclass 的 dealloc`、 `cxx_destruct` 、`Associated`、`Weak Reference`、`Side Table`等结构的，最后执行  `free`，所以不应该发生结构破坏导致的 crash，希望有了解的同学指教一下

笔者个人的理解是：Apple 做这种要求的原因是不想让子类影响父类的构造和析构过程。例如以下代码，子类通过覆写了 `Associated`方法， 会影响到父类的 `dealloc`过程

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

造成 crash 的原因是`HWSubObject:dealloc()中释放了变量debugInfo`然后调用 `HWObject:dealloc()` ，该函数使用 `Associated`设置 `info` ，由于子类覆写了  `setInfo`, 所以执行子类`setInfo`. 该函数内使用了已经被释放的变量 `debugInfo`。**正如上面说的， 子类通过重写Associated，最终影响到了父类的析构过程。**

#### dealloc 是什么时候释放变量的

其实在 `dealloc` 中无需开发处理成员变量， 当系统调用 `dealloc`时会自动调用析构函数（`.cxx_destruct`）释放变量，参考源码调用链：`[NSObject dealloc] => _objc_rootDealloc => rootDealloc => object_dispose =>objc_destructInstance => object_cxxDestruct => object_cxxDestructFromClass  `

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

沿着 superClass 链通过 `lookupMethodInClassAndLoadCache`去查询 `SEL_cxx_destruct`函数，查找到调用， 

`SEL_cxx_destruct`是 `objc`在初始化调用`map_images`时， 在`Sel_init`中赋值的，值就是`.cxx_destruct`

而 `cxx_destruct`就是用于释放变量的，当类中新增了变量后， 会自动插入该函数，这里可以通过 `LLDB watchpoint `监听实例的属性值变化， 然后查看堆栈信息验证

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/weekly_44_interview_02.jpg)

#### 避免在 dealloc 中使用__weak

```objective-c
- (void)dealloc {
    __weak typeof(self) weakSelf = self;
}
```

当在 `dealloc`中使用了 `__weak`后会直接 crash，报错信息为：`Cannot form weak reference to instance (0x2813c4d90) of class xxx. It is possible that this object was over-released, or is in the process of deallocation.` 报错原因是 `runtime` 在存储弱引用计数过程中判断了当前对象是否正在析构中， 如果正在析构则抛出异常

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

代码会在 line19 发生 crash， 报错为 `EXC_BAD_ACCESS`。原因很简单，因为 `dealloc`最终会调用 `free()`释放内存空间，而后 `GCD`再访问到 `self` 时已经是野指针，所以报错。

>  可以使用 `performSelector`代替 `GCD`实现， 确保线程操作先于dealloc完成。

总结：面试中对于内存管理和 dealloc 相关的考察应该不会很复杂， 建议熟读一次源码，了解 `dealloc`的调用时机以及整个释放流程，然后理解注意事项，基本可以一次性解决 `dealloc` 的相关面试题

* [为什么不能在init和dealloc函数中使用accessor方法](https://cloud.tencent.com/developer/article/1143323 "为什么不能在init和dealloc函数中使用accessor方法")
* [ARC下，Dealloc还需要注意什么？](https://gitkong.github.io/2019/10/24/ARC%E4%B8%8B-Dealloc%E8%BF%98%E9%9C%80%E8%A6%81%E6%B3%A8%E6%84%8F%E4%BB%80%E4%B9%88/ "ARC下，Dealloc还需要注意什么？")
* [Practical Memory Management](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/mmPractical.html#//apple_ref/doc/uid/TP40004447-SW4 “Practical Memory Management”)


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
