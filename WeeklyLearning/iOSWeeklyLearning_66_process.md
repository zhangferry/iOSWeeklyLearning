# iOS 摸鱼周报 #64 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：Shazam 迎来问世 20 周年
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [Shazam 迎来问世 20 周年](https://www.apple.com.cn/newsroom/2022/08/shazam-turns-20/ "Shazam 迎来问世 20 周年")

[@远恒之义](https://github.com/eternaljust)：Shazam 是一款歌曲识别 App，适用于所有的 Apple 设备上。你可以使用 Shazam 快速查找几乎任何歌曲，识别 App 中播放或者通过耳机播放的音乐，也能通过快捷指令和控制中心使用 Shazam 识别歌曲，同时可以在 Apple Music 中打开已识别的歌曲，更多实用技巧可查看 [Shazam 使用手册](https://support.apple.com/zh-cn/guide/shazam-iphone/welcome/ios "Shazam 使用手册")。

![控制中心使用 Shazam 识别歌曲](https://cdn.zhangferry.com/Images/shazam-music.png)

2018 年 9 月 Shazam 加入了 Apple 家庭，在 WWDC21 中 Apple 推出了 [ShazamKit](https://developer.apple.com/cn/shazamkit/ "ShazamKit")。借助 ShazamKit，可以为你的 App 增加音频识别功能。将音乐与 Shazam 庞大乐库中的数百万首歌曲进行匹配，或者使用视频和播客等来源中的音频创建你自己的自定义乐库，帮助用户轻松识别任何预录制的音频。

以下是 Shazam 20 年来历史上的重要时刻与里程碑事件。

* 2002 年 8 月：Shazam 作为一项短信服务在英国推出。当时，用户需要在电话上拨打“2580”，然后将听筒对准音源。不久后，他们会收到一条短信，获悉歌曲名称与艺人姓名。
* 2008 年 7 月：Shazam app 在全新的 App Store 上发布。2008 年 10 月，Shazam 发布 Android 版本。
* 2015 年 4 月：Shazam app 在第一代 Apple Watch 上发布。
* 2018 年 9 月：Shazam 加入 Apple 家庭。
* 2021 年 6 月：Shazam 月度识别次数首次超过 10 亿次。
* 2022 年 5 月：Shazam app 总安装次数超过 20 亿次。
* 2022 年 8 月：Shazam 庆祝 20 年音乐发现之旅，且突破 700 亿次歌曲识别。

### [App 和 app 内购买项目即将实行税率和价格调整](https://developer.apple.com/cn/news/?id=l42tc8ie "App 和 app 内购买项目即将实行税率和价格调整")

[@远恒之义](https://github.com/eternaljust)：从本周开始，加纳和土耳其 App Store 的 App 及 App 内购买项目 (自动续期订阅除外) 的价格将有所提高。加纳的价格提升将包含 12.5% 的新增值税和 6% 的附加税。此外，如果你在 App Store Connect 中选择了适当的税收类别，爱沙尼亚的电子出版物的收益会进行调整，增值税从 9% 下调至 5%。

## 本周学习

整理编辑：[FBY 展菲](https://github.com/fanbaoying)

### 如何将 NSImage 转换为 PNG

首先创建 `NSBitmapImageRep` 尺寸，并在上面绘制 `NSImage`。`NSBitmapImageRep` 需要专门构建，不是直接使用 `NSBitmapImageRep(data:)` 初始化，`NSBitmapImageRep(cgImage:)` 可以避免一些分辨率问题。

```Swift
extension NSImage {
    func pngData(
        size: CGSize,
        imageInterpolation: NSImageInterpolation = .high
    ) -> Data? {
        guard let bitmap = NSBitmapImageRep(
            bitmapDataPlanes: nil,
            pixelsWide: Int(size.width),
            pixelsHigh: Int(size.height),
            bitsPerSample: 8,
            samplesPerPixel: 4,
            hasAlpha: true,
            isPlanar: false,
            colorSpaceName: .deviceRGB,
            bitmapFormat: [],
            bytesPerRow: 0,
            bitsPerPixel: 0
        ) else {
            return nil
        }

        bitmap.size = size
        NSGraphicsContext.saveGraphicsState()
        NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
        NSGraphicsContext.current?.imageInterpolation = imageInterpolation
        draw(
            in: NSRect(origin: .zero, size: size),
            from: .zero,
            operation: .copy,
            fraction: 1.0
        )
        NSGraphicsContext.restoreGraphicsState()

        return bitmap.representation(using: .png, properties: [:])
    }
}
```

来源：[如何将 NSImage 转换为 PNG - Swift 社区](https://blog.csdn.net/qq_36478920/article/details/126182661?spm=1001.2014.3001.5501 "如何将 NSImage 转换为 PNG - Swift 社区")

### 如何在 macOS 中找到以前最前沿的应用程序

监听 `didActivateApplicationNotification` 并过滤结果获取希望找到的应用程序。

```Swift
NSWorkspace.shared.notificationCenter
    .publisher(for: NSWorkspace.didActivateApplicationNotification)
    .sink(receiveValue: { [weak self] note in
        guard
            let app = note.userInfo?[NSWorkspace.applicationUserInfoKey] as? NSRunningApplication,
            app.bundleIdentifier != Bundle.main.bundleIdentifier
        else { return }
        
        self?.frontMostApp = app
    })
    .store(in: &bag)
```

来源：[如何在 macOS 中找到以前最前沿的应用程序 - Swift 社区](https://blog.csdn.net/qq_36478920/article/details/126504375?spm=1001.2014.3001.5501 "如何在 macOS 中找到以前最前沿的应用程序 - Swift 社区")


## 内容推荐

整理编辑：[Mim0sa](https://juejin.cn/user/1433418892590136)

1、[从响应式编程到 Combine 实践](https://mp.weixin.qq.com/s/b_q6R64xkq8Rl9EiIde4MA "从响应式编程到 Combine 实践") -- 来自：字节跳动技术团队

[@Mim0sa](https://juejin.cn/user/1433418892590136)：来自字节跳动技术团队的 Combine 实践记录，文章从浅到深讲解了响应式编程的特点、选择 Combine 的理由以及具体实践。也介绍了 Combine 中的三个关键概念，事件发布／操作变形／订阅使用，也提及了一些常见错误等，很适合不是特别了解响应式编程的同学。

2、[不改一行业务代码，飞书 iOS 低端机启动优化实践](https://mp.weixin.qq.com/s/KQJ5QXHdhwHRN65KdD45qA "不改一行业务代码，飞书 iOS 低端机启动优化实践") -- 来自：字节跳动技术团队

[@Mim0sa](https://juejin.cn/user/1433418892590136)：低端机启动优化实践，文章讨论了在低端机的情况下，会在启动时有哪些特点，介绍了在 GCD queue 上发现的问题和优化方案。

3、[RunLoop的实际使用](https://mp.weixin.qq.com/s/GrkCUyxsoxqdkbeJcoAIdw ''RunLoop的实际使用') -- 来自：搜狐技术产品

[@Mim0sa](https://juejin.cn/user/1433418892590136)：来自搜狐技术产品的一篇比较基础的 RunLoop 文章，从线程保活开始介绍了 RunLoop 在实际开发中的使用，然后介绍了卡顿监测和 Crash 防护中的高阶使用。

4、[iOS下锁的独白](https://mp.weixin.qq.com/s/3d365xrDKp7TwwY_htloiA ''iOS下锁的独白') -- 来自：搜狐技术产品

[@Mim0sa](https://juejin.cn/user/1433418892590136)：来自搜狐技术产品的一篇关于锁的文章，介绍了 iOS 中的锁有哪一些，以及如何使用。文章中的代码和注释清晰明了，归纳的也很全。

5、[Avoiding race conditions in Swift](https://medium.com/swiftcairo/avoiding-race-conditions-in-swift-9ccef0ec0b26 "Avoiding race conditions in Swift") -- 来自：Mostafa Abdellateef

[@Mim0sa](https://juejin.cn/user/1433418892590136)：一篇关于如何避免竞争的文章，文章内容比较简单，但是观点很深入，探讨了在软件的设计中去避免资源的竞争，靠的不是一味的使用各种锁、栅栏，而是精良的设计。文中举的例子生动易懂且随文的图片制作精良。

6、[How do 3D transforms of iOS views work under the hood?](https://www.thealexanderlee.com/blog/how-do-3d-transforms-of-ios-views-work-under-the-hood ''How do 3D transforms of iOS views work under the hood?') -- 来自：Alex Lee

[@Mim0sa](https://juejin.cn/user/1433418892590136)：本文主要介绍了 3D transforms 的各种变化是怎么得来的，配有手绘介绍图，但需要一点点数学知识才可以读懂。


## 摸一下鱼

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #63 | Apple 企业家培训营已开放申请](https://mp.weixin.qq.com/s/nAMshUG4AjWLAAHOFPVqXg)

[iOS 摸鱼周报 #62 |  Live Activity 上线 Beta 版 ](https://mp.weixin.qq.com/s/HySX4Yaf3Zxy8Wn-LyUO0A)

[iOS 摸鱼周报 #61 |  Developer 设计开发加速器](https://mp.weixin.qq.com/s/WfwqRhC-9-isUanv8ZnvMQ)

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
