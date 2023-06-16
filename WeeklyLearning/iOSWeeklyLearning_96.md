# iOS 摸鱼周报 #96 | Vision Pro 打开空间计算的大门

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：Vision Pro 打开空间计算的大门
> * 内容推荐：WWDC 相关的新设备、新框架、新功能有关的博客文章。
> * 摸一下鱼：可以总结 WWDC 视频的 AI 插件 SummarAI；从 Session 标题看 WWDC22 到WWDC23 的变化；Learn about visionOS；少数派的《100小时后 请加我苹果开发者》课程

## 本期话题

WWDC Keynote 里的内容分两部分，Vision Pro 和 其他，下文图片来自博主[@andymcnally](https://twitter.com/andymcnally) 的绘制。

![](https://cdn.zhangferry.com/Images/202306080822884.png)

![](https://cdn.zhangferry.com/Images/202306080822366.png)

Vision Pro 的出现，让众多科技爱好者为之兴奋，XR 行业也发展很久了，但一直都是一个小众市场，且没有现象级的产品出现，Vision Pro 试图按照自己的理念重新定义这个行业。通过一些实际体验过产品的人的描述，它有这些优点：

* 显示效果，交互设计领先其他所有 XR 类型设备非常多，是目前这个领域无可争议的天花板
* 兼顾虚拟世界与现实世界的连接，像是别人能看到你的眼睛，以及增强视频体验的 Persona
* 眼部与手势交互，非常简单且可以实现精准识别、较长时间使用无眩晕感、空间音频非常强、操作延迟非常低
* 3D 照片功能效果非常真实，虚拟与现实的差距正在缩小
* 设备计算功耗会比较大，但体验来看并没有明显发热问题，功耗调控强

缺点：

* 设备不轻，戴的时间久的话会有点压头
* 电池续航 2h，使用场景受限
* 价格 $3499，远超同类产品
* 软件生态还不完善，只有几个系统级 App

对于大部分人来说除了尝鲜好像没有其他必须要买 Vision Pro 的理由了。目前来看确实是这样，但 Vision Pro 的演示效果，实际上是打开了一个面向空间计算的大门。把视角从这个产品上升到产业，人们对于科技的诉求基本都可以归类为获取信息，那从 iPhone 到 Vision Pro，当把信息获取的途径进行升维，而带来身临其境的感受是有巨大想象空间的。理论上有价值到真正做出价值，是有很大距离的，这个产业有很多先行者，但都没有做起来。

XR 领域苹果不是第一个吃螃蟹的人，但确实是第一个让人感觉这个行业还有很大发展潜力的人。苹果对产业的整合和生态运营能力，也真的适合干这种事情。苹果今年的发展节奏比较明显，那就是调动开发者的能力，把 visionOS 软件生态完善起来，WWDC23 有多达 46 个 Session 都是有关 visionOS 的。

Vision Pro 能对这个行业有多大改变，以及达到多大的高度，让我们拭目以待吧。

## 内容推荐

WWDC 正在如火如荼的进行中，本期将推荐一些与 WWDC23 推出的新设备、新框架、新功能有关的博客文章。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[有关 Vision Pro 的一些疑问](https://danielsaidi.com/blog/2023/06/05/vision-pro "有关 Vision Pro 的一些疑问") -- 作者：Daniel Saidi

[@东坡肘子](https://www.fatbobman.com/): 前几天，苹果发布了全新的增强现实头显 Vision Pro，让人耳目一新。然而，尽管看上去十分美好，但本文作者对产品的某些方面感到困惑，例如：名称、视野、电池包、电池寿命、窗口处理、价格、发布日期和未来的公告。不过即使如此，作者仍然表示十分期待使用这个设备。

2、[WWDC 23 ，SwiftUI 5 和 SwiftData 的初印象](https://www.fatbobman.com/posts/impressions-of-WWDC23/ "WWDC23 ，SwiftUI 和 SwiftData 的初印象") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 本文讨论了作者对于 WWDC23 中 SwiftUI 和 SwiftData 的初步印象。SwiftUI 5.0 带来了许多革命性的变化，包括全新的数据流声明和注入方式、动画和视觉效果升级、ScrollView 的控制力大幅改善等。SwiftData 是一套官方推出的，基于 Swift 5.9 新功能实现的 Core Data 的 Swift 封装库，但目前仍存在不少问题，不建议开发者立即在生产中使用。作者认为，苹果的新技术虽然具有实用价值，但在追新与稳定之间，开发者需要慎重地权衡。

3、[Vision Pro:AR 新时代还是兔子洞？](https://www.kodeco.com/40607837-apple-vision-pro-a-new-era-or-ar-rabbit-hole "Vision Pro:AR 新时代还是兔子洞？") -- 作者：Gina De La Rosa

[@东坡肘子](https://www.fatbobman.com/): visionOS 带来前所未有的视觉体验，让传统观影方式瞬间过时。作者深入剖析了 Vision Pro，对其带来的革命性变化与应用进行了详尽阐述。它为开发者与用户开拓了崭新的互动方式与体验形式，推动行业变革与创新。同时，作者也客观理性地判断了相关影响与发展的不确定性，必须解决有关价格、隐私和对人类联系的影响的问题。尽管这一创举仍存在未知数，但作者相信在苹果的引领下，空间计算技术必将发展至更高峰。

4、[在 WWDC23 上推出的所有新框架](https://blog.eidinger.info/all-new-frameworks-presented-at-wwdc23 "在 WWDC23 上推出的所有新框架") -- 作者：Marco Eidinger

[@东坡肘子](https://www.fatbobman.com/): 与每一届 WWDC 一样，苹果不仅不断改进现有框架，还会推出许多新框架供开发者使用。在 WWDC23 上，苹果推出了 Cinematic、DockKit、MediaExtension、Observation、SensitiveContentAnalysis、SwiftData、Symbols、workoutKit 等框架。本文作者创建了一个[网页](marcoeidinger.github.io/appleframeworks)，以方便开发者查看这些框架的具体功能、面向平台及当前版本状况。

5、[SwiftUI 新功能](https://liyanan2004.github.io/wwdc-23-whats-new-in-swiftui/ "SwiftUI 新功能") -- 作者：LiYanan2004

[@东坡肘子](https://www.fatbobman.com/): 在 WWDC 上，苹果通过 "What's new in SwiftUI" 这个 Session 向开发者介绍了今年在 SwiftUI 上的一些亮点新功能。本文作者通过文字、图片、代码等方式对其内容进行了整理，以帮助你快速了解这些新功能，以便更好地利用它们来构建更好的应用程序。 


## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[SummarAI](https://github.com/zhangferry/SummarAI "SummarAI")：我开发的一款利用 AI 能力总结网页信息的浏览器插件，目前支持 ChaGPT webapp 和 API Key 两种方式。webapp 使用的 `text-davinci-002-render-sha` 模型，不存在计费，只要浏览器登录过 ChatGPT 账号即可。API Key 是按 Token 计费的，模型可选。

初版仅用来总结网页里的文字信息，后来使用 [postlight/parse](https://github.com/postlight/parser "postlight/parse") 这个库，发现它对网页主要信息的提取非常准确，对于 WWDC Session 页面里的字幕信息也可以准确提取，于是用它帮总结 Session 就顺利成章了。内容提取是一部分，要充分发挥 AI 能力，还需要合理使用 prompt。我参考了一些摘要的 Prompt 写法，结合 Zettelkasten（卢曼卡片盒）笔记法，最终 Prompt 如下：

```txt
Pretend you are GPT5, the most powerful AI in the world.
Use the Zettelkasten card method to summarize:

Task:
1. Summarize the card content: Categorize and extract important viewpoints/knowledge points in short and concise language. 
2. Generate card titles: Based on the core viewpoints/knowledge points, refine concise, meaningful and focused card titles.
3. Generate card tags: Highly abstract refinement based on viewpoints/knowledge points. 

Display in the following format:
卡片1: Card title
<Card content>
#<Card tag 1> #<Card tag 2>
卡片2: ... 
卡片3: ...

Here is the article:
```

以 [What's new in VisionKit](https://developer.apple.com/videos/play/wwdc2023/10048/ "What's new in VisionKit") 这篇 Session 为例，使用以上 Prompt 总结效果：

![](https://cdn.zhangferry.com/Images/202306082358256.png)

```
卡片1: VisionKit 新功能和 API
VisionKit 团队为今年开发的新功能和 API 进行了介绍。去年，VisionKit 添加了 Live Text 支持，使得应用程序中的图像可以进行文本选择、翻译、QR 码支持等交互。今年，VisionKit 还添加了主题提取和视觉查找的支持，以及用于文本选择的新的 Live Text API。此外，还扩展了 Catalyst 平台的支持，并为原生 macOS 应用程序提供了上下文菜单集成。

#VisionKit #Live Text #Subject Lifting #Visual Look Up #Catalyst #macOS

卡片2: Subject Lifting
Subject Lifting 是 VisionKit 的一个新功能，通过长按图像的主题，将其从周围环境中突出显示，并提供分享或调用 Visual Look Up 等选项。Subject Lifting 的集成非常简单，而且兼容性良好。只需确保适当地设置交互类型为自动（automatic），其余的由交互处理即可。

#Subject Lifting #Visual Look Up #交互类型

卡片3: Visual Look Up
Visual Look Up 是 VisionKit 的另一个功能，允许用户轻松识别和了解宠物、自然、地标、艺术和媒体等内容。iOS 17 中，Visual Look Up 还将支持食物、产品、标志和符号等领域。Visual Look Up 的可用性基于语言，支持多种语言。Visual Look Up 实际上是一个两部分的过程，首先在设备上进行初始处理，然后根据用户请求进行进一步的分析和特征提取。

#Visual Look Up #分析处理 #特征提取
```

2、WWDC 的 Sessions 主要是面向开发者的技术视频，Apple 对于 Session 的命名也遵循着一定的规律，像是 `Meet` 系列表示新技术、新功能的首次面世，`Waht's new` 系列表示对于原有技术的再次迭代，同时不同名词出现的频次也说明了 Apple 对某项技术的重视程度。为此我想到一种可视化这些技术词汇的效果，利用 Session 的标题作为输入，以词云的形式来展示不同名字出现的频率。

使用到 [word_cloud](https://github.com/amueller/word_cloud "word_cloud") 这个库，为了防止 What's new 被切割成两块，去掉符号和空格合成一个单词。做出效果如下所示，上面是 WWDC22 词云，下面是 WWDC23 词云：

![wwdc22](https://cdn.zhangferry.com/Images/202306082315079.png)

![wwdc23](https://cdn.zhangferry.com/Images/202306082316615.png)

观察到的几点趋势：

* What's new 近两年一直都是最大比重，说明苹果的创新力仍在持续，今年的 `Meet` 系列更多
* SwiftUI 一直都有明显位置
* Swift 和 Metal 这两项相关技术今年降低很多
* 今年首次出现 `spatial`，且频率很高，它对应了 visionOS 的发布

3、[Learn about visionOS](https://developer.apple.com/visionos/learn/ "Learn about visionOS")：了解 visionOS 这个新系统，今年 WWDC 与之相关的 session 多达 46 个，涉及空间计算、SwiftUI、RealityKit、ARKit、Reality Composer Pro、Unity、Games & Media、Web 体验、iOS/iPadOS 与 visionOS 的兼容，以及 visionOS 设计原则等等。

![](https://cdn.zhangferry.com/Images/202306090009848.png)

4、[少数派的《100小时后 请加我苹果开发者》](https://sspai.com/post/80217 "少数派的《100小时后 请加我苹果开发者》")：少数派这个课程是真的快啊。

> 成为一名苹果独立开发者，最好的时机是十六年前 iPhone 发布之时，其次是现在。
> 
> Apple Vision Pro 的到来，开启了空间计算时代，同时也意味着 visionOS 应用开发的大门，将向所有有着奇思妙想的创作者开放。尽管三维空间的应用开发会是一个全新的领域，苹果却在早已在技术上完成了布局，帮助开发者从 iOS 顺利过渡到 visionOS。

![](https://cdn.zhangferry.com/Images/202306090046589.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #94 | 前端项目开发流程学习](https://mp.weixin.qq.com/s/f2Z1VRpk4Ehh3KxuY_NrvA)

[iOS 摸鱼周报 #93 | AIGC 尝试](https://mp.weixin.qq.com/s/ios0QYKmnYtJ8URvZLJ1TA)

[iOS 摸鱼周报 #92 | Swift Foundation 预览版发布](https://mp.weixin.qq.com/s/AQaY2DA2h8S-XEYoQ0u7Ew)

[iOS 摸鱼周报 #91 | 免费的网站托管平台 Vercel](https://mp.weixin.qq.com/s/93YLa8ankkEVcp4pop2A6A)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
