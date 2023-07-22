# iOS 摸鱼周报 #100 | 最后一期

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：关于摸鱼周报的运营感受，这是最后一期
> * 本周学习：Xcode 中更好的异常提示
> * 内容推荐： String Catalogs、自定义字体加载、HTTP 类型、单向数据流、构建类 Facetime 应用等内容
> * 摸一下鱼：不换账号切换 App Store 商店内容；吐司 Tusi.Art；Swift AST 可视化展示网站；开源的 AI 角色模拟框架 RealChar；一份小册：「精益副业：程序员如何优雅地做副业」

## 本期话题

### 最后一期摸鱼周报

不知不觉摸鱼周报已经做到第 100 期了。从公众号后台看第 99 期到第 1 期的变化，找到第二期周报一位读者的留言：

![](https://cdn.zhangferry.com/Images/202307192337354.png)

当时很受鼓舞，但确实没想过要做多久，100 期是一个很玄幻的目标。但从那开始命运的齿轮开始转动，两年半之后，竟然真的做到了 100 期。通过后台数据能大致分析出周报的一些变化，前中期阅读量和互动量都还不错，到了近期反而有些下滑。可能是选题上的差异，也可能是受众的变化，周报的运作似乎也达到了一种难以突破的瓶颈。

就我本身来说呢，工作上有很多事情需要更全面的规划，字节内部也有很多东西想要深入了解；业余时间最近对 AI、前后端技术兴趣比较大，已经列了好几个支线任务，都还是待完成状态；家庭方面，随着孩子的成长，也想给她更多的陪伴，最近也都尽量早点下班陪孩子。但是呢，时间是有限的，在一个地方的投入更多就意味着另一个地方就要减少，最近半年都没咋打开原神了。

所以摸鱼周报还要不要做下去，就变成了一个需要衡量 ROI 的事情了。早期的收获更多是定期输出的习惯培养、公众号运营、与读者的互动、认识更多的朋友等等，现在呢，考虑到时间成本，这些都不足以再支撑我有巨大的热情来继续搞摸鱼周报了。这个决定也想过很久了，100 是一个很完美的数字，摸鱼周报就停留在这一期吧。

感谢一直以来支持摸鱼周报的编辑们，特别是肘子，不是他的帮助可能 100 期都做不到；也感谢各位陪伴的读者，被人关注，被人期待的感觉很美好，这些都是你们给的，希望大家拥有更多这样的经历。后面也还是会继续输出一些内容，只不过密度会小一些，最后一期，大家继续享用吧。

## 本周学习

整理编辑：[zhangferry](https://zhangferry.com)

### 给代码异常提供更丝滑的提醒方式

在平常开发过程中，对于一些非预期的行为，我们通常使用 `assert`或者 `fatalError`附加一些信息，并中断程序来提醒开发者注意这类异常。但它最大的问题在于触发此类语句，程序会立即崩溃，除了异常语句提供的信息，什么都获取不到的，想跟进一些执行的上下文时也变得不可能，那这种行为除了增加开发阻塞感就没有其他任何益处了。这里介绍两种相对不那么生硬，还能起到比较直接提醒的形式。后面内容参考自 [Unobtrusive runtime warnings for libraries](https://www.pointfree.co/blog/posts/70-unobtrusive-runtime-warnings-for-libraries "Unobtrusive runtime warnings for libraries")。

**断点提醒**

就是程序运行到此处时，不再崩溃，取而代之是一个自动的断点，你可以选择调试上下文，也可以选择继续执行。主要逻辑是向运行的进程发送 SIGTRAP 信号：

```swift
raise(SIGTRAP)
```

它生效的前提是当前程序已经被 LLDB attach 了，SIGTRAP 全名是 "Trace/breakpoint trap"，它是 POSIX 标准定义下的信号之一。这个信号的默认操作是让进程停止执行，并进入断点停止状态。`raise(SIGTRAP) `就是向当前进程发送 SIGTRAP 信号，使其进入断点停止状态。如果要跳过断点，输入 "c"，或点击跳过断言按钮都可以。

![](https://cdn.zhangferry.com/Images/202307200921665.png)

完整代码如下：

```swift
@inline(__always) func breakpoint(_ message: @autoclosure () -> String = "") {
  #if DEBUG
    var name = [CTL_KERN, KERN_PROC, KERN_PROC_PID, getpid()]
    var info = kinfo_proc()
    var info_size = MemoryLayout<kinfo_proc>.size

    let isDebuggerAttached = sysctl(&name, 4, &info, &info_size, nil, 0) != -1
      && info.kp_proc.p_flag & P_TRACED != 0

    if isDebuggerAttached {
      fputs(
        """
        \(message())

        Caught debug breakpoint. Type "continue" ("c") to resume execution.

        """,
        stderr
      )
      raise(SIGTRAP)
    }
  #endif
}
```

这个方案的问题在于断点的位置无法控制，可能会让人疑惑。

**issue 提醒**

Xcode 会默认开启主线程检查，就是非主线程操作 UI 会被识别到并以一种紫色的提醒展示出来，它不会打断程序执行，仅仅用于展示。

![](https://cdn.zhangferry.com/Images/202307202210465.png)

这种能力其实也是可以自定义的，有一种方案是通过函数地址去调用 `__main_thread_checker_on_report`，但因为它展示的分类还是 Main Thread Cheker，效果不太好。还有一种方案是通过 os_log，这种形式相对 trick，记得把它限定在 DEBUG 环境下。

```swift

// os_log 定义
@available(macOS 10.14, iOS 12.0, watchOS 5.0, tvOS 12.0, *)
public func os_log(_ type: OSLogType, dso: UnsafeRawPointer = #dsohandle, log: OSLog = .default, _ message: StaticString, _ args: CVarArg...)

// os_log 使用
os_log(
  .fault, // 日志类型，有：default, info, debug, error, fault
  dso: <UnsafeRawPointer>,
  log: OSLog(
    subsystem: "com.apple.runtime-issues", // 可固定
    category: "CustomXcodeIssue" // 日志类别
  ),
  "We encountered a runtime warning" // 需要自定义展示的日志信息
)
```

这里还有一个参数没有填，就是这个 `dso`，它对应的是一个系统动态库的基址，而且它还不是随便一个动态库都行，哪谁可以呢，文章中用的是 SwiftUI，但非 SwiftUI 项目回来加载这个库，测试发现 Foundation 也是可以。获取 Foundation 的基地址有两种方式：

* 通过 `nm` 获取一个 Foundation 里的符号，然后通过 `dladdr` 获取库的基值：

  ```swift
  var info = Dl_info()
  dladdr(
    dlsym(
      dlopen(nil, RTLD_LAZY), "+[NSBundle allBundles]" // Foundation 内部符号
    ),
    &info
  )
  // info.dli_fbase 就是这个基址
  ```

* 通过检测所有需要加载的动态库，根据加载地址判断出 Foundation：

  ```swift
  let count = _dyld_image_count()
  for i in 0..<count {
    guard let name = _dyld_get_image_name(i),
      String(cString: name).hasSuffix("/Foundation"),
      let header = _dyld_get_image_header(i) else {
        continue
    }
    // header对应的就是基地址
  }
  ```

为了让提示能够停留在我们的调用的地方，还需要给日志函数加上内联，最终效果如下：

![](https://cdn.zhangferry.com/Images/202307221459902.png)

完整代码：

```swift
@_transparent
@inline(__always)
func runtimeWarning(
  _ message: @autoclosure () -> StaticString,
  _ args: @autoclosure () -> [CVarArg] = []
) {
  #if DEBUG
    let message = message()
    let log = OSLog(subsystem: "com.apple.runtime-issues", category: "CustomXcodeIssue")
    struct DSOFinder {
        static let dso: UnsafeMutableRawPointer = {
          let count = _dyld_image_count()
          for i in 0..<count {
              guard let name = _dyld_get_image_name(i),
                    String(cString: name).hasSuffix("/Foundation"),
                    let header = _dyld_get_image_header(i) else {
                  continue
              }
              return UnsafeMutableRawPointer(mutating: UnsafeRawPointer(header))
          }
          return UnsafeMutableRawPointer(mutating: #dsohandle)
        }()
      }
    
    os_log(.fault, dso: DSOFinder.dso, log: log, message, args())
  #endif
}
```

## 内容推荐

推荐近期的一些优秀博文，内容涵盖 String Catalogs、自定义字体加载、HTTP 类型、单向数据流、构建类 Facetime 应用等方面。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[与 String Catalogs 有关的常见问题解答](https://www.fline.dev/the-missing-string-catalogs-faq-for-xcode-15/ "与 String Catalogs 有关的常见问题解答") -- 作者：Cihat Gündüz

[@东坡肘子](https://www.fatbobman.com/): 在 WWDC23 上，苹果为 Xcode 推出了一个新功能：String Catalogs。该功能取代了传统的本地化文件，简化了本地化流程。本文作者同时为 [RemafoX](https://remafox.app/)（ 一个本地化工具）的开发者，他在 Slack activity 上与苹果的工程师进行了深入探讨。作者将通过问题解答的形式对 String Catalogs 进行说明，以帮助开发者了解为什么应该对 Xcode 15 中的这个强大工具感到兴奋。

2、[使用 Swift Package 插件将自定义字体加载到应用程序中](https://www.polpiella.dev/load-custom-fonts-with-no-code-using-swift-package-plugins/ "使用 Swift Package 插件将自定义字体加载到应用程序中") -- 作者：Pol Piella Abadia

[@东坡肘子](https://www.fatbobman.com/): 如果你发现自己一遍又一遍地使用相同的字体，那么就要考虑是否需要创建一个 Swift Package 来包含共享的字体文件和字体加载代码。这样可以更快地创建新的应用程序，通过一个单一的地方来更新所有应用程序的字体文件，并减少代码重复。本文作者将向你展示如何使用 [SwiftGen](https://github.com/SwiftGen/SwiftGen) 来实现这一点，让你的应用程序更加高效和可维护。

3、[介绍 Swift HTTP 类型](https://www.swift.org/blog/introducing-swift-http-types/ "介绍 Swift HTTP 类型") -- 作者：Guoye Zhang、Eric Kinnear、Cory Benfield

[@东坡肘子](https://www.fatbobman.com/): Swift 社区刚刚发布了一个名为 [Swift HTTP Types](https://github.com/apple/swift-http-types) 的开源软件包，通过 HTTPRequest 和 HTTPResponse 提供了 HTTP 消息的核心构建块的通用表示。在项目中采用这些类型，可以在客户端和服务器之间共享更多的代码，从而减少在类型之间进行转换的成本。Swift 社区的最终目标是使用 Swift HTTP Types 替换 SwiftNIO 的 HTTPRequestHead 和 HTTPResponseHead，以及 Foundation 的 URLRequest 和 URLResponse 中的 HTTP 消息信息。

4、[单向数据流](https://swiftwithmajid.com/2023/07/11/unidirectional-flow-in-swift/ "单向数据流") -- 作者：Majid

[@东坡肘子](https://www.fatbobman.com/): Majid 写过很多关于 SwiftUI 数据流的文章，分享了他在该领域的灵感和想法。这些想法经过多年应用程序构建的实践，最终产生了一个名为 [swift-unidirectional-flow](https://github.com/mecid/swift-unidirectional-flow) 的 Swift 软件包。该软件包实现了 Majid 所有的想法，并被用于他的项目中，支持并发以及构建实际应用所需的其他功能（如可预测、可预览、可调试、模块化）。但是，Majid 并不建议开发者直接使用该软件包。他认为，开发者不应该导入任何第三方库或框架来构建应用程序的核心功能。你可以使用它作为灵感，在应用程序中根据你的需求构建状态管理系统。

5、[流式视频通话：如何使用 SwiftUI 构建类似 FaceTime 的应用](https://getstream.io/blog/facetime-clone/ "流式视频通话：如何使用 SwiftUI 构建类似 FaceTime 的应用") -- 作者：Amos G

[@东坡肘子](https://www.fatbobman.com/): 无论通话参与者身在何处，使用苹果设备，都可以通过 FaceTime 创建一对一或群组的音频/视频通话。本文将演示如何使用 SwiftUI 和 iOS Video SDK from Stream 来构建一个类似 FaceTime 的应用，与朋友和家人进行面对面的聊天。构建的 iOS 语音和视频通话应用程序可以支持多种用例，例如 1-1 通话，群组会议，远程医疗，约会和会议等。


## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[切换 App Store]("https://as.dogged.cn")：要登录不同国家的 App Store 通常都需要有各个国家的 AppleID 才行，这个网站则可以做到随意切换 App Store 商城。用 iPhone 端 Safari 打开网站地址：https://as.dogged.cn，点击对应的国家会跳转至 App Store，并刷新 App Store 内容为当前国家的信息。当然你只能浏览商店，无法下载。

2、[吐司 Tusi.Art](https://tusi.art/images/615780714069126582?post_id=616351352009977730&source_id=nz-zoFvmkkS7pfsjbX3x8xMh "吐司 Tusi.Art")：一个国内的类 civitai 网站，有 AI 模型和 AI 图片的分类展示，我看一些 C 站有名的作者也有在吐司发布模型。该网站还提供了在线生成 AI 图片的功能，每天提供 100 算力，如果都使用文生图 + 高清修复的话，每天可以白嫖 50 张图片。最主要的是比我本地跑的要快。

![](https://cdn.zhangferry.com/Images/202307202330596.png)

3、[Swift AST Explorer](https://swift-ast-explorer.com/ "Swift AST Explorer")：一个把 Swift 代码的 AST 可视化展示出来的网站。如下图是 Swift 中一个枚举声明 EnumCaseDecl 的结构：

![](https://cdn.zhangferry.com/Images/202307192306027.png)



4、[RealChar](https://github.com/Shaunwei/RealChar "RealChar")：最近比较火的一个 AI 项目，类似 character.ai，但要更优秀，它可以自定义 AI 角色的行为、背景，甚至声音；可以实现语音对话，且实时性很高，语音也让交流过程显得更加自然；提供多端接入能力，网页、iPhone、终端都可以。

![](https://cdn.zhangferry.com/Images/202307210016026.png)

还有提供了一个体验的平台：https://realchar.ai/，可能是声音的加持，跟这里的乔布斯交流，更显自然，很奇妙的感觉。对了，他还能说中文😅

![](https://cdn.zhangferry.com/Images/202307210038106.png)

5、[精益副业：程序员如何优雅地做副业](https://github.com/easychen/lean-side-bussiness "精益副业：程序员如何优雅地做副业")：副业是一个比较理想的存在，这篇小书提到的几个实践有知识付费、社区付费、独立产品，这些适用性已经没有那么强了，能做出来的概率很低。但考虑副业，把一个目标拆分，尝试做成产品这件事本身还是比较有价值的。作为程序员很多时候我们了解的只是技术细节，而完成的产品设计还有很多。其中举了一个「福利单词」项目的商业模式画布，对于大多数产品都可以通过类似环节进行拆分。

![](https://cdn.zhangferry.com/Images/202307210858883.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #99 | 躺平、摆烂、开心就好](https://mp.weixin.qq.com/s/0r-ni--4jEN4pnIHVajHqg)

[iOS 摸鱼周报 #98 | visionOS 模拟器体验](https://mp.weixin.qq.com/s/PNEYW71BfkQ2Y3n7uRdxsQ)

[iOS 摸鱼周报 #97 | 智源大会线下参会体验](https://mp.weixin.qq.com/s/6HRxZXAJcTZKGZiNX2eBYQ)

[iOS 摸鱼周报 #96 | Vision Pro 打开空间计算的大门](https://mp.weixin.qq.com/s/BM3SucfO9yhQChIPbnuwrA)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
