# iOS 摸鱼周报 #78 | App Store 定价机制最重大升级

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：App Store 定价机制最重大升级
> * 本周学习：Mac Intel 转 Apple Silicon iOS 开发环境配置解决
> * 内容推荐：本期将推荐近期的一些优秀博文，涵盖 ChatGPT、SwiftUI、Swift 等方面的内容
> * 摸一下鱼：本期摸鱼带来可以无限生成配色组合的网站 **randoma11y**，听猫咪不同状态声音的网站 **purrli**，由前任天堂设计师的创意团队建立的像素风格的透明素材网站 **dotown**，以及在 Webstorm 中配置 Touchbar 的指南。

## 本期话题

### [Apple 宣布 App Store 定价机制最重大升级，新增 700 个价格点](https://developer.apple.com/cn/news/?id=qzex35ch "Apple 宣布 App Store 定价机制最重大升级，新增 700 个价格点")

[@远恒之义](https://github.com/eternaljust)：近日，Apple 对 App Store 进行全面的定价机制升级。新定价机制增加了 700 个价格点和全新定价工具，提供自动续期订阅服务的 App 从 2022 年 12 月 6 日起即可使用升级，其他所有 App 及 App 内购买内容将可从 2023 年春季开始使用新定价机制。在新定价机制中，所有开发者均可在 900 个价格点中选择定价。Apple 提供更高的定价灵活度，价格点将从最低 ¥1 到最高 ¥74,999。同时，订阅 App 的开发者将可选择自己最熟悉的地区商店，以此为基础自动为其他商店生成定价。此外，开发者也可按需针对不同商店分别定价，该功能将在 2023 年春季拓展至其他所有 App。新定价机制的价格区间逐渐递增，各档位变化如下所示：

![](https://cdn.zhangferry.com/Images/78-appstore-upgrade-pricing.jpeg)

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Mac Intel 转 Apple Silicon iOS 开发环境配置解决

越来越多的开发者已经使用 Apple Silicon 芯片的 mac 作为开发工具，笔者近期也更换了 M2 作为主力机，记录一下从 Intel 切换到 M2 过程中遇到的环境配置问题。

我使用 **迁移助理** 工具做的整个开发环境的拷贝，用时 1~2 小时完成了大约 250G 内容的传输，这种切换方式优势在于整个开发环境完全保持一致，不会丢失现有环境配置导致项目开发运行时才发现问题。可以快速投入开发，但也为后续的环境兼容带来了一些麻烦。所以如果你的开发机环境配置不复杂，建议重新安装开发环境。

1. 先从简单的项目适配说起，由于 Apple Silicon 是 arm 架构，如果工程 debug 环境暂未支持 arm 架构并且需要使用模拟器运行项目，有两种办法：使用 Rosetta 模式运行模拟器、或者更新 SDK 以适配 arm 架构

    建议优先工程适配 arm 架构，因为目前 Rosetta 模式运行模拟器会存在一些问题，例如列表滚动阻尼效果缺失，xcode 14 后模拟器二次 build 会黑屏卡在 `launching $(projectname)` 阶段等各种使用问题。

    > 但是一些引入的二进制 SDK 暂不支持 debug 模式的 arm架构，例如微信的 SDK。只能退而求其次通过 Rosetta 模式运行模拟器。需要设置 `Build Setting => Architectures =>Excluded Architectures` 在 debug 模式设置 `arm64` 以此移除工程 debug 模式对 arm 架构的支持，模拟器会自动切换到 Rosetta 模式。

2. 从 Intel 切换过来时 Mac 上安装的 app 大部分都是基于 Intel 架构的，在 Apple Silicon 上使用不存在问题，但是性能效率会有影响，部分软件使用时会有明显卡顿。所以建议如果软件有arm 架构或者通用架构的版本，重新安装即可。这里推荐一个应用[iMobie M1 App Checker](https://www.imobie.com/m1-app-checker/ "iMobie M1 App Checker")可以快速查询所有安装的 app 架构，如图所示：

    ![](https://cdn.zhangferry.com/Images/weekly_78_study_01.png)

3. 如果有使用 `Homebrew` 管理工具，重新安装 arm 版本后，管理的包路径发生了变更，新路径为 **/opt/homebrew/bin**，如果脚本或者配置中使用了 `Homebrew` 管理命令的绝对路径，则需要修改，例如我们工程中有引入过 `Carthage`，该工具需要在项目`Build Phases`中添加执行命令 `/usr/local/bin/carthage copy-frameworks`，编译会报错找不到 `carthage` 执行文件。

4. 更新 `Homebrew` 后建议重新安装所有已安装的库，否则后续会遇到各种离奇的问题。例如在使用 `Rbenv` 管理安装 `Ruby` 时会各种报错，因为 `Ruby`依赖 `ruby-build、readline、openssl`等工具，如果这些工具仍然是旧版本，可能会不兼容，需要重新安装最新版本。

    > `homebrew` 没有提供实现重新安装所有库的命令，可以使用管道结合`xargs`命令: `brew list | xargs brew reinstall`
    >
    > **Tips**: shell 中 **|**表示管道，可以将左侧命令的标准输出转换为标准输入，提供给右侧命令。而   `xargs` 是将标准输入转为命令行参数，更多内容参考 [xargs 命令教程](https://www.ruanyifeng.com/blog/2019/08/xargs-tutorial.html "xargs 命令教程")

5. `Rbenv` 可以直接安装 `Ruby`**3.x** 版本，**2.7.1 **版本则需要使用 `RUBY_CFLAGS="-w" rbenv install 2.7.1` 参数禁止所有warring 和 error，安装 **2.7.2** 及更高版本在环境中做以下配置即可（验证成功）：

    ![](https://cdn.zhangferry.com/Images/weekly78_study_02.png)

暂时遇到以上问题，如果有更多问题和疑问，可以留言讨论。

* [Installation issues with Arm Mac](https://github.com/rbenv/ruby-build/issues/1691 "Installation issues with Arm Mac")


## 内容推荐

> 本期将推荐近期的一些优秀博文，涵盖 ChatGPT、SwiftUI、Swift 等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[注册 ChatGPT 全攻略](https://zhuanlan.zhihu.com/p/589365506 "注册 ChatGPT 全攻略") -- 来自：BoxChen

[@东坡肘子](https://www.fatbobman.com/): 上周 IT 届最火爆的新闻莫过于 OpenAI 推出了用于人机交流的 ChatGPT 模型。遗憾的是，由于验证码的关系，国内开发者很难亲身体验。本文将介绍通过接入码平台实现注册的全过程。由于原文网站访问不便，附带的是知乎转载的地址。

2、[用 OpenAI 的 ChatGPT 会话机器学习模型为 SwitfUI 应用程序创建工作代码](https://www.createwithswift.com/prototyping-swiftui-interfaces-with-openais-chatgpt/ "用 OpenAI 的 ChatGPT 会话机器学习模型为 SwitfUI 应用程序创建工作代码") -- 来自：Moritz Philip Recke

[@东坡肘子](https://www.fatbobman.com/): 最近一段时间，OpenAI 发布了许多人工智能 API 和机器学习模型，支持文本摘要、翻译、解析非结构化数据、分类、文本组合等用例。最新添加的是一个名为 ChatGPT 的模型，它是作为对话工具实现的。本文将介绍如何使用 OpenAI 的 ChatGPT 会话机器学习模型为 SwitfUI 应用程序创建工作代码。

3、[在 SwiftUI 中构建自定义布局](https://swiftwithmajid.com/2022/11/16/building-custom-layout-in-swiftui-basics/ "在 SwiftUI 中构建自定义布局") -- 来自：Majid

[@东坡肘子](https://www.fatbobman.com/): SwiftUI 4 中提供了 Layout 协议，允许开发者在不使用GeometryReader 的情况下挖掘布局系统来构建自定义布局。作者将通过三篇文章（ 基础、缓存、间距 ）介绍如何通过新的布局协议在 SwiftUI 中构建布局。

4、[MacOS Ventura 系统 ssh 不再支持 ssh-rsa 的原因及解决办法](https://blog.twofei.com/881/ "MacOS Ventura 系统 ssh 不再支持 ssh-rsa 的原因及解决办法") -- 来自：桃子

[@东坡肘子](https://www.fatbobman.com/): 升级到 MacOS Ventura 系统后，如果尝试使用 ssh 登录服务器，大概率会发现无法登录。本文将分析出现问题的原因并提供解决的办法。

5、[SwiftUI 与 Core Data](https://www.fatbobman.com/posts/modern-Core-Data-Problem/ "SwiftUI 与 Core Data") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 如何让 Core Data 融入流行的应用架构体系，在 SwiftUI、TCA、Unit Tests、Preview 等环境下更加顺畅地工作已成为很多开发者当前主要困扰。作者将通过几篇文章来介绍近半年来在这方面的一些想法、收获、体会及实践。

6、[Swift Error](https://juejin.cn/post/7130593449174106149/ "Swift Error") -- 来自：移动端小伙伴

[@东坡肘子](https://www.fatbobman.com/): 在开发中，往往最容易被忽略的内容就是对错误的处理。有经验的开发者，能够对自己写的每行代码负责，而且非常清楚自己写的代码在什么时候会出现异常，这样就能提前做好错误处理。Swift Error Handling 能够让开发者快速而简便的告知编译器一个函数能否抛出错误，并且在抛出后以合适的方式去处理错误。作者将通过两篇文章对 Swift Error 的用法、特点、优化等内容进行介绍。

## 摸一下鱼

整理编辑：[Mim0sa](https://juejin.cn/user/1433418892590136/posts)

1. Apple 官方放出的 [Stable Diffusion with Core ML on Apple Silicon ](https://machinelearning.apple.com/research/stable-diffusion-coreml-apple-silicon "Stable Diffusion with Core ML on Apple Silicon")，你现在可以在 Apple 的平台上以 CoreML 的形式运行 Stable Diffusion 了。

   ![sd_apple](https://cdn.zhangferry.com/Images/sd_apple.jpg)

2. 一个很棒的配色网站 [randoma11y](https://randoma11y.com/ "randoma11y")，可以无限生成配色组合。

   ![randoma11yImg](https://cdn.zhangferry.com/Images/randoma11yImg.png)

3. [purrli](https://purrli.com/ "purrli") 一个可以听猫咪不同状态声音的网站。

   ![purrliImg](https://cdn.zhangferry.com/Images/purrliImg.png)

4. [dotown](https://dotown.maeda-design-room.net/ "dotown") 一个由前任天堂设计师的创意团队建立的像素风格的透明素材网站，这些素材的都使用尽可能低的分辨率进行抽象的点阵表达，风格一致，充满怀旧游戏氛围，极具特色。

   ![dotownImg](https://cdn.zhangferry.com/Images/dotownImg.png)

5. 一份在 Webstorm 中配置 Touchbar 的[指南](https://juejin.cn/post/7174175965113745416 "指南")。

6. [赛百味的台湾官网](https://subway.com.tw/GoWeb2/include/meals-nutrition.html "赛百味的台湾官网")有所有三明治的营养信息，虽然产品略有不同但有需要的话也可以参考一下。

   ![subwayImg](https://cdn.zhangferry.com/Images/subwayImg.png)


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/UmXvtKYS6Z0a30yPRyIV9g)

[iOS 摸鱼周报 #75 | 远程工作推行之难](https://mp.weixin.qq.com/s/nguqKvkuzDBR9o-Yw6y3KQ)

[iOS 摸鱼周报 #74 | 抖音 iOS 基础技术大揭秘 Vol.02 周六见](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
