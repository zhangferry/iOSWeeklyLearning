# iOS 摸鱼周报 #57 | 周报改版，WWDC22 讲座集锦

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：周报改版，WWDC22 讲座集锦，Apple 夏令营课程回归
> * 本周学习：Xcode Playground Tips
> * 内容推荐：苹果开发者大会落幕，介绍一些 WWDC22 推出的新技术和新内容
> * 摸一下鱼：Apple Logo Artwork，收录苹果独特多彩风格的媒体版本 Logo
> * 岗位推荐：抖音 iOS 基础技术研发效能方向

## 本期话题

### 周报改版

[@zhangferry](zhangferry.com)：周报停了一期，主要是为了这期改版，算是一个小变动吧。之前周报篇幅稍微有些大，对整理编辑的人员和读者来说完整看下来都会有一些压力。鉴于此周报部分内容进行了合并，另外增加了一个摸鱼模块，分享一些最近看到的有趣的内容。大家如果对内容改进上有其他什么建议，也欢迎给我们留言提意见。

###  Developer 设计开发加速器｜WWDC22 讲座集锦 

@师大小海腾：本期活动精选了 WWDC22 公布的最新技术，邀请 Apple 设计和技术布道师为中国开发者带来中文讲座集锦。通过本次活动您可以了解最新技术趋势、学习平台的最新功能，从而打造更为卓越的 App 体验。

**活动日期**：2022 年 6 月 28 日至 29 日

**报名截止日期**：2022 年 6 月 27 日

**议程：**

| 6 月 28 日 上午             |
| --------------------------- |
| 锁屏小组件及复杂功能        |
| 探索 App Intents            |
| 在您的 App 内支持 Live Text |

| 6 月 28 日 下午                                |
| ---------------------------------------------- |
| 探索 Swift 更新                                |
| 探索 SwiftUI 更新                              |
| 探索设计新特性: iPad App, Charts 及 SF Symbols |
| 探索 Metal 3                                   |
| 探索 Xcode 14 更新                             |

| 6 月 29 日 上午                                       |
| ----------------------------------------------------- |
| 探索 AR 技术更新: RoomPlan, Object Capture 及 ARKit 6 |
| 探索隐私技术的更新                                    |

**报名地址**：https://developer.apple.com/cn/accelerator/

您也可以通过扫描以下二维码报名：

![](https://cdn.zhangferry.com/Images/WechatIMG12.jpeg)

### Apple 邀请全球家庭参加 Apple 夏令营课程，同享创造与学习体验

[@远恒之义](https://github.com/eternaljust)：从 6 月 20 日到 8 月 31 日，Apple 每周都会举办课程。Apple 夏令营已进入第 20 个年头，此次将以全新的两小时家庭课程形式回归，帮助参与者创作以保护与歌颂地球为主题的数字漫画书。

**家长与监护人报名地址**：https://www.apple.com.cn/today/collection/apple-camp/

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Xcode Playground Tips

`Playground` 是学习 Swift 和 SwiftUI 的必不可少的工具，这里总结一些可能涉及到的 Tips，方便更好的学习和使用。

#### 模块化

`Playground` 中也是支持模块化管理的，主要涉及辅助代码和资源两部分：

- 辅助代码(位于 Sources 目录下的代码)：

    辅助代码只在编辑内容并保存后才会编译，运行时不会每次都编译。辅助代码编译后是以 module 形式引入到 Page 中的。所以被访问的符号都需要使用 `public` 修饰。

    添加到 Playground Sources 下的辅助代码，所有 Page 主代码和辅助代码 都可使用。区别在于 Page 辅助代码如果未 import 导入 module, 则不会有代码提示，主代码无需 import。

    添加到 Page Sources 下的辅助代码，只有当前的 Page 可用（Apple 文档）。module 命名格式为 **xxx(PageName)_PageSources**。

    > 实际测试，如果在其他 Page 主代码中和辅助代码中同时 `import` 当前 Sources Module 也是可用的，但是只在辅助代码中 `import`，则不生效。如果有不同测试结果的同学可以交流下

- 资源（位于 Resources）：

使用时作用域同辅助代码基本相同，由于无法作为 module 被 `import` 到 Page 主代码，所以跨 Page 之间的资源是无法访问的。

`Playground` 编译时将当前 Page 和 `Playground` 项目的资源汇总到 Page 项目路径下，因此无论是项目资源还是 Page 专属资源，在 Page 主代码或 Page 的辅助代码中，都可以使用 `Bundle.main` 来访问。

#### 运行方式

`Playground` 可以修改运行方式，分别是 `Automatically Run` 和 `Manually Run`，区别就是自动模式在每次键入后自动编译。调整方式为长按运行按钮，如图：

![](https://cdn.zhangferry.com/Images/weekly_57_weeklyStudy_01.png)

另外，通过快捷键 `shift-回车` 可以只运行到当前鼠标所在位置代码，作用同直接点击代码所在行的运行按钮一致。

#### PlaygroundSupport

`PlaygroundSupport` 是用于扩展 Playground 的框架，在使用上主要有两个作用：

- 执行一些延迟、异步操作、或者存在交互的视图时，这时需要 `Playground` 在执行完最后代码后不会直接 Finish，否则一些回调和交互不会生效。需要设置属性 `needsIndefiniteExecution == true`。

    ```swift
    // 需要无限执行
    PlaygroundPage.current.needsIndefiniteExecution = true
    // 终止无限执行
    PlaygroundPage.current.finishExecution()
    ```

- 使用 `Playground` 展示实时视图时，需要将视图添加到属性 `liveView` 上。如果设置了 `liveView` 则系统会自动设置 `needsIndefiniteExecution`，无需重复设置。

    > 如果是 `UIKit` 视图则通过 `liveView` 属性赋值或者 `setLiveView()` 函数调用都可以，但是 `SwiftUI` 只支持 `setLiveView()` 函数调用方式。

    ```swift
    struct contentView: View {...}
    let label = UILabel(frame: .init(x: 0, y: 0, width: 200, height: 100))
    PlaygroundPage.current.setLiveView(label) // PlaygroundPage.current.liveView = label
    PlaygroundPage.current.setLiveView(contentView)
    ```

#### markup 注释

根据文档，markup 支持标题、列表、代码、粗体、斜体、链接、资产、转移字符等，目的是在 `Quick Help` 和代码提示中显示更丰富的描述信息

书写格式分两种，单行使用 `//: 描述区` 多行使用 `/*: 描述区 */`

源码/渲染模式切换方式：`Editor -> Show Rendered Markup` 或者设置右侧扩展栏的 `Playground Settings ->Render Documentation`。

由于大部分格式都是和 markdown 类似的，这里只学习一个特殊的特性，即导航。

导航可以实现在不同的 Page 页之间跳转，有三种跳转方式：previous、next、指定页

```swift
[前一页](@previous)、[下一页](@next)、[指定页](name)
```

> 指定具体页时，页面名称去掉扩展名，并且编码替换空格和特殊字符。不需要使用 `@` 符号

Markup 更多格式可以查看官方文档 [markup-apple](https://developer.apple.com/library/archive/documentation/Xcode/Reference/xcode_markup_formatting_ref/index.html#//apple_ref/doc/uid/TP40016497-CH2-SW1 "markup-apple")，另外 `Playground` 还支持和框架或者工程结合使用，可以通过另一位主编的博客内容了解学习 [玩转 Xcode Playground（下）- 东坡肘子](https://www.fatbobman.com/posts/xcodePlayground2/ "玩转 Xcode Playground（下）- 东坡肘子")

## 内容推荐

> 每年一度的苹果开发者盛会在不久前落幕了。今年的 WWDC 一如既往地精彩。我们将分几期将一些有关 WWDC 2022 上推出的新内容、新技术介绍给大家。

整理编辑：[东坡肘子](https://www.fatbobman.com), [Mimosa](https://juejin.cn/user/1433418892590136)

1、[怎么快速看完 WWDC22](https://www.ethanhuang13.com/p/144 "怎么快速看完 WWDC22") -- 来自：Ethan Huang

[@东坡肘子](https://www.fatbobman.com/)：今年的 WWDC 2022 很精彩，内容也非常多。跟其他人不同的是，Ethan Huang 写的不是整理好的笔记、个别的知识点，而是一套有效率的吸收策略。涵盖：建立全面的印象、挑选有兴趣的主题深入以及如何利用社群来发现重要的知识。

2、[WWDC22 笔记](https://ming1016.github.io/2022/06/10/wwdc22-notes/ "WWDC22 笔记") -- 来自：戴铭

[@东坡肘子](https://www.fatbobman.com/)：边看、边记、边整理是本文的特色。作者采用了类似日记的方式，记录并整理了自己在观看 WWDC 2022 期间的每日心得。这种方式也值得其他的开发者借鉴。

3、[Swift 5.7 新特性](https://juejin.cn/post/7107058234409615373 "Swift 5.7 新特性") -- 来自：Paul Hudson 中文译者：猫克杯

[@东坡肘子](https://www.fatbobman.com/)：Swift 5.7 变化巨大，新特性中包括正则表达式， if let 速记语法，以及围绕 any 和 some 关键字的一致性改动。在本文中，Paul Hudson 想向你介绍重大变化，提供一些实际操作示例，以便你可以快速了解和掌握。

4、[WWDC 2022 在线休息室中有关 SwiftUI 的讨论](https://swiftui-lab.com/digital-lounges-2022/ "WWDC 2022 在线休息室中有关 SwiftUI 的讨论") -- 来自：Javier

[@东坡肘子](https://www.fatbobman.com/)：从 WWDC 2021 开始，苹果引入了在线休息室（ Digital Lounge ），为广大开发者提供了同苹果各个团队的工程师和设计师展开文字形式的讨论，针对最新技术提出问题，寻求编程方面的帮助以及结交演讲嘉宾的机会。今年 Javier 一如既往地对 WWDC 2022 在线休息室中有关 SwiftUI 方面的讨论进行了整理，并添加了自己的评论。

5、[SwiftUI 4.0 的全新导航系统](https://www.fatbobman.com/posts/new_navigator_of_SwiftUI_4/ "SwiftUI 4.0 的全新导航系统") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：长久以来，开发者对 SwiftUI 的导航系统颇有微词。受 NavigationView 的能力限制，开发者需要动用各种技巧乃至黑科技才能实现一些本应具备的基本功能（例如：返回根视图、向堆栈添加任意视图、返回任意层级视图 、Deep Link 跳转等 ）。SwiftUI 4.0 对导航系统作出了重大改变，提供了以视图堆栈为管理对象的新 API ，让开发者可以轻松实现编程式导航。本文将对新的导航系统作以介绍。

6、[WWDC 2022 Swift Student Challenge Submissions](https://wwdc.github.io/2022 "WWDC 2022 Swift Student Challenge Submissions") -- 来自：WWDC Students

[@Mimosa](https://juejin.cn/user/1433418892590136)：一年一度的 [WWDC Swift Student Challenge](https://developer.apple.com/wwdc22/swift-student-challenge/) 随着 WWDC 22 的召开也随之落幕了，全球无数学生开发者通过提交作品来争抢 300 多张 WWDC 现场门票，在这个网站可以看到许多优秀学生开发者今年制作的作品，以及视频演示链接，其中许多作品效果令人惊艳，难以想象其中某些作品仅出自初高中生之手。

7、[WWDC 2022 Summary for Designers](https://uxmisfit.com/2022/06/06/wwdc-2022-summary/ "WWDC 2022 Summary for Designers") -- 来自：Thalion

[@Mimosa](https://juejin.cn/user/1433418892590136)：最关注每年 WWDC 的群体莫过于程序员了，但其实除了程序员之外，也有许多并非是 Coder 的人在默默地关注着，设计师（UX/UI）就是其中的一员。本文作者通过自己的视角来解读了对于设计师们来说，这次 WWDC 中有哪些值得注意的点、在新系统中，有哪些地方更加提升了用户的体验的、以及一些他自己的看法等等。

## 摸一下鱼

1、[Felibe444](https://twitter.com/felibe444 "Felibe444") 总结了 WWDC22 里 What's new in Swift 和 What's new in UIKit 对应的功能点，并将它们做成 Sketchnote：

![](https://cdn.zhangferry.com/Images/20220623091955.png)

![](https://cdn.zhangferry.com/Images/20220623092017.png)

2、iOS 16、iPadOS 16、macOS 13、watchOS 9、tvOS 16 发布了第二个 beta 版本。

![](https://cdn.zhangferry.com/Images/FV34em9WAAAAAzH.jpeg)

3、[Apple Logo Artwork](https://www.figma.com/community/file/1117235995751919225 "Apple Logo Artwork")：

![](https://cdn.zhangferry.com/Images/20220619104319.png)

早在 2018 年，苹果公司就发出了独特的媒体邀请，它为自己的 logo 设计了无数个独特、多彩的版本，每个人似乎都收到了不同风格的邀请。苹果公司的商标图案从抽象到经典各不相同，由多位艺术家参与设计。在 Figma 上的这个仓库收录了多达 350 个 Logo。

4、[Brooklyn](https://github.com/pedrommcarrasco/Brooklyn "Brooklyn") 一款 Mac 版屏保，灵感来源于 2018 年的 Apple Event，这些素材正是 Apple Logo Artwork，效果非常酷炫。

![](https://cdn.zhangferry.com/Images/showcase.gif)

5、[PicX](https://github.com/XPoet/picx "PicX") 是一款基于 GitHub API & jsDelivr 开发的具有 CDN 加速功能的图床管理工具。

## 岗位推荐

会整理一些内推信息放到周报里，大家有合适的岗位欢迎提 issue 来录入。

1、[抖音 iOS 基础技术 - 研发效能方向](https://mp.weixin.qq.com/s/-mu76FMWaSPp8XXbP_7mNg)

我们是负责抖音客户端基础能力研发和新技术探索的团队。我们在工程/业务架构，研发工具，编译系统等方向深耕，支撑业务快速迭代的同时，保证超大规模团队的研发效能和工程质量。在性能/稳定性方面不断探索，努力为全球数亿用户提供最极致的基础体验。岗位详情可以点击上面链接查看👆。

工作地点：北京、上海、深圳、杭州

岗位需求：有扎实的数据结构和算法基础，对新技术保持热情，具备良好的分析、解决问题的能力。有这些经验会成为加分项：脚本语言、静态分析、LLVM、单元测试、自动测试框架、架构、工程效率、全栈开发

联系方式：微信号：zhangferry，或者发送简历到 `zhangfei.ferry@bytedance.com`。

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #56 | WWDC 进行时](https://mp.weixin.qq.com/s/ZyGV6WlFsZOX6Aqgrf1QRQ)

[iOS 摸鱼周报 #55 | WWDC 码上就位](https://mp.weixin.qq.com/s/zDhnOwOiLGJ_Nwxy5NBePw)

[iOS 摸鱼周报 #54 | Apple 辅助功能持续创新](https://mp.weixin.qq.com/s/6jdqa143Y5yr6lbjCuzlqA)

[iOS 摸鱼周报 #53 | 远程办公正在成为趋势](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
