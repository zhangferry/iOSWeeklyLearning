# iOS 摸鱼周报 #90

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

推荐近期的一些优秀博文，涵盖：自定义 Swift Toolchain、软件测试、AI 应用、Dark Sky 设计经验等方面的内容。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[抖音 Swift 编译优化 - 基于自定义 Toolchain 编译提速 60%](https://mp.weixin.qq.com/s/MT5MHhZIlyrhuVNM3Ckteg "抖音 Swift 编译优化 - 基于自定义 Toolchain 编译提速 60%") -- 作者：抖音基础技术团队

[@东坡肘子](https://www.fatbobman.com/): 对于大型项目来说，编译速度至关重要。本文探讨了全部模块化后带来的依赖解析瓶颈问题，并介绍了如何通过自定义工具链来提高抖音的 Swift 编译速度。作者解释了自定义工具链的过程，包括如何增加入参定义、白名单解析和自定义诊断信息等，并分享了如何验证和上线自定义工具链，以及未来可以进一步优化编译速度的方向。本文有助于学习如何提高编译速度，以及如何利用 Swift 工具链进行深度优化。

2、[一些关于开发的杂谈话题 —— 测试](https://onevcat.com/2023/04/dev-talk-testing/ "一些关于开发的杂谈话题 —— 测试") -- 作者：王巍(onevcat)

[@东坡肘子](https://www.fatbobman.com/): 本文讨论了软件开发中测试的各个方面，包括为什么要写测试、测试风格和框架选择等。文章还探讨了使用人工智能生成测试代码所具备的潜力。作者强调在苹果平台上使用 XCTest 的好处，并建议初学者将其作为重点。文章还讨论了如何提高测试质量，例如减少代码耦合、使用依赖注入、Mock 和 Stub 等。最后，作者重申了使用纯函数来简化测试的重要性。

3、[为数据可视化杰作 —— Dark Sky 致哀](https://nightingaledvs.com/dark-sky-weather-data-viz/ "为数据可视化杰作 —— Dark Sky 致哀") -- 作者：Srini KadamatiMarch

[@东坡肘子](https://www.fatbobman.com/): 2023 年 1 月 1 日，苹果公司终止了在 iOS 上运行的 Dark Sky 移动应用程序（ 苹果公司在 2020 年初收购了该应用的开发公司 ）。作者对 Dark Sky 的设计深感骄傲，认为该应用程序是信息设计的典范。文章还提供了该应用程序微妙设计元素的例子，并分享了前用户的抱怨，他们怀念该应用程序的效率和降水图。在文章最后，作者呼吁开发者应借鉴 Dark Sky 将数据情境化的做法，提供更好的用户体验。

4、[我目前正在使用的 AI 服务](https://www.fatbobman.com/posts/AI-Services-I-am-currently-using/ "我目前正在使用的 AI 服务") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 本文介绍了作者如何将 AI 服务导入到他的工作流程中以提高工作效率。作者使用了 Github Copilot、Notion AI、Warp AI、ChatGPT 和 MidJourney 等 AI 工具。作者认为，无论是 AI 服务的提供者还是使用者都应该仅将 AI 视为工作或生活助手，无需抵制，也不必过度赞美。就像大多数新技术一样，几年后回首，它们已经完全融入了我们的生活中。人们会感叹由技术更新所带来的便利，同时也会唏嘘因变革所带来的时代阵痛。

5、[将 Swift 字符串转换为布尔值](https://useyourloaf.com/blog/converting-a-swift-string-to-a-bool/ "将 Swift 字符串转换为布尔值") -- 作者：Keith Harrison

[@东坡肘子](https://www.fatbobman.com/): 在某些不规范的文件中，往往会用多种方式来表示布尔值。例如：true、True、Yes、1、False、no、0 、faLse、not true 等，这会对解析造成一定的影响。本文讨论了将 Swift 字符串转换为布尔值的多种方法，包括使用 Swift 标准库和 Core Foundation 的 NSString。作者最终创建了自己的扩展，以满足其特定需求，包括不区分大小写、忽略空格和返回无效输入的 nil 值。

6、[在 SwiftUI 中显示可扩展文本字段](https://serialcoder.dev/text-tutorials/swiftui/presenting-expandable-textfields-in-swiftui/ "[在 SwiftUI 中显示可扩展文本字段") -- 作者：Gabriel Theodoropoulos

[@东坡肘子](https://www.fatbobman.com/): 在 iOS 和 macOS 中，传统上有两种文本输入控件：TextField 和 TextView。TextField 只接受单行文本，而 TextView 则提供了多行文本输入选项。本文介绍了如何在 SwiftUI 中呈现可扩展的文本字段，这是在 iOS 16 和 macOS 13 中引入的功能。同时，还将说明如何限制显示行数以及在 macOS 中的注意事项。作者认为，SwiftUI 4 使创建可扩展和可滚动的文本字段变得容易。

## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[designtools.ai](https://designtools.ai/ "designtools.ai")：把 AI 融入设计领域的工具汇总网站。可以发现，现在 AI 的能力已经开始往各个垂类蔓延发扬光大了。

![](https://cdn.zhangferry.com/Images/202304112320465.png)

* 交互类：通过 Figma 设计稿生成可交互网站和 React 组件；Figma 工作流自动化；在Figma 里自动生成素材图片；
* 图像类：生成人物形象；生成产品图、广告营销图；生成 icon，矢量图
* 颜色类：自动生成色盘
* 字体类：生成合适的字体

2、[把GPT模型融入游戏角色里](https://reverie.herokuapp.com/arXiv_Demo)：斯坦福大学和Google的研究员做了这样一个产品，创建一个虚拟小镇，里面有 25 个角色，他们的身份提前在 ChatGPT 里定义好，行为方式由 ChatGPT 自动生成，然后驱动各个角色做各自的事情。

各个角色的行为有时间线，且比较多样，像是对话、写作、吃饭、休息、谈恋爱、上班、散步都有。而且他们做的事情时间还可以相互影响，我们关注某一个正在聊天的对象，暂停时间线可以看他聊的啥：

> GR：我在思考如何把数学模式应用到药物研究上，你有什么想法吗？
>
> RP：我最近刚读了一篇相关的论文，等下发给你。JM 对这个专题很感兴趣，你也可以跟她交流下。

这个效果真的很有意思，除了游戏层面人物，也可以把这个场景扩展为一个影视剧，类似《楚门的世界》。还可以在一个大环境里，给两个人塑造两个性格，观察他们以后的行为，用来做心理学行为学的研究等等。

![](https://cdn.zhangferry.com/Images/202304112328897.png)

![](https://cdn.zhangferry.com/Images/202304112336624.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
