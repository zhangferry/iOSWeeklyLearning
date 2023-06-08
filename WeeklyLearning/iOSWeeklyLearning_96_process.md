# iOS 摸鱼周报 #96

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

WWDC Keynote 里的内容分两部分，Vision Pro 和 其他，下文图片来自博主[@andymcnally](https://twitter.com/andymcnally) 的绘制。

### WWDC

![](https://cdn.zhangferry.com/Images/202306080822884.png)

![](https://cdn.zhangferry.com/Images/202306080822366.png)

Vision Pro 才是 WWDC23 的重头戏，众多科技爱好者为之兴奋，XR 行业也发展很久了，但一直都是一个小众市场，且没有现象级的产品出现，Vision Pro 似乎在按照自己的理念重新定义这个行业。通过一些实际体验过产品的人来看，它的优点是：

* 显示效果，交互设计领先其他所有 VR、AR 类型设备一个大的身位，师目前这个领域无可争议的天花板
* 兼顾虚拟世界与现实世界的连接，像是别人能看到你的眼睛，以及增强视频体验的 Persona
* 眼部与手势交互，非常简单且可以实现精准识别、较长时间使用无眩晕感、空间音频非常强
* 3D 照片功能效果非常真实
* 考虑计算量实际功耗会比较大，但体验来看并没有明显发热问题，功耗的调控很牛

缺点：

* 设备较重，戴的时间久的话会比较累
* 电池续航 2h，使用场景受限
* 价格 $3499，劝退大部分人

对于大部分人来说除了尝鲜好像没有其他必须要买 Vision Pro 的理由了。目前来看确实是这样，但 Vision Pro 的演示效果，实际上是打开了一个面向空间计算的大门。借助这个能力，面相家庭、教育、体育、娱乐等场景，原有的二维体验直接扩展到三维，接收信息和感受信息所带来的体验感也更加真实和深刻。生活的意义就是感受生活，那更真实的感受就更容易获得认可。虽然现在还有很多不完善，但往后这个东西会越来越强大。

## 内容推荐

WWDC 正在如火如荼的进行中，本期将推荐一些与 WWDC23 推出的新设备、新框架、新功能有关的博客文章。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[有关 Vision Pro 的一些疑问](https://danielsaidi.com/blog/2023/06/05/vision-pro "有关 Vision Pro 的一些疑问") -- 作者：Daniel Saidi

[@东坡肘子](https://www.fatbobman.com/): 前几天，苹果发布了全新的增强现实头显 Vision Pro，让人耳目一新。然而，尽管看上去十分美好，但本文作者对产品的某些方面感到困惑，例如：名称、视野、电池包、电池寿命、窗口处理、价格、发布日期和未来的公告。不过即使如此，作者仍然表示十分期待使用这个设备。

2、[WWDC 23 ，SwiftUI 5 和 SwiftData 的初印象](https://www.fatbobman.com/posts/impressions-of-WWDC23/ "WWDC23 ，SwiftUI 和 SwiftData 的初印象") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 本文讨论了作者对于 WWDC23 中 SwiftUI 和 SwiftData 的初步印象。SwiftUI 5.0 带来了许多革命性的变化，包括全新的数据流声明和注入方式、动画和视觉效果升级、ScrollView 的控制力大幅改善等。SwiftData 是一套官方推出的，基于 Swift 5.9 新功能实现的 Core Data 的 Swift 封装库，但目前仍存在不少问题，不建议开发者立即在生产中使用。作者认为，苹果的新技术虽然具有实用价值，但在追新与稳定之间，开发者需要慎重地权衡。

3、[Vision Pro:AR 新时代还是兔子洞？](https://www.kodeco.com/40607837-apple-vision-pro-a-new-era-or-ar-rabbit-hole "Vision Pro:AR 新时代还是兔子洞？") -- 作者：Gina De La Rosa

[@东坡肘子](https://www.fatbobman.com/): visionOS 带来前所未有的视觉体验，让传统观影方式瞬间过时。作者深入剖析了 Vision Pro，对其带来的革命性变化与应用进行了详尽阐述。它为开发者与用户开拓了崭新的互动方式与体验形式，推动行业变革与创新。同时，作者也客观理性地判断了相关影响与发展的不确定性，必须解决有关价格、隐私和对人类联系的影响的问题。尽管这一创举仍存在未知数，但作者相信在苹果的引领下，空间计算技术必将发展至更高峰。

4、[在 WWDC23 上推出的所有新框架](https://blog.eidinger.info/all-new-frameworks-presented-at-wwdc23 "在 WWDC23 上推出的所有新框架") -- 作者：
Marco Eidinger

[@东坡肘子](https://www.fatbobman.com/): 与每一届 WWDC 一样，苹果不仅不断改进现有框架，还会推出许多新框架供开发者使用。在 WWDC23 上，苹果推出了 Cinematic、DockKit、MediaExtension、Observation、SensitiveContentAnalysis、SwiftData、Symbols、workoutKit 等框架。本文作者创建了一个[网页](marcoeidinger.github.io/appleframeworks)，以方便开发者查看这些框架的具体功能、面向平台及当前版本状况。

5、[SwiftUI 新功能](https://liyanan2004.github.io/wwdc-23-whats-new-in-swiftui/ "SwiftUI 新功能") -- 作者：LiYanan2004

[@东坡肘子](https://www.fatbobman.com/): 在 WWDC 上，苹果通过 "What's new in SwiftUI" 这个 Session 向开发者介绍了今年在 SwiftUI 上的一些亮点新功能。本文作者通过文字、图片、代码等方式对其内容进行了整理，以帮助你快速了解这些新功能，以便更好地利用它们来构建更好的应用程序。 


## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[SummarAI](https://github.com/zhangferry/SummarAI "SummarAI")：我开发的一款利用 AI 能力总结网页信息的浏览器插件。初版仅用来总结网页里的文字信息，后来使用 [postlight/parse](https://github.com/postlight/parser "postlight/parse") 这个库，发现它对网页主要信息的提取非常准确，且能够视频 wwdc session 页面里的字幕信息，于是用它帮总结 WWDC 视频就顺利成章了。内容提取是一部分，要充分发挥 AI 能力，还需要合理使用 prompt。我参考了一些摘要的 Prompt 写法，并把 Zettelkasten（卢曼卡片盒）笔记法思路引入进来，最终 Prompt 为：

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

以 [What's new in VisionKit](https://developer.apple.com/videos/play/wwdc2023/10048/ "What's new in VisionKit") 这篇 Session 为例，使用以上 Prompt 总结结果如下：

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

使用到 [word_cloud](https://github.com/amueller/word_cloud "word_cloud") 这个库，为了防止 What's new 被切割成两块，去掉符号和空格合成一个单词。做出效果如下所示，上面是 WWDC22，下面是 WWDC23：

![wwdc22](https://cdn.zhangferry.com/Images/202306082315079.png)

![wwdc23](https://cdn.zhangferry.com/Images/202306082316615.png)

观察到的几点趋势：

* What's new 一直都是最大比重，苹果的创新力仍在持续，今年的 `Meet` 系列更多
* Swift 和 Metal 这两项相关技术今年降低很多
* 今年首次出现 `spatial`，且频率很高，可见苹果对 Vision Pro 真的给予众望

3、[Learn about visionOS](https://developer.apple.com/visionos/learn/ "Learn about visionOS")：了解 visionOS 这个新系统，今年 WWDC 与之相关的 session 多达 46 个，涉及空间计算、SwiftUI、RealityKit、ARKit、Reality Composer Pro、Unity、Games & Media、Web 体验、iOS/iPadOS 与 visionOS 的兼容，以及 visionOS 设计原则等等。

![](https://cdn.zhangferry.com/Images/202306090009848.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #94 | 前端项目开发流程学习](https://mp.weixin.qq.com/s/f2Z1VRpk4Ehh3KxuY_NrvA)

[iOS 摸鱼周报 #93 | AIGC 尝试](https://mp.weixin.qq.com/s/ios0QYKmnYtJ8URvZLJ1TA)

[iOS 摸鱼周报 #92 | Swift Foundation 预览版发布](https://mp.weixin.qq.com/s/AQaY2DA2h8S-XEYoQ0u7Ew)

[iOS 摸鱼周报 #91 | 免费的网站托管平台 Vercel](https://mp.weixin.qq.com/s/93YLa8ankkEVcp4pop2A6A)https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
