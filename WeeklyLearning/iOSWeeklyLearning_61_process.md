# iOS 摸鱼周报 #59

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：
> * 岗位推荐：

## 本期话题

###  Developer 设计开发加速器｜探索 Create ML Components

[@远恒之义](https://github.com/eternaljust)：本次活动将探索全新的 Create ML Components 框架，来配置更细颗粒度的机器学习任务。了解如何通过 Create ML Components 在图片类、列表类、视频类等任务上创建自定义模型，更好地配合您的使用场景。

活动将于 2022 年 8 月 2 日 (周二) 举办，完全免费，但仅限受邀开发人员参加。您可在您的开发团队中额外邀请最多 5 位成员参加，详情查看[设计开发加速器活动注册指南](https://essentials.applesurveys.com/WRQualtricsControlPanel_rel/File.php?F=F_a4rFfRXziNGhoAm "设计开发加速器活动注册指南")。活动注册截止日期为 2022 年 8 月 1 日，**报名地址**：https://developer.apple.com/events/view/upcoming-events。

## 本周学习

### 解决使用 AVAudioRecorder 录音保存 .WAV 文件遇到的问题

整理编辑：[FBY 展菲](https://github.com/fanbaoying)

#### 问题背景

App 实现录音保存音频文件，并实现本地语音识别匹配功能。

通过网络请求上传完成语音匹配的音频文件。

服务器接收到文件并进行语音识别，使用的是第三方微软语音识别，只支持 `PCM` 数据源的 `WAV` 格式。

本地识别没有任何问题，上传到服务器的文件无法识别，微软库直接报错。猜测上传的音频格式有误，导致的问题。

#### 问题代码

```objectivec
- (NSDictionary *)getAudioSetting {NSMutableDictionary *dicM=[NSMutableDictionary dictionary];
    // 设置录音格式
    [dicM setObject:@(kAudioFormatLinearPCM) forKey:AVFormatIDKey];
    // 设置录音采样率，8000 是电话采样率，对于一般录音已经够了
    [dicM setObject:@(16000) forKey:AVSampleRateKey];
    // 设置通道, 这里采用单声道 1 2
    [dicM setObject:@(2) forKey:AVNumberOfChannelsKey];
    // 每个采样点位数, 分为 8、16、24、32
    [dicM setObject:@(16) forKey:AVLinearPCMBitDepthKey];
    // 是否使用浮点数采样
    [dicM setObject:@(NO) forKey:AVLinearPCMIsFloatKey];
    //.... 其他设置等
    return dicM;
}
```

在没有使用微软语音识别库之前，使用上面的代码没有任何问题。识别库更新之后，不识别上传的的音频文件。

一开始以为是因为没有使用浮点数采样导致音频文件被压缩。修改后依然没有解决问题。

经过和服务器的联调，发现 .wav 音频文件的头部信息服务区无法识别。

#### 解决方案

当音频文件保存为 `.wav` 格式的时候，`iOS11` 以下的系统，`.wav` 文件的头部信息是没问题，但是在 `iOS11+` `.wav` 文件的头部信息服务区识别不了。

需要设置 `AVAudioFileTypeKey` 来解决这个问题。代码如下：

```objectivec
- (NSDictionary *)getAudioSetting {NSMutableDictionary *dicM=[NSMutableDictionary dictionary];
    // 设置录音格式
    [dicM setObject:@(kAudioFormatLinearPCM) forKey:AVFormatIDKey];
    if (@available(iOS 11.0, *)) {[dicM setObject:@(kAudioFileWAVEType) forKey:AVAudioFileTypeKey];
    } else {// Fallback on earlier versions}
    // 设置录音采样率，8000 是电话采样率，对于一般录音已经够了
    [dicM setObject:@(16000) forKey:AVSampleRateKey];
    // 设置通道, 这里采用单声道 1 2
    [dicM setObject:@(2) forKey:AVNumberOfChannelsKey];
    // 每个采样点位数, 分为 8、16、24、32
    [dicM setObject:@(16) forKey:AVLinearPCMBitDepthKey];
    // 是否使用浮点数采样
    [dicM setObject:@(NO) forKey:AVLinearPCMIsFloatKey];
    //.... 其他设置等
    return dicM;
}
```

参考：[解决使用 AVAudioRecorder 录音保存 .WAV 文件遇到的问题 - Swift 社区](https://mp.weixin.qq.com/s/MZqpzCAkWE9gGpsAYyo_aw "解决使用 AVAudioRecorder 录音保存 .WAV 文件遇到的问题 - Swift 社区")

## 内容推荐

1、[SwiftUI中的后台任务](https://swiftwithmajid.com/2022/07/06/background-tasks-in-swiftui/ "SwiftUI中的后台任务") -- 来自：Majid

[@东坡肘子](https://www.fatbobman.com/)：苹果随着 iOS 13 一起发布了一个 BackgroundTasks 框架。该框架允许开发者使用代码在后台智能地安排工作。在 SwiftUI 4.0 中，苹果又新增了 backgroundTask 视图修饰器，进一步降低了使用后台框架的难度。Majid 将通过本文介绍如何在 SwiftUI 中安排和处理后台任务。

2、[SwiftUI 布局 —— 尺寸](https://www.fatbobman.com/posts/layout-dimensions-1/ "SwiftUI 布局 —— 尺寸") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：在 SwiftUI 中，尺寸这一布局中极为重要的概念，似乎变得有些神秘。无论是设置尺寸还是获取尺寸都不是那么地符合直觉。本文将从布局的角度入手，为你揭开盖在 SwiftUI 尺寸概念上面纱，了解并掌握 SwiftUI 中众多尺寸的含义与用法；并通过创建符合 Layout 协议的 frame 和 fixedSize 视图修饰器的复制品，让你对 SwiftUI 的布局机制有更加深入地理解。

3、[WWDC 2022 数字会客室中有关 Core Data 的内容](https://useyourloaf.com/blog/wwdc22-core-data-lab-notes/ "WWDC 2022 数字会客室中有关 Core Data 的内容") -- 来自：Keith Harrison

[@东坡肘子](https://www.fatbobman.com/)：在 WWDC 2022 中，虽然苹果没有为 Core Data 增加新的功能，但这并不意味着 Core Data 在苹果生态中变得不那么重要。Keith Harrison 整理了在 WWDC 2022 数字会客室中有关 Core Data 方面的一些讨论，主要涉及：数据同步、异步加载等方面的内容。

4、[Bottom Sheet in SwiftUI on iOS 16 with presentationDetents modifier](https://sarunw.com/posts/swiftui-bottom-sheet/ "Bottom Sheet in SwiftUI on iOS 16 with presentationDetents modifier") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：底部表单(Bottom Sheet)是一种类似 Apple 地图主页面拖动的控件，你可以从设备屏幕底部向上滑动，来调整页面内容的显示大小。在 iOS 15 UIKit 中，Apple 推出了 `UISheetPresentationController`，支持展示 `.medium` 和 `.large` 两种形态。今年，iOS 16 SwiftUI 推出了 `presentationdetents` 修饰符，除了支持之前的大中尺寸，新的修饰符还升级了三种设置方式：固定高度(`.height`)，分数(`.fraction`)以及自定义高度逻辑(`.custom`)。

5、[利用新的 ImageRenderer API 輕鬆把 SwiftUI 視圖轉換為圖像](https://www.appcoda.com.tw/imagerenderer-swiftui/ "利用新的 ImageRenderer API 輕鬆把 SwiftUI 視圖轉換為圖像") -- 来自：Simon Ng

[@远恒之义](https://github.com/eternaljust)：iOS 16 SwiftUI 新推出了 `ImageRenderer`。利用这个 API，我们可以轻松把 SwiftUI 中的视图转换为图像，再保存这个图像到系统相册中。同时，分享视图转换后的图像也是轻而易举的操作。此外，通过设置 `ImageRenderer` 类别中的 `scale` 属性，你还可以调整渲染图像的比例，从而提高图像的解析度。

## 摸一下鱼

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1. [JSON Hero](https://github.com/jsonhero-io/jsonhero-web)，一款让你轻松直观地查看 JSON 文档的工具，为你提供类似 Mac Finder 体验的工具。

   ![](https://raw.githubusercontent.com/jsonhero-io/documentation-hosting/main/images/features-treeview.gif)

   如果你的 JSON 文件足够庞大，这款软件必不可少。

2. [SingleFile](https://github.com/gildas-lormeau/SingleFile)是一种 Web 扩展（和 CLI 工具），与Chrome、Firefox（桌面和移动）、Microsoft Edge、Vivaldi、Brave、Waterbox、Yandex browser 和 Opera 兼容。它可以帮助您将完整的网页保存到单个 HTML 文件中。

3. [State-of-the-Art Shitcode Principles](https://github.com/trekhleb/state-of-the-art-shitcode) 这是一个`Shitcode`书写准则.

4. [This-repo-has-N-stars](https://github.com/fslongjin/This-repo-has-838-stars) 如项目名称所示，这个项目有 N 个 Star，当 Star 的数量发生改变时，项目名称会被动态地更新。

5. [摸鱼游戏](https://moyu.games) 可能是一个全方位的摸鱼指南，无论你是想休闲娱乐还是需要学习，都能给你提供不一样内容。

   

## 岗位推荐



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS 成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #56 | WWDC 进行时](https://mp.weixin.qq.com/s/ZyGV6WlFsZOX6Aqgrf1QRQ)

[iOS 摸鱼周报 #55 | WWDC 码上就位](https://mp.weixin.qq.com/s/zDhnOwOiLGJ_Nwxy5NBePw)

[iOS 摸鱼周报 #54 | Apple 辅助功能持续创新](https://mp.weixin.qq.com/s/6jdqa143Y5yr6lbjCuzlqA)

[iOS 摸鱼周报 #53 | 远程办公正在成为趋势](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
