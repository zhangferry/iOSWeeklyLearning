# iOS 摸鱼周报 #64 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：今年 8 月，把握与 App Store 专家会面交流的机会
> * 本周学习：Swift 闭包中的变量捕获
> * 内容推荐：程序开发文档及资源网站
> * 摸一下鱼：

## 本期话题

### 今年 8 月，把握与 App Store 专家会面交流的机会

[@师大小海腾](https://juejin.cn/user/782508012091645/posts)：想让你的产品页更加出色？对 TestFlight 或实施订阅有疑问？与 App Store 专家交流探讨，了解如何充分利用这些功能。探索如何吸引新顾客、测试营销策略、添加订阅等等。在整个 8 月，Apple 将在多个时区以多种语言进行实时演讲和答疑。如果你是 Apple Developer Program 的成员，现在即可注册申请。

![](https://cdn.zhangferry.com/Images/20220811001526.png)

![](https://cdn.zhangferry.com/Images/20220811001546.png)

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Swift 闭包中的变量捕获

熟悉 OC 的读者都了解，OC 中 `Block`变量捕获根据变量的类型不同和修饰符的不同，有引用和拷贝两种方式。然而这套逻辑直接套用到 Swift 的闭包捕获中是不成立的。Swift 捕获方式有两种：捕获列表、隐式捕获。

#### 隐式捕获

隐式捕获即直接引用变量，这种方式是对变量指针的捕获，使其引用计数增加，在闭包作用域期间指针不会被释放。这类似于 `Block `中对引用类型变量的捕获。区别在于 Swift 中即使是值类型的变量，捕获的也是该变量的指针而非值的拷贝，即闭包中执行时是变量改变后的新值。

```swift
var value = 10
    delay(seconds: 1) {
        print("value : \(value)")
    }
    value = 20

// 打印结果为 value: 20
```

简单理解就是，直接捕获捕获到的是变量指针，无论该指针指向的是引用类型变量，还是值类型变量，都是在闭包执行时再通过指针去获取最终的值。所以在闭包执行之前改变变量值都会生效。

#### 捕获列表

捕获列表又称为显式捕获，这种方式是对变量指针指向的值进行捕获。形式上表现出的特征是在闭包创建时就立即捕获指针的值，后续即使改变指针的指向，也不会影响闭包内的值 **注意这里改变的是指针指向，而非指针指向的值更新**。

```swift
var value = 10
    delay(seconds: 1) { [vle = value] in
        print("value : \(vle)")
    }

    value = 20

// 打印结果为 value: 10
```

**需要注意的是：当使用捕获列表时，针对变量是引用类型还是值类型，结果是不一样的，会涉及到拷贝还是引用，这里是和直接捕获有所差异的地方。**

```swift
var per = PersonClosure(name: "哈哈", age: 10)
    
    delay(seconds: 1) { [per = per] in
        print("name: \(per.name) age: \(per.age)")
    }

    per.name = "xxi"
```

当 `PersonClosure` 是值类型，则改变 `per.name`的值不会影响闭包创建时捕获到的值。原因是值类型创建时是拷贝方式捕获的。后续改变不影响拷贝的值。

当 `PersonClosure`是引用类型，则闭包创建时对该 `PersonClosure`对象只是引用计数增加，`per.name` 会改变闭包执行时的值。 但是如果是 `per = PersonClosure(name: "xxi", age: 10)` 改变指针指向，则不会改变闭包内的捕获的变量值。（这里就是上文所提到的：改变指针指向不会影响值，而改变指针指向的值更新会影响闭包执行）

#### 弱引用捕获

弱引用捕获是捕获列表的一种特殊情况，不会导致引用计数的增加。由于变量类型是值类型时，捕获列表是直接拷贝，所以无法针对值类型的捕获列表使用弱引用。

弱引用捕获用来处理闭包的循环引用，类似 OC 中的 weak 修饰符的作用。

最后以一道测试题，来测试下是否理解了闭包的捕获方式：

```swift
class Pokemon: CustomDebugStringConvertible {
  let name: String
  init(name: String) {
    self.name = name
  }
  var debugDescription: String { return "<Pokemon \(name)>" }
  deinit { print("\(self) escaped!") }
}

func delay(seconds: Int, closure: @escaping ()->()) {
  let time = DispatchTime.now() + .seconds(seconds)
    DispatchQueue.main.asyncAfter(deadline: time, execute: DispatchWorkItem(block: {
        print("🕑")
        closure()
    }))
}

func demo7() {
  var pokemon = Pokemon(name: "Mew")
  print("➡️ Initial pokemon is \(pokemon)")
  delay(1) { [capturedPokemon = pokemon] in
    print("closure 1 — pokemon captured at creation time: \(capturedPokemon)")
    print("closure 1 — variable evaluated at execution time: \(pokemon)")
    pokemon = Pokemon(name: "Pikachu")
    print("closure 1 - pokemon has been now set to \(pokemon)")
  }
  pokemon = Pokemon(name: "Mewtwo")
  print("🔄 pokemon changed to \(pokemon)")
  delay(2) { [capturedPokemon = pokemon] in
    print("closure 2 — pokemon captured at creation time: \(capturedPokemon)")
    print("closure 2 — variable evaluated at execution time: \(pokemon)")
    pokemon = Pokemon(name: "Charizard")
    print("closure 2 - value has been now set to \(pokemon)")
  }
}

输出结果为：
➡️ Initial pokemon is <Pokemon Mew>
🔄 pokemon changed to <Pokemon Mewtwo>
🕑
closure 1 — pokemon captured at creation time: <Pokemon Mew>
closure 1 — variable evaluated at execution time: <Pokemon Mewtwo>
closure 1 - pokemon has been now set to <Pokemon Pikachu>
<Pokemon Mew> escaped!
🕑
closure 2 — pokemon captured at creation time: <Pokemon Mewtwo>
closure 2 — variable evaluated at execution time: <Pokemon Pikachu>
<Pokemon Pikachu> escaped!
closure 2 - value has been now set to <Pokemon Charizard>
<Pokemon Mewtwo> escaped!
<Pokemon Charizard> escaped!
```

- [Closures Capture Semantics: Catch them all!](https://alisoftware.github.io/swift/closures/2016/07/25/closure-capture-1/ "Closures Capture Semantics: Catch them all!")

## 内容推荐

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1、[Xamarin 文档](https://docs.microsoft.com/zh-cn/xamarin/ "Xamarin 文档") -- 来自：Microsoft

[@夏天](https://juejin.cn/user/3298190611456638)：除了常见的 React Native、Flutter、Weex 之外，在跨平台上还有一些值得尝试的跨平台方案，比如来自 Microsoft 的 Xamarin 就允许你使用 .NET 代码和特定于平台的用户界面生成适用于 Android、iOS 和 macOS 的本机应用。也许，这不失为一个新的全栈选择。

2、[Qt](https://www.qt.io/ "Qt") -- 来自：*Qt* Company 

[@夏天](https://juejin.cn/user/3298190611456638)：除了上文的 C# 之外，由 *Qt* Company 开发的跨平台 C++ 图形用户界面应用程序开发框架。C ++ 拥有卓越的性能，那么用它开发出来的桌面或移动端应用是否能够在编写之初就能够凌驾在其他应用之上呢？当然其涵盖的点还包括嵌入式及微控制器（MCU），一次学习，干啥都行。除了付费以外，似乎没啥缺点。

3、[Geeks for Geeks](https://practice.geeksforgeeks.org/home "Geeks for Geeks") -- 来自：GeeksforGeeks

[@夏天](https://juejin.cn/user/3298190611456638)：一个对开发者来说很全面的网站，提供了算法，系统设计等基础内容。还提供了 [Practice](https://practice.geeksforgeeks.org/explore?page=1&curated[]=1&sortBy=submissions&curated_names[]=SDE%20Sheet) 和一些付费/免费的课程及文章。你也可以订阅他们的 [YouTube 账号](https://www.youtube.com/geeksforgeeksvideos) 观看视频课程，教程中的 CS Subject 适合大量入门或者基础不扎实的程序员。不过语言教学没有 Swift...

4、[iOS Conf SG](https://iosconf.sg/ "iOS Conf SG") -- 来自：iOS Conf SG

[@夏天](https://juejin.cn/user/3298190611456638)：号称东南亚最大的 iOS 开发者大会。从 2016 年举办至今已有 6 年，一个纯为 iOS 开发者举办的开发者大会。每年大概有 15 个左右的视频来讲述一些 iOS 相关的视频，你可以在 [YouTube ](https://www.youtube.com/c/iOSConfSG) 进行观看。

## 摸一下鱼

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #63 | Apple 企业家培训营已开放申请](https://mp.weixin.qq.com/s/nAMshUG4AjWLAAHOFPVqXg)

[iOS 摸鱼周报 #62 |  Live Activity 上线 Beta 版 ](https://mp.weixin.qq.com/s/HySX4Yaf3Zxy8Wn-LyUO0A)

[iOS 摸鱼周报 #61 |  Developer 设计开发加速器](https://mp.weixin.qq.com/s/WfwqRhC-9-isUanv8ZnvMQ)

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
