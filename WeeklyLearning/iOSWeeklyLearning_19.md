# iOS摸鱼周报 第十九期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 本期话题讲了关于学习和记忆的一些方法。
> * 开发 Tips 讲了如何区分 minimumLineSpacing 和 minimumInteritemSpacing 这两个属性及本地化关于日期的注意事项。
> * 面试解析本期讲解了属性及属性关键字的几个知识点，由[@师大小海腾](https://juejin.cn/user/782508012091645)和[@反向抽烟](https://blog.csdn.net/opooc)整理，内容非常之详细。
> * 优秀博客整理了几篇卡顿优化的优质文章。
> * 学习资料有两个内容，Combine Operators：帮助理解 Combine 操作符的手机端 App；还有 Stanford 最新的 SwiftUI 2.0 双语教程。
> * 开发工具带来了一个基于 linkmap 分析执行文件大小的工具：LinkMap。

## 本期话题

[@zhangferry](https://zhangferry.com)：本期讲下高效记忆这个话题，多数内容来源于《暗时间》。关于知识书中有句话是这样说的：

> 你所拥有的知识并不取决于你记得多少，而在于它们能否在恰当的时候被回忆起来。

这让我想起爱因斯坦的一句话：

> 教育就是忘记了在学校所学的一切之后剩下的东西。

两种说法很相似，都在强调为我所用才是知识的真正价值。而为我所用的前提就是记忆，记住了，才有可能在适当的时候被唤醒，记忆与学习也总是相辅相成的。关于记忆有一个被广泛认可的机制：我们在记忆的时候会将很多线索（例如当时的场景、语言环境等）一并编码进行记忆，事后能否快速提取出来主要就取决于这些线索有多丰富。

针对这一机制有以下方法可用于加深记忆并辅助学习：

* 过段时间尝试再回忆。它的作用一方面是转换为长时记忆，还有一方面可以通过当前掌握的知识体系重新整合原有知识，这样有时还可以得到新的启发。
* 用自己的语言表述，书写下来，甚至讲给他人听。这个就是费曼学习法了，它的作用是确保不是我以为我理解了，而是我用自己的方式理解了。
* 气味，背景音乐，天气等这些外界因素，都可以作为线索进行编码记忆。有时我们偶然听一段以前的音乐，就能一下子回忆起当时的场景和感受，感觉尘封记忆被打开，DNA 动了一样，这些都是由于一个线索串连起来一系列回忆引起的。
* 对于经验知识的学习，光听别人说或者看着别人做还不够，我们可以努力设想自己处于别人的境地，感受它们，将它们和你的情绪记忆挂钩。
* 如果一件事情就是一件事情，那我们永远也无法学到“未来”的知识，所以我们还要剥去无关紧要的细节，抽象出那个关键点，这样才能进行知识的迁移与推广。

## 开发Tips

### UICollectionView 的 scrollDirection 对 minimumLineSpacing 和 minimumInteritemSpacing 影响

整理编辑：[人魔七七](https://github.com/renmoqiqi)

`minimumLineSpacing` 和 `minimumInteritemSpacing` 这两个值表示含义是受滚动方向影响的，不同滚动方向，行列的排列方式不同，我们仅需记住行间距为 lineSpace 即可。下图为可视化的描述：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210716180322.png)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/3162666d7fa108da73e6549aea9154cf.png)

### 本地化时一些需要注意的日期设置

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

不同地域会有不同的日期格式，一般而言，我们都默认使用 `[NSLocale defaultLocale]` 来获取存储在设备设置中 `Regional Settings` 的地域，而不是指定某个地域，该行为不需要显示设置。

默认的语言/区域设置会导致 `NSCalendar`，`NSDateFormatter` 等跟区域关联的类上存在不同的展示

#### **Calendar** 的 firstWeekday

> The firstWeekday property tells you what day of the week the week starts in your locale. In the US, which is the default locale, a week starts on Sun.

当我们使用 `Calendar` 的 `firstWeekday` 属性时，需要注意，这个世界上不是所有地域其 `firstWeekday`  值都是 `1`。比如，对莫斯科来说，其  `firstWeekday`   的值是 `2`。 

如果你的日历控件并没有考虑到这些，对于某一天具体排列在一周的哪天来说，其值是不同的。

笔者之前所做的日历头部是按照周一至周日固定展示的，然后用户在俄罗斯发现日期乱了，日期与周几错乱。

后续直接定死了`firstWeekday = 1` 来功能上解决了这个问题。

#### **DateFormatter**

目前部分地域（部分欧美国家）存在**夏令时**，其会在接近春季开始的时候，将时间调快一小时，并在秋季调回正常时间。

虽然目前现有的设备支持特定的夏令时的展示，但是存在某些历史原因，如俄罗斯：

```swift
let dFmt = DateFormatter()
dFmt.dateFormat = "yyyy-MM-dd"
dFmt.timeZone = TimeZone(identifier:"Europe/Moscow")
print(dFmt.date(from:"1981-04-01") as Any) // nil
print(dFmt.date(from:"1982-04-01") as Any) // nil
print(dFmt.date(from:"1983-04-01") as Any) // nil
print(dFmt.date(from:"1984-04-01") as Any) // nil
```

对于 1981 年 - 1984 年 4 个年度的俄罗斯来说，4 月 1 号当天没有零点，会导致转化出的 `Date` 为 nil。如果我们需要做类似转换，就需注意该特殊情况。

## 面试解析

整理编辑：[反向抽烟](https://blog.csdn.net/opooc)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**属性及属性关键字**。

### 谈属性及属性关键字

#### @property、@synthesize 和 @dynamic

##### @property

属性用于封装对象中数据，属性的本质是 ivar + setter + getter。

可以用 @property 语法来声明属性。@property 会帮我们自动生成属性的 setter 和 getter 方法的声明。

##### @synthesize

帮我们自动生成 setter 和 getter 方法的实现以及 _ivar。

你还可以通过 @synthesize 来指定实例变量名字，如果你不喜欢默认的以下划线开头来命名实例变量的话。但最好还是用默认的，否则影响可读性。

如果不想令编译器合成存取方法，则可以自己实现。如果你只实现了其中一个存取方法 setter or getter，那么另一个还是会由编译器来合成。但是需要注意的是，如果你实现了属性所需的全部方法（如果属性是 readwrite 则需实现 setter and getter，如果是 readonly 则只需实现 getter 方法），那么编译器就不会自动进行 @synthesize，这时候就不会生成该属性的实例变量，需要根据实际情况自己手动 @synthesize 一下。

```objectivec
@synthesize ivar = _ivar;
```

##### @dynamic

告诉编译器不用自动进行 @synthesize，你会在运行时再提供这些方法的实现，无需产生警告，但是它不会影响 @property 生成的 setter 和 getter 方法的声明。@dynamic 是 OC 为动态运行时语言的体现。动态运行时语言与编译时语言的区别：动态运行时语言将函数决议推迟到运行时，编译时语言在编译器进行函数决议。

```objectivec
@dynamic ivar;
```

以前我们需要手动对每个 @property 添加 @synthesize，而在 iOS 6 之后 LLVM 编译器引入了 `property autosynthesis`，即属性自动合成。换句话说，就是编译器会自动为每个 @property 添加 @synthesize。

那你可能就会问了，@synthesize 现在有什么用呢？

1. 如果我们同时重写了 setter 和 getter 方法，则编译器就不会自动为这个 @property 添加 @synthesize，这时候就不存在 _ivar，所以我们需要手动添加 @synthesize。
2. 如果该属性是 readonly，那么只要你重写了 getter 方法，`property autosynthesis` 就不会执行，同样的你需要手动添加 @synthesize 如果你需要的话，看你这个属性是要定义为存储属性还是计算属性吧。
3. 实现协议中要求的属性。

此外需要注意的是，分类当中添加的属性，也不会 `property autosynthesis` 哦。因为类的内存布局在编译的时候会确定，但是分类是在运行时才加载并将数据合并到宿主类中的，所以分类当中不能添加成员变量，只能通过关联对象间接实现分类有成员变量的效果。如果你给分类添加了一个属性，但没有手动给它实现 getter、setter（如果属性是 readonly 则不需要实现）的话，编译器就会给你警告啦 `Property 'ivar' requires method 'ivar'、'setIvar:' to be defined - use @dynamic or provide a method implementation in this category`，编译器已经告诉我们了有两种解决方式来消除警告：

1. 在这个分类当中提供该属性 getter、setter 方法的实现
2. 使用 @dynamic 告诉编译器 getter、setter 方法的实现在运行时自然会有，您就不用操心了。当然在这里 @dynamic 只是消除了警告而已，如果你没有在运行时动态添加方法实现的话，那么调用该属性的存取方法还是会 Crash。


#### 属性修饰符分类


分类|属性关键字
--|--
原子性|`atomic`、`nonatomic`
读写权限|`readwrite`、`readonly`
方法名|`setter`、`getter`
内存管理|`assign`、`weak`、`unsafe_unretained`、`retain`、`strong`、`copy`
可空性|(`nullable`、`_Nullable` 、`__nullable`)、<br>(`nonnull`、`_Nonnull`、`__nonnull`)、<br>(`null_unspecified`、`_Null_unspecified` 、`__null_unspecified`)、<br>`null_resettable`
类属性|`class`


##### 原子性

属性关键字|用法
-- |--
atomic|原子性（默认），编译器会自动生成互斥锁（以前是自旋锁，后面改为了互斥锁），对 setter 和 getter 方法进行加锁，可以保证属性的赋值和取值的原子性操作是线程安全的，但不包括操作和访问。<br>比如说 atomic 修饰的是一个数组的话，那么我们对数组进行赋值和取值是可以保证线程安全的。但是如果我们对数组进行操作，比如说给数组添加对象或者移除对象，是不在 atomic 的负责范围之内的，所以给被 atomic 修饰的数组添加对象或者移除对象是没办法保证线程安全的。
nonatomic|非原子性，一般属性都用 nonatomic 进行修饰，因为 atomic 耗时。

##### 读写权限

属性关键字|用法
--|--
readwrite|可读可写（默认），同时生成 setter 方法和 getter 方法的声明和实现。
readonly|只读，只生成 getter 方法的声明和实现。为了达到封装的目的，我们应该只在确有必要时才将属性对外暴露，并且尽量把对外暴露的属性设为 readonly。如果这时候想在对象内部通过 setter 修改属性，可以在类扩展中将属性重新声明为 readwrite；如果仅在对象内部通过 _ivar 修改，则不需要重新声明为 readwrite。


##### 方法名

属性关键字|用法
--|--
setter|可以指定生成的 setter 方法名，如 setter = setName。这个关键字笔者在给分类添加属性的时候会用得比较多，为了避免分类方法“覆盖”同名的宿主类（或者其它分类）方法的问题，一般我们都会加前缀，比如 bbIvar，但是这样生成的 setter 方法名就不美观了（为 setBbIvar），于是就使用到了 setter 关键字 `@property (nonatomic, strong, setter = bb_setIvar:) NSObject *bbIvar;`
getter|可以指定生成的 getter 方法名，如 getter = getName。使用示例：`@property (nonatomic, assign, getter = isEnabled) BOOL enabled;`

##### 内存管理

属性关键字|用法
--|--
assign|1. 既可以修饰基本数据类型，也可以修饰对象类型；<br>2. setter 方法的实现是直接赋值，一般用于基本数据类型 ；<br>3. 修饰基本数据类型，如 NSInteger、BOOL、int、float 等；<br>4. 修饰对象类型时，不增加其引用计数；<br>5. 会产生悬垂指针（悬垂指针：assign 修饰的对象在被释放之后，指针仍然指向原对象地址，该指针变为悬垂指针。这时候如果继续通过该指针访问原对象的话，就可能导致程序崩溃）。
weak|1. 只能修饰对象类型；<br>2. ARC 下才能使用；<br>3. 修饰弱引用，不增加对象引用计数，主要可以用于避免循环引用；<br>4. weak 修饰的对象在被释放之后，会自动将指针置为 nil，不会产生悬垂指针；<br>5. 对于视图，通常还是用在 xib 和 storyboard 上；代码中对于有必要进行 remove 的视图也可以使用 weak，这样 remove 之后会自动置为 nil。
unsafe_unretained|1. 既可以修饰基本数据类型，也可以修饰对象类型；<br>2. MRC 下经常使用，ARC 下基本不用；<br>3. 同 weak，区别就在于 unsafe_unretained 会产生悬垂指针；<br>4. weak 对性能会有一定的消耗，当一个对象 dealloc 时，需要遍历对象的 weak 表，把表里的所有 weak 指针变量值置为 nil，指向对象的 weak 指针越多，性能消耗就越多。所以 unsafe_unretained 比 weak 快。当明确知道对象的生命周期时，选择 unsafe_unretained 会有一些性能提升。比如 A 持有 B 对象，当 A 销毁时 B 也销毁。这样当 B 存在，A 就一定会存在。而 B 又要调用 A 的接口时，B 就可以存储 A 的 unsafe_unretained 指针。虽然这种性能上的提升是很微小的。但当你很清楚这种情况下，unsafe_unretained 也是安全的，自然可以快一点就是一点。而当情况不确定的时候，应该优先选用 weak。
retain|1. MRC 下使用，ARC 下基本使用 strong；<br>2. 修饰强引用，将指针原来指向的旧对象释放掉，然后指向新对象，同时将新对象的引用计数加 1；<br>3. setter 方法的实现是 release 旧值，retain 新值，用于 OC 对象类型。
strong|1. ARC 下才能使用；<br>2. 原理同 retain；<br>3. 但是在修饰 block 时，strong 相当于 copy，而 retain 相当于 assign。
copy|setter 方法的实现是 release 旧值，copy 新值，一般用于 block、NSString、NSArray、NSDictionary 等类型。使用 copy 和 strong 修饰 block 其实都一样，用 copy 是为了和 MRC 下保持一致的写法；用于 NSString、NSArray、NSDictionary 是为了保证赋值后是一个不可变对象，以免遭外部修改而导致不可预期的结果。


##### 可空性

[Nullability and Objective-C](https://developer.apple.com/swift/blog/?id=25 "Nullability and Objective-C")

苹果在 Xcode 6.3 引入的一个 Objective-C 的新特性 `nullability annotations`。这些关键字可以用于属性、方法返回值和参数中，来指定对象的可空性，这样编写代码的时候就会智能提示。在 Swift 中可以使用 `?` 和 `!` 来表示一个对象是 `optional` 的还是 `non-optional`，如 `UIView?` 和 `UIView!`。而在 Objective-C 中则没有这一区分，`UIView` 即可表示这个对象是 `optional`，也可表示是 `non-optioanl`。这样就会造成一个问题：在 Swift 与 Objective-C 混编时，Swift 编译器并不知道一个 Objective-C 对象到底是 `optional` 还是 `non-optional`，因此这种情况下编译器会隐式地将 Objective-C 的对象当成是 `non-optional`。引入 `nullability annotations` 一方面为了让 iOS 程序员平滑地从 Objective-C 过渡到 Swift，另一方面也促使开发者在编写 Objective-C 代码时更加规范，减少同事之间的沟通成本。

关键字 `__nullable` 和 `__nonnull` 是苹果在 Xcode 6.3 中发行的。由于与第三方库的潜在冲突，苹果在 Xcode 7 中将它们更改为 `_Nullable` 和 `_Nonnull`。但是，为了与 Xcode 6.3 兼容，苹果预定义了宏 `__nullable` 和 `__nonnull` 来扩展为新名称。同时苹果同样还支持没有下划线的写法 `nullable` 和 `nonnull`，它们的区别在与放置位置不同。

>注意：此类关键词仅仅提供警告，并不会报编译错误。只能用于声明对象类型，不能声明基本数据类型。

属性关键字|用法
--|--
nullable、_Nullable 、__nullable|对象可以为空，区别在于放置位置不同
nonnull、_Nonnull、__nonnull|对象不能为空，区别在于放置位置不同
null_unspecified、_Null_unspecified 、__null_unspecified|未指定是否可为空，区别在于放置位置不同
null_resettable|1. getter 方法不能返回为空，setter 方法可以为空；<br>2. 必须重写 setter 或 getter 方法做非空处理。否则会报警告 `Synthesized setter 'setName:' for null_resettable property 'name' does not handle nil`


###### 使用效果

```objectivec
@interface AAPLList : NSObject <NSCoding, NSCopying>
// ...
- (AAPLListItem * _Nullable)itemWithName:(NSString * _Nonnull)name;
@property (copy, readonly) NSArray * _Nonnull allItems;
// ...
@end

// --------------

[self.list itemWithName:nil]; // warning!
```

###### Audited Regions：Nonnull 区域设置

如果每个属性或每个方法都去指定 `nonnull `和 `nullable`，将是一件非常繁琐的事。苹果为了减轻我们的工作量，专门提供了两个宏： `NS_ASSUME_NONNULL_BEGIN` 和 `NS_ASSUME_NONNULL_END`。在这两个宏之间的代码，所有简单指针类型都被假定为 `nonnull`，因此我们只需要去指定那些 `nullable` 指针类型即可。示例代码如下：

```objectivec
NS_ASSUME_NONNULL_BEGIN
@interface AAPLList : NSObject <NSCoding, NSCopying>
// ...
- (nullable AAPLListItem *)itemWithName:(NSString *)name;
- (NSInteger)indexOfItem:(AAPLListItem *)item;

@property (copy, nullable) NSString *name;
@property (copy, readonly) NSArray *allItems;
// ...
@end
NS_ASSUME_NONNULL_END

// --------------

self.list.name = nil;   // okay

AAPLListItem *matchingItem = [self.list itemWithName:nil];  // warning!
```

###### 笔者的一些经验总结

* 使用好可空性关键字可以让 Objective-C 开发者平滑地过渡到 Swift，而不会被 Swift 可选类型绊倒。
* 使用好可空性关键字可以让代码更加规范，比如你不应该将一个指定为 nonnull 的属性赋值为 nil。
* `NS_ASSUME_NONNULL_BEGIN` 和 `NS_ASSUME_NONNULL_END` 只是苹果为了减轻我们的工作量而提供的宏，而不是允许我们忽略可空性关键字。
* 如果你没有指定属性/方法参数为 nullable 的话，当给该属性赋值/传参 nil 的时候，会得到烦人的警告。
* 进行混编的时候，如果你没有给一个可为空的属性指定 nullable，就无法进行可选链式调用，因为 Swift 会把它当作非可选类型来处理，而且你还不能强制解包，因为它可能为 nil，这时候你就得加一层保护。


##### 类属性 class

属性可以分为实例属性和类属性：

* 实例属性：每个实例都有一套属于自己的属性值，它们之前是相互独立的；
* 类属性：可以为类本身定义属性，无论创建了多少个该类型的实例，这些属性都只有唯一一份，因为类是单例。

说白了就是实例属性与 instance 关联，类属性与 class 关联。

用处：类属性用于定义某个类型所有实例共享的数据，比如所有实例都能用的一个常量/变量（就像 C 语言中的静态常量/静态变量）。

通过给属性添加 class 关键字来定义`类属性`。

```objectivec
@property (class, nonatimoc, strong) NSObject *object;
```

类属性是不会进行 `property autosynthesis` 的，那怎么关联值呢？

* 如果是存储属性
    1. 在 .m 中定义一个 static 全局变量，然后在 setter 和 getter 方法中对此变量进行操作。
    2. 在 setter 和 getter 方法中使用关联对象来存储值。笔者之前遇到的一个使用场景就是，类是通过 Runtime 动态创建的，这样就没办法使用 static 全局变量存储值。于是笔者在父类中定义了一个类属性并使用关联对象来存储值，这样动态创建的子类就可以给它的类属性关联值了。
* 如果是计算属性，就直接实现 setter 和 getter 方法就好。

#### 其它补充

在设置属性所对应的实例变量时，一定要遵从该属性所声明的语义：

```objectivec
@property (nonatomic, copy) NSString *name;

— (instancetype)initWithName:(NSString *)name {
    if (self = [super init]) {
        _name = [name copy];
    }
   	return self;
}
```

若是自己来实现存取方法，也应该保证其具备相关属性所声明的性质。

参考：[iOS - 再谈 OC 属性及属性关键字](https://juejin.cn/post/6986323251911720997/ "iOS - 再谈 OC 属性及属性关键字")

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`卡顿优化`

1、[iOS卡顿监测方案总结](https://juejin.cn/post/6844903944867545096 "iOS卡顿监测方案总结")


文章总结了业界的很多卡顿监控技术。包括：FPS、runloop、子线程 Ping、CPU 占用率监测。文章中附带了作者参考和收集到的原文链接，以及部分相关上下游技术的文章。如果您想要做卡顿监控，阅读本文可以节省不少时间和精力。

2、[iOS 渲染原理解析](https://mp.weixin.qq.com/s/6ckRnyAALbCsXfZu56kTDw)


文章细致的介绍了图像渲染的流程。包括一些细小有趣的知识点，比如 CALayer 的 contents 保存了 bitmap 信息等。文中当然少不了对离屏渲染的介绍，包括离屏渲染的场景、离屏渲染的原因以及如何避免离屏渲染。文后附有小题目，可以让大家带着问题回顾文章，加深对知识的理解。

3、[UIView 动画降帧探究](https://mp.weixin.qq.com/s/EcVrrT1M4mI4f4d2b3qV0Q)


本文首先介绍为了降帧的目的：降低 GPU 的使用率，并介绍了为什么动画渲染对 GPU 有较大的影响。正文中主要介绍了降帧的方案：UIView animation 指定 `UIViewAnimationOptionPreferredFramesPerSecond30` 进行降帧、`CADisplayLink` 逐帧动画降帧。

4、[天罗地网？ iOS卡顿监控实战](https://juejin.cn/post/6844904005437489165 "天罗地网？ iOS卡顿监控实战") -- 来自掘金：进击的蜗牛君

本文利用 `ping` 方案，即每隔一段时间就去目标线程中检测状态，如果目标线程"运行良好"，则标记为正常，当一段时间 `ping` 均不正常时，上报目标线程的堆栈，此时认为目标线程发生了卡顿，作者已经做出了开源工具，方便大家深入研究。

5、[列表流畅度优化](https://juejin.cn/post/6844903656769208334 "列表流畅度优化") -- 来自掘金：Hello_Vincent

作者借鉴了 WWDC18 的相关 session，从实际角度出发，进行一次列表优化的旅程，从原因到解决办法，最后提出意见，称得上是一篇佳作。

6、[WWDC2016 Session笔记 - iOS 10 UICollectionView新特性](https://juejin.cn/post/6844903441416847374 "WWDC2016 Session笔记 - iOS 10 UICollectionView新特性
") -- 来自掘金：一缕殇流化隐半边冰霜

早在 WWDC16，官方针对 `UICollectionView` 已经做过优化教程，如果你还不知道，可以看一看这篇文章。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Combine Operators

地址：https://apps.apple.com/app/combine-operators/id1507756027

一个用来学习 Combine 的 App，他将一些 Combine 中的各种操作符用可视化的手段表达了出来，还附加了蠢萌蠢萌的动画效果，很适合刚接触 Combine 的朋友尝试一下。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/co.png)

### Stanford CS193P 2021 SwiftUI 2.0 双语字幕

地址：https://www.bilibili.com/video/BV1q64y1d7x5

Stanford CS193P 2021 SwiftUI 2.0 课程，该课程的老师是 Paul Hegarty，在 Stanford 执教 10 年左右了。该课程创办了很多年，每当 Apple 推出了新技术，例如 Storyboard、SwiftUI，这个白胡子老爷爷就会迅速跟上，更新他的课程，实乃一 it 潮人。你可以去油管 Stanford 官方账号查看该课程，也可以看看 up 主转载的该课程，还上传了中文字幕、英文字幕、繁体字幕的双语版本。理论上来说，你只需要有面向对象编程及 Swift 语言的相关基础和了解，你就可以看懂该课程，适合想要学习 SwiftUI 入门的朋友。

## 工具推荐

整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

**地址**： https://github.com/huanxsd/LinkMap

**软件状态**： 免费 

**软件介绍**

iOS 包的大小，是每个开发必须关注的问题，对于大型项目来说，只是代码段就有可能超过 100M，算上 armv7 和 arm64 架构，会超过 200M。 LinkMap 工具通过分析项目的 LinkMap 文件，能够计算出各个类、各个三方库占用的空间大小（代码段+数据段），方便开发者快速定位需要优化的文件。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/linkmap.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十八期](https://mp.weixin.qq.com/s/JsGmu7pzYLI3Svrmk5i2cA)

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
