# iOS 摸鱼周报 #64 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题



## 本周学习

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### 当设置 `UIImageView` 高亮时，会暂停当前的动画

#### 问题背景

项目通过配置 `UIImageView` 的 `animationImages` 实现 `loading` 动画。项目基于 `UICollectionView` 实现分页组件。当  `loading` 动画时，双击图片，动画会暂停。

#### 问题描述

通过 `hook``UIImageView` 的 `stopAnimating` 方法并添加断点，查看当动画停止时的调用栈，发现正在设置当前 `imageView` 为高亮。

这是因为当我们双击`UICollectionView` 时，`UICollectionView` 会高亮展示当前的 `CollectionViewCell`，此行为会将当前 `CollectionViewCell`上支持高亮展示的 `subview` 的显示状态成高亮。

 `UIImageView` 在设置高亮状态时，会先调用 `stopAnimating`。

#### 解决方案

禁止 `UICollectionView` 高亮行为, `UICollectionView` 的代理方法`shouldHighlightItemAt` 返回 `false`。

```swift
optional func collectionView(
    _ collectionView: UICollectionView,
    shouldHighlightItemAt indexPath: IndexPath
) -> Bool
```

### Xcode 14 编译包在 iOS 12.2 以下设备崩溃

由于项目支持 iOS 12.0 以上，最新版本测试时发现 iOS 12.1.4 的系统无法打开安装包，而 12.4 的设备可以正常打开。

Xcode 14 的编译包会多出一些系统库，你需要添加 `libswiftCoreGraphics.tbd` ，否则在 iOS 12.2 以下的系统找不到 `libswiftCoreGraphics.tbd`  而发生崩溃。

![](https://cdn.zhangferry.com/Images/add.png)

来源：[iOS小技能：Xcode14新特性(适配）](https://juejin.cn/post/7150842048944767006)

## 内容推荐

> 本期我们将推荐一些与实时活动和灵动岛有关的优秀内容

1、[在 iOS 16 中显示实时活动](https://swiftwithmajid.com/2022/09/21/displaying-live-activities-in-ios16/ "在 iOS 16 中显示实时活动") -- 来自：Majid

[@东坡肘子](https://www.fatbobman.com/)：实时活动小组件是 iOS 16 最突出的功能之一。iOS 16 允许我们在锁屏界面或 iPhone 14 Pro 的灵动岛区域显示来自应用程序持续活动的实时状态。本文将介绍如何使用新的 ActivityKit 框架为我们的应用程序构建实时活动小组件。

2、[掌握 SwiftUI 的灵动岛](https://swiftwithmajid.com/2022/09/28/mastering-dynamic-island-in-swiftui/ "掌握 SwiftUI 的灵动岛") -- 来自：Majid

[@东坡肘子](https://www.fatbobman.com/)：本文将介绍如何使用灵动岛功能在 iPhone 14 Pro 上显示应用程序中的实时活动，是上篇文章的延续。

3、[灵动岛 Dynamic Island 初探](https://kingnight.github.io/programming/2022/09/28/灵动岛Dynamic-Island初探.html "灵动岛 Dynamic Island 初探") -- 来自：Kingnight

[@东坡肘子](https://www.fatbobman.com/)：本篇文章将从软件开发角度，探索灵动岛的展现形式、功能限制、如何具体实现、适用场景等各方面的问题；帮助还不了解相关信息的开发者快速理解这一新的展现形式，并结合自身产品形态做出创新。

4、[为 iPhone 14 Pro 的灵动岛设计](https://uxdesign.cc/designing-for-iphone-14-pro-dynamic-island-90ea7f68b71 "为 iPhone 14 Pro 的灵动岛设计") -- 来自：Niels Boey

[@东坡肘子](https://www.fatbobman.com/)：作者是一个产品设计师，本文将从设计师的角度对灵动岛功能进行了介绍和讲解。

5、[实时活动（ Live Activity ）- 在锁定屏幕和灵动岛上显示应用程序的实时数据](https://juejin.cn/post/7144268555779850248 "实时活动（ Live Activity ）- 在锁定屏幕和灵动岛上显示应用程序的实时数据") -- 来自：Layer

[@东坡肘子](https://www.fatbobman.com/)：本文参考、翻译并实现了 Apple‘s documentation activitykit displaying live data with live activities 及 Updating and ending your Live Activity with remote push notifications 内容，并提供了范例代码。

6、[如何激活灵动岛中的像素](https://twitter.com/iphone15ultra/status/1580821164594585600 "如何激活灵动岛中的像素") -- 来自：iPhone 15 Ultra

[@东坡肘子](https://www.fatbobman.com/)：打开黑暗模式 -> 在后台播放一些音乐 -> 转到设置 -> 辅助功能 -> 显示与文本大小 -> 开启/关闭智能反转 -> 你将看到完整的💊。

7、[iOS灵动岛【电商商品秒杀】开发实践](https://juejin.cn/post/7153236337074634788 "iOS灵动岛【电商商品秒杀】开发实践") -- 来自掘金

[@邓利兵](https://github.com/erduoniba)：iOS灵动岛【电商商品秒杀】开发实践，详细讲解了灵动岛的基本概念、开发基本要素及细节。Demo中展示了主工程和灵动岛Widget的通讯方式及灵动岛Widget的布局方式。

## 摸一下鱼

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #63 | Apple 企业家培训营已开放申请](https://mp.weixin.qq.com/s/nAMshUG4AjWLAAHOFPVqXg)

[iOS 摸鱼周报 #62 |  Live Activity 上线 Beta 版 ](https://mp.weixin.qq.com/s/HySX4Yaf3Zxy8Wn-LyUO0A)

[iOS 摸鱼周报 #61 |  Developer 设计开发加速器](https://mp.weixin.qq.com/s/WfwqRhC-9-isUanv8ZnvMQ)

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
