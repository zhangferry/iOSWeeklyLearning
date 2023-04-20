# iOS 摸鱼周报 #91 | 免费的网站托管平台 Vercel

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：线上讲座：探索 Vision 框架；5月9号，App Store定价以美国价格为基准进行更新
> * 内容推荐：推荐近期的一些优秀博文，涵盖：App Clip、CloudKit、Swift ABI 稳定性等方面的内容
> * 摸一下鱼：建了一个交流 AGI 知识的社群；在 Vercel 上部署 ChatGPT 的聊天能力；一个把 AI 拟人化的网站；AI Talk 基于 GPT4 让马斯克和乔布斯进行对话；基于 Apple 健康数据分析的 App HealthGPT

## 本期话题

### [线上讲座：探索 Vision 框架](https://developer.apple.com/events/view/93396BVQ5Y/dashboard "线上讲座：探索 Vision 框架")

[@远恒之义](https://github.com/eternaljust)：Vision 是一款基于 Core ML 封装的图像识别框架，支持人脸检测、文本检测、二维码检测、图像配准和特征追踪等能力。本期讲座将探索学习 Vision 框架在 App 内应用计算机视觉相关的能力，进一步了解如何通过不同的 API 在图片和视频上执行任务。会议时间为 2023 年 5 月 9 日上午 10:00 – 中午 11:00，截止报名时间 2023 年 5 月 8 日前。

### [迎接 5 月 9 日推出的增强全球定价机制](https://developer.apple.com/cn/news/?id=74739es1 "迎接 5 月 9 日推出的增强全球定价机制")

[@远恒之义](https://github.com/eternaljust)：Apple 提醒，自 2023 年 5 月 9 日起，App Store 各店面的现有 App 和一次性 App 内购买项目的价格都将以产品当前在美国店面的价格为基础进行更新，除非你在 2023 年 3 月 8 日后进行了相关更新。[全新的增强定价机制](https://developer.apple.com/cn/news/?id=dbrszv62 "全新的增强定价机制")适用于当地顾客的价格，你可以根据你熟悉的国家或地区来生成全球均衡价格，也可以为各个市场分发定制的内容和服务。

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

AI 仍然是科技圈最热的领域，我目前对这个领域非常感兴趣，感觉正在见证一个领域的兴起，可以发现最近几期摸鱼的内容全部变成 AI 相关的了。我获取这些信息的途径，要么是看一些博主分享，要么是去 Twitter 进行定向的筛选。但这种方式获取和分享的途径还是有些单一，一直想有一个合适的交流这方面内容的社群，外部一直没有找到，就决定自己先建一个看看吧。考虑社群的形式，微信群虽然易用，但很容易沦为吹水群，且会受到管制的影响，最终决定建一个 discord 频道，discord 有话题的概念，可以看历史信息，还可以方便的加各种扩展功能。聊天室已经就位，地址是：https://discord.gg/Fz6V2rej，如果你感兴趣可以加进来聊一哈。

1、[AI playground](https://play.vercel.ai/)：Vercel 发布的 AI 模型实验网站，可以选择 OpenAI 的 GPT4，Google 的模型，以及 claude 模型等，还完全免费，缺点也很明显就是不保留聊天记录，不具备上下文能力。

![](https://cdn.zhangferry.com/Images/202304192253945.png)

[Vercel](vercel.com) 是一个免费的网站托管平台，可以部署静态和动态网站，提供免费的域名和 HTTPS 证书。Github 有一个项目[ChatGPT-Next-Web](https://github.com/Yidadaa/ChatGPT-Next-Web "ChatGPT-Next-Web")实现了 ChatGPT 的聊天界面，可以直接部署到 Vercel 上。然后再关联自己的二级域名，就有了属于自己的调用地址：`chat.zhangferry.com`，大家感兴趣可以访问这个地址体验下。

![](https://cdn.zhangferry.com/Images/202304202218678.png)

2、[character.ai](https://beta.character.ai/ "character.ai")：一个尝试把 AI 拟人化的网站，他们给 AI 赋予了各种各样的角色，你可以根据自己的需求跟他们对话。这个想法非常好，因为我们需要解决的问题都是具有特定场景的，这省去了自己去培养 AI 的步骤。

![](https://cdn.zhangferry.com/Images/202304192324509.png)

3、[AI Talk](https://v.douyin.com/D2TDfgW "AI Talk")：这是抖音博主「AI Talk」制作的视频，「AI马斯克对谈AI乔布斯，辩论人工智能对人类的威胁 两位智者谈论AI是否能具有直觉和情感，一场久违的架空对话」。对话均有 GPT4 生成，这个对话的质量非常高，因为声音上也做了语音的拟合，看上去更像是真实存在的一样。

而这也跟数字人的概念非常一致了，在世的人或者逝去但是留有很多资料记录的人都可以根据现有的数据生成一份数字人模型。我们可以随时跟他们交流，他们也能够在网络的世界里永生。

![](https://cdn.zhangferry.com/Images/202304192341147.png)

4、[HealthGPT](https://twitter.com/varunshenoy_/status/1648374949537775616 "Twitter HealthGPT")：来自斯坦福的一位小哥做的基于健康数据分析的 HealthGPT，目前该项目已经[开源](https://github.com/StanfordBDHG/HealthGPT "HealthGPt")。想象一下，未来每个人都有一个个性化的人工智能健康助手，它可以:

* 保证隐私的情况下追踪你的信息

* 了解你身体的独特需求

* 能够为你的健身目标提供量身定制的建议

![](https://cdn.zhangferry.com/Images/202304192346044.png)

## iOS 招聘 - 蔚来汽车 APP

### 岗位及团队介绍

电动车是未来几年最热的技术领域之一，所处行业前景一片光明，详见：https://www.nio.cn/events/shanghai-autoshow

* 上下班不需要打卡，弹性工作
* 领导 Nice，团队工作氛围很融洽，注重个人发展，很好沟通
* 只要技术 OK，薪资绝对让你满意

工作地点：上海市闵行区宜山路 1999 号科技绿洲三期 23 号楼

### 职责介绍及岗位要求

* 责公司移动产品架构设计，方案的制定，技术可行性研究，系统性能优化及安全加固；
* 责移动技术难题攻关，解决系统中关键架构问题，对系统稳定性负责；
* 项目组开发人员的设计评审，Code Review，以保证代码的可读性、可扩展性、易维护性。

**职位要求**

* 本科以上学历，5年以上iOS平台开发经验；有通用中间件SDK相关开发经验优先；
* 熟悉 WKWebView 基础组件，有 Hybrid 框架、JS Binding 经验优先；
* 悉 React Native、Flutter，有动态化框架开发经验者优先；
* 基础 SDK 开发流程，有图片库、埋点、离线包、AB相关开发经验者优先；
* APM 系统，有稳定性、性能、内存优化经验者优先；

### 联系方式

微信：cuilh2018

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #90 | 面相任务的 GPT 项目诞生](https://mp.weixin.qq.com/s/Bx8N9HqMP5HE9mzy6l3QVA)

[iOS 摸鱼周报 #89 | WWDC 23 公布](https://mp.weixin.qq.com/s/3B_R0j8dpXpR5G9bCRsyXw)

[iOS 摸鱼周报 #88 | 把 AI 集成到研发流程](https://mp.weixin.qq.com/s/ex3aHSPjKj9woxQwHyRzZA)

[iOS 摸鱼周报 #87 | Planning for AGI](https://mp.weixin.qq.com/s/TwugmMEiGoFKYQY9euhg6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
