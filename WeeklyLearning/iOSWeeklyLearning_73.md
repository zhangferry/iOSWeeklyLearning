# iOS 摸鱼周报 #73 | macOS Ventura 初体验

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：Apple Search Ads 新增广告位；macOS Ventura 体验
> * 本周学习：Swift 函数派发方式总结
> * 内容推荐：网络监控内容推荐，iOS 博主在新西兰找工作的心路历程
> * 摸一下鱼：多种脚本语言中优雅处理参数的三方库

## 本期话题

### [Apple Search Ads 新增广告位](https://searchads.apple.com/advanced "Apple Search Ads 新增广告位")

[zhangferry](zhangferry.com)：Apple Search Ads 是 Apple 自己的广告投放产品，它主要用于 App Store 内的广告投放。原来广告位是在搜索结果页（不搜索时也会展示广告），最近又新增了两个广告入口（国区没有），一个是 Today 产品卡片的底部，一个是在产品详情页的底部。

![](https://cdn.zhangferry.com/Images/20221027230936.png)

关于 Apple 对广告位的扩展，遭到不少人的反对，主要集中在这几点：

* Apple 在注重隐私的背景下逐步限制 Facebook 和 Google 等的广告追踪能力，而自己却在一步步扩大广告的范围。限制广告追踪难道不是在为自己的广告业务铺路？
* 广告最重要的是精准推荐，Apple Search Ads 如果说推荐精准那是不是就意味着它在分析用户行为。
* 按照这个趋势，Apple 很有可能还会在 App Store 或者其他系统级应用层面添加广告位。

### macOS Ventura 体验

![](https://cdn.zhangferry.com/Images/20221030212611.png)

[@zhangferry](zhangferry.com)：macOS Ventrua 已经发布了正式版，家里电脑涉及开发环节介绍，就很自信的进行了升级。听说有些人升级之后不少软件没有适配，直接用不了了，所以升级之前对于强依赖的软件可以上网查一下是否能够正常运行再决定是否升级。新系统体验一段时间之后，有这些功能值得说一下。

* 设置界面大改，跟 iPhone 风格保持一致：用意应该是想统一 macOS 与 iOS 的交互，对于初次从 iPhone 切换到 macOS 的用户比较友好。但对于习惯了老板 macOS 设置界面的人来说，有点难受，很多内容都需要重新适应。
* Stage Manager（台前调度）：它是一个独立功能，如果打开，当桌面出现超过 1 个窗口时就会自动触发，将多余窗口折叠到屏幕一侧变成缩略窗口，一块显示器中缩略窗口最多有 5 组，双显示器就是 10 组，基本满足大多数情况了。一屏如果超过 5 组，较早折叠的会被覆盖，手动将缩略窗口拖出，还可以让一屏同时展示多个窗口。如果想查看桌面的文件，可以点击屏幕空白切换，再次点击切换为窗口模式。习惯了之后感觉还是挺实用的一项功能。
* Spotlight 加强：可以搜索更详细的内容，这项提升是跟 iOS 一起的，结合图片中的文字识别，搜索结果会更加丰富。我测试发现还能搜索 iCloud 里的内容
* Metal 3：Metal 3 的意义不仅是在 Mac 端能够直接开发出特效更加复杂的游戏，它凭借很多渲染层面的补足及加强，能够让很多 DirectX 的游戏可以相对完整的转换到 Metal 3 上，但就这个层面来说，Mac 端可玩的游戏就会有很大补充。[《生化危机 村庄》](https://www.residentevil.com/village/en-asia/mac/ "《生化危机 村庄》")也已经登录 Mac App Store，售价 39.99 美元，国区没有上线。根据网上的测评这款游戏在 Mac 上的表现还不错，期待未来有更多游戏大作登录 Mac。

## 本周学习

整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)

#### Swift 函数派发方式总结

`Swift` 当中主要有三种派发方式
- sil_witness_table/sil_vtable：函数表派发
- objc_method：消息机制派发
- 不在上述范围内的属于直接派发



这里总结了一份 `Swift` 派发方式的表格

|            |                         **直接派发**                         |  **函数表派发**  |                   **消息派发**                   |
| :--------: | :----------------------------------------------------------: | :--------------: | :----------------------------------------------: |
|  NSObject  |                @nonobjc 或者 final 修饰的方法                | 声明作用域中方法 |         扩展方法及被 dynamic 修饰的方法          |
|   Class    |        不被 @objc 修饰的扩展方法及被 final 修饰的方法        | 声明作用域中方法 |  dynamic 修饰的方法或者被 @objc 修饰的扩展方法   |
|  Protocol  |                           扩展方法                           | 声明作用域中方法 | @objc 修饰的方法或者被 objc 修饰的协议中所有方法 |
| Value Type |                           所有方法                           |        无        |                        无                        |
|    其他    | 全局方法，staic 修饰的方法；使用 final 声明的类里面的所有方法；使用 private 声明的方法和属性会隐式 final 声明； |                  |                                                  |

##### 协议 + 拓展

由上表我们可以得知，在 `Swift` 中，协议声明作用域中的方法是函数表派发，而拓展则是直接派发，当协议当中实现了 `print` 函数，那么最后调用会根据当前对象的实际类型进行调用 

```Swift
protocol testA{
  func print()
}

extension testA{
  func print(){
    print("print A")
  }
}

struct testStruct:testA {
  func print(){
    print("print B")
  }
}

let one:testA = testStruct()
let two:testStruct = testStruct()
one.print() // print B
two.print() // print B
```

**追问：如果 `protocol` 没有实现 `print()` 方法，又出输出什么？**

```swift
protocol testA{}

extension testA{
  func print(){
    print("print A")
  }
}

struct testStruct:testA {
  func print(){
    print("print B")
  }
}

let one:testA = testStruct()
let two:testStruct = testStruct()
one.print() // print A
two.print() // print B
```

因为协议中没有声明 `print` 函数，所以这时，`one` 被声明成`testA` ， 只会按照拓展中的声明类型去进行直接派发

而 `two` 被声明成为 `testStruct`，所用调用的是 `testStruct` 当中的 `print` 函数


## 内容推荐

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1、[Check for internet connection with Swift](https://stackoverflow.com/questions/30743408/check-for-internet-connection-with-swift "Check for internet connection with Swift") -- Stack Overflow

[@夏天](https://juejin.cn/user/3298190611456638): 当存在在 iOS App 上监测网络状态的需求时，不妨看一看这个提问，在回答中介绍了通过 `SCNetworkReachability` 来实现网络状态监听及 `NWPathMonitor`。如果你的系统支持的版本在 `iOS 12` 以上并且你有需要实现一个网络状态监听的程序，可以试一试`NWPathMonitor`。

2、[Detecting Internet Access on iOS 12+ | by Ross Butler | Medium](https://medium.com/@rwbutler/nwpathmonitor-the-new-reachability-de101a5a8835 "Detecting Internet Access on iOS 12+ | by Ross Butler | Medium") -- Medium

[@夏天](https://juejin.cn/user/3298190611456638): 这是一篇关于如果通过 `NWPathMonitor` 来实现 `iOS 12` 以上实现网络可达性判断的文章，文章介绍了 `NWPathMonitor` 的优点以及在后面断网时的不足，并且介绍了一个兼容的库 [Connectivity](https://github.com/rwbutler/Connectivity)，但是该库由于使用了 `Combine` 并不兼容 iOS 13 以下了。

3、[我是如何在新西兰找到iOS开发工作的？](https://www.youtube.com/channel/UCiEbxa6e5o3mtBJIwhRxbHA?sub_confirmation=1 "我是如何在新西兰找到iOS开发工作的？")-- 陈宜龙(@iOS程序犭袁)

[@夏天](https://juejin.cn/user/3298190611456638):  陈宜龙大佬是我学习 iOS 比较追寻的一个博主了，最近他润去了新西兰，可以查看他的其他的  `YouTube`  视频。


## 摸一下鱼

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

1、最近在写脚本，这期介绍几个帮助脚本语言接收参数更优雅的三方库；

- shell: [getoptions](https://github.com/ko1nksm/getoptions "getoptions")
- python: [python-fire](https://github.com/google/python-fire "python-fire")
- js：[commander.js](https://github.com/tj/commander.js "commander.js")
- ruby：[commander](https://github.com/commander-rb/commander "commander")

2、[原神助手 - mac端](https://github.com/zhangferry/genshin-helper "原神助手-mac端")：最近完了一段时间原神，偶然间看到一个原神助手的工具：[vikiboss/genshin-helper](https://github.com/vikiboss/genshin-helper "vikiboss/genshin-helper")，支持原神签到、祈愿分析、游戏详细数据等功能。项目是基于 Electron 和 React 开发的，作者因为没有 mac 电脑，仅提供了windows的包。于是我 fork 了该项目，添加了 mac 版本的包，大家如果有需要可以自行下载。

祈愿分析抓取祈愿详情分析页面的链接填入即可。

![](https://cdn.zhangferry.com/Images/20221103093409.png)

3、[网页飙车](https://slowroads.io/ "网页飙车")：该游戏可以通过程序自动生成景观和道路，用户可以在这条路上驾驶，无需登录，无需安装，只有无尽的道路。

如果不想亲自开车的话，按 F 键可以打开自动驾驶，用 E 键切换自己喜欢的场景，用 C 键切换摄像头，只是看看风景，享受坐车的乐趣。

![](https://cdn.zhangferry.com/Images/20221030162820.png)

## 岗位内推

**[上海/北京] 小红书 - 客户基础架构技术团队 - iOS - P6/P7/P8**

### 团队介绍
小红书是中文互联网最后的独角兽，字节一直在模仿从来没超越的对手，月活超过 2 亿，大厂中唯一一家 iOS 用户量占比能够达到 50% 的公司。

客户端基础架构团队致力于打造最佳的移动端体验，核心业务包括稳定性、性能、埋点与数据监控、日志/网络/路由等基础组件、工程效率和代码质量、RN 引擎容器等方面。技术栈采用 Swift 为主，提供了完整的基于语言特性的基础能力，可以大幅提升客户端开发的研发效率。

### 岗位描述
 1. 熟悉社区/社交/内容形态的产品，对用户体验负责
 2. 打造极致的 App 性能和稳定性
 3. 提升客户端研发幸福感，提高团队研发效率
 4. 参与关键方案设计，用技术和数据解决问题

### 岗位要求
有过千万级 DAU App 的基础架构方面开发经验，具有钻研 iOS 系统底层实现与优化的能力，能够对行业最前沿技术保持好奇心，对技术推动业务有深刻理解。

### 内推联系方式

JY微信：q491964334、安滋：18616378992，anzi@xiaohongshu.com

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #72 | 1024 开始预热](https://mp.weixin.qq.com/s/WUVAHbJe_dmA-DVFXpF2Qw)

[iOS 摸鱼周报 #71 | iOS / One More Thing?](https://mp.weixin.qq.com/s/0mAKYvVuPLKEA2qnsNfCvQ)

[iOS 摸鱼周报 #70 | iOS / iPadOS 16.1 公测版 Beta 3 发布，支持老款 iPad 台前调度](https://mp.weixin.qq.com/s/rSPC8lgvUKPKfgR53xdHqg)

[iOS 摸鱼周报 #69| 准备登陆灵动岛](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
