# iOS 摸鱼周报 #82

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：App Store 的定价机制升级扩展；四位女性开发者与 App Store 的故事
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [App Store 的定价机制升级现已扩展至所有购买类型](https://developer.apple.com/cn/news/?id=dbrszv62 "App Store 的定价机制升级现已扩展至所有购买类型")

[@远恒之义](https://github.com/eternaljust)：即日起，App Store 最全面的定价机制升级迎来更新，包括新增价格点和按店面管理定价的全新工具。其中，你可在 900 个价格点中选择更灵活的定价，根据你熟悉的国家或地区来生成生成全球均衡价格，也可以为各个市场分发定制的内容和服务。此外，全新的增强定价机制更适用于当地顾客的价格，该机制将会在 2023 年 5 月 9 日更新调整。

### [四位女性通过 app 与游戏推动文化发展并创造改变](https://www.apple.com.cn/newsroom/2023/03/meet-four-women-using-apps-and-games-to-drive-culture-and-create-change/ "四位女性通过 app 与游戏推动文化发展并创造改变")

[@远恒之义](https://github.com/eternaljust)：女性开发者在开发者生态圈是一股不可忽视的力量，Apple 也一直在竭尽全力帮助女性开发者获得更好的成长，此前开展了包括 Apple Entrepreneur Camp（苹果企业家培训营）课程活动，以及针对中国女性开发者的“女性开发者社区日”特别活动。本篇内容为国际妇女节的主题特写，Apple 沟通了四位不同女性，这些女性主导的团队正在努力彰显女性的声音，文中分享了她们如何利用技术来鼓舞女性、创造社会变革的心得。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

推荐近期的一些优秀博文，涵盖结构化并发、开发者故事、开发经验分享、Swift Builtin 函数等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[神秘的 Swift 内置模块](https://juejin.cn/post/7208534700223250487 "神秘的 Swift 内置模块") -- 作者：ankit 中文翻译：桃红宿雨

[@东坡肘子](https://www.fatbobman.com/): 如果你已经阅读过 Swift 的 stdlib 库，那大概率注意到了有很多 Builtin.* 类的函数，诸如：`Builtin.Int1`、`Builtin.RawPointer`、`Builtin.NativeObject` 等，这些神秘的 Builtin 到底是什么呢？本文主要解释了 Builtin 存在的原因：加快编译速度（Swift 很多 struct 值类型，最终内部都封装了 IILV IR 基础类型，不需要过多转换）；提高运行性能（由于不需要做过多转换，直接使用的 IILV IR 的函数，相当于使用很多类似底层函数在开发，性能更高）。

2、[手工打造 HTML 解析器的那些事](https://zhgchg.li/posts/2724f02f6e7/ "手工打造 HTML 解析器的那些事") -- 作者：ZhgChgLi

[@东坡肘子](https://www.fatbobman.com/): [ZMarkupParser](https://github.com/ZhgChgLi/ZMarkupParser) 是一个纯 Swift 库，可帮助你将 HTML 字符串转换为具有自定义样式和标签的 NSAttributedString。在本文中，ZhgChgLi 详细介绍了开发该库过程中所涉及的技术细节(HTML String 的 Tokenization 转换、Normalization 处理、Abstract Syntax Tree 的产生、Visitor Pattern / Builder Pattern 的应用)以及一些开发杂谈。本文篇幅很长，难得有开发者会做如此详尽的记录。

3、[结构化并发](http://chuquan.me/2023/03/11/structured-concurrency/ "结构化并发") -- 作者：楚权

[@东坡肘子](https://www.fatbobman.com/): 对于异步与并发，一直以来，业界都有着非常广泛的研究，针对特定场景提出了很多相关的技术，如：Future/Promise、Actor、CSP、异步函数等等。本文通过 GOTO 有害论引出编程历史中结构化编程的演化。以结构化编程作为类比，介绍了结构化并发的核心观点，以及结构化并发的设计理念。结构化并发主要包括作用域、异步函数、计算续体、协程等技术，此外还需要运行时系统的调度，才能最终实现理想的结构化并发。

4、[通过 vacuuming 优化 CoreData 存储文件尺寸](https://blog.eidinger.info/keep-your-coredata-store-small-by-vacuuming "通过 vacuuming 优化 CoreData 存储文件尺寸") -- 作者：Marco Eidinger

[@东坡肘子](https://www.fatbobman.com/): 默认情况下，当你从表中删除数据或删除表、视图或索引等数据库对象时，SQLite 数据库不会自动“释放”磁盘空间。因为 SQLite 只是将删除的对象标记为空闲并保留空间以供将来使用。结果，数据库文件的大小总是在增长。在这篇博文中，Marco Eidinger 将解释 VACUUM 这个概念以及如何将这个概念应用到你的 CoreData 存储中来减少存储文件的尺寸。

5、[独立开发周报 #4 (0306-0312)](https://mp.weixin.qq.com/s/cEieMaUxSxDAZq0Cm_gwEQ "独立开发周报 #4 (0306-0312)") -- 作者：vulgur

[@东坡肘子](https://www.fatbobman.com/):  vulgur 是“极简时钟”、“极简日记”等 App 的作者，从一个月前开始，每周都通过博客的方式来记录自己的开发生活。通过他的记录，你可以对国内独立开发者的工作、生活状态有更多的了解。



## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
