# iOS摸鱼周报 第七期

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享大家开发过程遇到的经验教训及学习内容。虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug经历。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips

开发小技巧收录。

### 文件夹命名

最近执行shell脚本时，发生了奇怪的问题，很简单的`rm`命令却一直执行出错。看了日志发现是文件路径路径中包含`&`符号，其中某个文件夹的命名带有这个与符号。执行命令时这被作为特殊符号，被拆成了两条命令，导致出错。

所以之后文件或者文件夹命名切记不要用`&`、`|` 这些特殊字符。

### 动态库vs静态库

使用Swift的第三方库的时候我们可以选择静态或者动态库，那它们之间有什么区别呢？可以参考这篇文章

[Static VS dynamic frameworks in Swift: an in-depth analysis](https://acecilia.medium.com/static-vs-dynamic-frameworks-in-swift-an-in-depth-analysis-ff61a77eec65 "Static VS dynamic frameworks in Swift: an in-depth analysis")

测试项目有27个动态库，其中6个是用Carthage集成的，21个是用CocoaPods集成的。把他们全部转成静态库之后，软件Size降低了14.55%，启动时间降低了35%左右，主要是降低了动态库的加载时间，以下是各阶段详细的时间对比：

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20210328160207.png)

这里启动时间降低好理解，大小降低是因为啥呢，是因为静态库时编译器移除了无用的符号表。

因为应用内的动态库，不像系统动态库一样可以供别的App共享，所以它无法起到减少包体的作用。所以通常情况下我们都应该考虑优先使用静态库。

另外静态库可以依赖动态库，但是动态库是不能依赖静态库的。

## 编程概念

### 什么是SSH

SSH是一个网络安全协议，用于计算机之间的加密登录（非对称加密），每台Linux上都安装有SSH。它工作在传输层，能防止中间人攻击，DNS欺骗。它的用法是

```shell
$ ssh user@host
```

host可以是ip地址或者域名，还可以通过-p指定端口号。

ssh登录流程为：

1、远程主机收到用户的登录请求，把自己的公钥发给用户。

2、用户使用这个公钥，将登录密码加密后，发送回来。

3、远程主机用自己的私钥，解密登录密码，如果密码正确，就同意用户登录。


如果不想每次登录时都输密码，可以将本地的公钥发送到远程主机，这样登录过程就变成了：

1、每次远程主机发送一个随机字符串

2、用户用自己的私钥加密

3、远程主机利用公钥解密，如果成功就就同意用户登录。

### 什么是Nginx

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/nginx.png)

Nginx是一款轻量级的Web服务器、反向代理服务器，由于其开源、内存占用少，启动快，高并发能力强，在互联网项目中广泛应用；同时它还是一个IMAP、POP3、SMTP代理服务器，还可以作为反向代理进行负载均衡的实现。

应用场景：在博客站点中，它担任HTTP服务器的作用，通过HTTP协议将服务器上的静态文件（HTML、图片）展现给客户端。

### 什么是负载均衡

负载均衡是一种提高网络可用性的解决方案。当没有负载均衡时，当前服务器宕机或访问量超过服务器上限都会导致网站瘫痪无法访问。负载均衡的解决方案是，设立多台服务器，在访问服务器之前首先经过负载均衡器，由负载均衡器进行分配当前请求应该访问哪一个服务器。既提高了网站瘫痪的容错率又分摊了单个服务器的压力。

负载均衡的实现关键点是如何分配服务器。前置条件是定期检测服务器健康状态，维护一个健康服务器池，然后用一定的算法进行服务器分配，有三种常见分配算法：

轮询：按健康服务器表逐一分配

最小链接：优先选择连接数最少的服务器

Source：根据来源ip地址选择服务器，保证特定用户连接同一服务器

Nginx可以用于实现负载均衡，也提供了以上几种分配算法实现。

### 什么是Apache

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/apache.png)

Apache有多个含义：

一是Apache基金会，它是专门为支持开源软件项目而创办的一个非营利性组织，它所发行的软件都遵循Apache协议。

二是Apache服务器，即httpd，它是Apache团队最早开发的项目，由于它的跨平台和安全性的特点，它成为了世界上最流行的Web服务器软件之一。Apache作为服务器跟Nginx是一样的东西，他们都只支持静态网页，Nginx更轻量，Apache则更稳定。

三是Apache协议（Apache Licence），Apache协议的目的是为了鼓励代码共享，并达到尊重原作者的著作权的作用。你可以使用遵循Apache协议的开源框架并投入商用，但要保留其原有协议声明，如果进行了修改也需要进行说明。

### 什么是Tomcat

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/tomcat.png)

Tomcat是由Apache基金会推出的一款开源的可实现JavaWeb程序的Web服务器框架，它是配置JSP（Java Server Page）和JAVA系统必备的一款环境。

它与Apache服务器的区别在于，Apache只支持静态网页，比如博客网站，而Tomcat支持JSP，Servlet，可以实现动态的web应用，像是图书管管理系统。两者也可以结合，处理既有动态又有静态的网站。

### 什么是Docker 

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20210326231951.png)

理解Docker之前需要知道容器的概念，容器就是一个封闭的开发环境，类似移动端的沙盒，每个沙盒都可以配置不同的程序，甚至相同程序的不同版本，我在沙盒做的操作不会影响别的沙盒程序。

虚拟机也是一种容器，我可以在不同虚拟机的配置里运行不同的程序，他们互不影响。但是虚拟机太占用系统资源了，不同虚拟机占用不同的内核资源，能否把其中一些共性的东西进行共享？当然是可以的，这就是Docker做的事情。

Docker是一家公司，它还做了一个好事情，就是供了很多配置好的镜像资源（一整套的环境搭建），存储在公共的镜像仓库，大大简化了应用的分发，部署流程。


## 优秀博客

[翻译-为什么objc_msgSend必须用汇编实现](http://tutuge.me/2016/06/19/translation-why-objcmsgsend-must-be-written-in-assembly/ "翻译-为什么objc_msgSend必须用汇编实现") -- 来自博客：土土哥的blog

[深度长文：细说iOS代码签名](http://xelz.info/blog/2019/01/11/ios-code-signature/ "深度长文：细说iOS代码签名") -- 来自博客：xelz's blog

[从Mach-O角度谈谈Swift和OC的存储差异](https://www.jianshu.com/p/ef0ff6ee6bc6 "从Mach-O角度谈谈Swift和OC的存储差异") -- 来自简书：皮拉夫大王在此

[一种Swift Hook新思路——从Swift的虚函数表说起](https://www.jianshu.com/p/0cbbbe783ac9 "一种Swift Hook新思路——从Swift的虚函数表说起") -- 来自简书：皮拉夫大王在此

[Swift5.0 的 Runtime 机制浅析](https://juejin.cn/post/6844903889523884039 "Swift5.0 的 Runtime 机制浅析") -- 来自掘金：欧阳大哥2013

[编译原理初学者入门指南](https://mp.weixin.qq.com/s/ZTxVG6KG-4vzbvclC_Q1LQ "编译原理初学者入门指南") -- 来自公众号：腾讯技术工程

[神秘！申请内存时底层发生了什么？](https://mp.weixin.qq.com/s/DN-ckM1YrPMeicN7P9FvXg "神秘！申请内存时底层发生了什么？") -- 来自公众号：码农的荒岛求生

[推荐收藏 | 美团技术团队的书单](https://tech.meituan.com/2020/04/23/read-book-2020-04-23.html "推荐收藏 | 美团技术团队的书单") -- 来自博客：美团技术团队

[青年人在美团是怎样成长的？](https://tech.meituan.com/2020/05/04/meituan-0504-young-people.html "青年人在美团是怎样成长的？") -- 来自博客：美团技术团队


## 学习资料

### 一个人工智能的诞生

地址：https://jibencaozuo.com/product/1/episode/0。

由回形针制作的人工智能交互视频课程，对，可交互的视频，这种可交互性作为学习还是非常棒的。视频质量很高，趣味性也很强。你可以1元体验第一个章节，如果认为很不错，需要支付49元解锁剩余内容。

作者在每个章节都会设计一些问题，答对了才能进到下一章节。前面几节在讲人工智能学习的一些概念和核心数学思想，最后的两个章节属于练习题，我感觉还是有点难的。但课程整体还是很有意思的，如果想了解可以买来看看。下图是课程的目录：

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20210328103223.png)

## 工具推荐

推荐好用的工具。

### P4Merge

**推荐来源**：zhangferry

**地址**：https://www.perforce.com/downloads/visual-merge-tool

**软件状态**：对开发者免费

**使用介绍**

非常强大的可视化diff工具，如果你嫌[Kaleidoscope](https://kaleidoscope.app/)太贵的话，可以用它做代替品。我们可以把它集成进git，通常diff工具有两个作用一个是作为difftool，一个是作为mergetool。配置流程如下：

```shell
# difftool
$ git config --global diff.tool p4merge
$ git config --global difftool.p4merge.cmd \
"/Applications/p4merge.app/Contents/Resources/launchp4merge \$LOCAL \$REMOTE"
# mergetool
$ git config --global merge.tool p4merge
$ git config --global mergetool.p4merge.cmd "/Applications/p4merge.app/Contents/MacOS/p4merge $PWD/$BASE $PWD/$LOCAL $PWD/$REMOTE"
```

以下是作为mergetool的界面，下面内容为最终合并的内容，我们可以通过右侧的扩展按钮选择当前应该选择哪个分支的内容。

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20210327200304.png)

## ProfilesManager

**推荐来源**：[jcexk](https://github.com/jcexk)

**地址**：https://github.com/shaojiankui/ProfilesManager/releases

**软件状态**：免费，开源

**使用介绍**

一款Provisioning Profile管理工具，ProfilesManager特点如下：

1. 方便快捷：支持查看电脑中所有的描述文件
2. 一目了然：通过美化描述文件名，不再是难以辨认的'uuid+ext'格式
3. 功能强大：支持查看ipa中描述文件和info.plist信息
4. 结构清晰：通过树状结构查看描述文件包含的详细信息，如：创建时间、失效时间和包含的移动设备信息等
5. 免费使用：而在App Store上类似功能的软件居然还要收费？？？
6. 可排序和过滤：通过关键词筛选过滤找到想要的文件，也可以通过头部标签排序文件

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20210327112346.png)

## 联系我们

[摸鱼周报第三期](https://zhangferry.com/2021/01/10/iOSWeeklyLearning_3/)

[摸鱼周报第四期](https://zhangferry.com/2021/01/24/iOSWeeklyLearning_4/)

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

[摸鱼周报第六期](https://zhangferry.com/2021/03/14/iOSWeeklyLearning_6/)

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/wechat_official.png)
