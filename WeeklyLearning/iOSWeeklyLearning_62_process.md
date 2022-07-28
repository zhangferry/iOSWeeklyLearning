# iOS 摸鱼周报 #62 | Live Activity 上线 Beta 版 

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 开发资讯：Live Activity 上线 iOS Beta 4 版本 & App Store 专家会面交流 & Carbon 语言发布
> * 本周学习：iOS 使用 Pod 在现有项目上集成 React Native
> * 内容推荐：性能优化文件以及 WWDC22 优秀内容推荐
> * 摸一下鱼：Flowful 用程序生成氛围音乐；柠檬清理开源；网页版便携小空调带给你夏季清凉

## 开发资讯

### [Live Activity 已上线 iOS 16 Beta 4](https://developer.apple.com/cn/news/?id=hi37aek8 "Live Activity 已上线 iOS 16 Beta 4")

![](https://cdn.zhangferry.com/Images/20220728223617.png)

[@zhangferry](zhangferry.com)：Live Activity 是 iOS 16 推出的新功能，它可以实现在锁屏界面实时更新应用信息。像是体育比赛的比分、打车软件当前定位等信息，如果是当前系统，我们需要通过多次推送或者打开 App 才能查看最新信息，现在只需点亮屏幕即可实时获取信息。

开发 Live Activity 功能需要使用 ActivityKit 框架，该框架会被包含在 iOS 16 Beta 4 版本中。Live Activity 和 Widget 有诸多相似之处，需要使用 SwiftUI 开发，你甚至可以直接复用 Widget 的代码。但是他们更新数据的机制不同，Widget 采用时间线机制， Live Activity 则是通过 ActivityKit 或者 Push 更新数据。

注意，Live Activity 不会包含在早期的的正式版本中，它会晚些时候发布。到时候你才能将配置了 Live Activity 功能的应用提交至 App Store。

### [与 App Store 专家会面交流](https://developer.apple.com/cn/news/?id=20ikqram "与 App Store 专家会面交流")

[@zhangferry](zhangferry.com)：8 月份，Apple 将做一个线上的专家交流会，主要是讲授如何利用 App Store 能力吸引新顾客、测试营销策略、添加订阅等。其实有不少公司是专门做这个事情的， 但因为 Apple Store 采取的策略是不公开的，像是 SEO、排名策略等，外部只能通过不通的测试去推断如何做才能最优。这些公司就是依靠这些积累的信息赚钱的，现在是有了一个免费获取付费信息的渠道，还是一手的信息。看简介内容都是能够直接提升 App 收益的干货，所以这个交流会会是非常有价值的。现在只要是注册的开发者身份都可以预约参与。

### [Carbon 语言发布](https://www.youtube.com/watch?v=omrY53kbVoA "Carbon 语言发布")

[@zhangferry](zhangferry.com)：Google 在 CppNorth 发布了 Carbon 语言，目标是作为 C++ 的继任者。它可以和兼容现有的 C++ 项目，是一个现代化的语言，当然它还是[开源](https://github.com/carbon-language/carbon-lang "Github carbon-lang") 的。原有语言的继任者，看看 Java 和 Kotlin，ObjectiveC 和 Swift 的关系，开发者会因为更现代的语法喜欢新的编程语言，但开发生态的搭建是一项漫长过程，因为跟生态的耦合，一个领域的初代编程语言会有非常长的生命力。更别提已经诞生 37 年，应用到无数领域的 C++ 了。

所以新语言的意义在哪？我感觉是新语言在于摒弃原有思路，基于现有想法用全新思路去设计，它做的是尝试打破僵局的事情。类似于一个维护很久的框架，即使有人对它有怨言，还是不得不使用它，因为重新设计的成本远高于缝缝补补。敢于推翻重构已经算是勇者了，不管新语言未来发展如何，这种精神值得点赞。

## 本周学习

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### iOS 使用 Pod 在现有项目上集成 React Native

#### 问题背景

现有前端开发人员的技术栈为 React，在实践中尝试集成 RN

原生项目与 RN 项目为双独立项目，互不干预

现有项目较小，未涉及到组件化，且暂时未有相关沉淀

#### 解决方案

首先，获取 React Native  项目：我们将 RN 项目作为子项目集成现有原生项目中，利用 Git 提供的子模块功能，将一个 、RN  仓库作为 iOS 仓库的子目录。 子模块能让你将另一个仓库克隆到自己的项目中，同时还保持提交的独立。

> git submodule add <url> <repo_name>

其次，搭建 RN 开发环境，进入到 RN  的子目录中，参照[搭建开发环境](https://www.react-native.cn/docs/environment-setup)完成 [Node](http://nodejs.cn)、[Watchman](https://facebook.github.io/watchman)、[Yarn](http://yarnpkg.com/) 的安装，并通过命令安装 RN

> yarn add react-native

这里需要注意的是，我们是根据已有的子某块来创建的，所以我们还需要安装指定版本的 React

> yarn add react@xx.xx.xx

再次，安装成功之后，我们通过 CocoaPods 来完成相关依赖的安装。建议使用官方推荐 Podfile 完成安装

```ruby
require_relative '../node_modules/react-native/scripts/react_native_pods'
require_relative '../node_modules/@react-native-community/cli-platform-ios/native_modules'

platform :ios, '12.4'
install! 'cocoapods', :deterministic_uuids => false

production = ENV["PRODUCTION"] == "1"

target 'HelloWorld' do
  config = use_native_modules!

  # Flags change depending on the env values.
  flags = get_default_flags()

  use_react_native!(
    :path => config[:reactNativePath],
    # to enable hermes on iOS, change `false` to `true` and then install pods
    :production => production,
    :hermes_enabled => flags[:hermes_enabled],
    :fabric_enabled => flags[:fabric_enabled],
    :flipper_configuration => FlipperConfiguration.enabled,
    # An absolute path to your application root.
    :app_path => "#{Pod::Config.instance.installation_root}/.."
  )

  target 'HelloWorldTests' do
    inherit! :complete
    # Pods for testing
  end
  
end
```

你可以将 `react_native_pods` 文件移到原生项目目录，移除 `hermes` 和 `fabric` 这两个三方库，其余为 RN 必备的核心库。`native_modules` 中对应的是项目中添加的其他三方依赖的内容，你也可以手动安装。

最后，新增官网项目中的两个 `Build Phase` 用于启动 RN 服务。分别是

```shell
export RCT_METRO_PORT="${RCT_METRO_PORT:=8081}"
echo "export RCT_METRO_PORT=${RCT_METRO_PORT}" > "${SRCROOT}/../node_modules/react-native/scripts/.packager.env"
if [ -z "${RCT_NO_LAUNCH_PACKAGER+xxx}" ] ; then
  if nc -w 5 -z localhost ${RCT_METRO_PORT} ; then
    if ! curl -s "http://localhost:${RCT_METRO_PORT}/status" | grep -q "packager-status:running" ; then
      echo "Port ${RCT_METRO_PORT} already in use, packager is either not running or not running correctly"
      exit 2
    fi
  else
    open "$SRCROOT/../node_modules/react-native/scripts/launchPackager.command" || echo "Can't start packager automatically"
  fi
fi
```

和

```shell
set -e

WITH_ENVIRONMENT="../node_modules/react-native/scripts/xcode/with-environment.sh"
REACT_NATIVE_XCODE="../node_modules/react-native/scripts/react-native-xcode.sh"

/bin/sh -c "$WITH_ENVIRONMENT $REACT_NATIVE_XCODE"
```

至此，完成了在 iOS 中使用 Pod 在现有项目上集成 RN

以上就是单应用集成 RN 的方式，建议可以比对 CLI 自动化处的 iOS 项目来创造属于自己的脚本。

### 参考资料

[iOS 已有项目利用 Pod 集成 RN](https://blog.csdn.net/ljmios/article/details/119451577 "iOS 已有项目利用 Pod 集成 RN")

[git-submodules](https://git-scm.com/docs/git-submodule "git-submodules")

## 内容推荐

1、 [开源｜WBBlades 重要节点更新-专为提效而设计](https://mp.weixin.qq.com/s/tXxhnDKerobyxoWuEBGjNQ) -- 来自：58技术

[@皮拉夫大王]()：给 iOS 开发人员提供基于 Mach-O 文件解析的工具集，工具包括无用类检测（支持 OC 和 Swift）、包大小分析（支持单个静态库/动态库的包大小分析）、点对点崩溃解析（基于系统日志，支持有符号状态和无符号状态），主要基于 Mach-O 文件的分析、轻量符号表剥离，系统日志解析等技术手段。

2、[iOS 不必现崩溃的点对点解析以及治理](https://mp.weixin.qq.com/s/tGvE-2flzhm4skkrfbUIBA) -- 来自：58技术

[@皮拉夫大王]()：本文章中介绍 iOS 端发生崩溃后，在无法复现的情况下如何针对各种不同类型的崩溃日志进行解析，包括普通堆栈，wakesup 崩溃，json 格式日志，bugly 堆栈类型等。此外还介绍了系统日志存在异常情况进行自动修正的方法，包括进程名称丢失，基地址丢失，偏移地址错误等。

3、[西瓜视频iOS启动优化实践](https://juejin.cn/post/7122472926792089607 "西瓜视频iOS启动优化实践") -- 来自：QYizhong

[@Mimosa](https://juejin.cn/user/1433418892590136)：本文介绍了在西瓜视频在 iOS 启动方面做了哪些努力去优化，将启动时面临的问题都一一列出，并根据问题的不同性质和影响阶段，提供了不同的优化的方案，并配上精致的动画来帮助读者理解优化前后的区别。同时也介绍了防劣化与监控的相关知识和实践来保证保持优化效果以及感知线上劣化情况。

4、[Background Modes Tutorial: Getting Started](https://www.raywenderlich.com/34269507-background-modes-tutorial-getting-started "Background Modes Tutorial: Getting Started") -- 来自：raywenderlich

[@Mimosa](https://juejin.cn/user/1433418892590136)：这是一篇面向新手的 Background Modes 开发指南，通过该教程，你可以了解到应用程序可以在后台执行的逻辑，以及四个样例：播放音频、获取位置更新、有限长度任务、后台请求。并且有 Swift 5.5 的代码工程样例佐以配合。

5、[WWDC 22 Sessions 手绘笔记](https://drive.google.com/drive/folders/1Ux57jowC_IziRpJgPrvqf4M6GlLxslOL "WWDC 22 Sessions 手绘笔记") -- 来自：manu

[@Mimosa](https://juejin.cn/user/1433418892590136)：来自 Apple 系统开发工程师 [manu](https://twitter.com/codePrincess) 的 WWDC 22 手绘笔记，包含多个 What's New 系列以及 Create ML、Actors 等热门 session。她的手绘笔记制作精美、风格强烈，言简意赅的概括了 session 的内容，非常推荐大家看一下。

6、[SwiftUI Split View Configuration](https://useyourloaf.com/blog/swiftui-split-view-configuration "SwiftUI Split View Configuration") -- 来自：useyourloaf

[@Mimosa](https://juejin.cn/user/1433418892590136)：本文主要讨论了在 iOS 16 SwiftUI 中使用 NavigationSplitView 创建两列或三列布局的过程，提到了一些在 beta 或者之后版本可能出现的坑以及对应的解决方案。

## 摸一下鱼

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[Flowful](https://flowful.app "Flowful") 是一个提供多种氛围类型环境音乐（ 由程序生成 ）的播放器网站。其目标是通过可定制的环境音乐生成器来激发无尽的专注。经过试听后，很难说这些音乐是否能够起到开发助力器的作用，但相当地适合冥想。目前网站提供的音乐大多数都是免费的。

![Flowful](https://cdn.zhangferry.com/Images/flowful.png)

2、[Tencent/lemon-cleaner](https://github.com/Tencent/lemon-cleaner "Tencent/lemon-cleaner")：腾讯柠檬清理是针对 macOS 系统专属制定的清理工具。主要功能包括重复文件和相似照片的识别、软件的定制化垃圾扫描、可视化的全盘空间分析、内存释放、浏览器隐私清理以及设备实时状态的监控等。重点聚焦清理功能，对上百款软件提供定制化的清理方案，提供专业的清理建议，帮助用户轻松完成一键式清理。

腾讯的柠檬清理在上周开源了。这个 app 是针对 macOS 系统专属制定的清理工具。此次开源的是完整版本（ App Store 版本中功能不全 ）。社区对于腾讯的这次开源行为给予了良好的反馈，48 小时该项目已经获得了 1K+ 的 star 。由于此次的开源很突然且并不符合腾讯的一贯风格，不少人打趣说是否开发团队领大礼包了。

![腾讯柠檬清理](https://cdn.zhangferry.com/Images/lemon-cleaner.png)

3、[便携小空调](http://game.waimai.zone/air/ "便携小空调")：今年夏天，世界各地都进入了烤箱模式，每个人都渴望在充满冷气的房间里，听着音乐，喝着冷饮。便携小空调将为你提供全方位的空调体验（ 除了不制冷 ），为你的精神空间带来一丝冰凉。

![便携小空调](https://cdn.zhangferry.com/Images/air-conditioner.png)

4、[Awesome Readme Template](https://github.com/Louis3797/awesome-readme-template "Awesome Readme Template")：一个开源项目，提供了数种 Readme 模板。降低使用者创建文档的难度，为摸鱼提供便利。

5、[回村三天，二舅治好了我的精神内耗](https://www.bilibili.com/video/BV1MN4y177PB?spm_id_from=333.337.search-card.all.click&vd_source=47c38aa7a1b9837457a41f3f489f9377 "回村三天，二舅治好了我的精神内耗")：从夏日祭到 CBA 侵权，最近几天 B 站的日子不太好过。不知道横空出世的二舅能否缓解 BiliBili 的危机。

6、[文昌哪些地方可以观测火箭发射](http://haikou.bendibao.com/tour/20201030/47241.shtm "文昌哪些地方可以观测火箭发射")：随着“问天”舱的对接成功，我国的空间站建设又向前迈进了一大步。2022 下半年海南文昌还会迎来多次的发射，有兴趣现场观看的小伙伴应该提前做好攻略。

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #61 |  Developer 设计开发加速器](https://mp.weixin.qq.com/s/WfwqRhC-9-isUanv8ZnvMQ)

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/Sv3goAv198eXjmlVJsN1rw)

[iOS 摸鱼周报 #59 | DevOps 再理解 ](https://mp.weixin.qq.com/s/LJNCo0Eg11shGZN75-TZcg)

[iOS 摸鱼周报 #58 | 极客风听歌网站，纯文字音乐播放器](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
