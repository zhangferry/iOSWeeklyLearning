# iOS 摸鱼周报 第四十二期

![](http://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：2022年1月31号之后提交的应用需提供账号删除功能。
> * Tips：openssh 8.8 默认禁用 ssh-rsa 加密算法导致 git 验证失效。
> * 面试模块：如何治理 OOM。
> * 优秀博客：一些优秀开发者的年终总结。
> * 学习资料：程序员考公指南；Vim 从入门到精通（中文）。
> * 开发工具：摸鱼单词，专注于利用碎片时间学习记忆英语单词。

## 本期话题

### 2022年1月31号之后提交的应用需提供账号删除功能

内容如题，该项要求是 2021 年 10 月 6 号提出的，主要目的是加强苹果生态的隐私保护。在 App Store 审核指南的 5.1.1 条款第 v 条更新了这句话：

> If your app supports account creation, you must also offer account deletion within the app.

但对于如何设置该功能，苹果并没有明确的要求。如果删除用户账号，应用端可以根据相关法律继续保留用户信息，但这需要在隐私政策中进行说明所采集用户数据的内容和保留策略。

[Account deletion within apps required starting January 31](https://developer.apple.com/news/?id=mdkbobfo "Account deletion within apps required starting January 31")

## 开发 Tips

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### openssh 8.8 默认禁用 ssh-rsa 加密算法导致 git 验证失效

问题源自于最近无意间在工作机上升级了 openssh 版本（后续才发现是版本问题），导致所有基于 ssh 方式的 git 操作全部失效；

`git pull` 一直提示请输入密码，在我输入了无数次个人 gitlab 密码仍然失败后，第一直觉是我的 ssh 密钥对出了问题，重新生成并上传了新的公钥，还是同样的提示；

使用 `ssh -vT` 命令查看了详细的日志信息，最终发现了问题所在。在解析日志之前，这里先了解一下简化的 ssh 密钥登录的原理。

#### SSH 登录原理

我们都知道 ssh 是基于非对称加密的一种通信加密协议，常用于做登录校验，

一般支持两种方式：**口令登录和公钥登录**；由于篇幅问题这里只介绍公钥的简化流程，该登录流程分为两部分：

**生成会话密钥**

- 客户端和服务端互相发送 ssh 协议版本以及 openssh 版本，并约定协议版本
- 客户端和服务端互相发送支持的加密算法并约定使用的算法类型
- 服务端生成非对称密钥，并将公钥以及公钥指纹发送到客户端
- 客户端和服务端分别使用 DH 算法计算出会话密钥，后续所有流程都会使用会话密钥加密传输

**验证阶段**

- 如果是公钥登录，则会将客户端将公钥指纹信息，使用上述的会话密钥加密发送到服务端
- 服务端拿到后解密，并去 authorized_keys 中匹配对应的公钥，生成一个随机数，使用该客户端公钥加密后发送到客户端
- 客户端使用自己的私钥解密，获取到随机数，使用会话密钥对随机数加密，并做 MD5 生成摘要发送给服务端
- 服务端对原始随机数也使用会话密钥加密后计算 MD5，对比两个值是否相等决定是否登录

> 常说的 ssh 只是一种抽象的协议标准的，实际开发中我们使用的是开源 openssh 库，该库是对 ssh 这一抽象协议标准的实现

以上是 ssh 协议登录校验的流程概要，我们了解到在验证阶段会用到客户端的公钥，openssh 会判断公钥生成算法类型，由于不再支持 ssh-rsa，publickey 方式失败后会尝试使用口令登录方式，这也是一直提示我们输入密码的原因。

具体可以通过日志查看，针对日志做了简化，部分内容做了注释，你也可以对照自己的 log 日志查看更详细的过程

```bash
ssh -vT git@github.com

# 日志如下
# 版本信息
OpenSSH_8.8p1, OpenSSL 1.1.1m  14 Dec 2021 
# 读取配置文件
debug1: Reading configuration data /Users/clownfish/.ssh/config
debug1: Reading configuration data /usr/local/etc/ssh/ssh_config
...
# 查找身份文件, 成功返回 0, 失败返回 -1, 由于本地只有默认的 id_ras 所以只有这一项返回 0
debug1: identity file /Users/clownfish/.ssh/id_rsa type 0
debug1: identity file /Users/clownfish/.ssh/id_rsa-cert type -1
...

# 版本号
debug1: Local version string SSH-2.0-OpenSSH_8.8
debug1: Remote protocol version 2.0, remote software version OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.8
...
# 查找到host
debug1: Found key in /Users/clownfish/.ssh/known_hosts:5

debug1: Will attempt key: /Users/clownfish/.ssh/id_rsa RSA SHA256:7KTOiN2jUDgc5SJm22GnEk5TpshjTBk/lU9stwJYx48
... # Will attempt key 尝试其他类型密钥

# 认证支持两种方式, 公钥和口令
debug1: Authentications that can continue: publickey,password
debug1: Next authentication method: publickey
debug1: Offering public key: /Users/clownfish/.ssh/id_rsa RSA SHA256:7KTOiN2jUDgc5SJm22GnEk5TpshjTBk/lU9stwJYx48
# 针对上文找到的 public key 没有相互支持的签名算法
debug1: send_pubkey_test: no mutual signature algorithm
... # Trying private key 尝试其他私有 key
# 尝试口令登录
debug1: Next authentication method: password
... # 一直提示输入密码
```

找到关键字 **no mutual signature supported**。去查了一下，发现是 **openssh 8.8 版本问题不再支持 ssh-rsa**，
openssh 8.8 release notes 中说明默认会自动转换，但是链接到版本较低的 server 时（从日志中可以看到我们 serve r的版本是 6.6），还是要手工处理。

#### 解决方案

那么解决办法也就有了，要么重新生成其他算法的秘钥对上传，要么修改配置再次开启支持，这里只针对第二种。在 config 中做如下配置：

```
Host * # 第一行说明对所有主机生效
  PubkeyAcceptedKeyTypes=+ssh-rsa # 第二行是将 ssh-rsa 加允许使用的范围，没配置会提示 no mutual signature supported.表示找不到匹配的签名算法
  # HostKeyAlgorithms +ssh-rsa # 第三行是指定所有主机使用的都是 ssh-rsa 算法的 key，我个人测试可以不写，如果仍不生效可以打开测试
```

再次测试发现可以正常登录。另外开头提到的，提示输入的密码，其实应该是登录服务器 git 用户的密码，而不是指的 gitlab 中的个人账号密码；
因为 git 使用 ssh 目的仅仅是登录校验，而不用于访问数据，由于个人对 server 端了解的较少，所以在这里也坑了很久，希望了解的同学多多指教。

* [解决Openssh8.8后ssh-rsa算法密钥对校验失效问题](https://juejin.cn/post/7055116684335513631/ "解决Openssh8.8后ssh-rsa算法密钥对校验失效问题")
* [OpenSSH Release Notes](https://www.openssh.com/releasenotes.html "OpenSSH Release Notes")

## 面试解析

整理编辑：[zhangferry](https://zhangferry.com)

### 如何治理 OOM

OOM（Out Of Memory）指的是应用内存占用过高被系统强制杀死的情况，通常还会再分为 FOOM （前台 OOM） 和 BOOM （后台 OOM）两种。其中 FOOM 现象跟常规 Crash 一样，对用户体验影响比较大。

OOM 产生的原因是应用内存占用过高，治理方法就是降低内存占用，这可以分两部分进行：

1、现存代码：问题检测，查找内存占用较大的情况进行治理。

2、未来代码：防裂化，对内存使用进行合理的规范。

#### 问题检测

OOM 与其他 Crash 不同的一点是它的触发是通过 `SIGKILL` 信号进行的，常规的 Crash 捕获方案无法捕获这类异常。那么该如何定位呢，线下我们可以通过 Schems 里的 Memory Management，生成 memgraph 文件进行内存分析，但这无法应用到线上环境。目前主流的线上检测 OOM 方案有以下几个：

**FBAllocationTracker**

由 Facebook 提出，它会 hook OC 中的 `+alloc` 和 `+ dealloc` 方法，分别在分配和释放内存时增加和减少实例计数。

```objectivec
@implementation NSObject (AllocationTracker)

+ (id)fb_newAlloc
{
 id object = [self fb_originalAlloc];
 AllocationTracker::tracker()->incrementInstanceCountForClass([object class]);
 return object;
}

- (void)fb_newDealloc
{
 AllocationTracker::tracker()->decrementInstanceCountForClass([object class]);
 [self fb_originalDealloc];
}
@end
```

然后，当应用程序运行时，可以定期调用快照方法来记录当前活动的实例数。通过实例数量的异常变化来定位发生OOM的问题。

该方案的问题是无法检测非 OC 对象的内存占用，且没有堆栈信息。

参考：[Reducing FOOMs in the Facebook iOS app](https://engineering.fb.com/2015/08/24/ios/reducing-fooms-in-the-facebook-ios-app/ "Reducing FOOMs in the Facebook iOS app")

**OOMDetector**

这个是腾讯采用的方案。

通过 Hook iOS 系统底层内存分配的相关方法（包括 `malloc_*zone`相关的堆内存分配以及 `vm*_allocate` 对应的 VM 内存分配方法），跟踪并记录进程中每个对象内存的分配信息，包括分配堆栈、累计分配次数、累计分配内存等，这些信息也会被缓存到进程内存中。在内存触顶的时候，组件会定时 Dump 这些堆栈信息到本地磁盘，这样如果程序爆内存了，就可以将爆内存前 Dump 的堆栈数据上报到后台服务器进行分析。

![](http://cdn.zhangferry.com/Images/20220119232138.png)

参考：[【腾讯开源】iOS爆内存问题解决方案-OOMDetector组件](https://juejin.cn/post/6844903550187733000 "【腾讯开源】iOS爆内存问题解决方案-OOMDetector组件")

**Memory Graph**

这个是字节采用的方案，基于内存快照生成内存分布情况。线上 Memory Graph 核心的原理是扫描进程中所有 Dirty 内存，通过内存节点中保存的其他内存节点的地址值建立起内存节点之间的引用关系的有向图，用于内存问题的分析定位，整个过程不使用任何私有 API。该方案实现细节未开源，目前已搭载在字节跳动火山引擎旗下应用性能管理平台（[APMInsight](https://www.volcengine.com/product/apminsight "APMInsight")）上，供开发者注册使用。

![](http://cdn.zhangferry.com/Images/20220120225034.png)

[有一篇文章](https://juejin.cn/post/6895583288451465230 "分析字节跳动解决OOM的在线Memory Graph技术实现")分析了这个方案的实现原理：通过 mach 内核的 `vm_*region_recurse/vm_region_recurse64` 函数遍历进程内所有 VM Region。这里包括二进制，动态库等内存，我们需要的是 Malloc Zone，然后通过 `malloc*_get_all_zones` 获取 libmalloc 内部所有的 zone，并遍历每个 zone 中管理的内存节点，获取 libmalloc 管理的存活的所有内存节点的指针和大小。再根据指针判断是 OC/Swift 对象，还是 C++ 对象，还是普通的 Buffer。

参考：[iOS 性能优化实践：头条抖音如何实现 OOM 崩溃率下降50%+](https://juejin.cn/post/6885144933997494280 "iOS 性能优化实践：头条抖音如何实现 OOM 崩溃率下降50%+")

#### 防劣化

防劣化即防止出现 OOM 的一些手段，可以从以下方面入手：

- 内存泄漏：关于内存泄漏的检测可以见[上期内容](https://mp.weixin.qq.com/s/DNXrfZgx0JaXyvfVZ4sYVA)。
- autoreleasepool：在循环里产生大量临时对象，内存峰值会猛涨，甚至出现 OOM。适当的添加 autoreleasepool 能及时释放内存，降低峰值。
- 大图压缩：可以降低图片采样率。
- 前后台切换：后台更容易发生 OOM，因为后台可利用的内存更小，我们可以在进入后台时考虑释放一些内存。

## 优秀博客

整理编辑：[我是熊大](https://juejin.cn/user/1151943916921885)

1、[2021 年终总结](https://onevcat.com/2021/12/2021-final/ "2021 年终总结") -- 来自博客：王巍 (onevcat)

[@我是熊大](https://github.com/Tliens)：王巍，拥有知名开源库 Kingfisher，创办了网站 [ObjC CN](https://objccn.io/)，是 iOS 开发者重点关注对象。

2、[大厂逃离后上岸人员的年终总结](https://juejin.cn/post/7047809990916046862 "大厂逃离后上岸人员的年终总结") -- 来自掘金：东方赞

[@我是熊大](https://github.com/Tliens)：工作不卷，生活要开心，收入稳中有升。

3、[下一个五年计划起航 ！](https://halfrost.com/halfrost_2020/ "下一个五年计划起航 ！") -- 来自博客：halfrost

[@我是熊大](https://github.com/Tliens)：霜神是前阿里巴巴资深后端工程师，iOS 开发届的大佬级别人物，这是 2020 的年终总结，来的更晚一些。

4、[【年度总结】2021年度总结](https://blog.yuusann.com/corpus/article/21021 "【年度总结】2021年度总结") -- 来自博客：郑宇琦

[@我是熊大](https://github.com/Tliens)：郑宇琦，LinkedIn 高级研发工程师，曾就职于百度，作者过去一年的经历十分丰富，生活不止有 coding。

5、[2020年我阅读了87本书，推荐这12本好书给你](https://mp.weixin.qq.com/s/f6_Sa_C4uU983UBaiMtJdQ) -- 来自公众号： 千古壹号

[@我是熊大](https://github.com/Tliens)：作者是京东的一位前端开发，读书爱好者，一年的读书清单有 87 本之多。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 程序员考公指南

**地址**：https://github.com/coder2gwy/coder2gwy

互联网首份程序员考公指南，由 3 位已经进入体制内的前大厂程序员联合献上。程序员近几年内卷的程度有些加重了，不少人萌生了回家当公务员的想法，这个仓库主要分享了他们上岸的一些经历和一些最佳实践，也有他们上岸之后的一些感想和感悟。

### Vim 从入门到精通（中文）

**地址**：https://github.com/wsdjeg/vim-galore-zh_cn

许多程序员可能了解过一点点 Vim，但从没用过，也不知道具体是怎么用的以及有什么有点，为什么有这么多人用。该仓库会从 Vim 是什么开始，讲述 Vim 的哲学，并带你入门 Vim 的世界。同时仓库中也记录列举了大部分用法和规则，其作为一个速查表也是很好用的。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### 摸鱼单词

**地址**：https://apps.apple.com/cn/app/id1488909953?mt=12

**软件状态**：免费

**软件介绍**：

软件作者自述：电脑大部分使用场景是用来办公，如果在办公之余可以背背单词就很好啦，于是就有了摸鱼单词。专注于利用碎片时间学习记忆英语单词。

> 和《摸鱼周报》相得益彰，作者也是一直在维护这个软件。

![摸鱼单词](http://cdn.zhangferry.com/Images/Snipaste_2022-01-18_20-46-39%E7%9A%84%E5%89%AF%E6%9C%AC.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS 成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第四十一期](https://mp.weixin.qq.com/s/DNXrfZgx0JaXyvfVZ4sYVA)

[iOS摸鱼周报 第四十期](https://mp.weixin.qq.com/s/y4229I_l8aLILR7WA7y01Q)

[iOS摸鱼周报 第三十九期](https://mp.weixin.qq.com/s/DolkTjL6d-KkvFftd2RLUQ)

[iOS摸鱼周报 第三十八期](https://mp.weixin.qq.com/s/a1aOOn1sFh5EaxISz5tAxA)

![](http://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
