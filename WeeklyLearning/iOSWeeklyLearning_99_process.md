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



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
