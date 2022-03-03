# iOS摸鱼周报 第四十五期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：苹果公司宣布暂停在俄销售产品并关闭部分功能
> * Tips：在 SPM 集成 SwiftLint
> * 面试模块：Swift 的 weak 是如何实现的？
> * 优秀博客：iOS项目中的脚手架/CLI介绍
> * 学习资料：Swift 实现的设计模式
> * 开发工具：nginxedit：Nginx 在线配置工具

## 本期话题

[@zhangferry](https://zhangferry.com)：

### 苹果公司宣布暂停在俄销售产品并关闭部分功能

根据 CNBC 的[报道](https://www.cnbc.com/2022/03/01/apple-halts-product-sales-in-russia-.html "Apple halts product sales in Russia")，苹果公司在3月1号表示，已停止在俄罗斯的产品销售。与此同时，属于俄官方媒体的两款应用被下架，该地区 Apple Pay 等功能受限。以下是苹果发言人的原话：

> We have taken a number of actions in response to the invasion. We have paused all product sales in Russia. Last week, we stopped all exports into our sales channel in the country. Apple Pay and other services have been limited. RT News and Sputnik News are no longer available for download from the App Store outside Russia. And we have disabled both traffic and live incidents in Apple Maps in Ukraine as a safety and precautionary measure for Ukrainian citizens.

有很多人说应该支持国产手机了，但国产也是魔改的安卓系统，这虽没有像苹果那样被牢牢掌控，也并非完全的可控。这几天不只是苹果，谷歌、推特、台积电、英特尔，甚至连开发社区 Github、开源库 React 都在抵制俄罗斯，「科技无国界」已经完全沦为谎言，这不禁令人惶恐。

现代战争是复杂的，它不只是枪炮还会伴随着各类舆论战、信息战，而信息战的主动权就掌握在拥有核心技术的一方。反观俄罗斯，类似的事情是不是也会发生在我们身上？由此事件引发的思考是，仅仅用言语冲了某个社区留言板是不够的，打破垄断，不断提高我们自己的核心技术能力才是王道。科技强国，吾辈当自强！

## 开发Tips

### 获取 Build Setting 对应的环境变量 Key

整理编辑：[zhangferry](zhangferry.com)

Xcode 的 build setting 里有很多配置项，这些配置项都有对应的环境变量，当我们要用脚本自定义的话就需要知道对应的环境变量 Key是哪个才好设置。比如下面这个 Header Search Paths

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220220215645.png)

其对应的 Key 是 `HEADER_SEARCH_PATHS`。那如何或者这个 Key 呢，除了网上查相关资料我们还可以通过 Xcode 获取。

**方法一（由@CodeStar提供）**

选中该配置项，展开右部侧边栏，选中点击帮助按钮就能够看到这个配置的说明和对应的环境变量名称。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220220220200.png)

**方法二**

选中该配置，按住 Option 键，双击该配置，会出现一个描述该选项的帮助卡片，这个内容与上面的帮助侧边栏内容一致。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220220220534.png)

### 在 SPM 集成 SwiftLint

整理编辑：[FBY展菲](https://github.com/fanbaoying)

#### SwiftLint 介绍

`SwiftLint` 是一个实用工具，用于实现 Swift 的风格。 在 Xcode 项目构建阶段，集成 SwiftLint 很简单，构建阶段会在编译项目时自动触发 SwiftLint。

遗憾的是，目前无法轻松地将 `SwiftLint` 与 `Swift Packages` 集成，Swift Packages 没有构建阶段，也无法自动运行脚本。

下面介绍如何在 Xcode 中使用 `post action` 脚本在成功编译 Swift Package 后自动触发 SwiftLint。

`SucceedsPostAction.sh` 是一个 bash 脚本，用作 Xcode 中的 “Succeeds” 发布操作。当你编译一个 Swift 包时，这个脚本会自动触发 `SwiftLint`。

#### SwiftLint 安装

1. 在 Mac 上下载脚本 `SucceedsPostAction.sh`。

2. 确保脚本具有适当的权限，即运行 `chmod 755 SucceedsPostAction.sh`。

3. 如果要使用自定义 SwiftLint 规则，请将 `.swiftlint.yml` 文件添加到脚本旁边。

4. 启动 Xcode 13.0 或更高版本

5. 打开 Preferences > Locations 并确保 `Command Line Tools` 设置为 Xcode 版本

6. 打开 Preferences > Behaviors > Succeeds

7. 选择脚本 `SucceedsPostAction.sh`

![](https://files.mdnice.com/user/17787/7cce4fc6-82bc-4c66-b499-6541b75ca08c.png)

就是这样：每次编译 Swift 包时，`SucceedsPostAction.sh` 都会运行 SwiftLint。

**演示**

![](https://files.mdnice.com/user/17787/89f7a065-f200-4158-a701-99b217c38a4a.gif)

#### 存在一些问题

在 Xcode 中运行的 `post action` 脚本无法向 Xcode 构建结果添加日志、警告或错误。因此，`SucceedsPostAction.sh` 在 Xcode 中以新窗口的形式打开一个文本文件，其中包含 SwiftLint 报告列表。没有深度集成可以轻松跳转到 SwiftLint 警告。

**Swift 5.6**

请注意，由于[SE-0303: Package Manager Extensible Build Tools](https://github.com/apple/swift-evolution/blob/main/proposals/0303-swiftpm-extensible-build-tools.md "Package Manager Extensible Build Tools")，Swift 5.6（在撰写本文时尚不可用）可能会有所帮助。集成 SE-0303 后，不再需要此脚本。

参考：[Swift 实用工具 — SwiftLint - Swift社区](https://mp.weixin.qq.com/s/WMCwt6KjiBV2ddES-rQtyw)


## 面试解析
整理编辑：[JY](https://juejin.cn/user/1574156380931144)

### Swift 的 weak 是如何实现的？

在 Swift 中，也是拥有 `SideTable` 的，`SideTable` 是针对有需要的对象而创建，系统会为目标对象分配一块新的内存来保存该对象额外的信息。

对象会有一个指向 `SideTable` 的指针，同时 `SideTable` 也有一个指回原对象的指针。在实现上为了不额外多占用内存，目前只有在创建弱引用时，会先把对象的引用计数放到新创建的 `SideTable` 去，再把空出来的空间存放 `SideTable` 的地址，会通过一个标志位来区分对象是否有 `SideTable`。

```Swift 
class JYObject {
    var age :Int = 18
    var name:String = "JY"
}
var t = JYObject()
weak var t2 = t
print("----")
```

我们在`print`处打上断点，查看 t2 对象

```
(lldb) po t2
▿ Optional<JYObject>
  ▿ some : <JYObject: 0x6000001a9710>

(lldb) x/8gx  0x6000001a9710
0x6000001a9710: 0x0000000100491e18 0xc0000c00001f03dc
0x6000001a9720: 0x0000000000000012 0x000000000000594a
0x6000001a9730: 0xe200000000000000 0x0000000000000000
0x6000001a9740: 0x00007efd22b59740 0x000000000000009c
(lldb) 
```

通过查看汇编，定义了一个`weak`变量，编译器自动调用了`swift_weakInit`函数，这个函数是由`WeakReference`调用的。说明`weak`字段在编译器声明的过程当中自动生成了`WeakReference`对象。

```C++
WeakReference *swift::swift_weakInit(WeakReference *ref, HeapObject *value) {
		ref->nativeInit(value);
  	return ref;
}

void nativeInit(HeapObject *object) {
    auto side = object ? object->refCounts.formWeakReference() : nullptr;
    nativeValue.store(WeakReferenceBits(side), std::memory_order_relaxed);
}

template <>
HeapObjectSideTableEntry* RefCounts<InlineRefCountBits>::formWeakReference() {
    // 创建一个 Side Table
  	auto side = allocateSideTable(true);
  	if (side)
      // 增加一个弱引用
    	return side->incrementWeak();
  	else
    	return nullptr;
}
```

我们来看一下`allocateSideTable`方法，是如何创建一个`Side Table`的

```C++
template <>
HeapObjectSideTableEntry* RefCounts<InlineRefCountBits>::allocateSideTable(bool failIfDeiniting) {
  //1.拿到原有的引用计数
  auto oldbits = refCounts.load(SWIFT_MEMORY_ORDER_CONSUME);
  
  // 判断是否有SideTable，
  if (oldbits.hasSideTable()) {
    // Already have a side table. Return it.
    return oldbits.getSideTable();
  } 
  else if (failIfDeiniting && oldbits.getIsDeiniting()) {
    // Already past the start of deinit. Do nothing.
    return nullptr;
  }

  // Preflight passed. Allocate a side table.
  
  // FIXME: custom side table allocator
 
  //2.通过HeapObject创建了一个HeapObjectSideTableEntry实例对象
  HeapObjectSideTableEntry *side = new HeapObjectSideTableEntry(getHeapObject());
 
  //3.将创建的实例对象地址给了InlineRefCountBits，也就是 RefCountBitsT
  auto newbits = InlineRefCountBits(side);
  
  do {
    if (oldbits.hasSideTable()) {
      // Already have a side table. Return it and delete ours.
      // Read before delete to streamline barriers.
      auto result = oldbits.getSideTable();
      delete side;
      return result;
    }
    else if (failIfDeiniting && oldbits.getIsDeiniting()) {
      // Already past the start of deinit. Do nothing.
      return nullptr;
    }
     
    // 将原有的引用计数存储
    side->initRefCounts(oldbits);
     
  } while (!refCounts.compare_exchange_weak(oldbits, newbits,
                                             std::memory_order_release,
                                             std::memory_order_relaxed));
  return side;
}
```

> 总结一下上面所做的事情
>
> 1.拿到原有的引用计数
> 2.通过 HeapObject 创建了一个 HeapObjectSideTableEntry 实例对象
> 3.将创建的实例对象地址给了`InlineRefCountBits`，也就是 RefCountBitsT。

构造完 `Side Table` 以后，对象中的 `RefCountBitsT` 就不是原来的引用计数了，而是一个指向 `Side Table` 的指针，然而由于它们实际都是 `uint64_t`，因此需要一个方法来区分。区分的方法我们可以来看 `InlineRefCountBits` 的构造函数：

```C++
//弱引用
LLVM_ATTRIBUTE_ALWAYS_INLINE
  RefCountBitsT(HeapObjectSideTableEntry* side)
    : bits((reinterpret_cast<BitsType>(side) >> Offsets::SideTableUnusedLowBits)
           | (BitsType(1) << Offsets::UseSlowRCShift)
           | (BitsType(1) << Offsets::SideTableMarkShift))
  {
    assert(refcountIsInline);
  }
```

> 在弱引用方法中把创建出来的地址做了偏移操作然后存放到了内存当中。
>
> `SideTableUnusedLowBits` = 3，所以，在这个过程中，传进来的`side`往右移了 3 位，下面的两个是 62 位和 63 位标记成 1

我们接着来看一下 ` HeapObjectSideTableEntry ` 的结构

```C++
class HeapObjectSideTableEntry {
  // FIXME: does object need to be atomic?
  std::atomic<HeapObject*> object;
  SideTableRefCounts refCounts;

  public:
  HeapObjectSideTableEntry(HeapObject *newObject)
    : object(newObject), refCounts()
  { }
```

我们来尝试还原一下拿到弱引用计数 ：

`0xc0000c00001f03dc`62位和63位清0得到 `HeapObjectSideTableEntry` 实例对象的地址`0xC00001F03DC`

它既然是右移 3 位，那么我左移 3 位把它还原，`HeapObjectSideTableEntry`左移三位 得到`0x10062AFE0`

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220302155825.png)


- `0x6000001a9710` 就是实例对象的地址
- `0x0000000000000002`就是弱引用计数
  这里弱引用为`2`的原因是因为`SideTableRefCountBits`初始化的时候从`1`开始

`Side Table`的生命周期与对象是分离的，当强引用计数为 0 时，只有 `HeapObject` 被释放了，并没有释放`Side Table`，只有所有的 `weak` 引用者都被释放了或相关变量被置 `nil` 后，`Side Table` 才能得以释放。


## 优秀博客
整理编辑：[@我是熊大](https://github.com/Tliens)

> 本期优秀博客的主题为：脚手架/CLI。在项目最开始的时候，脚手架工具，就会帮你搭建好架子，并生成一些基本代码。脚手架的存在有利于团队统一架构风格，加速项目开发。

1、[从0构建自己的脚手架/CLI知识体系](https://juejin.cn/post/6966119324478079007 "从0构建自己的脚手架/CLI知识体系") -- 来自掘金：IT老班长

[@我是熊大](https://github.com/Tliens)：如何生成搭建脚手架呢？本文作者使用 NodeJS，从0开始搭建了一个脚手架，每一步都很详细，介绍了热门脚手架工具库，没有 NodeJS 基础的也能看懂，非常适合作为新手篇入场学习。

2、[iOS自动化工具Gckit CLI](https://seongbrave.github.io/gckit/guide/#%E6%B5%81%E7%A8%8B%E8%AF%B4%E6%98%8E "iOS自动化工具Gckit CLI") -- 来自博客：SeongBrave

[@我是熊大](https://github.com/Tliens)：在项目开发中，大家水平参差不齐，代码风格迥异，尤其是有新人加入团队时，适应期会比较长。那有没有可能让新同学也能像老同学一样，不仅快速进行开发，而且代码风格也近似呢？Gckit CLI 就是为此诞生的，大家在看完上篇文章后就可以对该库进行调整了，打造属于自己的自动化工具


3、[Swift + RxSwift MVVM 模块化项目实践](https://juejin.cn/post/6844903821160742919 "Swift + RxSwift MVVM 模块化项目实践") -- 来自掘金：SeongBrave

[@我是熊大](https://github.com/Tliens)：本文是 Gckit 作者的实践总结，主要讲解通过 CocoaPods 结合 Gckit-CLI 实现开发效率的最大化的一些项目实践。


4、[iOS自动化方案附脚本](https://juejin.cn/post/6948239939809050638 "iOS自动化方案附脚本") -- 来自掘金：我是熊大

[@我是熊大](https://github.com/Tliens)：不同的电脑开发环境不同，多人协作下，因环境不同会导致各种问题，比如 CocoaPods 的版本不同，就会导致某些库无法下载，.lock文件频繁更新等。本文介绍了如何统一开发环境，以及自动化脚本的使用，可以把它放进你的脚手架工具中。文章最后提到了关于脚手架工具的遐想。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Swift 实现的设计模式

**地址**：https://oldbird.run/design-patterns/#/

一份由 Swift 语言实现的设计模式教程。其中设计模式的举例清晰明了，代码也简洁易懂，大部分例子中有 UML 图来帮助理解，其中也会有一些对于不同设计模式之间区别与联系的总结和归纳，是很不错的学习设计模式的资源。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220302215124.png)

## 工具推荐


整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### nginxedit 

**地址**：https://www.nginxedit.cn/

**软件状态**：免费

**软件介绍**：

`Nginx`在线配置生成工具，配置高性能，安全和稳定的`Nginx`服务器的最简单方法。

![nginxedit](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Nginx%E5%9C%A8%E7%BA%BF%E9%85%8D%E7%BD%AE%E7%94%9F%E6%88%90%E5%B7%A5%E5%85%B7.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第四十四期](https://mp.weixin.qq.com/s/q__-veuaUZAK6xGQFxzsEg)

[iOS摸鱼周报 第四十三期](https://mp.weixin.qq.com/s/Ktk5wCMPZQ5E-UASwHD7uw)

[iOS摸鱼周报 第四十二期](https://mp.weixin.qq.com/s/ybANWeLNHPOTkr5_alha9g)

[iOS摸鱼周报 第四十一期](https://mp.weixin.qq.com/s/DNXrfZgx0JaXyvfVZ4sYVA)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
