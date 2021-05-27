# iOS摸鱼周报 第十三期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 开发Tips




## 那些Bug


## 编程概念

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)




## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)


本期博客汇总的主题是`watchdog`

1、[iOS watchdog (看门狗机制)](https://www.jianshu.com/p/6cf4aeced795 "iOS watchdog (看门狗机制)") -- 来自简书：__Mr_Xie__


先来简单了解什么是watchdog。

2、[iOS App 后台任务的坑](http://www.cocoachina.com/articles/27303 "iOS App 后台任务的坑") -- 来自cocoachina ：米米狗


后台任务泄漏是导致触发watchdog常见情况之一，还有一种情况就是主线程卡死，文章中有介绍如何区分。


3、[Addressing Watchdog Terminations](https://developer.apple.com/documentation/xcode/addressing-watchdog-terminations "Addressing Watchdog Terminations")


苹果的官方文档。对我个人而言，了解scene-create和scene-update的含义在排查问题过程中起到了一定的作用。


4、[你的 App 在 iOS 13 上被卡死了吗](https://zhuanlan.zhihu.com/p/99232749 "你的 App 在 iOS 13 上被卡死了吗")


进入实践阶段，其实我们很少真的在主线程做大量耗时操作如网络请求等。触发watchdog往往是不经意的，甚至你不会怀疑你的代码有任何问题。这篇文章介绍的是58同城团队如何定位到剪切板造成的启动卡死。


5、[iOS 稳定性问题治理：卡死崩溃监控原理及最佳实践](https://juejin.cn/post/6937091641656721438 "iOS 稳定性问题治理：卡死崩溃监控原理及最佳实践")


这篇文章是字节跳动APM团队早些时候发表的，是业界少有的公开介绍卡死崩溃的原因的文章，具有很强的借鉴意义。我们在做启动卡死优化的过程中，文中提到的相关问题基本都有遇到，只不过在此之前并不知道什么原因以及如何解决。所以说如果你想做卡死治理，可以参考下这篇文章。

6、[面试过500+位候选人之后，想谈谈面试官视角的一些期待](https://mp.weixin.qq.com/s/kv-_oZObp7QRHeAbrkdfsA "面试过500+位候选人之后，想谈谈面试官视角的一些期待")


《iOS 稳定性问题治理：卡死崩溃监控原理及最佳实践》的作者在面试了500+候选人后写的文章，有需要的同学可以针对性的做些准备。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

## 工具推荐

整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### Application Name

**地址**：

**软件状态**：

**使用介绍**



## 联系我们

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

[摸鱼周报第六期](https://zhangferry.com/2021/03/14/iOSWeeklyLearning_6/)

[摸鱼周报第七期](https://zhangferry.com/2021/03/28/iOSWeeklyLearning_7/)

[摸鱼周报第八期](https://zhangferry.com/2021/04/11/iOSWeeklyLearning_8/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
