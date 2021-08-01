# iOS摸鱼周报 第二十一期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> 本期话题讲了一些身体的特殊机制，希望大家看完能少熬夜。
>
> 开发 Tips 本期讲的是 `UserDefaults` 的一些用法。
>
> 面试解析本期讲解 load 和 initialize 的一些知识点。
>
> 博客内容推荐了几篇不同方式的内存优化文章。
>
> Open Source Society University：非常受欢迎的计算机科学自学教程，Swift Programming for macOS：用 Swift 开发 Mac 应用的一些示例介绍。
>
> Messier：一个 Objective-C 方法耗时监控的方案。

## 本期话题

[@zhangferry](https://zhangferry.com)：今天看到一个视频，来自北医三院的薄世宁医生，他是危重医学科副主任医师，讲人在危重的时候，身体会有什么反应。当时看完还是比较震撼的，这里转成如下文字：

> 我们经常被教育在危难的时候要努力，但你可能完全不知道你身体里面的细胞比你还努力。人在大出血的时候血压会迅速下降，这么做的目的是为了减缓出血的速度，而且肾脏会没有尿，是为了把有限的血流供应给更关键的大脑和心脏。
>
> 我们每天，人体会有 3300 亿个细胞死亡，同时会新生出 3300 亿个新生的细胞。孕妇在即将生产的前几天，血液当中有一个凝血指标会升高几十倍，这么做的目的是为了防止生产过程有可能发生的大出血。你肯定还会想不到，心脏每一次收缩跳动，它的电活动是要从窦房结，到房室结，然后还要传导到心脏。当危难病重的时候，窦房结失败了，不能跳动了房室结开始替它跳，房室结也不能够传导的时候，心脏、心室开始自主逸博跳动。这个时候的跳动，心电图已经面目全非，人的血流也会非常微弱，但是即便是这么微弱的血流，也保证了大脑和心脏自身的供血，等着援兵的到来。你看，在危机时刻，所有这些细胞都在为你拼命，拼命到生命的最后一刻。
>
> 讲这么多其实就是要告诉你，你还有什么资格熬夜抽烟喝酒，虐待你身体里这些组织和细胞呢。在困难面前，你还有什么资格轻言放弃呢。

## 开发Tips
### 关于 `UserDefaults` 你应该这么用
整理编辑：[CoderStar](https://juejin.cn/user/588993964541288)
#### 构造器的选用
`UserDefaults` 生成对象实例大概有以下三种方式：

```swift
open class var standard: UserDefaults { get }

public convenience init()

@available(iOS 7.0, *)
public init?(suiteName suitename: String?)
```

平时大家经常使用的应该是第一种方式，第二种方式和第一种方式产生的结果是一样的，实际上操作的都是 **APP 沙箱中 `Library/Preferences` 目录下的以 `bundle id` 命名的 `plist` 文件**，只不过第一种方式获取到的是一个单例对象，而第二种方式每次获取到都是新的对象，从内存优化来看，很明显是第一种方式比较合适，其可以避免对象的生成和销毁。

如果一个 APP 使用了一些 SDK，这些 SDK 或多或少的会使用 `UserDefaults` 来存储信息，如果都使用前两种方式，这样就会带来一系列问题：

- 各个 SDK 需要保证设置数据 KEY 的唯一性，以防止存取冲突；
- `plist` 文件越来越大造成的读写效率问题；
- 无法便捷的清除由某一个 SDK 创建的 `UserDefaults` 数据；

针对上述问题，我们可以使用第三种方式。

第三种方式根据传入的 `suiteName` 的不同会产生四种情况：

- 传入 `nil`：跟使用 `UserDefaults.standard` 效果相同；
- 传入 `bundle id`：无效，返回 nil；
- 传入 `App Groups` 配置中 `Group ID`：会操作 APP 的共享目录中创建的以 `Group ID` 命名的 `plist` 文件，方便宿主应用与扩展应用之间共享数据；
- 传入其他值：操作的是沙箱中 `Library/Preferences` 目录下以 `suiteName` 命名的 `plist` 文件。

#### `UserDefaults` 的统一管理
经常会在一些项目中看到 `UserDefaults` 的数据存、取操作，`key` 直接用的字符串魔法变量，搞到最后都不知道项目中 `UserDefaults` 到底用了哪些 key，对 key 的管理没有很好的重视起来。下面介绍两种 `UserDefaults` 使用管理的方式，一种是通过 `protocol` 及其默认实现的方式，另一种是通过 `@propertyWrapper` 的方式，因第一种方式涉及代码比较多，不便在周报中展示，这里就只介绍第二种方式。

Swift 5.1 推出了为 SwiftUI 量身定做的 `@propertyWrapper` 关键字，翻译过来就是 `属性包装器`，有点类似 java 中的元注解，它的推出其实可以简化很多属性的存储操作，使用场景比较丰富，用来管理 `UserDefaults` 只是其使用场景中的一种而已。

先上代码，相关说明请看代码注释。

```swift
@propertyWrapper
public struct UserDefaultWrapper<T> {
    let key: String
    let defaultValue: T
    let userDefaults: UserDefaults

    /// 构造函数
    /// - Parameters:
    ///   - key: 存储 key 值
    ///   - defaultValue: 当存储值不存在时返回的默认值
    public init(_ key: String, defaultValue: T, userDefaults: UserDefaults = UserDefaults.standard) {
        self.key = key
        self.defaultValue = defaultValue
        self.userDefaults = userDefaults
    }

    /// wrappedValue 是 @propertyWrapper 必须需要实现的属性
    /// 当操作我们要包裹的属性时，其具体的 set、get 方法实际上走的都是 wrappedValue 的 get、set 方法
    public var wrappedValue: T {
        get {
            return userDefaults.object(forKey: key) as? T ?? defaultValue
        }
        set {
            userDefaults.setValue(newValue, forKey: key)
        }
    }
}

// MARK: - 使用示例

enum UserDefaultsConfig {
    /// 是否显示指引
    @UserDefaultWrapper("hadShownGuideView", defaultValue: false)
    static var hadShownGuideView: Bool

    /// 用户名称
    @UserDefaultWrapper("username", defaultValue: "")
    static var username: String

    /// 保存用户年龄
    @UserDefaultWrapper("age", defaultValue: nil)
    static var age: Int?
}

func test() {
  /// 存
  UserDefaultsConfig.hadShownGuideView = true
  /// 取
  let hadShownGuideView = UserDefaultsConfig.hadShownGuideView
}
```
`UserDefaults` 的一些相关问题以及第一种利用 `protocol` 及其默认实现的管理方式的详细描述可以前往 [UserDefaults 浅析及其使用管理](https://mp.weixin.qq.com/s/Xlph6pkR8ZV02D7VYVWlOw)查看。

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)

本期讲解 load 和 initialize 的相关知识点。

### load 和 initialize 的区别

区别|load|initialize
--|--|--
调用时刻|在 `Runtime` 加载类、分类时调用<br>（不管有没有用到这些类，在程序运行起来的时候都会加载进内存，并调用 `load` 方法）。<br><br>每个类、分类的 `load`，在程序运行过程中只调用一次（除非开发者手动调用）。|在`类`第一次接收到消息时调用。<br><br>如果子类没有实现 `initialize` 方法，会调用父类的 `initialize`，所以父类的 `initialize` 方法可能会被调用多次，但不代表父类初始化多次，每个类只会初始化一次。
调用方式|① 系统自动调用 `load` 方式为直接通过函数地址调用；<br>② 开发者手动调用 `load` 方式为消息机制 `objc_msgSend` 函数调用。|消息机制 `objc_msgSend` 函数调用。
调用顺序|① 先调用类的 `load`，按照编译先后顺序调用（先编译，先调用），调用子类的 `load` 之前会先调用父类的 `load`；<br>② 再调用分类的 `load`，按照编译先后顺序调用（先编译，先调用）（注意：通过消息机制调用分类方法是：后编译，优先调用）。|① 先调用父类的 `initialize`<br>② 再调用子类的 `initialize`<br>（先初识化父类，再初始化子类）。

### 手动调用子类的 load 方法，但是子类没有实现该方法，会怎样？

* `load` 方法可以继承，手动调用 `load` 的方式为是通过消息机制调用，先查找子类是否实现了 `load` 方法，由于子类没有实现，就会去查找父类，如果父类实现了 `load` 方法则调用，否则继续逐级查找；
* 如果父类的分类实现了 `load` 方法，那么会调用分类的，因为分类方法会“覆盖”同名宿主类方法；
* 如果存在多个父类的分类都实现了 `load` 方法的话，那么会调用最后参与编译的分类的 `load` 方法。


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

内存优化可以从以下几点入手：

* 工具分析，可以利用 Xcode 自带的 Instruments 中的 leak、allocation，也可以利用 MLeaksFinder 等开源工具。找到内存泄漏、内存激增、内存不释放的位置。
* 利用 mmap，一种低内存的首选方案。
* 图片优化，经过第一步之后，一定会发现内存激增极有可能与图片相关。

1、[iOS的文件内存映射——mmap](https://www.jianshu.com/p/516e7ff6f251 "iOS的文件内存映射——mmap") -- 来自简书：落影loyinglin

mmap 一定是低内存方案的首选。文件映射，用于将文件或设备映射到虚拟地址空间中，以使用户可以像操作内存地址一样操作文件或设备，作者介绍了 mmap 原理并根据官方代码，整理了一个简单的 Demo，有兴趣的人还可以阅读下微信的开源仓库：MMKV。

2、[iOS图片加载速度极限优化—FastImageCache解析](http://blog.cnbang.net/tech/2578/ "iOS图片加载速度极限优化—FastImageCache解析") -- 来自博客：bang

在 app 中，图片在内存中占用比例相对较大，有没有办法优化缓存一些图片到磁盘中呢？答案是：FastImageCache。FastImageCache 是 Path 团队开发的一个开源库，用于提升图片的加载和渲染速度，让基于图片的列表滑动起来更顺畅，来看看它是怎么做的。

3、[Instruments学习之Allocations](https://www.jianshu.com/p/b617f16acb7f "Instruments学习之Allocations") -- 来自简书：Thebloodelves

详细介绍 Allocations 的使用，为你分析 app 内存助力。

4、[【基本功】深入剖析Swift性能优化](https://tech.meituan.com/2018/11/01/swift-compile-performance-optimization.html "[基本功]深入剖析Swift性能优化") -- 来自美团技术团队：亚男


Swift 已经是大势所趋，各个大厂都已经在做尝试和推广，所以内存优化也离不开 Swift。本文前半部分介绍了 Swift 的数据类型的内存分配情况，先了解 Swift 的内存基本原理才能在日常开发中提前避免问题的发生。

5、[Swift内存泄漏详解([weak self]使用场景)](https://www.jianshu.com/p/cb45b5e016ff "Swift内存泄漏详解([weak self]使用场景") -- 来自简书：码农淏


本文通过代码的方式列举了 Swift 中造成内存泄漏的一些情况，比较适合 Swift 的初学者，文章较短但是比较实用。OC 转 Swift 的同学可以关注下。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Open Source Society University

地址：https://github.com/ossu/computer-science

这是在 Github 有 92.7k Stars 的计算机科学自学教程。它是根据计算机科学专业本科生的学位要求设计的。这些课程本身是世界上最好的课程之一，通常来自哈佛、普林斯顿、麻省理工学院等。该课程不仅仅是为了职业培训或专业发展，它是为那些希望在所有计算机学科的基本概念方面有一个适当的、全面的基础的人而设的，也是为那些有纪律、意志和（最重要的是！）良好习惯的人而设的，可以使他们通过这种方式靠自己来获得这些知识。

### Swift Programming for macOS

地址：https://gavinw.me/swift-macos/

尽管 iPhone 和 iPad 的 App 都需要 Mac 来进行代码开发，但关于实际创建原生 Mac App 的相关资料在网上很少见到。这个网站囊括了最新版本使用 Swift 和 SwiftUI 来开发 Mac App 的一些简单例子，给想要学习 Mac 开发的开发者提供一个小型的资源库。

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

### Messier

**地址**：https://messier-app.github.io/

**软件状态**：免费

**软件介绍**：

Messier 是基于 AppleTrace 开发的 Objective-C 方法耗时测量应用，其相对于 AppleTrace 更易用，且能更方便的在越狱设备上 Trace 任意应用。它由三部分组成：Tweak 插件，动态库（Messier.framework），桌面端应用。非越狱场景，我们使用后两个部分可完成对自己应用的耗时监控，输出为 json 文件，再使用 `chrome://tracing` 将 json 文件绘制为火焰图，效果如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/messier-content.gif)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第二十期](https://mp.weixin.qq.com/s/PjiZzx3VSAfAGHRJs160aQ)

[iOS摸鱼周报 第十九期](https://mp.weixin.qq.com/s/dtyozlqCO7PcpyGhx2qB5g)

[iOS摸鱼周报 第十八期](https://mp.weixin.qq.com/s/JsGmu7pzYLI3Svrmk5i2cA)

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
