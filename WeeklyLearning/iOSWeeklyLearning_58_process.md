# iOS 摸鱼周报 #58 | 周报改版，WWDC22 讲座集锦

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：在您的 App 中提供帐户删除选项
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：
> * 岗位推荐：

## 本期话题

### [在您的 App 中提供帐户删除选项](https://developer.apple.com/cn/support/offering-account-deletion-in-your-app "在您的 App 中提供帐户删除选项")

[@远恒之义](https://github.com/eternaljust)：苹果要求，自 2022 年 6 月 30 日起，如果您的 App 支持帐户创建，提交到 App Store 审核，必须支持用户在 App 中发起帐户删除，以避免审核延迟。

⚠️ 注意事项：
* 支持“通过 Apple 登录”的 App 应使用 Sign in with Apple REST API 来[撤销用户令牌](https://www.yuque.com/eternaljust/rpmt31/bxmc3d#khpAl "撤销用户令牌")。
* 如果 App 帐户删除流程是手动的（如在应用内申请删除账号，需要管理员后台审核），请告知用户删除帐户需要多长时间，并在删除完成时提供一条确认信息。
* 如何避免拥有自动续期订阅的用户在删除帐户后意外被 Apple 继续扣款？可提供[链接](https://apps.apple.com/account/subscriptions "打开用户管理订阅链接")来让用户管理取消自己的订阅。

## 本周学习

整理编辑：[JY](https://juejin.cn/user/1574156380931144)



## 内容推荐

> 每年一度的苹果开发者盛会在不久前落幕了。今年的 WWDC 一如既往地精彩。我们将分几期将一些有关 WWDC 2022 上推出的新内容、新技术介绍给大家。

整理编辑：[远恒之义](https://github.com/eternaljust)

1、[WWDC22: Wrap up and recommended talks](https://www.hackingwithswift.com/articles/254/wwdc22-wrap-up-and-recommended-talks "WWDC22: Wrap up and recommended talks") -- 来自：hackingwithswift

[@远恒之义](https://github.com/eternaljust)：WWDC22 精彩纷呈，本文作者回顾了他参与本次活动的过程，一些现场有趣的故事，10 个最喜欢的演讲主题，6 个推荐视频来了解刚推出的新内容，还有几个丰富的 WWDC22 周边社区活动。

2、[在 SwiftUI 利用 Live Text API 從圖片中擷取文本](https://www.appcoda.com.tw/live-text-api/ "在 SwiftUI 利用 Live Text API 從圖片中擷取文本") -- 来自：appcoda

[@远恒之义](https://github.com/eternaljust)：在新的 iOS 16，Apple 发布了 Live Text API，可以将图像转换为机器可读的文本格式。我们只需使用 VisionKit 中的一个新类别 DataScannerViewController，来启用有 Live Text 功能的相机，就能提取出图像中的文本。本文同时为你提供了一个 demo 来快速上手体验。

3、[Swift 5.7 中的 any 和 some (译)](https://juejin.cn/post/7113802054455263268 "Swift 5.7 中的 any 和 some (译)") -- 来自：donnywals 中文译者：Sunxb

[@远恒之义](https://github.com/eternaljust)：关于 Swift 5.7 中的 any 和 some 关键字的改动，作者使用例子来帮助我们了解 any 和 some 两者之间的差异。通过对比，本文将解释它们分别解决了什么问题，以及对于选择 some 还是 any 做了解答。

4、[iOS CarPlay｜WWDC22 - 通过 CarPlay 让你的 App 发挥更大的作用](https://juejin.cn/post/7114239495360233479 "iOS CarPlay｜WWDC22 - 通过 CarPlay 让你的 App 发挥更大的作用") -- 来自：师大小海腾

[@远恒之义](https://github.com/eternaljust)：时隔 2 年，CarPlay 迎来了大更新。在 iOS16 中新增的两种支持 CarPlay 的 App 类型：Fueling App 和 Driving Task App。感兴趣的话，和作者一起来探索 Navigation App 如何在受支持车辆中的数字仪表盘上实时绘制地图。

此外，Apple 今年给我们带来了 CarPlay Simulator，它是一个 Mac App，可以帮助你在不离开办公桌的情况下连接 iPhone Device 来开发和测试 CarPlay App，模拟真实环境，而无需经常来回跑到你的车上或购买售后市场主机进行测试。这大幅度提升了开发者的开发测试体验。

5、[用 Table 在 SwiftUI 下创建表格](https://www.fatbobman.com/posts/table_in_SwiftUI/ "用 Table 在 SwiftUI 下创建表格") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：Table 是 SwiftUI 3.0 中为 macOS 平台提供的表格控件，开发者通过它可以快捷地创建可交互的多列表格。在 WWDC 2022 中，Table 被拓展到 iPadOS 平台，让其拥有了更大的施展空间。本文将介绍 Table 的用法、分析 Table 的特点以及如何在其他的平台上实现类似的功能。

## 摸一下鱼

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

## 岗位推荐


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #57 | 周报改版，WWDC22 讲座集锦](https://mp.weixin.qq.com/s/e4ZbFBPqclgy7KyfxVyQZA)

[iOS 摸鱼周报 #56 | WWDC 进行时](https://mp.weixin.qq.com/s/ZyGV6WlFsZOX6Aqgrf1QRQ)

[iOS 摸鱼周报 #55 | WWDC 码上就位](https://mp.weixin.qq.com/s/zDhnOwOiLGJ_Nwxy5NBePw)

[iOS 摸鱼周报 #54 | Apple 辅助功能持续创新](https://mp.weixin.qq.com/s/6jdqa143Y5yr6lbjCuzlqA)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
