# iOS摸鱼周报 第二十二期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> 

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)



## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`电量优化`


1、[iOS性能优化之耗电检测](https://www.diffit.cn/2020/09/03/EnergyDetection/) -- 来自：杂货铺

文章介绍了耗电量检测的三种方式：Energy impact、Energy Log、sysdiagnose。 每种方案详细介绍了检测步骤。在Energy Log中提到了“当前台三分钟或后台一分钟CPU线程连续占用80%以上就判定为耗电，同时记录耗电线程堆栈供分析”，这对我们日常分析有一定的帮助。

2、[Analyzing Your App’s Battery Use](https://developer.apple.com/documentation/xcode/analyzing-your-app-s-battery-use) -- 来自：Apple

苹果官方提供了一些性能监控的手段，通过Xcode Organizer可以查看24小时的性能数据，包括电量数据。

3、[iOS 性能优化：使用 MetricKit 2.0 收集数据](https://mp.weixin.qq.com/s/cbP0QlxVlr5oeTrf6yYfFw) -- 来自老司机周报：Jerry4me

既然提到了官方的方案就不得不提到MetricKit。本文介绍了什么是MetricKit，如何使用以及iOS 14之后的新的数据指标。另外需要注意的是MetricKit是iOS13之后才支持的，并且并不能搜集全部用户的数据，只有共享 iPhone 分析的用户数据才能被收集。

4、[iOS进阶--App功耗优化](http://www.cocoachina.com/articles/21428 "iOS进阶--App功耗优化") -- 来自cocoachina：yyuuzhu 

直观上耗电大户主要包括：CPU、设备唤醒、网络、图像、动画、视频、动作传感器、定位、蓝牙。测试工具：Energy Impact、Energy Log，更加具体的信息查看本文。

5、[iOS耗电量和性能优化的全新框架](https://punmy.cn/2019/06/16/wwdc_417_metrics.html "iOS耗电量和性能优化的全新框架") -- 来自博客：Punmy

在 Session 417 中，苹果推出了三项新的电量和性能监测工具，分别用于开发阶段、内测阶段、以及线上阶段。相信通过本文，你会对你的 App 接下去的耗电量和性能优化的方向，有更好的计划。

6、[耗电优化的几点建议](https://lizhaobomb.github.io/2020/03/02/iOS%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%9606%20-%20%E8%80%97%E7%94%B5%E4%BC%98%E5%8C%96/ "耗电优化的几点建议") -- 来自博客：Catalog

关于耗电优化的几点实操性的建议。

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
