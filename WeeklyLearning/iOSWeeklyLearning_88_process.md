# iOS 摸鱼周报 #82

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：Apple 公布 iOS 16 的普及率已达 81%
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [Apple 公布 iOS 16 的普及率已达 81%](https://developer.apple.com/cn/support/app-store/ "Apple 公布 iOS 16 的普及率达 81%")

[@远恒之义](https://github.com/eternaljust)：Apple 官方数据来源于 App Store 上进行交易的设备统计，时间截止至 2023 年 2 月 14 日。在过去四年推出的设备中，iOS 16 的普及率达 81%。在所有的设备中，iOS 16 的普及率达 72%，加上 iOS 15 的 20%，iOS 15 系统及以上的普及率总计 92%。是时候修改 iOS 项目最低版本的限制了，开发者们要紧跟 Apple 的步伐，毕竟现在「小而美」的微信，也早已是 iOS 13 系统起步。

![](https://cdn.zhangferry.com/Images/85-ios16-ipados16.png)

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

整理编辑：[@远恒之义](https://github.com/eternaljust)



## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[Cursor](https://www.cursor.so/ "Cursor")：集成 GPT-4 的代码编辑器，不需要 OpenAI Key，免费使用。体验了一下，感觉真的改变了很多编程习惯。它主要有这几个功能：

* Generate：用于生成内容，在空白区域键入 Commond + K，输入指令即可。这里即可以生成模版代码，也可以通过提问题的方式，让它给出答案。

* Edit：代码编辑，这里需要选中代码才能执行编辑操作。我在上一步问了 IDE 一个问题，如果在 Swift 中调用 C 函数，它给了我一个示例。然后我选中这段代码，执行Edit，输入指令：把示例中的 int 参数转成 char 参数。它逐行扫描，还显示出了修改之后的 Diff 信息，点击 Accept 即可以实现替换。

  ![](https://cdn.zhangferry.com/Images/202303212355300.png)

* Chat：这个也是针对内容选中的功能，它可以支持长段对话。我让它帮我介绍整个文件的含义，有时中文输入的问题，结果还是英文。然后问他代码有没有什么优化的空间，它也很快给了一些建议，也挺符合编程规范的。

![](https://cdn.zhangferry.com/Images/202303212334574.png)

基于GPT4协作编程这件事，有人总结了一些[可以遵循的要点](https://twitter.com/goldengrape/status/1638049866604777472 "GPT4协作编程要点-Twitter")：

> 0.建立一个markdown文件记录prompt 
>
> 1.写明程序目的 
>
> 2.写明程序实现目的的方法/流程 
>
> 3.注明编程风格，要求GPT4写出函数的作用描述、输入、输出，但不必列出函数的具体实现。 
>
> 4.由GPT4生成函数设计 
>
> 5.注明需要使用的库，列出库中的几个典型示例，复制之上所有部分交GPT4生成代码
>
> 6.debug，将代码和报错一起交给GPT4，询问错误出现的原因，并修改。注意GPT4的知识过时，有可能引用不存在的库中的函数方法，可能需要以ChatPDF或者Bing Chat协助或者手动找到对应的函数，并找到说明或者示例，一同交给GPT4生成新代码。 
>
> 7.记录debug要点于文件中。

2、[Prompt 编写模式](https://prompt-patterns.phodal.com/ "Prompt 编写模式")：像 ChatGPT、MidJourney 这类 AI 工具，正在一步步颠覆我们之前对工具的使用方式。如何使用 AI，就像是电脑刚出现时，如何使用电脑一样，它很强大，但如何发挥它的强大，如何借助于 AI 让自己的做事效率提升，这是一件差异很大的事情。

目前我们跟 AI 的交互基本都是通过 Prompt 进行的，如何编写 Prompt，如果高效的获取我们希望的结果，正是这篇文章想要解答的问题。作者并非按各个用途总结 Prompt 使用方式，而是按照设计模式的形式把跟AI对话的 Prompt 进行了抽象，正如它的目标：**如何将思维框架赋予机器，以设计模式的形式来思考 prompt**。

![](https://cdn.zhangferry.com/Images/202303222234824.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
