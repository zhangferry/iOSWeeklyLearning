# iOS 摸鱼周报 #61 |  Developer 设计开发加速器

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题： Developer 设计开发加速器｜探索 Create ML Components
> * 本周学习：解决使用 AVAudioRecorder 录音保存 .WAV 文件遇到的问题
> * 内容推荐：SwiftUI 本周好文推荐
> * 摸一下鱼：摸鱼网站推荐

## 本期话题

###  Developer 设计开发加速器｜探索 Create ML Components

[@远恒之义](https://github.com/eternaljust)：本次活动将探索全新的 Create ML Components 框架，来配置更细颗粒度的机器学习任务。了解如何通过 Create ML Components 在图片类、列表类、视频类等任务上创建自定义模型，更好地配合您的使用场景。

活动将于 2022 年 8 月 2 日 (周二) 举办，完全免费，但仅限受邀开发人员参加。您可在您的开发团队中额外邀请最多 5 位成员参加，详情查看[设计开发加速器活动注册指南](https://essentials.applesurveys.com/WRQualtricsControlPanel_rel/File.php?F=F_a4rFfRXziNGhoAm "设计开发加速器活动注册指南")。活动注册截止日期为 2022 年 8 月 1 日，**报名地址**：https://developer.apple.com/events/view/upcoming-events。

### [即将从 XML Feed 过渡到 App Store Connect API](https://developer.apple.com/cn/news/?id=yqf4kgwb "即将从 XML Feed 过渡到 App Store Connect API")

[@师大小海腾](https://juejin.cn/user/782508012091645/posts)：App Store Connect REST API 让您可以跨各种开发者工具自定义任务并实现任务自动化，使工作流程更灵活、更高效。从 2022 年 11 月开始，您将需要使用此 API 来代替 XML Feed，从而实现对 App 内购买项目、订阅、元数据和 App 定价的自动化管理。XML Feed 将继续为现有的 Game Center 管理功能提供支持。

### [Apple 介绍如何通过健康信息为用户赋能](https://www.apple.com.cn/newsroom/2022/07/how-apple-is-empowering-people-with-their-health-information/ "Apple 介绍如何通过健康信息为用户赋能")

[@师大小海腾](https://juejin.cn/user/782508012091645/posts)：Apple 于 7 月 20 日公布了一份新报告，简要介绍 Apple 产品帮助用户掌控自身健康，担当用户健康与安全智能守护者的多种方式。全球各地的用户、开发者、医疗机构与保健组织正在使用 Apple 设备、功能与 API 帮助人们消除获取自身健康信息的障碍，同时严格保障个人隐私。

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

6、[信息安全 | 互联网时代，如何建立信任？](https://mp.weixin.qq.com/s?__biz=Mzg3MjcxNzUxOQ==&mid=2247484972&idx=1&sn=4f0d819e8ab9456bd2ee81942abb3f22&chksm=ceea4b8cf99dc29ad27798c860c9db89621d81497fb6a5d206ed0602d75cffbb1bfdbec5809a&token=2062691669&lang=zh_CN#rd) -- 来自公众号：Bo2SS

[@doubleLLL3](https://github.com/doubleLLL3)：文章从信息安全是什么说起，到为什么，到怎么做，脉络清晰，层层递进，最后还聊了一些相关的应用加深理解。

通过文章可以让读者回答并理解以下问题：

1）信息传输一般使用对称加密+非对称加密，为什么？不能只使用其中一种吗？

2）信息安全为什么需要数字签名？

3）为什么签名前需要做哈希操作？

4）信息安全为什么需要数字证书？

文章的终极目标是：当我们在遇到密码学相关问题时，不再恐惧和迷惑。

## 摸一下鱼

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1. [JSON Hero](https://github.com/jsonhero-io/jsonhero-web "JSON Hero")，一款让你轻松直观地查看 JSON 文档的工具，为你提供类似 Mac Finder 体验的工具。

   ![](https://cdn.zhangferry.com/Images/features-treeview.gif)

   如果你的 JSON 文件足够庞大，这款软件必不可少。

2. [SingleFile](https://github.com/gildas-lormeau/SingleFile "SingleFile")是一种 Web 扩展（和 CLI 工具），与Chrome、Firefox（桌面和移动）、Microsoft Edge、Vivaldi、Brave、Waterbox、Yandex browser 和 Opera 兼容。它可以帮助您将完整的网页保存到单个 HTML 文件中。

3. [State-of-the-Art Shitcode Principles](https://github.com/trekhleb/state-of-the-art-shitcode "State-of-the-Art Shitcode Principles") 这是一个`Shitcode`书写准则，来学习下「垃圾」代码的艺术。

   ```swift
   /// 💩 Mix variable/functions naming style
   
   ///Good 👍🏻
   let wWidth = 640;
   let w_height = 480;
   
   ///Bad 👎🏻
   let windowWidth = 640;
   let windowHeight = 480;
   ```

4. [This-repo-has-N-stars](https://github.com/fslongjin/This-repo-has-838-stars "This-repo-has-N-stars") 如项目名称所示，这个项目有 N 个 Star，当 Star 的数量发生改变时，项目名称会被动态地更新。

5. [摸鱼游戏](https://moyu.games "摸鱼游戏") 可能是一个全方位的摸鱼指南，无论你是想休闲娱乐还是需要学习，都能给你提供不一样内容。

6. [Qwerty Learner](https://qwerty.kaiyi.cool/ "Qwerty Learner")：练打字，学英语，学编程词汇，一个网站全搞定w(ﾟДﾟ)w

   ![](https://cdn.zhangferry.com/Images/20220721230920.png)

7. Apple 全系系统迎来了一波更新，最新版本如下：

   | OS      | Version | Build |
   | ------- | ------- | ----- |
   | iOS     | 15.6    | 19G71 |
   | iPadOS  | 15.6    | 19G71 |
   | macOS   | 12.5    | 21G72 |
   | watchOS | 8.7     | 19U66 |
   | tvOS    | 15.6    | 19M65 |

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS 成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/Sv3goAv198eXjmlVJsN1rw)

[iOS 摸鱼周报 #59 | DevOps 再理解 ](https://mp.weixin.qq.com/s/LJNCo0Eg11shGZN75-TZcg)

[iOS 摸鱼周报 #58 | 极客风听歌网站，纯文字音乐播放器](https://mp.weixin.qq.com/s/KwqFraJk40f9bEy0eKa8Kw)

[iOS 摸鱼周报 #57 | 周报改版，WWDC22 讲座集锦](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
