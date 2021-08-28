# iOS摸鱼周报 第二十五期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> 

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

### 如何清除 iOS APP 的启动屏幕缓存

整理编辑：[FBY展菲](https://github.com/fanbaoying)

每当我在我的 `iOS` 应用程序中修改了 `LaunchScreen.storyboad` 中的某些内容时，我都会遇到一个问题：

**系统会缓存启动图像，即使删除了该应用程序，它实际上也很难清除原来的缓存。**

有时我修改了 `LaunchScreen.storyboad`，删除应用程序并重新启动，它显示了新的 `LaunchScreen.storyboad`，但 `LaunchScreen.storyboad` 中引用的任何图片都不会显示，从而使启动屏显得不正常。

今天，我在应用程序的沙盒中进行了一些挖掘，发现该 `Library` 文件夹中有一个名为 `SplashBoard` 的文件夹，该文件夹是启动屏缓存的存储位置。

因此，要完全清除应用程序的启动屏幕缓存，您所需要做的就是在应用程序内部运行以下代码（已将该代码扩展到 `UIApplication` 的中）：

```swift
import UIKit

public extension  UIApplication {

    func clearLaunchScreenCache() {
        do {
            try FileManager.default.removeItem(atPath: NSHomeDirectory()+"/Library/SplashBoard")
        } catch {
            print("Failed to delete launch screen cache: \(error)")
        }
    }

}
```

在启动屏开发过程中，您可以将其放在应用程序初始化代码中，然后在不修改启动屏时将其禁用。

这个技巧在启动屏出问题时为我节省了很多时间，希望也能为您节省一些时间。

**使用介绍**

```swift
UIApplication.shared.clearLaunchScreenCache()
```

* 文章提到的缓存目录在沙盒下如下图所示：

![](https://user-images.githubusercontent.com/24238160/131212546-3ac9cf3c-cad5-48c5-913a-3e1408595e44.png)

* OC 代码,创建一个 `UIApplication` 的 `Category`

```objectivec
#import <UIKit/UIKit.h>

@interface UIApplication (LaunchScreen)
- (void)clearLaunchScreenCache;
@end
#import "UIApplication+LaunchScreen.h"

@implementation UIApplication (LaunchScreen)
- (void)clearLaunchScreenCache {
    NSError *error;
    [NSFileManager.defaultManager removeItemAtPath:[NSString stringWithFormat:@"%@/Library/SplashBoard",NSHomeDirectory()] error:&error];
    if (error) {
        NSLog(@"Failed to delete launch screen cache: %@",error);
    }
}
@end
```

OC使用方法

```objectivec
#import "UIApplication+LaunchScreen.h"

[UIApplication.sharedApplication clearLaunchScreenCache];
```

参考：[如何清除 iOS APP 的启动屏幕缓存](https://mp.weixin.qq.com/s/1esgRgu1iqFwB1Wv8-GlEQ)


## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[FBY展菲](https://github.com/fanbaoying)

本期主题：`Swift 泛型`

1、[Swift 进阶： 泛型](https://mp.weixin.qq.com/s/WOPbESx7YIAUes_1y3wyMw) -- 来自公众号：Swift社区

泛型是 Swift 最强大的特性之一，很多 Swift 标准库是基于泛型代码构建的。你可以创建一个容纳  Int 值的数组，或者容纳 String 值的数组，甚至容纳任何 Swift 可以创建的其他类型的数组。同样，你可以创建一个存储任何指定类型值的字典，而且类型没有限制。

2、[Swift 泛型解析](https://juejin.cn/post/7000916678150193159/ "Swift 泛型解析") -- 来自掘金：我是熊大

本文通俗易懂的解析了什么是泛型，泛型的应用场景，泛型和其他Swift特性摩擦出的火花，最后对泛型进行了总结。

3、[WWDC2018 - Swift 泛型 Swift Generics](https://juejin.cn/post/6844903623185399822/ "WWDC2018 - Swift 泛型 Swift Generics") -- 来自掘金：西野圭吾

本文回顾了 Swift 中对于泛型支持的历史变更，可以了解下泛型不同版本的历史以及特性。

4、[Swift 性能优化(2)——协议与泛型的实现](http://chuquan.me/2020/02/19/swift-performance-protocol-type-generic-type/ "Swift 性能优化(2)——协议与泛型的实现") -- 来自博客：楚权的世界

本文探讨了协议和泛型的底层实现原理，文中涉及到编译器对于 Swift 的性能优化，十分推荐阅读。

5、[Swift 泛型底层实现原理](http://chuquan.me/2020/04/20/implementing-swift-generic/ "Swift 泛型底层实现原理") -- 来自博客：楚权的世界


本文介绍了swift相关的底层原理，干货较多。例如VWT的作用、什么是Type Metadata、Metadata Pattern等等。如果有些概念不是很清楚的话可以阅读文章下面的参考文献。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Adobe Color Wheel

地址：https://color.adobe.com/zh/create/color-wheel

来自 Adobe 的调色盘网站，可以选择不同的色彩规则，例如：类比、分割辅色、三元色等等方案来生成配色，也可以通过导入照片来提取颜色，并且可以通过辅助工具例如对比度检查器来，确认文字和图案在底色上的预览情况。另外，你也可以通过 Adobe 的「探索」和「趋势」社区来学习如何搭配颜色，或者是寻找配色灵感。

### Awesome-tips

地址：https://awesome-tips.gitbook.io/ios/

来自知识小集整理的 iOS 开发 tip，已经整合成了 gitbook。虽然时间稍稍有点久了，但其中的文章都比较优质，在遇到的问题的时候可以翻阅一下，讲不定会有新的收获。

## 工具推荐

整理编辑：[CoderStar](http://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18#wechat_redirect)

# OhMyStar

**地址**：https://ohmystarapp.com/

**软件状态**：普通版免费，Pro版收费

**软件介绍**：

直接引用官方自己介绍的话吧
> The best way to organise your GitHub Stars. Beautiful and efficient way to manage, explore and share your Github Stars.

其中Pro版增加的功能是设备间同步，不过软件本身也支持数据的导入导出，大家根据自己的情况进行选择。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/mbp.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
