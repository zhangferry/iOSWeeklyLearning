# iOS 摸鱼周报 #90

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [Apple 展示无障碍软件辅助新功能](https://www.apple.com.cn/newsroom/2023/05/apple-previews-live-speech-personal-voice-and-more-new-accessibility-features/ "Apple 展示无障碍软件辅助新功能")

[@远恒之义](https://github.com/eternaljust)：Apple 一直秉承制造所有人都能顺畅使用产品的理念，为迎接本周四的全球无障碍宣传日（每年五月第三个星期四），展示了一套为认知能力、视力、听力与肢体活动能力而设计的软件辅助功能。这些功能将于今年晚些时候推出，预计会在秋季的 iOS 17 正式版系统中上线。

针对有认知障碍的用户，Apple 推出 Assistive Access，把电话、信息、相机、照片与音乐等 App 整合为一个单独的 App，并提炼出这些常用 App 的基本功能，以减轻用他们的认知负担。这相当于是系统层级的长辈模式，简化原本复杂的交互逻辑，突出放大文字按钮操作。

对于有语言能力障碍的用户，通过 Live Speech 新功能，他们可以在 iPhone 上打电话时键盘输入文字，当前设备会将文字转成语音并朗读出来。此外，对于面临失语风险的用户，他们可使用 iPhone 录制 15 分钟的音频，通过机器学习的 Personal Voice 技术，创建与自己嗓音相似的 AI 语音，后续就能使用此语音进行文字朗读。

面对失明或低视力用户，iPhone 内置的放大器将新增 Point and Speak 功能，结合相机与激光雷达扫描，视障用户在使用微波炉等家用电器时，iPhone 能识别在按键区移动的手指，朗读出手指指向按键上的功能文字。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

推荐近期的一些优秀博文，涵盖：#file 的行为变更、如何使用 @_exported 属性、In-App Purchase 实践总结等方面的内容。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[使用 @_exported 属性避免大规模重构](https://www.polpiella.dev/how-we-avoided-a-big-refactor-with-the-exported-attribute "使用 @_exported 属性避免大规模重构") -- 作者：Pol Piella Abadia

[@东坡肘子](https://www.fatbobman.com/): 本文介绍了如何在实际项目中使用 Swift 的 @_exported 属性，以最小化变更的影响并降低引入错误的风险。文章提供了一个用例，其中 @_exported 属性被用来减少重构所影响的文件数量。这种方法的优点是可以减少应用程序中的更改数量，从而降低引入错误的风险。尽管这种方法对于特定的用例非常有效，但在 Swift 单库之外使用 @_exported 属性是不被鼓励的。因此，在使用此方法时，需要仔细考虑其长期影响，并确保使用此属性的场景是必要的，并且仅在必要时使用。

2、[Swift 5.8 中 #file 的行为变更](https://sarunw.com/posts/file-behavior-change/ "Swift 5.8 中 #file 的行为变更") -- 作者：Sarunw

[@东坡肘子](https://www.fatbobman.com/): Swift 5.8 带来了 #file 字面表达式行为的新变化，本文对此进行了介绍。在之前的版本中，#file 和 #filePath 返回相同的结果，即它所在文件的路径。然而，在 Swift 5.8 中，#file 已经被修改为仅返回文件名和模块，而不包括路径。由于这个变化是一项破坏性变化，可能会影响当前代码，在默认情况下该行为被禁用，用户需要使用特性标志启用它（在 Swift 6 中将强制开启）。为了更具体地描述这个行为，开发人员还可以使用 #filePath 和 #fileID 字面表达式。前者返回它所在文件的路径，而后者返回文件名和模块。

3、[云音乐中 In-App Purchase 实践总结篇](https://juejin.cn/post/7233948883045941303 "云音乐中 In-App Purchase 实践总结篇") -- 作者：0linatan0 网易云音乐技术团队

[@东坡肘子](https://www.fatbobman.com/): IAP 的使用曾经备受开发者批评，其中包括商品创建流程过于繁琐和接入自动续费时遇到的许多问题。本文总结了网易云音乐在 In-App Purchase 实践中遇到的问题以及解决方案，包括票据验证、自动续费、退款等内容。作者还介绍了他们开发的基础库 NEStoreKit。通过对业务流程进行抽象，各团队可以快速接入，从而保障支付履约完成、完善交易场景并记录各交易日志。

4、[WWDC 2023，我期待 Core Data 带来的新变化](https://www.fatbobman.com/posts/What-I-Hope-to-See-for-Core-Data-at-WWDC-2023/ "WWDC 2023，我期待 Core Data 带来的新变化") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 本文列举了作者期待在 WWDC 2023 中看到 Core Data 带来的新变化。其中包括传说中的 Swift 重制版（尽管可能性极低）、用 Swift 重制部分 API、支持更多 SQLite 新特性、更好的 Model Editor 体验、完善 Core Data with CloudKit 的部分 API 以及改善 Core Data with CloudKit 的同步表现。作者希望苹果能够继续发扬这个拥有悠久历史的框架，焕发其第二春。

5、[macOS Swift 原生项目集成 Python3 运行环境](https://juejin.cn/post/7229310327268032569 "macOS Swift 原生项目集成 Python3 运行环境") -- 作者：别nil了

[@东坡肘子](https://www.fatbobman.com/): 与 Swift 相比，Python 拥有更多的第三方库。如果能在 Swift 中使用这些库，开发者可以节省大量时间和精力。本文介绍了在 macOS Swift 原生项目中集成 Python3 运行环境的方法，内容涉及：设置 Python.xcframework、添加 SystemConfiguration.Framework、检查 python-stdlib、创建 Python 头文件、添加 Run Script、检查 Python3 运行环境、使用 pip3 安装第三方依赖库、Python 第三方依赖库的调用方法等方面，并对有关 App Store 审核和打包的 bug 等内容也做了探讨。

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
