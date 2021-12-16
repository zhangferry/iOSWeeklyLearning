# iOS摸鱼周报 第三十五期

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



## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

1、[SwiftUI 视图的生命周期研究](https://www.fatbobman.com/posts/swiftUILifeCycle/ "SwiftUI 视图的生命周期研究") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：在 UIKit（AppKit）的世界中，通过框架提供的大量钩子（例如 viewDidLoad、viewWillLayoutSubviews 等），开发者可以将自己的意志注入视图控制器生命周期的各个节点之中，宛如神明。在 SwiftUI 中，系统收回了上述的权利，开发者基本丧失了对视图生命周期的掌控。不少 SwiftUI 开发者都碰到过视图生命周期的行为超出预期的状况（例如视图多次构造、onAppear 无从控制等）。本文将作者对 SwiftUI 视图、SwiftUI 视图生命周期的理解和研究做以介绍，供大家一起探讨。

2、[探究视图树](https://mp.weixin.qq.com/s/JMxJqCoho-LGJcLrNt9ibQ "探究视图树") -- 来自：Javier

[@东坡肘子](https://www.fatbobman.com/)：大多 SwiftUI 的开发者都已经熟练掌握了如何从父视图向子视图传递数据的方法，但如何获取子视图的状态和变化对很多人仍然比较陌生。swiftui-lab 的 Javier 写了三篇文章详细介绍了如何通过 PreferenceKey、AnchorPreferences 等方式向上传递数据的手段。链接中提供的是 Swift 花园的中文译本。

3、[SwiftUI 中的 Text 插值和本地化](https://onevcat.com/2021/03/swiftui-text-1/ "SwiftUI 中的 Text 插值和本地化") -- 来自：onevcat

[@东坡肘子](https://www.fatbobman.com/)：Text 是 SwiftUI 中最简单和最常见的 View 了，相较 String，Text 提供了更加丰富的差值和本地化功能。本文不仅介绍了 Text 中关于差值和本地化的一些特色功能，并讲解了在Text中创建自定义差值的方法。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 软件随想录

地址：https://book.douban.com/subject/4163938/

Joel Spolsky 的 Blog 纸质版文集，中文版由阮一峰翻译。作者 Joel Spolsky 毕业于耶鲁大学，曾任微软公司 Excel 开发小组项目经理，现在自己创业做 CEO，也是 Stack Overflow 的合伙人。他在书中以诙谐幽默的笔触将自己在软件行业的亲身感悟娓娓道来，其中包含关于软件、人才、创业和管理的很多看法，需要提醒读者的是本书的大部分内容都写于 2004 年底之后。我这边节选一些有意思的观点供没看过的读者过过瘾:

> 1. 从数量上来说，优秀的人才很少，而且从不出现在招聘市场上。
> 2. 我从来没有见过哪个能用 Scheme 语言、Haskell 语言、C 语言中的指针函数编程的人，竟然不能在两天里面学会 Java，并且写出的 Java 程序质量竟然不能胜过那些有 5 年 Java 编程经验的人士。
> 3. 看东西的时候，你的视力只是在你的视野中很小一块区域是高分辨率的，而且视野中央还有相当大的一个盲点。但是，你依然想当然的认定你能够超清晰的看清视野中的每一个角落。
> 4. 别担心所有工作都被印度人抢走。😁

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

推荐人：[iOSleep](https://github.com/iOSleep)

### Dropshelf

**地址**：https://pilotmoon.com/dropshelf/

**软件状态**：之前付费但是目前下架了，可以使用上面链接免费使用。

**软件介绍**：

Dropshelf是一款Mac OS下的拖拽效率应用。它提供了一个可以吸附在屏幕边缘的Dock，你可以拖拽任何东西「图片、文件、文字、链接...」暂存到Dock中，方便你在其他App中来使用。
![Dropshelf](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/9964d0eee2c48e3d24ba63c09e25b10c_720w.jpeg)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
