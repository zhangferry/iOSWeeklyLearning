# iOS 摸鱼周报 #74 | 待定

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：iOS NSDateFormatter 设置问题 & iOS 16 部分 pods 库签名问题
> * 内容推荐：SPM 工程实践以及性能优化好文推荐
> * 摸一下鱼：本期推荐一款跨平台的摸鱼网站、和两款坐姿监控 APP，摸鱼的时候也不要忘记保持正确坐姿；一个根据年历、地图、人物等生成文学图谱的网站；帮助从 intel 平缓过渡到苹果自研 M 系列芯片的软件检测 app。

## 本期话题



## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### iOS NSDateFormatter 设置问题

最近在项目里遇到了一些时间格式的问题，场景是用户在关闭了系统时间 24 小时制的时候，以下代码会表现出不一样的执行结果：

```objective-c
NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
dateFormatter.dateFormat = @"yyyyMMddHH";
dateFormatter.timeZone = [NSTimeZone timeZoneWithName:@"Asia/Shanghai"];
NSString *dateString = [dateFormatter stringFromDate:[NSDate date]];

// 开启 24 ： 2022110123
// 关闭 24： 2022110111 PM
```

即使 `Formatter` 设置了 `HH` 格式，仍然按照 12 小时制打印结果。并没有强制 24 时间制输出。

问题原因总结为：用户的时间设置对 `Formatter`格式产生了影响。

通过查阅资料 [NSDateFormatter-Apple Developer](https://developer.apple.com/documentation/foundation/nsdateformatter "NSDateFormatter-Apple Developer")  有这样一段描述：

> When working with fixed format dates, such as RFC 3339, you set the [`dateFormat`](https://developer.apple.com/documentation/foundation/nsdateformatter/1413514-dateformat) property to specify a format string. For most fixed formats, you should also set the [`locale`](https://developer.apple.com/documentation/foundation/nsdateformatter/1411973-locale) property to a POSIX locale (`"en_US_POSIX"`), and set the [`timeZone`](https://developer.apple.com/documentation/foundation/nsdateformatter/1411406-timezone) property to UTC.

当需要设置自定义格式时，除了需要设置 `dateFormat`属性，还需要设置时区 `timeZone`和环境 `locale`属性。`locale`属性可以强制指定环境变量，避免用户自定义的系统设置对时间格式造成影响。

另外 [qa1480-apple](https://developer.apple.com/library/archive/qa/qa1480/_index.html "qa1480-apple") 中也明确说明了，自定义格式会被用户设置影响，诸如日历、小时制等本地环境。

该 QA 中还明确指导了`NSDateFormatter`的使用场景：

- 用于用户可见的时间显示
- 用于配置和解析固定格式的时间数据

对于前者，苹果不建议自定义 `dateFormat`，因为不同的地区用户，时间格式习惯是不同的，建议使用系统的预留格式，例如`setDateStyle` 和 `setTimeStyle`等。

如果是后者，则建议明确指定 `locale`属性，并且还就 `en_US`和 `en_US_POSIX`两个 **LocaleIdentifier** 的区别做了解释。

最终解决方案也就确定了，指定 `locale`属性即可。

```objective-c
  dateFormatter.locale = [NSLocale localeWithLocaleIdentifier:@"en_US_POSIX"];
```

总结：该类问题都是对 API 使用不规范导致的，类似前几年的`yyyy `和 `YYYY`的问题。大部分场景结果是一致的，特定 case 才会触发不一样的结论，导致日常很难发现这类问题。

### iOS 16 部分 pods 库提示签名问题

在最近通过 `cocoapods`导入部分库的时候，会提示签名的 error，以我业务中使用的 Google SDK 为例：

**xxx/Pods/Pods.xcodeproj: error: Signing for "GoogleSignIn-GoogleSignIn" requires a development team. Select a development team in the Signing & Capabilities editor. (in target 'GoogleSignIn-GoogleSignIn' from project 'Pods')**

解决方案也很简单，可以手动选择一下签名证书，这种需要每次 install 后手动更改，比较繁琐，另外一种方式是通过 `pod hook`关闭该签名配置项:

```ruby
post_install do |installer|
  installer.pods_project.targets.each do |target|
    target.build_configurations.each do |config|
      config.build_settings['CODE_SIGNING_ALLOWED'] = "NO"
    end
  end
end
 
```

目前该问题只出现在Xcode 14及以上的版本中，最新的 Xcode 14.1 release 仍未解决该问题。


## 内容推荐

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

1、[SwifterSwift](https://github.com/SwifterSwift/SwifterSwift) -- github

[@夏天](https://juejin.cn/user/3298190611456638): SwifterSwift 是 **500 多个原生 Swift 扩展的集合**，为 iOS、macOS、tvOS、watchOS 和 Linux 提供了（超过 500 个）适用于各种原生数据类型、UIKit 和 Cocoa 类的便捷方法、语法糖和性能改进。

![](https://cdn.zhangferry.com/Images/SwifterSwift.png)

2、[货拉拉用户 iOS 端卡顿优化实践](https://juejin.cn/post/7160951025782751263 "货拉拉用户 iOS 端卡顿优化实践") -- 货拉拉技术

[@Mimosa](https://juejin.cn/user/1433418892590136)：卡顿优化一直是客户端性能治理的重要方向之一，优化卡顿，将 APP 的用户体验做到极致，在一定程度上能够提升用户的忠诚度和 APP 的市场占有率。本文是货拉拉技术通过检测卡顿以及对卡顿的治理实践的记录，同时也总结了一些在编码阶段就规避卡顿的方法。

3、[云音乐 iOS 端代码静态检测实践](https://mp.weixin.qq.com/s/5ZcGBCnrUYwUA0RXyPJt9w "云音乐iOS端代码静态检测实践") -- 网易云音乐技术团队

[@Mimosa](https://juejin.cn/user/1433418892590136)：本文是网易云音乐技术团队保障代码质量、防止代码劣化的一套静态代码检测实践，文中代码详尽，步骤也很清晰地记录了通过定制 OCLint 并自定义规则、优化静态检测耗时的过程。

4、[Swift Package Manager 工程实践](https://mp.weixin.qq.com/s/q7jolU99K7FI9JvAxjwRwg “Swift Package Manager 工程实践”) -- 狐友技术团队

[@Mimosa](https://juejin.cn/user/1433418892590136)：本文将详细介绍狐友团队在引入 Swift Package Manager 进行工程实践中，探索和累积的相关知识和实践经验，我们将从结构设计、资源处理、链接方式的选择、编译与链接参数设置、异常处理，这五个方面展开详细介绍，每个小部分结尾都提供了最佳实践的总结。

5、[5-Second Test](https://babich.biz/5-second-test-in-product-design/ “5-Second Test”) -- Nick Babich

[@Mimosa](https://juejin.cn/user/1433418892590136)：5 秒测试是一个简单的练习，可以帮助衡量用户对您的设计的第一印象。本文是有关如何使用此类测试的快速指南，对于 app 开发来说，对我们的产品设计有点作用。

6、[百度APP iOS端内存优化实践-内存管控方案](https://mp.weixin.qq.com/s/dETOGD3NYU2SdZhxGu0SZg) --  百度App技术

[@Hello World](https://juejin.cn/user/2999123453164605/posts): 内存问题是业务开发中经常被忽视的问题，恰恰它又是很多 Crash 的罪魁祸首。例如 OOM Crash，如何治理内存成了开发中的重要一环。本文从基础原理出发讲述了如何监控内存。并从源码角度分析了应该如何选取内存指标作为衡量的阈值。

## 摸一下鱼

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1. [知识图谱](https://cnkgraph.com)：一个根据年历、地图、人物等生成文学图谱。关于本月的相关文献，关于本地的相关诗词，关于某地的相关文档。

没事的时候准备准备，有可能用的上。

![](https://cdn.zhangferry.com/Images/知识图谱.png)

2. [Thief](https://github.com/cteamx/Thief): 作者说这是**一款真正的创新摸鱼神器**。一款创新跨平台摸鱼神器，支持小说、股票、网页、视频、直播、PDF、游戏等摸鱼模式，为上班族打造的上班必备神器，使用此软件可以让上班倍感轻松，远离 ICU。
3. [iMobie M1 App Checker](https://www.imobie.com/m1-app-checker/ "iMobie M1 App Checker"): 这款应用由专注于 Apple 领域 10 年的 iMobie 团队打造，旨在为所有需要平稳过渡到苹果自研 Mx 芯片的用户提供帮助，可以实现对所有已安装 App 的 CPU 类型检测，同时提供检查 iOS 应用是否可以安装到 Mac 端。
4. [pose-monitor](github.com/linyiLYi/pose-monitor "pose-monitor"): 国内开发者在 GitHub 开源的一款 Android 应用：「PoseMon 让爷康康」，可借助 AI 技术，实时监测不良坐姿，并及时给出语音提示。应用不需要联网使用，所有 AI 特性均在手机本地运行，不需要将视频画面传输至外部服务器，仅需要摄像头权限用于获取姿态画面。
5. [顶瓜瓜](https://apps.apple.com/cn/app/id1629577265 “顶瓜瓜”)：顶瓜瓜是一款检测头部位置、帮助保持坐姿的 App。将设备放在桌上，打开摄像头，即可开始坐姿守护。你会化身为一只头顶西瓜的动物，当你低头、歪头时，西瓜会掉下来。功能通过设备的原深感相机（True Depth Camera）实现，无需购买其他智能硬件，无需穿戴、无接触。无需联网，全部本地计算，保护您的隐私！

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #73 | macOS Ventura 初体验](https://mp.weixin.qq.com/s/Om_1TOGKWkMiNneB6Ittrw)

[iOS 摸鱼周报 #72 | 1024 开始预热](https://mp.weixin.qq.com/s/WUVAHbJe_dmA-DVFXpF2Qw)

[iOS 摸鱼周报 #71 | iOS / One More Thing?](https://mp.weixin.qq.com/s/0mAKYvVuPLKEA2qnsNfCvQ)

[iOS 摸鱼周报 #70 | iOS / iPadOS 16.1 公测版 Beta 3 发布，支持老款 iPad 台前调度](https://mp.weixin.qq.com/s/rSPC8lgvUKPKfgR53xdHqg)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
