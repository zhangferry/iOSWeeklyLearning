# iOS摸鱼周报 第二十期

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

本期主题：`包大小优化`

1、[今日头条 iOS 安装包大小优化—— 新阶段、新实践](https://www.infoq.cn/article/iowjwhbirqeobzf5m2o8) -- 来自InfoQ：字节跳动技术团队


在多个渠道多次推荐的老文章了，再次推荐还是希望能跟大家一块打开思路，尤其在二进制文件的控制上，目前还有很多比较深入的手段去优化，资源的优化可能并不是全部的手段。


2、[今日头条优化实践： iOS 包大小二进制优化，一行代码减少 60 MB 下载大小](https://www.infoq.cn/article/XUJL32hTDKYqAKz0hkMM) -- 来自InfoQ：字节跳动技术团队


上篇文章的姊妹篇，也是大家比较熟悉的文章了。总而言之段迁移技术效果很明显，但是段迁移会带来一些其他的问题，比如文中提到的日志解析问题。我们在实践过程中也遇到了各种各样的小问题，一些二进制分析工具会失效，需要针对段迁移的ipa做适配。


3、[基于mach-o+反汇编的无用类检测](https://www.jianshu.com/p/c41ad330e81c) -- 来自简书：皮拉夫大王


很少在周报中推荐自己的文章，尤其是自己2年前的老文章。推荐这篇文章的原因是我在文中列举了58各个业务线的包大小占比分析。从数据中可以看出我们经过多年包大小治理后，资源的优化空间并不大，只能从二进制文件的瘦身上入手。可能很多公司的APP也有同样的问题，就是资源瘦身已经没有太大的空间了，这时我们就应该从二进制层面寻找突破口。文中工具地址：[Github WBBlades](https://github.com/wuba/WBBlades)


4、[Flutter包大小治理上的探索与实践](https://tech.meituan.com/2020/09/18/flutter-in-meituan.html) -- 来自美团技术团队：艳东 宗文 会超


谈点新鲜的内容。作者首先对Flutter的包大小进行了细致的分析，并在双平台选择了不同的优化方案。在Android平台选择动态下发，而iOS平台则将部分非指令数据进行动态下发。通过修改Flutter的编译后端将data重定向输入到文件，从而实现了数据段与文本段的拆分。使用Flutter的团队可以关注下这个方案。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐

整理编辑：[CoderStar](https://juejin.cn/user/588993964541288/posts)
### Snipaste
**地址**： https://zh.snipaste.com/

**软件状态**： 普通版免费，专业版收费，有Mac、Windows两个版本

**软件介绍**

Snipaste 是一个简单但强大的截图工具，也可以让你将截图贴回到屏幕上！普通版的功能已经足够使用，笔者认为是最好用的截图软件了！（下图是官方图）
![Snipaste](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/N3QEb3VA.png)
### LSUnusedResources
**地址**： https://github.com/tinymind/LSUnusedResources

**软件状态**： 免费

**软件介绍**

一个 Mac 应用程序，用于在 Xcode 项目中查找未使用的图像和资源，可以辅助我们优化包体积大小。

![LSUnusedResources](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/LSUnusedResourcesExample.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
