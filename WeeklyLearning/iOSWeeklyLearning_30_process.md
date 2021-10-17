# iOS摸鱼周报 第三十期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：
> * Tips：
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)



## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

1、[或许你并不需要重写 init(from:) 方法](https://kemchenj.github.io/2018-07-09/ "或许你并不需要重写 init(from:) 方法") -- 来自：kemchenj

[@东坡肘子](https://www.fatbobman.com)：Codable 作为 Swift 的特性之一也是很注重安全，也很严谨，这就导致了它在实际使用时总会有这样那样的磕磕绊绊，我们不得不重写 init 方法去让它跟外部环境融洽地共存。本文介绍了一种通过重载decodeIfPresent方法以实现应对特殊类型的思路。从某种程度上来说，作者认为这甚至是比 Objective-C 的消息机制更加灵活的一种函数声明机制，而且它的影响范围是有限的，不容易对外部模块造成破坏（别声明为 open 或者 public 就没问题）。

2、[使用 Property Wrapper 为 Codable 解码设定默认值](https://onevcat.com/2020/11/codable-default/ "使用 Property Wrapper 为 Codable 解码设定默认值") -- 来自：onevcat

[@东坡肘子](https://www.fatbobman.com)：本文介绍了一个使用 Swift Codable 解码时难以设置默认值问题，并利用 Property Wrapper 给出了一种相对优雅的解决方式，来在 key 不存在时或者解码失败时，为某个属性设置默认值。这为编解码系统提供了更好的稳定性和可扩展性。最后，对 enum 类型在某些情况下是否胜任进行了简单讨论。

3、[2021 年了，Swift 的 JSON-Model 转换还能有什么新花样](https://zhuanlan.zhihu.com/p/351928579?ivk_sa=1024320u "2021 年了，Swift 的 JSON-Model 转换还能有什么新花样") -- 来自知乎：非著名程序员，作者明林清

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7):本文主要介绍ExCodable的特性和使用方法。在文章开头先介绍了常见的json转模型的几种方式，并这些方式各自的优缺点进行了总结，随后引出ExCodable的特性及使用方法。

4、[json 解析有什么可说道的](https://mp.weixin.qq.com/s/_jFHgAP0vKx1Cv9XGkh_DA "json 解析有什么可说道的") -- 来自公众号：码农哈皮

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7):文章开头先介绍了什么是json。正文主要篇幅在介绍SwiftyJSON和YYModel的实现方案。文章最后引出了HandyJSON，HandyJSON是基于借助metadata结构来实现json 转 model的。在这里额外提一句，如何推断metadata的结构，可以参考[GenMeta.cpp ](https://github.com/apple/swift/blob/main/lib/IRGen/GenMeta.cpp "GenMeta.cpp ")中每个结构的layout 函数

5、[Swift中Json转Model的便捷方式](https://juejin.cn/post/7019910939340193805/ "Swift中Json转Model的便捷方式") -- 来自掘金：我是熊大

[@我是熊大](https://github.com/Tliens):本文介绍json、model、data、dict相互转换的小技巧和代码段，适合在实际工作中使用。

6、[Swift 码了个 JSON 解析器(一)](https://zhuanlan.zhihu.com/p/364032254 "Swift 码了个 JSON 解析器(一)") -- 来自知乎：OldBirds

[@我是熊大](https://github.com/Tliens):正如作者所言，码了个 JSON 解析器,感兴趣的可以看一下。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### wakapi

**地址**：https://wakapi.dev/

**软件状态**：免费

**软件介绍**：

Keep Track of Your Coding Time!
Wakapi is an open-source tool that helps you keep track of the time you have spent coding on different projects in different programming languages and more. Ideal for statistics freaks and anyone else.

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/screenshot.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
