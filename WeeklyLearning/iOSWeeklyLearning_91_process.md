# iOS 摸鱼周报 #90

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

![](https://cdn.zhangferry.com/Images/85-ios16-ipados16.png)

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

推荐近期的一些优秀博文，涵盖：App Clip、CloudKit、Swift ABI 稳定性等方面的内容。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[苹果的产品经理设计的 App Clip 是有意为之，还是必然趋势，详解 App Clip 技术之谜](https://juejin.cn/post/7219889814116024380 "苹果的产品经理设计的 App Clip 是有意为之，还是必然趋势，详解 App Clip 技术之谜") -- 作者：会飞的金鱼

[@东坡肘子](https://www.fatbobman.com/): 该文介绍了 PWA、微信小程序和 Clip 应用，并进行了比较。作者认为，在特定的线下场景中，Clip 应用具有相当好的用户体验。虽然 PWA 看起来很美好，但实际上更多是 web 开发者的美好愿景。总的来说，Clip 应用和小程序并不是直接竞争关系，而是在特定场景下对小程序原生能力不足的一种补充。此文拥有本栏目创建以来所推荐文章的最长标题。

2、[我在编写自己的 CloudKit 同步库时学到的东西](https://ryanashcraft.com/what-i-learned-writing-my-own-cloudkit-sync-library/ "我在编写自己的 CloudKit 同步库时学到的东西") -- 作者：Ryan Ashcraft

[@东坡肘子](https://www.fatbobman.com/): 几年之前，还有一些第三方库使用 CloudKit 服务来实现 Core Data 数据的云存储和同步功能。这种情况在苹果推出 Core Data with CloudKit 后就基本停止了，这些库也不再更新。Ryan Ashcraft 则认为官方的解决方案仍无法满足他的需求，为此，重新开发了 CloudSyncSession 库。本文分享了作者创建 CloudSyncSession 的经验。涵盖了 CloudKit 同步的基本概念，预防和处理错误的方法，冲突解决，模式设计以及其他建议。即使你不打算使用该库，仅阅读它的代码也将让你对 CloudKit 的运作机制有更多的认识。

3、[Swift 最佳实践之 Generics](https://juejin.cn/post/7219908995338731575 "Swift 最佳实践之 Generics") -- 作者：峰之巅

[@东坡肘子](https://www.fatbobman.com/): 本文探讨了 Swift 中的泛型，包括泛型类型约束和泛型特化，这些都是 Swift 中非常重要的概念。虽然泛型能够提高代码的复用性，但也可能对性能产生影响，因此需要通过泛型特化来优化代码。此外，本文还介绍了 Phantom Types 的概念和用法，这是一种非常有用的编程技巧，可以帮助开发者更好地利用 Swift 的类型系统。在文章的最后，还讨论了一些与泛型相关的小问题，例如泛型方法参数不应定义为 Optional，以及在 Swift 5.7 中无法将任意类型的实例作为泛型参数等问题。

4、[什么时候我可以称自己为高级开发人员？](https://www.kodeco.com/38327766-when-can-i-call-myself-a-senior-developer "什么时候我可以称自己为高级开发人员？") -- 作者：Renan Benatti Dias

[@东坡肘子](https://www.fatbobman.com/): 尽管 Renan Benatti Dias 认为自己有资格担任高级职位，但他仍在中级开发岗位停留了不短的时间。为此，他花了很多时间思考成为高级开发人员需要什么，以及如何为此做好准备。在明确并掌握了需要能和责任后，他最终实现了理想。在本文中，他概述了高级开发人员所需的必要技能和经验，并提供了一些其他建议，例如建立扎实的技术基础、提升软技能、在公司内寻找机会等。

5、[Swift ABI 稳定性探究](https://juejin.cn/post/7223045442891284540 "Swift ABI 稳定性探究") -- 作者：姚亚杰 货拉拉出行研发部-架构组

[@东坡肘子](https://www.fatbobman.com/): 本文的灵感来源于一个 Bug，通过对 Bug 进行分析和排查，作者介绍了 Swift 5.1 的模块稳定性和库进化特性。其中，模块稳定性通过存储模块信息的 swiftinterface 文件格式来实现，而库进化则通过开启 Library Evolution 特性来实现。在文章最后，还指出了开启 Library Evolution 特性后需要注意与 Objective-C 互操作性的问题。

## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
