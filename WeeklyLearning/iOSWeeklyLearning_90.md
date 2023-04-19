# iOS 摸鱼周报 #90 | 面相任务的 GPT 项目诞生

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：4 月 25 日起必须使用 Xcode 14.1 构建提交 App
> * 内容推荐：推荐近期的一些优秀博文，涵盖：自定义 Swift Toolchain、软件测试、AI 应用、Dark Sky 设计经验等方面的内容。
> * 摸一下鱼：面向任务的 GPT 项目 Auto-GPT；把 GPT 模型融于模拟角色；把 AI 融于设计流程；Xcode 版本的 Copilot 插件

## 本期话题

### [4 月 25 日起必须使用 Xcode 14.1 构建提交 App](https://developer.apple.com/cn/news/?id=jd9wcyov "4 月 25 日起必须使用 Xcode 14.1 构建提交 App")

[@远恒之义](https://github.com/eternaljust)：Apple 于 2022 年 10 月 18 日开放了 iOS 16.1 的 App 提交，鼓励开发者利用“实时活动”来适配 iOS 16 上的锁定屏幕和灵动岛功能。同时也提醒开发者，会在 4 月份限制提交至 App Store 的 App 必须使用 Xcode 14.1 或更高版本构建。近日，Apple 确定了具体截止时间为 2023 年 4 月 25 日，开发者还剩十来天完成项目的适配工作，留给同学们的时间不多了。

推荐下载 Xcode 14.2 来构建项目，使用最新的 Xcode 14.3 打包会遇到 [CocoaPods 报错](https://github.com/CocoaPods/CocoaPods/issues/11808 "Xcode 14.3 Archive CocoaPods 报错") `rsync: link_stat failed:`，需手动修改 `Pods-项目名-frameworks.sh文件` 中 `source="$(readlink "${source}")"` 为 `source="$(readlink -f "${source}")"`。

### [线上讲座：探索 App Store 定价机制升级](https://developer.apple.com/events/view/LMKG9DJV2M/dashboard "线上讲座：探索 App Store 定价机制升级")

[@远恒之义](https://github.com/eternaljust)：本次讲座会探索 App Store 中提供的最新定价功能，Apple 将介绍增强的全球定价机制、按店面管理定价的全新工具、新增价格点以及全球均衡价格功能。同时，Apple 还会分享一些定价的配置示例。

## 内容推荐

推荐近期的一些优秀博文，涵盖：自定义 Swift Toolchain、软件测试、AI 应用、Dark Sky 设计经验等方面的内容。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[抖音 Swift 编译优化 - 基于自定义 Toolchain 编译提速 60%](https://mp.weixin.qq.com/s/MT5MHhZIlyrhuVNM3Ckteg) -- 作者：抖音基础技术团队

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

目前 AI 的演进方向分为两条路，一个是用 AI 覆盖传统的生产流程，一个是探索 AI 更广阔的应用场景。

1、[Auto-GPT](https://github.com/Torantulino/Auto-GPT "Auto-GPT")：这是一个实验性的开源项目，由 GPT-4 驱动。它最大的特点是把 LLM 的想法串在一起，以实现设定的目标。这个东西恰好跟上一期内容分享的 GPT4 的能力限制有关：

> 它还没有面向任务的自驱动架构。这个含义是，它可以自己去分解目标，一步步完成，这个处理流程就像一个人去做一件事的步骤一样。

而这个项目就是为了达成这个目标设计的，示例项目中给它的目标是：为接下来要发生的节日创建一个食谱，然后保存这个文件，完成之后你退出程序。以下是 Auto-GPT 的执行流程：

![](https://cdn.zhangferry.com/Images/202304132143819.png)

> 1、Google 搜索即将到来的节日
>
> 2、检索第一个返回的网站信息，没有找到合适的节日信息
>
> 3、检索第二个网站信息，也没有找到合适的节日信息
>
> 4、开始变换策略：直接 Google 搜索当前的日期，然后加上「节日」
>
> 5、检索结果有很多，它为了提高效率，选择了一个带日历视图的网站
>
> 6、检索该网站信息，确认了「地球日」比较适合做目标节日
>
> 7、把地球日和对应的日期，记录到自己的内存里
>
> 8、使用 GPT-4 生成一份地球日主题的食谱，发生命令错误
>
> 9、重新纠正再用 GPT-4 去创建食谱，获得结果

这个才是 AGI 所表现出来的智能，它会自我学习，也会自动纠错，这就像人一样去完成一件事。另一方面因为 AI 有很大的自主性，如果为了达成目标需要付出一定的代价，AI 对这个代价的衡量跟人是不同的，所以这个事情的危险性也很大。项目中也多次提到危险性和免责说明，当这项能力被完全打开的时候，打开的会是潘多拉的盒子吗？

2、[把GPT模型融入游戏角色里](https://reverie.herokuapp.com/arXiv_Demo)：斯坦福大学和 Google 的研究员做这样一个产品，创建一个虚拟小镇，里面有 25 个角色，他们的身份提前在 ChatGPT 里定义好，行为方式由 ChatGPT 自动生成，然后驱动各个角色做各自的事情。

各个角色的行为有时间线，且比较多样，像是对话、写作、吃饭、休息、谈恋爱、上班、散步都有。而且他们做的事情时间还可以相互影响，我们关注某一个正在聊天的对象，暂停时间线可以看他聊的啥：

> GR：我在思考如何把数学模式应用到药物研究上，你有什么想法吗？
>
> RP：我最近刚读了一篇相关的论文，等下发给你。JM 对这个专题很感兴趣，你也可以跟她交流下。

这个效果真的很有意思，除了游戏层面人物，也可以把这个场景扩展为一个影视剧，类似《楚门的世界》。还可以在一个大环境里，给两个人塑造两个性格，观察他们以后的行为，用来做心理学行为学的研究等等。

![](https://cdn.zhangferry.com/Images/202304112328897.png)

![](https://cdn.zhangferry.com/Images/202304112336624.png)

3、[designtools.ai](https://designtools.ai/ "designtools.ai")：把 AI 融入设计领域的工具汇总网站。可以发现，现在 AI 的能力已经开始往各个垂类蔓延发扬光大了。

![](https://cdn.zhangferry.com/Images/202304112320465.png)

* 交互类：通过 Figma 设计稿生成可交互网站和 React 组件；Figma 工作流自动化；在Figma 里自动生成素材图片；
* 图像类：生成人物形象；生成产品图、广告营销图；生成 icon，矢量图
* 颜色类：自动生成配色色盘
* 字体类：生成最合适当前布局的字体

4、[Copilot for Xcode](https://github.com/intitni/CopilotForXcode "Copilot for Xcode")：Copilot 官方并没有 Xcode 插件，[intitni](https://github.com/intitni) 写了这个 Xcode 版的Copilot 插件，它同时支持 Github Copilot 和 ChatGPT。和大多数 GPT 插件一样，内置了代码建议和聊天功能。

![](https://cdn.zhangferry.com/Images/202304122232286.png)


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #88 | 把 AI 集成到研发流程](https://mp.weixin.qq.com/s/ex3aHSPjKj9woxQwHyRzZA)

[iOS 摸鱼周报 #87 | Planning for AGI](https://mp.weixin.qq.com/s/TwugmMEiGoFKYQY9euhg6Q)

[iOS 摸鱼周报 #86 | 更多基于 ChatGPT API 的产品诞生了](https://mp.weixin.qq.com/s/y1_V0WKfdwsUL2WjP2zPyA)

[iOS 摸鱼周报 #85 | ChatGPT 的 API 开放使用](https://mp.weixin.qq.com/s/Hhb7ZCDDqEcpIRTlUKiGTQ)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
