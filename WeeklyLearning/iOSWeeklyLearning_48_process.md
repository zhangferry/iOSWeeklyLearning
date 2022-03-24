# iOS 摸鱼周报 第四十二期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * Tips：
> * 面试模块：
> * 优秀博客：程序员如何自我提升
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：这期稍微聊一点 [「node-ipc 包以反战为名进行供应链投毒」](https://www.zhihu.com/question/522144107/answer/2391166752 "如何看待 node-ipc 包以反战为名进行供应链投毒？")这件事。这件事的原委是这样的，[node-ipc](https://github.com/RIAEvangelist/node-ipc "node-ipc")  是 npm 下的一个组件（iOS 开发可以将其理解为 CocoaPods 下的一个组件），其作者为了表达反战宣言，在该组件库里注入了恶意脚本，往用户的桌面和 OneDrive 里写一个文件，用于表达自己的政治观点。供应链的含义是你发布的软件所依赖的三方库、系统库、开发工具等组成的依赖链，你的软件属于其中一环，它受以上所有环节的影响。而供应链投毒的含义是，只要依赖链里有它，就会中招，其中就包括使用很广泛的 vue-cli 。

当前国内 nmp 镜像已经将 node-ipc 列入黑名单，该作者推特也遭黑客攻击，个人信息被人肉。

这件事算是结束了，但也暴露出开源社区的脆弱，谴责该作者之时，「**我们需要建立一种开源世界的反分裂共识**」，开源社区的规则不应该被政治因素打破。

## 开发 Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

## 优秀博客


整理编辑：[@我是熊大](https://github.com/Tliens)

> 本期优秀博客的主题为：程序员如何自我提升。学习前辈们的经验，找到适合自己的路径。

1、[程序员如何在业余时间提升自己](https://juejin.cn/post/6995079191548936223 "程序员如何在业余时间提升自己") -- 来自掘金：阿里巴巴大淘宝技术

[@我是熊大](https://github.com/Tliens)：工作本身就很忙碌，如何在繁忙的工作中利用碎片化时间学习或是做自己感兴趣的事情，来自4名淘系技术的工程师的分享。

2、[阿里毕玄：程序员如何提升自己的硬实力](https://segmentfault.com/a/1190000018005178 "阿里毕玄：程序员如何提升自己的硬实力") -- 来自segmentfault：阿里云云栖号

[@我是熊大](https://github.com/Tliens)：作者从生物专业转到程序员，从业余程序员到职业程序员。

3、[如何提升你的能力？给年轻程序员的几条建议](https://tech.glowing.com/cn/advices-to-junior-developers "如何提升你的能力？给年轻程序员的几条建议") -- 来自Glow 技术团队博客

[@我是熊大](https://github.com/Tliens)：作者前后服务于NVIDIA、Google、Slide、Glow。在Glow，作者的个人的工作也从Developer，Tech Lead，Engineering Manager到CTO，他的看法可能会更全面。

4、[程序员一定会有35岁危机吗](https://juejin.cn/post/6948239939809050638 "程序员一定会有35岁危机吗") -- 来自掘金：黄轶

[@我是熊大](https://github.com/Tliens)：一个资深架构师的分享，正如他所说，企业并不是排斥大龄程序员，而是排斥能力与自己工龄不匹配的大龄程序员。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

## 见闻

> 这一周阅读或者观看到的有趣的讯息。

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

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### flomo

**地址**：https://flomoapp.com/

**软件状态**：免费

**软件介绍**：

 `flomo` 是新一代卡片笔记工具，秉承尼克拉斯 · 卢曼（Niklas Luhmann）的卡片笔记法理念，让你能更好的利用碎片时间积累知识，建立知识间的关联。

![flomo](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/pic_feature_product.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS 成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
