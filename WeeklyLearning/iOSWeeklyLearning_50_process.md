# iOS摸鱼周报 第五十期

![](http://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：WWDC 22 Call to Code
> * 面试模块：事件响应与传递
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

### [WWDC 22 Call to Code](https://www.apple.com/newsroom/2022/04/apples-worldwide-developers-conference-returns-in-its-all-online-format/ "WWDC 2022 Call to Code")

![](http://cdn.zhangferry.com/Images/20220411235752.png)

Apple 宣布了 WWDC 22 的相关事项，时间是 6 月 6 号到 10 号，形式还是线上播放。苹果一向喜欢玩彩蛋，可以通过这张图片简单推测下，从图片看主体是 Swift 图标，更准确的说表示 SwiftUI 的可能性更大，边缘透出的光亮还有一种黎明到来，开启新篇章的感觉，所以很可能 SwiftUI 将迎来重大更新。就可联想的范围来说，什么样的更新才算重大呢，对标 Flutter，有没有可能支持全栈：Windows、Linux、Web 等平台？这个想法确实能配得上黎明到来，但还是有些大胆了，跨端和模仿也一直不是苹果的调性。具体会有怎样的更新，还是等发布会的时候见分晓吧。

同时 Swift Student Challenge 将继续举办，学生们可以通过 Swift Playgrounds 创造有趣的项目。项目提交截止时间是 4 月 25 号，获奖者将获得 Apple 提供的一件 WWDC22 主题外套，一套定制的别针套装和一年的开发者会员资格。活动详情可以点击 [Swift Student Challenge ](https://developer.apple.com/wwdc22/swift-student-challenge/ "Swift Student Challenge")查看。

## 面试解析

整理编辑：[JY](https://juejin.cn/user/1574156380931144)

### 当指尖触碰屏幕，触摸事件由触屏生成后如何传递到当前应用？

通过 `IOKit.framework` 事件发生，被封装为 `IOHIDEvent `对象，然后通过 `mach port`  转发到 `SpringBoard`（也就是桌面）。然后再通过`mach port`转发给当前 APP 的主线程，主线程`Runloop`的`Source1`触发,`Source1`回调内部触发`Source0回调`，`Source0`的回调内部将事件封装成`UIEvent` ，然后调用`UIApplication`的`sendEvent`将`UIEvent`传给了`UIWindow`。

>  `souce1`回调方法： `__IOHIDEventSystemClientQueueCallback()`
>
>  `souce0`回调方法:    `__UIApplicationHandleEventQueue()`

寻找最佳响应者，这个过程也就是`hit-testing`，确定了响应链，接下来就是传递事件。

如果事件没能找到能够相应的对象，最终会释放掉。`Runloop` 在事件处理完后也会睡眠等待下一次事件。

#### 寻找事件的最佳响应者（Hit-Testing）

当 APP 接受到触摸事件后，会被放入到当前应用的一个事件队列中（先发生先执行），出队后，`Application` 首先将事件传递给当前应用最后显示的`UIWindow`，询问是否能够响应事件，若窗口能够响应事件，则向下传递子视图是否能响应事件，优先询问后添加的视图的子视图，如果视图没有能够响应的子视图了，则自身就是最合适的响应者。

```objectivec
- (UIView *)hitTest:(CGPoint)point withEvent:(UIEvent *)event{
    //3种状态无法响应事件
     if (self.userInteractionEnabled == NO || self.hidden == YES ||  self.alpha <= 0.01) return nil; 
    //触摸点若不在当前视图上则无法响应事件
    if ([self pointInside:point withEvent:event] == NO) return nil; 
    //从后往前遍历子视图数组 
    int count = (int)self.subviews.count; 
    for (int i = count - 1; i >= 0; i--) 
    { 
        // 获取子视图
        UIView *childView = self.subviews[i]; 
        // 坐标系的转换,把触摸点在当前视图上坐标转换为在子视图上的坐标
        CGPoint childP = [self convertPoint:point toView:childView]; 
        //询问子视图层级中的最佳响应视图
        UIView *fitView = [childView hitTest:childP withEvent:event]; 
        if (fitView) 
        {
            //如果子视图中有更合适的就返回
            return fitView; 
        }
    } 
    //没有在子视图中找到更合适的响应视图，那么自身就是最合适的
    return self;
}
```

#### 传递事件

找到最佳响应者后开始传递事件

`UIApplication sendEvent ` =>`UIWindow sendEvent` =>`UIWindow _sendTouchesForEvent` =>`touchesBegin` 

#### UIApplication 是怎么知道要把事件传给哪个 window 的？window 又是怎么知道哪个视图才是最佳响应者的呢？

在`hit-testing`过程中将 `Window`与 `view`绑定在 `UIEvent`上的`touch`对象

#### 响应者为什么能够处理响应事件，提供了哪些方法？

```objectivec
//手指触碰屏幕，触摸开始
- (void)touchesBegan:(NSSet<UITouch *> *)touches withEvent:(nullable UIEvent *)event;
//手指在屏幕上移动
- (void)touchesMoved:(NSSet<UITouch *> *)touches withEvent:(nullable UIEvent *)event;
//手指离开屏幕，触摸结束
- (void)touchesEnded:(NSSet<UITouch *> *)touches withEvent:(nullable UIEvent *)event;
//触摸结束前，某个系统事件中断了触摸，例如电话呼入
- (void)touchesCancelled:(NSSet<UITouch *> *)touches withEvent:(nullable UIEvent *)event;
```

### 触摸事件如何沿着响应链流动？

在确定最佳响应者之后，优先给最佳的对象响应，如果最佳对象要将事件传递给其他响应者，这个从底到上的过程叫做响应链。

#### 如果有 UIResponder、手势、UIControl 同时存在，是怎么处理的？

系统提供的有默认 `action` 操作的 `UIControl`，例如 `UIButton、UISwitch` 等的单击，响应优先级比手势高，而自定义的却比手势识别器要低，然后才是  `UIResponder` 。

`Window` 在将事件传递给 `hit-tested view` 之前，会先将事件传递给相关的手势识别器,并由手势识别器优先识别。若手势识别器成功识别了事件，就会取消 `hit-tested view`对事件的响应；若手势识别器没能识别事件，`hit-tested view` 才完全接手事件的响应权。

#### Window怎么知道要把事件传递给哪些手势识别器？

`event` 绑定的`touch`对象维护了一个手势数组，在 `hit-testing` 的过程中收集对应的手势识别器， `Window` 先将事件传递给这些手势识别器，再传给 `hit-tested view`。一旦有手势识别器成功识别了手势，`Application` 就会取消`hit-tested view`对事件的响应。

#### 手势识别器与UIResponder对于事件响应的联系？

* `Window`先将绑定了触摸对象的事件传递给触摸对象上绑定的手势识别器，再发送给触摸对象对应的 `hit-tested view`。

* 手势识别器识别手势期间，若触摸对象的触摸状态发生变化，事件都是先发送给手势识别器再发送给 `hit-test view`。

* 手势识别器若成功识别了手势，则通知 `Application` 取消 `hit-tested view` 对于事件的响应，并停止向 `hit-tested view` 发送事件；

* 若手势识别器未能识别手势，而此时触摸并未结束，则停止向手势识别器发送事件，仅向 `hit-test view` 发送事件。

* 若手势识别器未能识别手势，且此时触摸已经结束，则向 `hit-tested view` 发送 `end` 状态的 `touch`事件以停止对事件的响应。

>  **cancelsTouchesInView** 若设置成YES，则表示手势识别器在识别手势期间，截断事件，即不会将事件发送给hit-tested view。
>
>  **delaysTouchesBegan** 若设置成NO，则在手势识别失败时会立即通知Application发送状态为end的touch事件给hit-tested view以调用 `touchesEnded:withEvent:` 结束事件响应。

#### 有哪些情况无法响应？

* **不允许交互**：`userInteractionEnabled = NO`

* **隐藏**（`hidden = YES `）：如果父视图隐藏，那么子视图也会隐藏，隐藏的视图无法接收事件

* **透明度**：alpha < 0.01 如果设置一个视图的透明度<0.01，会直接影响子视图的透明度。alpha：0.0~0.01为透明。

### 参考

[iOS触摸事件全家桶](https://www.jianshu.com/p/c294d1bd963d "iOS触摸事件全家桶")

## 优秀博客

整理编辑：皮拉夫大王在此

> 本期优秀博客主题为重新了解`rebase` & ` bind` 。前段时间字节发了篇关于iOS 15`fixup-chain`机制的相关文章，其中`rebase`机制引起了大家热烈的讨论。在讨论的过程中，包括我在内的部分同学纠正了之前对`rebase`的错误认识，因此有必要跟大家一块再来学习下`rebase` & ` bind`
>
> **在阅读之前，先来问几个问题：**
>
> - `reabse` 时会修改TEXT段的数据吗？如果不修改，那静态链接时还不知道ASLR后的真实地址难道不需要通过rebase修正吗？如果要修改，TEXT段不是只读段吗，为什么可以修改呢？
> - iOS 15之前的`fixup-chain`机制与之前的`rebase` & ` bind`有何不同？
>
> 如果你真正了解`rebase` & ` bind`机制，那么这两个问题要弄清楚。

1、**复习iOS的rebase和bind**

1.1 [深入理解 Symbol](https://mp.weixin.qq.com/s/uss-RFgWhIIPc6JPqymsNg) -- 来自公众号：小集

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：在了解rebase和bind之前必须要了解iOS的符号，符号是bind的桥梁。文章中对符号的介绍比较详细，包含之前很少提到的lazy symbol，weak symbol等。

1.2 [给实习生讲明白 Lazy/Non-lazy Binding](https://juejin.cn/post/7001842254495268877) -- 来自掘金：No

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：这篇文章是对bind讲解的浅显易懂，非常适合之前不了解bind的同学阅读。

1.3 [图解 Mach-O 中的 got](https://juejin.cn/post/6918645161303998478) -- 来自掘金：微微笑的蜗牛

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：这篇文章也是介绍相关知识的，可以补充阅读。

2、**关于iOS15的fixup机制**

2.1  [iOS 15 如何让你的应用启动更快]( https://juejin.cn/post/6978750428632580110) -- 来自掘金：ZacJi

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：iOS15的fixup介绍将主要通过三篇文章，逐次加深深度。阅读这篇文章后，大家应该要弄清楚作者所说的启动加速的原因，以及与二进制重排是否有关系。

2.2 [从野指针探测到对iOS 15 bind 的探索](https://mp.weixin.qq.com/s/BNIWBwemmz4isbjBb9-pnQ) -- 来自公众号：皮拉夫大王在此

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：在阅读了《iOS 15 如何让你的应用启动更快》，进一步探索了bind机制并且加以应用。

2.3 [iOS15 动态链接 fixup chain 原理详解](https://mp.weixin.qq.com/s/k_RI2in_Q5hwT33KWig34A "iOS15 动态链接 fixup chain 原理详解") -- 来自公众号：字节跳动终端技术

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：更加完善地介绍iOS 15的fixup机制。


## 见闻

> 这一周阅读/浏览到的有趣的资讯。

1、[识花软件-形色](https://apps.apple.com/cn/app/%E5%BD%A2%E8%89%B2-%E6%8B%8D%E7%85%A7%E8%AF%86%E8%8A%B1%E8%AF%86%E5%88%AB%E6%A4%8D%E7%89%A9/id1018747351?l=en "形色")

[@zhangferry](zhangferry.com)：春天来了，又到了踏春赏花的时候，如果此时没有疫情可能大家的脚步能走的更远。春天的信号最明显的就是马路或者公园里盛开了各种各样的花，五颜六色的，非常招人喜欢。当我把手机对准这些花的时候，才发现他们在我眼里统称为花，即使相差很大，我也很难说这是什么花那是什么花。后来找到了一个叫做形色的软件，它可以通过拍照识别花的名字。我将小区和附近公园里的花用它来识别，于是就有了下面这张图：

![](http://cdn.zhangferry.com/Images/spring_flowers.jpg)

终于知道这些花叫什么名字了，当我把花和它们各自的名字对应上之后，花也感觉更好看了。

2、[互联网用户公众账号信息服务管理规定](http://www.cac.gov.cn/2021-01/22/c_1612887880656609.htm "互联网用户公众账号信息服务管理规定")

[@zhangferry](zhangferry.com)：最近在公众号读到几篇疫情相关的文章，转发了一下，没多久就被平台删文了。在被删文的说明里附了一个链接，链接指向即是《互联网用户公众账号信息服务管理规定》，该规定的管理范围覆盖我们通过网络获取的几乎所有信息。我们需要理解公众信息生产的三方：平台、内容生产者和监管之间各自的职责和义务。内容不长，分五个章节，以下仅是概括，不属于解读。

第一章：总则。是整个规定的纲领，说明了公众账号信息服务涉及的三方（平台方、内容生产者、监督者）各自的职责。包含这些要点：

* 国家网信部分负责该规定的监督、执法、管理工作。
* 公众账号信息服务平台和公众账号生产运营者应当遵守法律法规，生产发布向上向善的优质信息内容。
* 鼓励各级党政机关、企事业单位和人民团体注册运营公众账号，生产发布高质量政务信息或者公共服务信息，满足公众信息需求。（这也是各个社交媒体都能看到政务机关官方号的原因。）
* 公众账号信息服务平台的运营需取得互联网新闻信息服务许可。

第二章：公众账号信息服务平台。这一章节内容最多，是对平台方的一些约束。包含这些要点：

* 平台是信息生成内容的主题责任对象。
* 需建立公众账号分类注册和分类生产制度、公众账号主体信息核验、注册限制、保证数据真实性等措施。

第三章：公众账号生产运营者。是对生成信息的一些约束。包含这些：

* 如实填写账号注册信息。
* 公众账号生产运营者应当履行信息内容生产和公众账号运营管理主体责任。
* 遵守著作权保护相关法律法规。
* 不得发布虚假、煽动用户情绪、不实、违法等信息。

第四章：监督管理。公共信息中参与的三方都需要的监督管理。

* 平台。应加强对公众账号的管理，及时处理违法违规行为。
* 内容生产者。也包括平台，应接受社会的监督
* 各级网信部门。建立健全响应的工作制度。

第五章：附则。附加说明：

* 互联网公众账号覆盖范围，在互联网中发布文字、图片、音视频等信息内容都包括。
* 生效时间：2021 年 2 月 22 日起施行。

3、[什么是CNAME以及CDN？](https://zhuanlan.zhihu.com/p/400556541 "什么是CNAME以及CDN？") -- 来自知乎：漢堡再来一个

[@zhangferry](zhangferry.com)：前一段时间发现往 Gitee 上传图片失败，博客的图片也全挂了，打开邮箱发现 Gitee 发的一封邮件：

![](http://cdn.zhangferry.com/Images/20220413232557.png)

果然免费的东西不好用，简单调研之后决定迁移到七牛云上。

使用七牛云作为图床的话，需要用到它的两个服务：存储和访问（使用七牛云的前提是要有备案域名）。存储是每月免费 10 个 G。访问的话，默认开启 CDN 加速，这部分流量需要付费，这个可以根据需求购买对应的流量包，很便宜。这里可以讲下配置 CDN 加速时遇到的两个概念，CNAME 和 CDN。

![](http://cdn.zhangferry.com/Images/20220414003247.png)

CDN 的作用是访问加速，如何加速呢，就是分配多个服务器上，就近访问，访问之后该服务器会缓存源站的资源，之后的访问就不会请求源站而是直接访问这台就近的服务器了。

我们配置一个域名，例如  `cdn.zhangferry.com`，将它的源站指向七牛的存储空间。这里是一对一的关系，为了能够实现一对多，我们不直接指向源站，而是指向七牛的调度服务器。这个实现就是利用 CNAME，它相当于给我们需要解析的域名起一个别名，访问 `cdn.zhangferry`，就会访问到七牛调度服务器，这台服务器还可以配置 CNAME，再去指向另外一个域名。我们可以使用 `dig` 命令验证这个流程，cdn 域名的最终指向是一个特定的 IP 服务器，只不过在不同地区这个目标服务器 IP 不同。

4、[GIF：一个观察互联网历史的切面](https://mp.weixin.qq.com/s/_-3FsN-jDyxaqSSW7hUibw) -- 来自公众号：全媒派

[@远恒之义](https://github.com/eternaljust/)：GIF 动图是数字时代的图像语言。GIF 生产方便，传播迅速，满足了人类交际的需求，刺激人们的视觉与情感，成了线上文化的迷因。当我们在斗图的时候，比的是表情包的资源，拼的是网上冲浪的时间，笑的是对“梗”文化的认同。不知道大家平时在社交媒体上使用表情包的频率如何，有没有想过 GIF 到底是怎么来的呢？

5、[手中有粮，心里不慌：如何储备自己的物资「大后方」](https://sspai.com/post/72477 "手中有粮，心里不慌：如何储备自己的物资「大后方」") -- 来自少数派：乔淼

[@远恒之义](https://github.com/eternaljust/)：最近吉林长春和上海疫情严重，身边有朋友身处这两地被困家中，暂时性的物质短缺。看到群里的小伙伴自己用黄豆发豆芽，心中感慨万千，不是滋味。

这是一份科学的囤货指南，总结了作者在物资储备方面的心得体会，满足短期与长期的食物存储需求。关于其他物资的储备以及培养个人储备习惯，作者在文章中也有明确的建议。希望大家都能成为生活的高手。

> 生存危机未必只发生在远离文明世界的地方。（各种突发事件）将切断所有的日常服务和食物供应。……在大城市，商店的食品架上将空空如也……公园和花园里的植物皮将会被剥光……（在正常的秩序恢复前）你只有依靠自身的资源条件和技巧安排生活。  
> ———约翰·怀斯曼，《生存手册》，第 11 章 14 节，「大后方」

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 闲话 Swift 协程

**地址**：https://www.bennyhuo.com/book/swift-coroutines/

该系列博客从浅入深地介绍了 Swift 在 5.5 中新支持的协程特性。该系列文章介绍了 Swift 协程的特性，内容以 Swift 协程的基本概念、语法设计、使用场景等方面为基础展开，也会与大前端开发者常见的 Kotlin、JavaScript 做对比（作者是 Kotlin GDE），作者希望这个系列能给大家一个更多元化的视角来理解这个语法特性，十分推荐。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### AppleParty

**地址**：https://github.com/37iOS/AppleParty

**软件状态**：开源

**软件介绍**：

介绍一个我们周报团队成员所在公司开源的一个项目：`AppleParty`

`AppleParty` 是三七互娱旗下37手游 iOS 团队研发，实现快速操作 `App Store Connect` 后台的自动化 `macOS` 工具。

支持功能：

* 内购买项目管理（批量创建和更新）；
* 批量商店图和预览视频上传和更新；
* 邮件发送工具；
* 二维码扫描和生成工具；

![AppleParty](http://cdn.zhangferry.com/06.jpeg)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第四十八期](https://mp.weixin.qq.com/s/vdUy-BqxWzuPcjYO6fFsJA)

[iOS摸鱼周报 第四十七期](https://mp.weixin.qq.com/s/X6lPQ5qwY1epF6fEUhvCpQ)

[iOS摸鱼周报 第四十六期](https://mp.weixin.qq.com/s/8Wpfk9yxpjwaDXN7iXIcvQ)

![](http://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
