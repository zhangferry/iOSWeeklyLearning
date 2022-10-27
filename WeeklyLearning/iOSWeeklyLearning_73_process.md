# iOS 摸鱼周报 #73 | 待定

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：Swift 函数派发方式总结
> * 内容推荐：网络监控内容推荐，iOS 博主在新西兰找工作的心路历程
> * 摸一下鱼：多种脚本语言中优雅处理参数的三方库

## 本期话题



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

[@夏天](https://juejin.cn/user/3298190611456638): 这是一篇关于如果通过`NWPathMonitor`来实现 `iOS 12` 以上实现网络可达性判断的文章，文章介绍了 `NWPathMonitor` 的优点以及在后面断网时的不足，并且介绍了一个兼容的库 [Connectivity](https://github.com/rwbutler/Connectivity)，但是该库由于使用了 `Combine` 并不兼容 iOS 13 以下了。

3、[我是如何在新西兰找到iOS开发工作的？](https://www.youtube.com/channel/UCiEbxa6e5o3mtBJIwhRxbHA?sub_confirmation=1 "我是如何在新西兰找到iOS开发工作的？")-- 陈宜龙(@iOS程序犭袁)

[@夏天](https://juejin.cn/user/3298190611456638):  陈宜龙大佬是我学习 iOS 比较追寻的一个博主了，最近他润去了新西兰，可以查看他的其他的  `YouTube`  视频。


## 摸一下鱼

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

最近在写脚本，这期介绍几个帮助脚本语言接收参数更优雅的三方库；

- shell: [getoptions](https://github.com/ko1nksm/getoptions "getoptions")
- python: [python-fire](https://github.com/google/python-fire "python-fire")
- js：[commander.js](https://github.com/tj/commander.js "commander.js")
- ruby：[commander](https://github.com/commander-rb/commander "commander")


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #72 | 1024 开始预热](https://mp.weixin.qq.com/s/WUVAHbJe_dmA-DVFXpF2Qw)

[iOS 摸鱼周报 #71 | iOS / One More Thing?](https://mp.weixin.qq.com/s/0mAKYvVuPLKEA2qnsNfCvQ)

[iOS 摸鱼周报 #70 | iOS / iPadOS 16.1 公测版 Beta 3 发布，支持老款 iPad 台前调度](https://mp.weixin.qq.com/s/rSPC8lgvUKPKfgR53xdHqg)

[iOS 摸鱼周报 #69| 准备登陆灵动岛](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
