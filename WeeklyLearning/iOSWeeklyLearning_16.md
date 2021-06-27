# iOS摸鱼周报 第十六期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 本期话题

[@zhangferry](https://zhangferry.com)：大家好，iOS摸鱼周报不知不觉已经发布到第 16 期啦！为了了解大家对周报的想法和建议，我们做了一次问卷调查，问卷的结果大体上符合预期的设想，有一些好的建议我们也采纳了。所以在上一周我们停更一期做了新内容的准备，本期内容就是改版后的第一期。如果大家后续有什么好的想法和建议，还可以继续给我们留言反馈，希望摸鱼周报能同大家一起进步~

**调整内容**：去掉了`那些Bug`、`编程概念`模块，增加了`本期话题`和`面试解析`。

重点说下`本期话题`模块的作用，我们在调研了各个领域有名气的周报之后，发现了一份独树一帜且跟我们气质相符的周报：阮一峰的科技爱好者周刊。阮一峰的周刊特别之处在于它不仅是在讲科技，还会有每周话题用来讲述生活中的一些思考，比如近几期的话题：“培训班 vs 大学，求职成功率比较”，“你的城市有多少张病床”等。为了让一份技术性周报变的有温度，我认为是需要加入一些人文性质的思考的。

所以我们决定加这个`本期话题`模块，主题来源不仅限于众位联合编辑，也欢迎各位读者跟我们一起探讨问题，或者向我们抛出问题。可以是技术思考，生活感想，读书感悟，职场教训，职业困境等等。之后的`本期话题`会从多个选题里选一个进行探讨，如果问题超出了我们的认知范围，会找认识的其他大佬进行解答。so，对于这个新东西，欢迎大家贡献有趣的话题内容啊~

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### 图片压缩

在 iOS 减包的 Tip 中，我们了解到资源问题是影响包大小的主要部分，而图片资源是开发过程中最常见的。使用正确的图片压缩工具能够有效的进行减包。

#### 有损压缩和无损压缩

常见的压缩工具有 TinyPNG，pngquant，ImageAlpha、ImageOptim、pngcrush、optipng、pngout、pngnq、advpng 等，根据其压缩方式分成两大阵营：有损压缩和无损压缩。

根据资料显示，TinyPNG、pngquant、ImageAlpha、pngnq 都是有损压缩，基本采用的都是 quantization 算法，将 24 位的 PNG 图片转换为 8 位的 PNG 图片，减少图片的颜色数；pngcrush、optipng、pngout、advpng 都是无损压缩，采用的都是基于 LZ/Huffman 的 DEFLATE 算法，减少图片 IDAT chunk 区域的数据。一般有损压缩的压缩率会大大高于无损压缩。

#### 压缩工具

对于项目中常见的背景图、占位图和大的标签图来说，推荐使用以下两种工具

* [TinyPNG4Mac](https://github.com/kyleduo/TinyPNG4Mac)：利用 [tinify](https://tinify.cn) 提供的 API，目前 tinify 的免费版压缩数量是单次不超过 20 张且大小不超过 5M。对于一般的 iOS 应用程序来说，足够日常开发的使用；
* [ImageOptim-CLI](https://github.com/JamieMason/ImageOptim-CLI)：自动先后执行压缩率较高的为 [ImageAlpha](http://pngmini.com/) 的有损压缩 加上 [ImageOptim](https://imageoptim.com/) 的无损压缩。

可以通过查看[这个表格](http://jamiemason.github.io/ImageOptim-CLI/comparison/png/photoshop/desc/ "压缩对比表格")对比 TinyPng 和 ImageOptim-CLI 。

对于小图来说，例如我们常见的 icon 图标来说，我们通过改变其编码方式为 `RGB with palette` 来达到图片压缩效果。你可以使用 ImageOptim 改变图片的编码方式为 `RGB with palette`。

```shell
imageoptim -Q --no-imageoptim --imagealpha --number-of-colors 16 --quality 40-80 ./1.png
```

通过 [Palette Images](http://www.manifold.net/doc/mfd9/palette_images.htm "Palette Images") 深入了解 `palette`。

这里的压缩是指使用 Xcode 自带的压缩功能。

#### Xcode `负优化`

我们一般使用  Assets Catalogs 对图片资源进行管理。其会存在对应的优化方式

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210626221623.png)

在构建过程中，Xcode 会通过自己的压缩算法重新对图片进行处理。在构建 Assets Catalogs 的编译产物 Assest.car 的过程中，Xcode 会使用 `actool` 对  Assets Catalogs  中的 png 图片进行解码，由此得到 Bitmap 数据，然后再运用 actool 的编码压缩算法进行编码压缩处理。所以不改变编码方式的无损压缩方法对最终的包大小来说，可能没有什么作用。

对同一张图片，在不同设备、不同 iOS 系统上 Xcode 采用了不同的压缩算法这也导致了下载时不同的设备针对图片出现大小的区别。

可以利用 `assetutil` 工具分析 `Assest.car` 来得到其具体的压缩方法：

```shell
assetutil --info ***.app/Assets.car > ***.json
```

需要注意 Json 文件中这几个参数的值 `Compression` 、`Encoding`、`SizeOnDisk`。

```json
 {
    "AssetType" : "Image",
    "BitsPerComponent" : 8,
    "ColorModel" : "RGB",
    "Colorspace" : "srgb",
    "Compression" : "deepmap2",
    "Encoding" : "ARGB",
    "Name" : "image",
    "NameIdentifier" : 51357,
    "Opaque" : false,
    "PixelHeight" : 300,
    "PixelWidth" : 705,
    "RenditionName" : "image.png",
    "Scale" : 1,
    "SHA1Digest" : "294FEE01362591334E3C3B4ECE54AF0EA8491781",
    "SizeOnDisk" : 113789,
    "Template Mode" : "automatic"
  }
```

如果启用  APP Thinning 来生成不同设备的 ipa 包，然后针对每个 ipa 包都进行一次解压缩，并获取其中的 Assets.car 导出对应的 assets.json 似乎有些冗余，你也可以利用 [京东商城的 APP 瘦身实践](https://mp.weixin.qq.com/s/xzlFQJ2b-rrw5QIszSLXXQ) 中提及的  `assetutil`  的方法从通用包的 Assets.car 文件导出指定设备的 Assets.car 文件：

```shell
assetutil --idiom phone --subtype 570 --scale 3 --display-gamut srgb --graphicsclass MTL2,2 --graphicsclassfallbacks MTL1,2:GLES2,0 --memory 1 --hostedidioms car,watch xxx/Assets.car -o xxx/thinning_assets.car
```

#### 压缩的`危害`

不要盲目的追求最大的压缩比，既需要考虑压缩出图片的质量，也需要考虑经过 Xcode 最终构成文件的真实大小。

压缩完成的图片尽量在高分辨率的设备上看看会不会有什么问题，让 UI 妹子好好看看，会不会出现噪点、毛边等现象。

如果一个图片经过有损压缩最终导致其在 Assets.car 中 `SizeOnDisk` 值变得很大的话，但其在各个设备上的表现情况又挺好，你可以尝试将其加到 bundle 中使用，并将其图片格式修改为 `Data`，这样 Xcode 就不会对其进行压缩处理了。不过不要忘记将调用方法改为 `imageWithContentOfFile:`。

## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

### 输入网址进入网页按回车刷新网页都发生了什么？URL 输入到显示的过程？

1. **DNS 解析**：当用户输入一个网址并按下回车键的时候，浏览器获得一个域名，而在实际通信过程中，我们需要的是一个 IP 地址，因此我们需要先把域名转换成相应 IP 地址；
2. **TCP 连接**：浏览器通过 DNS 获取到 Web 服务器真正的 IP 地址后，便向 Web 服务器发起 TCP 连接请求，通过 TCP 三次握手建立好连接后，浏览器便可以将 HTTP 请求数据发送给服务器了；
3. **发送 HTTP 请求**：浏览器向 Web 服务器发起一个 HTTP 请求，HTTP 协议是建立在 TCP 协议之上的应用层协议，其本质是在建立起的 TCP 连接中，按照 HTTP 协议标准发送一个索要网页的请求。在这一过程中，会涉及到负载均衡等操作；
4. **处理请求并返回**：服务器获取到客户端的 HTTP 请求后，会根据 HTTP 请求中的内容来决定如何获取相应的文件，并将文件发送给浏览器；
5. **浏览器渲染**：浏览器根据响应开始显示页面，首先解析 HTML 文件构建 DOM 树，然后解析 CSS 文件构建渲染树。如果页面有 JavaScript 脚本文件，那么 JavaScript 文件下载完成并加载后，通过 DOM API 和 CSSOM API 来操作渲染树，等到渲染树构建完成后，浏览器开始布局渲染树并将其绘制到屏幕上；
6. **断开连接**：客户端和服务器通过四次挥手终止 TCP 连接。

### 拥塞控制有哪些阶段？如何实现拥塞控制？TCP 的拥塞控制解释一下？

1. 拥塞控制考虑整个网络，是全局性的考虑；
2. **慢启动算法**：由小到大逐渐增加发送数据量，每收到一个报文确认就加 1 倍的报文数量，以指数规律增长，增长到慢启动阈值后就不增了；
3. **拥塞避免算法**：维护一个拥塞窗口的变量，只要网络不拥塞，就试探着拥塞窗口调大，以加法规律增长，该算法可以保证在网络不拥塞的情况下，发送更多的数据；
4. **快速重传**：接收端收到的序列号不连续时，连发 3 个重复的确认报文给发送方；
5. **快速恢复**：拥塞窗口变为原来的一半，阈值也变为发生拥塞时大小的一半，继续拥塞避免算法。

### TCP 怎么保证可靠传输？TCP 怎样实现可靠传输的？TCP 为什么可以保证可靠传输？怎么理解 TCP 的连接，可靠和字节流？

1. **数据分块**：应用数据被分割成 TCP 认为最适合发送的数据块；
2. **序列号和确认应答**：TCP 给发送的每一个包进行编号，在传输的过程中，每次接收方收到数据后，都会对传输方进行确认应答，即发送 ACK 报文，这个 ACK 报文当中带有对应的确认序列号，告诉发送方成功接收了哪些数据以及下一次的数据从哪里开始发。除此之外，接收方可以根据序列号对数据包进行排序，把有序数据传送给应用层，并丢弃重复的数据；
3. **校验和**：TCP 将保持它首部和数据部分的检验和。这是一个端到端的检验和，目的是检测数据在传输过程中的任何变化。如果收到报文段的检验和有差错，TCP 将丢弃这个报文段并且不确认收到此报文段；
4. **流量控制**：TCP 连接的双方都有一个固定大小的缓冲空间，发送方发送的数据量不能超过接收端缓冲区的大小。当接收方来不及处理发送方的数据，会提示发送方降低发送的速率，防止产生丢包。TCP 通过滑动窗口协议来支持流量控制机制；
5. **拥塞控制**：当网络某个节点发生拥塞时，减少数据的发送；
6. **ARQ 协议**：也是为了实现可靠传输的，它的基本原理就是每发完一个分组就停止发送，等待对方确认。在收到确认后再发下一个分组；
7. **超时重传**：当 TCP 发出一个报文段后，它启动一个定时器，等待目的端确认收到这个报文段。如果超过某个时间还没有收到确认，将重发这个报文段。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`启动优化`

一、[如何实现 iOS App 的冷启动优化](https://juejin.cn/post/6844904085108310024 "如何实现 iOS App 的冷启动优化") -- 来自掘金：FiTeen

工欲善其事，必先利其器。想要优化启动速度首先要了解什么是冷启动，以及冷启动过程中经历了哪些阶段，然后找到可以进行优化的关键点。作者详细介绍了启动的理论知识和检测工具，包括冷启动与热启动的区别，如何查看阶段耗时以及相关概念解读。这是优化启动速度的必备功课，对于想要做启动速度优化相关同学来说，值得学习。

二、[深入探索 iOS 启动速度优化（二进制重排）](https://juejin.cn/post/6844904121896534024 "深入探索 iOS 启动速度优化（二进制重排）") -- 来自掘金：SimonYe

二进制重排原理是，在启动过程中，会调用各种函数，这些函数分布在各个 TEXT 段中且可能是不连续的，此时需要多次 page fault 创建分页，而每页大概 16kb，每次 page fault 都有耗时。如果我们重排二进制，把他们放在一起，减少 page fault 的次数，是不是就可以减少耗时了？作者介绍了二进制重排的理论基础，以及实践流程，还有关于二进制重排的总结，具体二进制重排能提升多少，还得你自己实践。如果想要实践二进制重排，这篇文章将给你帮助。

三、[🐻记录启动速度优化30%的过程](https://juejin.cn/post/6844904151483154445 "🐻记录启动速度优化30%的过程") -- 来自掘金：我是熊大

早期的 Pod 对于 Swift 工程只支持动态库的形式导入，但在 Cocoapods 1.9 中增加了新的特性 `use_frameworks! :linkage => :static` 支持以静态库形式导入，如果你是 Swift 的工程，那么可以试一下。本文还介绍了动态库与静态库的区别。

四、[抖音品质建设 - iOS启动优化《原理篇》]( https://juejin.cn/post/6887741815529832456  "抖音品质建设 - iOS启动优化《原理篇》") -- 来自掘金：字节跳动技术团队

面试官经常问一个问题：从用户点击图标开始，到用户看到第一帧图像，都经历了哪些过程。这篇文章将会给出非常全面的答案。想要做启动优化首先要了解 iOS 在启动时都做了哪些事情。文章首先介绍了一些基础概念，如：启动的种类、dyld、mmap、Page In等。随后介绍了 IPA 的构建流程，透露了如何基于 LLVM 插桩来实现无用代码检测。文章着重介绍了 dyld3 的启动流程。dyld3 都缓存了哪些内容？Rebase & Bind 各自是做什么的？启动终点应该定在哪里？这些内容是面试中常见的问题。

五、[58 同城 App 性能治理实践-iOS 启动时间优化]( https://mp.weixin.qq.com/s/wkK2UBvuUZW3Pf0Yd_3XTA) -- 来自公众号：58技术

这篇文章是 58同城 APP 做启动优化的实践整理。从启动耗时监控到启动治理文章都有介绍。文中介绍了如何横向对比两个 APP 的启动时间、如何进行动态库懒加载实现启动优化、Swift 符号如何收集等方案。对 APP 的启动优化实践有一定的参考意义。


六、[哈啰出行iOS App首屏秒开优化](https://mp.weixin.qq.com/s/5Ez2BrsyBgQ8aHZqlYtAjg) -- 来自公众号：哈啰技术

此篇文章与前两篇文章内容上稍有重叠，但是偏重于介绍图片及动画解码对 APP 启动的影响。本文提供了多个具有参考价值的案例，如：Lottie 框架在同步处理转码时的性能问题。作者提出了 Lottie 处理大图或者关键帧多张的图片阻塞主线程的问题，并给出了相应的处理方式。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### RSSHub

地址：https://docs.rsshub.app/

RSSHub 是一个开源、简单易用、易于扩展的 RSS 生成器，可以给任何奇奇怪怪的内容生成 RSS 订阅源。RSSHub 借助于开源社区的力量快速发展中，目前已适配数百家网站的上千项内容，且可以配合浏览器扩展和移动端的 App 一起使用，同时也欢迎编写你感兴趣的订阅源。

### 中文技术文档的写作规范

地址：https://github.com/ruanyf/document-style-guide

来自阮一峰的中文技术文档的写作规范。编者在各大博客平台看技术文章的时候，经常会为文章的格式所苦恼，严重的情况下甚至导致编者直接关闭该篇文章。实际上中文文案的写作规范不是那么复杂，学十几分钟、练习几篇文章，就能写出得体的文案格式。良好的写作规范既能节约沟通成本，也能提升文章气质，学到就是赚到，是一辈子的财富。另也强力推荐这篇 [中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines#%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%88%E6%8E%92%E7%89%88%E6%8C%87%E5%8C%97 "中文文案排版指北") 做参考。

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

### WWDC

**地址**：https://wwdc.io/ 

**软件状态**：免费，[开源](https://github.com/insidegui/WWDC)

**介绍**

一个开源的非官方 WWDC 视频的应用，其支持视频下载、最高 5 分钟的视频切割、书签功能、iCloud 同步、Chromecast 投屏、画中画功能等等。相比于官方应用来说，其功能只多不少（官方新版的 Developer 应用添加了代码片段预览功能），而且更新比较迅速，已经发展到了 v7.3.3 版本，可以查看 2021 年的 Sessions。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210626230114.png)

### ScreenSize

**地址**：https://www.screensizes.app/

**介绍**

一个在线的 Apple 设备尺寸及设备内各组件的尺寸整理网站，非常之全。这里简要概括下其在 iPhone 设备包含的内容：

* 横竖屏状态的安全区域大小
* 三种 Widget 尺寸的大小
* 标准模式和系统放大模式的尺寸大小
* 各个设备之间的尺寸对比

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210626223430.png)

## 联系我们

[iOS摸鱼周报 第十一期](https://zhangferry.com/2021/05/16/iOSWeeklyLearning_11/)

[iOS摸鱼周报 第十二期](https://zhangferry.com/2021/05/22/iOSWeeklyLearning_12/)

[iOS摸鱼周报 第十三期](https://zhangferry.com/2021/05/30/iOSWeeklyLearning_13/)

[iOS摸鱼周报 第十四期](https://zhangferry.com/2021/06/06/iOSWeeklyLearning_14/)

[iOS摸鱼周报 第十五期](https://zhangferry.com/2021/06/14/iOSWeeklyLearning_15/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)