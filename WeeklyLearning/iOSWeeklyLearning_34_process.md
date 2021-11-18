# iOS摸鱼周报 第三十四期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：
> * Tips：混编｜NS_SWIFT_NAME。
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)



### 混编｜NS_SWIFT_NAME

`NS_SWIFT_NAME` 宏用于在混编时为 Swift 重命名 Objective-C API，它可用在类、协议、枚举、属性、方法或函数、类型别名等等之中。通过 Apple 举的一些例子，我们可以学习到它的一些应用场景：

* 重命名与 Swift 风格不符的 API，使其在 Swift 中有合适的名称
* 重命名与类 A 相关联的类 B 或者枚举 C，使其作为内部类或枚举附属于类 A

* 重命名 “命名去掉完整前缀后以数字开头的” 枚举的 case，改善所有 case 导入到 Swift 中的命名
* 重命名 “命名不满足自动转换为构造器导入到 Swift 中的约定的” 工厂方法，使其作为构造器导入到 Swift 中
* 在处理全局常量、变量，特别是在处理全局函数时，它的能力更加强大，能够极大程度地改变 API。比如可以将 `全局函数` 转变为 `静态方法`，或是 `实例⽅法`，甚至是 `实例属性`。如果你在 Objective-C 和 Swift 里都用过 Core Graphics 的话，你会深有体会。Apple 称其把 `NS_SWIFT_NAME` 用在了数百个全局函数上，将它们转换为方法、属性和构造器，以更加方便地在 Swift 中使用。

你可以在 [iOS 混编｜为 Swift 重命名 Objective-C API](https://juejin.cn/post/7022302122867687454#heading-7) 中查看完整示例。

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

1、[Alamofire的基本用法](https://juejin.cn/post/6875140053635432462 "Alamofire 的使用 - 基本用法") -- 来自掘金：Lebron

[@我是熊大](https://github.com/Tliens)：Alamofire是AFNetWorking原作者写的，Swift版本相比AFN更加完善，本文介绍了Alamofire基本用法，很全面，适合精读；作者还有一篇[高级用法](https://juejin.cn/post/6875140780680282125)，欢迎阅读。

2、[Kingfisher源码解析](https://juejin.cn/post/6844904015738699790 "Kingfisher源码解析") -- 来自掘金：李坤

[@我是熊大](https://github.com/Tliens)：Kingfisher对标OC中的SDWebImage，作者是大名鼎鼎的王巍，本文是Kingfisher源码解析系列的总结，建议阅读。

3、[iOS SnapKit架构之道](https://rimson.top/2019/09/04/ios-snapkit-1/ "iOS SnapKit架构之道") -- 来自博客：Rimson

[@我是熊大](https://github.com/Tliens)：SnapKit作为在Swift中的页面布局的地位，相当于OC中的Masonry，使用起来几乎一模一样，本文作者详细梳理了Snapkit布局的过程和原理。

4、[第三方图表库Charts使用详解](https://www.hangge.com/blog/cache/detail_2116.html "第三方图表库Charts使用详解")-- 来自航歌：hangge

[@东坡肘子](https://www.fatbobman.com/)：Charts 是一个功能强大的图表框架，使用 Swift 编写。是对 Android 上大名鼎鼎的图表库 MPAndroidChart 在苹果生态上的移植。hangge通过大量的范例代码对 Charts 的使用进行了相近地说明。

5、[访问 SwiftUI 内部的 UIKit 组件](https://mp.weixin.qq.com/s/xYKGs3FkrlI_9pq1cdnC5Q "访问 SwiftUI 内部的 UIKit 组件")-- 来自 Swift花园：猫克杯

[@东坡肘子](https://www.fatbobman.com/)：抛开 SwiftUI 尚不完备的工具不说，SwiftUI 的确因其构建 UI 的便捷性给开发者带来了兴奋。有一个令人欣慰的事实是，许多 SwiftUI 组件实际上是基于 UIKit 构建的。本文将带你探索一个令人惊讶的 SwiftUI 库，它叫 Introspect 。利用它，开发者能够访问 SwiftUI 组件底层的 UIKit 视图。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 棒棒彬·技术参考周刊

地址：https://www.yuque.com/binboy/increment-magzine

这是一份由 [Binboy👻棒棒彬](https://www.yuque.com/binboy) 在语雀上梳理总结的技术参考周刊。这份周刊是作者学习与生活的沉淀和思考，既有广度，也有深度，还有态度。就像其发刊词的标题：「与技术世界保持链接」，在周刊中你可以看到作者学习技术的过程和经验，也能看到科技与生活的一些新鲜事，这里可能有你正在关注的，亦或者是从来没听说过的技术信息，这些信息既是作者与他自己「第二大脑」的链接，也是作者与读者交流的媒介，同时推动着作者与读者一起前进。这里改编引用一段[发刊词](https://www.yuque.com/binboy/increment-magzine/sno2ef)中的一段话来抛砖引玉 ：

> 做技术，追求深度无可厚非，只是无需厚此薄彼，我个人而言倾向于「修学储能，先博后渊」的。技术世界的开源、互联网的开放更是给了见多识广一片良好的土壤，我们可以了解了技术、工具现状，将其充分地应用、解决现实世界中的普通问题，并在过程中不断完善。当真正遇到边界时，再结合对已有技术和工具的融会贯通去创造真正的新技术、新工具，也不迟。
>
> *朝一个方向看得再远，你也未必能看到新方向*
>
> *———— 修学储能，先博后渊*

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
