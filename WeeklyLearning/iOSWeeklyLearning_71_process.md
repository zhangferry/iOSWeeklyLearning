# iOS 摸鱼周报 #71 | One More Thing?

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：十月份 One More Thing? Apple 新增 QA 活动；Swift 和  SwiftUI 在 iOS 系统中的使用情况。 
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### One More Thing?

[@zhangferry](zhangferry.com)：虽然还没有官宣，但是网上已经讨论很多了，Apple 10 月还会有一场发布会。YouTube 博主 GregsGadgets 录了一期视频爆料新产品：[Apple October Event LEAKS!](https://www.youtube.com/watch?v=euUGv_Fz71o&list=RDCMUCoi3Uk6JtP9QgA5BRwnh6NQ "Apple October Event LEAKS!")。

![](https://cdn.zhangferry.com/Images/20221011224436.png)

新产品会有这些：New iPads、New M2 iPad Pros、M2 Mac mini、M2 MacBook Pro（14/16寸），M2 版本的 Mac Pro 和 Apple TV 也可能会一起发布。

### [Apple 提供 Ask People 服务](https://developer.apple.com/cn/events/ask-apple/ "Ask People")

![](https://cdn.zhangferry.com/Images/20221012233542.png)

[@zhangferry](zhangferry.com)：Apple 提供了 Ask People 服务让开发者能够通过 Slack 与 Apple 专家进行交流。Ask People 可以理解为一个 QA 环节，可以问代码级别的支持、设计建议、系统库使用等内容，Apple 指定了一段时间用于问答，从 10月 17 号开始到 21 号结束，这个期间会按照不同专题进行问答，这些专题对应 Slack 不同频道。活动注册，需要为开发者计划会员，具体日程和话题安排可以参照这个[日程表](https://developer.apple.com/cn/events/ask-apple/questions-and-answers/ "Ask People 日程表")。

Tech Talks 和 Meet with Apple Store Experts 项目在过去一年提供了 200 多个现场演示时长达数千小时。Apple 从这些活动中看到开发者对 Apple 专家交流的诉求，于是有了 Ask People。所以有理由相信后面还会有更多的 Ask People。

### [Swift 和 SwiftUI 在系统层面使用情况](https://blog.timac.org/2022/1005-state-of-swift-and-swiftui-ios16/ "Swift 和 SwiftUI 在系统层面使用情况")

[@zhangferry](zhangferry.com)：作者通过分析系统库的所有二进制文件来统计 Swift 和 SwiftUI 在系统版本上的占比情况：

![](https://cdn.zhangferry.com/Images/20221011222541.png)

统计方式是把系统中的所有二进制文件数量作为总数（不包含 XNU 和固件代码），如果该二进制文件中包含以上统计信息（语言或框架）就加一，按照比例划分做出上图。从这张图中可以得出以下结论：

* Objective-C 仍然是 iOS 系统的核心语言。
* Swift 在系统库中的使用越来越高，相对成熟；SwiftUI 开始崭露头角但仍处于早期阶段。
* C 语言在慢慢退出。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)


## 内容推荐

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)


## 摸一下鱼

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[迷宫生成器](https://www.mazegenerator.net/ "迷宫生成器")：一个可以生成多种形状、规格迷宫的网站。生成的迷宫图形可以以 PDF 的格式下载，并且会附带迷宫解法。

![image-20221013094111617](https://cdn.zhangferry.com/Images/image-20221013094111617.png)

2、[老地图查询](https://www.oldmapsonline.org/ "老地图查询")：该网站汇总了大量文献中的老地图，选择你要查询的位置，网站会列出与其相关的各个时期的老地图资料。

![image-20221013095128193](https://cdn.zhangferry.com/Images/image-20221013095128193.png)

3、[来自幽灵的数字](https://www.anumberfromtheghost.com/ "来自幽灵的数字")：Peter Adams 为自己的音乐创建的一个虚幻的空间。音乐与视觉共同营造了一个梦幻的氛围。

![image-20221013100119087](https://cdn.zhangferry.com/Images/image-20221013100119087.png)

4、[imagesTool —— 无需上传的在线图片处理服务](https://imagestool.com/zh_CN/ "imagesTool —— 无需上传的在线图片处理服务")：提供了格式转换、水印、拼接、Gif 处理、视频转 Gif 等多项功能。所有工具均使用浏览器本地技术实现，无需上传，速度更快、隐私也更有保障。

![image-20221013101815464](https://cdn.zhangferry.com/Images/image-20221013101815464.png)

5、[第一批彩色字体在谷歌字体上发布](https://material.io/blog/color-fonts-are-here "第一批彩色字体在谷歌字体上发布")：通过 COLRv1 格式，字体设计师可以设计并制作更富表现力的可定义字体。本次一共发布了九款彩色字体。Chrome、Android 和 Google 字体 API 中已经提供了对 COLRv1 格式的支持。

![1-google-font.png](https://cdn.zhangferry.com/Images/71-google-font.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #63 | Apple 企业家培训营已开放申请](https://mp.weixin.qq.com/s/nAMshUG4AjWLAAHOFPVqXg)

[iOS 摸鱼周报 #62 |  Live Activity 上线 Beta 版 ](https://mp.weixin.qq.com/s/HySX4Yaf3Zxy8Wn-LyUO0A)

[iOS 摸鱼周报 #61 |  Developer 设计开发加速器](https://mp.weixin.qq.com/s/WfwqRhC-9-isUanv8ZnvMQ)

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
