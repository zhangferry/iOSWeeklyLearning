# iOS摸鱼周报 第十九期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

### UICollectionView 的scrollDirection 对 minimumLineSpacing 和 minimumInteritemSpacing 影响

滚动方向垂直方向时候原理图

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210716180322.png)

滚动方向水平方向时候原理图

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/3162666d7fa108da73e6549aea9154cf.png)

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)



## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`卡顿优化`
[iOS卡顿监测方案总结](https://juejin.cn/post/6844903944867545096 "iOS卡顿监测方案总结")


文章总结了业界的很多卡顿监控技术。包括：FPS、runloop、子线程Ping、CPU占用率监测。文章中附带了作者参考和收集到的原文链接，以及部分相关上下游技术的文章。如果您想要做卡顿监控，阅读本文可以节省不少时间和精力。


[iOS 渲染原理解析](https://mp.weixin.qq.com/s/6ckRnyAALbCsXfZu56kTDw "iOS 渲染原理解析")


文章细致的介绍了图像渲染的流程。包括一些细小有趣的知识点，比如CALayer的contents保存了 bitmap信息等。文中当然少不了对离屏渲染的介绍，包括离屏渲染的场景、离屏渲染的原因以及如何避免离屏渲染。文后附有小题目，可以让大家带着问题回顾文章，加深对知识的理解。


[UIView 动画降帧探究](https://mp.weixin.qq.com/s/EcVrrT1M4mI4f4d2b3qV0Q  "UIView 动画降帧探究")


本文首先介绍为了降帧的目的：降低GPU的使用率，并介绍了为什么动画渲染对GPU有较大的影响。正文中主要介绍了降帧的方案：UIView animation 指定 UIViewAnimationOptionPreferredFramesPerSecond30进行降帧、CADisplayLink逐帧动画降帧。



## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)



## 联系我们

[iOS摸鱼周报 第十一期](https://zhangferry.com/2021/05/16/iOSWeeklyLearning_11/)

[iOS摸鱼周报 第十二期](https://zhangferry.com/2021/05/22/iOSWeeklyLearning_12/)

[iOS摸鱼周报 第十三期](https://zhangferry.com/2021/05/30/iOSWeeklyLearning_13/)

[iOS摸鱼周报 第十四期](https://zhangferry.com/2021/06/06/iOSWeeklyLearning_14/)

[iOS摸鱼周报 第十五期](https://zhangferry.com/2021/06/14/iOSWeeklyLearning_15/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
