# iOS 摸鱼周报 #64 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

整理编辑：[zhangferry](zhangferry.com)

### Apple 秋季发布会

在发布会之前关于 iPhone 14 的爆料已经不少了，但看到灵动岛（Dynamic Island，翻译太赞了）的创意，还是让人眼前一亮。

![](https://cdn.zhangferry.com/Images/iphone_14_dynamic_island.GIF)

回想一下从 Home 键、3D Touch、全面屏的解锁手势、灵动岛，再包括 MacBook 的 Touch bar，Apple 对于交互的设计都是软硬件结合的。但灵动岛又不太一样，挖孔屏对于苹果来说不是首发，他是在一个本来就带槽点的能力上做的设计，把劣势变成优势这个能力是非常厉害的。

再说回这个设计，看过宣传视频，对于灵动岛具备的能力可能还会有些疑惑，这个控件能否由开发者控制呢？能控制到什么地步？原有通知的样式是否需要适配？因为这个功能可以配合 Live Activities 使用，应该是有一种配置是用于在灵动岛中展示的，但当我想看下这个文档，看能否找到一些相关的 API时，发现这个[文档链接](https://developer.apple.com/documentation/activitykit/displaying-live-data-on-the-lock-screen-with-live-activities "displaying-live-data-on-the-lock-screen-with-live-activities")被下掉了，整个 ActivityKit 文档也都没了，不知道这是要干啥。既然没法看文档就从网上爆出的视频简单推测下它的能力吧。

* 与  Live Activities 能力结合，作为一个小的通知面板，这块样式定制应该是写到 ActivityKit 框架里的。

* 样式上支持开发者的控制，但能控制的内容不多，比如为了跟屏幕融为一体，背景会被限定为黑色。
* 这算是一种后台能力，应该是只有申请嘞这类能力的 App 才有此功能。
* 支持最多两个 App 的停留，会变成「叹号」样式。如果有更多后台 App 会如何替换，这个还不清楚。
* 点击切换至对应 App，长按展开为大屏，目前已知的大屏样式有长条状、圆角正方形状、延伸屏幕边缘的矮矩形和高矩形、还有一种介于圆角正方形和屏幕宽度之间的尺寸。对于形状的定义应该会比 Widget 多，但不会是任意定制。
* 灵动岛长短的变化会影响左右两侧时间和信号的展示，如果灵动岛展示为大尺寸，两边的元素会被挤压至屏幕外。

* 关于通知的样式，原有通知样式应该还会在挖孔的下面展示，因为要所有的通知样式适配黑色背景有点难。但针对灵动岛的通知样式应该会有提供。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)


## 内容推荐

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)


## 摸一下鱼

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

介绍几个关于iOS开发国际化的工具；

- genstrings：Xcode内置工具，从指定的 C 或者 Objective-C 源文件生成 `.strings` 文件；
- ibtool：Xcode内置工具，正如 `genstrings` 作用于源代码，而 `ibtool` 作用于 `XIB` 文件；
- bartycrouch：bartycrouch 可以依据 interfaces 文件( xib 文件) 和代码(swift 、m、h 文件)来增量更新 strings 文件。在这里 增量 是指 bartycrouch 会默认保留已经翻译的值及改变了的注释；
- Poedit：Poedit 是一款基于多语言的本地化工具，支持 Win/Mac/Linux 三大主流平台，经常被用于本地化各种计算机软件；


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #63 | Apple 企业家培训营已开放申请](https://mp.weixin.qq.com/s/nAMshUG4AjWLAAHOFPVqXg)

[iOS 摸鱼周报 #62 |  Live Activity 上线 Beta 版 ](https://mp.weixin.qq.com/s/HySX4Yaf3Zxy8Wn-LyUO0A)

[iOS 摸鱼周报 #61 |  Developer 设计开发加速器](https://mp.weixin.qq.com/s/WfwqRhC-9-isUanv8ZnvMQ)

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
