# iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：iOS 16.2 发布，带来了无边记 App；D2 本周开始
> * 本周学习：Xcode 僵尸对象 Zombie Objects
> * 内容推荐：几篇 Swift 相关的文章
> * 摸一下鱼：再次解读灵动岛的定位；面相算法初学者的算法书「Hello 算法」；关于独立开发如何养活自己的讨论

## 本期话题

### iOS 16.2 发布

[@zhangferry](zhangferry.com)：iOS 16.2 主要发布了这些功能，其中 Freeform 这个全新内置 App 感觉值得拿出来单独讲一讲。

![](https://cdn.zhangferry.com/Images/20221215234359.png)

#### [Freeform App 上线](https://www.apple.com/newsroom/2022/12/apple-launches-freeform-a-powerful-new-app-designed-for-creative-collaboration/ "Freeform App上线")

![](https://cdn.zhangferry.com/Images/20221215212106.png)

随 iOS 16.2，Apple 发布了新的系统应用 Freeform，同时有 iPad 和 Mac 版，中文译为：「无边记」，该 App 定位于创造性的头脑风暴和协作。Freeform 有这些特点：

* 创作空间无限，想画多大就画多大。

* 支持非常多格式的嵌入，包括图片、PDF、网站链接、视频、地图定位、图表等等。

* 可以多人创作，支持最多邀请 100 位协作者。

* iClound 同步，你可以无缝切换到 iPad 和 Mac 场景继续使用。

* 可以边创作边开启 Facetime。

白板是一个相对自由的创作空间，我想到的一些使用场景是，办公室的远程会议，大家一起想一些 idea；网课里老师远程教授知识，通过 Freeform 跟学生进行互动。

### 第十七届 D2 本周末开始

本届 D2 为期两天共五场活动，议题范围从开发者的研发交付到监控运维，从运行时的上层框架到底层引擎，从过去始终在效率与体验间平衡的跨端技术，到将引领下一代体验革命的 3D/XR 技术全部都会涵盖。会议详情可以查看这篇介绍：[3D/XR、自研 SwiftUI、Lynx、QUIC、边缘计算、Flutter 等话题集结，与32位技术专家相约第十七届 D2！](https://mp.weixin.qq.com/s/xFeWpkZcRHQygmORAuHkFw "3D/XR、自研 SwiftUI、Lynx、QUIC、边缘计算、Flutter 等话题集结，与32位技术专家相约第十七届 D2！")。

因为是付费活动，所以整体的会议质量和讨论氛围都会好很多。如果你对议题感兴趣可以付费购买门票或者在上面那篇文章底部留言获取门票抽取资格。

## 本周学习

整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)
#### Xcode 僵尸对象 Zombie Objects

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

1、[源码探索SwiftUI框架—TCA](https://juejin.cn/post/7164699554711863326 "源码探索SwiftUI框架—TCA") -- 来自：合合信息

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：本文将会详细的带你体验 TCA 框架该如何去使用，从定义、绑定到调用，并从源码探析整个流程的逻辑，清晰易懂。同时 TCA 也还在快速的发展和推进中，可以期待 TCA 的完善。

2、[《游戏学导论》- 笔记](http://pjhubs.com/2022/01/29/game05/ "《游戏学导论》- 笔记") -- 来自：PJHubs

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：这是一份博主学习华科熊硕老师的《游戏学导论》的系列笔记文章，主要讨论了游戏作为人文社会的一部分中，人与游戏之间的关系和理解，感兴趣的朋友可以读一下。

3、[GCDWebServer 使用详解](https://xiaovv.me/2018/11/30/GCDWebServer-BasicUse/ "GCDWebServer 使用详解") -- 来自：笑忘书店

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：GCDWebServer 是一个基于 GCD 的轻量级服务器框架，使用 GCDWebServer 我们可以很轻松的在我们的应用中搭建一个 HTTP 服务器，比如可以使用 GCDWebServer 来实现一个无线U盘 App。该篇文章比较详细的讲解了这个框架的主要使用流程，有两种语言的实现，代码内容详实。

4、[SwiftOnTap](https://swiftontap.com/ "SwiftOnTap") -- 来自：SwiftOnTap

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：这是一份看起来很像官方文档，但是又比官方文档详细很多的 SwiftUI 文档，由一些 iOS 开发者一起维护，将一些在官方文档上写的不清楚、不详细的地方重新编写，填补了 Apple 文档的一些漏洞，其中各种 UI 类的实现还有动画和图片作为辅佐，很好用。

5、[What is the difference between #available and @available](https://sarunw.com/posts/available-vs-available/ "What is the difference between #available and @available") -- 来自：Sarunw

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：本文主要讨论了 # 和 @ 在 Swift 代码中的不同的意义。

6、[iOS APP添加桌面快捷方式](https://mp.weixin.qq.com/s/z_CfthCni7m1mKtM0KzH6g) -- 来自：搜狐技术产品

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：本文记录了实现添加桌面快捷方式的一些实现，给出了两个具体的方案，同时也分析了两个方案的利弊。




## 摸一下鱼

整理编辑：[zhangferry](zhangferry.com)

1、[【深度解读】喧嚣过后，再来聊聊灵动岛](https://www.bilibili.com/video/BV1W14y1N7MY "【深度解读】喧嚣过后，再来聊聊灵动岛")：这是ZEALER官方频道的一期视频，作者从 Apple 的开发者文档和UI交互的深层用意两方面去考虑灵动岛的设计意图。灵动岛的主要作用是「补上了iOS高频更新信息管理缺失的一环」，由此也延伸出了几个观点：

* 微信消息不可能适配灵动岛
* 灵动岛未来不会成为多任务的入口

2、[Hello 算法](https://www.hello-algo.com/ "Hello 算法")：「如果您是 **算法初学者**，完全没有接触过算法，或者已经有少量刷题，对数据结构与算法有朦胧的理解，在会与不会之间反复横跳，那么这本书就是为您而写！」这本书第一作者是 Krahets，力扣全网阅读量最高博主。 他曾经求职也踩过算法的雷，于是就有了后来的发愤图强，并写作这本面相初学者的算法小书。

![](https://cdn.zhangferry.com/Images/20221216000024.png)

3、[那些独立开发者（非外包）都是怎么养活自己的](https://www.v2ex.com/t/900741 "哪些独立开发者都是怎么养活自己的")：来自 V2EX 上的一个帖子，评论区有很多独立开发者的项目。我们可以发现一些有趣的独立项目，同时也能看到一些独立开发者的生活状态，这条路不那么容易走。如果你向往独立开发的话，也可以了解他们遇到的问题。

4、[新冠病毒感染者居家预防治疗指南](https://docs.qq.com/doc/DTVZTdENJbnhWaFpQ "新冠病毒感染者居家预防治疗指南")：随着防疫政策的放开，身边有越来越多的人🐑了，🐑了该如何应对？这份在线文档综合多份机构的新冠治疗指南汇总制作而成，比如什么症状应该用什么药？跟自己同住的人应该如何防护？如何消杀？儿童、孕妇被感染应该如何处理？去医院就诊应该注意什么情况？另外还提供了很多中医和饮食相关的注意事项。


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #78 | iOS 摸鱼周报 #78 | 用 ChatGPT 做点好玩的](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/UmXvtKYS6Z0a30yPRyIV9g)

[iOS 摸鱼周报 #75 | 远程工作推行之难](https://mp.weixin.qq.com/s/nguqKvkuzDBR9o-Yw6y3KQ)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
