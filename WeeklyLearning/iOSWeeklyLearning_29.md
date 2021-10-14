# iOS摸鱼周报 第二十九期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * Tips：关于低电量模式的一些介绍。
> * 面试模块：Objective-C 的消息机制（下）。
> * 优秀博客：整理了几篇 Swift Tips 的文章。
> * 学习资料：Gitmoji：一个 GitHub 提交信息的 emoji 指南😎。
> * 开发工具：能够使用 Swift 开发安卓应用的工具：SCADE；可视化解析 `.ndjson` 文件的工具：Privacy-Insight。

## 本期话题

[@zhangferry](https://zhangferry.com)：本期访谈内容独立成篇了，大家可以查看本期公众号推送的次条。或者访问这个链接：

本期摸鱼周报迎来一位新伙伴：东坡肘子。肘子之前因为身体原因修养过一段时间，也因为身体的原因需要做健康记录，但并没有找到满意的记录方式，于是决定自己开发，由此结缘 iOS 做起了独立开发。之后我们还会对他进行一次访谈，带大家了解他的更多故事，你也可以关注他的博客：*肘子的 Swift 记事本 https://www.fatbobman.com/*。

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### 低电量模式

从 iOS 9 开始，Apple 为 iPhone 添加了低电量模式（**Low Power Mode**）。用户可以在 **设置 -> 电池** 启用低电量模式。在低电量模式下，iOS 通过制定某些节能措施来延长电池寿命，包括但不限于以下措施：

* 降低 CPU 和 GPU 性能，降低屏幕刷新率
* 包括联网在内的主动或后台活动都将被暂停
* 降低屏幕亮度
* 减少设备的自动锁定时间
* 邮件无法自动获取，陀螺仪及指南针等动态效果将被减弱，动态屏保将会失效
* 对于支持 5G 的 iPhone 设备来说，其 5G 能力将被限制，除非你在观看流媒体

上述节能措施是否会影响到你的应用程序，如果有的话，你可能需要针对低电量模式来适当采取某些措施。

#### lowPowerModeEnabled

我们可以通过 **NSProcessInfo** 来获取我们想要的进程信息。这个**线程安全**的单例类可以为开发人员提供与当前进程相关的各种信息。

一个值得注意的点是，NSProcessInfo 将尝试将环境变量和命令行参数解释为 Unicode，以 UTF-8 字符串返回。如果该进程无法成功转换为 Unicode 或随后的 C 字符串转换失败的话 —— 该进程将被**忽略**。

当然，我们还是需要关注于低电量模式的标志，一个表示设备是否启用了低电量模式的布尔值 —— `lowPowerModeEnabled`。

```swift
if NSProcessInfo.processInfo().lowPowerModeEnabled {
    // 当前用户启用低电量模式
} else {
    // 当前用户未启用低电量模式
}
```

#### NSProcessInfoPowerStateDidChangeNotification

为了更好的响应电量模式的切换——**当电池充电到 80% 时将退出低电量模式**，Apple 为我们提供了一个全局的通知`NSProcessInfoPowerStateDidChangeNotification`。

```swift
NSNotificationCenter.defaultCenter().addObserver(
    self,
    selector: "yourMethodName:",
    name: NSProcessInfoPowerStateDidChangeNotification,
    object: nil
)

func yourMethodName:(note:NSNotification) {  
    if (NSProcessInfo.processInfo().isLowPowerModeEnabled) {  
      // 当前用户启用低电量模式
      // 在这里减少动画、降低帧频、停止位置更新、禁用同步和备份等
    } else {  
      // 当前用户未启用低电量模式
      // 在这里恢复被禁止的操作
    }  
}
```

#### 总结

通过遵守 **iOS 应用程序能效指南** 推荐的方式，为平台的整体能效和用户体验做出改变。

#### 参考

* [在 iPhone 上启用低电量模式将丢失 15 项功能](https://igamesnews.com/mobile/15-functions-you-will-lose-by-activating-low-power-mode-on-iphone/ "在 iPhone 上启用低电量模式将丢失 15 项功能" )
* [iOS 应用程序能效指南](https://developer.apple.com/library/watchos/documentation/Performance/Conceptual/EnergyGuide-iOS/index.html "iOS 应用程序能效指南")
* [响应 iPhone 设备的低电量模式](https://developer.apple.com/library/archive/documentation/Performance/Conceptual/EnergyGuide-iOS/LowPowerMode.html#//apple_ref/doc/uid/TP40015243-CH31-SW1 "响应 iPhone 设备的低电量模式" )
* [WWDC 2015 Session 707 Achieving All-day Battery Life](https://developer.apple.com/videos/play/wwdc2015/707 "WWDC 2015 Session 707 Achieving All-day Battery Life")

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

本期面试解析讲解的知识点是 Objective-C 的消息机制（下）。在上一期摸鱼周报中我们讲解了 objc_msgSend 执行流程的第一大阶段 `消息发送`，那么这一期我们就来聊聊后两大阶段 `动态方法解析` 与 `消息转发`。

**动态方法解析**

如果 `消息发送` 阶段未能处理未知消息，那么就会进行一次 `动态方法解析`。我们可以在该阶段通过动态添加方法实现，来处理未知消息。`动态方法解析` 后，会再次进入 `消息发送` 阶段，从 “去 receiverClass 的 method cache 中查找 IMP” 这一步开始执行。

具体来说，在该阶段，Runtime 会根据 receiverClass 的类型是 class/meta-class 来调用以下方法：

```objectivec
+ (BOOL)resolveInstanceMethod:(SEL)sel;
+ (BOOL)resolveClassMethod:(SEL)sel;
```

我们可以重写以上方法，并通过 `class_addMethod` 函数来动态添加方法实现。需要注意的一点是，实例方法存储在类对象中，类方法存储在元类对象中，因此这里要注意传参。

```c
BOOL class_addMethod(Class cls, SEL name, IMP imp, const char *types)
```

如果我们在该阶段正确地处理了未知消息，那么再次进入到 `消息发送` 阶段肯定能找到 IMP 并调用，否则将进入 `消息转发` 阶段。

**消息转发**

`消息转发` 又分为 Fast 和 Normal 两个阶段，顾名思义 Fast 更快。

1. Fast：找一个备用接收者，尝试将未知消息转发给备用接收者去处理。

具体来说，就是给 receiver 发送一条如下消息，注意有类方法和实例方法之分。

```objectivec
+/- (id)forwordingTargetForSelector:(SEL)selector;
```

如果我们重写了以上方法，并正确返回了一个 != receiver 的对象（备用接收者），那么 Runtime 就会通过 objc_msgSend 给备用接收者发送当前的未知消息，开启新的消息执行流程。

如果该阶段还是没能处理未知消息，就进入 Normal。需要注意，在 Fast 阶段无法修改未知消息的内容，如果需要，请在 Normal 阶段去处理。

2. Normal：启动完整的消息转发，将消息有关的全部细节都封装到一个 NSInvocation 实例中，再给接收者最后一次机会去处理未知消息。

具体来说，Runtime 会先通过调用以下方法来获取适合未知消息的方法签名。

```objectivec
+/- (NSMethodSignature *)methodSignatureForSelector:(SEL)aSelector;
```

然后根据这个方法签名，创建一个封装了未知消息的全部内容（target、selector、arguments）的 NSInvocation 实例，然后调用以下方法并将该 NSInvocation 实例作为参数传入。

```objectivec
+/- (void)forwardInvocation:(NSInvocation *)invocation;
```

我们可以重写以上方法来处理未知消息。在 `forwardInvocation:` 方法中，我们可以直接将未知消息转发给其它对象（代价太大，不如在 Fast 处理），或者改变未知消息的内容再转发给其它对象，甚至可以定义任何逻辑。

如果到了 Normal 还是没能处理未知消息，如果是没有返回方法签名，那么将调用 `doesNotRecognizeSelector:`；如果是没有重写 `forwardInvocation:`，将调用 NSObject 的 `forwardInvocation:` 的默认实现，而该方法的默认实现也是调用 `doesNotRecognizeSelector:`，表明未知消息最终未能得到处理，以 Crash 程序结束 objc_msgSend 的全部流程。

**一些注意点**

* 重写以上方法时，不应由本类处理的未知消息，应该调用父类的实现，这样继承体系中的每个类都有机会处理未知消息，直至 NSObject。
* 以上几个阶段均有机会处理消息，但处理消息的时间越早，性能就越高。
  - 最好在 `动态方法解析` 阶段就处理完，这样 Runtime 就可以将此方法缓存，稍后这个对象再接收到同一消息时就无须再启动 `动态方法解析` 与 `消息转发` 流程。
  - 如果在 `消息转发` 阶段只是单纯想将消息转发给备用接收者，那么最好在 Fast 阶段就完成。否则还得创建并处理 NSInvocation 实例。
* `respondsToSelector:`  会触发 `动态方法解析`，但不会触发 `消息转发`。


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://github.com/Tliens)、[东坡肘子](https://www.fatbobman.com)

1、[【iOS】Swift Tips - （一）](https://juejin.cn/post/6973623744119963679 "【iOS】Swift Tips - （一）") -- 来自掘金：Layer

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：文章是作者的学习笔记，作者将 objccn.io/ 的内容整理出来，一共 6 篇，适合在地铁上阅读。在这篇文章中主要介绍了柯里化、多元组、操作符等写法和用途。


2、[十个技巧让你成为更加优秀的 Swift 工程师](https://zhuanlan.zhihu.com/p/43119391 "十个技巧让你成为更加优秀的 Swift 工程师") -- 来自知乎：Summer

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：学习 Swift 不光要能写 Swift 代码，更要优雅地使用 Swift，这也是本期博客主题的目的。这篇文章介绍了巧用扩展、泛型、计算属性等优化代码，在初学者看来是比较有意思的。

3、[写更好的 Swift 代码：技巧拾遗](https://juejin.cn/post/7012541709561102367 "写更好的 Swift 代码：技巧拾遗") -- 来自掘金：OldBirds

[@东坡肘子](https://www.fatbobman.com)：作者在文章中介绍了几个很实用的 Swift 使用技巧，包括：通过前缀避免命名冲突、快速交换值、@discardableresult、访问控制等，对日常的开发很有帮助。

4、[Swift：where关键词使用](https://juejin.cn/post/7017605307593392159 "Swift：where关键词使用") -- 来自掘金：season_zhu

[@东坡肘子](https://www.fatbobman.com)：本文介绍了 where 在 Swift 中的几个使用场景，除了应用于 for 循环外，还包括泛型约束、指明类型等。有助于更好的理解在不同上下文中的 where 用法。

5、[Swift - 使用Color Literal实现代码中颜色的智能提示（Xcode自带功能）](https://www.hangge.com/blog/cache/detail_1902.html "Swift - 使用Color Literal实现代码中颜色的智能提示（Xcode自带功能）") -- 来自航歌

[@我是熊大](https://github.com/Tliens)：Color Literal 让颜色赋值可视化。

6、[【译】使用Swift自定义运算符重载](https://juejin.cn/post/6844903926232252424 "【译】使用Swift自定义运算符重载") -- 来自掘金：shankss

[@我是熊大](https://github.com/Tliens)：有没有想过 “+”，“-”，“??” 底层是怎么实现的？想不想自己也实现一个特有的运算符，如：“-->”，这篇文章带你一起探究。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### gitmoji

地址：https://gitmoji.js.org/

gitmoji 是一个 GitHub 提交信息的 emoji 指南😎，致力于成为一个标准化的 emoji 备忘单📋，当你在提交信息时，使用 emoji 来描述成了一种简单的方式来识别提交的目的和意图🍰，因为维护者只需要看一眼所使用的 emoji 就能明白🧐。由于有很多的 emoji，所以这里创建了一份指南来让使用 emoji 变得轻松、易懂、一致🥳。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18) 、[zhangferry](zhangferry.com)

### SCADE

**地址**：https://www.scade.io/

**软件状态** 
- SCADE Community：免费
- SCADE Professional：$29 per month / user

**软件介绍**：

利用 `SCADE` 我们可以使用 Swift 语言进行跨端原生开发。其描述特点如下：
- 跨平台：使用相同的源代码为 iOS 和 Android 开发
- 原生功能：不受限制地使用所有 iOS 和 Android 功能
- 无与伦比的速度：Swift 被编译为本机二进制代码以获得无与伦比的应用程序性能
- Swift 框架：在 iOS 和 Android 上使用流行的 Swift 框架，如 Swift Foundation，无需更改代码
- ...

![SCADE](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/SCD_Auora1-1-1-1240x791.png)

### Privacy-Insight

**地址**：https://github.com/Co2333/Privacy-Insight/releases

**软件状态** ：免费，开源

**软件介绍**：

解析 iOS 15 下格式为 `.ndjson` 的系统隐私报告，用 SwiftUI 写成。

隐私日志的生成为设置 -> 隐私 -> 打开记录 App 活动，等待一段时间之后点击下面的存储 App 活动按钮，即可收集这一段时间的隐私日志。存储会生成一个 `.ndjson` 格式的文件，导出使用 Privacy-Insight 打开即可查看。

以下为我使用 1 天的隐私请求记录：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/4301634041484_.pic_hd.jpg)

微信和今日头条的隐私权限获取频率均非常高，我是肯定没有那么频繁通过微信访问相册的。对于微信频繁获取相册权限的问题最近也在热议，希望不仅是微信，各个主流 App 都应该对于用户隐私问题予以重视。

作为使用者相对有效的保护隐私的方案是，关闭对应 App 的「后台刷新」，非必要情况下关闭蓝牙、定位等权限，并将相册调用权限改为「选中的照片」。

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第二十八期](https://mp.weixin.qq.com/s/dKOkF_P5JvQnDLq09DOzaQ)

[iOS摸鱼周报 第二十七期](https://mp.weixin.qq.com/s/WvctY6OG1joJez2g6owroA)

[iOS摸鱼周报 第二十六期](https://mp.weixin.qq.com/s/PnUZLoyKr8i_smi0H-pQgQ)

[iOS摸鱼周报 第二十五期](https://mp.weixin.qq.com/s/LLwiEmezRkXHVk66A6GDlQ)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
