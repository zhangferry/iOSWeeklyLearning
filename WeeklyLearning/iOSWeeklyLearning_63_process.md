# iOS 摸鱼周报 #59

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：Apple 企业家培训营已开放申请
> * 本周学习：Swift 当中的 Sequence
> * 内容推荐：
> * 摸一下鱼：
> * 岗位推荐：

## 本期话题

### [Apple Entrepreneur Camp 已开放申请，欢迎女性、黑人和西班牙裔/拉丁裔创业者参加](https://developer.apple.com/cn/news/?id=g2414inv "Apple Entrepreneur Camp 已开放申请，欢迎女性、黑人和西班牙裔/拉丁裔创业者参加")

[@远恒之义](https://github.com/eternaljust)：Apple Entrepreneur Camp（苹果企业家培训营）创建目的是为 App 驱动型组织中的少数群体创业者及开发者提供支持，助力其研发新一代的前沿 App 并开拓全球网络，鼓励这些创业者在技术领域不断探索并取得持续发展。

Apple Entrepreneur Camp 的核心是一个密集的技术实验室，获得申请的组织可免费获得以下服务：
* Apple 工程师提供的一对一代码级指导。
* Apple 开发人员代表的持续支持至少一年。
* 一年的 Apple Developer Program 会员资格。
* 访问 Apple Entrepreneur Camp 校友网络，一个由鼓舞人心且雄心勃勃的领导者组成的世界级团体。

世界各地的开发人员都接受申请，你的组织最多可以有三名成员参加。不过必须具备以下资格才能申请成功：
* 你的组织必须具备：
  * 一位女性的创始人、联合创始人或首席执行官。
  * 一位熟练使用 Swift 或 Objective-C 的女性开发者。
  * 以及 App Store 上的现有应用程序或 TestFlight 中的功能性 beta 版本，或者同等的产品。
* 女性创始人、联合创始人或首席执行官；女性开发者；以及另一位年满 18 岁且熟练英语的同事，能够在整个实验室期间一起参加。

三组面向女性、黑人以及西班牙裔及拉丁裔创业者的在线课程将在 2022 年 10 月开展，国内符合条件的创业者可以选择女性这一组提交申请。申请截止日期为 2022 年 8 月 24 日。

谜底科技是一家杭州小而精的开发团队，创始人为柳毅和梁逸伦夫妇，他们开发了许多优秀的应用产品，其中包括广受好评的 OffScreen。谜底科技的梁逸伦是首批参加 Apple 企业家培训营的中国开发者代表之一。

![谜底科技柳毅和梁逸伦夫妇](https://cdn.zhangferry.com/Images/midi-couple.jpg)

## 本周学习

整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)

### 什么是 Sequence？
`Sequence` 协议是集合类型的基础，`Swift` 中的 `Sequence` 协议为序列提供了迭代能力。 `Sequence` 协议只要求实现 `makeIterator()` 方法，该方法会返回一个迭代器 `Iterator`，我们来看一下 `Sequence` 源码实现:

```Swift
public protocol Sequence {
  /// 元素类型
  associatedtype Element 
  
  /// 迭代器
  associatedtype Iterator: IteratorProtocol where Iterator.Element == Element
  
  /// 子序列
  associatedtype SubSequence : Sequence = AnySequence<Element>
    where Element == SubSequence.Element,
          SubSequence.SubSequence == SubSequence
  
  /// 返回当前迭代器
  __consuming func makeIterator() -> Iterator
  ///...
}
```

子序列 `subSequence`  是 `Sequence` 的另一个关联类型，通过切片操作（`split`,`prefix`,`suffix`,`drop`等）会返回 `subSequence` 类型



首先我们先看下 `IteratorProtocol` 的源码:

```Swift
public protocol IteratorProtocol {
  
  associatedtype Element

  mutating func next() -> Element?
}
```

`IteratorProtocol` 的核心是 `next()`  方法，这个方法在每次被调用时返回序列中的下一个值。当序列下一个值为空时，`next()` 则返回 `nil` 



`IteratorProtocol` 协议与 `Sequence` 协议是一对紧密相连的协议。序列通过创建一个提供对其元素进行访问的迭代器，它通过跟踪迭代过程并在调用 `next()` 时返回一个元素。

`for-in` 访问序列或者集合时，`Swift` 底层则是通过迭代器来循环遍历数据

```Swift
let numbers = ["1", "2", "3"]
for num in numbers {
    print(num)
}

/// 底层代码
let numbers = ["1", "2", "3"]
var iterator = numbers.makeIterator()
while let num = iterator.next() {
    print(num)
}
```



我们可以实现一个自己的序列，实现一个输出 0..n 的平方数的序列

```Swift
struct SquareIterator: IteratorProtocol {
    typealias Element = Int
    var state = (curr: 0, next: 1)
    mutating func next() -> SquareIterator.Element? {
        let curr = state.curr
        let next = state.next
        state = (curr: next, next: next + 1)
        if curr == 0 {
            return 0
        }
        return curr * curr
    }
}

struct Square: Sequence {
    typealias Element = Int
    func makeIterator() -> SquareIterator {
        return SquareIterator()
    }
}

// 通过实现了 Sequence 与 IteratorProtocol 两个协议，就可以实现我们的自定义序列
let square = Square()
var iterator = square.makeIterator()
while let num = iterator.next(), num <= 100 {
    print(num) // 0,1,4,9,16,25,36,49,64,81,100
}
```

 我们实现了一个自定义的序列，它支持通过迭代器遍历序列的所有元素，但是无法通过索引下标的方式来访问序列元素，想要实现下标访问，就需要 `Collection` 协议了



### Collection
`Collection` 继承自 `Sequence` ，是一个元素可以反复遍历并且可以通过索引的下标访问的有限集合。我们来看一下 `Collection` 源码实现：

```Swift
public protocol Collection: Sequence {
  /// 重写 Sequence 的 Element 
  override associatedtype Element
  associatedtype Index : Comparable
  
  /// 非空集合中第一个、最后一个元素的位置；
  var startIndex: Index { get }
  var endIndex: Index { get }
  associatedtype Iterator = IndexingIterator<Self>
  
  /// 重写 Sequence 的 makeIterator 
  override __consuming func makeIterator() -> Iterator

  associatedtype SubSequence: Collection = Slice<Self>
  where SubSequence.Index == Index,
        Element == SubSequence.Element,
        SubSequence.SubSequence == SubSequence
  
  /// 下标访问集合元素
  @_borrowed
  subscript(position: Index) -> Element { get }
  subscript(bounds: Range<Index>) -> SubSequence { get }

  associatedtype Indices : Collection = DefaultIndices<Self>
    where Indices.Element == Index, 
          Indices.Index == Index,
          Indices.SubSequence == Indices
   /// 集合的索引    
  var indices: Indices { get }
}
```



通过源码解析，我们可以发现 `Collection` 与 `Sequence` 最大的不同点是提供了索引能力，提供了通过下标访问元素的能力。 `Collection` 的自定义了迭代器 `IndexingIterator` , 我们来看一下 `IndexingIterator` 的源码实现：

 ```Swift
public struct IndexingIterator<Elements : Collection> {
  /// 需要迭代的集合
  internal let _elements: Elements
  
  /// 记录遍历的index
  internal var _position: Elements.Index
  
  init(_elements: Elements) {
    self._elements = _elements
    self._position = _elements.startIndex
  }
  init(_elements: Elements, _position: Elements.Index) {
    self._elements = _elements
    self._position = _position
  }
}
extension IndexingIterator: IteratorProtocol, Sequence {
  public typealias Element = Elements.Element
  public typealias Iterator = IndexingIterator<Elements>
  public typealias SubSequence = AnySequence<Element>
  
  public mutating func next() -> Elements.Element? {
    if _position == _elements.endIndex { return nil }
    let element = _elements[_position]
    _elements.formIndex(after: &_position)
    return element
  }
}
```

从源码可以看出，`IndexingIterator` 的主要作用就是在迭代器执行 `next()`方法时，记录了当前的 `position`，从而实现了记录索引，以及当 `position `等于 `elements.endIndex` 时，返回 `nil`


这只是 `Collection` 的冰山一角，还有`LazySequence`、高阶函数实现等， 如果感兴趣的同学，可以深入研究研究


## 内容推荐

1、[Experimenting with Live Activities](https://oleb.net/2022/live-activity/ "Experimenting with Live Activities") -- 来自：Ole Begemann

[@远恒之义](https://github.com/eternaljust)：上周更新的 iOS 16 beta 4 是第一个支持实时活动 Live Activities 的版本，实时活动是一个类似于小组件的视图，放置在锁定屏幕底部并能实时更新。苹果官方推荐的有用示例包括现场体育比分或火车出发时间。

本文作者和一群朋友设计了一个小盒子，可以连接到自行车的轮毂发电机，测量速度和距离，并通过蓝牙将数据发送到 iOS 应用程序，再利用 Live Activities 把数据同步更新到手机锁定屏幕上。本文是作者使用该 API 来实现第一个 Live Activities 的笔记，文中展示了一个实际操作视频，同时介绍了作者使用 Live Activities 的一些尝试和疑问，主要关于实时活动的几点：使用限制条件、锁屏配色、动画控制以及代码共享。

2、[Ultimate guide on Timer in Swift](https://www.swiftanytime.com/ultimate-guide-on-timer-in-swift/ "Ultimate guide on Timer in Swift") -- 来自：Team SA

[@远恒之义](https://github.com/eternaljust)：计时器 Timer 是用于在特定时间间隔后执行任何任务的类。计时器在 Swift 中使用非常方便，我们可以用于执行有延迟的任务或重复的工作。本文介绍以下了内容：如何执行任务，重复和非重复的定时器，使用 RunLoop 模式，跟踪计时器，定时器优化以减少能源和功率影响。这些内容覆盖了 Timer 方方面面的使用场景，是一份 Swift 计时器的终极指南。

3、[Variable Color in SF Symbols 4](https://sarunw.com/posts/sf-symbols-variable-color/ "Variable Color in SF Symbols 4") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：今年在 WWDC22 中，Apple 推出了 SF Symbols 4，带来了新特性可变颜色 Variable Color，你可以根据百分比值来更改符号的外观显示。新功能将有利于一些可以显示进度趋势的符号，例如 Wi-Fi 信号、扬声器响度。需要注意的是，并非所有符号都支持可变颜色。你需要下载最新的 SF Symbols App，通过从左侧面板中选择“变量”类别来浏览支持可变颜色的符号。

4、[How to Use the SwiftUI PhotosPicker](https://swiftsenpai.com/development/swiftui-photos-picker/?utm_source=rss&utm_medium=rss&utm_campaign=swiftui-photos-picker "How to Use the SwiftUI PhotosPicker") -- 来自：Lee Kah Seng

[@远恒之义](https://github.com/eternaljust)：在今年的 WWDC22 中，Apple 对 SwiftUI 进行了大量改进，SwiftUI 终于在 iOS 16 中获得了自己的原生图片选择器视图 PhotosPicker。PhotosPicker 视图支持 PHPickerViewController 中所有常见的功能，包括单选、多选、资源类型过滤和相册切换等功能。在 SwiftUI 中使用 PhotosPicker 视图非常简单，本文将介绍如何使用该图片选择器。

5、[实时切换 Core Data 的云同步状态](https://www.fatbobman.com/posts/real-time-switching-of-cloud-syncs-status/ "实时切换 Core Data 的云同步状态") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：在 WWDC 2019 上，苹果推出了 Core Data with CloudKit API，极大地降低了 Core Data 数据的云同步门槛。由于该服务对于开发者来说几乎是免费的，因此在之后的几年中，越来越多的开发者在应用中集成了该服务，并为用户带来了良好的跨设备、跨平台的使用体验。本文将对实时切换 Core Data 云同步状态的实现原理、操作细节以及注意事项进行探讨和说明。

6、[避免 SwiftUI 视图的重复计算](https://www.fatbobman.com/posts/avoid_repeated_calculations_of_SwiftUI_views/ "避免 SwiftUI 视图的重复计算") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：在 SwiftUI 中，每个视图都有与其对应的状态，当状态变化时，SwiftUI 都将重新计算与其对应视图的 body 值，这就是 SwiftUI “视图是状态的函数”的基本概念。如果视图响应了不该响应的状态，或者视图的状态中包含了不该包含的成员，都可能造成 SwiftUI 对该视图进行不必要的更新（重复计算），当类似情况集中出现，将直接影响应用的交互响应，并产生卡顿的状况。通常我们会将这种多余的计算行为称之为过度计算或重复计算。本文将介绍如何减少（甚至避免）类似的情况发生，从而改善 SwiftUI 应用的整体表现。

## 摸一下鱼

现在的网页功能是非常强，不只是各种各样的应用，现在很多操作系统都搬到了网页上，本期内容会推荐几个在线的操作系统，虽然不知真的操作系统，但作为预览，功能还是很丰富的。

1、[win11在线体验](https://win11.blueedge.me/ "win 11 在线体验")：该项目使用React实现的，代码地址：https://github.com/blueedgetechno/win11React 。

![](https://cdn.zhangferry.com/Images/20220731124759.png)

2、[操作系统风格的博客](goodmanwen.github.io)：这是一个 Blog 项目，该 Blog 的主题是模拟 Linux 桌面主题中的 Deepin distro。其本质是一个托管在 Github Page 上的博客，你也可以配置一个这样酷酷的主题。

![](https://cdn.zhangferry.com/Images/20220731130051.png)

3、[dustinbrett.com](dustinbrett.com)：一个模拟 Windows 的网站，也可以把它理解成一个作者的个人网站。这里面还集成了一个毁灭战士早期的版本，你可以在这个网站里玩它。

![](https://cdn.zhangferry.com/Images/20220731143028.png)

4、[copy/v86](https://copy.sh/v86/)：在浏览器中运行 x86 操作系统，这个模拟跟前面提到的 H5 技术不同，它是采用 WebAssembly 把原来的 x86 OS 代码转成 wasm 在线上运行的，更贴近「真」操作系统。

![](https://cdn.zhangferry.com/Images/20220731150332.png)

这个是远程运行的 Windows 98 系统：

![](https://cdn.zhangferry.com/Images/20220731145541.png)

## 岗位推荐



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #56 | WWDC 进行时](https://mp.weixin.qq.com/s/ZyGV6WlFsZOX6Aqgrf1QRQ)

[iOS 摸鱼周报 #55 | WWDC 码上就位](https://mp.weixin.qq.com/s/zDhnOwOiLGJ_Nwxy5NBePw)

[iOS 摸鱼周报 #54 | Apple 辅助功能持续创新](https://mp.weixin.qq.com/s/6jdqa143Y5yr6lbjCuzlqA)

[iOS 摸鱼周报 #53 | 远程办公正在成为趋势](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
