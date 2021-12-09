# iOS摸鱼周报 第三十五期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：苹果正式开放 AppStore 的 2 个重磅功能：自定义产品页和产品页优化。
> * Tips：设备启动流程的梳理。
> * 面试模块：HTTP/1.0，HTTP/1.1，HTTP/2 有哪些区别？
> * 优秀博客：Swift 相关的几个优秀三方库介绍。
> * 学习资料：计算机教育中缺失的一课（中文版）。
> * 开发工具：myyearwithgit，开启你的年度报告。

## 本期话题

[@iHTCboy](https://ihtcboy.com)：

12 月 8 号，苹果正式开放 AppStore 的 2 个重磅功能：

* Custom product pages（自定义产品页）
* Product page optimization（产品页优化）

默认 App Store Connect 后台是没有这些功能，开发者需要通过 [Updated App Store Submission](https://developer.apple.com/app-store-connect/submission-update/) 页面接受苹果的内测协议后，才能使用这些功能。

具体的功能介绍可以参考苹果文档：[Product Page Optimization](https://developer.apple.com/app-store/product-page-optimization/) 和 [Custom Product Pages](https://developer.apple.com/app-store/custom-product-pages/)。

App Store Connect 后台的操作文档，可以参考：[配置自定产品页](https://help.apple.com/app-store-connect/#/dev3a2998d9f) 和 [产品页优化](https://help.apple.com/app-store-connect/#/dev6aa9d8d7b)。

推荐有推广需求的开发者尝试使用，通过自定义产品页来突出 app 不同的功能和不同用户群体的喜好，通过测试不同图标、商店图和视频的效果，增加 App 的曝光量和提高用户下载意愿等。



## 开发Tips

整理编辑：[zhangferry](zhangferry.com)

### 设备启动流程

我们对 App 的启动流程通常会关注比较多，而忽视设备的启动流程，这次来梳理一下设备的启动流程。设备的启动流程分两类：OS X 和 iOS 等 i系列设备，过程大致如下图所示：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20211209222931.png)

#### 开机

按开机键，激活设备，此时硬件通电，CPU 就可以开始工作了。

#### 启动引导

启动引导即是引导至系统内核的加载。

OS X 通过 EFI 进行引导，EFI 是相对 BIOS 的一种升级版设计，它有多种功能，像是引导加载器、驱动程序等。OS X 中的 `boot.efi` 就是一个引导加载器，由它激活 OS 的内核程序。

i 系列设备没有采用 EFI 的方案，而使用了一种更加注重安全性的设计。i 系列设备内部有一个引导 ROM，这个 ROM 是设备本身的一部分。引导 ROM 会激活 LLB（Low Level Bootloader 底层加载器），LLB 这一步开始就有了签名校验。这一步完成之后会进入 iBoot 阶段。iBoot 是内核的引导加载器，由它来加载内核。

（iOS 系列设备的升级其实还有一个 DFU 升级的流程，为了简化这里略过。）

#### launchd

Launchd 是用户态的第一个进程，由内核直接启动，其 pid=1，位于如下路径，该路径会被硬编码到内核中：

```bash
$ ll /sbin/launchd
-rwxr-xr-x  1 root  wheel   857K Jan  1  2020 /sbin/launchd
```

launchd 的主要任务就是按照预定的设置加载其他启动需要的程序。这类预定的任务分为守护进程（daemon）和代理进程（agent）。

launchd 不仅是负责这些启动必备进程，很多用户使用中的进程，像是我们点击应用图标所创建的进程也是由它处理的。

#### 守护进程 & 代理进程

守护进程是与用户登录无关的程序。代理进程是用户登录之后才加载的程序。

iOS 没有用户登录的概念，所以只有守护进程。这些启动进程会被放到 plist 文件里：

```
/System/Library/LaunchDaemons #系统守护进程plist文件
/System/Library/LaunchAgents  #系统代理进程plist文件
/Library/LaunchDaemons #第三方守护进程plist文件
/Library/LaunchAgents  #第三方代理进程plist文件
~/Library/LaunchAgents #用户自由的代理程序plist文件,用户登录时启动
```

`Finder` 是 OS X 的代理程序，用于提供图形功能，配合 `Dock` 我们就能看到 Mac 的桌面了。

在 iOS 上与之对应的就是 `SpringBoard`，它就是 iPhone 的桌面进程。

到这一步就算是设备启动完成了！

参考：《深入解析 MAC OS X & IOS 操作系统》

## 面试解析

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) 

面试题：HTTP/1.0，HTTP/1.1，HTTP/2 有哪些区别？

### 什么是 HTTP

HTTP（超文本传输协议，HyperText Transfer Protocol）是互联网上应用最为广泛的一种网络协议。其默认使用 80 端口，由 HTTP 客户端发起一个请求，建立一个到服务器指定端口（默认是 80 端口）的 **TCP** 连接。

### HTTP/1.0

老的 HTTP 协议标准是 **HTTP/1.0**，为了提高系统的效率，**HTTP/1.0** 规定浏览器与服务器只保持短暂的连接，每次请求都需要与服务器建立一个 TCP 连接，服务器完成请求处理后立即断开 TCP 连接，服务器不会跟踪客户也不会记录已经请求过的请求。

这就是  **HTTP/1.0** 的两个主要特性：

* 无状态：服务器不跟踪不记录请求过的状态
* 无连接：每次请求都需要建立 TCP 连接

对于 `无状态` 来说，可以通过设置 `cookie` 或 `seesion` 等机制来实现身份校验和状态记录。

影响一个 HTTP 网络请求的因素主要有两个：**带宽**和**延迟**。 当下，网络设施的逐渐完善使得带宽问题得到较好的解决，从而**延迟**成为主要的影响因素。

**HTTP/1.0** `无连接` 特性导致两种了性能缺陷：

* **连接无法复用**

  连接无法复用会导致每次请求都需要进行一次 TCP 连接（即 3 次握手 4 次挥手）和慢启动，降低了网络使用率。

* **队头阻塞**

  在前一个请求响应到达之后下一个请求才能发送，如果前一个阻塞，后面的请求也会阻塞的。这会导致带宽无法被充分利用，以及后续健康请求被阻塞。

### HTTP/1.1

为了消除  **HTTP/1.0** 标准中的歧义内容和提升性能，我们很快的就过渡到了 **HTTP/1.1** 标准，也是当前使用最为广泛的 HTTP 协议 ：

* **默认支持长连接**：在 Header 中新增 `Connection` 参数，其值默认为 `Keep-Alive`。默认保持长连接，数据传输完成后保持 TCP 连接不断开，可以继续使用这个通道传输数据。
  > 默认的服务端的长连接时间是 30S。在 iOS 端的实践过程中会有概率出现下面的错误：
  >
  > > Error Domain=NSURLErrorDomain Code=-1005 "The network connection was lost.
* **HTTP pipeline**：基于长连接的基础，在同一个 TCP 连接上可以传送多个 HTTP 请求和响应，减少了建立和关闭连接的消耗和延迟。管道化可以不等第一个请求响应继续发送后面的请求，但响应的顺序还是按照请求的顺序返回。
* **缓存处理**：相较于 **HTTP/1.0**，**HTTP/1.1** 提供了更为丰富的缓存策略。在 **HTTP/1.0** 中主要是根据 Header 里的 `If-Modified-Since`、`Expires` 来做为判断缓存的标准，**HTTP/1.1** 则引入了诸如 `Entity tag`、`If-Unmodified-Since`、 `If-Match`、 `If-None-Match` 等缓存方式。并且还在 Header 中新增了 `Cache-control` 参数来管理缓存。
* **断点传输**：相较于 **HTTP/1.0** 无法部分返回数据对象，**HTTP/1.1** 在 Header 中新增了两个参数来支持**请求响应分块**，客户端发请求时对应的是 `Range`，服务器端响应时对应的是 `Content-Range`。
* **Host 头处理**： **HTTP/1.0** 认为每台服务器都指向了唯一的 IP 地址，请求消息中的 URL 中并没有主机的信息。在 **HTTP/1.1** 中新增了 Host 头域，能够使不同域名配置在同一个 IP 地址的服务器上。

### HTTP/2

**SPDY 协议是 HTTP/2 协议的基础**。**HTTP/2** 最大的改进就是从**文本协议**转变为**二进制协议**。

* **帧、消息、流和 TCP 连接**：**HTTP/2** 将一个 TCP 连接分为若干个流（`Stream`），每个流中可以传输若干消息（`Message`），每个消息由若干最小的二进制帧（`Frame`）组成。**HTTP/2** 中，每个用户的操作行为被分配了一个流编号（`stream ID`），这意味着用户与服务端之间创建了一个 TCP 通道；协议将每个请求分割为二进制的控制帧与数据帧部分，以便解析。
* **多路复用**：基于二进制分帧，在同一域名下所有访问都是从同一个 TCP 连接中走，HTTP 消息被分解为独立的帧，无序发送，服务端根据标识符和首部将消息重新组装起来。
* **请求优先级**：为了避免多路复用可能会导致关键请求被阻塞，即利用请求优先级完成高优先级请求先处理。
* **HPACK 算法**：**HTTP/2** 引入了头部压缩算法。利用合适的压缩算法来处理消息头的数据。避免了重复 Header 的传输，减小了传输数据的大小。
* **服务端推送（Server Push）**：在 **HTTP/2**  中，服务器可以对客户端的一个请求发送多个响应。

## 优秀博客

整理编辑：[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

1、[适配 SwiftUI 的苹果语言识别封装库 —— SwiftSpeech](https://github.com/Cay-Zhang/SwiftSpeech "@cayZ：适配 SwiftUI 的苹果语言识别封装库 —— SwiftSpeech") -- 来自：cayZ

[@东坡肘子](https://www.fatbobman.com/)：SwiftSpeech 是苹果语音框架的一个封装器，与 SwiftUI 和 Combine 深度集成。只需几行代码就能实现 UI 控制 + 语音识别功能。SwiftSpeech 的作者是一位国人，提供的范例代码很有中国特色。

2、[适用于苹果生态的音频合成、处理分析平台 —— AudioKit](https://github.com/AudioKit/AudioKit "@AudioKit：适用于苹果生态的音频合成、处理分析平台 —— AudioKit") -- 来自：AudioKit

[@东坡肘子](https://www.fatbobman.com/)：AudioKit 是一个由代码库、包、库、算法、应用程序、playgorunds、测试和脚本组成的整个音频开发生态系统，由音频程序员、应用程序开发人员、工程师、研究人员、科学家、音乐家、游戏玩家和编程新手组成的社区建立和使用。AudioKit 提供了丰富的文档和范例，拥有十分活跃的社区。

3、[Swift 编写的相机系统 —— NextLevel](https://github.com/NextLevel/NextLevel "@NextLevel：Swift 编写的相机系统 —— NextLevel") -- 来自：NextLevel

[@东坡肘子](https://www.fatbobman.com/)：NextLevel 最初是一个周末项目，现在已经发展成为一个由相机平台爱好者组成的开放社区。该软件为管理媒体录制、相机界面定制、手势交互定制和 iOS 上的图像流提供基础组件。同样的功能也可以在 Snapchat、Instagram 和 Vine 等应用中找到。NextLevel 提供了用于捕捉 ARKit 视频和照片的组件，并利用了 NextLevel 现有的记录功能和媒体管理。

4、[GPUImage2](https://github.com/BradLarson/GPUImage2 "GPUImage2") -- 来自：GitHub

[@我是熊大](https://github.com/Tliens)：早在 2016 年，GPUImage 就已经被大家知晓，各大图像处理软件，几乎都基于此开发，可以说是一个里程碑意义的开源库，后续作者又写了 Swift 版本 GPUImage2（OpenGL ES）、GPUImage3（Metal）。

5、[神笔马良——基于 Metal 的涂鸦框架](https://me.harley-xk.studio/posts/201805072231 "@Harley：神笔马良——基于 Metal 的涂鸦框架") -- 来自博客：Harley

[@我是熊大](https://github.com/Tliens)：MaLiang 作者是中国人，一个全栈工程师；MaLiang 可以用于开发画板类似的功能，同样也是基于 Metal 开发的，是一个有了 4 年沉淀的开源库，目前 star 1.2k+。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 计算机教育中缺失的一课（中文版）

**地址**：https://missing-semester-cn.github.io/

大学里的计算机课程通常专注于讲授从操作系统到机器学习这些学院派的课程或主题，而对于如何**精通工具**这一主题则往往会留给学生自行探索。在这个系列课程中，会讲授**命令行**、**文本编辑器**、**Git** 提供的多种特性等等。学生在他们受教育阶段以及在他们的未来职业生涯中都会和这些工具朝夕相处。因此，花时间打磨使用这些工具的能力并能够最终熟练地、流畅地使用它们，在计算机教育中也是重要的一个部分。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### myyearwithgit

**地址**：https://github.com/Co2333/myyearwithgit

**软件状态**：开源、免费

**软件介绍**：

看名字大家就知道这个是干啥的，还是配上老王的描述吧：
> 本程序目前支持使用常见 Git 仓库托管提供商以及本地代码仓库进行分析。

![myyearwithgit](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Screenshot.png)


### 往期推荐

[iOS摸鱼周报 第三十六期](https://mp.weixin.qq.com/s/K_JHs1EoEn222huWIoJRmA)

[iOS摸鱼周报 第三十五期](https://mp.weixin.qq.com/s/fCEbYkAPlK0nm7UtLKFx5A)

[iOS摸鱼周报 第三十四期](https://mp.weixin.qq.com/s/P0HjLDCIM3T-hAgQFjO1mg)

[iOS摸鱼周报 第三十三期](https://mp.weixin.qq.com/s/nznnGmBsqsrWcvZ4XFMttg)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
