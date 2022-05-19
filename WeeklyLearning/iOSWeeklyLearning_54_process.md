iOS 摸鱼周报 52 | 如何规划个人发展

![](http://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

### [Apple 在辅助功能上的又一创新](https://www.apple.com/newsroom/2022/05/apple-previews-innovative-accessibility-features/ "Apple 在辅助功能上的又一创新")

[@zhangferry](zhangferry.com)：作为一款受众非常广的产品，针对特殊人群的辅助功能就显得尤为重要，不得不说 Apple 对辅助功能的重视程度和探索精神都是值得尊敬的。最近 Apple 又公布了一些基于软硬件和机器学习带来的辅助功能提升。

针对盲人和视力障碍的人群：Apple 基于配有 LiDAR 的设备可以探测到前方是否有门，门距离自己有多远，甚至要通过推还是拉的方式开门都能识别出来。

针对行动不便的人群：有一项 iPhone 结合 Apple Watch 的功能，借助于 Apple Watch 的 Mirroring 功能，可以用手机远程操作 Apple Watch。同时 Apple Watch 也有提升，通过 AssistiveTouch 技术，可以让 Apple Watch 识别特定手势，像是手指两次捏合的手势可以用于接电话、拍照、暂定音乐等。

针对听力障碍的人群：在 iPhone、iPad、Mac 配备了实时字幕功能，不只是针对 Facetime，对于任意音频内容，包括外部 App 都可以使用。样式是在设备顶部展示一个文本转义框，字体大小还可调整。

同时 VoiceOver 也进一步完善，增加了 20 多个地区语言的支持。

## 面试解析

整理编辑：[JY](https://juejin.cn/user/1574156380931144)



## 优秀博客



## 见闻

> 这一周阅读/浏览到的有趣的资讯。

1、[Mac 与游戏无缘，M1 来了也没用](https://mp.weixin.qq.com/s/z10cepyRBFVPql52Ym1m0g) -- 来自公众号：APPSO

[@远恒之义](https://github.com/eternaljust)：提到游戏，具体到 PC 端的游戏，Mac 电脑基本是沾不上边的。传统意义上的 PC 游戏，指的是在 Windows 电脑上玩的游戏，Mac 电脑只是一个生产力工具。我曾下载过战网客户端，在 Mac 上玩暴雪游戏《炉石传说》，但这样原生支持 Mac 平台的厂商并不多。我也用过腾讯 START 云游戏，对网络要求很高，在 MacBook 上玩《英雄联盟》，打团时的延迟尚能接受。最近拿 PS5 手柄在 iPad 上试玩 Arcade 游戏，游戏体验还不错，也能兼容 Mac 平台。那么，为什么 Mac 距离主流游戏市场这么远呢？M1 芯片的到来，能给 Mac 游戏带来新的机遇吗？作者在文中给出了答案。

2、[对 iPod 说再见，我想带你走进无数人的「青春记忆」](https://sspai.com/post/73225 "对 iPod 说再见，我想带你走进无数人的「青春记忆」") -- 来自少数派：宛潼

[@远恒之义](https://github.com/eternaljust)：停产了，售罄了，下架了，拥有 20 年寿命的 iPod，走到了生命的终点。作为一款音乐播放器，iPod 的产品线十分丰富。无论是初代经典 iPod Classic，还是短暂尝试的 iPod mini，还有被用户吐槽最多的 iPod shuffle，多次探索新形态、新功能和新技术的 iPod nano，功能强大的 iPod touch，这些都已成为了历史，让人怀恋。拥有过 iPod 的你，是否也有「爷青结」的感叹呢。就让本文的作者带你一起了解 iPod 相关的彩蛋产品，唤起你的「青春记忆」吧。

3、[Bash tips: Colors and formatting (ANSI/VT100 Control sequences)](https://misc.flogisoft.com/bash/tip_colors_and_formatting "Bash tips: Colors and formatting (ANSI/VT100 Control sequences)")

[@zhangferry](zhangferry.com)：终端常见的输出样式是黑白，但实际上它还可以设置颜色和一些简单的格式，这些样式的配置可以利用 ANSI 转义码。整个过程分为两步，第一，让 Bash 识别转义码，第二步，指定转义码颜色。看一个例子：

```bash
$ echo -e "\e[31mRed Text\e[0m"
```

这个命令输出内容是红色文本的 Red Text，参数含义说明如下：

| Option |                         Description                          |
| :----: | :----------------------------------------------------------: |
|   -e   |                     开启反斜杠的转义功能                     |
|  \e[   | 它是 Bash 识别转义的起始标志符。`\e` 是 ASCII 码中的 ESC，表示控制符，8 进制表示为 `\033`，也是常见用法。`[` 是转义序列开始标记符 |
|  31m   |     由 ANSI 转义码定义，31 表示红色，m 表示颜色取值结束      |
| \e[0m  |         `\e` 含义同上，开始识别 ANSI，0 表示重置设置         |

## 学习资料

整理编辑：[zhangferry](https://zhangferry.com)

### 英语进阶指南

地址：https://babyyoung.gitbook.io/english-level-up-tips/

![](http://cdn.zhangferry.com/Images/20220518204154.png)

英语是程序员绕不过去的一项技能，虽然我们可能从小学就开始接触英语了，但直到毕业工作，英语能够不成为学习障碍还是一件不容易的事情。这其中的差别很大成分可以归结为学习方法，这份文档就是这样一个注重方法和可操作性的英语学习指南。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### CotEditor

**地址**：https://coteditor.com/

**软件状态**：免费

**软件介绍**：

适用于 `macOS` 的纯文本编辑器，轻巧、整洁并且功能强大。

![CotEditor](http://cdn.zhangferry.com/screenshot@2x.png)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #51 | 游戏版号恢复发放](https://mp.weixin.qq.com/s/ogjhELipiVFRaYJkT2NQwA)

[iOS 摸鱼周报 第五十期](https://mp.weixin.qq.com/s/6IS0RlytWxjeRHyh0f2fXA)

[iOS 摸鱼周报 第四十九期](https://mp.weixin.qq.com/s/6GvVh8_CJmsm1dp-CfIRvw)

[iOS摸鱼周报 第四十八期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](http://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
