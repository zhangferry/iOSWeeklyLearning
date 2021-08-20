# iOS摸鱼周报 第二十四期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> 

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)



## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)、[FBY展菲](https://github.com/fanbaoying)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

**为什么圆角和裁剪后 iOS 绘制会触发离屏渲染？**

默认情况下每个视图都是完全独立绘制渲染的。
而当某个父视图设置了圆角和裁剪并且又有子视图时，父视图只会对自身进行裁剪绘制和渲染。

当子视图绘制时就要考虑被父视图裁剪部分的绘制渲染处理，因此需要反复递归回溯和拷贝父视图的渲染上下文和裁剪信息，再和子视图做合并处理，以便完成最终的裁剪效果。这样势必产生大量的时间和内存的开销。

解决的方法是当父视图被裁剪和有圆角并且有子视图时，就单独的开辟一块绘制上下文，把自身和所有子视图的内容都统一绘制在这个上下文中，这样子视图也不需要再单独绘制了，所有裁剪都会统一处理。当父视图绘制完成时再将开辟的缓冲上下文拷贝到屏幕上下文中去。这个过程就是离屏渲染！！

所以离屏渲染其实和我们先将内容绘制在位图内存上下文然后再统一拷贝到屏幕上下文中的双缓存技术是非常相似的。使用离屏渲染主要因为iOS内部的视图独立绘制技术所导致的一些缺陷而不得不才用的技术。


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)




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
