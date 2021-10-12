# iOS摸鱼周报 第二十七期

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

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)

### 低电量模式

从 iOS 9 开始，Apple 为 iPhone 添加了低电量模式（**Low Power Mode** ）。用户可以在可以在**设置**>**电池**启用低电量模式。在低电量模式下，iOS 通过制定某些节能措施来延长电池寿命，包括但不限于以下措施：

* 降低 CPU 和 GPU 性能，降低屏幕刷新率
* 包括联网在内的主动或后台活动都将被暂停
* 降低屏幕亮度
* 减少设备的自动锁定时间
* 邮件无法自动获取，陀螺仪及指南针等动态效果将被减弱，动态屏保将会失效
* 对于支持 5 G 的 iPhone 设备来说，其 5G 能力将被限制，除非你在观看流媒体

上述节能措施是否会影响到你的应用程序，如果有的话，你可能需要针对低电量模式来适当采取某些措施。

#### lowPowerModeEnabled

我们可以通过 **NSProcessInfo** 来获取我们想要的进程信息。这个**线程安全**的单例类可以为开发人员提供与当前进程相关的各种的信息。

一个值得注意的是，NSProcessInfo 将尝试将环境变量和命令行参数解释为 Unicode，以 UTF-8 字符串返回。如果该进程无法成功转换为 Unicode 或随后的 C 字符串转换失败的话 —— 该进程将被**忽略**。

当然，我们还是需要关注于低电量模式的标志，一个表示设备是否启用了低电量模式的布尔值 —— `lowPowerModeEnabled`。

**Objective-C**

```objective-c
if ([[NSProcessInfo processInfo] isLowPowerModeEnabled]) {
    // 当前用户启用低电量模式
} else {
    // 当前用户未启用低电量模式
}
```

**Swift**

```swift
if NSProcessInfo.processInfo().lowPowerModeEnabled {
    // 当前用户启用低电量模式
} else {
    // 当前用户未启用低电量模式
}
```

#### NSProcessInfoPowerStateDidChangeNotification

为了更好的响应电量模式的切换——**当电池充电到80%时将退出低电量模式**，Apple 为我们提供了一个全局的通知`NSProcessInfoPowerStateDidChangeNotification`。

**Objective-C**

```objective-c
[[NSNotificationCenter defaultCenter] addObserver:self
   selector: @selector(yourMethodName:)
   name: NSProcessInfoPowerStateDidChangeNotification
   object: nil];

- (void) yourMethodName:(NSNotification *)note {
  if ([[NSProcessInfo processInfo] isLowPowerModeEnabled]) {
    // 当前用户启用低电量模式
    // 在这里减少动画、降低帧频、停止位置更新、禁用同步和备份等。
  } else {
    // 当前用户未启用低电量模式
    // 在这里恢复禁止的操作
  }
}

```

**Swift**

```swift
NSNotificationCenter.defaultCenter().addObserver(
    self,
    selector: “yourMethodName:”,
    name: NSProcessInfoPowerStateDidChangeNotification,
    object: nil
)

func yourMethodName:(note:NSNotification) {  
    if(NSProcessInfo.processInfo().isLowPowerModeEnabled) {  
      // 当前用户启用低电量模式
      // 在这里减少动画、降低帧频、停止位置更新、禁用同步和备份等。 
    } else {  
      // 当前用户未启用低电量模式
      // 在这里恢复禁止的操作
    }  
}
```

#### 总结

通过遵守 **iOS 应用程序能效指南** 推荐的方式，为平台的整体能效和用户体验做出改变。

### 参考资料 辛苦移步了

[在 iPhone 上启用低电量模式将丢失 15 项功能](https://igamesnews.com/mobile/15-functions-you-will-lose-by-activating-low-power-mode-on-iphone/)

[iOS 应用程序能效指南](https://developer.apple.com/library/watchos/documentation/Performance/Conceptual/EnergyGuide-iOS/index.html)

[响应 iPhone 设备的低电量模式](https://developer.apple.com/library/archive/documentation/Performance/Conceptual/EnergyGuide-iOS/LowPowerMode.html#//apple_ref/doc/uid/TP40015243-CH31-SW1)

[WWDC 2015 Session 707 Achieving All-day Battery Life](https://developer.apple.com/videos/play/wwdc2015/707)

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)


3、[https://juejin.cn/post/7012541709561102367](https://juejin.cn/post/7012541709561102367 "写更好的 Swift 代码：技巧拾遗") -- 来自掘金：OldBirds


[@东坡肘子](https://www.fatbobman.com)：作者在文章中介绍了如何几个很实用的Swift使用技巧，包括：通过前缀避免命名冲突、快速交换值、@discardableresult、访问控制等，对日常的开发很有帮助。

4、[https://juejin.cn/post/7017605307593392159](https://juejin.cn/post/7017605307593392159 "Swift：where关键词使用") -- 来自掘金：season_zhu


[@东坡肘子](https://www.fatbobman.com)：本文介绍了where在Swift中的几个使用场景，除了应用于for循环外，还包括泛型约束、指明类型等。有助于更好的理解在不同上下文中的where用法。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### gitmoji

地址：https://gitmoji.js.org/

Gitmoji 是一个 GitHub 提交信息的 emoji 指南😎，致力于成为一个标准化的 emoji 备忘单📋，当你在在提交信息时，使用 emoji 来描述成了一种简单的方式来识别提交的目的和意图🍰，因为维护者只需要看一眼所使用的 emoji 就能明白🧐。由于有很多的 emoji，所以这里创建一份指南来让使用 emoji 变得轻松、易懂、一致🥳。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### SCADE

**地址**：https://www.scade.io/

**软件状态** 
- SCADE Community：免费
- SCADE Professional：$29 per month / user

**软件介绍**：
Native App Development with Swift for iOS and Android.
Cross Platform Native Development - Native Code, Controls and Use of all OS specific Functionality combined with the Power of Swift.


![SCADE](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/SCD_Auora1-1-1-1240x791.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
