# iOS 摸鱼周报 第四十六期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * Tips：如何在SwiftUI中显示二维码；如何将 JSON 字典编码为 JSONEncoder 
> * 面试模块：iOS 内存管理：Autorelease 细节速记
> * 优秀博客：SwiftUI 进阶技巧
> * 学习资料：KKBOX iOS/Mac OS X 基礎開發教材
> * 开发工具：几款面向 iOS 开发的 UI 调试工具

## 本期话题

[@zhangferry](https://zhangferry.com)：苹果在北京时间的3月9号凌晨举行了春季发布会，本次发布会也是诚意满满，带来了很多惊喜。这最重要的就是 M1 Ultra 芯片，M1 Ultra 是两颗 M1 Max 的组合，但这也是不是简单的拼接，而是得益于M1 Max 的隐藏特性：突破性的晶粒到晶粒技术，然后使用了一个叫做 UltraFusion 的封装架构将两颗M1 Max 融合到一起，对于应用层来说它就是一颗完整的芯片。它拥有这些东西：

* 20 核中央处理器：16 个高性能核心 + 4 个高能效核心，用于CPU密集操作。

* 64 核图形处理器，用于图形密集任务。

* 32 个神经网络核心，用于机器学习。

* 10 个多媒体处理引擎，用于提升视频的编解码能力，对 H264/HEVC/ProRes/ProRes RAW 处理有硬件层面的加速。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/image-20220310224908485.png)

当然这么强大的芯片要有一个产品使用，它就是 Mac Studio。这是一条新的产品线，它看上去像是 Mac Mini 「加厚」版，但得益于其强大的性能，它的定位确是工作站。到目前为止 Mac 端的产品线基本都用上 M1 了，除了 Mac Pro。Mac Pro 之前的定位也是工作站，从「垃圾桶」进化到「行李箱」，它作为苹果性能的最强代表不断经验着我们，但随着 M1 的到来，这两款产品都不香了，更不用说「行李箱」起售价就 47999。虽然 M1 Ultra 已经让我们大呼苹果不讲武德了，但发布会结尾特意提了一下 Mac Pro，这很有理由相信作为性能天花板的 Mac Pro 的下一代才是真正的大杀器。

## 开发 Tips

### 如何在 SwiftUI 中显示二维码 

整理编辑：[FBY展菲](https://github.com/fanbaoying)

使用 `CoreImage` 生成二维码图像。

```swift
import SwiftUI
import CoreImage.CIFilterBuiltins
 
struct QRView: View {
    let qrCode: String
    @State private var image: UIImage?
 
    var body: some View {
        ZStack {
            if let image = image {
                Image(uiImage: image)
                    .resizable()
                    .interpolation(.none)
                    .frame(width: 210, height: 210)
            }
        }
        .onAppear {
            generateImage()
        }
    }
 
    private func generateImage() {
        guard image == nil else { return }
 
        let context = CIContext()
        let filter = CIFilter.qrCodeGenerator()
        filter.message = Data(qrCode.utf8)
 
        guard
            let outputImage = filter.outputImage,
            let cgImage = context.createCGImage(outputImage, from: outputImage.extent)
        else { return }
 
        self.image = UIImage(cgImage: cgimg)
    }
}
```
参考：[如何在 SwiftUI 中显示二维码 - Swift社区](https://mp.weixin.qq.com/s/qsc8ZCnrpeHu4hQoM_BTzg)

### 如何将 JSON 字典编码为 JSONEncoder 

整理编辑：[FBY展菲](https://github.com/fanbaoying)

`JSONEncoder` 处理类型安全，因此我们需要为所有可能的类型声明枚举 `JSONValue`。我们还需要一个自定义 `initializer` 来从 JSON 字典中初始化 `JSONValue`。

```swift
import Foundation
 
enum JSONValue {
    case string(String)
    case int(Int)
    case double(Double)
    case bool(Bool)
    case object([String: JSONValue])
    case array([JSONValue])
}
 
extension JSONValue: Encodable {
    public func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        switch self {
        case .string(let string): try container.encode(string)
        case .int(let int): try container.encode(int)
        case .double(let double): try container.encode(double)
        case .bool(let bool): try container.encode(bool)
        case .object(let object): try container.encode(object)
        case .array(let array): try container.encode(array)
        }
    }
}
 
extension JSONValue {
    init?(any: Any) {
        if let value = any as? String {
            self = .string(value)
        } else if let value = any as? Int {
            self = .int(value)
        } else if let value = any as? Double {
            self = .double(value)
        } else if let value = any as? Bool {
            self = .bool(value)
        } else if let json = any as? [String: Any] {
            var dict: [String: JSONValue] = [:]
            for (key, value) in json {
                dict[key] = JSONValue(any: value)
            }
            self = .object(dict)
        } else if let jsonArray = any as? [Any] {
            let array = jsonArray.compactMap { JSONValue(any: $0) }
            self = .array(array)
        } else {
            return nil
        }
    }
}
 
var dict: [String: Any] = [
    "anArray": [1, 2, 3],
    "anObject": [
        "key1": "value1",
        "key2": "value2"
    ],
    "aString": "hello world",
    "aDouble": 1.2,
    "aBool": true,
    "anInt": 12
]
 
let encoder = JSONEncoder()
let value = JSONValue(any: dict)
let data = try! encoder.encode(value)
print(String(data: data, encoding: .utf8))
```

参考：[如何将 JSON 字典编码为 JSONEncoder - Swift社区](https://mp.weixin.qq.com/s/PI7s8cXxzErqOB0e9BHqvg)

## 面试解析

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Autorelease 细节速记

本文内容是基于 `Autorelease-818`版本源码来分析的， 如果你还未了解 `Autorelease`的原理，请先按照另一位编辑的文章学习 [AutoreleasePool](https://mp.weixin.qq.com/s/Z3MWUxR2SLtmzFZ3e5WzYQ)。下面会介绍一些源码细节。

#### AutoreleasePool 数据结构

`AutoreleasePool`底层数据结构是基于 `AutoreleasePoolPage`, 本质上是个双向链表， 每一页的大小为 4K,可以在 `usr/include/mach/arm/vm_param.h`文件中查看 `PAGE_MIN_SIZE`的值，

```cpp
#define PAGE_MAX_SHIFT          14
#define PAGE_MAX_SIZE           (1 << PAGE_MAX_SHIFT)

#define PAGE_MIN_SHIFT          12
#define PAGE_MIN_SIZE           (1 << PAGE_MIN_SHIFT)

class AutoreleasePoolPage : private AutoreleasePoolPageData
{
    static size_t const SIZE =
        // `PROTECT_AUTORELEASEPOOL`默认是定义为 0 的，
    #if PROTECT_AUTORELEASEPOOL
            PAGE_MAX_SIZE;  // must be multiple of vm page size 必须是 vm 页面大小的倍数 定义为1<<14 = 4096K,正好是虚拟页大小
    #else
            PAGE_MIN_SIZE;  // size and alignment, power of 2 大小和对齐， 2的指数倍
    #endif
}
```

#### 64 位系统下的存储优化

在最新的 `818`版本代码中，`AutoreleasePoolPage::add()`中对连续添加的相同对象存储方式做了优化，使用 `LRU` 算法结合新的`AutoreleasePoolEntry` 对象来合并存储，简化后核心源码如下：

```cpp
struct AutoreleasePoolPageData
    struct AutoreleasePoolEntry {
            uintptr_t ptr: 48;  // 关联的 autorelease 的对象
            uintptr_t count: 16; // 关联对象 push 的次数
            static const uintptr_t maxCount = 65535; // 2^16 - 1 可以存储的最大次数
        };
	// ...其他变量
}

id *add(id obj)
{
      // .. 准备工作
        for (uintptr_t offset = 0; offset < 4; offset++) {
                        AutoreleasePoolEntry *offsetEntry = topEntry - offset;
                        if (offsetEntry <= (AutoreleasePoolEntry*)begin() || *(id *)offsetEntry == POOL_BOUNDARY) {
                            break;
                        }
                        if (offsetEntry->ptr == (uintptr_t)obj && offsetEntry->count < AutoreleasePoolEntry::maxCount) {
                            if (offset > 0) {
                                AutoreleasePoolEntry found = *offsetEntry;
                                // 将offsetEntry + 1中
                                memmove(offsetEntry, offsetEntry + 1, offset * sizeof(*offsetEntry));
                                *topEntry = found;
                            }
                            topEntry->count++;
                            ret = (id *)topEntry;  // need to reset ret
                            goto done;
                        }
#endif
        // 旧版本依次插入对象的存储方式
    }
```

如果使用 `LRU` 算法, 则插入时从 `next`指针向上遍历最近的四个对象， 遍历中如果和当前对象匹配，则 `Entry` 实体记录的 `count`属性加一, 然后通过 `memmove`函数移动内存数据，将匹配的 `Entry`放到距离 `next`指针最近的位置，以实现 `LRU`的特征。如果只是单纯的合并存储，则只匹配 `next`指针相邻的`Entry`，未匹配到则插入

> 是否开启合并和 `LRU`的环境变量为`OBJC_DISABLE_AUTORELEASE_COALESCING` & `OBJC_DISABLE_AUTORELEASE_COALESCING_LRU`
>
> 另外最好一起准备下缓存淘汰算法，因为如果面试中提到了 `LRU`，面试官很可能会延伸到缓存算法实现，比如 `LFU`、`LRU`。

#### 和线程以及 Runloop 的关系

`AutoreleasePool`和线程的直观关系：

1. 数据结构中存储了和线程相关的成员变量 `thread`，

2. 在实现方案中使用了 `TLS`线程相关技术用来存储状态数据。例如 `Hotpage`以及 `EMPTY_POOL_PLACEHOLDER`等状态值。

3. `objc`初始化时调用了 `AutoreleasePoolPage::init()`，该函数内部通过 `pthread_key_init_np`注册了回调函数 `tls_dealloc`,在线程销毁时调用清理 `Autorelease`相关内容。大致流程为：`_pthread_exit` => `_pthread_tsd_cleanup` => `_pthread_tsd_cleanup_new` => `_pthread_tsd_cleanup_key` => `tls_dealloc`。相关源码可以在 `libpthread`中查看。

    ```cpp
    static void tls_dealloc(void *p) 
        {
            if (p == (void*)EMPTY_POOL_PLACEHOLDER) {
                // No objects or pool pages to clean up here.
                return;
            }
            // reinstate TLS value while we work
            setHotPage((AutoreleasePoolPage *)p);
    
            if (AutoreleasePoolPage *page = coldPage()) {
                if (!page->empty()) objc_autoreleasePoolPop(page->begin());  // pop all of the pools
                if (slowpath(DebugMissingPools || DebugPoolAllocation)) {
                    // pop() killed the pages already
                } else {
                    page->kill();  // free all of the pages
                }
            }
            // clear TLS value so TLS destruction doesn't loop
            setHotPage(nil);
        }
    ```

    由以上流程可知，子线程处理 `Autorelease` 的时机一般有两种：线程销毁时 & 自定义 `pool`作用域退出时

    在主线程中由于开启了 `Runloop`并且主动注册了两个回调，所以在每次 `Runloop`循环时都会去处理默认添加的 `AutoreleasePool`，该详细内容请参考文章  [AutoreleasePool](https://mp.weixin.qq.com/s/Z3MWUxR2SLtmzFZ3e5WzYQ)，这也不做重复复述。

#### Autorelease ARC环境下基于 tls 的返回值优化方案以及失效场景

主要是通过嵌入 `objc_autoreleaseReturnValue` & `objc_retainAutoreleasedReturnValue`两个函数，基于 `tls`存储状态值实现优化。

优化思路概括为：

- `objc_autoreleaseReturnValue` 通过 `__builtin_return_address()`函数可以查找到函数返回后下一条指令的地址，判断是否为 `mov x29, x29`（arm64）进而决定是否进行优化，
- 如果开启优化会设置 `tls`存储` 状态值 1 `并直接返回对象，否则放入自动释放池走普通逻辑
- `objc_retainAutoreleasedReturnValue`调用`acceptOptimizedReturn`校验 `tls`中的值是否为 1，为 1 表示启动优化直接返回对象， 否则走未优化逻辑先 `retain` 再放入 自动释放池

> 优化思路是基于 `tls`以及`__builtin_return_address()`实现的，以是否插入无实际效果的汇编指令 `mov x29, x29`作为优化标识。 另外查看源码时需要注意 `objc_retainAutoreleasedReturnValue`和`objc_retainAutoreleaseReturnValue`的区别

ARC 下函数返回值是否一定会开启优化呢，存在一种情况会破坏系统的优化逻辑，即 `for`或者`while`等场景。示例如下：

```objective-c
- (HWModel *)takeModel {
//    for (HWModel *model in self.models) {}
    HWModel *model = [HWModel new];
    return model;
}
```

如果打开注释代码，会导致返回的 `model`未优化，通过动态调试可以查看原因。

注释 `for`代码后跳转用的 `b`指令，所以 `lr` 寄存器存储的是调用方调用 `takeModel`函数后的指令地址

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/weekly_45_interview_02.png)

有 `for` 循环时，跳转到 `objc_autoreleaseReturnValue`的汇编指令是 `bl`。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/weekly_45_interview_01.png)

`bl`表示执行完函数后继续执行后续指令，后续汇编指令目的主要是为了检测是否存在函数调用栈溢出操作，详细解释可以参考[Revisit iOS Autorelease  二](http://satanwoo.github.io/2019/07/07/RevisitAutorelease2/)。这造成我们上面提到的 `__builtin_return_address()`函数获取到的返回值下一条指令地址，并不是优化标识指令 `mov x29 x29`，而是检测代码指令，导致优化未开启。

> 未开启优化的影响是多做一次 `retain`操作和两次 `autorelease`操作， 笔者未测试出五子棋前辈遇到的 `Autoreleas` 对象未释放的情况， 可能是后续 apple 已经优化过，如果读者有不同的结果，欢迎指教

总结： 以上是笔者在搜集面试题时关于 `AutoreleasePool`的一些扩展内容，再次强调需要精读[AutoreleasePool](https://mp.weixin.qq.com/s/Z3MWUxR2SLtmzFZ3e5WzYQ)，尤其需要掌握 `ARC` 下手动处理的几种场景。希望各位可以对 `Autorelease`面试题一网打尽。

* [黑幕背后的Autorelease](https://blog.sunnyxx.com/2014/10/15/behind-autorelease/ "黑幕背后的Autorelease")
* [AutoreleasePool](https://mp.weixin.qq.com/s/Z3MWUxR2SLtmzFZ3e5WzYQ "AutoreleasePool")
* [Revisit iOS Autorelease  一](http://satanwoo.github.io/2019/07/02/RevisitAutorelease/?nsukey=jw8uyyU1C%2BzqPgSpg5Kie0F9Bj4HNHiPMBkxPWPBuEs1ZyVoZwklMAJVkv0TeJgILqxLQOH2a0Di8DhFj5abLdtFE3p09pb3az4o9B7IY7rvyZHamZN1OIh5zBQZv1J%2FnHLc6QkiMW%2Fo2PY9fVAeVQN%2FQ5lBojKaT%2FXmKQuCTY5E1MoBK4Ir7Qi6un5pXxvKQutSkFhgEVUn%2FboyV6pdxQ%3D%3D "Revisit iOS Autorelease  一")
* [Revisit iOS Autorelease  二](http://satanwoo.github.io/2019/07/07/RevisitAutorelease2/ "Revisit iOS Autorelease  二")
* [[iOS13 一次Crash定位 - 被释放的NSURL.host](https://segmentfault.com/a/1190000020058030)](https://segmentfault.com/a/1190000020058030 "[iOS13 一次Crash定位 - 被释放的NSURL.host](https://segmentfault.com/a/1190000020058030)")

## 优秀博客

> 转眼间 SwiftUI 已推出接近 3 年。越来越多的开发者尝试使用 SwiftUI 来构建其应用。本期介绍的博文将更多地涉及 SwiftUI 的进阶技巧，帮助开发者对 SwiftUI 有更加深入的认识和理解。

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[无法解释的 SwiftUI —— SwiftUI 的编程语言本质](https://wezzard.com/post/2022/03/unexplained-swiftui-the-programming-language-nature-of-swiftui-d20e "Unexplained SwiftUI - The Programming Language Nature of SwiftUI") -- 来自：WeZZard

[@东坡肘子](https://www.fatbobman.com/)：作者 WeZZard 从一个十分新颖的角度来看待、分析 SwiftUI。通过一个斐波纳契数实例，来展示 SwiftUI 的图灵完整性，进而提出一个有趣的观点——SwiftUI 是一种编程语言，而不是 UI 框架。

2、[SwiftUI 底层：可变视图](https://movingparts.io/variadic-views-in-swiftui "SwiftUI under the Hood: Variadic Views") -- 来自：The Moving Parts Team

[@东坡肘子](https://www.fatbobman.com/)：本文介绍了一些 View 协议中尚未公开的 API。通过使用这些 API，开发者可以编写出更加强大、灵活，且与原生实现类似的容器，构建自己的布局逻辑。作者 Moving Parts 团队当前正在开发一个功能强大的 SwiftUI 组建库。

3、[了解 SwiftUI 如何以及何时决定重绘视图](https://www.donnywals.com/understanding-how-and-when-swiftui-decides-to-redraw-views/ "Understanding how and when SwiftUI decides to redraw views") -- 来自：Donny Wals

[@东坡肘子](https://www.fatbobman.com/)：作者通过观察和实践，尝试了解和总结 SwiftUI 中对视图重绘的规律。尽管该文没有给出内部实现的具体证明，但沿着作者的测试路径，读者依然可以从中获取到相当宝贵的经验。

4、[了解 SwiftUI 的 onChange](https://www.fatbobman.com/posts/onChange/ "了解 SwiftUI 的 onChange") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：onChange 是从 SwiftUI 2.0 后提供的功能，可以将其作为另一种驱动视图重绘的手段。本文将对 onChange 的特点、用法、注意事项以及替代方案做以详细介绍。结合上文「了解 SwiftUI 如何以及何时决定重绘视图」以及「SwiftUI 视图的生命周期研究」一文，可以对视图的计算、布局、绘制有更深入的了解。

5、[谁说我们不能对 SwiftUI 视图进行单元测试？](https://nalexn.github.io/swiftui-unit-testing/ "Who said we cannot unit test SwiftUI views?") -- 来自：Alexey Naumov

[@东坡肘子](https://www.fatbobman.com/)：因为很难构建依赖和运行环境，对 SwiftUI 视图进行单元测试是十分困难的。Alexey Naumov 是著名的 SwiftUI 测试框架 ViewInspector 的作者，本文介绍了他在创建 ViewInspector 框架背后的故事，其中有关获取 SwiftUI 黑盒中秘密的思路和途径十分值得借鉴。

6、[高级 SwiftUI 动画 1-5](https://mp.weixin.qq.com/s/5KinQfNtcovf_451UGwLQQ "高级 SwiftUI 动画") -- 来自：Javier 中文版：Swift 君

[@东坡肘子](https://www.fatbobman.com/)：仅需少量的代码，SwiftUI 即可为开发者实现相当优秀的动画效果。但如果想创建更加炫酷、灵活、高效的动画则需要掌握更多的知识和高级技巧。本系列文章已持续更新 2 年之久（SwiftUI 诞生至今不到 3 年），详细讲解了各种有关 SwiftUI 高级动画的内容。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### KKBOX iOS/Mac OS X 基礎開發教材

**地址**：https://zonble.gitbooks.io/kkbox-ios-dev/content/

一份来自台湾 KKBOX 的 iOS/Mac OS 开发部门编写的新人学习材料。这份学习材料不算是从 0 到 1 的入门材料，阅读这份教材需要一些简单的基础，教材主要是在你已经会一些简单 OC 代码的基础上帮助你深入探讨一些在代码中常见的小问题和小细节，也是对技术探索方向的一些指引和指导。教材中的描述语言非常亲切不生硬，就像是有一位同龄人在你旁边指导你的代码有什么问题一样，阅读体验非常不错，虽然内容略有陈旧，但也值得新手开发者阅读一下。

## 工具推荐

本次推荐一系列关于 UI 调试的软件，包含电脑端以及 App 端两种类型；

**电脑端**

- [Reveal](https://revealapp.com/)：经典UI调试软件，但需要付费；
- [Lookin](https://lookin.work/)：腾讯出品的一款免费好用的 iOS UI 调试软件；

**App 端**

- [FLEX](https://github.com/FLEXTool/FLEX)：FLEX (Flipboard Explorer) 是一套用于 iOS 开发的应用内调试工具；
- [啄幕鸟iOS开发工具](https://github.com/alibaba/youku-sdk-tool-woodpecker)：阿里出品的一套用于 iOS 开发的应用内调试工具；

> 其中 Reveal、Lookin、FLEX 都有对应的`Tweak`，有越狱设备的小伙伴可以玩一玩；

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS 成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第四十五期](https://mp.weixin.qq.com/s/_N98ADlfQCUkxYjmH0SvZw)

[iOS摸鱼周报 第四十四期](https://mp.weixin.qq.com/s/q__-veuaUZAK6xGQFxzsEg)

[iOS摸鱼周报 第四十三期](https://mp.weixin.qq.com/s/Ktk5wCMPZQ5E-UASwHD7uw)

[iOS摸鱼周报 第四十二期](https://mp.weixin.qq.com/s/ybANWeLNHPOTkr5_alha9g)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
