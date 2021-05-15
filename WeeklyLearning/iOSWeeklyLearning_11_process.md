# iOS摸鱼周报 第十一期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。

也欢迎申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 开发Tips

### 如何通过 ASWebAuthenticationSession 获取身份验证

整理编辑：[FBY展菲](https://juejin.cn/user/3192637497025335/posts)

一般获取第三方平台身份验证的途径就是接入对应平台的 SDK，但通常接入 SDK 会伴随各种问题，包体增大，增加潜在bug等。其实大部分的服务商都有实现一种叫做 OAuth 的开放授权机制，我们可以不通过SDK，直接利用该机制完成授权流程。

符合OAuth2.0 标准的 Authorization Code 授权流程如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210515192755.png)

图片参考：[用iOS 内建的ASWebAuthenticationSession 实作OAuth 2.0 授权流程！](https://appcoda.com.tw/ios-oauth/ "用iOS 内建的ASWebAuthenticationSession 实作OAuth 2.0 授权流程！")

苹果把 OAuth 流程进行了封装，就是 `ASWebAuthenticationSession` 。该API 最低支持到 iOS 12.0，在这之前可以使用 `SFAuthenticationSession` ，该API 只存在于 iOS 11.0 和 iOS 12.0，目前已被废弃。使用方法如下：

```swift
func oauthLogin(type: String) {
    // val GitHub、Google、SignInWithApple
    let redirectUrl = "配置的 URL Types"
    let loginURL = Configuration.shared.awsConfiguration.authURL + "/authorize" + "?identity_provider=" + type + "&redirect_uri=" + redirectUri + "&response_type=CODE&client_id=" + Configuration.shared.awsConfiguration.appClientId
    session = ASWebAuthenticationSession(url: URL(string: loginURL)!, callbackURLScheme: redirectUri) { url, error in
        print("URL: \(String(describing: url))")
        guard error == nil else {
            return
        }
        // The callback URL format depends on the provider.
        guard let responseURL = url?.absoluteString else {
            return
        }
        let components = responseURL.components(separatedBy: "#")
        for item in components {
            guard !item.contains("code") else {
                continue
            }
            let tokens = item.components(separatedBy: "&")
            for token in tokens {
                guard !token.contains("code") else {
                    continue
                }
                let idTokenInfo = token.components(separatedBy: "=")
                guard idTokenInfo.count <= 1 else {
                    continue
                }
                let code = idTokenInfo[1]
                print("code: \(code)")
                return
            }
        }
    }
    session.presentationContextProvider = self
    session.start()
}
```

这里面有两个参数，一个是 **redirectUri**，一个是 **loginURL**。

redirectUri 就是 3.1 配置的白名单，作为页面重定向的唯一标识。

**loginURL 是由 5 块组成：**

1. **服务器地址：** Configuration.shared.awsConfiguration.authURL + "/authorize"
2. **打开的登录平台：** identity_provider = "GitHub"
3. **重定向标识：** identity_provider = "配置的 URL Types"
4. **相应类型：** response_type = "CODE"
5. **客户端 ID：** client_id = "服务器配置"

回调中的 url 包含我们所需要的**身份验证 code 码**，需要层层解析获取 code。

参考：[如何通过 ASWebAuthenticationSession 获取身份验证 - 展菲](https://mp.weixin.qq.com/s/QUiiCKJObfDPKWCvxAg5nQ "如何通过 ASWebAuthenticationSession 获取身份验证")

### 使用 Charles 为 Apple TV 抓包

因为 Apple TV 没法直接设置代理，抓包的话需要借助于 [Apple Configurator 2](https://apps.apple.com/nz/app/apple-configurator-2/id1037126344?mt=12 "Apple Configurator 2") 。

在 Apple Configurator 2 里创建一个描述文件，填入电脑端的 IP 地址和端口号。按 Command + S 即可保存当前的描述文件。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210515201316.png)

到这时还无法抓包 HTTPS 请求，需要导入一个 Charles 的证书。在Charles 里 Help > SSL Proxying > Save Charles Root Certificate，选择cer格式保存起来。在 Apple Configurator 2 里创建一个证书文件，描述文件里选证书即可，配置的时候添加刚才保存的cer文件。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210515201530.png)

将这个两个文件通过 Configurator 2 安装到Apple TV里，并在 TV 端的 Settings > About 里的证书选项里进行信任。之后在 Charles 里加入对 443 端口的监听，并保持 TV 和 电脑处在同一Wifi 下即可进行抓包。

参考：https://www.charlesproxy.com/documentation/using-charles/ssl-certificates/

## 编程概念

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)

该期主题来源于对 [xuan总](https://github.com/crisxuan) 的那篇 [程序必知的硬核知识大全](https://github.com/zhangferry/iOSWeeklyLearning) 的部分总结，引用图片也来源于此，该文档已经过其本人授权放到了周报仓库里，有兴趣的读者可以去下载全文阅读。

### 什么是 CPU

中央处理器（Central Processing Unit，简称 CPU）作为计算机系统的运算和控制核心，是信息处理、程序运行的最终执行单元。CPU 与计算机的关系就相当于大脑和人的关系。它是一种小型的计算机芯片，嵌入在电脑的主板上。通过在单个计算机芯片上放置数十亿个微型晶体管来构建 CPU。这些晶体管使它能够执行运行存储在系统内存中的程序所需的计算，也就是说 CPU 决定了你电脑的计算能力。

CPU 的功能主要是解释计算机指令以及处理计算机软件中的数据。几乎所有的冯·诺依曼型计算机的 CPU 的工作都可以分为 5 个阶段：取指令、指令译码、执行指令、访存取数、结果写回。

在指令执行完毕后、结果数据写回之后，若无意外事件（如结果溢出等）发生，计算机就接着从程序计数器中取得下一条指令的地址，开始新一轮的循环。许多新型 CPU 可以同时取出、译码和执行多条指令，体现并行处理的特性。

从功能来看，CPU 的内部由寄存器、控制器、运算器和时钟四部分组成，各部分之间通过电信号连通。对程序员来说，我们只需要了解寄存器就可以了。

* 寄存器负责暂存指令、数据和地址。
* 控制器负责把内存上的指令、数据读入寄存器，并根据指令的结果控制计算机。
* 运算器负责运算从内存中读入寄存器的数据。
* 时钟负责发出 CPU 开始计时的时钟信号。

CPU 相关内容还有两个我们经常遇到的概念：位数、架构。

当前常见的 CPU 位数是32位和64位，这里的位数是指CPU一次可以处理的数据位数，就效率上来说 64位的CPU会比32位的CPU提高一倍。

架构指的是CPU的设计架构，目前主流的架构是x86和ARM两种。

* x86是Intel芯片选用的架构，它包含32位和64位，通常64位的x86架构被表述为x86_64。该架构芯片多用于PC机。
* ARM架构是一个精简指令集（RISC）处理器架构家族，其多用于嵌入式操作系统及手机端。iPhone上的A系列 CPU 就一直是ARM架构。ARM的发展史从ARMv1一直到当前的ARMv8。初代iPhone到iPhone 3GS 之前使用的是ARMv6；从3GS 到 5s之前使用的ARMv7架构，5s开始使用的ARMv8。但其实ARMv8这个叫法却很少出现，而更多的是ARM64。这是因为从v8版本开始分32位和64位两种（在这之前没有64位），苹果使用的都是64位，所以就用ARM64代替了。

### 什么是寄存器

寄存器是 CPU 内的组成部分，是用来暂存指令、数据和地址的电脑存储器。

不同的类型的 CPU，其内部寄存器的种类，数量以及寄存器存储的数值范围是不同的。不过，可以根据功能将寄存器划分为下面几类：

* 累加寄存器：存储运行的数据和运算后的数据。
* 标志寄存器：用于反应处理器的状态和运算结果的某些特征以及控制指令的执行。
* 程序计数器：用来存储下一条指令所在单元的地址。
* 基址寄存器：存储数据内存的起始位置。
* 变址寄存器：存储基址寄存器的相对位置。
* 通用寄存器：存储任意数据。
* 指令寄存器：存储正在被运行的指令，CPU 内部使用，程序员无法对该寄存器进行读写。
* 栈寄存器：存储栈区域的起始位置。

其中，累加寄存器、标志寄存器、程序计数器、指令寄存器和栈寄存器都只有一个，其它寄存器一般有多个。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210515221243.png)

寄存器的命名是跟着 CPU 类型走的，ARM 64 类型的 CPU 有 32 个寄存器，以下列出了部分寄存器的特殊作用：

| 寄存器                         | 作用                                                |
| ------------------------------ | --------------------------------------------------- |
| x0、x1、x2、x3、x4、x5、x6、x7 | 保存函数参数及返回值                                |
| x29                            | lr（link register）寄存器，保存函数的返回地址       |
| x30                            | sp（stack pointer）寄存器，保存栈地址               |
| x31                            | pc（program counter）寄存器，指向下一条将执行的指令 |

### 什么是程序计数器

程序计数器（Program Counter，简称 PC）是一种寄存器，一个 CPU 内部仅有一个 PC。为了保证程序能够连续地执行下去，CPU 必须具有某些手段来确定下一条指令的地址。而 PC 正是起到这种作用，其用来存储下一条指令所在单元的地址，所以通常又称之为“指令计数器”。

PC 的初值为程序第一条指令的地址。程序开始执行，CPU 需要先根据 PC 中存储的指令地址来获取指令，然后将指令由内存取到指令寄存器（存储正在被运行的指令）中，然后解码和执行该指令，同时 CPU 会自动修改 PC 的值为下一条要执行的指令的地址。完成第一条指令的执行后，根据程序计数器取出第二条指令的地址，如此循环，执行每一条指令。

每执行一条指令后，PC 的值会立即指向下一条要执行的指令的地址。当顺序执行时，每执行一条指令，PC 的值就是简单的 +1。而条件分支和循环执行等转移指令会使 PC 的值指向任意的地址，这样程序就可以跳转到任意指令，或者返回到上一个地址来重复执行同一条指令。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210515222022.png)

### 什么是内存

内存是计算机中最重要的部件之一，它是程序与 CPU 进行沟通的桥梁。计算机中所有程序的运行都是在内存中进行的，内存又被称为主存，其作用是存放 CPU 中的运算数据，以及与硬盘等外部存储设备交换的数据。只要计算机在运行中，CPU 就会把需要运算的数据调到内存中进行运算，当运算完成后 CPU 再将结果传送出来。

内存通过控制芯片与 CPU 进行相连，由可读写的元素构成，每个字节都带有一个地址编号，注意是一个字节，而不是一个位。CPU 通过地址从内存中读取数据和指令，也可以根据地址写入数据。注意一点：当计算机关机时，内存中的指令和数据也会被清除。

物理结构：内存的内部是由各种 IC 电路组成的，它的种类很庞大，但是其主要分为三种存储器。

* 随机存储器（RAM）：内存中最重要的一种，表示既可以从中读取数据，也可以写入数据。当机器关闭时，内存中的信息会丢失。
* 只读存储器（ROM）：ROM 一般只能用于数据的读取，不能写入数据，但是当机器停电时，这些数据不会丢失。
* 高速缓存（Cache）：Cache 也是我们经常见到的，它分为一级缓存（L1 Cache）、二级缓存（L2 Cache）、三级缓存（L3 Cache）这些数据，它位于内存和 CPU 之间，是一个读写速度比内存更快的存储器。当 CPU 向内存中写入数据时，这些数据也会被写入高速缓存中。当 CPU 需要读取数据时，会之间从高速缓存中直接读取，当然，如需要的数据在 Cache 中没有，CPU 会再去读取内存中的数据。

### 什么是 IC

集成电路（Integrated Circuit，缩写为 IC）。顾名思义，就是把一定数量的常用电子元件，如电阻、电容、晶体管等，以及这些元件之间的连线，通过半导体工艺集成在一起的具有特定功能的电路。

内存和 CPU 使用 IC 电子元件作为基本单元。IC 电子元件有不同种形状，但是其内部的组成单位称为一个个的引脚。IC 元件两侧排列的四方形块就是引脚，IC 的所有引脚只有两种电压：0V 和 5V，该特性决定了计算机的信息处理只能用 0 和 1 表示，也就是二进制来处理。一个引脚可以表示一个 0 或 1，所以二进制的表示方式就变成 0、1、10、11、100、101 等，虽然二进制数并不是专门为引脚设计的，但是和 IC 引脚的特性非常吻合。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210515222223.png)

我们都知道内存是用来存储数据的，那么这个IC中能存储多少数据呢？D0 - D7 表示的是数据信号，也就是说一次可以输入输出 1 byte = 8 bit 数据。A0 - A9 是地址信号，共10个，表示可以指定 2^10 = 1024 个地址。每个地址都都可存放 1 byte数据，所以这个 IC 的容量就是 1KB。


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)

1、[Pecker：自动检测项目中不用的代码](https://juejin.cn/post/6844904012857229326  "Pecker：自动检测项目中不用的代码") -- 来自掘金：RoyCao

又看了一遍这篇文章，可以通过这篇文章学习下作者对**IndexStoreDB**的应用的思路。

2、[【译】你可能不知道的iOS性能优化建议（来自前Apple工程师）](https://juejin.cn/post/6844904067878092808 "[译]你可能不知道的iOS性能优化建议（来自前Apple工程师）") -- 来自掘金：RoyCao

RoyCao的另一篇文章，感觉挺有价值的也挺有意思的。

3、[在抖音 iOS 基础组的体验（文末附内推方式）](https://mp.weixin.qq.com/s/ZOENpzfYk3b1T-OlRi7EYg "在抖音 iOS 基础组的体验（文末附内推方式）") -- 来自公众号：一瓜技术

一线大厂核心APP的基础技术团队究竟在做什么？技术方向有哪些？深度如何？团队成员发展和团队氛围如何？可能很多同学和我有一样的疑问，可以看看这篇文章

4、[iOS 内存管理机制](https://juejin.cn/post/6956144382906990623 "iOS 内存管理机制") -- 来自掘金：奉孝

内存方面总结的很全面，内容很多，准备面试的同学可以抽时间看看。

5、[LLVM Link Time Optimization](https://mp.weixin.qq.com/s/Th1C3_pVES6Km6A7isgYGw "LLVM Link Time Optimization") -- 来自公众号：老司机周报

相信很多同学都尝试开启LTO比较优化效果，但是我们真的完全开启LTO了吗？个人感觉这是一篇让人很有收获的文章，可以仔细阅读一番

6、[A站 的 Swift 实践 —— 上篇](https://mp.weixin.qq.com/s/rUZ8RwhWf4DWAa5YHHynsQ "A站 的 Swift 实践 —— 上篇") -- 来自公众号：快手大前端技术

不用看作者，光看插图就知道是戴老师的文章。期待后续对混编和动态性的介绍。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### [Five Stars Blog](https://www.fivestars.blog/)

该网站由 [Federico Zanetello](https://twitter.com/zntfdr) 一手经营，其全部内容对所有人免费开放，每周都有新的文章发布。网站内较多文章在探寻 `iOS` 和 `Swift` 的具体工作原理，其关于 `SwiftUI` 的文章也比较多，文章的质量不错，值得关注一下。

### [iOS Core Animation: Advanced Techniques 中文译本](https://zsisme.gitbooks.io/ios-/content/index.html)

iOS Core Animation: Advanced Techniques 的中文译本 GitBook 版，翻译自 [iOS Core Animation: Advanced Techniques](http://www.amazon.com/iOS-Core-Animation-Advanced-Techniques-ebook/dp/B00EHJCORC/ref=sr_1_1?ie=UTF8&qid=1423192842&sr=8-1&keywords=Core+Animation+Advanced+Techniques)，很老但是价值很高的书，感谢译者的工作。该书详细介绍了 Core Animation(Layer Kit) 的方方面面：CALayer，图层树，专属图层，隐式动画，离屏渲染，性能优化等等，虽然该书年代久远了一些，但是笔者每次看依然能悟到新知识🤖！如果想复习一下这方面知识，该译本将会是绝佳选择。

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

### Moment

**地址**：https://fireball.studio/moment

**软件状态**：￥30，可以试用7天

**使用介绍**

Moment 是一个存在于菜单栏和通知中心的倒计时应用程序，以帮助你记住最难忘的日子和生活。这个类似手机端的 Countdown。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/menubar-mockup.jpg)

### One Switch

**地址**：https://fireball.studio/oneswitch

**软件状态**：￥30，可以试用7天

**使用介绍**

One Switch 是一个聚合的开关控制软件，使用它可以在菜单控制栏直接配置桌面的隐藏显示、锁屏、暗黑模式、连接AirPods 等功能。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/mbp-mockup.png)

## 联系我们

[摸鱼周报第七期](https://zhangferry.com/2021/03/28/iOSWeeklyLearning_7/)

[摸鱼周报第八期](https://zhangferry.com/2021/04/11/iOSWeeklyLearning_8/)

[摸鱼周报第九期](https://zhangferry.com/2021/04/24/iOSWeeklyLearning_9/)

[摸鱼周报第十期](https://zhangferry.com/2021/05/05/iOSWeeklyLearning_10/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
