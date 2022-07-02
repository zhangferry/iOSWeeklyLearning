# iOS摸鱼周报 第三十八期

![](https://cdn.zhangferry.com/Images/iOS摸鱼周报模板.png)

### 本期概要

> * 话题： Xcode 13.2 和 iOS 15.2 的正式版值得关注的几项新功能。
> * Tips：内存相关的一些机制。
> * 面试模块：dealloc 在哪个线程执行；NSString *str = @"123" 这里的 str 和  "123" 分别存储在哪个区域。
> * 优秀博客：SwiftUI 相关的几篇优秀博客。
> * 学习资料：软件随想录，Joel Spolsky 的 Blog 纸质版文集。
> * 开发工具：Dropshelf，一款 Mac OS 下的拖拽效率应用。

## 本期话题

[@zhangferry](https://zhangferry.com)：12 月 13 号，Apple 发布了 Xcode 13.2 和 iOS 15.2 的正式版。其中有几项新功能值得关注。

### [Xcode 13.2](https://developer.apple.com/documentation/xcode-release-notes/xcode-13_2-release-notes "Xcode 13.2")

编译系统和 Swift 编译器有了一个新模式可以充分利用 CPU 核心，以达到优化 Swift 项目的效果。该模式可选，可以执行如下命令打开：

```bash
defaults write com.apple.dt.XCBuild EnableSwiftBuildSystemIntegration 1
```

### [iOS 15.2](https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-15_2-release-notes "iOS 15.2")

是关于 StoreKit 的新特性：

* StoreKit 中展示退款请求的弹窗可以在 Xcode 中进行测试了。UIKit 模式下可利用：[`beginRefundRequest(in:)`](https://developer.apple.com/documentation/storekit/transaction/3803220-beginrefundrequest) 或者 [`beginRefundRequest(for:in:)`](https://developer.apple.com/documentation/storekit/transaction/3803219-beginrefundrequest) ，SwiftUI 下可利用 `refundRequestSheet(for:isPresented:onDismiss:)` 作为视图修饰器。
- StoreKit 中管理订阅的弹窗也可以在 Xcode 中进行测试了。 UIKit 模式下课利用 [`showManageSubscriptions(in:)`](https://developer.apple.com/documentation/storekit/appstore/3803198-showmanagesubscriptions) ，SwiftUI 下可利用  `manageSubscriptionsSheet(isPresented:)` 作为视图修饰器完成。

- 新的 [`SKTestSession.TimeRate`](https://developer.apple.com/documentation/storekittest/sktestsession/timerate) 值可用于 StoreKit Test 模块的自动化测试。

## 开发Tips

整理编辑：[zhangferry](zhangferry.com)

### 内存相关的一些机制

#### 虚拟内存寻址

为了安全性，防止物理内存被篡写（还有其他很多优势），操作系统引入了虚拟内存机制，虚拟内存是对物理内存的映射，操作系统会为每个进程提供一个连续并且私有的虚拟内存空间。

实际的数据读写首先要通过虚拟地址找到对应的物理地址，这个过程就是 CPU 寻址，CPU 寻址由位于 CPU 的 MMU（Memory Management Unit 内存管理单元）负责。

为了便于管理，虚拟内存被分割为大小固定的虚拟页（Virtual Page, VP）。程序加载过程中，虚拟内存由磁盘到内存的映射是以页为单位进行处理的。每次映射完成都会对应一个关联的物理内存地址，为了管理这个映射关系出现了页表条目（Page Table Entry）PTE 的一个数据表。这个页表条目里有一个标记位比特位，0 表示还未加载到内存，1 表示已经加载到内存。当访问到 0 就出产生缺页（Page Fault），之后会填充数据到内存，并修改这个标记位。

这个 PTE 通常是位于高速缓存或者内存中的，但即使是高速缓存它相对于 CPU 的读取速度仍然是很慢的。后来又引入了后备缓冲器（Translation Lookaside Buffer，TLB），这个缓存器位于 CPU 内部，其存储了 PTE 内容。虽然它的存储空间较小，但因为在 CPU 内部访问很快，由局部性原理来说这个处理仍是非常值得的。

汇总一下寻址流程如下图所示：

![](https://cdn.zhangferry.com/Images/20211216194314.png)

#### 内存不足的处理

在 Linux 中虚拟内存空间是大于实际物理内存地址的，这就会出现一个状况，当内存物理地址不够用时会发生什么？实际操作系统会将物理内存中的部分内容迁移到磁盘中，然后腾出地方给申请内存方使用，这个过程叫 Swap Out。当又要使用那部分内存时会触发 Swap Int，再移出部分内存，将需要的内容映射到空缺内存空间里。这个机制的好处是可以使用更大的内存地址，但坏处也很明显就是 Swap 会造成较大性能损耗。

##### iOS 处理机制

iOS 没有 Disk Swap 机制，因为其本身磁盘空间相对电脑是比较小的，而且频繁读取闪存会影响闪存寿命。基于此 iOS 设备可申请内存地址是有限度的，关于各个设备所能允许申请的最大内存，[Stack OverFlow](https://stackoverflow.com/questions/5887248/ios-app-maximum-memory-budget/15200855#15200855 "ios-app-maximum-memory-budget") 有人做过测试：

```
device: (crash amount/total amount/percentage of total)

iPhone5: 645MB/1024MB/62%
iPhone5s: 646MB/1024MB/63%
iPhone6: 645MB/1024MB/62% (iOS 8.x)
iPhone6+: 645MB/1024MB/62% (iOS 8.x)
iPhone6s: 1396MB/2048MB/68% (iOS 9.2)
iPhone6s+: 1392MB/2048MB/68% (iOS 10.2.1)
iPhoneSE: 1395MB/2048MB/69% (iOS 9.3)
iPhone7: 1395/2048MB/68% (iOS 10.2)
iPhone7+: 2040MB/3072MB/66% (iOS 10.2.1)
iPhone8: 1364/1990MB/70% (iOS 12.1)
iPhone X: 1392/2785/50% (iOS 11.2.1)
iPhone XS: 2040/3754/54% (iOS 12.1)
iPhone XS Max: 2039/3735/55% (iOS 12.1)
iPhone XR: 1792/2813/63% (iOS 12.1)
iPhone 11: 2068/3844/54% (iOS 13.1.3)
iPhone 11 Pro Max: 2067/3740/55% (iOS 13.2.3)
```

以 iPhone 11 Pro Max 为例，应用可申请内存为 2067M，占系统内容的 55%，这已经是很高了。但即使这样，仍会出现内存过高的情况，iOS 系统的处理主要是清理 + 压缩这两个方案。

**Clean Page & Dirty Page**

iOS 将内存页分为 Clean Page 和 Dirty Page，Clean Page 一般是固定内容，可以被系统回收，需要时从磁盘再加载回来。

![](https://cdn.zhangferry.com/Images/20211216191758.png)

上图可以看出，写入数据前申请内存为 Clean 内存，使用的部分就变成了 Dirty 内存。

**Compressed Memory**

iOS 还有另一种机制是压缩内存（Compressed Memory），这也是一种 Swap 机制。举个例子，某个 Dictionary 使用了 3 个 Page 的内存，如果一段时间没有被访问同时内存吃紧，则系统会尝试对它进行压缩从 3 个 Page 压缩为 1 个 Page 从而释放出 2 个 Page 的内存。但是如果之后需要对它进行访问，则它占用的 Page 又会变为 3 个。

这部分内存可以被 Instrument 统计到，对应的就是 VM Tracker 里的 Swapped Size：

![](https://cdn.zhangferry.com/Images/20211216193218.png)

参考：

* [jonyfang-iOS 内存相关梳理](https://blog.jonyfang.com/2020/04/08/2020-04-08-about-ram/ "jonyfang-iOS 内存相关梳理")
* [Reducing Your App's Memory Use](https://developer.apple.com/documentation/metrickit/improving_your_app_s_performance/reducing_your_app_s_memory_use "Reducing Your App's Memory Use")
* 《深入理解计算机系统》

## 面试解析

整理编辑：[zhangferry](https://zhangferry.com)

### dealloc 在哪个线程执行

在回答这个问题前需要了解 `dealloc` 在什么时机调用，`dealloc` 是在对象最后一次 `release` 操作的时候进行调用的，对应的源码在 `rootRelease` 中，针对 `nonpointer` 和 SideTable 有两种释放的操作。

 SideTable 管理的引用计数会调用 `sidetable_release`：

```c
uintptr_t
objc_object::sidetable_release(bool performDealloc)
{
#if SUPPORT_NONPOINTER_ISA
    ASSERT(!isa.nonpointer);
#endif
    SideTable& table = SideTables()[this];

    bool do_dealloc = false;

    table.lock();
    auto it = table.refcnts.try_emplace(this, SIDE_TABLE_DEALLOCATING);
    auto &refcnt = it.first->second;
    if (it.second) {
        do_dealloc = true;
    } else if (refcnt < SIDE_TABLE_DEALLOCATING) {
        // SIDE_TABLE_WEAKLY_REFERENCED may be set. Don't change it.
        do_dealloc = true;
        refcnt |= SIDE_TABLE_DEALLOCATING;
    } else if (! (refcnt & SIDE_TABLE_RC_PINNED)) {
        refcnt -= SIDE_TABLE_RC_ONE;
    }
    table.unlock();
    if (do_dealloc  &&  performDealloc) {
          // 可以释放的话，调用dealloc
        ((void(*)(objc_object *, SEL))objc_msgSend)(this, @selector(dealloc));
    }
    return do_dealloc;
}
```

对于 `nonpointer` 指针管理的引用计数，会修改 `extra_rc`值，需要释放时在`rootRelease`方法的底部还是会调用：

```c
if (do_dealloc  &&  performDealloc) {
    ((void(*)(objc_object *, SEL))objc_msgSend)(this, @selector(dealloc));
}
```

这里可以看出 `dealloc` 的调用并没有设置线程，所以其执行会根据触发时所在的线程而定，就是说其即可以是子线程也可以是主线程。这个也可以很方便的验证。

### NSString *str = @"123" 这里的 str 和  "123" 分别存储在哪个区域

可以先做一下测试：

```objectivec
NSString *str1 = @"123"; // __NSCFConstantString
NSLog(@"str1.class=%@, str1 = %p, *str1 = %p", str1.class, str1, &str1);
// str1.class=__NSCFConstantString, str1 = 0x1046b8110, *str1 = 0x7ffeeb54dc50
```

这时的 str1 类型是 `__NSCFConstantString`，str1 的内容地址较短，它代表的是常量区，指向该常量区的指针 `0x7ffeeb54dc50` 是在栈区的。

再看另外两种情况：

```objectivec
NSString *str2 = [NSString stringWithFormat:@"%@", @"123"];
NSLog(@"str2.class=%@, str2 = %p, *str2 = %p", str2.class, str2, &str2);
// str2.class=NSTaggedPointerString, str2 = 0xe7f1d0f8856c5253, *str2 = 0x7ffeeb54dc58

NSString *str3 = [NSString stringWithFormat:@"%@", @"iOS摸鱼周报"]; //
NSLog(@"str3.class=%@, str3 = %p, *str3 = %p", str3.class, str3, &str3);
// str3.class=__NSCFString, str3 = 0x600002ef8900, *str3 = 0x7ffeeb54dc30
```

这里的字符串类型为 `NSTaggedPointerString` 和 `__NSCFString`，他们的指针都是在栈区，这三个对象的指针还是连续的，内容部分，前者在指针里面，后者在堆区。（栈区地址比堆区地址更高）

这里再回顾下内存的分区情况，大多数情况我们只需关注进程的虚拟内存就可以了：

![](https://cdn.zhangferry.com/Images/20211216172748.png)

## 优秀博客

整理编辑：[东坡肘子](https://www.fatbobman.com)、[我是熊大](https://juejin.cn/user/1151943916921885)

1、[SwiftUI 视图的生命周期研究](https://www.fatbobman.com/posts/swiftUILifeCycle/ "@东坡肘子：SwiftUI 视图的生命周期研究") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：在 UIKit（AppKit）的世界中，通过框架提供的大量钩子（例如 viewDidLoad、viewWillLayoutSubviews 等），开发者可以将自己的意志注入视图控制器生命周期的各个节点之中，宛如神明。在 SwiftUI 中，系统收回了上述的权利，开发者基本丧失了对视图生命周期的掌控。不少 SwiftUI 开发者都碰到过视图生命周期的行为超出预期的状况（例如视图多次构造、onAppear 无从控制等）。本文将作者对 SwiftUI 视图、SwiftUI 视图生命周期的理解和研究做以介绍，供大家一起探讨。

2、[探究视图树](https://mp.weixin.qq.com/s/JMxJqCoho-LGJcLrNt9ibQ "@Javier：探究视图树") -- 来自：Javier

[@东坡肘子](https://www.fatbobman.com/)：大多 SwiftUI 的开发者都已经熟练掌握了如何从父视图向子视图传递数据的方法，但如何获取子视图的状态和变化对很多人仍然比较陌生。swiftui-lab 的 Javier 写了三篇文章详细介绍了如何通过 PreferenceKey、AnchorPreferences 等方式向上传递数据的手段。链接中提供的是 Swift 花园的中文译本。

3、[SwiftUI 中的 Text 插值和本地化](https://onevcat.com/2021/03/swiftui-text-1/ "@onevcat：SwiftUI 中的 Text 插值和本地化") -- 来自：onevcat

[@东坡肘子](https://www.fatbobman.com/)：Text 是 SwiftUI 中最简单和最常见的 View 了，相较 String，Text 提供了更加丰富的差值和本地化功能。本文不仅介绍了 Text 中关于差值和本地化的一些特色功能，并讲解了在 Text 中创建自定义差值的方法。

4、[TCA - SwiftUI 的救星？(一)](https://onevcat.com/2021/12/tca-1/ "@onevcat：TCA - SwiftUI 的救星？(一)") -- 来自博客：onevcat

[@我是熊大](https://github.com/Tliens)：SwiftUI 似乎可以真正走向前台，成为开发利器，本文是 TCA - SwiftUI 系列的第一篇文章。

5、[SwiftUI Tab Bar](https://www.objc.io/blog/2020/02/25/swiftui-tab-bar/ "SwiftUI Tab Bar") -- 来自博客：objc.io

[@我是熊大](https://github.com/Tliens)：当你信心满满的准备用 SwiftUI 开发 App 时，可能会被困在第一步：Tab Bar 样式怎么处理，本文将替你解惑。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 软件随想录

**地址**：https://book.douban.com/subject/4163938/

Joel Spolsky 的 Blog 纸质版文集，中文版由阮一峰翻译。作者 Joel Spolsky 毕业于耶鲁大学，曾任微软公司 Excel 开发小组项目经理，现在自己创业做 CEO，同时也是 Stack Overflow 的合伙人。他在书中以诙谐幽默的笔触将自己在软件行业的亲身感悟娓娓道来，其中包含关于软件、人才、创业和管理的很多看法。需要提醒读者的是本书的大部分内容都写于 2004 年底左右，是一本老书了，但其中很多内容都值得细细品味。这边节选一些有意思的观点供没看过的读者过过瘾:

> 1. 从数量上来说，优秀的人才很少，而且从不出现在招聘市场上。
> 2. 我从来没有见过哪个能用 Scheme 语言、Haskell 语言、C 语言中的指针函数编程的人，竟然不能在两天里面学会 Java，并且写出的 Java 程序质量竟然不能胜过那些有 5 年 Java 编程经验的人士。
> 3. 看东西的时候，你的视力只是在你的视野中很小一块区域是高分辨率的，而且视野中央还有相当大的一个盲点。但是，你依然想当然的认定你能够超清晰的看清视野中的每一个角落。
> 4. 别担心所有工作都被印度人抢走。😁

## 工具推荐

推荐来源：[iOSleep](https://github.com/iOSleep)

### Dropshelf

**地址**：https://pilotmoon.com/dropshelf/

**软件状态**：之前付费但是目前下架了，可以使用上面链接免费使用。

**软件介绍**：

Dropshelf 是一款 Mac OS 下的拖拽效率应用。它提供了一个可以吸附在屏幕边缘的 Dock，你可以拖拽任何东西「图片、文件、文字、链接...」暂存到 Dock 中，方便你在其他 App 中来使用。

![Dropshelf](https://cdn.zhangferry.com/Images/9964d0eee2c48e3d24ba63c09e25b10c_720w.jpeg)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第三十七期](https://mp.weixin.qq.com/s/PwZ2nIHRo0GDsjMx7lSFLg)

[iOS摸鱼周报 第三十六期](https://mp.weixin.qq.com/s/K_JHs1EoEn222huWIoJRmA)

[iOS摸鱼周报 第三十五期](https://mp.weixin.qq.com/s/fCEbYkAPlK0nm7UtLKFx5A)

[iOS摸鱼周报 第三十四期](https://mp.weixin.qq.com/s/P0HjLDCIM3T-hAgQFjO1mg)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
