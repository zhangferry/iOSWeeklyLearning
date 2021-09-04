# iOS摸鱼周报 第二十六期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：
> * Tips：
> * 面试模块：本期解析 KVO 的实现原理。
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：

1、简单介绍下自己吧

> 大家好，我是熊大，野生iOS开发者，目前正在做一款海外社交App，在团队中主要负责 iOS 的架构设计以及性能优化。

2、你有多款独立开发的应用，能简单介绍下当时独立开发应用的初衷和现状吗？

> 独立开发过两个产品《今日计划》、《imi我的小家》。

> 当时做独立开发的目的有两个：一个是自己有些想法想要实现出来，二是希望能有睡后收入；后来发现独立开发最首要的问题不是时间，而是运营和验证；如何找到产品定位人群，如何ASO如何优化，关键词如何填写，产品留存怎样才是及格？这些都是我们独立开发者，从未遇到的挑战，也正因此，我做了个公众号[《独立开发者基地》](https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=Mzg4OTU1Njk1MQ==&scene=124#wechat_redirect)，分享独立开发遇到的问题。

3、在你看来要做独立开发需要具备哪些重要技能（可以分技术和非技术）

> 以下5个方面可能是我们需要的：

> 1、具备产品思维，能编写需求文档，分析产品数据，摸索产品方向
> 
> 2、具备使用Sketch、Figma、蓝湖的能力
> 
> 3、运营推广能力，如何让app能被更多的人知道，如何召回用户
> 
> 4、具备iOS、Android、小程序等一个或多个的开发能力
> 
> 5、后端开发能力，其实这个前期可以使用第三方代替

> 最关键的是执行力和创造力，如果你有想法，那就不要等待。

4、你的工作和独立应用多涉及音视频技能，能说下音视频开发和普通应用开发有什么区别吗？如果想往这个方面学习，需要注意和关注哪些东西。

> 在我的工作中，音视频开发主要涉及到AVFoundation、FFmpeg、OpenGL ES、MetalKit等框架。

> 音视频开发入门会更难一些，需要有图形图像学的基础知识；有时需要编写C\C++代码，很多第三方的音视频库都是C\C++写的，比如常用的libjpeg-turbo、lame；同时要熟悉CMake工具进行编译等。

> 赠送给大家一个我写的专栏：[《GPUImage By Metal》](https://xiaozhuanlan.com/GPUImage/present/42a8fba462217d3717c54d707db55ae7b49d86ce)

> 推荐学习路线:
> 
> 1、数字图像的基本知识
> 
> 2、开源库 GPUImage，AVFoundation + OpenGL ES,2016年时，很多第三方SDK图像处理框架都是基于这个开发的。
> 
> 3、开源库 GPUImage3，这是AVFoundation + Metal。
> 
> 4、李明杰老师今年有一个FFmpeg的课程。

5、老问题了，如何保持学习的热情，能否分享一些你的学习方法

> 保持热情的最好办法就是热爱或追求。

> 1、学习时，陌生的东西不要太多，会打消积极性。
> 
> 2、如果遇到几天都无法理解的东西，放一放，发酵几个月后再看。
> 
> 3、要有目标和实践方案

6、有什么需要借助于摸鱼周报宣传的（公司内推或者个人产品宣传）

> 1、希望大家多多关注 SpeedySwift 开源项目：https://github.com/Tliens/SpeedySwift ，觉得 OK 的话给我个 star 鼓励一下。

> 2、北京连趣科技，寻找一起并肩作战的小伙伴，各个岗位都有需求，简历可以投递到 tliens.jp@gmail.com，我的微信：bear0000001。

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)



## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

本期解析 KVO 的实现原理。

Apple 使用了 isa-swizzling 方案来实现 KVO。

**注册：**

当我们调用 `addObserver:forKeyPath:options:context:` 方法，为 **被观察对象** a 添加 KVO 监听时，系统会在运行时动态创建 a 对象所属类 A 的子类 `NSKVONotifying_A`，并且让 a 对象的 isa 指向这个子类，同时重写父类 A 的 **被观察属性** 的 setter 方法来达到可以通知所有 **观察者对象** 的目的。

这个子类的 isa 指针指向它自己的 meta-class 对象，而不是原类的 meta-class 对象。

重写的 setter 方法的 SEL 对应的 IMP 为 Foundation 中的 `_NSSetXXXValueAndNotify` 函数（XXX 为 Key 的数据类型）。因此，当 **被观察对象** 的属性发生改变时，会调用 _NSSetXXXValueAndNotify 函数，这个函数中会调用：

* `willChangeValueForKey:` 方法
*  父类 A 的 setter 方法
*  `didChangeValueForKey:` 方法

**监听：**

而 willChangeValueForKey: 和 didChangeValueForKey: 方法内部会触发 **观察者对象** 的监听方法：`observeValueForKeyPath:ofObject:change:context:`，以此完成 KVO 的监听。

willChangeValueForKey: 和 didChangeValueForKey: 触发监听方法的时机：

* didChangeValueForKey: 方法会直接触发监听方法
* `NSKeyValueObservingOptionPrior` 是分别在值改变前后触发监听方法，即一次修改有两次触发。而这两次触发分别在 willChangeValueForKey: 和 didChangeValueForKey: 的时候进行的。如果注册方法中 options 传入 NSKeyValueObservingOptionPrior，那么可以通过只调用 willChangeValueForKey: 来触发改变前的那次 KVO，可以用于在属性值即将更改前做一些操作。

**移除：**

在移除 KVO 监听后，被观察对象的 isa 会指回原类 A，但是 NSKVONotifying_A 类并没有销毁，还保存在内存中。

**重写方法：**

NSKVONotifying_A 除了重写 setter 方法外，还重写了 class、dealloc、_isKVOA 这三个方法（可以通过 class_copyMethodList 获得），其中：

* class：返回父类的 class 对象，目的是为了不让外界知道 KVO 动态生成类的存在，隐藏 KVO 实现
* dealloc：释放 KVO 使用过程中产生的东西
* _isKVOA：用来标志它是一个 KVO 的类

参考：[iOS - 关于 KVO 的一些总结](https://juejin.cn/post/6844903972528979976 "iOS - 关于 KVO 的一些总结")

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

1、[RxSwift 中文文档](https://beeth0ven.github.io/RxSwift-Chinese-Documentation/ "RxSwift 中文文档") -- 来自RxSwift 中文文档

[@我是熊大](https://juejin.cn/user/1151943916921885)：其实RxSwift的中文文档完善度很高，其目的就是帮助iOS开发人员快速上手RxSwift，其中不仅讲了核心成员使用，还附带了精选的demo以及生态架构的相关文章。

2、[RxSwift 核心实现原理](http://chuquan.me/2020/08/24/rxswift-core-implement/ "RxSwift 核心实现原理") -- 来自博客：楚权的世界

[@我是熊大](https://juejin.cn/user/1151943916921885)：泛型和闭包，让RxSwift诞生，这篇文章带你还原RxSwift的设计现场，深入浅出，帮助你更深入的了解RxSwift的原理。


3、[开始使用Combine框架](https://beeth0ven.github.io/RxSwift-Chinese-Documentation/ "开始使用Combine框架") -- 来自博客：avanderlee

[@我是熊大](https://juejin.cn/user/1151943916921885)：WWDC2019苹果也提出了函数响应式编程框架，侧面展示了函数响应式编程未来的地位，本文作者就带你感受下Combine的魅力。


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
