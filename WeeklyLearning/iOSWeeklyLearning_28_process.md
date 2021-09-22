# iOS摸鱼周报 第二十七期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：跟彭飞聊一下职业选择和如何提高学习兴趣。
> * Tips：
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：彭飞是群里非常活跃也很有趣的一位小伙伴，工作时间还不是太长但学习热情很高，一起来了解下他是如何看待学习这件事的。

zhangferry：简单介绍下自己吧。

> 大家好，我就是我们成长之路群里自诩瓜皮的同学，为什么我自诩瓜皮呢，因为我 19 年毕业，就工作经验而言对于很多前辈而言还是稚嫩了些。刚毕业时去了一个 P2P 背景的公司，后来 P2P 在疫情前没几个月就倒了，急于找到一份工作，去了一家传统行业做开发，然后今年跳槽去了家互联网股票头部公司。

zhangferry：你之前在传统企业也工作过，传统企业跟互联网公司工作的感受有什么不同。

> 就拿我之前的公司而言，最大的不同就是对开发过程的重视，对技术的重视程度不同。
>
> 虽然我之前带的传统行业，就这家公司而言，员工也是不少，但是对于开发部门来说，完全就是个小作坊。没有合理的生产流程，只注重生产出产品（其实也不是很注重）。一个人负责的东西很杂，测试离职后就只能自测，甚至有一个星期被迫下店当了店员（一生黑）。其实我之前早就想要离开那里，可是碍于疫情只能多留了一年。
>
> 现在在这家公司，最大的感受就是流程规范了许多，公司重视技术，有定期的技术分享，生产流程也规范了许多，也有内部的自动化平台，目前也有机会参与公司的自动化流程构建优化（脚本自动化打包等），感觉在这里可以接触到学习到很多东西。

zhangferry：感觉你兴趣范围挺广的，逆向、算法，这些由兴趣推动的技术方向，你是如何保热情持持续不断的学习的呢？

> 也可以说是一种有目标，也是为了成功的成就感。
>
>在我看清了前司要离开却迫于疫情留下后，我就知道要为以后做打算了，我于是每天开始刷算法题，每个模块有目的性的做下来，然后参照题解，分析自己的时空复杂度是否有优化空间。在换工作前做了300余道算法题，刷算法的同时感受到了算法思维的重要性。
>
>逆向的学习也是机缘巧合，当时我的好基友有一款付费办公软件找我，希望我能破解。当时我就决定去学习这部分的知识。学了一段时间，也买了 Hopper 作为分析工具，帮基友破解掉了里面的内购付费功能。为了简化部分重复的工作，抽了一段时间学习写 Shell 脚本（也稍微了解了 Python，以后会详细学习），然后自写了一套重签名脚本。软件破解成功以后我真的是满满的成就感。

zhangferry：有了学习动力还需要一些学习方法，分享一些你的学习方法吧。

> 我认为最重要的是要有目的性，当初我决定要跳槽后，基本上能抽的空闲时间都抽出来了，地铁上刷MJ的视频，回去以后打开 Leetcode 刷题，每天制定学习的时长，时间不到不能进行娱乐活动。然后只玩休闲类益智类游戏，保证不会在游戏上花掉太多时间。像现在的话，我虽然已经没有跳槽的目的性，不过最近 *OS internals part3 译本已经出来了，我也购入了一本，当前目标就是先读完这本书。虽然里面也很多陌生的概念，也磕磕绊绊的看了一百余页。所以对我而言，目的性是我学习的最大动力。

zhangferry：说一下最近的思想感悟吧。

> 主要就是想以我自己的经历，向跟我差不多年龄的同学分享下，一定做好职业规划。之前我去那传统公司也是看人比较多，结果却大失所望，走了不少弯路。但是也是因为在那个公司，我才明白了只有提升自己才能进入好企业来摆脱它。
>
> 之前看群里的同学们，有分享过一些开发者视频（油管上的），都是英文的。感觉虽然工作了，英语也是相当重要，建议英文基础薄弱些的同学还是花些精力在这里，毕竟一手的资料比二手的译本更能代表原作者的意思是吧。
>
> 如果有什么想跟我聊的欢迎在群里骚扰我哈，基本秒回^_^

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [zhangferry](https://zhangferry.com)

### 缓动函数

很多动画为了效果更加自然，通常都不是线性变化的，而是先慢后快，或者先慢后快再慢的速度进行的。在 iOS 开发里会用 `UIView.AnimationOptions`这个枚举值进行描述，它有这几个值：

```swift
public struct AnimationOptions : OptionSet {
	public static var curveEaseInOut: UIView.AnimationOptions { get } // default
	public static var curveEaseIn: UIView.AnimationOptions { get }
	public static var curveEaseOut: UIView.AnimationOptions { get }
	public static var curveLinear: UIView.AnimationOptions { get }
}
```

ease 表示减缓，所以 easeInOut 表示，进入和完成都是减缓的，则中间就是快速的，就是表示先慢后快再慢。那这个先慢后快，或者先快后慢的过程具体是如何描述的呢？这里就引入了缓动函数，缓动函数就是描述这一快慢过程的函数，其对应三种状态：easeIn、easeOut、easeInOut。

缓动函数并非特定的某一个函数，它有不同的拟合方式，不同形式的拟合效果可以参看[下图](https://easings.net/)：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210920125221.png)

缓动函数名例如 easeInSine 后面的 Sine 就是拟合类型，其对应的就是三角函数拟合。常见的还有二次函数Quad，三次函数Cubic等。以上函数有对应的 [TypeScript 源码](https://github.com/ai/easings.net/blob/33774b5880a787e467d6f4f65000608d17b577e2/src/easings/easingsFunctions.ts "easingsFunctions.ts")，有了具体的计算规则，我们就可以将缓动效果应用到颜色渐变等各个方面。以下是三角函数和二次函数拟合的Swift版本：

```swift
struct EasingsFunctions {
    /// sine
    static func easeInSine(_ x: CGFloat) -> CGFloat {
        return 1 - cos((x * CGFloat.pi) / 2)
    }
    static func easeOutSine(_ x: CGFloat) -> CGFloat {
        return sin((x * CGFloat.pi) / 2)
    }
    static func easeInOutSine(_ x: CGFloat) -> CGFloat {
        return -(cos(CGFloat.pi * x) - 1) / 2
    }
    /// quad
    static func easeInQuad(_ x: CGFloat) -> CGFloat {
        return x * x
    }
    static func easeOutQuad(_ x: CGFloat) -> CGFloat {
        return 1 - (1 - x) * (1 - x)
    }
    static func easeInOutQuad(_ x: CGFloat) -> CGFloat {
        if x < 0.5 {
           return 2 * x * x
        } else {
           return 1 - pow(-2 * x + 2, 2) / 2
        }
    }
}
```

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

1、[面向协议编程与 Cocoa 的邂逅 (上)](https://onevcat.com/2016/11/pop-cocoa-1/  "面向协议编程与 Cocoa 的邂逅 (上)") -- 来自：OneV's Den

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：文章先通过引入例子介绍OOP的核心思想：封装、继承。随后介绍OOP中“Cross-Cutting Concerns”、多继承的菱形缺陷问题、动态派发的安全问题这三大困境。面向协议编程可以解决除菱形问题外的其他问题。

2、[Swift Protocol 详解 - 协议&面向协议编程](https://juejin.cn/post/6844903502817263630 "Swift Protocol 详解 - 协议&面向协议编程") -- 来自掘金：RickeyBoy


[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：文章概念性的东西较多，本文先介绍了协议的基本使用方法，主要介绍耦合相关的概念，例如耦合的5个级别、耦合带来的问题、依赖翻转和协议解耦等。

3、[如果你还在用子类（Subclassing），那就不对了](https://www.jianshu.com/p/80bd6633ec7c?utm_campaign=hugo&utm_medium=reader_share&utm_content=note "如果你还在用子类（Subclassing），那就不对了") -- 来自简书：97c49dfd1f9f 


[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：  本文主要介绍了面向协议、面向对象、函数式编程的优缺点。OC->Swift不仅仅是语法上的变化，想想大家项目中的xxxBasexxx.m，如果用Swift开发需要避免再出现此类情况。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### a-picture-is-worth-a-1000-words

地址：https://github.com/girliemac/a-picture-is-worth-a-1000-words

把复杂知识放进简单涂鸦！该仓库中用可爱的涂鸦绘制了包涵数据结构、算法、机器学习入门、web 基础开发的一些知识，画风可爱，简单易懂。但要下载的时候要注意一下，涂鸦图片很大。

### raywenderlich/swift-style-guide

地址：https://github.com/raywenderlich/swift-style-guide

来自 raywenderlich 的 Swift 代码风格指南，其风格的重点在于印刷和网页版的可读性，这个风格指南是为了保持他们的书籍、教程和入门套件中的代码的优雅和一致性。可以供大家有特别需要时参考和借鉴。

## 工具推荐


整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### XcodesApp

**地址**： https://github.com/RobotsAndPencils/XcodesApp

**软件状态**： 免费，开源

**软件介绍**

Xcode多版本切换工具，支持下载不同版本的Xcode，动态切换指定版本


![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/xcodes.png)


 

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第二十七期](https://mp.weixin.qq.com/s/WvctY6OG1joJez2g6owroA)

[iOS摸鱼周报 第二十六期](https://mp.weixin.qq.com/s/PnUZLoyKr8i_smi0H-pQgQ)

[iOS摸鱼周报 第二十五期](https://mp.weixin.qq.com/s/LLwiEmezRkXHVk66A6GDlQ)

[iOS摸鱼周报 第二十四期](https://mp.weixin.qq.com/s/vXyD_q5p2WGdoM_YmT-iQg)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
