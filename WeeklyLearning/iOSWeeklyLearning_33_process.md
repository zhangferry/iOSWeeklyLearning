# iOS摸鱼周报 第三十三期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：
> * Tips：
> * 面试模块：
> * 优秀博客：
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

对于某些特定需求我们必须使用 String 附加参数的话，可以用 `%{public}s` 的形式添加参数。

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

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

1、[使用Vision框架对图像进行分类](https://developer.apple.com/documentation/vision/classifying_images_with_vision_and_core_ml "使用 Vision 框架裁剪和缩放照片") -- 来自：Apple


[@我是熊大](https://github.com/Tliens)：本文演示了如何使用 Vision 和 Core ML 对图像进行识别并分类，附Apple官方Demo。

2、[识别视频流中的对象](https://developer.apple.com/documentation/vision/recognizing_objects_in_live_capture "识别视频流中的对象") -- 来自：Apple

[@我是熊大](https://github.com/Tliens)：直接识别来自相机中的视频流，实时识别物体，本文附Apple官方Demo。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



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
