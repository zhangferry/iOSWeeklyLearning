iOS 摸鱼周报 52 | 如何规划个人发展

![](http://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题



## 面试解析

整理编辑：[JY](https://juejin.cn/user/1574156380931144)



## 优秀博客

整理编辑：皮拉夫大王在此

> 本期博客主题：iOS内存。如果你对以下几个问题不了解的话，推荐阅读本期的博客。
> - 什么是MMU?什么是clean/dirty/compressed memory？
> - 申请malloc(1)，malloc_size是多少？
> - 小内存释放，内存会立即还给系统吗？
> - TCMalloc 主要解决什么问题？

1. [iOS Memory 内存详解 (长文)](https://juejin.cn/post/6844903902169710600#heading-2 "iOS Memory 内存详解 (长文)") -- 来自掘金：RickeyBoy

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：本文主要介绍了iOS 内存相关的基础知识，可以帮助读者建立内存知识全景图。我们可以带着问题去阅读这篇文章：（1）、虚拟内存是如何映射到物理内存的？（2）、clean/dirty memory是如何区分的？一块dirty memory的单位大小是多少？

2. [深入理解内存分配](https://sq.sf.163.com/blog/article/178605610527186944 "深入理解内存分配") -- 来自网易数帆：阿凡达

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：内存分配的硬核文章，内容很有意思。通过阅读这篇文章，首先我们会了解free的过程，顺带也就能理解作者举的例子：str[0]='a'报错非bad_access的原因了。另外作者列举了多种替换系统默认内存分配方式，这也是比较有意思的一点。

3. [Matrix-iOS 内存监控](https://cloud.tencent.com/developer/article/1427932 "Matrix-iOS 内存监控") -- 来自腾讯云：微信终端团队

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：来自微信的matrix 内存监控原理介绍工具，能够抓取每个对象生成时的堆栈。与OOMDetector的原理一致，但是性能上更胜一筹。如此大量且高频的堆栈抓取和保存，matrix是如何做优化的？可以通过阅读本文来了解细节。

4. [TCMalloc解密](https://wallenwang.com/2018/11/tcmalloc/ "TCMalloc解密") -- 来自：Wallen's Blog

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：对《深入理解内存分配》中提到的TCMalloc感兴趣的可以继续阅读这篇文章。


## 见闻

> 这一周阅读/浏览到的有趣的资讯。

1、[Mac 与游戏无缘，M1 来了也没用](https://mp.weixin.qq.com/s/z10cepyRBFVPql52Ym1m0g) -- 来自公众号：APPSO

[@远恒之义](https://github.com/eternaljust)：提到游戏，具体到 PC 端的游戏，Mac 电脑基本是沾不上边的。传统意义上的 PC 游戏，指的是在 Windows 电脑上玩的游戏，Mac 电脑只是一个生产力工具。我曾下载过战网客户端，在 Mac 上玩暴雪游戏《炉石传说》，但这样原生支持 Mac 平台的厂商并不多。我也用过腾讯 START 云游戏，对网络要求很高，在 MacBook 上玩《英雄联盟》，打团时的延迟尚能接受。最近拿 PS5 手柄在 iPad 上试玩 Arcade 游戏，游戏体验还不错，也能兼容 Mac 平台。那么，为什么 Mac 距离主流游戏市场这么远呢？M1 芯片的到来，能给 Mac 游戏带来新的机遇吗？作者在文中给出了答案。

2、[对 iPod 说再见，我想带你走进无数人的「青春记忆」](https://sspai.com/post/73225 "对 iPod 说再见，我想带你走进无数人的「青春记忆」") -- 来自少数派：宛潼

[@远恒之义](https://github.com/eternaljust)：停产了，售罄了，下架了，拥有 20 年寿命的 iPod，走到了生命的终点。作为一款音乐播放器，iPod 的产品线十分丰富。无论是初代经典 iPod Classic，还是短暂尝试的 iPod mini，还有被用户吐槽最多的 iPod shuffle，多次探索新形态、新功能和新技术的 iPod nano，功能强大的 iPod touch，这些都已成为了历史，让人怀恋。拥有过 iPod 的你，是否也有「爷青结」的感叹呢。就让本文的作者带你一起了解 iPod 相关的彩蛋产品，唤起你的「青春记忆」吧。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### CotEditor

**地址**：https://coteditor.com/

**软件状态**：免费

**软件介绍**：

适用于 `macOS` 的纯文本编辑器，轻巧、整洁并且功能强大。

![CotEditor](http://cdn.zhangferry.com/screenshot@2x.png)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #51 | 游戏版号恢复发放](https://mp.weixin.qq.com/s/ogjhELipiVFRaYJkT2NQwA)

[iOS 摸鱼周报 第五十期](https://mp.weixin.qq.com/s/6IS0RlytWxjeRHyh0f2fXA)

[iOS 摸鱼周报 第四十九期](https://mp.weixin.qq.com/s/6GvVh8_CJmsm1dp-CfIRvw)

[iOS摸鱼周报 第四十八期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](http://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
