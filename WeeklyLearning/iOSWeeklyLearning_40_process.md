# iOS摸鱼周报 第四十期

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

1、[iOS包依赖管理工具](https://juejin.cn/post/6932739864613879821 "iOS包依赖管理工具") -- 来自掘金：小小青叶

[@东坡肘子](https://www.fatbobman.com/)：本系列一共六篇文章，不仅从原理、使用、创建自定义库等方面，对 CocoaPods 和 Swift Package Manager 进行了介绍，并且对两种包管理工具进行了比较。

2、[CocoaPods Podspec 解析原理](http://chuquan.me/2022/01/03/podspec-analyze-principle/ "CocoaPods Podspec 解析原理") -- 来自楚权的世界：楚权

[@东坡肘子](https://www.fatbobman.com/)：在 CocoaPods 中，podspec 文件主要用于描述一个 pod 库的基本信息，包括：名称、版本、源、依赖等等。本文介绍了如何通过 DSL 方法将配置的属性保存在一个对象的哈希表中，通过构建一棵保存所有配置信息的树从而建立相互之间的依赖关系。

3、[关于 Swift Package Manager 的一些经验分享](https://juejin.cn/post/7007987863954391054 "关于 Swift Package Manager 的一些经验分享") -- 来自：字节跳动技术团队

[@东坡肘子](https://www.fatbobman.com/)：Swift Package Manager 是 Apple 为了弥补当前 iOS 开发中缺少官方组件库管理工具的产物。相较于其他组件管理控件，他的定义文件更加轻松易懂，使用起来也很 Magic，只需将源码放入对应的文件夹内，Xcode 就会自动生成工程文件，并生成编译目标产物所需要的相关配置。同时，SPM 与 Cocoapods 相互兼容，可以在特性上提供互补。本文除了介绍 Swift Package Manager 的现状、常见使用方法外，还阐述了作者对于 SPM 未来的一些思考。

4、[解决swift package manager fetch慢的问题](https://juejin.cn/post/7007987863954391054 "解决swift package manager fetch慢的问题") -- 来自简书：chocoford

[@东坡肘子](https://www.fatbobman.com/)：由于网络的某些限制，在 Xcode 中直接 fetch Github 上的 SPM 库并不容易。本文中给出了几种提高 fetch 成功率的解决方案。（编辑特别提示：Xcode 程序包中内置了终端、命令行工具等应用，任何在系统终端下的代理设定对其都不会产生作用。使用 SS + Proxifier 的方式可以实现让 Xcode 中的网络数据从指定代理通过）

5、[Swift Package Manager 添加资源文件](https://juejin.cn/post/6854573220784242702 "Swift Package Manager 添加资源文件") -- 来自掘金：moxacist

[@东坡肘子](https://www.fatbobman.com/)：从  swift-tool-version 5.3 版本开始，Swift Package Manager 提供了在包中添加资源文件的能力。本文是 WWDC 2020 —— 【Swift 软件包资源和本地化】 专题演讲的中文整理。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



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
