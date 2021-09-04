# iOS摸鱼周报 第二十六期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：跟熊大聊一下独立开发和音视频开发。
> * Tips：关于 TestFlight 外部测试的一些介绍。
> * 面试模块：本期解析 KVO 的实现原理。
> * 优秀博客：收录了一些 RxSwift 相关的文章。
> * 学习资料：
> * 开发工具：公众号文章同步工具 Wechatsync。

## 本期话题

[@zhangferry](https://zhangferry.com)：本期交流对象是摸鱼周报的另一位编辑：[🐻我是熊大](https://juejin.cn/user/1151943916921885/posts)。他在音视频方向有很多经验，自己也独立维护了两款应用，我们围绕这两个层面来和他交流一下。

zhangferry：简单介绍下自己吧。

> 大家好，我是熊大，野生iOS开发者，目前正在做一款海外社交 App，在团队中主要负责 iOS 的架构设计以及性能优化。

zhangferry：你有多款独立开发的应用，能简单介绍下当时独立开发的初衷和现状吗？

> 独立开发的产品是[《今日计划》](https://apps.apple.com/cn/app/id1505020317)、[《imi我的小家》](https://apps.apple.com/cn/app/id1543829703)。
>
> 当时做独立开发的目的有两个：一个是自己有些想法想要实现出来，二是希望能有睡后收入。之前认为独立开发可能需要更多时间投入，后来发现独立开发最首要的问题不是时间，而是运营和验证；如何找到产品定位人群，如何优化 ASO，关键词如何填写，产品留存达到多少才是及格？这些都是初次尝试独立开发容易忽略却不得不面对的挑战。也正因此，我做了个公众号[独立开发者基地](https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=Mzg4OTU1Njk1MQ==&scene=124#wechat_redirect)，分享独立开发遇到的问题。

zhangferry：在你看来要做独立开发需要具备哪些重要技能呢？

> 以下 5 个方面可能是我们需要的：
>
> 1、具备产品思维，能编写需求文档，分析产品数据，摸索产品方向。
> 
> 2、具备使用 Sketch、Figma、蓝湖的能力。
> 
> 3、运营推广能力，如何让app能被更多的人知道，如何召回用户
> 
> 4、具备iOS、Android、小程序等一个或多个的开发能力
> 
> 5、后端开发能力，其实这个前期可以使用第三方代替
> 
> 这些都是硬件实例，最关键的还是执行力和创造力，如果你有想法，那就不要等待。

4、你的工作中多涉及音视频技能，能说下音视频开发和普通应用开发有什么区别吗？如果想往这个方面学习，需要注意和关注哪些东西。

> 在我的工作中，音视频开发主要涉及到AVFoundation、FFmpeg、OpenGL ES、MetalKit等框架。
> 
> 音视频开发入门会更难一些，需要有图形图像学的基础知识；有时需要编写 C\C++ 代码，很多第三方的音视频库都是 C\C++ 写的，比如常用的 libjpeg-turbo、lame；同时要熟悉CMake工具进行编译等。
> 
> 推荐学习路线:
> 
> 1、数字图像的基本知识
> 
> 2、开源库 GPUImage，AVFoundation + OpenGL ES,2016年时，很多第三方SDK图像处理框架都是基于这个开发的。
> 
> 3、开源库 GPUImage3，这是AVFoundation + Metal。
> 
> 4、李明杰老师今年有一个FFmpeg的课程。
> 
> 我在小专栏开了一个介绍音视频技术的专栏：[GPUImage By Metal](https://xiaozhuanlan.com/GPUImage)，大家如果对这类知识感兴趣的话欢迎订阅。另外再送大家一些免费领取资格，名额有限只有十个，[点击这里领取](https://xiaozhuanlan.com/GPUImage/present/42a8fba462217d3717c54d707db55ae7b49d86ce)。

5、如何保持学习的热情，能否分享一些你的学习方法。

> 保持热情的最好办法就是热爱或追求。
> 
> 1、学习要循序渐进，不要一下学太多，陌生的东西太多会打消积极性。
> 
> 2、如果遇到几天都无法理解的东西，放一放，发酵几个月后再看。
> 
> 3、要有目标和实践方案

6、有什么需要借助于摸鱼周报宣传的。

> 1、希望大家多多关注 SpeedySwift 这个开源项目：https://github.com/Tliens/SpeedySwift ，这是一个用于提效 Swift 开发的仓库，觉得 OK 的话给我个 star 鼓励一下吧。
> 
> 2、北京连趣科技，寻找一起并肩作战的小伙伴，各个岗位都有需求，简历可以投递到 tliens.jp@gmail.com，我的微信：`bear0000001`。

## 开发Tips

整理编辑：[zhangferry](https://zhangferry.com)

### 关于 TestFlight 外部测试

TestFlight 分为内部和外部测试两种。

内部测试需要通过邮件邀请制，对方同意邀请才可以参与到内部测试流程，最多可邀请100人。每次上传应用到AppStore Connect，内部测试人员就会自动收到测试邮件的通知。

外部测试可以通过邮件邀请也可以通过公开链接的形式直接参与测试，链接生成之后就固定不变了，其总是指向当前最新版本。外部测试最多可邀请10000人。

与内测不同的是，外测每个版本的首次提交都需要经过苹果的审核。比如应用新版本为 1.0.0，首次提交对应的 build 号为 100，这个 100 的版本无法直接发布到外部测试，需要等待 TestFlight 团队的审核通过。注意这个审核不同于上线审核，AppStore 和 TestFlight 也是两个不同的团队。外测审核条件较宽泛，一般24小时之内会通过。通过之后点击公开连接或者邮件通知就可以下载 100 版本包。后面同属 1.0.0 的其他 build 号版本，无需审核，但需要每次手动发布。

采用公开链接的形式是无法看到测试者的信息的，只能查看对应版本的安装次数和崩溃测试。

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

### RxSwift

1、[RxSwift 中文文档](https://beeth0ven.github.io/RxSwift-Chinese-Documentation/ "RxSwift 中文文档") -- 来自RxSwift 中文文档

[@我是熊大](https://juejin.cn/user/1151943916921885)：其实 RxSwift 的中文文档完善度很高，其目的就是帮助 iOS 开发人员快速上手 RxSwift，其中不仅讲了核心成员使用，还附带了精选的 demo 以及生态架构的相关文章。

2、[RxSwift 核心实现原理](http://chuquan.me/2020/08/24/rxswift-core-implement/ "RxSwift 核心实现原理") -- 来自博客：楚权的世界

[@我是熊大](https://juejin.cn/user/1151943916921885)：泛型和闭包，让 RxSwift 诞生，这篇文章带你还原 RxSwift 的设计现场，深入浅出，帮助你更深入的了解RxSwift 的原理。

3、[初识RxSwift及使用教程](https://developer.aliyun.com/article/233478?spm=a2c6h.13262185.0.0.3c6263e6j04OZD "初识RxSwift及使用教程")  -- 来自：韩俊强的博客

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：RxSwift 是 Swift 函数响应式编程的一个开源库。初次接触的同学可能会提问为什么要用 RxSwift。因此可以看看这篇文章。作为初学者，通过阅读这篇文章感觉 RxSwift 使逻辑离散的代码变的聚合，逻辑更加清晰。当然，RxSwift 不止于此，纸上得来终觉浅，更多的优势可能只有深入使用才会有所体会。

4、[RxSwift使用教程大全](https://developer.aliyun.com/article/233477?spm=a2c6h.13262185.0.0.3c6263e6hxn23r "RxSwift使用教程大全") -- 来自：韩俊强的博客

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：RxSwift 的教程大全，罗列了比较多的 RxSwift 使用方法。

5、[使用 RxSwift 进行响应式编程](http://t.swift.gg/d/2-rxswift) -- 来自：AltConf

[@zhangferry](https://zhangferry.com)：这是 [AltConf 2016](http://altconf.com/) 中的一期讲座内容，整理翻译成了中文。虽然是2016年的内容，但RxSwift的基本概念是不会改变的，这篇内容 Scott Gardner 将带大家走入到响应式编程的世界当中，并告诉大家一个简单的方法来开始学习 RxSwift。

6、[RxSwift vs PromiseKit](https://medium.com/@DianQK/rxswift-vs-promisekit-5c617fc1b789 "RxSwift vs PromiseKit") -- 来自：靛青DKQing

[@zhangferry](https://zhangferry.com)：如果仅是为了处理回调地狱就选择引入 RxSwift，就有些大材小用了，处理回调地狱用 PromiseKit 就可以。RxSwift 里的回调处理只是附加功能，其真正的思想是响应式，PromiseKit 非响应式框架。**响应式是一种面向数据流和变化传播的编程范式**，不只是异步的网络请求，像是点击行为，文本框不同的输入都是数据流的一种形式，概念的理解在学习响应式编程中尤为重要。文中通过一个简单的例子，来说明 PromiseKit 不具备流的特性。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)、[zhangferry](https://zhangferry.com)

### RxSwift 学习教程

地址：http://t.swift.gg/t/rxswift-course

结合本期优秀博客的内容再推荐一个 RxSwift 学习教程。大家如果仔细看 AltConf 那篇译文的话会注意到里面的译者注：

> 国内最好的 RxSwift 教程推荐[靛青DKQing](https://medium.com/@DianQK/)所撰写的 *RxSwift 教程系列*，有兴趣的同学可以前往阅读。

由此可见靛青是当时公认的 RxSwift 代表人物，他是国内较早一批接触并深入理解 RxSwift 的人之一，对 RxSwift 在国内的推广起到了很大的帮助。

课程系列的顺序大致是这样：基本的使用 -> 基本的概念 -> 进阶的使用 -> 源码解读。

该课程写于2016年，至今有一段时间了，部分语法可能有变，但不影响我们对概念的理解，仍有一定的参考学习价值。

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

### Wechatsync

**地址**：https://www.wechatsync.com/

**软件状态**：免费，[开源](https://github.com/wechatsync/Wechatsync)

**软件介绍**：

作为号主通常会将文章发布到多个平台，每个平台都重复地登录、复制、粘贴是一件很麻烦的事。Wechatsync就是这样一款解脱重复工作的神器。它是一款 Chrome 浏览器插件，支持多个平台的文章发布，这需要我们提前登录各个平台获得授权。它会自动识别公众号文章，弹出「同步该文章」按钮，然后点击就可以同步文章到我们授权的平台。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210904171532.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第二十五期](https://mp.weixin.qq.com/s/LLwiEmezRkXHVk66A6GDlQ)

[iOS摸鱼周报 第二十四期](https://mp.weixin.qq.com/s/vXyD_q5p2WGdoM_YmT-iQg)

[iOS摸鱼周报 第二十三期](https://mp.weixin.qq.com/s/1Vs50Lbo0Z27dnU-ARQ96A)

[iOS摸鱼周报 第二十二期](https://mp.weixin.qq.com/s/JI5mlzX9cYhXJS81k1WE6A)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
