# iOS 摸鱼周报 #64 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [Freeform App 上线](https://www.apple.com/newsroom/2022/12/apple-launches-freeform-a-powerful-new-app-designed-for-creative-collaboration/ "Freeform App上线")

![](https://cdn.zhangferry.com/Images/20221215212106.png)

[@zhangferry](zhangferry.com)：随 iOS 16.2，Apple 发布了新的系统应用 Freeform，同时有 iPad 和 Mac 版，中文译为：「无边记」，该 App 定位于创造性的头脑风暴和协作。Freeform 有这些特点：

* 创作空间无限，想画多大就画多大。

* 支持非常多格式的嵌入，包括图片、PDF、网站链接、视频、地图定位、图表等等。

* 可以多人创作，支持最多邀请 100 位协作者。

* iClound 同步，你可以无缝切换到 iPad 和 Mac 场景继续使用。

* 可以边创作边开启 Facetime。

白板是一个相对自由的创作空间，我想到的一些使用场景是，办公室的远程会议，大家一起想一些 idea；网课里老师远程教授知识，通过 Freeform 跟学生进行互动。

## 本周学习

整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)
#### Xcode 僵尸对象Zombie Objects

Zombie Objects 是用来调试与内存有关的问题，跟踪对象的释放过程的工具，通常用来排查野指针问题。

在 `Xcode` -> `Edit Scheme` -> `Memory Management` -> `Zombie Objects` 

#### 僵尸对象的生成过程：

```C++
// 获取到即将deallocted对象所属类（Class）
Class cls = object_getClass(self);
    
// 获取类名
const char *clsName = class_getName(cls)
    
// 生成僵尸对象类名
const char *zombieClsName = "_NSZombie_" + clsName;
    
// 查看是否存在相同的僵尸对象类名，不存在则创建
Class zombieCls = objc_lookUpClass(zombieClsName);
if (!zombieCls) {
    // 获取僵尸对象类 _NSZombie_
    Class baseZombieCls = objc_lookUpClass(“_NSZombie_");
        
    // 创建zombieClsName类
    zombieCls = objc_duplicateClass(baseZombieCls, zombieClsName, 0);
}
// 在对象内存未被释放的情况下销毁对象的成员变量及关联引用。
objc_destructInstance(self);
    
// 修改对象的isa指针，令其指向特殊的僵尸类
objc_setClass(self, zombieCls);
```

#### Zombie Object 触发时做了什么？

```C++
// 获取对象class
Class cls = object_getClass(self);
    
// 获取对象类名
const char *clsName = class_getName(cls);
    
// 检测是否带有前缀_NSZombie_
if (string_has_prefix(clsName, "_NSZombie_")) {
    // 获取被野指针对象类名
    const char *originalClsName = substring_from(clsName, 10);
     
    // 获取当前调用方法名
    const char *selectorName = sel_getName(_cmd);
    　　
    // 输出日志
    print("*** - [%s %s]: message sent to deallocated instance %p", originalClsName, selectorName, self);
        
    // 结束进程
    abort();
}
```

系统修改对象的 `isa` 指针，令其指向特殊的僵尸类，使其变为僵尸对象，并且打印一条包含该对象的日志，然后终止应用程序。

## 内容推荐

整理编辑：[Mim0sa](https://juejin.cn/user/1433418892590136/posts)

1、[源码探索SwiftUI框架—TCA](https://juejin.cn/post/7164699554711863326) -- 来自：合合信息

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：本文将会详细的带你体验 TCA 框架该如何去使用，从定义、绑定到调用，并从源码探析整个流程的逻辑，清晰易懂。同时 TCA 也还在快速的发展和推进中，可以期待 TCA 的完善。

2、[《游戏学导论》- 笔记](http://pjhubs.com/2022/01/29/game05/) -- 来自：PJHubs

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：这是一份博主学习华科熊硕老师的《游戏学导论》的系列笔记文章，主要讨论了游戏作为人文社会的一部分中，人与游戏之间的关系和理解，感兴趣的朋友可以读一下。

3、[GCDWebServer 使用详解](https://xiaovv.me/2018/11/30/GCDWebServer-BasicUse/) -- 来自：笑忘书店

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：GCDWebServer 是一个基于 GCD 的轻量级服务器框架，使用 GCDWebServer 我们可以很轻松的在我们的应用中搭建一个 HTTP 服务器，比如可以使用 GCDWebServer 来实现一个无线U盘 App。该篇文章比较详细的讲解了这个框架的主要使用流程，有两种语言的实现，代码内容详实。

4、[SwiftOnTap](https://swiftontap.com/) -- 来自：SwiftOnTap

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：这是一份看起来很像官方文档，但是又比官方文档详细很多的 SwiftUI 文档，由一些 iOS 开发者一起维护，将一些在官方文档上写的不清楚、不详细的地方重新编写，填补了 Apple 文档的一些漏洞，其中各种 UI 类的实现还有动画和图片作为辅佐，很好用。

5、[What is the difference between #available and @available](https://sarunw.com/posts/available-vs-available/) -- 来自：Sarunw

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：本文主要讨论了 # 和 @ 在 Swift 代码中的不同的意义。

6、[iOS APP添加桌面快捷方式](https://mp.weixin.qq.com/s/z_CfthCni7m1mKtM0KzH6g) -- 来自：搜狐技术产品

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：本文记录了实现添加桌面快捷方式的一些实现，给出了两个具体的方案，同时也分析了两个方案的利弊。




## 摸一下鱼

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

1、[【深度解读】喧嚣过后，再来聊聊灵动岛](https://www.bilibili.com/video/BV1W14y1N7MY "【深度解读】喧嚣过后，再来聊聊灵动岛")：这是ZEALER官方频道的一期视频，作者从 Apple 的开发者文档和UI交互的深层用意两方面去考虑灵动岛的设计意图。灵动岛的主要作用是「补上了iOS高频更新信息管理缺失的一环」，由此也延伸出了几个观点：

* 微信消息不可能适配灵动岛
* 灵动岛未来不会成为多任务的入口


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #63 | Apple 企业家培训营已开放申请](https://mp.weixin.qq.com/s/nAMshUG4AjWLAAHOFPVqXg)

[iOS 摸鱼周报 #62 |  Live Activity 上线 Beta 版 ](https://mp.weixin.qq.com/s/HySX4Yaf3Zxy8Wn-LyUO0A)

[iOS 摸鱼周报 #61 |  Developer 设计开发加速器](https://mp.weixin.qq.com/s/WfwqRhC-9-isUanv8ZnvMQ)

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
