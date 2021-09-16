# iOS摸鱼周报 第二十七期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：跟 RunsCode 聊聊编程和兴趣爱好，以及如何在 1min 之内复原魔方😏。
>
> * Tips：iOS 识别虚拟定位调研；使用 App Store Connect API Key 解决 Fastlane 双重验证问题。
> * 面试模块：KVC 取值和赋值过程的工作原理。
> * 优秀博客：关于 Combine 的相关文章推荐。
> * 学习资料：阮一峰最新发布的 C 语言入门教程，GitHub 漫游指南。
> * 开发工具：Xcode 工程管理工具 XcodeProjects。

## 本期话题

[@zhangferry](https://zhangferry.com)：这期参与访谈的对象是摸鱼周报的另一个编辑：[RunsCode](https://github.com/RunsCode)，RunsCode 在我看来是一个非常酷的人。这个酷来自于他很强的学习能力和个人要求，编程和兴趣爱好都能被他玩出花来。下面通过几个问题，一起了解下他。

zhangferry：简单介绍下自己吧。

> Hello，大家好我是 RunsCode，目前就职于 Hello出行，坐标杭州。
>
> 小时候因为沉迷于电脑游戏，毕业后入坑做手游，后来机缘巧合之下结识 iOS，从此移情别恋了，跟 iOS 相爱相杀至今。

zhangferry：你的学习范围比较广，安卓、Ruby、Applescript 都有写过，你是在什么场景下接触一门新语言的？学习一门新的语言，首先应该关注哪部分内容？

> 因为之前做的 cpp 游戏要做移动端跨平台移植对接移动支付 SDK，被迫学了 Android 和 iOS，但是还是被 iOS 的纯粹给吸引了。后来在 15 年搞 iOS 的过程中来了一个 CSDN 当时前十的大神当我们领导，开拓视野学习 Swift 和 Ruby，因为他说 Swift 借鉴了很多 Ruby 的特性，再加上 CocoaPods 也是 Ruby 写的，也就稍稍学习了一下。AppleScript 也是这个 CSDN 大神提醒的搞 Mac 自动化，后来也是一发不可收拾。
>
> 这些语言对我而言他们共性是让我写起来很开心，就像那种小孩子看到好吃的那种感觉（主要说 Swift 和 Ruby）
> 其实学语言都是有针对的学习，不同的语言都是有自己擅长的领域，比如说我要用 Ruby 写一个 iOS App，这就有点过分了，相比 OC/Swift 这就不是很适合了，虽说有点过分，但是真的有人这么干了，可以了解下 [RubyMotion](http://www.rubymotion.com/ "RubyMotion")，真是极客啊。
>
> 个人觉得学习一门新语言除了一开始掌握基本的词法语法之外，慢慢的你就会发现这个语言跟你有没有共鸣，你的思路跟它的处理逻辑是不是很契合，就像大家都喜欢脚本 Python 我却更喜欢 Ruby，这主要是Ruby 的处理逻辑跟我很契合，就是同样的展示你用德玛习惯，我却用吕布更加习惯。

zhangferry：听说你乒乓球和魔方都玩的很好，这些东西的学习跟编程有没有什么共性呢？我之前也着迷过一段时间魔方（三阶），但最快也要 2min 以上，听说你的记录是 15s。由不会到会再到熟练是相对简单的过程，一般人都能做到，但再往上突破就很难了。就魔方来说，1min 对我来说就是一个大的突破了，如果要达到这一步需要做哪些事情呢？

> 乒乓球会一点，请过教练专门训练过基础技能，不能说玩的很好，跟小区大爷打球有时候经常翻车的，尤其打长胶翻车不少，哎......
>
> 魔方这个吧，就是比一般复原的稍微快一点，三阶止步 CFOP。
>
> 跟编程的共性：兴趣第一， 然后就是坚持，用正确的方法刻意练习就是了（高手都是寂寞的）。
>
> 一分钟还原三阶魔方来说，学会七步还原法，然后在苦练一个礼拜，每天练习两个小时应该就差不多了。当然掌握正确手法的天赋型选手也许只要两三天。
>
> 然后最重要的事情说三遍，买个好魔方， 买个好魔方， 买个好魔方！！！
> 千万不要买路边摊十块钱那种啊，那种容易卡住或者 POP（就是爆炸开了），及其打击自信，过来人血的教训。
>
> 怎么的也得三十块起步，国甲，孤鸿，圣手这种吧。
>
> ![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/魔方.jpeg)

zhangferry：学习很多时候并不是有趣的，该如何保持学习热情？

> 这个我不知道怎么回答，或许是好奇，或许是焦虑，或许是爱好兴趣。我只知道是这三点支配了我。还有就是我只做自己喜欢的事情，我从不跟风，跟风容易迷失自己，适合别人的不一定适合自己。
>
> 主要还是要坚持，坚持下去能让人更坚定。时间长了你就习惯学习了，如果突然一下子你不学习，你是不是都会感到空虚、焦虑和内疚吧，哈哈哈。
>

zhangferry：说一个最近的思想感悟吧。

> 提升生活幸福感还是要终身学习，不仅限于工作技能，其他一切都可以。

## 开发Tips

整理编辑：[FBY展菲](https://github.com/fanbaoying)、[zhangferry](https://zhangferry.com)

### iOS 识别虚拟定位调研

#### 前言

最近业务开发中，有遇到我们的项目 App 定位被篡改的情况，在 `Android` 端表现的尤为明显。为了防止这种黑产使用虚拟定位薅羊毛，`iOS` 也不得不进行虚拟定位的规避。

#### 第一种：使用越狱手机

一般 App 用户存在使用越狱苹果手机的情况，一般可以推断用户的行为存在薅羊毛的嫌疑（也有 App 被竞品公司做逆向分析的可能），因为买一部越狱的手机比买一部正常的手机有难度，且在系统升级和 `Appstore` 的使用上，均不如正常手机，本人曾经浅浅的接触皮毛知识通过越狱 `iPhone5s` 进行的 App 逆向。

**代码实现**

```swift
/// 判断是否是越狱设备
/// - Returns: true 表示设备越狱
func isBrokenDevice() -> Bool {

    var isBroken = false

    let cydiaPath = "/Applications/Cydia.app"

    let aptPath = "/private/var/lib/apt"

    if FileManager.default.fileExists(atPath: cydiaPath) {
        isBroken = true
    }

    if FileManager.default.fileExists(atPath: aptPath) {
        isBroken = true
    }

    return isBroken
}
```

#### 第二种：使用爱思助手

对于使用虚拟定位的场景，大多应该是司机或对接人员打卡了。而在这种场景下，就可能催生了一批专门以使用虚拟定位进行打卡薅羊毛的黑产。对于苹果手机，目前而言，能够很好的实现的，当数爱思助手的虚拟定位功能了。

**使用步骤：** 下载爱思助手 Mac 客户端，连接苹果手机，工具箱中点击虚拟定位，即可在地图上选定位，然后点击修改虚拟定位即可实现修改地图的定位信息。

**原理：** 在未越狱的设备上通过电脑和手机进行 `USB` 连接，电脑通过特殊协议向手机上的 `DTSimulateLocation` 服务发送模拟的坐标数据来实现虚假定位，目前 `Xcode` 上内置位置模拟就是借助这个技术来实现的。

**识别方式**

一、通过多次记录爱思助手的虚拟定位的数据发现，其虚拟的定位信息的经纬度的高度是为 0 且经纬度的数据位数也是值得考究的。

二、把定位后的数据的经纬度上传给后台，后台再根据收到的经纬度获取详细的经纬度信息，对司机的除经纬度以外的地理信息进行深度比较，优先比较 `altitude`、`horizontalAccuracy`、`verticalAccuracy` 值，根据值是否相等进行权衡后确定。

三、具体识别流程

* 通过获取公网 `ip`，大概再通过接口根据 `ip` 地址可获取大概的位置，但误差范围有点大。
* 通过 `Wi-Fi` 热点来读取 `App` 位置
* 利用 `CLCircularRegion` 设定区域中心的指定经纬度和可设定半径范围，进行监听。
* 通过 `IBeacon` 技术，使用 `CoreBluetooth` 框架下的 `CBPeripheralManager` 建立一个蓝牙基站。这种定位直接是端对端的直接定位，省去了 `GPS` 的卫星和蜂窝数据的基站通信。

四、[iOS 防黑产虚假定位检测技术](https://cloud.tencent.com/developer/article/1800531 "iOS 防黑产虚假定位检测技术")

文章的末尾附的解法本人有尝试过，一层一层通过 KVC 读取 CLLocation 的 _internal 的 fLocation，只能读取到此。

参考：[iOS 识别虚拟定位调研](https://mp.weixin.qq.com/s/ZbZ4pFzzyfrQifmLewrxsw "iOS 识别虚拟定位调研")

### Fastlane 使用 App Store Connect API Key 解决双重验证问题

现在申请的 AppleId 都是要求必须要有双重验证的，这在处理 CI 问题时通常会引来麻烦，之前的解决方案使用 `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD` 和 `FASTLANE_SESSION`，但 `FASTLANE_SESSION` 具有时效性，每过一个月就需要更新一次，也不是长期方案。Fastlane 在 2.160.0 版本开始支持 Apple 的 App Store Connect API 功能。App Store Connect API 由苹果提供，需登录 App Store Connect 完成授权问题。使用方法如下：

1、在 [这里](https://appstoreconnect.apple.com/access/shared-secret) 创建共享秘钥。

请求权限：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/1_request_access-2.png)

创建秘钥：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/2_create_key-1.png)

这里的 `.p8` 秘钥文件只能下载一次，注意保存。

2、fastfile 的配置。

可以直接用 `app_store_connect_api_key` 对象配置，也可以写成 json 供多个 `lane` 共享，这里推荐使用 json 形式管理，新建一个json文件，配置如下内容：

```json
{
  "key_id": "D383SF739",
  "issuer_id": "6053b7fe-68a8-4acb-89be-165aa6465141",
  "key": "-----BEGIN PRIVATE KEY-----\nMIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHknlhdlYdLu\n-----END PRIVATE KEY-----",
  "duration": 1200, 
  "in_house": false
}
```

前面三项都是对秘钥文件的描述，可以根据自己的项目进行修改。这里需注意 `key` 的内容，原始 `.p8` 文件是带换行的，转成字符串时用 `\n` 表示换行。注意这里的值为 `key`，官网写法是 `key_content`，这是官网的错误，我开始也被坑了，已经有人提出了 [issues 19341](https://github.com/fastlane/fastlane/issues/19341 "issues 19341")。

基本所有需要登录 app conenct 的命令都包含 api_key_path 这个参数，传入 json 文件路径即可：

```json
lane :release do
  pilot(api_key_path: "fastlane/D383SF739.json" )
end
```

参考：[fastlane app-store-connect-api documents](https://docs.fastlane.tools/app-store-connect-api/ "app-store-connect-api documents")

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

本期面试解析讲解的知识点是 **KVC 取值和赋值过程的工作原理**。

**Getter**

以下是 `valueForKey:` 方法的默认实现，给定一个 `key` 作为输入参数，在消息接收者类中操作，执行以下过程。
* ① 按照 `get<Key>`、`<key>`、`is<Key>`、`_<key>` 顺序查找方法。
	<br>如果找到就调用取值并执行 ⑤，否则执行 ②；
* ② 查找 `countOf<Key>`、`objectIn<Key>AtIndex:`、`<key>AtIndexes:` 命名的方法。
	<br>如果找到第一个和后面两个中的至少一个，则创建一个能够响应所有 `NSArray` 的方法的集合代理对象（类型为 `NSKeyValueArray`，继承自 `NSArray`），并返回该对象。否则执行 ③；
    * 代理对象随后将其接收到的任何 `NSArray` 消息转换为 `countOf<Key>`、`objectIn<Key>AtIndex:`、`<Key>AtIndexes:` 消息的组合，并将其发送给 `KVC` 调用方。如果原始对象还实现了一个名为 `get<Key>:range:` 的可选方法，则代理对象也会在适当时使用该方法。
* ③ 查找 `countOf<Key>`、`enumeratorOf<Key>`、`memberOf<Key>:` 命名的方法。
	<br>如果三个方法都找到，则创建一个能够响应所有 `NSSet` 的方法的集合代理对象（类型为 `NSKeyValueSet`，继承自 `NSSet`），并返回该对象。否则执行④；
    * 代理对象随后将其接收到的任何 `NSSet` 消息转换为 `countOf<Key>`、`enumeratorOf<Key>`、`memberOf<Key>:` 消息的组合，并将其发送给 `KVC` 调用方。
* ④ 查看消息接收者类的 `+accessInstanceVariablesDirectly` 方法的返回值（默认返回 `YES`）。如果返回 `YES`，就按照 `_<key>`、`_is<Key>`、`<key>`、`is<Key>` 顺序查找成员变量。如果找到就直接取值并执行 ⑤，否则执行 ⑥。如果 `+accessInstanceVariablesDirectly` 方法返回 `NO` 也执行 ⑥。
* ⑤ 如果取到的值是一个对象指针，即获取的是对象，则直接将对象返回。
	* 如果取到的值是一个 `NSNumber` 支持的数据类型，则将其存储在 `NSNumber` 实例并返回。
	* 如果取到的值不是一个 `NSNumber` 支持的数据类型，则转换为 `NSValue` 对象, 然后返回。
* ⑥ 调用 `valueForUndefinedKey:` 方法，该方法抛出异常 `NSUnknownKeyException`，程序 `Crash`。这是默认实现，我们可以重写该方法对特定 `key` 做一些特殊处理。

**Setter**

以下是 `setValue:forKey:` 方法的默认实现，给定 `key` 和 `value` 作为输入参数，尝试将 `KVC` 调用方 `key` 的值设置为 `value`，执行以下过程。
* ① 按照 `set<Key>:`、`_set<Key>:` 顺序查找方法。
	<br>如果找到就调用并将 `value` 传进去（根据需要进行数据类型转换），否则执行 ②。
* ② 查看消息接收者类的 `+accessInstanceVariablesDirectly` 方法的返回值（默认返回 `YES`）。如果返回 `YES`，就按照 `_<key>`、`_is<Key>`、`<key>`、`is<Key>` 顺序查找成员变量（同 Getter）。如果找到就将 `value` 赋值给它（根据需要进行数据类型转换），否则执行 ③。如果 `+accessInstanceVariablesDirectly` 方法返回 `NO` 也执行 ③。
* ③ 调用 `setValue:forUndefinedKey:` 方法，该方法抛出异常 `NSUnknownKeyException`，程序 `Crash`。这是默认实现，我们可以重写该方法对特定 `key` 做一些特殊处理。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

1、[深入浅出 Apple 响应式框架 Combine](https://www.infoq.cn/article/eaq01u5jevuvqfghlqbs "深入浅出 Apple 响应式框架 Combine") -- 来自 InfoQ：青花瓷的平方

[@我是熊大](https://juejin.cn/user/1151943916921885)：本文是 Joseph Heck 编写的教程的中文版本，适合新手阅读，学习 Combine。

2、[Combine debugging using operators in Swift](https://www.avanderlee.com/swift/combine-error-handling/ "Combine debugging using operators in Swift") -- 来自博客：avanderlee

[@我是熊大](https://juejin.cn/user/1151943916921885)：使用 RxSwift 会产生大量的不可读堆栈信息，这也是开发人员放弃 RxSwift 的原因之一，在 Combine 中这一点依旧如此。但好在有一些提示和技巧可以改善，本文就介绍了几种方式。

3、[Combine: Getting Started](https://www.raywenderlich.com/7864801-combine-getting-started#toc-anchor-011 "Combine: Getting Started")  -- 来自：raywenderlich

[@我是熊大](https://juejin.cn/user/1151943916921885)：Swift Combine 的硬核教程，作者利用 UnsplashAPI 带大家实现了一个简易的 App，让我们学习了解如何使用 Combine 的发布者和订阅者来处理事件流、合并多个发布者等。

4、[Combine - 介绍、核心概念](https://zhuanlan.zhihu.com/p/154621268 "Combine - 介绍、核心概念") -- 来自知乎：Talaxy

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：提到响应式编程就不得不说 Combine。这篇文章介绍了Combine 的相关概念和用法。包括发布者-订阅者的生命周期、发布者订阅者操作者的概念等等。

5、[Apple 官方异步编程框架：Swift Combine 应用](https://nemocdz.github.io/post/apple-官方异步编程框架swift-combine-应用/ "Apple 官方异步编程框架：Swift Combine 应用") -- 来自：Nemocdz's Blog

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：本文通过例子和代码介绍了 Combine 的用法，适合了解 Combine 相关概念和基础的同学阅读。

6、[RxSwift to Combine Cheatsheet](https://github.com/CombineCommunity/rxswift-to-combine-cheatsheet "RxSwift to Combine Cheatsheet") -- 来自 GitHub：CombineCommunity

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：RxSwift 与 Combine 的对照关系，如果你想从 RxSwift 过渡到 Combine，可以参考此文章。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 阮一峰的《C 语言入门教程》

地址：https://wangdoc.com/clang

阮一峰最近新写的《C 语言入门教程》，他对该教程做了一些介绍可以看 [这里](https://mp.weixin.qq.com/s/BLNX0MtktumBvwV5tj2ZUQ)，这对想重拾 C 语言这一门手艺的读者来说一定是一个巨大的帮助。同时各位读者若发现错误和遗漏，欢迎大家到仓库提交补丁。

### Github 漫游指南

地址：http://github.phodal.com/

如果你是一名 Github 新手的话，这本《Github 漫游指南》将会带你漫游 Github 的世界，带你了解 Github 到底是什么，他有什么用，该怎么去使用它。如果你是一名老手了，它也可以带你深入平时可能不会注意的细节，帮助你更加了解这个我们每天都在使用的工具。

## 工具推荐


整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### XcodeProjects

**地址**： https://github.com/DKalachniuk/XcodeProjects

**软件状态**： 免费，开源

**软件介绍**

日常开发过程中，经常在终端中执行 pod install、pod update、或者 clear derived data 等操作，XcodeProjects 工具执行这些操作，只需要点击两下就能完成，还能为自己的项目自定义 command，很大程度的简化我们的操作步骤，节省开发时间。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/XcodeProjects.png)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第二十六期](https://mp.weixin.qq.com/s/PnUZLoyKr8i_smi0H-pQgQ)

[iOS摸鱼周报 第二十五期](https://mp.weixin.qq.com/s/LLwiEmezRkXHVk66A6GDlQ)

[iOS摸鱼周报 第二十四期](https://mp.weixin.qq.com/s/vXyD_q5p2WGdoM_YmT-iQg)

[iOS摸鱼周报 第二十三期](https://mp.weixin.qq.com/s/1Vs50Lbo0Z27dnU-ARQ96A)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
