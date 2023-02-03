# iOS 摸鱼周报 #82 | 去中心化社交软件 Damus

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：设计开发加速器线下活动：女性开发者社区日；
> * 本周学习：Python 如何调用 Swift 程序
> * 内容推荐：涵盖现代 SwiftUI 编程探讨、可变视图、NSTimer、Swift Charts 等方面的内容
> * 摸一下鱼：去中心化社交软件 Damus；2022 年最后欢迎的 Chrome 插件；一款通过工作流驱动提效的办公工具 monday

## 本期话题

### [设计开发加速器线下活动：女性开发者社区日](https://developer.apple.com/events/view/CN36QR48T5/dashboard "设计开发加速器线下活动：女性开发者社区日")

[@远恒之义](https://github.com/eternaljust)：Apple 在 2022 年 10 月开展了 Apple Entrepreneur Camp（苹果企业家培训营）课程活动，主要面向女性、黑人和西班牙裔/拉丁裔创业者，帮助她们提供技术支持与免费服务。女性开发者社区日是针对中国女性开发者的特别活动，以此帮助更多的中国女性开发者熟悉了解 Apple 平台。相比之前的企业家培训营要求，本次活动降低了门槛，参会资格不再限制组织必须满足女性创业者与女性开发者。

![](https://cdn.zhangferry.com/Images/82-women-developer-community-day.jpeg)

### [App 和 App 内购买项目即将实行税率和价格调整](https://developer.apple.com/cn/news/?id=g8dce2t4 "App 和 App 内购买项目即将实行税率和价格调整")

[@远恒之义](https://github.com/eternaljust)：2023 年 2 月 13 日起，哥伦比亚、埃及、匈牙利、尼日利亚、挪威、南非和英国 App Store 的 App 及 App 内购买项目 (自动续期订阅除外) 的价格将上调。从 2023 年春季起，App 和 App 内购买项目的定价功能升级将带来 700 个新增的价格点，开发者可更加灵活地管理全球各地区定价。

## 本周学习

整理编辑：[zhangferry](https://zhangferry.com)

### Python 如何调用 Swift 程序

Swift 调用 Python 有现成的方案，就是 [PythonKit](https://github.com/pvieito/PythonKit "PythonKit")，这个库是从 TensorFlow 迁移出来的，利用 Swift 里 `@dynamicCallable`和 `@dynamicMemberLookup`实现动态调用。

Python 调 Swift 则相对绕一些，核心思路是将 Swift 转成 C 语言库，然后利用 Python 的`ctypes` 去调用这个 C 语言库。大概流程如下：

![](https://cdn.zhangferry.com/Images/20230203004524.png)

1、导出 C 语言符号。

```swift
@_cdecl("myname")
public func myname (x: UnsafePointer<CChar>) -> UnsafePointer<CChar>{
    let ret : String = "My name is \(String(cString: x))"
    return UnsafePointer<CChar>(ret)
}
```

Swift 在编译时会根据命名空间和参数进行符号签名，为了保证符号的统一性，使用`@_cdecl`固定函数签名。另外C 语言的字符串跟Swift字符串不同，将字符串转成`UnsafePointer<CChar>`类型指针。

2、生成动态库让 ctypes 引用

```bash
$ swiftc -emit-library modules.swift
```

生成的动态库为`libmodules.dylib`。有时候还会出现一些动态库依赖关系，为了让 ctypes 也能够找到这个库，还需要修改动态检索路径：

```bash
export DYLD_FRAMEWORK_PATH="path/to/depend_dylib_folder"
```

该环境变量的指定要在 python 脚本外部执行。

3、python 通过 ctypes 调用对应函数

需要注意的是不同语言之间的类型转换

| ctypes   | Python | C      | Swift  |
| -------- | ------ | ------ | ------ |
| c_int    | int    | int    | Int    |
| c_char_p | str    | char * | String |

关于ctypes使用可以参看官方文档：[ctypes Python 的外部函数库](https://docs.python.org/zh-cn/3/library/ctypes.html#module-ctypes "ctypes`Python的外部函数库")。

以下是调用示例：

```python
import ctypes
# 把对应动态库转成ctypes类型
modules = ctypes.CDLL('path/to/libmodules.dylib')

def py_myname(x):
    # 定义返回值类型
    modules.myname.restype = ctypes.c_char_p
    # python str to char
    y = ctypes.c_char_p(x.encode())
    # char to python str
    return modules.myname(y).decode()
    
str = py_myname("zhangferry")
print(str)  # My name is zhangferry
```

## 内容推荐

本期将推荐近期的一些优秀博文，涵盖现代 SwiftUI 编程探讨、可变视图、NSTimer、Swift Charts 等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[现代 SwiftUI](https://www.pointfree.co/blog/posts/94-modern-swiftui-parent-child-communication "现代 SwiftUI") -- 来自：Piont Free

[@东坡肘子](https://www.fatbobman.com/): 近期 Point Free 在其博客上发表了多篇免费文章，以探索现代 SwiftUI 开发的最佳实践。内容涵盖：视图沟通、可识别数组、状态驱动导航、依赖项、测试等内容。

2、[可变视图](https://chris.eidhof.nl/post/variadic-views/ "可变视图") -- 来自：Chris Eidhof

[@东坡肘子](https://www.fatbobman.com/): _VariadicView 是 SwiftUI 提供的一个未公开 API ，它为布局容器提供了遍历子视图的能力。Chris Eidhof 在 [Moving Parts](https://movingparts.io/variadic-views-in-swiftui) 博客的基础上进一步对该 API 进行了研究，并提出了视图是列表的观点。

3、[NSTimer Block 为什么不会触发循环引用？！](https://juejin.cn/post/7194064273960599611 "NSTimer Block 为什么不会触发循环引用？！") -- 来自：wiiale

[@东坡肘子](https://www.fatbobman.com/): NSTimer 是 iOS Foundation 框架中一种计时器，在经过一定的时间间隔后触发，向目标对象发送指定的消息。本文将通过探究 NSTimer 与 Runloop 之间的关系来分析不会触发循环引用的原因。

4、[Searchable](https://kean.blog/post/pulse-search "Searchable") -- 来自：Alex Grebenyuk

[@东坡肘子](https://www.fatbobman.com/): 从 iOS 15 开始，SwiftUI 通过新的 .searchable 修饰符开始支持搜索栏功能。Alex Grebenyuk 通过本文将其在 Pulse 应用中有关 searchable 的使用体验和心得分享给大家。

5、[掌握 Swift Charts](https://swiftwithmajid.com/2023/01/26/mastering-charts-in-swiftui-custom-marks/ "掌握 Swift Charts") -- 来自：Majid

[@东坡肘子](https://www.fatbobman.com/): Swift Charts 是苹果的一个新框架，允许我们使用 SwiftUI 以声明性的方式可视化数据。Majid 将通过多篇文章对 Swift Charts 进行详尽介绍，目前已以完成：基础、自定义标记、标记样式等内容。

## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[Damus](https://damus.io/ "Damus")：一个建立在去中心化网络上的社交软件，最近挺火的，被称为「推特杀手」，目前已上线 App Store，国区没有。它具有这些特点：

* 你发的内容完全由你自己控制
* 端到端加密，交流过程无法被其他人查看
* 无注册限制，创建账户会生成一对公私钥，公钥表示你的id，可以让其他人找到你，私钥表示登录凭证
* 无中心服务器，而是利用去中心化中继器来分发消息
* 可编程，支持自定义机器人，用于处理消息分发和通知
* 可以赚钱，利用比特币给帖子打赏

App 端目前功能还比较粗糙，可以通过 [iris](https://iris.to/ "iris") 体验这种社交形式。去中心化优点是自由，不会有人删你帖子，但缺点也明显，容易成为非法活动的温床。它能提供的价值有多大以及多大范围内能成为主流社交平台，还有待观察。

![](https://cdn.zhangferry.com/Images/20230202222757.png)

2、[2022 年最受欢迎的 Chrome 插件](https://blog.google/products/chrome/our-favorite-chrome-extensions-of-2022/ "2022 年最受欢迎的 Chrome 插件")：这些插件覆盖工作、学习、娱乐多个方面，列几个我感觉还不错的插件：

* [Tango](https://chrome.google.com/webstore/detail/tango-screenshots-trainin/lggdbpblkekjjbobadliahffoaobaknh?hl=en "Tango")：对于一个复杂的操作页面，如果我们想演示如何操作，可以利用 Tango 快速生成一个操作步骤指南。

* [workona](https://chrome.google.com/webstore/detail/workona-tab-manager/ailcmbgekjpnablpdkmaaccecekgdhlh?hl=en "workona")：一个书签管理插件，我看大部分人使用 chrome 都会出现 tab 栏占满的情况，tab 管理对我来说也一直是一个头疼的事情。这个插件提供了一种解决方案，就是为所有页面和书签建一个管理页面，每次对tab的切换都通过这个管理页面进行。

  ![](https://cdn.zhangferry.com/Images/20230202232756.png)

3、[monday](https://monday.com "'monday'")：一个面相工作场景的项目管理平台，可以定制工作流来满足不同工作的需求，从而提高团队的一致性、效率和生产力。

![](https://cdn.zhangferry.com/Images/20230202234211.png)

4、Github 在个人信息页面新增了社交网络的链接，可以填四个链接：

![](https://cdn.zhangferry.com/Images/20230202225613.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #81 | Apple 推出 Apple Business Connect](https://mp.weixin.qq.com/s/Ek6W0MTBDP6PN1uxWQ5M_A)

[iOS 摸鱼周报 #80 | 开发加速器 SwiftUI 中管理数据模型](https://mp.weixin.qq.com/s/eIQLuAIsRQ7eeEnsrL5QuA)

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 | 用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
