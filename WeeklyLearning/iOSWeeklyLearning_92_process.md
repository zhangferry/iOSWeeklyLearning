# iOS 摸鱼周报 #90

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [线上讲座：让你的 App 更加无障碍](https://developer.apple.com/events/view/7F793DZPF3/dashboard "线上讲座：让你的 App 更加无障碍")

[@远恒之义](https://github.com/eternaljust)：Apple 非常关注“有障碍”群体在使用苹果设备上的无障碍使用体验，推出了许多个性化的[辅助功能](https://www.apple.com.cn/accessibility/ "辅助功能")，其中最广为人知的是 Voice Over “旁白”功能。旁白是一种基于手势的屏幕阅读器，适用于失明或弱视用户，为其提供语音播报内容。Apple 针对听障群体强化了视觉反馈，可以通过 iPhone 震动或者快速闪烁的 LED 灯来接受提醒消息。此外，当设备识别到特殊的声音或警示音时，用户也会收到视觉提醒和振动通知。

在本次线上讲座中，你将了解如何通过 Apple 操作系统提供的无障碍功能、无障碍 API 和开发者工具，来为每一个人打造卓越的用户体验。参加本次线上讲座，你还能在当天报名参与无障碍适配挑战活动，有机会通过审核并参加 5 月 18 日在上海设计与开发加速器举办的无障碍宣传日线下活动。活动时间 2023 年 5 月 10 日上午 10:00 – 中午 11:00，报名截止时间 2023 年 5 月 9 日前。

### [Swift 社区开源了基于 Swift 实现的 Foundation 预览版](https://github.com/apple/swift-foundation "Swift 社区开源了基于 Swift 实现的 Foundation 预览版")

[@东坡肘子](https://www.fatbobman.com/)：几个月前，Swift 社区提出了一个计划，即基于 Swift 实现 Foundation，以改善 Swift 的跨平台开发。现在，这个计划已经得到了很好的落实。这个软件包提供了更快、更安全的 Foundation 实现，并设立了一个新的 Foundation 工作组来协调 Swift 社区的需求和苹果工程的需要。新 Foundation 构建了许多类型的 Swift 实现，包括 JSONEncoder、Calendar、TimeZone 和 Locale 等，还有一个名为 FoundationICU 的单独软件包，用于在非 Darwin 平台上提供国际化支持。这个新实现在 JSON 解码和日期格式化等多方面比之前的 C 和 Objective-C 版本显著提高了性能。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

推荐近期的一些优秀博文，涵盖：Mirror API、网络可达性优化、SwiftLint 等方面的内容。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[深入了解 SwiftLint](https://www.kodeco.com/38422105-swiftlint-in-depth "深入了解 SwiftLint") -- 作者：Ehab Amer

[@东坡肘子](https://www.fatbobman.com/): 该文为使用 SwiftLint 进行 iOS 开发提供了全面的指南。其中详细介绍了如何使用 SwiftLint，包括构建规则文件、排除文件和文件夹、禁用和配置规则、修复违规、创建自定义规则等。此外，还介绍了如何使用远程规则来进行集中管理以及其他的一些技巧和注意事项，以帮助开发者更好地使用 SwiftLint，并避免一些常见的陷阱。

2、[针对网络可达性优化应用](https://www.avanderlee.com/swift/optimizing-network-reachability/ "针对网络可达性优化应用") -- 作者：ANTOINE VAN DER LEE

[@东坡肘子](https://www.fatbobman.com/): 当开发应用程序时，需要重视网络可达性，因为不是所有用户都拥有良好的互联网连接。因此，优化应用程序以适应不良的网络条件是必要的。在本文中，作者认为在发出请求之前预先检查可达性并不是推荐的方式。相反，配置你的网络层等待连接，并仅允许某些类型的连接可能是更好的选择。该文章还介绍了如何根据返回的错误更新用户界面以响应网络错误，如何使用 NWPathMonitor 检查恢复的连接性，以及如何使用 RocketSim 的网络扩展创建稳定的测试环境。

3、[使用 Swift 的反射功能](https://useyourloaf.com/blog/using-swift-reflection/ "使用 Swift 的反射功能") -- 作者：Keith Harrison

[@东坡肘子](https://www.fatbobman.com/): 许多开发者可能认为自己并没有多少机会使用到 Swift 的反射功能，但在实际开发中，它其实可以发挥重要作用。本文介绍了如何使用 Mirror API 迭代结构体的属性并检查它们是否为非空字符串，以及如何使用它来断言特定的字符串属性的方法是否正确工作。通过这些演示，我们可以重新审视反射功能，并在日常开发中更好地应用它。

4、[使用 SwiftUI 开发 RSS 阅读器](https://ming1016.github.io/2023/04/24/swiftui-rss-reader/ "使用 SwiftUI 开发 RSS 阅读器") -- 作者：戴铭

[@东坡肘子](https://www.fatbobman.com/): 本文是作者参加苹果举办的 SwiftUI 技术沙龙交流会后对内容进行的整理。文章介绍了一个使用 SwiftUI 和 Core Data 实现的 RSS 阅读器应用。其中分享了许多实现细节，比如去重、批量插入、iCloud 同步和数据索引等。该应用通过 NavigationSplitView 实现了 iPad 和 macOS 下的多窗口布局模式，并自定义了用于数据提取的 Controller。最终创建出一个功能齐全的 RSS 阅读器应用。

5、[打造可适配多平台的 SwiftUI 应用](https://www.fatbobman.com/posts/building-multiple-platforms-SwiftUI-App/ "打造可适配多平台的 SwiftUI 应用") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 在构建适用于多个平台的 SwiftUI 应用程序时，提前考虑兼容性和数据源问题非常重要。为了避免重复的代码调整，开发人员可以预先创建一些辅助代码用于所有需要适配的平台。对于数据源，开发者应该考虑哪些状态是整个应用的全局状态，哪些状态仅限于当前场景（窗口）。通过提前了解和规划这些问题，开发者可以节省花费在适配多平台上的时间，将更多的精力用于创建能够凸显平台特点的产品。同上文一样，本文也是作者在参加 SwiftUI 技术沙龙后对交流内容的整理。


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
