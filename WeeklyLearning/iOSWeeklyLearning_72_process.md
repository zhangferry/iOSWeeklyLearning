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

Xcode 14 的编译包会多出一些系统库，你需要添加 `libswiftCoreGraphics.tbd` ，否则在 iOS12.2 以下的系统找不到 `libswiftCoreGraphics.tbd`  而发生崩溃。

来源：[iOS小技能：Xcode14新特性(适配）](https://juejin.cn/post/7150842048944767006)

## 内容推荐

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)


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
