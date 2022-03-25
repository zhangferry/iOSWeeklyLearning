# iOS 摸鱼周报 第四十八期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：node-ipc 供应链投毒事件
> * 面试模块：OC 对象弱引用指针标识位
> * 优秀博客：程序员如何自我提升
> * 学习资料：以 Java 为背景的全栈知识体系
> * 开发工具：新一代卡片笔记工具：flomo

## 本期话题

[@zhangferry](https://zhangferry.com)：这期稍微聊一聊 [「node-ipc 包以反战为名进行供应链投毒」](https://www.zhihu.com/question/522144107/answer/2391166752 "如何看待 node-ipc 包以反战为名进行供应链投毒？")这件事。这件事的原委是这样的，[node-ipc](https://github.com/RIAEvangelist/node-ipc "node-ipc")  是 npm 下的一个组件（iOS 开发可以将其理解为 CocoaPods 下的一个组件），其作者为了表达反战宣言，在该组件库里注入了恶意脚本，往用户的桌面和 OneDrive 里写一个文件，用于表达自己的政治观点。供应链的含义是你发布的软件所依赖的三方库、系统库、开发工具等组成的依赖链，你的软件属于其中一环，它受以上所有环节的影响。而供应链投毒的含义是，只要依赖链里有它，就会中招，其中就包括使用很广泛的 vue-cli 。

当前国内 nmp 镜像已经将 node-ipc 列入黑名单，该作者推特也遭黑客攻击，个人信息被人肉。

这件事算是结束了，但也暴露出开源社区的脆弱，谴责该作者之时，「**我们需要建立一种开源世界的反分裂共识**」，开源社区的规则不应该被政治因素打破。

## 面试解析

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### OC 对象如何知道存在关联的弱引用指针

我们都知道在释放对象之前会检查是否存在弱引用指针， 而判断 OC 对象存在弱引用的依据是什么呢？

如果卷过八股文，肯定了解 `isa` 优化过后使用了 `union`存储更多的数据，其中有一个 `bit:weakly_referenced`是和弱引用指针相关的。

在弱引用对象创建成功后，会去设置该位的值为 1。结构如下：

```cpp
#     define ISA_BITFIELD                                                      \
        uintptr_t nonpointer        : 1;                                       \
        uintptr_t has_assoc         : 1;                                       \
        uintptr_t has_cxx_dtor      : 1;                                       \
        uintptr_t shiftcls          : 33; /*MACH_VM_MAX_ADDRESS 0x1000000000*/ \
        uintptr_t magic             : 6;                                       \
        uintptr_t weakly_referenced : 1;                                       \
        uintptr_t unused            : 1;                                       \
        uintptr_t has_sidetable_rc  : 1;                                       \
        uintptr_t extra_rc          : 19
```

但是未优化的 `isa`存储的是类对象的内存地址，不能存储弱引用信息， 那么它关联的弱引用信息应该存储在哪？答案是 **引用计数表**。

在学习内存管理 `release & retain`流程时，发现引用计数表都是通过 `SIDE_TABLE_RC_ONE` 进行增减操作的。并未直接获取到引用计数后进行 `+/- 1`。该掩码定义处还给出了其他的定义：

```cpp
#define SIDE_TABLE_WEAKLY_REFERENCED (1UL<<0)
#define SIDE_TABLE_DEALLOCATING      (1UL<<1)  // MSB-ward of weak bit
#define SIDE_TABLE_RC_ONE            (1UL<<2)  // MSB-ward of deallocating bit
```

从定义大概猜到，引用计数表中获取到的数值，从第三位开始是真正的引用计数。第一位是用来表示是否存在弱引用指针的。第二位表示正在析构中。

我们在 `weak`创建流程中的关键函数 `storeWeak`中可以证实这一点，该函数在操作完弱引用表之后， 会设置对象的相关弱引用标识位，具体函数是`setWeaklyReferenced_nolock `

```c
inline void
objc_object::setWeaklyReferenced_nolock()
{
    isa_t newisa, oldisa = LoadExclusive(&isa.bits);
    do {
        newisa = oldisa;
        // 未优化的 isa
        if (slowpath(!newisa.nonpointer)) {
            ClearExclusive(&isa.bits);
            sidetable_setWeaklyReferenced_nolock();
            return;
        }

        // 优化过的 isa
        if (newisa.weakly_referenced) {
            ClearExclusive(&isa.bits);
            return;
        }
        newisa.weakly_referenced = true;
    } while (slowpath(!StoreExclusive(&isa.bits, &oldisa.bits, newisa.bits)));
}

// 引用技术表中设置标识位
void
objc_object::sidetable_setWeaklyReferenced_nolock()
{
#if SUPPORT_NONPOINTER_ISA
    ASSERT(!isa.nonpointer);
#endif

    SideTable& table = SideTables()[this];

    table.refcnts[this] |= SIDE_TABLE_WEAKLY_REFERENCED;
}
```

`setWeaklyReferenced_nolock `判断如果是优化过的 `isa` 直接设置对应的 `weakly_referenced = 1` 。

如果是非优化的 `isa`，则通过查找引用计数表设置对应的位置为 1。

在对象释放过程中，查找对象关联弱引用的逻辑具体实现在 `objc_object::clearDeallocating()`中，如果判断是优化后 `isa`则调用 `clearDeallocating_slow`查找 `isa.weakly_referenced`；如果是未优化 `isa` 则调用 `objc_object::sidetable_clearDeallocating()`查找，可自行查看。

另外关于 swift 弱引用可以学习 [周报四十五期](https://mp.weixin.qq.com/s/_N98ADlfQCUkxYjmH0SvZw)

## 优秀博客

整理编辑：[@我是熊大](https://github.com/Tliens)

> 本期优秀博客的主题为：程序员如何自我提升。学习前辈们的经验，找到适合自己的路径。

1、[程序员如何在业余时间提升自己](https://juejin.cn/post/6995079191548936223 "程序员如何在业余时间提升自己") -- 来自掘金：阿里巴巴大淘宝技术

[@我是熊大](https://github.com/Tliens)：工作本身就很忙碌，如何在繁忙的工作中利用碎片化时间学习或是做自己感兴趣的事情，来自4名淘系技术的工程师的分享。

2、[阿里毕玄：程序员如何提升自己的硬实力](https://segmentfault.com/a/1190000018005178 "阿里毕玄：程序员如何提升自己的硬实力") -- 来自segmentfault：阿里云云栖号

[@我是熊大](https://github.com/Tliens)：作者从生物专业转到程序员，从业余程序员到职业程序员。

3、[如何提升你的能力？给年轻程序员的几条建议](https://tech.glowing.com/cn/advices-to-junior-developers "如何提升你的能力？给年轻程序员的几条建议") -- 来自Glow 技术团队博客

[@我是熊大](https://github.com/Tliens)：作者前后服务于NVIDIA、Google、Slide、Glow。在Glow，作者的个人的工作也从Developer，Tech Lead，Engineering Manager到CTO，他的看法可能会更全面。

4、[程序员一定会有35岁危机吗](https://juejin.cn/post/7012542827204706318 "程序员一定会有35岁危机吗") -- 来自掘金：黄轶

[@我是熊大](https://github.com/Tliens)：一个资深架构师的分享，正如他所说，企业并不是排斥大龄程序员，而是排斥能力与自己工龄不匹配的大龄程序员。

## 见闻

> 这一周阅读/浏览到的有趣的资讯。

1、[开源世界里的法律与政治](https://zhuangbiaowei.github.io/opensource/2022/03/07/law-and-politics-in-an-open-source-world.html "开源世界里的法律与政治") -- 来自博客：庄表伟

[@zhangferry](zhangferry.com)：文中有两个观点值得思考：

* 如果这个世界可能被割裂，无论代码仓库放在哪里，整个世界都会受到伤害。所以关键不是**自己也搞一个**。而是要努力建设不会被**割裂**的开源世界。

  我不是太认同，我认为自己搞和努力建设更好的开源世界要同时进行，因为前者更可控，为了避免陷入未来两难的境地，还要好好搞。

* 可以在个人账号发表政治观点，但不要代表开源社区，开源社区应该是”非政治“的。

2、[Facebook 工程师文化独特之处](https://chinese.catchen.me/2022/02/unique-engineering-culture-of-facebook.html "Facebook 工程师文化独特之处") -- 来自博客：Cat in Chinese

[@zhangferry](zhangferry.com)：作者讲述了他在 Facebook 工作 7 年 体会到的 Facebook 与其他公司的区别。

* 工程师要对产品结果负责。把技术做到极致是不够的，产品完成指定目标才行。可能很多人会感觉奇怪，但这样能部门上下目标一致，不会出现甩锅的情况。
* 基础架构被视为内部产品。比如某个部门产出了一个新的服务，你不能强行推进大家使用，而应把它当做一个产品，只不过用户是内部用户。这其中工程师还需要兼做销售和客服的工作。当初 React 和 React Native 早期就是经历了很多推广困难才得以成功。
* 救火比防火更容易获得回报。这个是缺点，因为完全的数据驱动，这导致防御性措施很难吸引人去做，因为成功阻止了坏事发生时你没办法收集数据说你成功阻止了多少件坏事，而对于解决问题你可以明确的列出指标。

3、[超越心流](https://www.xiaoyuzhoufm.com/episode/622edc14733d1b3a64340130?s=eyJ1IjogIjYwYTIwMzM3ZTBmNWU3MjNiYjYxZTc5ZiJ9 "超越心流") -- 来自播客：不可理喻

[@zhangferry](zhangferry.com)：「心流（Flow）」由心理学家米哈里-契克森米哈赖提出，它描述的是当一个人全神贯注的投入一件事情的时候，他全部的精神能量都专注于实现这个目标，心灵状态达到了一种最纯粹的、最优化的、最忘我的状态。「心流」代表着一种最优体验，它应该是我们追求的状态，但它非常依赖注意力，如何才能超越心流呢，作者结合了多个例子进行说明。

其中提到 [The Well-Played Game](https://mitpress.mit.edu/books/well-played-game "The Well-Played Game") 的作者对于真正的乐趣和纯粹的玩的定义，有几个标准：

* 人要不断的制造惊喜，制造幽默感，哪怕你在做一个重复的无趣的事情。除了务实的你，还要有一个调皮捣蛋，不断给出惊喜，带着玩乐心态的自己。（这一条跟我某些体验比较像）
* 要有玩的集体感，不要有竞争感和情绪化，而是考虑大家一起创造的游戏体验。
* 好好的去玩，要介于有目的性和无目的性之间，既要领悟，还要有神秘感。

但理论毕竟是理论，个体感受是复杂的，很难定义标准，我们还应该结合自己的方式体会生活的快乐。

4、[【亦】唠唠苹果 M1 Ultra：半导体新时代！](https://www.bilibili.com/video/BV1jS4y1g7xw "【亦】唠唠苹果M1 Ultra：半导体新时代！") -- 来自BiliBili：林亦LYi

[@zhangferry](zhangferry.com)：不同于 M1 Ultra 的芯片测评，这期节目更多讲的是 M1 Ultra 的出现对半导体行业的影响。半导体行业有摩尔定律：当价格不变时，集成电路上可容纳的晶体管数目，约每隔 18 个月便会增加一倍，性能也将提升一倍。芯片制程从 5nm 到 3nm，摩尔定律还在生效，但它的物理极限也快到了。M1 Ultra 使用新一代缝合技术，在制程不变的情况下，靠两个芯片的拼接就完成了性能翻倍。而且这玩意可没有物理极限，这种依靠「缝合」技术来让性能翻倍带来的则是「摩尔定律 2.0 时代」。

还有一点很有趣的地方，苹果对于 UltraFusion 的专利描述如下：

![img](https://cdn.nlark.com/yuque/0/2022/png/2215058/1648133857555-8401b605-89bb-4d72-8d81-76de49f98603.png)

在晶圆上排满 M1 Max 晶片，把相邻且联通达标的晶片找出来搭建信号通道，连上之后切割，作为M1 Ultra。对于跨电路通信有问题的晶片就单独拆成 M1 Max 来卖，M1 Max 来很复杂，万一也做坏了，可以横着来一刀变成 M1 Pro。M1 Pro 虽然没法再砍一刀变成 M1，但芯片里的 CPU、GPU 等还都可以复用到 M1 上（知道为啥 iPad 也上 M1 了吧。。） 。不得不说，苹果的这套设计确实强，这样不仅使得芯片造出来的良品很多，而且各种边角料都能复用，最大限度平摊芯片制造成本。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Java 全栈知识体系

**地址**：https://pdai.tech/

以 Java 开发为背景的全栈开发知识体系，内容包含软件开发、算法、面试、架构、项目、产品团队以及一些方法论的思考。站内资源海量详实，文章和网站的排版和设计很规范，阅读起来非常舒适，也多有漂亮的示意图来帮助读者理解，内容非常丰富。关于这个网站的建立初衷以及介绍可以看[这里](https://pdai.tech/md/about/me/about-me.html#q2---%E5%81%9A%E8%BF%99%E4%B8%AA%E7%BD%91%E7%AB%99%E7%9A%84%E5%88%9D%E8%A1%B7%E6%98%AF%E4%BB%80%E4%B9%88 "Java 全栈知识体系建设初衷")。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### flomo

**地址**：https://flomoapp.com/

**软件状态**：免费

**软件介绍**：

 `flomo` 是新一代卡片笔记工具，秉承尼克拉斯 · 卢曼（Niklas Luhmann）的卡片笔记法理念，让你能更好的利用碎片时间积累知识，建立知识间的关联。

![flomo](https://files.mdnice.com/user/15579/203f041f-a6ec-4d0a-af5b-599a579225c1.png)

### MoneyProgress

**地址**：https://github.com/Lakr233/MoneyProgress

**软件状态**：免费

**软件介绍**：

老王的又一力作：钱条。

> 上班的进度条，开始搬砖吧。

![MoneyProgress](https://files.mdnice.com/user/15579/65fa2fe0-11ad-4a00-9d5f-4007ebb2edab.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS 成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第四十七期](https://mp.weixin.qq.com/s/X6lPQ5qwY1epF6fEUhvCpQ)

[iOS摸鱼周报 第四十六期](https://mp.weixin.qq.com/s/8Wpfk9yxpjwaDXN7iXIcvQ)

[iOS摸鱼周报 第四十五期](https://mp.weixin.qq.com/s/_N98ADlfQCUkxYjmH0SvZw)

[iOS摸鱼周报 第四十四期](https://mp.weixin.qq.com/s/q__-veuaUZAK6xGQFxzsEg)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
