# iOS摸鱼周报 第三十三期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：
> * Tips：使用 os_signpost 标记函数执行和测量函数耗时；混编｜将 Objective-C typedef NSString 作为 String 桥接到 Swift 中
> * 面试模块：
> * 优秀博客：本期为大家整理了一些关于图像识别框架Vision的文章
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

### 使用 os_signpost 标记函数执行和测量函数耗时

整理编辑：[zhangferry](zhangferry.com)

os_signpost 是 iOS12 开始支持的一个用于辅助开发调试的轻量工具，它跟 Instruments 的结合使用可以发挥很大作用。os_signpost API 较简单，其主要有两大功能：做标记、测量函数耗时。

首先我们需要引入 os_signpost 并做一些初始化工作：

```swift
import os.signpost

// test function
func bindModel {
  let log = OSLog(subsystem: "com.ferry.app", category: "SignLogTest")
  let signpostID = OSSignpostID(log: log)
  // ...
}
```

其中 subsystem 用于标记应用，category 用于标记调试分类。

后面试下它标记和测量函数的功能。

#### 做标记

```swift
let functionName: String = #function
os_signpost(.event, log: log, name: "Complex Event", "%{public}s", functionName)
```

注意这个 API 中的 `name` 和后面的 `format` 都是 StaticString 类型（format 是可选参数）。StaticString 与 String 的区别是前者的值是由编译时确认的，其初始化之后无法修改，即使是使用 var 创建。系统的日志库 OSLog 也是选择 StaticString 作为参数类型，这么做的目的一部分在于编译器可采取一定的优化，另一部分则是出于对隐私的考量。

> The unified logging system considers dynamic strings and complex dynamic objects to be **private**, and does not collect them automatically. To ensure the privacy of users, it is recommended that log messages consist strictly of **static strings** and **numbers**. In situations where it is necessary to capture a dynamic string, you may **explicitly** declare the string public using the keyword **public**. For example, `%{public}s`.

对于调试期间我们需要使用 String 附加参数的话，可以用 `%{public}s` 的形式格式化参数，以达到捕获动态字符串的目的。

#### 测量函数耗时

```swift
os_signpost(.begin, log: log, name: "Complex calculations", signpostID: signpostID)
/// Complex Event
os_signpost(.end, log: log, name: "Complex calculations", signpostID: signpostID)
```

将需要测量的函数包裹在 begin 和 end 两个 os_signpost 函数之间即可。

#### 使用

打开 Instruments，选择创建 Blank 模板，点击右上角，添加"+"号，双击选择添加 os_signpost 和 Time Profiler 两个模板。运行应用直到触发标记函数时停止，我们展开os_signpost，找到我们创建的 SignLogTest，将其加到下方。调整 Time Profiler 的 Call Tree 之后就可以看到下图样式。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20211107192353.png)

event 事件被一个减号所标记，鼠标悬停可以看到标记的函数名，begin 和 end 表示那个耗时函数执行的开始和结束用一个区间块表示。

其中 event 事件可以跟项目中的打点结合起来，例如应用内比较重要的几个事件之间发生了什么，他们之间的耗时是多少。

### 混编｜将 Objective-C typedef NSString 作为 String 桥接到 Swift 中

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

在 Objective-C 与 Swift 混编的过程中，我遇到了如下问题：

我在 Objective-C Interface 中使用 typedef 为 NSString * 取了一个有意义的类型别名 TimerID，但 Generated Swift Interface 却不尽如人意。在方法参数中 TimerID 类型被转为了 String，而 TimerID 却还是 NSString 的类型别名。

```swift
// Objective-C Interface
typedef NSString * TimerID;

@interface Timer : NSObject
+ (void)cancelTimer:(TimerID)timerID NS_SWIFT_NAME(cancel(timerID:));

@end

// Generated Swift Interface
public typealias TimerID = NSString

open class Timer : NSObject {
     open class func cancel(timerID: String)
}
```

这在 Swift 中使用的时候就遇到了类型冲突问题。由于 TimerID 是 NSString 的类型别名，而 NSString 又不能隐式转换为 String。

```swift
// Use it in Swift
let timerID: TimerID = ""
Timer.cancel(timerID: timerID) // Error: 'TimerID' (aka 'NSString') is not implicitly convertible to 'String'; did you mean to use 'as' to explicitly convert? Insert ' as String'
```

可以通过以下方式解决该问题：

1. 在 Swift 中放弃使用 TimerID 类型，全部用 String 类型
2. 在 Swift 中使用到 TimerID 的地方显示转化为 String 类型

```swift
Timer.cancel(timerID: timerID as String)
```

但这些处理方式并不好。如果从根源上解决该问题，也就是在 Generate Swift Interface 阶段将 `typedef NSString *TimerID` 转换为 `typealias TimerID = String`，那就很棒。宏 `NS_SWIFT_BRIDGED_TYPEDEF` 就派上用场了。

```swift
// Objective-C Interface
typedef NSString * TimerID NS_SWIFT_BRIDGED_TYPEDEF;

@interface Timer : NSObject
+ (void)cancelTimer:(TimerID)timerID NS_SWIFT_NAME(cancel(timerID:));

@end

// Generated Swift Interface
public typealias TimerID = String // change: NSString -> String

open class Timer : NSObject {
    open class func cancel(timerID: TimerID) // change:  String -> TimerID
}
```

现在，我可以在 Swift 中愉快地使用 TimerID 类型啦！

```swift
let timerID: TimerID = ""
Timer.cancel(timerID: timerID) 
```

除了 NSString，`NS_SWIFT_BRIDGED_TYPEDEF` 还可以用在 NSDate、NSArray 等其它 Objective-C 类型别名中。

## 面试解析

整理编辑：


## 优秀博客

本期主题：Vision

Vision 是苹果在WWDC 2017推出的图像识别框架。与Core Image、AV Capture相比，Vision 在耗电量、耗时、精确度上表现优异。

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

1、[使用Vision框架对图像进行分类](https://developer.apple.com/documentation/vision/classifying_images_with_vision_and_core_ml "使用 Vision 框架裁剪和缩放照片") -- 来自：Apple


[@我是熊大](https://github.com/Tliens)：本文演示了如何使用 Vision 和 Core ML 对图像进行识别并分类，附Apple官方Demo。

2、[识别视频流中的对象](https://developer.apple.com/documentation/vision/recognizing_objects_in_live_capture "识别视频流中的对象") -- 来自：Apple

[@我是熊大](https://github.com/Tliens)：直接识别来自相机中的视频流，实时识别物体，本文附Apple官方Demo。

3、[Swift之Vision 图像识别框架](https://juejin.cn/post/6844903576821760014#heading-1 "Swift之Vision 图像识别框架") -- 来自掘金：RunTitan

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：Vision有很多应用场景，比如人脸检测、图像对比、二维码条形码检测、文字检测、目标跟踪等。每种使用场景文章都列举了代码样例。



## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Vue Color Avatar

地址：https://github.com/Codennnn/vue-color-avatar

一个纯前端实现的头像生成网站，使用 Vite + Vue3 开发，是一款矢量风格头像的生成器，你可以搭配不同的素材组件，或者通过配置代码，来生成自己的个性化头像。

### 浏览器的工作原理：新式网络浏览器幕后揭秘

地址：https://www.html5rocks.com/zh/tutorials/internals/howbrowserswork/

这是一篇全面介绍 WebKit 和 Gecko 内部操作的入门文章，是以色列开发人员塔利·加希尔大量研究的成果。在过去的几年中，她查阅了所有公开发布的关于浏览器内部机制的数据，并花了很多时间来研读网络浏览器的源代码。学习浏览器的内部工作原理将有助于您作出更明智的决策，并理解那些最佳开发实践的个中缘由。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### swiftenv

**地址**：https://github.com/kylef/swiftenv

**软件状态**：免费，[开源](https://github.com/kylef/swiftenv)

**软件介绍**：

`swiftenv` 允许您：
* 更改每个用户的全局 Swift 版本。
* 设置每个项目的 Swift 版本。
* 允许您使用环境变量覆盖 Swift 版本。

![swiftenv](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/swiftenv.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
