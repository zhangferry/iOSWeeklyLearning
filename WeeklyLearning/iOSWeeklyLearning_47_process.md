# iOS摸鱼周报 第四十七期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：苹果多个产品线的更新。
> * Tips：
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：苹果的多个产品线带来了一波更新。

### macOS Monterey 12.3

* Python 2 被从系统中移出了，但新系统中也并没有预装 Python 3，需要开发者手动安装。
* Universal Control（通用控制）：键盘、鼠标和触摸板可以在 Mac 和 iPad (iPadOS 15.4) 端无缝衔接。
* M1 芯片的电脑可以搭配支持空间音频的 AirPods 使用头部追踪功能。

### Xcode 13.3

听说又很多兼容问题

### iOS 15.4

* 支持戴口罩的 FaceID 功能，仅支持 iPhone 12 及之后的机型。
* 新增了 37个 Emoji 表情。

### Swift 5.6 Released

* 类型系统的提升。[Type Placeholders SE-0315](https://github.com/apple/swift-evolution/blob/main/proposals/0315-placeholder-types.md "Type Placeholders SE-0315")
* 改进了指针交互的功能
* SPM 增加了运行新插件的能力

还有一个便利性的提升：[SE-0290: Unavailability Condition](https://github.com/apple/swift-evolution/blob/main/proposals/0290-negative-availability.md "SE-0290: Unavailability Condition") 

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)



## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)



## 见闻

> 过一周阅读或者观看到的有价值的讯息。

1、[深度学习撞墙了](https://www.jiqizhixin.com/articles/2022-03-11-4 "深度学习撞墙了") -- 来自：机器之心

[@zhangferry](zhangferry.com)：早在2016年，深度学习教父级人物 Hinton 就曾说过，我们不用再培养放射科医生了。但如今 AI 并没有取代任何一位放射科医生，问题出在哪呢？在 Robust.AI 创始人Gary Marcus看来深度学习可能就要撞墙了。整个AI领域需要寻找新的出路。

深度学习本质上是一种识别模式，当我们只需粗略结果时，它非常适合，但是对于需要精确性操作且风险很高的事情，像放射学和无人驾驶，就需要很谨慎了。人工智能确实没有我们想象的进化那么快，所以它的未来是悲观的吗？并不是，作者提出 Hinton 这样的先驱把深度学习的研究方向带偏了，应当将深度学习和符号处理结合起来，这种混合人工智能可能才是最好的方向。

2、[估值超百亿的 Figma 封禁中国大疆：科技再无中立可言](https://www.infoq.cn/article/lHx2zw4QKWWs3PmvWXgS "估值超百亿的 Figma 封禁中国大疆：科技再无中立可言")

[@zhangferry](zhangferry.com)：Figma 决定遵守美国制裁名单，并停封所有遭制裁的企业账号，其中就包括大疆。与此同时，国内的产品设计协作平台蓝湖旗下的同类竞品 MasterGo 推出一键导入 Figma 素材功能。

3、[如何打造良好的分享氛围 ]()-- 来自公众号：hockor

[@zhangferry](zhangferry.com)：大多数人都会在工作中遇到技术分享这个事情，作为TL应该如何打造良好的分享氛围呢？首先明确良好的分享氛围是有很大好处的，比如提升团队的技术视野、发现团队牛人、提升团队战斗力、扩大团队影响力等。分享形式较普遍的定期举行技术分享会，任何的分享行为都应该被鼓励。“分享本身是一种精神上自我实现的行为，所以无论分享内容如何，至少这种行为是慷慨的，我们应该及时的、积极的反馈，去鼓励他们往前更进一步”。

同时作为分享的参与者，我们应该抱着探索者的积极的心态去听，有参与感的学习形式是非常高效的。

4、[Usage statistics of content languages for websites](https://w3techs.com/technologies/overview/content_language) -- 来自网站：W3Techs

[@zhangferry](zhangferry.com)：当前世界上的网站按语言划分的话，英语最多，这个毋庸置疑。但第二多的竟然是俄语，更令人意外的是，作为使用人口非常多的汉语，其网站数量占比竟然排到了第10位。我能想到的原因是，俄语地区互联网发展比较早，催生了很多网站；汉语虽然使用人数多，但是相对集中，国内互联网的发展比较晚，近几年移动互联网浪潮催生了很多App，但网站的创建则很少。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220316231714.png)


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

iOS摸鱼周报 第四十六期

[iOS摸鱼周报 第四十五期](https://mp.weixin.qq.com/s/_N98ADlfQCUkxYjmH0SvZw)

[iOS摸鱼周报 第四十四期](https://mp.weixin.qq.com/s/q__-veuaUZAK6xGQFxzsEg)

[iOS摸鱼周报 第四十三期](https://mp.weixin.qq.com/s/Ktk5wCMPZQ5E-UASwHD7uw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
