# iOS摸鱼周报 第十八期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 本期话题

[@zhangferry](https://zhangferry.com)：最近在看一本书《暗时间》，初听这个名字有点一头雾水，但是读了[那篇文章](http://mindhacks.cn/2009/12/20/dark-time/ "暗时间")了解这个概念之后，多少还是受到了一些震撼。

> 有时我们看了很多书却不见得有太多成长，通常是由于并没有领悟和运用起来书中的知识。要达到深入理解的程度是需要靠不断的推理和验证的，而这个过程就是你的思维时间，也即是“暗时间”。走路，做公交，吃饭，睡觉，这些都可以成为暗时间，条件就是你利用这段时间进行思考，反刍和消化看到的东西，日积月累会产生庞大的效应。

这里的暗时间，通常也就是碎片时间，大多数情况，他们都是未被利用的。但未被利用并不代表其不可利用，再考虑每个人使用时间的效率不一致，所以认为时间对每个人是均等的是一个错觉，认为别人有一天，我也有一天，其实根本不是这样。我们应该算的是投入时间和效率的乘积。

3、计算机里不同线程间的切换是有时间开销的，大脑也类似，所以专注的人总能拥有更高的效率。

4、能够迅速进入专注状态，以及能够长期保持专注状态，是高效学习的两个最重要习惯。

5、抗干扰能力是非常重要的一个习惯，只有具备这种能力，才能更有效的利用不同的暗时间。

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### UICollectionViewFlowLayout 的 scrollDirection 在 vertical 和 Horizontal 下的 item 布局顺序以及 minimumLineSpacing、minimumInteritemSpacing 的区别：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/8618ec82225e46df6702b5e13145b334.png)
![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/a2c7e0462462f88c6a0154edef46ccf6.png)


## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`编译优化`

1、[iOS 微信编译速度优化分享](https://cloud.tencent.com/developer/article/1564372 "iOS 微信编译速度优化分享") -- 来自云+社区：微信终端开发团队

文章对编译优化由浅入深做了介绍。作者首先介绍了常见的现有方案，利用现有方案以及精简代码、将模板基类改为虚基类、使用PCH等方案做了部分优化。文章精彩的部分在于作者并没有止步于此，而是从编译原理入手，结合量化手段，分析出编译耗时的瓶颈。在找到问题的瓶颈后，作者尝试人工进行优化，但是效率较低。最终在 IWYU 基础上，增加了 ObjC 语言的支持，高效地处理了一部分多余的头文件。

2、[iOS编译速度如何稳定提高10倍以上之一](https://juejin.cn/post/6903407900006449160 "iOS编译速度如何稳定提高10倍以上之一") -- 来自掘金：Mr_Coder

美柚iOS的编译提效历程。作者对常见的优化做了分析，列举了各自的优缺点。有想做编译优化的可以参考这篇文章了解一下。业界的主流技术方案别的技术文章往往只介绍优点，对方案的缺点谈的不够彻底。这篇文章从实践者的角度阐述了常见方案的优缺点，很有参考价值。文章介绍了双私有源二进制组件并与ccache做了对比，最后列出了方案支持的功能点。

3、[iOS编译速度如何稳定提高10倍以上之二](https://juejin.cn/post/6903408514778497031 "iOS编译速度如何稳定提高10倍以上之二") -- 来自掘金：Mr_Coder

作为上文文章的姊妹篇，本文详细介绍了双私有源二进制组件的方案细节以及使用方法。对方案感兴趣的可以关注下。

4、[一款可以让大型iOS工程编译速度提升50%的工具](https://tech.meituan.com/2021/02/25/cocoapods-hmap-prebuilt.html "一款可以让大型iOS工程编译速度提升50%的工具") -- 来自美团技术团队：思琦 旭陶 霜叶

本文主要介绍了如何通过优化头文件搜索机制来实现编译提速，全源码编译效率提升45%。文中涉及很多知识点，比如hmap文件的作用、Build Phases - Headers 中的Public，Private，Project 各自是什么作用。文中详细分析了podspec创建头文件产物的逻辑以及Use Header Map 失效的原因。干货比较多，可能得多读几遍。

5、[Xcode编译疾如风系列 - 分析编译耗时](https://cloud.tencent.com/developer/article/1817236 "Xcode编译疾如风系列 - 分析编译耗时") -- 来自腾讯社区：小菜与老鸟

在进行编译速度优化前，一个合适的分析工具是必要的，它能告诉你哪部分编译时长较多，让你发现问题，从而解决问题，本文介绍了几种分析编译耗时的方式，助你分析构建时间。该作者还有其他相关姊妹篇，建议前往阅读。

6、[iOS编译过程的原理和应用](https://blog.csdn.net/Hello_Hwc/article/details/53557308 "iOS编译过程的原理和应用") -- 来自CSDN：黄文臣

做编译优化前，先了解下编译原理吧！该作者通过iOS的视角，白话了编译原理，通俗易懂。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 从 0 到 1 设计一台计算机

地址：https://www.bilibili.com/video/BV1wi4y157D3

来自 [Ele实验室](https://space.bilibili.com/481434238) 的计算机组成原理课程，该系列视频主要目的是让大家对「计算机是如何工作的」有个较直观的认识，做为深入学习计算机科学的一个启蒙。观看该系列视频最好有一些数字电路和模拟电路的基础知识，Ele实验室同时也有关于[数电](https://www.bilibili.com/video/BV1Hi4y1t7zY)和[模电](https://www.bilibili.com/video/BV1774114798)的基础知识介绍供大家参考。

### Git Cheat Sheet 中文版

地址：https://github.com/flyhigher139/Git-Cheat-Sheet

Git Cheat Sheet 让你不用再去记所有的 git 命令！对新手友好，可以用于查阅简单的 git 命令。

### 正则表达式 30 分钟入门教程

地址：https://deerchao.cn/tutorials/regex/regex.htm

30 分钟内让你明白正则表达式是什么，并对它有一些基本的了解。别被那些复杂的表达式吓倒，只要跟着我一步一步来，你会发现正则表达式其实并没有想像中的那么困难。除了作为入门教程之外，本文还试图成为可以在日常工作中使用的正则表达式语法参考手册。

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

### SnippetsLab

**地址**：http://www.renfei.org/snippets-lab/

**软件状态**：$9.99

**软件介绍**：

一款强大的代码片段管理工具，从此告别手动复制粘贴，SnippetsLab 的设计更符合Apple 的交互习惯，支持导航栏快速操作。另外还可以同步 Github Gist 内容，使用iCloud 备份。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210710232333.png)

### CodeExpander

**地址**：https://codeexpander.com/

**软件状态**：普通版免费，高级版付费

**软件介绍**：

专为开发者开发的一个集输入增强、代码片段管理工具，支持跨平台，支持云同步（Github/码云）。免费版包含 90% 左右功能，相对 SnippetsLab 来说其适用范围更广泛，甚至包括一些日常文本的片段处理。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210710231521.png)



## 联系我们

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)