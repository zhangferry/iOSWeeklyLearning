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

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

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
