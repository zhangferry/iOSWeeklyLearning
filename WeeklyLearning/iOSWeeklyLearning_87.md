# iOS 摸鱼周报 #87 | Planning for AGI

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：App Store 的定价机制升级扩展；四位女性开发者与 App Store 的故事
> * 内容推荐：推荐近期的一些优秀博文，涵盖结构化并发、开发者故事、开发经验分享、Swift Builtin 函数等方面的内容
> * 摸一下鱼：Planning for AGI；GPT4 发布；stable-diffusion-webui 尝试；一个 Alfred 插件 AJTools；苹果新版定价解读

## 本期话题

### [App Store 的定价机制升级现已扩展至所有购买类型](https://developer.apple.com/cn/news/?id=dbrszv62 "App Store 的定价机制升级现已扩展至所有购买类型")

[@远恒之义](https://github.com/eternaljust)：即日起，App Store 最全面的定价机制升级迎来更新，包括新增价格点和按店面管理定价的全新工具。其中，你可在 900 个价格点中选择更灵活的定价，根据你熟悉的国家或地区来生成生成全球均衡价格，也可以为各个市场分发定制的内容和服务。此外，全新的增强定价机制更适用于当地顾客的价格，该机制将会在 2023 年 5 月 9 日更新调整。

### [四位女性通过 app 与游戏推动文化发展并创造改变](https://www.apple.com.cn/newsroom/2023/03/meet-four-women-using-apps-and-games-to-drive-culture-and-create-change/ "四位女性通过 app 与游戏推动文化发展并创造改变")

[@远恒之义](https://github.com/eternaljust)：女性开发者在开发者生态圈是一股不可忽视的力量，Apple 也一直在竭尽全力帮助女性开发者获得更好的成长，此前开展了包括 Apple Entrepreneur Camp（苹果企业家培训营）课程活动，以及针对中国女性开发者的“女性开发者社区日”特别活动。本篇内容为国际妇女节的主题特写，Apple 沟通了四位不同女性，这些女性主导的团队正在努力彰显女性的声音，文中分享了她们如何利用技术来鼓舞女性、创造社会变革的心得。


## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)


## 内容推荐

推荐近期的一些优秀博文，涵盖结构化并发、开发者故事、开发经验分享、Swift Builtin 函数等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[神秘的 Swift 内置模块](https://juejin.cn/post/7208534700223250487 "神秘的 Swift 内置模块") -- 作者：ankit 中文翻译：桃红宿雨

[@东坡肘子](https://www.fatbobman.com/): 如果你已经阅读过 Swift 的 stdlib 库，那大概率注意到了有很多 Builtin.* 类的函数，诸如：`Builtin.Int1`、`Builtin.RawPointer`、`Builtin.NativeObject` 等，这些神秘的 Builtin 到底是什么呢？本文主要解释了 Builtin 存在的原因：加快编译速度（Swift 很多 struct 值类型，最终内部都封装了 IILV IR 基础类型，不需要过多转换）；提高运行性能（由于不需要做过多转换，直接使用的 IILV IR 的函数，相当于使用很多类似底层函数在开发，性能更高）。

2、[手工打造 HTML 解析器的那些事](https://zhgchg.li/posts/2724f02f6e7/ "手工打造 HTML 解析器的那些事") -- 作者：ZhgChgLi

[@东坡肘子](https://www.fatbobman.com/): [ZMarkupParser](https://github.com/ZhgChgLi/ZMarkupParser) 是一个纯 Swift 库，可帮助你将 HTML 字符串转换为具有自定义样式和标签的 NSAttributedString。在本文中，ZhgChgLi 详细介绍了开发该库过程中所涉及的技术细节(HTML String 的 Tokenization 转换、Normalization 处理、Abstract Syntax Tree 的产生、Visitor Pattern / Builder Pattern 的应用)以及一些开发杂谈。本文篇幅很长，难得有开发者会做如此详尽的记录。

3、[结构化并发](http://chuquan.me/2023/03/11/structured-concurrency/ "结构化并发") -- 作者：楚权

[@东坡肘子](https://www.fatbobman.com/): 对于异步与并发，一直以来，业界都有着非常广泛的研究，针对特定场景提出了很多相关的技术，如：Future/Promise、Actor、CSP、异步函数等等。本文通过 GOTO 有害论引出编程历史中结构化编程的演化。以结构化编程作为类比，介绍了结构化并发的核心观点，以及结构化并发的设计理念。结构化并发主要包括作用域、异步函数、计算续体、协程等技术，此外还需要运行时系统的调度，才能最终实现理想的结构化并发。

4、[通过 vacuuming 优化 CoreData 存储文件尺寸](https://blog.eidinger.info/keep-your-coredata-store-small-by-vacuuming "通过 vacuuming 优化 CoreData 存储文件尺寸") -- 作者：Marco Eidinger

[@东坡肘子](https://www.fatbobman.com/): 默认情况下，当你从表中删除数据或删除表、视图或索引等数据库对象时，SQLite 数据库不会自动“释放”磁盘空间。因为 SQLite 只是将删除的对象标记为空闲并保留空间以供将来使用。结果，数据库文件的大小总是在增长。在这篇博文中，Marco Eidinger 将解释 VACUUM 这个概念以及如何将这个概念应用到你的 CoreData 存储中来减少存储文件的尺寸。

5、[独立开发周报 #4 (0306-0312)](https://mp.weixin.qq.com/s/cEieMaUxSxDAZq0Cm_gwEQ "独立开发周报 #4 (0306-0312)") -- 作者：vulgur

[@东坡肘子](https://www.fatbobman.com/):  vulgur 是“极简时钟”、“极简日记”等 App 的作者，从一个月前开始，每周都通过博客的方式来记录自己的开发生活。通过他的记录，你可以对国内独立开发者的工作、生活状态有更多的了解。



## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[OpenAI：通用人工智能规划及未来](https://mp.weixin.qq.com/s/Ku97-qx0EGnV9NVU20LyAA)：这是 OpenAI 发布的文章[Planning for AGI and beyond](https://openai.com/blog/planning-for-agi-and-beyond "Planning for AGI and beyond")的翻译版。人工智能的等级分三级：

* ANI（Artificial Narrow Intelligence，弱人工智能），像是 Alpha Go，只能应用在单一领域。
* AGI（Artificial General Intelligence，强人工智能，也叫通用人工智能），可以胜任人类几乎所有工作。目前还没有达到，随着 ChatGPT 的问世，这种能力应该很快就会到来。
* ASI（Artificial Superintelligence，超人工智能）。超越人类智慧的人工智能，拥有任何人都无法企及的智慧，这个会更远一些。

技术的发展通常都是一把双刃剑，这篇文章主要就在讲 OpenAI 在考虑和规划 AGI 到来所面临的一系列问题。这个问题不只是 OpenAI 所面临的，而是整个社会都将面临的。

> 1. 我们希望AGI能让人类在宇宙中最大限度地繁荣。我们不期望未来变成糟糕的乌托邦，我们希望把有利因素的最大化，把不利因素的最小化，让AGI成为人性良知的放大器。
>
> 2. 我们希望AGI的益处、使用和治理能够被广泛和公平地共享。
>
> 3. 我们希望成功应对巨大的风险。
>
>    在面对这些风险时，我们承认，理论上看似正确的事情，在实践中往往表现得比预期的更奇怪。我们相信，我们必须不断地学习和适应，部署功能较弱的技术版本，以尽量减少追求“一次做对”的场景。

2、[GPT4 发布](https://openai.com/research/gpt-4 "GPT4 发布")：GPT 4 相比 3.5 训练量大幅提升，训练参数已超万亿，这使其在多种自然语言处理任务上更加强大。它现在可以识别图像含义，可以快速创建一个完成程序，在多项人类的考试中均获得非常好的成绩。它能做的事情更多，做的速度也更快了。更厉害的是，相比于很多产品的概念发布和产品预热，这次发布是针对成品的。New bing 已经确认应用了 GPT4，除了图片识别的功能还在 alpha 阶段，其他文字类功能已经提供了可用的 API 调用。

从 3.5 到 4.0 已经是一个非常快的发展，而传言 GPT5 会在年底发布，相比于 GPT 4 它的训练量是这样的：

![](https://cdn.zhangferry.com/Images/202303152247544.png)

届时会增加对视频和声音的理解，AI 的 进化是飞速的，甚至就是指数级的。如果 GPT 4 的能力能代替 1% 的工作，那下一代的 GPT 5 对应的就不是 %2，而是10%，20%。所以关于 AGI 的到来会对社会有什么影响，如何将现有社会运作方式与 AGI 能力配合起来，都是不得不考虑的问题。

3、[stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui "stable-diffusion-webui")：Stable-diffusion 的 WebUI 版本，支持 Apple Silicon 设备，参考地址：[Installation on Apple Silicon](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Installation-on-Apple-Silicon "Installation on Apple Silicon")。通常运行起来遇到最多的问题就是环境的安装，大部分参照 Issues 都能解决。运行前给 `webui-user.sh`文件添加一个环境变量：

```bash
export COMMANDLINE_ARGS="--skip-torch-cuda-test --upcast-sampling --no-half-vae --use-cpu interrogate --xformers --disable-nan-check"
```

这表示运行 `webui.sh` 命令时填写的参数，以适用于 mac 设备。

运行起来需要现配置模型，再输入关键字。模型有两类，一类叫 base model，像 SD v1.5 、chilloutmix，这类模型通常比较大，一般几个 G。一类叫「修正模型」，像 Lora 就属于修正模型，还会有很多 Lora 的变体模型，这类文件比较小，一般 1 百多 M。模型可以在这个网站下载：[civitai](https://civitai.com/ "civitai")，下面是我跑出来的几张效果图，一张耗时大概 50s。

![](https://cdn.zhangferry.com/Images/00003-1295391836.png)

![](https://cdn.zhangferry.com/Images/00007-3265905480.png)

4、[AJTools - 开发工具](https://github.com/kaqijiang/AJTools-AlfredWorkflowa "AJTools - 开发工具")：一个 Alfred Workflow 工具集，用 Python 实现，封装了一系列开发常用功能。包含：时间戳转换、URL 解析、copy SHH Key、打开当前窗口在iTerm2中、当前文件夹下快速新建文件、ChatGPT聊天等。

5、[苹果内购录：关于新定价规则的理解与思考](https://mp.weixin.qq.com/s/ZQlBFHuRoDYmYpMfgnsp2Q)：苹果在 3 月 9 号 发布了[新的定价规则](https://developer.apple.com/cn/news/?id=dbrszv62 "Apple 新的定价规则")，其中有一些修改点可能会对现有业务逻辑带来一些影响。本文对历史规则进行了回顾，同时也对新的定价规则进行了分析解读。

除此之外，推荐需要处理内购的同学可以关注一下该 `#苹果内购录` 系列文章。


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #86 | 更多基于 ChatGPT API 的产品诞生了](https://mp.weixin.qq.com/s/y1_V0WKfdwsUL2WjP2zPyA)

[iOS 摸鱼周报 #85 | ChatGPT 的 API 开放使用](https://mp.weixin.qq.com/s/Hhb7ZCDDqEcpIRTlUKiGTQ)

[iOS 摸鱼周报 #84 | 开箱即用的云服务 AirCode](https://mp.weixin.qq.com/s/fKutqWAHfzkbbFgYCvPfIA)

[iOS 摸鱼周报 #83 | ChatGPT 的风又起来了](https://mp.weixin.qq.com/s/Ty95hGBIevHaJQ5TU774aQ)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
