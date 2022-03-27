# iOS摸鱼周报 第三十三期

![](http://cdn.zhangferry.com/Images/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：感恩节和圣诞节期间 AppStore 将正常接受审核。
> * Tips：使用 os_signpost 标记函数执行和测量函数耗时；混编｜将 Objective-C typedef NSString 作为 String 桥接到 Swift 中。
> * 面试模块：LeetCode - #1 Two Sum。
> * 优秀博客：本期为大家整理了一些关于图像识别框架 Vision 的文章。
> * 学习资料：Vue Color Avatar，一个纯前端实现的头像生成网站；一篇全面介绍 WebKit 和 Gecko 内部操作的入门文章。
> * 开发工具：swiftenv。

## 本期话题

[@zhangferry](https://zhangferry.com)：苹果发布了年末两个重要假期关于 AppStore 审核的声明。往年圣诞节期间一般都是停止审核的，今年则会正常接受提交。但是在 11 月 24 号到  28 号（感恩节），和 12 月 23 号到 27 号（圣诞节）之间的提交审核流程会比较慢。如果可以错开排期的话尽量不要在这个时间段提审。

信息来源：[Submissions now accepted through the holidays](https://developer.apple.com/news/?id=y4fgrhhe "Submissions now accepted through the holidays")

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

打开 Instruments，选择创建 Blank 模板，点击右上角，添加 "+" 号，双击选择添加 os_signpost 和 Time Profiler 两个模板。运行应用直到触发标记函数时停止，我们展开 os_signpost，找到我们创建的 SignLogTest，将其加到下方。调整 Time Profiler 的 Call Tree 之后就可以看到下图样式。

![](http://cdn.zhangferry.com/Images/20211107192353.png)

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

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

现代开发⼯程师在⾯试过程中，算法⾯试往往有⼀定程度的重要性。

算法⾯试作为基本功之⼀，它包含了太多的逻辑思维，可以考察你思考问题的逻辑和解决问题的能⼒。完全类似的业务选手只能靠`挖掘`，但当⼀个⼈逻辑思维和能⼒不错的情况下，其业务匹配及后期上⼿概率也会很⾼。 

⾯试算法题⽬在难度上（尤其是代码难度上）会略低⼀些，倾向于考察⼀些基础数据结构与算法，通过交流暴露更多的⾯试题细节。

这也就是为什么现代算法⾯试中推崇**⼀题多解**，在实际算法⾯试中出现原题的概率往往不⾼，随着与面试官交流且探讨让已知的面试题出现变化。

下⾯我们以 [LeetCode](https://leetcode.com) 开篇 [TwoSum](https://leetcode.com/problems/two-sum/ "LeetCode - #1 Two Sum") 来简要说明。

> 默认读者有关于时间复杂度和空间复杂度的概念。

### TwoSum

给定⼀个整数数组 `nums` 和⼀个整数⽬标值 `target` ，请你在该数组中找出**和**为⽬标值 `target` 的那**两个**整数，并返回它们的数组下标。 

你可以假设每种输⼊**只会对应⼀个答案**。但是，数组中**同⼀个元素**在答案⾥不能重复出现。 

你可以按**任意顺序**返回答案。 

**示例 1：**

```
输⼊：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
```

**示例 2：**

```
输⼊：nums = [3,2,4], target = 6 
输出：[1,2]
```

**示例 3：**

```
输⼊：nums = [3,3]，target = 6 
输出： [0,1]
```

**提示：**

* `2 <= nums.length <= 104` 
* `-109 <= nums[i] <= 109`
* `-109 <= target <= 109`
* **只会存在⼀个有效答案**

### 解析

作为⼏乎⼈⼈  [LeetCode](https://leetcode.com)  ，⼈⼈ Code 过的经典题⽬，本题的最优解就是时间复杂度及空间复杂度皆为 O(n) 的解法

```swift
class Solution {
  func twoSum(_ nums: [Int], _ target: Int) -> [Int] { 
    var dict: [Int: Int] = [:]
    
    for (i, n) in nums.enumerated() { 
      if let index = dict[target - n] { 
        return [i, index] 
      } 
      dict[n] = i 
    }
    
    return []
  }

}
```

但是这种面试原题，往往不是我们能正好遇到的。

#### 删减版两数之和

给定⼀个整数数组 `nums` 和⼀个整数⽬标值 `target` ，请你在该数组中找出和为⽬标值 target 的那**两个**整数，并返回它们的数组下标。

**示例 1：**

```
输⼊：nums = [2,7,11,15], target = 9 
输出：[0,1] 解释：
因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
```

这就很像我们会遇到的初始问题，现在我们一起跟`面试官` 来确认一下面试题吧！

##### 确认异常状态即确认出参与⼊参的限制

我们需要确保两数之和不会超过值的最⼤限制 `Int.Max` 以及会不会超过 `Int.min`

需要跟⾯试官确认参数的限制，以及超出限制以后返回的结果

##### 确认是否有多个答案及结果顺序，及同⼀位置能否⽤多次

确认是否存在**多个**答案，确认数组中是否存在相同数据，以及确认是否需要展示所有正确的值即答案是否唯一且两数下标是否是顺序的

例如：

```
输⼊：nums = [2,2,7,11,15], target = 9
```

这个答案可能是 `[0, 2]` 或 `[1, 2]` 这也会导致最终代码的编写

##### 确认是否整数数组是否有序

对于已经排序的数组，我们可以利⽤双指针的思想来优化我们的代码

```swift
class Solution {
  func twoSum(_ nums: [Int], _ target: Int) -> [Int] { 
    guard nums.count > 0 else {
      return []
    }

    var start = 0 
    var end = nums.count-1 
    while start < end {
      let sum = nums[start] + nums[end] 
      if sum == target { 
        return [start, end] 
      } else if sum < target { 
        start += 1 
      } else { 
        end -= 1 
      }
    } 
    
    return []
  }
}
```

##### ...

当然可能还有其他变种，如果你有什么想法也可以来丰富所有的示例。

### 总结

算法⾯试题是⼀个与⾯试官交流的好途径，而在⾯试过程中⼀步步与⾯试官交流，可以展现⾯试者逻辑思维能⼒以及沟通交流能⼒。

在实际遇到面试题的时候，我们不着急写出具体的代码，展现你的**思维过程**，利用交流丰富你的表现，思维能力和沟通交流能力。


## 优秀博客

本期主题：Vision

Vision 是苹果在 WWDC 2017 推出的图像识别框架。与 Core Image、AV Capture 相比，Vision 在耗电量、耗时、精确度上表现优异。

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

1、[使用 Vision 框架对图像进行分类](https://developer.apple.com/documentation/vision/classifying_images_with_vision_and_core_ml "使用 Vision 框架裁剪和缩放照片") -- 来自：Apple

[@我是熊大](https://github.com/Tliens)：本文演示了如何使用 Vision 和 Core ML 对图像进行识别并分类，附 Apple 官方 Demo。

2、[识别视频流中的对象](https://developer.apple.com/documentation/vision/recognizing_objects_in_live_capture "识别视频流中的对象") -- 来自：Apple

[@我是熊大](https://github.com/Tliens)：直接识别来自相机中的视频流，实时识别物体，本文附 Apple 官方 Demo。

3、[Swift之Vision 图像识别框架](https://juejin.cn/post/6844903576821760014#heading-1 "Swift之Vision 图像识别框架") -- 来自掘金：RunTitan

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：Vision 有很多应用场景，比如人脸检测、图像对比、二维码条形码检测、文字检测、目标跟踪等。每种使用场景文章都列举了代码样例。

5、[用苹果官方 API 实现 iOS 备忘录的扫描文稿功能](https://www.fatbobman.com/posts/docScaner/ "用苹果官方 API 实现 iOS 备忘录的扫描文稿功能") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：本文将介绍如何通过 VisionKit、Vision、NaturalLanguage、CoreSpotlight 等系统框架实现与备忘录扫描文稿类似的功能。

6、[理解 Vision 框架中的图片技术](https://juejin.cn/post/6844903869881778183 "理解 Vision 框架中的图片技术") -- 来自掘金：RickeyBoy

[@东坡肘子](https://www.fatbobman.com/)：本文主要介绍了 Vision 框架在图像技术方面的一些酷炫功能，并一定程度上阐述了其原理。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Vue Color Avatar

地址：https://github.com/Codennnn/vue-color-avatar

一个纯前端实现的头像生成网站，使用 Vite + Vue3 开发，是一款矢量风格头像的生成器，你可以搭配不同的素材组件，或者通过配置代码，来生成自己的个性化头像。

### 浏览器的工作原理：新式网络浏览器幕后揭秘

地址：https://www.html5rocks.com/zh/tutorials/internals/howbrowserswork/

这是一篇全面介绍 WebKit 和 Gecko 内部操作的入门文章，是以色列开发人员塔利·加希尔大量研究的成果。在过去的几年中，她查阅了所有公开发布的关于浏览器内部机制的数据，并花了很多时间来研读网络浏览器的源代码。学习浏览器的内部工作原理将有助于你作出更明智的决策，并理解那些最佳开发实践的个中缘由。

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

![swiftenv](http://cdn.zhangferry.com/Images/swiftenv.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第三十二期](https://mp.weixin.qq.com/s/6CyL0B6Zkf6KXRrfocohoQ)

[iOS摸鱼周报 第三十一期](https://mp.weixin.qq.com/s/DQpsOw90UsRg6A5WDyT_pg)

[iOS摸鱼周报 第三十期](https://mp.weixin.qq.com/s/KNyIcOKGfY5Ok-oSQqLs6w)

[iOS摸鱼周报 第二十九期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](http://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
