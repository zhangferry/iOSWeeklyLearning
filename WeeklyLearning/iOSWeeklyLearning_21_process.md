# iOS摸鱼周报 第二十一期

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

内存优化可以从以下几点入手：

1. 工具分析，可以利用Xcode自带的instruments中的leak、allocation，也可以利用MLeaksFinder等开源工具。找到内存泄漏、内存激增、内存不释放的位置。
2. 利用mmap，一种低内存的首选方案
3. 图片优化，经过第一步之后，一定会发现内存激增极有可能与图片相关


1、[iOS的文件内存映射——mmap](https://www.jianshu.com/p/516e7ff6f251 "iOS的文件内存映射——mmap") --来自简书：落影loyinglin

mmap一定是低内存方案的首选。文件映射，用于将文件或设备映射到虚拟地址空间中，以使用户可以像操作内存地址一样操作文件或设备，作者介绍了mmap原理并根据官方代码，整理了一个简单的Demo，有兴趣的人还可以阅读下微信的开源仓库：MMKV。

2、[iOS图片加载速度极限优化—FastImageCache解析](http://blog.cnbang.net/tech/2578/ "iOS图片加载速度极限优化—FastImageCache解析") -- 来自博客：bang

在app中，图片在内存中占用比例相对较大，有没有办法优化缓存一些图片到磁盘中呢？答案是：FastImageCache。FastImageCache是Path团队开发的一个开源库，用于提升图片的加载和渲染速度，让基于图片的列表滑动起来更顺畅，来看看它是怎么做的。

3、[Instruments学习之Allocations](https://www.jianshu.com/p/b617f16acb7f "Instruments学习之Allocations") -- 来自简书：Thebloodelves

详细介绍Allocations的使用，为你分析app内存助力。


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
