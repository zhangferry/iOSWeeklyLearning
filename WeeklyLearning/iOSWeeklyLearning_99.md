# iOS 摸鱼周报 #99 | 

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：macOS Sonoma 体验
> * 内容推荐：Swift 宏、Core Data 新特性、SwiftData 介绍、自动生成 RESTful APIs、iOS 应用保护等内容
> * 摸一下鱼：Public Apple Frameworks；微软提供的面相前端初学者的课程；苹果M2 Ultra：AI大模型的新希望；AI 生成的艺术二维码；

## 本期话题

### macOS Sonoma 

体验了一段时间新系统，更新非常小，苹果不告诉我我都不知道发生了哪些变化。说几个比较有意思的变化吧。

1、屏保

![](https://cdn.zhangferry.com/Images/202307042343315.png)

新增了动态屏保，如果你将它作为壁纸同时开启，锁屏时会看到一段航拍风景的视频，解锁桌面，视频缓慢减速，最后定格为桌面壁纸，整个过程自然，舒适。视频地址位于：`/Library/Application Support/com.apple.idleassetsd/Customer/4KSDR240FPS/`，通过目录名也可以看出来，这些屏保是 4K SDR  240帧的规格，每一帧停下来都可以当壁纸。

2、Web App

web app 是 macOS Sonoma 开始引入的新功能，类似 iOS 中的 Home Screen，它可以把浏览器中常访问的网站加到 Dock 栏中。

![](https://cdn.zhangferry.com/Images/202307042317428.png)

添加到 Dock 之后它就可以向普通的 App 一样供我们使用了。这个 web app 并非简单的网页入口，苹果给它融入了很多原生 App 才有的能力。

![](https://cdn.zhangferry.com/Images/202307042324626.png)

macOS 上的 Web App 要比移动端的 Home Screen 意义大的多，因为移动端并不缺应用，浏览特定网站是一个低频场景。而mac 的问题在于应用少，浏览网站是一个高频场景。有很多网站为了做 mac 端都是套壳 H5，有了 Web APP 直接无缝升级为 「Applicaiton」，这对苹果生态和应用本身都是利好的。

3、小组件

也是同步 iOS 端的 Widgets 功能，可以把小组件直接拖动到桌面上去。主要电脑桌面经常都是满的，会覆盖小组件，所以关注到它们的频率也不高。

![](https://cdn.zhangferry.com/Images/202307060855894.png)

## 内容推荐

推荐近期的一些优秀博文，内容涵盖 Swift 宏、Core Data 新特性、SwiftData 介绍、自动生成 RESTful APIs、iOS 应用保护等方面。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[一文看懂 Swift Macro](https://juejin.cn/post/7249888320166903867 "一文看懂 Swift Macro") -- 作者：Yasic

[@东坡肘子](https://www.fatbobman.com/): 在 5.9 版本中，Swift 引入了一个重要的新功能：宏（Macro）。Swift 宏可以在编译时生成源代码，从而避免开发者编写重复的代码。除了 Swift 标准库以及苹果众多的官方库提供的宏外，开发者也可以编写自己的宏。本文作者对宏的特点以及如何自定义宏做了详尽的介绍，并针对不同种类的自定义宏分别给出了示例代码。

2、[WWDC 2023，Core Data 有哪些新变化](https://www.fatbobman.com/posts/what's-new-in-core-data-in-wwdc23/ "WWDC 2023，Core Data 有哪些新变化") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 虽然在 WWDC 2023 上，苹果将主要精力放在介绍新的数据框架 SwiftData 上，但作为 SwiftData 的基石，Core Data 也得到了一定程度上的功能增强。本文将介绍今年 Core Data 获得的新功能，包括：复合属性（ Composite attributes）、在 Core Data 中使用新的 Predicate、VersionChecksum、延迟迁移（Deferred migration）以及阶段式迁移（ Staged migration ）等内容。

3、[使用 Swift 生成 RESTful APIs](https://blog.eidinger.info/generate-restful-apis-with-swift-in-2023 "使用 Swift 生成 RESTful APIs") -- 作者：Marco Eidinger

[@东坡肘子](https://www.fatbobman.com/): [Swift OpenAPI Generator](https://github.com/apple/swift-openapi-generator) 是一个 SwiftPM 插件，可以根据 OpenAPI 文档生成用于执行 HTTP 调用或处理这些调用的客户端或服务器端代码。本文作者介绍了他的经验，通过以下四个步骤使用 Swift OpenAPI Generator 生成客户端代码：获取后端的 RESTful API 定义，模拟后端，生成 Swift 客户端库，然后在应用程序中使用该 Swift 客户端库。

4、[构建 SwiftData 应用的终极指南](https://azamsharp.com/2023/07/04/the-ultimate-swift-data-guide.html "构建 SwiftData 应用的终极指南") -- 作者：Mohammad Azam

[@东坡肘子](https://www.fatbobman.com/): 作为 Core Data 框架的替代品，SwiftData 在 WWDC 2023 首次亮相。本文将通过几个部分全面介绍 SwiftData 的各项功能，其中包括：SwiftData 的基本概念、架构设计、关系管理、数据查询、数据预览、数据迁移、单元测试以及与 UIKit 集成等。通过本文，作者希望读者能全面了解 SwiftData 的功能和特性，从而在 iOS 开发中充分利用其潜力。

5、[iOS 防 dump 可行性调研报告](https://juejin.cn/post/7251501966592917563 "iOS 防 dump 可行性调研报告") -- 作者：ChatGPT(GPT-4) & iHTCboy

[@东坡肘子](https://www.fatbobman.com/): 在 iOS 平台上，保护 App 的源代码安全是开发者的一项重要任务。由于 App 可能包含敏感信息和重要算法，防止源代码被非法获取和篡改显得尤为重要。本文介绍了如何防止 iOS App 被 dump，包括代码混淆、加密、完整性检查等多层防御策略，以及服务器端验证、动态加载、API 安全性和多因素认证等方案。此外，监控与告警、定期安全审计和安全培训等后置方案也可以提高 App 的安全性。最后，还介绍了禁止越狱设备的实施方案，以及 DeviceCheck 和 App Attest API 等新技术方案。


## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[Public Apple Frameworks](https://marcoeidinger.github.io/appleframeworks/ "Public Apple Frameworks")：查看所有 Apple 提供的公共 Framework 在各个平台下是否被支持，以及支持的最低版本。筛选所有的 `Core` 系列框架：

![](https://cdn.zhangferry.com/Images/202307060905262.png) 

2、[Web-Dev-For-Beginners](https://microsoft.github.io/Web-Dev-For-Beginners/#/ "Web-Dev-For-Beginners")：微软提供的面相前端初学者的课程，学习 JS、CSS、HTML，课程公 24 节，包括课后作业，测试，解决方案等。最后会有多个实践项目，浏览器插件、太空游戏、银行应用等。

![](https://cdn.zhangferry.com/Images/202307062322477.png)

3、[苹果M2 Ultra：AI大模型的新希望](https://www.bilibili.com/video/BV1fh4y1M7DX/ "苹果M2 Ultra：AI大模型的新希望")： 今年科技圈最火的就是 AI 领域，各种大模型层出不穷，大模型对算力要求很高，这似乎成了模型训练最大的障碍之一。简单列一下 Nvidia 推出的几种显卡的显存和价格：

| 显卡     | 显存 | 价格    |
| -------- | ---- | ------- |
| RTX 4090 | 24G  | ￥1.3w  |
| A100     | 80G  | ￥8.1w  |
| H100     | 80G  | ￥24.2w |

H100 之所以比 A100 贵那么多是因为 H100 采用了全新一代的琥珀架构，计算性能提升了数倍。所以光看这个价格就知道，大模型训练不是普通人玩得起的。

回到今年发布的 M2 Ultra，最大内存可达 192 GB，在苹果芯片的统一内存架构下， 192 GB 内存就可以是 192 GB 显存。这就意味着原本 8 张 4090才能装得下的 AI 模型，在 M2 Ultra 一张芯片就可以跑起来了。M2 Ultra 192GB + 4 TB 只有 6 w，怎么越算越感觉便宜呢，这一波苹果属实算是弯道超车了。

作者购买了 128 GB 内存的 M2 Ultra，本地就跑起来了 LLaMA 330 亿参数的大模型。当然 完全发挥 M 系列芯片的优势还需要各类软件的适配，这个实现就有赖与开源社区针对 M 芯片在 LLaMA 模型上的特别优化。所以在 AI 芯片领域能打破 Nvidia 垄断的，很有可能就是苹果。

4、[QR Code AI Art Generator](https://huggingface.co/spaces/huggingface-projects/QR-code-AI-art-generator "QR Code AI Art Generator")：最近 AI 艺术的二维码比较火，它是由 4 名中国大学生开发出来的，项目是 [QR Code ControlNet](https://huggingface.co/ioclab/ioc-controlnet/tree/main/models "QR Code ControlNet")。在 StableDiffusion WebUI 中利用 ControlNet 控制灰度和光影，它们保证了二维码的准确性；再利用 Lora 模型实现不同的风格画风，就有了一张特定特别和二维码结合的新图片。这个项目可以让你线上体验这种 AI 艺术风格的二维码，我这里用的 Prompt 是：masterpiece, best quality, cyberpunk city，可以扫一下看出来的是什么：

![](https://cdn.zhangferry.com/Images/202307062236345.png)

5、[对谈半佛仙人：看似复制成功，实则刻舟求剑](https://www.xiaoyuzhoufm.com/episode/649c0aa1f5604aa55e1491c4 "对谈半佛仙人：看似复制成功，实则刻舟求剑")：这期博客非常欢乐，收获比较大的是半佛老师对待生态的态度。因为工作，因为家庭，因为学业，我们经常会有不开心、沮丧的时候。这个时候如果有人跟你说，别忙了，去出去散散心去；别躺着了，跑步运动去；别学了，打游戏去，刷刷短视频，看看修马蹄子的，洗地毯的，来一个赛博按摩。如果没人对你说，就自己跟自己说，让时间静静的浪费掉本身也是一件治愈的事情。

因为李玟越来越多的人又关注了抑郁症，看到一个数字，我国抑郁症就医率不足 10 %，说明大部分抑郁症患者对于抑郁都是选择逃避的。抑郁症本身是一种病，它是需要药物治疗的，而且大部分抑郁症都是可以治好的。很多抑郁症来自于平常负面情绪的积累，所以宣泄情绪，给自己减负非常重要，不要在意别人的看法，不要未还没有发生的事情担忧，躺平，摆烂，浪费时间，这些都没什么，自己开心最重要。

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #98 | visionOS 模拟器体验](https://mp.weixin.qq.com/s/PNEYW71BfkQ2Y3n7uRdxsQ)

[iOS 摸鱼周报 #97 | 智源大会线下参会体验](https://mp.weixin.qq.com/s/6HRxZXAJcTZKGZiNX2eBYQ)

[iOS 摸鱼周报 #96 | Vision Pro 打开空间计算的大门](https://mp.weixin.qq.com/s/BM3SucfO9yhQChIPbnuwrA)

[iOS 摸鱼周报 #95 | WWDC23 is coming](https://mp.weixin.qq.com/s/hi8Dy2H_iBFWeO0V_tQ5xw)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
