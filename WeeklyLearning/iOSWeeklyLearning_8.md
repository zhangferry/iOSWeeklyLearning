# iOS摸鱼周报 第八期

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享大家开发过程遇到的经验教训及学习内容。虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug经历。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips

开发小技巧收录。

### Github的仓库操作需求token验证

今天使用一个旧仓库访问Github时，收到一个Deprecation Notice的邮件，说是基于用户名密码的登录方式之后将不再支持，[官方通告](https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/ "2020-12-15-token-authentication-requirements-for-git-operations")可以看这里。

当前对于放在github的仓库有两种访问方式：用户名密码、Token。

用户名密码就是使用https访问git仓库。

Token是指私有访问（SSH）、OAuth、GitHub App这三种情况。

在**2021年8月13号**之后，github将不再接受用户名密码的访问形式。受影响的流程包含：

* 命令行访问
* 桌面应用访问（Github Desktop不受影响）
* 其他App或者服务使用用户名密码访问直接访问github的情况

不受影响的情况：

* 账号具有双重验证功能、SSH访问
* 使用GitHub Enterprise Server，没有收到Github的更改通知。
* 其他不支持用户名密码访问的Github App

### 配置Entitlements

entitlements是一种授权文件，用于配置相应的操作是否被允许。这个文件会在我们增加Capability的时候自动生成，它的实体是一个plist文件，用于记录我们增加的Capability。打包时entitlements会被放置到MachO文件的Code Signature段中，系统会根据这里的值判断当前应用的权限。

通常一个Target只会有一个entitlements，当如果我们想要根据不同configuration对应不同bundleId时，可能由于某些限制，他们之间的权限能力不同，这时就需要他们拥有不同的entitlements。

我们可以Copy原来的授权文件，重命名，然后在`Build Setting > Signing > Code Signing Entitlements `中配置刚才新增的entitlements文件。

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20210410115024.png)

### would clobber existing tag

在拉取远程tag时会报这种错误，含义是远程tag跟本地有tag冲突。解决方案是找出这个冲突的本地tag，删除掉。

可以通过`git ls-remote -t `和`git tag -l`结果进行比对，也可以直接删除本地仓库，重新拉取。

## 那些Bug

### Swift与OC block的差异

推荐来源：[weiminghuaa](https://github.com/weiminghuaa)

**Bug现象**

原生和web、小程序、flutter等等交互时，传递给原生的是方法名和数据，所以经常需要写方法转发函数，用到performSelector。在OC时，传递block没问题，Swift就不行，可能在performSelector闪退，也可能在block执行的地方闪退

![21617687306_ pic_hd](https://cdn.jsdelivr.net/gh/zhangferry/Images/blog/113679539-738ffb80-96f2-11eb-80e6-4bcdf86e7d78.jpg)

![271617690340_ pic_hd](https://cdn.jsdelivr.net/gh/zhangferry/Images/blog/113679460-5bb87780-96f2-11eb-9afd-9864e239ff38.jpg)

**解决方案**

swift调用performSelector传参之前，将swift的clourse，显示的转换为oc的block

```swift
let block : @convention(block) (Any, Bool) -> () = callback
```

https://stackoverflow.com/questions/26374792/difference-between-block-objective-c-and-closure-swift-in-ios

**Bug解释**

知识点太偏了，难搞。

解题思路记一下：（真正的技术群很关键，讨论才有灵感）
1、刚开始，完全不知所措

2、在开发者群里好友的建议下，分别写了oc和swift的demo，确认oc没问题，swift有问题

3、基于第二点的结果，猜测，swift的closure和oc的block，虽然都是闭包，但毕竟是不同语言，应该是不同实现，大多数情况在项目中通用，但是具体到这里，swift调oc的runtime去传参，把closure传过去，就出问题，无法copy，closure直接在函数结束时销毁了

4、尝试了解block的底层，并了解closure和block的差异，最终找到了可以显示转换的方法

## 编程概念

### 什么是VPS
VPS是Virtual Private Server （虚拟专用服务器）的缩写，它可以将一台物理服务器分割成多个虚拟专享服务器，每个虚拟服务器相互隔离，都有各自的操作系统，磁盘空间及IP地址。使用时VPS就像一台真正的实体服务器，并可以根据用户喜好进行定制。

云服务器跟VPS的概念很像，很多时候他们被混用，但其实还是有区别的。云服务器是VPS的升级版，它不再局限于从一台服务器分离出多个虚拟服务器而是，依托于更先进的集群技术，在一组服务器上虚拟出独立服务器，集群中每个服务器都有云服务器的一个镜像，所以云服务器能保证虚拟服务器的安全与稳定。但如果是VPS，你使用的那台主机发生宕机，你的VPS就无法访问了。

### 什么是Ajax

![image.png](https://cdn.jsdelivr.net/gh/zhangferry/Images/blog/1600421961892-7b7a6af6-c661-4886-a973-857376ff4b05.png)

Ajax是Asynchronous Javascript And XML 的缩写，即异步JavaScript和XML，它是一种提高web应用技术交互性的技术方案。

Ajax可以实现在浏览器和服务器之间的异步（不阻塞用户交互）数据传输，并在数据回传至浏览器时局部更新该内容（页面并没有刷新）。这样的好处是即提高了对用户动作的响应又避免了发送多余无用的信息。

第一个著名的Ajax应用是Gmail。

### 什么是UTF-8
UTF-8（8-bit Unicode Transformation Format）是一种Unicode编码形式。Unicode编码是ISO组织制定的包含全球所有文字，符号的编码规范，它规定所有的字符都使用两个字节表示。这样虽然可以包含全球所有文字，但对于仅处于低字节的英文字符也使用两个字节表示，其实是造成了一定程度的空间浪费，于是就有了UTF-8的编码形式。它是动态的使用1-4个字符表示Unicode编码内容的，英文字符占一个字节，此时同ASCII码，中文字符占三个字节。

UTF-8的编码规则总结如下：

```
Unicode符号范围      |        UTF-8编码方式
(十六进制)           |            （二进制）
--------------------+-------------------------------------
0000 0000-0000 007F | 0xxxxxxx
0000 0080-0000 07FF | 110xxxxx 10xxxxxx
0000 0800-0000 FFFF | 1110xxxx 10xxxxxx 10xxxxxx
0001 0000-0010 FFFF | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
```

这里再强调一下Unicode和UTF-8的区别：**前者是字符集，后者是编码规则**。

UTF-8编码使用非常广泛，在Cocoa编程环境中其作为官方推荐编码方式，在网页端的展示，UTF-8的应用范围也达到了95%左右。

另外两种编码规则UTF-16和UTF-32的最短长度分别为16位和32位，也会造成一部分的字节浪费，所以都没有UTF-8使用更广。

### 什么是响应式
响应式编程（英语：Reactive programming）是一种专注于数据流和变化传递的异步编程范式。面向对象、面向流程都是一种编程范式，他们的区别在于，响应式编程提高了代码的抽象层级，所以你可以只需关注定义了业务逻辑的那些相互依赖的事件，而非纠缠于大量的实现细节。

很多语言都与对应的响应式实现框架，OC：ReactiveCocoa，Swift：RxSwift/Combine，JavaScript：RxJS，Java：RxJava

响应式的关键在于这几点：

数据流：任何东西都可以看做数据流，一次网络请求、一次Click事件、用户输入、变量等。

变化传递：以上这些数据流单独或者组合作用产生了变化，对别的流有了影响，即为变化传递。

异步编程：非阻塞式的，数据流之间互不干涉。

应用示例：假设一个拥有计时器的场景，当用户关闭该页面和退到后台时暂停定时器，当应用回到前台时开启定时器，另外需要有一个地方展示定时器时间。
以下是用RxSwift实现的代码逻辑：

![image.png](https://cdn.jsdelivr.net/gh/zhangferry/Images/blog/1600940093178-769ca39a-5d60-425b-907c-8585a5afd8b0.png)

### 什么是Catalyst

![image.png](https://cdn.jsdelivr.net/gh/zhangferry/Images/blog/1600940194203-0c5d3a70-3794-4731-af22-5b41514c3318.png)

背景：苹果生态中，长期以来，移端和电脑端的App并不通用，开发者必须写两次代码，设计两套UI界面，才能分别为两个平台制作对应的App。这也直接导致了iOS应用百花齐放，macOS应用却凄凄惨惨戚戚。

Mac Catalyst 正是解决这一问题的技术方案，苹果在19年WWDC上发布它，开发者可以将iPad 应用移植到macOS上，之后也会支持iOS应用的移植。它的意义在于我们可以直接使用UIKit开发macOS应用，BigSur上的短信和地图均使用Mac Catalyst重写过。`Write once，run anywhere`是苹果的最终目标。

Mac Catalyst已被集成进了Xcode（11.0版本及之后），在平台选择选项框中找到mac选项，选中即可，Catalyst功能只有在Catalina及之后的系统版本才能使用。

### 什么是DSL

DSL（Domain Specific Language）即特定领域语言，与DSL相对的就是GPL，这里的 GPL 并不是我们知道的开源许可证，而是 General Purpose Language 的简称，即通用编程语言，也就是我们非常熟悉的 Objective-C、Swift、Python 以及 C 语言等等。

DSL是为了解决某一类任务而专门设计的计算机语言，其通过在表达能力上做的妥协换取在某一领域内的高效。

DSL包含外部DSL和内部DSL，外部DSL包括：Regex、SQL、HTML&CSS

内部DSL包括：基于Ruby构建的项目配置，Podfile、Gemfile、Fastfile文件里的语法

参考资料：https://draveness.me/dsl/

## 优秀博客

1、[我离职了](https://juejin.cn/post/6943384976909942815 "我离职了") -- 来自掘金：敖丙

敖丙还在B站录了[视频](https://www.bilibili.com/video/BV1cp4y1a7DW "我离职了 B站")，看视频可能更有感染力。

2、[我的玩具——乐高魔方机器人](http://xelz.info/blog/2017/02/18/lego-cube-solver/ "我的玩具——乐高魔方机器人") -- 来自博客：xelz's blog

这个真的非常有意思，有理工科思维做一件具体有趣的事情非常酷。大概思路是这样的;

- 手机与LEGO通过蓝牙连接
- LEGO检测到魔方放入之后通知手机开始扫描
- 手机扫描完一个面之后，通知LEGO将魔方翻转到下一个面
- 扫描完毕后，手机开始计算还原步骤
- 手机通过蓝牙将还原公式发送给LEGO
- LEGO按照公式将魔方还原

3、[关于bitcode, 知道这些就够了](http://xelz.info/blog/2018/11/24/all-you-need-to-know-about-bitcode/ "关于bitcode, 知道这些就够了") -- 来自博客：xelz's blog

4、[哈啰出行iOS App首屏秒开优化](https://mp.weixin.qq.com/s/5Ez2BrsyBgQ8aHZqlYtAjg "哈啰出行iOS App首屏秒开优化") -- 来自公众号：哈罗技术团队

5、[SwiftUI: Text 中的插值](https://mp.weixin.qq.com/s/PX8bXSFXgJWMgHqien85jQ "SwiftUI: Text 中的插值") -- 来自公众号：老司机技术周报

6、[深入理解MachO数据解析规则](https://mp.weixin.qq.com/s/z8s4urq_KCf2ny5kKOYMHA) -- 来自公众号：iOS成长之路

7、[MacBook 升级 SSD 硬盘指北](https://mp.weixin.qq.com/s/LMeO6chdac65JQu1Yy2-Iw) -- 来自公众号：iOS成长之路

8、[DWARF文件初探——提取轻量符号表](https://mp.weixin.qq.com/s/s8iwQLNtla5nxF_Tmj2wJg "DWARF文件初探——提取轻量符号表") -- 来自公众号：皮拉夫大王在此




## 学习资料

### Can Balkaya

Can Balkaya是WWDC20的学生挑战赛冠军，当前在Medium开了[专栏](https://canbalkaya.blog/ "Can Balkaya")，经常发布一些介绍Swift特性相关的文章，质量都很高。我在别的地方看到有人翻译过里面部分文章，说明它还是有一定关注度的，如果英文稍微好些的可以直接订阅这个专栏来看。

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20210411102014.png)

## 工具推荐

推荐好用的工具。

### Cleaner for Xcode

**推荐来源**：zhangferry

**地址**：https://github.com/waylybaye/XcodeCleaner-SwiftUI

**软件状态**：开源版本免费，AppStore版本$0.99

**使用介绍**

这个应用可以帮助你清除遗留以及废弃文件，从而极大的节省硬盘空间。 你可以每月或者每周运行一次进行清理。

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20210410105340.png)

## JSONExport

**推荐来源**：春起梨花开

**地址**：https://github.com/Ahmed-Ali/JSONExport

**软件状态**：免费，开源

**使用介绍**

支持JSON文件直接导出为开发中使用的Model类型。支持Java，Objective-C，Swift等语言的数据模型。

对于一些适配CoreData、Realm的特殊格式也可以完整适配。

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20210410123533.png)

## 联系我们

[摸鱼周报第三期](https://zhangferry.com/2021/01/10/iOSWeeklyLearning_3/)

[摸鱼周报第四期](https://zhangferry.com/2021/01/24/iOSWeeklyLearning_4/)

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

[摸鱼周报第六期](https://zhangferry.com/2021/03/14/iOSWeeklyLearning_6/)

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/wechat_official.png)
