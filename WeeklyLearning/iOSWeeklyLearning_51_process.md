# iOS摸鱼周报 第五十一期

![](http://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：游戏版号恢复发放，45款游戏获版号
> * 面试模块：简述 `mmap` 应用
> * 优秀博客：iOS内购
> * 学习资料：
> * 开发工具：`Quiver`是为程序员打造的笔记本。它让您可以在一个笔记中轻松混合文本、代码、`Markdown` 和 `LaTeX`

## 本期话题

### [游戏版号时隔8个月恢复发放，4月45款游戏获版号！](https://www.nppa.gov.cn/nppa/contents/320/103799.shtml "游戏版号时隔8个月恢复发放，4月45款游戏获版号！")

[@iHTCboy](https://ihtcboy.com/)：4 月 11 号下午，很多游戏公司的老板在朋友圈透露，今晚发版号了！从 2021 年 7 月 22 日至今，8 个月后游戏版号迎来重启。对我们游戏行业者来说无疑是一个好消息，因为有版号就有新游戏可以上线，对于游戏市场也是一个好的信号，一个全新的开始。另外，4 月 15 号，国家两部门[联合通知](http://www.nrta.gov.cn/art/2022/4/15/art_113_60105.html "联合通知")：严禁网络视听平台传播违规游戏。未经主管部门批准的网络游戏，不得通过各类平台进行传播。

网络直播乱象、青少年沉迷游戏等问题，也一直是全民关心的问题，所以，游戏作为一个重要的内容创作平台，应该传递更多正能量，理性表达、合理消费，共同维护文明健康的网络视听生态环境。

## 面试解析

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### mmap 应用

`mmap`是系统提供的一种虚拟内存映射文件的方法。可以将一个文件或者其他对象映射到进程的地址空间，实现文件磁盘地址和进程中虚拟内存地址的一个映射关系。

在 iOS 中经常用在对性能要求较高的场景使用。例如常见的 `APM` 的日志写入，大文件读写操作等。

> `mmap`还有可以用来做共享内存进程通信、匿名内存映射，感兴趣的同学可以自行学习

#### 普通`I/O`流程

普通的读写操作，由于考虑虚拟内存权限安全的问题，所有操作系统级别的行为（例如 `I/O`）都是在内核态处理的。同时  `I/O` 操作为了平衡主存和磁盘之间的读写速度以及保护磁盘写入次数，做了缓存处理，即 `page cache`该缓存是位于内核态主存中的。

内核态空间，用户进程是无法直接访问的，可以间接通过**系统调用**获取并拷贝到用户态空间进行读取。 即一次读操作的简化流程为：

1. 用户进程发起读取数据操作`read()`。

2. `read()`通过系统调用函数调用内核态的函数读取数据

3. 内核态会判断读取内存页是否在 `Page Cache`中，如果命中缓存，则直接拷贝到主存中供用户进程使用

4. 如果未命中，则先从磁盘将数据按照 `Page Size`对齐拷贝到 `Page Cache`中，然后再次执行上面步骤 3

所以一次普通读写，最多需要经历两次数据拷贝，一次是从磁盘映射到 `Page cache`，第二次是`Page Cachef`拷贝到用户进程空间。

以上只是简化后的流程，对文件读写操作感兴趣的可以通过该文章学习[从内核文件系统看文件读写过程 ](https://www.cnblogs.com/huxiao-tee/p/4657851.html "从内核文件系统看文件读写过程")

#### 优缺点

由上可知 `mmap`相比普通的文件读写，优势在于可以有选择的映射，只加载一部分内容到进程虚拟内存中。另一方面，由于 `mmap`是直接映射磁盘文件到虚拟内存，减少了数据交换的次数，所以写入性能也更快。

在存在优势的同时，也有一些缺点，例如 `mmap` 要求加载的最小单位为 `VM Page Size`，所以如果是小文件，该方法会导致碎片空间浪费。

#### mmap API 示例

`mmap` 实际应用主要是 `mmap() & munmap()`两个函数实现。两个函数原型如下：

```cpp
/// 需要导入头文件
#import <sys/mman.h>

void* mmap(void* start,size_t length,int prot,int flags,int fd,off_t offset);
 int munmap(void* start,size_t length);
```

函数参数：

- `start`：映射区的其实位置，设置为零表示由系统决定映射区的起始位置
- `length`： 映射区长度，单位是字节， 不足一页内存按一整页处理
- `prot`：期望的内存保护标志，不能与文件打开模式冲突，支持 `|` 取多个值
    - `PROT_EXEC`: 页内容允许执行
    - `PROT_READ`：页内容允许读取
    - `PROT_WRITE`：页内容可以写入
    - `PROT_NONE`：不可访问
- `flags`：指定映射对象的类型，映射选项和映射页是否可以共享（这里只注释使用的两项，其他更多定义可以自行查看）
    - `MAP_SHARED`：与其它所有映射这个文件对象的进程共享映射空间。对共享区的写入，相当于输出到文件。
    - `MAP_FILE`：默认值，表示从文件中映射
- `fd`：有效的文件描述词。一般是由open()函数返回，其值也可以设置为-1，此时需要指定flags参数中的MAP_ANON,表明是匿名映射。
- `off_set`：文件映射的偏移量，通常设置为0，代表从文件最前方开始对应offset必须是分页大小的整数倍。

`mmap` 回写时机并不是实时的，调用 `msync()`或者`munmap()` 时会从内存中回写到文件，系统异常退出也会进行内容回写，不会导致日志数据丢失，所以特别适合日志文件写入。

> Demo 可以参考开源库 `OOMDetector` 中的 `HighSppedLogger` 类的使用封装，有比较完整的映射、写入、读取、同步的代码封装，可直接使用。

#### 注意事项

`mmap` 允许映射到内存中的大小大于文件的大小，最后一个内存页不被使用的空间将会清零。但是如果映射的虚拟内存过大，超过了文件实际占用的内存页数量，后续访问会抛出异常。

示例可以参考[认真分析mmap：是什么 为什么 怎么用 ](https://www.cnblogs.com/huxiao-tee/p/4660352.html "认真分析 mmap: 是什么 为什么 怎么用")中的情景二：

![](http://cdn.zhangferry.com/Images/weekly_51_interview.png)

超出文件大小的虚拟内存区域，文件所在页的内存扔可以访问，超出所在页的访问会抛出 `Signal` 信号异常

#### 参考

- [认真分析mmap：是什么 为什么 怎么用 ](https://www.cnblogs.com/huxiao-tee/p/4660352.html "认真分析 mmap: 是什么 为什么 怎么用")
- [C语言mmap()函数：建立内存映射](http://c.biancheng.net/cpp/html/138.html "C语言mmap()函数：建立内存映射")
- [OOMDetector](https://github.com/Tencent/OOMDetector "OOMDetector")


## 优秀博客

整理编辑：[@我是熊大](https://github.com/Tliens)

> 本期优秀博客的主题为：iOS内购。

1、[iOS内购详解](https://juejin.cn/post/7029252038252822564 "iOS内购详解") -- 来自掘金：QiShare

[@我是熊大](https://github.com/Tliens)：本文是QiShare针对内购写的一篇文章，包含了内购前的准备、内购流程、恢复购买、内购掉单等内容。

2、[iOS内购（IAP）自动续订订阅类型总结](https://juejin.cn/post/6844904021229060103 "iOS内购（IAP）自动续订订阅类型总结") -- 来自简书：凡几多

[@我是熊大](https://github.com/Tliens)：本文主要介绍自动订阅的相关情况。自定订阅与其他的购买不同，是比较复杂的一种情况。自定续期订阅类是有连续性的，其中还有免费试用期、促销期、宽限期的概念。用户还可以取消续订，恢复续订等，这无疑又增加了复杂性。

3、[iOS项目技术还债之路《二》IAP掉单优化](https://juejin.cn/post/6844904021229060103 "iOS项目技术还债之路《二》IAP掉单优化") -- 来自掘金：njuxjy

[@我是熊大](https://github.com/Tliens)：IAP调单一定是大多数开发者不可避免的问题，作者针对调单情况做了非常详细的总结，如果你也正有类似的问题，推荐阅读。

4、[苹果iOS内购三步曲：App内退款、历史订单查询、绑定用户防掉单！--- WWDC21](https://juejin.cn/post/6974733392260644895 "苹果iOS内购三步曲：App内退款、历史订单查询、绑定用户防掉单！--- WWDC21") -- 来自掘金：37手游iOS技术运营团队

[@我是熊大](https://github.com/Tliens)：本文是基于WWDC21的总结，介绍了最新的内购情况，StoreKit 2的出现让内购更简单。惊喜的是：客户端已经支持用户退款了。

5、[SwiftyStoreKit](https://github.com/bizz84/SwiftyStoreKit "SwiftyStoreKit") -- 来自SwiftyStoreKit

[@我是熊大](https://github.com/Tliens)：一个star高达5.9k的开源库，支持内购查询、购买、校验、结束交易等。api简洁易懂，能帮助你在项目中快速接入内购，美中不足的是不支持订单退订，这还需要自己开发。

## 见闻

> 这一周阅读/浏览到的有趣的资讯。

1、[不止用手才能打字，用脸也行](https://www.ifanr.com/1482571 "不止用手才能打字，用脸也行") -- 来自爱范儿：邓 南

[@远恒之义](https://github.com/eternaljust/)：作为一名程序员，如果有一个要在照顾刚出生婴儿时完成的编码需求，遇到这种情况你会怎么做？购买静音键盘的打字声音或许对于小婴儿来说还是太吵了，那么如何才能一边带孩子一边工作呢，国外一名程序员给出了他的答案：面部打字。

![图片来自：YouTube 频道「Everything Is Hacked」](http://cdn.zhangferry.com/Images/face-detection.gif)

这款特殊的键盘名为「[CheekyKeys](https://github.com/everythingishacked/CheekyKeys "CheekyKeys github")」，开发采用了现代图像识别技术，利用 OpenCV 和 DLib 等工具跟踪用户脸部特定点的移动，打字识别的速度尚可。准备好电脑和摄像头，再学习一下摩斯密码，用户就可以开始尝试面部打字，非常锻炼脸部肌肉。

2、[程序员延寿指南](https://github.com/geekan/HowToLiveLonger "程序员延寿指南") -- 来自 Github: geekan

[@远恒之义](https://github.com/eternaljust/)：最近在逛 V 站的时候刷到一个[帖子](https://fast.v2ex.com/t/847490#reply42 "V 站原帖")，作者分享了一些如何活得更久的方法，里面提到了一个术语 ACM: All-Cause Mortality / 全因死亡率，十分好奇就去阅读了一下。作者提到的部分参考文献有矛盾争议，有几个观点我也不太赞同，该指南仅供大家参考。

如何稳健的活得更久，关键在于降低全因死亡率，具体可从三个方面来调整。
* 输入
  * 固体：吃白肉（-3%\~-11% ACM）、蔬果为主（-17%\~-26% ACM），多吃辣（-23% ACM），多吃坚果（-4%\~-27% ACM），中量碳水、多吃植物蛋白（-10% ACM）
  * 液体：喝咖啡（-12%\~-22% ACM），喝牛奶（-10%\~-17% ACM），喝茶（-8%\~15% ACM），少喝或不喝甜味饮料（否则每天一杯 +7% ACM），戒酒或每周 100g 内（否则 +\~50% ACM）
  * 气体：不吸烟（否则 +~50% ACM）
  * 光照：晒太阳（-~40% ACM）
* 输出
  * 运动：每周 3 次 45 分钟挥拍运动（-47% ACM）
  * 日常：刷牙（-25% ACM）
  * 睡眠：每天睡 7 小时全因死亡率最低；且 10-12 点间最好，早睡 +43% ACM，晚睡 +15% ACM
* 上下文
  * 体重：减肥（-54% ACM）

3、[Flying Through Giga Berlin](https://www.youtube.com/watch?v=7-4yOx1CnXE "Flying Through Giga Berlin")

这是特斯拉在 YouTube 发布的柏林工厂的航拍视频，国内也有人搬运，可以在 [B 站](https://www.bilibili.com/s/video/BV1B34y1s7wr "Giga 柏林特斯拉工厂航拍 - Bilibili")查看，清晰度差一些。不同于室外的高空航拍，这是一次工厂车间内的穿梭拍摄。无人机经过车间的各个厂区，飞跃车床和舞动的机械臂，从板材定型到成品车完成的主要环节都有展示。看着这些高度机械化的画面，真的非常震撼。

4、[Apple 微距摄影大赛获奖作品赏析](https://www.apple.com/newsroom/2022/04/apple-unveils-the-best-photos-from-the-shot-on-iphone-macro-challenge/ "Apple 微距摄影大赛获奖作品赏析")

微距模式是 iPhone 13 Pro 和 iPhone 13 Pro Max 开始支持的一种专门用于拍摄事物细节的功能。本次摄影大赛也是针对这两款机型举办，下面是其中一副获奖作品，很难想象这是用手机拍摄出来的。一片简单的树叶都有这么丰富的纹理，可以感受到微距模式下的镜头细节表现能力真的非常强。

![](http://cdn.zhangferry.com/Images/20220419230049.png)

5、[Web 3.0 漫游指南 2022【完整篇】](https://mirror.xyz/tannhauser2049.eth/vPrV-lqGjFpT2VWT4kDvtjhZayxm6n8ym7ra4wiegSc "Web 3.0 漫游指南 2022【完整篇】")

Web 3.0 是一个最近很热的概念，那什么是 Web 3.0 呢？作者用一个非常简单的类比，现实世界里的读书、写博客、出书，分别对应 Web1（只读）、Web2（读-写）和Web3（读-写-拥有）的区别。Web3 里的拥有不仅表示所属权，还有收益权，你有权获得它所带来的收益。听着这像是一个完美世界，这样一个世界离我们又有多远呢？大家可以通过这部小书获得答案。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### iOS 高性能app架构

**地址**：https://github.com/dudongge/iOS_Architecture

该仓库是 [Advanced iOS App Architecture (1st Edition)](https://zh.sg1lib.org/book/5002805/90c154) 的大量机翻译本，对于译文修改了一些错别字，有 pdf 和 word 可以选择。本书主要讨论了在开发 App 的时候，代码在各种架构中的表现和细节的不同，讨论了各种架构的优缺点以及在 iOS 中，这些架构又有何特点和不同。


## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Quiver

**地址**：https://yliansoft.com/#quiver

**软件状态**：免费

**软件介绍**：

`Quiver`是为程序员打造的笔记本。它让您可以在一个笔记中轻松混合文本、代码、`Markdown` 和 `LaTeX`，使用出色的代码编辑器编辑代码，实时预览 `Markdown` 和 `LaTeX`，并通过全文搜索立即找到任何笔记。

包含`MacOS`、`iOS`两端。

![Quiver](http://cdn.zhangferry.com/screenshot1.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 第五十期](https://mp.weixin.qq.com/s/6IS0RlytWxjeRHyh0f2fXA)

[iOS 摸鱼周报 第四十九期](https://mp.weixin.qq.com/s/6GvVh8_CJmsm1dp-CfIRvw)

[iOS摸鱼周报 第四十八期](https://mp.weixin.qq.com/s/vdUy-BqxWzuPcjYO6fFsJA)

[iOS摸鱼周报 第四十七期](https://mp.weixin.qq.com/s/X6lPQ5qwY1epF6fEUhvCpQ)

![](http://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
