# iOS摸鱼周报 第二十三期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 本期邀请 CoderStar 聊一下他的学习方法。
> * 简版 PromiseKit 的设计思路；如何通过配置文件区分 AdHoc/AppStore。
> * `isMemberOfClass`、 `isKindOfClass` 的含义与区别。
> * 博客部分整理了Swift 指针、Swift 属性包裹器的几篇文章。
> * 学习资料：
> * 一个帮助解析 Shell 脚本的网站：explainshell。

## 本期话题

[@zhangferry](https://zhangferry.com)：上周跟 [@展菲](https://github.com/fanbaoying) 聊过之后，有了这个跟各位博主进行访谈的想法。博主+访谈，即可以帮大家介绍优秀的开发者，又能利用访谈的形式近距离了解博主，学习他们的思考和学习方法。本期所选问题是一个初步尝试，大家如果有更好的问题，欢迎留言告诉我们。

本期介绍的博主也是摸鱼周报的一位联合编辑：[CoderStar](https://juejin.cn/user/588993964541288)。

### 博主访谈

zhangferry：简单介绍下自己和自己的公众号吧

> 自己：CoderStar，坐标北京，目前主要工作与 iOS 相关，对大前端、后端都有一定涉猎，喜欢分享干货博文。
>
> 公众号：CoderStar，分享大前端相关的技术知识，只聊技术干货，目前分享的内容主要是 iOS 相关的，后续还会分享一些 Flutter、Vue 前端等相关技术知识。目前公众号文章内容均是自己原创，很欢迎大家投稿一些好文章，大家一块进步。


zhangferry：为什么有写公众号的打算？写公众号有带来什么好处吗？

> 最开始写公众号的原因其实比较简单，
>
> 1、因为过去积累了一些笔记，比较零散，想整理一下；
>
> 2、觉得工作经验已经到了一定的阶段，也是时候将知识梳理一遍，打造自己的知识体系了，融会贯通；
>
> 3、是想把自己积累的一些技术知识分享出来，大家一起来交流，创造一个好的技术圈子，一个好的技术圈子实在是太重要了。

> 写公众号的好处：
>
> 1、写文章不仅能让我对一个知识点理解的更透彻，也增强了我的写作能力，对于技术知识而言，自己理解是一个阶段，深入浅出的写出来又是一个更高的阶段；
>
> 2、可以认识很多小伙伴，同行的路上不会孤单，比如和飞哥就是这样认识的。


zhangferry：最近在研究什么有趣的东西？是否可以透露下未来几篇文章的规划？

> 最近在做优化方面的事情，未来几篇文章可能会偏向优化系列或者底层相关。


zhangferry：如何让自己每周都能抽出时间写博客呢？有没有什么好的学习方法可以分享？

> 我目前更新的频率是一周一篇文章，一般工作日晚上会去看一些本期文章涉及的资料以及做一些代码实践，然后积累一些笔记，在周末时候将笔记进行整理聚合，形成文章，其实这个过程中还是比较累的，毕竟有的时候工作会忙，但是这个事情一定要坚持，给自己一个目标，不能随随便便就断更，毕竟有第一次断更就有第二次。
>
> 学习方法：说一点吧，我自己对于技术的态度是实践型+更优解，当看到一些好的文章的时候，会自己将文章里面的原理或者实现自己动手实践一下，考虑这个方法有什么缺点，并围绕这个技术点去思考有没有更好的解决方案，不断地去寻找更优解。

## 开发Tips

整理编辑：[RunsCode](https://github.com/RunsCode)、 [zhangferry](https://zhangferry.com)
###  如何摊平复杂逻辑流程的设计

开发中我们通常会遇到以下问题：

* 运营活动优先级问题
* 后续慢慢在使用过程中逐渐衍生新的功能（延时，轮询，条件校验等）
* 逐级递增的回调地狱

#### Talk is cheap, show code

```swift
// 1
func function0() {
    obj0.closure { _ in
        // to do something
        obj1.closure { _ in
            // to do something                      
            obj2.closure { _ in
                ...
                objn.closure { _ in
                       ...
                }         
            }             
        }        
    }
}

or
// 2.
func function1 {
    if 满足活动0条件 {
        // to do something
    } else if 满足活动1条件 {
        // to do something
    } else if 满足活动2条件 {
        // to do something
    }
    ...
    else {
        // to do something
    }
}
```

分析上面那种代码我们可以得出以下几点结论：

* 不管怎么看都是按流程或者条件设计的
* 可读性还行，但可维护性较差，二次修改错误率较高
* 无扩展性，只能不断增加代码的行数、条件分支以及更深层级的回调
* 如果功能升级增加类似延迟、轮询，那完全不支持
* 复用性可以说无

#### 解决方案

* 实现一个容器 `Element` 搭载所有外部实现逻辑
* 容器 `Element` 以单向链表的方式链接，执行完就自动执行下一个
* 容器内聚合一个抽象条件逻辑助手 `Promise`，可随意扩展增加行为，用来检查外部实现是否可以执行链表下一个 `Element`（可以形象理解为自来水管路的阀门，电路电气开关之类，当然会有更复杂的阀门与电气开关）
* 自己管理自己的生命周期，无需外部强引用
* 容器 `Element` 可以被继承实现，参考 `NSOperation` 设计

#### Example
```swift
private func head() -> PriorityElement<String, Int> {
    return PriorityElement(id: "Head") {  (promise: PriorityPromise<String, Int>) in
        Println("head input : \(promise.input ?? "")")
        self.delay(1) { promise.next(1) }
    }.subscribe { i in
        Println("head subscribe : \(i ?? -1)")
    }.catch { err in
        Println("head catch : \(String(describing: err))")
    }.dispose {
        Println("head dispose")
    }
}
// This is a minimalist way to create element, 
// using anonymous closure parameters and initializing default parameters
private func neck() -> PriorityElement<Int, String> {
    return PriorityElement {
        Println("neck input : \($0.input ?? -1)")
        $0.output = "I am Neck"
        $0.validated($0.input == 1)
    }.subscribe { ... }.catch { err in ... }.dispose { ... }
}
// This is a recommended way to create element, providing an ID for debugging
private func lung() -> PriorityElement<String, String> {
    return PriorityElement(id: "Lung") { 
        Println("lung input : \($0.input ?? "-1")")
        self.count += 1
        //
        $0.output = "I am Lung"
        $0.loop(validated: self.count >= 5, t: 1)
    }.subscribe { ... }.catch { err in ... }.dispose { ... }
}
private func heart() -> PriorityElement<String, String> {}
private func liver() -> PriorityElement<String, String> {}
private func over() -> PriorityElement<String, String> {}
// ... ...
let head: PriorityElement<String, Int> = self.head()
head.then(neck())
    .then(lung())
    .then(heart())
    .then(liver())
    .then(over())
// nil also default value()
head.execute()
```

也许大家看到这里闻到一股熟悉的 Goolge `Promises`、mxcl 的`PromiseKit` 或者 `RAC` 等味道，那么为啥不用那些个大神的框架来解决实际问题呢？

主要有一点：框架功能过于丰富而复杂，而我呢，弱水三千我只要一瓢，越轻越好的原则！哈哈

这里可以看到[详细的设计介绍](https://www.yuque.com/runscode/ios-thinking/priority_element "PrioritySessionElement设计与使用")，目前有 `OC、Swift、Java` 三个版本的具体实现。仓库地址：https://github.com/RunsCode/PromisePriorityChain 欢迎大家指正。

### 项目中区分 AppStore/Adhoc 包（二）

上期介绍了一种约定 `Configuration`，自定义预编译宏进行区分 AppStore/Adhoc 包的方法。后来尝试发现还可以通过应用内配置文件（embedded.mobileprovision）和 IAP 收据名区分包类型。

embedded.mobileprovison 仅在非 AppStore 环境存在，而且它里面还有一个参数 `aps-environment` 可以区分证书的类型是 `development` 还是 `production`，这两个值就对应了 Development 和 AdHoc 包。

另外 IAP 在非上架场景都是沙盒环境（上线 AppStoreConnect 的 TestFlight 包也是沙盒环境），是否为支付的沙盒环境我们可以用 `Bundle.main.appStoreReceiptURL?.lastPathComponent` 是否为 `sandboxReceipt` 进行判断。

所以使用上面两项内容我们可以区分：Development、AdHoc、TestFlight、AppStore。

#### 读取 embedded.mobileprovision

在命令行中我们可以利用 `security` 读取：

```bash
$ security cms -D -i embedded.mobileprovision
```

在开发阶段读取方式如下：

```swift
struct MobileProvision: Decodable {
    var name: String
    var appIDName: String
    var platform: [String]
    var isXcodeManaged: Bool? = false
    var creationDate: Date
    var expirationDate: Date
    var entitlements: Entitlements
    
    private enum CodingKeys : String, CodingKey {
        case name = "Name"
        case appIDName = "AppIDName"
        case platform = "Platform"
        case isXcodeManaged = "IsXcodeManaged"
        case creationDate = "CreationDate"
        case expirationDate = "ExpirationDate"
        case entitlements = "Entitlements"
    }
    
    // Sublevel: decode entitlements informations
    struct Entitlements: Decodable {
        let keychainAccessGroups: [String]
        let getTaskAllow: Bool
        let apsEnvironment: Environment
        
        private enum CodingKeys: String, CodingKey {
            case keychainAccessGroups = "keychain-access-groups"
            case getTaskAllow = "get-task-allow"
            case apsEnvironment = "aps-environment"
        }
        // Occasionally there will be a disable
        enum Environment: String, Decodable {
            case development, production, disabled
        }
    }
}

class AppEnv {
    
    enum AppCertEnv {
        case devolopment
        case adhoc
        case testflight
        case appstore
    }
    
    var isAppStoreReceiptSandbox: Bool {
        return Bundle.main.appStoreReceiptURL?.lastPathComponent == "sandboxReceipt"
    }
    
    var embeddedMobileProvisionFile: URL? {
        return Bundle.main.url(forResource: "embedded", withExtension: "mobileprovision")
    }
    
    var appCerEnv: AppCertEnv!
    
    init() {
      	// init or other time
        assemblyEnv()
    }
    
    func assemblyEnv() {
        if let provision = parseMobileProvision() {
            switch provision.entitlements.apsEnvironment {
            case .development, .disabled:
                appCerEnv = .devolopment
            case .production:
                appCerEnv = .adhoc
            }
        } else {
            if isAppStoreReceiptSandbox {
                appCerEnv = .testflight
            } else {
                appCerEnv = .appstore
            }
        }
    }
    
    /// ref://gist.github.com/perlmunger/8318538a02166ab4c275789a9feb8992
    func parseMobileProvision() -> MobileProvision? {
        guard let file = embeddedMobileProvisionFile,
              let string = try? String.init(contentsOf: file, encoding: .isoLatin1) else {
            return nil
        }
        
        // Extract the relevant part of the data string from the start of the opening plist tag to the ending one.
        let scanner = Scanner.init(string: string)
        guard scanner.scanUpTo("<plist", into: nil) != false  else {
            return nil
        }
        var extractedPlist: NSString?
        guard scanner.scanUpTo("</plist>", into: &extractedPlist) != false else {
            return nil
        }
        
        guard let plist = extractedPlist?.appending("</plist>").data(using: .isoLatin1) else { return nil}
        
        let decoder = PropertyListDecoder()
        do {
            let provision = try decoder.decode(MobileProvision.self, from: plist)
            return provision
        } catch let error {
            // TODO: log / handle error
            print(error.localizedDescription)
            return nil
        }
    }
}
```

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)

本期通过一个 demo 讲解 `isMemberOfClass:`、`isKindOfClass:` 两个方法的相关知识点。

**以下打印结果是什么？**（严谨点就添加个说明吧：Person 类继承于 NSObject 类）

```objectivec
BOOL res1 = [[NSObject class] isKindOfClass:[NSObject class]];
BOOL res2 = [[NSObject class] isMemberOfClass:[NSObject class]];
BOOL res3 = [[Person class] isKindOfClass:[Person class]];
BOOL res4 = [[Person class] isMemberOfClass:[Person class]];

NSLog(@"%d, %d, %d, %d", res1, res2, res3, res4);
```

打印结果：1, 0, 0, 0

**解释：**

以下是 objc4-723 中 `isMemberOfClass:`、`isKindOfClass:` 方法以及 `object_getClass()` 函数的实现。

```objectivec
+ (BOOL)isMemberOfClass:(Class)cls {
    return object_getClass((id)self) == cls;
}

- (BOOL)isMemberOfClass:(Class)cls {
    return [self class] == cls;
}

+ (BOOL)isKindOfClass:(Class)cls {
    for (Class tcls = object_getClass((id)self); tcls; tcls = tcls->superclass) {
        if (tcls == cls) return YES;
    }
    return NO;
}

- (BOOL)isKindOfClass:(Class)cls {
    for (Class tcls = [self class]; tcls; tcls = tcls->superclass) {
        if (tcls == cls) return YES;
    }
    return NO;
}

Class object_getClass(id obj)
{
    if (obj) return obj->getIsa();
    else return Nil;
}
```

emmm 整理的时候发现后面的版本又做了小优化，具体就不展开了，不过原理不变，以下是 824 版本的：

```objectivec
+ (BOOL)isMemberOfClass:(Class)cls {
    return self->ISA() == cls;
}

- (BOOL)isMemberOfClass:(Class)cls {
    return [self class] == cls;
}

+ (BOOL)isKindOfClass:(Class)cls {
    for (Class tcls = self->ISA(); tcls; tcls = tcls->getSuperclass()) {
        if (tcls == cls) return YES;
    }
    return NO;
}

- (BOOL)isKindOfClass:(Class)cls {
    for (Class tcls = [self class]; tcls; tcls = tcls->getSuperclass()) {
        if (tcls == cls) return YES;
    }
    return NO;
}
```

由此我们可以得出结论：

* `isMemberOfClass:` 方法是判断当前 `instance/class` 对象的 `isa` 指向是不是 `class/meta-class` 对象类型；
* `isKindOfClass:` 方法是判断当前 `instance/class` 对象的 `isa` 指向是不是 `class/meta-class` 对象或者它的子类类型。

显然 `isKindOfClass:` 的范围更大。如果方法调用者是 instance 对象，传参就应该是 class 对象。如果方法调用着是 class 对象，传参就应该是 meta-class 对象。所以 res2-res4 都为 0。那为什么 res1 为 1 呢？

因为 NSObject 的 class 的对象的 isa 指向它的 meta-class 对象，而它的 meta-class 的 superclass 指向它的 class 对象，所以 `[[NSObject class] isKindOfClass:[NSObject class]]` 成立 。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/objc-isa-class-diagram.jpg)

总之，`[instance/class isKindOfClass:[NSObject class]]` 恒成立。（严谨点，需要是 NSObject 及其子类类型）


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`Swift 指针`、`Swift 属性包裹器`

1、[Swift 中的指针使用]( https://onevcat.com/2015/01/swift-pointer/  "Swift 中的指针使用") -- 来自：onevcat

Swift 中指针使用场景并不常见，但是有些时候我们又不得不尝试去使用指针，因此还是需要对 Swift 的指针运用有一定的了解。这篇文章是喵神 15 年写的，并在 2020 年做了更新。文章对 C 指针和 Swift 的指针应用做了映射，对于有一定 C 指针基础的同学阅读比较友好。

2、[The 5-Minute Guide to C Pointers](https://denniskubes.com/2017/01/24/the-5-minute-guide-to-c-pointers/ "C语言指针5分钟教程") -- 来自：Dennis Kubes

喵神文章中推荐的 C 语言指针教程，如果对 C 指针不了解的话，直接切入到 Swift 的指针还是有一定的困难的。

3、[Swift5.1 - 指针Pointer](https://www.jianshu.com/p/8cff1ef20e8c "Swift5.1 - 指针Pointer") -- 来自简书：HChase

这篇文章根据 Swift 的类型给出了多种使用方法，查找用法非常方便。例如 malloc 之后如何填充字节、如何根据地址创建指针、如何进行类型转换等。如果在开发中需要使用 Swift 的指针，在不熟悉的情况下可以参考文中的小 demo。

4、[使用 Property Wrapper 为 Codable 解码设定默认值](https://onevcat.com/2020/11/codable-default/ "使用 Property Wrapper 为 Codable 解码设定默认值
") -- 来自：onevcat

在 Swift 中，json 转 model 可以使用 Codable，但因为其无法指定可选值的默认属性，在开发的过程中需要更冗余的代码进行解可选操作；onevcat 的这篇文章就利用 Property Wrapper 为 Codable 解码设定了默认值。此外我将其总结成了一个文件 [SSCodableDefault.swift](https://github.com/Tliens/SpeedySwift/blob/master/Example/SpeedySwift/SSCodableDefault.swift)，欢迎大家使用。

5、[What is a Property Wrapper in Swift](https://sarunw.com/posts/what-is-property-wrappers-in-swift/#custom-logic-over-swift-properties "What is a Property Wrapper in Swift") -- 来自：sarunw

属性包装器是一种包装属性以添加额外逻辑的新类型。作者先抛出问题，分析属性包装器出现之前如何对属性进行包装以及他遇到的问题，然后来利用属性包装器对属性进行逻辑包装，比较了二种方式的区别，简述了属性包装器的好处。

6、[Swift 5 属性包装器Property Wrappers完整指南](https://juejin.cn/post/6844904018121064456 "Swift 5 属性包装器Property Wrappers完整指南") -- 来自掘金：乐Coding

本文是使用属性包装器的一篇中文教程、可以结合 4、5 阅读。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Machine Learning Crash Course from Google

地址：https://developers.google.com/machine-learning/crash-course

来自 Google 的机器学习教程资料，以 TensorFlow APIs 为基础，进行包括视频教学、真实的案例探究和动手实践练习。由于是谷歌支持的项目，你也可以在通过学习之后，去 Kaggle 竞赛获得真实竞赛经验，或者访问 [Learn with Google AI](https://ai.google/education)，探索更完整的培训资源库。

### ML-For-Beginners from Microsoft

地址：https://github.com/microsoft/ML-For-Beginners

来自 Microsoft 的机器学习教程资料。提供了一个为期 12 周、有 24 个课时的关于机器学习的课程。在这个课程中，你将学习经典的机器学习，主要使用 Scikit-learn 作为一个库来接触机器学习。这在我们即将推出的「AI初学者」课程中有所涉及。这些课程也可以与我们即将推出的「数据科学初学者」课程搭配使用。我们将这些经典技术应用于世界上许多地区的一些数据，请与我们一起到世界各地旅行，来边学习边旅行！在 Microsoft 的仓库中你也可以找到其他所有课程。

### turicreate from Apple

地址：https://apple.github.io/turicreate/docs/userguide/

来自 Apple 的 [turicreate](https://github.com/apple/turicreate) 样例模型以及简化模型程序，他并不是学习机器学习的教程，而是给你提供解决任务的方案。你可以使用 turicreate 来训练推荐算法、对象检测、图像分类、图像相似性或活动分类等简单的机器学习模型。通过产生的 `.mlmodel` 模型，可以直接放到工程中使用 Core ML 来轻松使用。

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

### explainshell

**地址**：https://explainshell.com/

这个网站跟上期介绍的 [regex101](https://regex101.com) 很类似，一个用于解析正则表达式，一个用于解析 shell 指令。不常接触 shell 的小伙伴对于一个参数巨多，又巨长的指令可能会手足无措，没关系，这个网站来帮你😏。它会把主要命令和各个参数，传值进行详细的拆分讲解。比如这句列出所有包含 `1a1b1c` 这一 commit 的分支：

```bash
git branch -a -v --no-abbrev --contains 1a1b1c
```

解析结果：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210814184638.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第二十二期](https://mp.weixin.qq.com/s/JI5mlzX9cYhXJS81k1WE6A)

[iOS摸鱼周报 第二十一期](https://mp.weixin.qq.com/s/Hcd8CtkyqD8IXM0SbVJo-A)

[iOS摸鱼周报 第二十期](https://mp.weixin.qq.com/s/PjiZzx3VSAfAGHRJs160aQ)

[iOS摸鱼周报 第十九期](https://mp.weixin.qq.com/s/dtyozlqCO7PcpyGhx2qB5g)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
