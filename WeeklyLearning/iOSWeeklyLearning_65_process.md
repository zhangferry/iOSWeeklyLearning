# iOS 摸鱼周报 #59

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：
> * 岗位推荐：

## 本期话题

### App Accelerator

近期有两场分享：

* 设计卓越的桌面级 iPad App，8 月 22 号。iPadOS 16 有一项重要更新就是对桌面级应用的支持，这样改动会为 iPad 生态带来哪些改变还不确定。如果对这方面内容感兴趣可以报名这场分享，该次分享会通过 Apple 在搜索、导航栏、编辑菜单、多选等功能当中的一系列改进，来介绍如何在 iPad 上设计出桌面级的 App。
* 了解和消除 App 的卡顿，8 月 25 号。本次分享会讲解通过 Xcode 14 提供的新能力发现卡顿及其相关原因的工具和方法，以及 App 卡顿的一些反面典型，学习避免这些卡顿的最佳实践。


### 精准测试

在讲精准测试之前先来了解下传统的测试流程，传统测试流程会有黑盒测试、白盒测试，白盒测试会更精准一些，因为它是基于已知逻辑编写的测试用例。但白盒测试有个问题是它没有代码概念，每次回归都需要跑全量用例，随着项目越来越大，测试用例可能会多达上万条。要知道每个版本的修改相对代码总量来说都是比较小的，如果每次都跑全量用例显然是一种浪费，那有没有办法再精准一些，涉及改动的部分才跑对应的用例？有的，这就是精准测试要解决的问题。

精准测试的核心技术就是把用例和代码关联起来，关联的方式是插桩，给每一个执行语句（Basic Block）插上桩，当该语句被执行时创建一个标记记录其执行次数。一个用例执行完的时候，导出插桩内容并解析，我们就可以记录该用例执行代码的覆盖率。覆盖率数据可以用来测量当前用例测试的充分程度，集合增量覆盖率可以更有效的测试MR/版本维度的测试充分程度。

再回到精准测试，当我们拿到覆盖率数据时其实也就拿到了代码与用于之间的映射关系，把这部分数据落入数据库中，根据MR/版本变更代码内容就可以推测出应该执行的用例了，而这部分用例就是我们需要「精准的测试用例」。


## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

> 本期介绍三个着重于报道 Swift 语言发展的电子报以及近期的几篇优秀博文

1、[Swift 周报](https://mp.weixin.qq.com/s/npUMmAzYjzThEjrf0jJ4GQ "Swift 周报") -- 来自：Swift社区

[@东坡肘子](https://www.fatbobman.com/)：由于英文版的 Swift 周报停更，由国内 Swift 爱好者维护的中文版 Swift 周报也停滞了一段时间。从八月开始，中文版 Swift 周报重装上阵，全部内容由周报编辑组自行整理。当前模块分为：新闻、提案、Swift 论坛、推荐博文等。

2、[波报|Pofat 的 Swift 中文电子報](https://pofat.substack.com/archive "波报|Pofat 的 Swift 中文电子報") -- 来自：Pofat

[@东坡肘子](https://www.fatbobman.com/)：Pofat 是一个在苹果生态系打滚多年的 App 工程师，出于对 “工作的表层之下” 有更多了解的渴望，创办了波报，作为他用来探索的手段。当前的内容包括：Swift 和 LLVM 官方消息、Swift 和 LLVM 论坛新鲜事、Swift （或其它相关）的底层原理探讨等内容。

3、[Swift Evolution Monthly](https://se-monthly.flinedev.com/issues/swift-evolution-monthly-first-issue-background-history-chris-lattner-6-proposals-1092625 "Swift Evolution Monthly") -- 来自：Cihat Gündüz

[@东坡肘子](https://www.fatbobman.com/)：由 Cihat Gündüz 于数月前创建的月报，专注于介绍进展中的 Swift 提案。创建该刊物很大的原因也是由于 Swift Weekly Brief 的停刊。

4、[iOS 中的手势传递（一）操作系统层](https://juejin.cn/post/7132069500656517151 "iOS 中的手势传递（一）操作系统层") -- 来自：RickeyBoy

[@东坡肘子](https://www.fatbobman.com/)：通常我们处理手势是在 UIView 层级，直接使用 UIButton、UIGestureRecognizer 等来捕获手势，而本文重点讲的是在此之前，手势识别与传递的过程，在介绍整个过程的同时，也能对整个操作系统的工作方式有一定的了解。

5、[在 SwiftUI 中用 Text 实现图文混排](https://www.fatbobman.com/posts/mixing_text_and_graphics_with_Text_in_SwiftUI/ "在 SwiftUI 中用 Text 实现图文混排") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：SwiftUI 提供了强大的布局能力，不过这些布局操作都是在视图之间进行的。当我们想在 Text 中进行图文混排时，需要采用与视图布局不同的思路与操作方式。本文将首先介绍一些与 Text 有关的知识，并通过一个实际案例，为大家梳理出在 SwiftUI 中用 Text 实现图文混排的思路。

6、[Github 实用小技巧](https://xuanwo.io/reports/2022-32/ "Github 实用小技巧") -- 来自：漩涡

[@东坡肘子](https://www.fatbobman.com/)：漩涡从一个开源项目从业者的角度，介绍了一些他在工作中经常使用的 Github 实用小技巧。包括：引用 Github Issues/PR/Discussion、使用 Fix / Close 来关联一个 Issue、可折叠的区块、Draft / Ready for review、请求 Review、引用回复等内容。

## 摸一下鱼

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

1、介绍两款动态图片生成器，可根据访问地址上携带的参数动态控制返回图片的大小、格式等属性，适合Mock 数据等场景；

- [placeholder](https://placeholder.com/ "placeholder")
- [dummyimage](https://dummyimage.com/ "dummyimage")

2、iOS 16 beta 5



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #56 | WWDC 进行时](https://mp.weixin.qq.com/s/ZyGV6WlFsZOX6Aqgrf1QRQ)

[iOS 摸鱼周报 #55 | WWDC 码上就位](https://mp.weixin.qq.com/s/zDhnOwOiLGJ_Nwxy5NBePw)

[iOS 摸鱼周报 #54 | Apple 辅助功能持续创新](https://mp.weixin.qq.com/s/6jdqa143Y5yr6lbjCuzlqA)

[iOS 摸鱼周报 #53 | 远程办公正在成为趋势](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
