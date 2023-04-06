# iOS 摸鱼周报 #89 | WWDC 23 公布

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：WWDC 23 全球开发者大会日期公布
> * 内容推荐：推荐近期的一些优秀博文，涵盖：通过 ReplayKit 录制屏幕、在 SwiftUI 中使用相对比例进行布局、保护小组件中的用户隐私等方面的内容
> * 摸一下鱼：AGI 元年；微软对于 GPT-4 的研究论文；可以自定义数据源的 ChatGPT 插件；国产开源模型 ChatGLM

## 本期话题

### [WWDC 23 全球开发者大会日期公布](https://developer.apple.com/cn/wwdc23/ "WWDC 23 全球开发者大会日期公布")

![](https://cdn.zhangferry.com/Images/89-wwdc23.jpeg)

Apple 宣布 WWDC 23 将在北京时间 6 月 6 日至 10 日举行，主要内容是为期一周丰富多彩的技术和社区活动，大会仍采用线上播放形式。通过邀请函图片猜测，本次大会 Apple 可能会带来新的 MR 头显硬件。除了 iOS、iPadOS、macOS、watchOS 和 tvOS 等系统新功能的更新，大会上是否会有 xrOS 新系统的推出也值得关注。

Apple 同时会在 Apple Park 举办面向开发者和学生的全天特别活动，[Swift Student Challenge](https://developer.apple.com/cn/wwdc23/swift-student-challenge/ "Swift Student Challenge ") 也将继续举行，全世界满足条件的学生可以构建自己的 App Playground。完成作品提交截止日期为太平洋夏令时间 2023 年 4 月 19 日，获奖者将会得到 WWDC23 专属夹克、AirPods Pro、定制徽章套装，以及一年开发者会员资格。此外，获奖者还有一次专属的随机抽取出席 Apple Park 特别活动的机会。

## 内容推荐

推荐近期的一些优秀博文，涵盖：通过 ReplayKit 录制屏幕、在 SwiftUI 中使用相对比例进行布局、保护小组件中的用户隐私等方面的内容。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[当 matchGeometryEffect 不起作用时](https://chris.eidhof.nl/post/matched-geometry-effect/ "当 matchGeometryEffect 不起作用时") -- 作者：Chris Eidhof

[@东坡肘子](https://www.fatbobman.com/): 在 SwiftUI 中，视图的 modifier 顺序十分重要，不同的顺序可能会产生完全不一样的结果。作者通过分析一段 matchGeometryEffect 不起作用的代码，从另一个角度阐述了视图的布局逻辑以及 modifier 顺序的重要性。

2、[iOS ReplayKit 与 屏幕录制](https://juejin.cn/post/7217692600647254071 "iOS ReplayKit 与 屏幕录制") -- 作者：网易云音乐技术团队

[@东坡肘子](https://www.fatbobman.com/): 在客户端开发过程中，有时会遇到这样一些场景，需要对用户在应用内的操作做进行屏幕录制，甚至是系统层级的跨应用屏幕录制来实现某种特殊需求，例如在线监考、应用问题反馈、游戏直播等。网易云音乐技术团队在本文中介绍了云音乐 LOOK 直播客户端如何通过 ReplayKit Framework 实现了上述需求。

3、[在 SwiftUI 布局中使用百分比](https://oleb.net/2023/swiftui-relative-size/ "在 SwiftUI 布局中使用百分比") -- 作者：Ole Begemann

[@东坡肘子](https://www.fatbobman.com/): SwiftUI 没有提供使用相对大小进行布局的工具，例如“使此视图是其容器宽度的 50% ”。Ole Begemann 通过 Layout 协议实现了上述的想法，本文提供了思路以及完整代码。有趣的是，在 SwiftUI 1.0 的测试版本中，曾经出现过官方提供的使用相对比例进行布局的 modifier，不过在最终版本中取消了，并且也再没有出现过。

4、[onAppear 的调用时机](https://www.fatbobman.com/posts/onAppear-call-timing/ "onAppear 的调用时机") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): onAppear 是 SwiftUI 开发者经常使用的一个修饰符，但一直没有权威的文档明确它的闭包被调用的时机。本文将通过 SwiftUI 4 提供的新 API ，证明 onAppear 的调用时机是在布局之后、渲染之前。

5、[深入了解 NotificationCenter 的实现原理](https://juejin.cn/post/7216340356949459004 "深入了解 NotificationCenter 的实现原理") -- 作者：向辉_

[@东坡肘子](https://www.fatbobman.com/): NotificationCenter 是一个系统组件，它负责协调和管理事件的通知和响应。它的基本原理是基于观察者模式。由于 Apple 对其是闭源的，因此无法查看 NotificationCenter 的源码。作者采用了曲线救国的方式，通过分析开源的 Swift 来理解 NotificationCenter 的实现。

6、[设备锁定时如何隐藏敏感的小组件数据](https://swiftsenpai.com/development/hide-sensitive-widget-data/?utm_source=rss&utm_medium=rss&utm_campaign=hide-sensitive-widget-data "设备锁定时如何隐藏敏感的小组件数据") -- 作者：Lee Kah Seng

[@东坡肘子](https://www.fatbobman.com/): 随着 iOS 引入小组件，用户现在可以在锁屏和今日视图中轻松访问他们喜爱的应用程序的信息。尽管看起来不错，但这确实带来了隐私问题 —— 即使设备被锁定，敏感数据也可以被访问。在本文中，作者将介绍如何在小组件上隐藏敏感数据，保护用户隐私。


## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、2023 AGI 元年：一位爱好 AGI 的同事在公司内做了一次分享，学到一些东西，尝试总结一些精华的内容。他在 12 年就关注 AGI 领域，该领域在当时还非常小众，随着 ChatGPT 的到来，AGI 概念热了起来，2023年可以被称之为 AGI 元年。

![](https://cdn.zhangferry.com/Images/202304062357097.png)

AGI 全称 Artificial General intelligence，通用人工智能，它没有标准定义，可以理解为具有人类智能的能力。那什么是人类智能的能力，人类智能又是什么，这个最早可以追溯到佛经和柏拉图时代，总之自古以来，人类就一直在思考和探索自己的智慧和思维的本质。到了现代社会，很多学科都与人类智慧的探索相关，心理学、脑科学、认知科学、计算机科学等。

我们先了解下人是怎么认知世界的，为什么我们能很快的分别出一只猫，一个人。≈在认知科学上的解释是在意识层面，存在一个工作记忆，将任务目标、当前注意的实体对象等可操纵的物体都放到一个舞台空间集中加工，进行动态的建模，预测，决策。这就是人去理解这个物理世界的主要步骤，回到计算机领域，人工神经网络正是基于人类的思考模式建立起来的，再往后就是 Transformer 的出现统一了人工智能演进的方向，再往后就是 ChatGPT 的出现。

智能的本质是预测，如何做到预测，从简单的状态机模式，到图灵机，现代计算机，GPT4 他们的工作原理都是非常相似的，逐渐逼近能够预测的程度。为什么计算机原理简单，但却那么强大，就是因为人脑就是这种工作模式。（一种简单的模式，或者叫算法，无限叠加产生了智能，有点理解马斯克说的：我们生活的世界不是虚拟世界的可能性不到十亿分之一）

GPT4 在某些领域已经超过了大多数人，那它还差什么？它还缺少跟真实物理世界的连接，它目前仅能接收和处理文字图片内容，不具备运动控制；它还没有面向任务的自驱动架构，就是它自己去分解目标，一步步完成，这更像一个人的思考过程了。这些都是可实现的，只不过还没有人这么搞（太危险了）。

AGI 势必会影响社会的方方面面，回顾技术的发展史，科技在进步人类的需求却基本没变，基本就是衣食住行、医教娱金。所以到了 AGI，我们还是会继续关注这些内容，只不过与之相对的产业链会发生重塑。

2、[Sparks of Artificial General Intelligence: Early experiments with GPT-4](https://ask.qcloudimg.com/draft/8642415/na64oeidz2.pdf "Sparks of Artificial General Intelligence: Early experiments with GPT-4")：微软对 GPT-4 能力介绍的论文，里面除了介绍很多 GPT-4 在文字理解上的优化和一些多模态能力。还有一个重要结论：GPT-4 已经可以被视为 AGI 的早期版本，它已经初步具备人类意识的雏形。

同时微软研究员抛出了问题，他们也不知道为什么 GPT-4 会如此智能。之前听过一次分享说的是，为什么只有大模型才做到了高效语义的理解，是因为训练量与理解能力不能简单的线性关系，而是到了某个阶段之后会有指数级变化，具体名词叫「思维涌现」。也可以简单的理解为量变产生质变，学了那么多东西，一下子学通了，研究员也不知道它是如何学通的，只是不停地喂数据，它自己就都理解了。这个模式跟人类思考过程也很像，也侧面验证了其具备人类的意识能力。

3、[chatgpt-retrieval-plugin](https://github.com/openai/chatgpt-retrieval-plugin "chatgpt-retrieval-plugin")：一个chatgpt的检索插件，它支持自己定义数据源。可以想到的场景有两个，一个是企业场景，把技术文档、内部资料全部放进去；一个是个人场景，把个人笔记，收集的各类信息放进去。除了纯定制向的数据，他还支持添加来自互联网的数据集。汇合这些信息，再用自然语言去检索。

这个插件让智能化个人助理成为了可能，我们可以基于自己的日常数据，像是聊天记录、音视频记录、健康数据等等来训练自己的私人助理了。已经可以感觉到，未来可能会有更多往这个方向探索的产品出现。就是这个 plugin waitlist 啥时候能通过啊，一只在申请 waitlist 0。0

4、[ChatGLM：千亿基座的对话模型开启内测](https://chatglm.cn/blog)：一个国产的千亿级别参数的针对中英双语的对话模型，与ChatGPT采用的 Generative Pretrained Transformer 架构不同，该模型选用 General Language Model 架构。千亿级别的训练模型 GLM-130B 也是开源的，目前公布了其基座模型（这个时间点是 [2022 年的 8 月 4 号](https://keg.cs.tsinghua.edu.cn/glm-130b/zh/posts/glm-130b/ "GLM-130B：开源的双语预训练模型")，所以国内对于大模型的探索是一直就有的）。

另一个较小的训练模型 [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B "ChatGLM-6B")已完全开源（2023年4月14号），它经过约 1T 标识符的中英双语训练，辅以监督微调、反馈自助、人类反馈强化学习等技术的加持。62 亿参数的 ChatGLM-6B 已经能生成相当符合人类偏好的回答。

![](https://cdn.zhangferry.com/Images/202304052349220.png)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #88 | 把 AI 集成到研发流程](https://mp.weixin.qq.com/s/ex3aHSPjKj9woxQwHyRzZA)

[iOS 摸鱼周报 #87 | Planning for AGI](https://mp.weixin.qq.com/s/TwugmMEiGoFKYQY9euhg6Q)

[iOS 摸鱼周报 #86 | 更多基于 ChatGPT API 的产品诞生了](https://mp.weixin.qq.com/s/y1_V0WKfdwsUL2WjP2zPyA)

[iOS 摸鱼周报 #85 | ChatGPT 的 API 开放使用](https://mp.weixin.qq.com/s/Hhb7ZCDDqEcpIRTlUKiGTQ)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
