# iOS摸鱼周报 第三期

![](https://cdn.zhangferry.com/Images/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享大家开发过程遇到的经验教训及学习内容。虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug经历。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips

开发小技巧收录。

### 关于dateFormat

在程序开发过程中如果想将字符串和`Date`类型进行互转，就需要借助于dateFormat进行格式指定。关于dateFormat有两个国际标准，一个是[ISO8601](https://www.iso.org/iso-8601-date-and-time-format.html "ISO8601")，一个是[RFC3339](https://www.ietf.org/rfc/rfc3339.txt "RFC3339")，这两个标准基本一致，但有一处不同是ISO允许24点，而 RFC3339 为了减少混淆，限制小时必须在0至23之间。23:59过1分钟，是第二天的0:00。

| 符号  | 含义         |
| ----- | ------------ |
| YYYY  | 按周算的年份 |
| yyyy  | 自然年       |
| MM    | 月           |
| DD/dd | 天           |
| hh    | 小时         |
| mm    | 分           |
| ss    | 秒           |

其中比较特殊的YYYY，举个例子：

```swift
let dateForamtter_yyyy = DateFormatter()
dateForamtter_yyyy.timeZone = TimeZone.init(secondsFromGMT: 8)
dateForamtter_yyyy.dateFormat = "yyyy-MM-dd"

let dateString = "2015-12-31"//2015-12-30
let date = dateForamtter_yyyy.date(from: dateString)!
print(date)//2015-12-31 00:00:00 +0000

let dateForamtter_YYYY = DateFormatter()
dateForamtter_YYYY.timeZone = TimeZone.init(secondsFromGMT: 8)
dateForamtter_YYYY.dateFormat = "YYYY-MM-dd"

let dateString_YYYY = dateForamtter_YYYY.string(from: date)
print(dateString_YYYY)//2016-12-31
```

会发现使用YYYY会多出一年，这是因为YYYY是按周定义的年，即系统认为，2015年12月31号这天是2016年的第一周。测试发现1月1号所在的那周被称为新年第一周，注意是按周日为新一周第一天算的。

这与ISO8601定义的不同，它的定义为1月4号所在那一周为新年第一周，注意这里是以周一为新一周第一天算的。同时它还可以表述为新旧年交替周四在哪一年，则该周为哪一年的周。有一个`ISO8601DateFormatter`类，可以进行验证：

```swift
let dateForamtter_iso8601 = ISO8601DateFormatter()
dateForamtter_iso8601.timeZone = TimeZone.init(secondsFromGMT: 8)
dateForamtter_iso8601.formatOptions = [.withYear, .withMonth, .withDay, .withWeekOfYear]

let isoDateString = dateForamtter_iso8601.string(from: date)
print(isoDateString)//201512W5304
```

由此可以看出苹果的日期格式并没有完全遵守ISO8601规范，但它提供了特定类进行标准转换。

对于RFC 3339 格式，可以指定dateFormat和locale进行转换：

```swift
let RFC3339DateFormatter = DateFormatter()
RFC3339DateFormatter.locale = Locale(identifier: "en_US_POSIX")
RFC3339DateFormatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ssZZZZZ"
RFC3339DateFormatter.timeZone = TimeZone(secondsFromGMT: 0)
 
/* 39 minutes and 57 seconds after the 16th hour of December 19th, 1996 with an offset of -08:00 from UTC (Pacific Standard Time) */
let string = "1996-12-19T16:39:57-08:00"
let date = RFC3339DateFormatter.date(from: string)
```

参考：

https://en.wikipedia.org/wiki/ISO_week_date

https://developer.apple.com/documentation/foundation/dateformatter

## 那些bug

### pod缓存问题

**bug出现的现象是什么样的？**

编译失败，由pod管理的三方库提示无法找到头文件。在项目的引用文件中确实没有该头文件，去`Pods`文件夹查看，发现对应库的引用出现了一个临时文件夹，而这里的文件确实是缺失该头文件的。

**是如何解决的？**

有两种解决方案：

1、升级或者回退对应库的版本号（会影响功能使用，不推荐）

2、清除对应的pod库的缓存：

```bash
$ pod cache clean 'PodModule' —-all # 清除特定仓库的仓库
$ pod cache clean —-all # 清除所有库的缓存
```

在`Pods`文件里删除对应库的文件，重新`install`一下。

**bug引发的反思**

该问题仅在某个需要频繁编译打包的机器出现过，尚不清楚出现的原因，猜测是频繁的库文件更新导致了pod文件添加出错。因为pod是有缓存的，对于出错的版本，它会一直加载错误的内容，除非换一个未被错误缓存的版本或者清除缓存重新install。但对于该问题的解决方式，可以参考一下此解决方式。先确认文件引用关系，对于未正确引用的pod文件，清除缓存解决。

### Error in PodSpec Validation due to architectures

**bug出现的现象是什么样的？**

在制作私有pod库时，使用Xcode12进行`lint`操作，报错提示：

```
ld: building for iOS Simulator, but linking in dylib built for iOS, file '/pathToSDK' for architecture arm64 clang: error: linker command failed with exit code 1 (use -v to see invocation)
```

**是如何解决的？**

在podspec文件里增加下面这个设置：

```ruby
s.pod_target_xcconfig = { 'EXCLUDED_ARCHS[sdk=iphonesimulator*]' => 'arm64' }
```

参考：https://github.com/CocoaPods/CocoaPods/issues/10104

**bug引发的反思**

Xcode 12支持arm64架构的模拟器（为了M1芯片），pod的 `lint` 操作会尝试编译所有架构的情况，对于没上M1芯片的电脑，就会导致上述失败提示。这时我们可以选择在模拟器支持的架构里去掉arm64。

## 编程概念

### 什么是shell

shell有两层含义，首先它表示一个应用程序，它连接了用户和系统内核，让用户能够更加高效、安全、低成本地使用系统内核，这就是 Shell 的本质。shell本身并不是shell内核，而是在内核的基础上编写的一个应用程序。

Linux上的shell程序有bash，zsh，Windows也有shell程序叫PowerShell。

第二层含义是脚本语言（Script），它是同JavaScript，Python，Ruby一样的脚本语言；Shell有一套自己的语法，你可以利用它的规则进行编程，完成很多复杂的任务。Shell脚本适合处理系统底层的操作，像Python等脚本语言也都支持直接执行shell命令。

这里的Shell脚本语言是指能够被bash或者zsh解释的脚本，shell脚本不能直接被windows识别，通常需要安装bash程序辅助识别。

在iOS开发期间，shell作为脚本常用于以下场景：

1、在Xcode中我们可以在Build Phase中添加脚本完成一些编译时工作。

2、配置打包脚本，CI/CD等

### 什么是bash

Bash，Unix shell的一种，1989年发布第一个正式版本，原先是计划用在GNU操作系统上，但能运行于大多数类Unix系统的操作系统之上，包括Linux与Mac OS X v10.4起至macOS Mojave都将它作为默认shell，而自macOS Catalina，默认Shell以zsh取代。

Bash是一个满足POSIX规范的shell，支持文件名替换（通配符匹配）、管道、here文档、命令替换、变量，以及条件判断和循环遍历的结构控制语句，同时它也做了很多扩展。

通常shell脚本的第一行会写`#!/bin/bash`，即代表使用bash解释该脚本。

### 什么是zsh

zsh是一款可用作交互式登录的shell命令解释器，zsh对Bourne shell做了大量改进，同时加入了bash、ksh的某些功能。从macOS Catalina起系统默认shell从bash改为了zsh。

用户社区网站Oh My Zsh专门收集zsh插件及主题，使得zsh使用起来更加便利也更受大家欢迎。

> Oh My Zsh will not make you a 10x developer...but you may feel like one.

截止目前Oh My Zsh有1700+贡献者，包含200+插件和超过140个主题。

ohmyzsh地址：https://github.com/ohmyzsh/ohmyzsh

### 包管理器是什么

包管理器又称软件包管理系统，它是在电脑中安装、配置、卸载、升级，有时还包含搜索、发布的工具组合。

**Homebrew**是一款Mac OS平台下的包管理器，拥有安装、卸载、更新、查看、搜索等很多实用的功能。

**apt-get**和**yum**跟Homebrew类似，只不过他们适用的平台是Linux，二者一般会被分别安装到Debian、Ubuntu和RedHat、CentOS中。

软件包管理器，适用于特定开发语言，这类软件包本身的安装需要依赖特定语言环境。

**NPM**（node package manager)，通常称为node包管理器，主要功能就是管理node包，使用Node.js开发的多数主流软件都可以通过npm下载。

**RubyGems**是Ruby的一个包管理器，提供了分发Ruby程序和库的标准格式“gem”，旨在方便地管理gem安装的工具，以及用于分发gem的服务器。使用Ruby开发的软件一般都通过gem进行管理。

**pip** 是通用的 Python 包管理工具，python3对应的是pip3。使用Python开发的软件多使用pip进行管理。

### 什么是ttys000

每次打开一个新的终端窗口，第一行显示的内容就是`Last login: Tue Dec 15 19:23:41 on ttys000`，如果再开一个窗口（包括新的tab），除了时间的变化，还有就是最后的那个名称，会变成ttys001，它会随着窗口打开数量不断增加。

这个ttys000是窗体的名称，它来源于UNIX中的tty命令。终端中输入tty，会返回当前的终端名称：`/dev/ttys000`。dev是Linux系统的设备特殊文件目录，该目录不可见。

另外在窗体中输入`logout`可以关闭当前终端窗口。

### 什么是Command Line Tools
Command Line Tools 是 一个运行在macos上的命令行工具集，它的安装命令是：`xcode-select --install`。

它是独立于xcode的，名字带有xcode只是因为它包含编译iOS项目的命令行工具。

它安装的内容除了clang、llvm等常见的工具外，还包括gcc、git等工具。

该工具集的安装路径是：`/Library/Developer/CommandLineTools/usr/bin/`

## 优秀博客

这期博客推荐顺带考察了一下各大厂的技术公众号运营情况（仅限移动端），虽然技术号不能反映一个公司的全貌，但多少还是能够体现出该公司的开源分享精神的，顺道推荐几篇高质量的文章。内容较多，还会再有一期，先后顺序不代表排名。

### 爱奇艺

公众号：**爱奇艺技术产品团队**

综合公众号，输出稳定，质量较高，排版方面可以，大绿框用了好久了，真的可以换一下🤣。

[效率提升50%，移动端UI自助验收在爱奇艺的探索与实践](https://mp.weixin.qq.com/s/K9p8986Gq1DoQ1fUYivPrg "效率提升50%，移动端UI自助验收在爱奇艺的探索与实践")

[爱奇艺知识移动端组件化探索和实践](https://mp.weixin.qq.com/s/DCrixXqnEnuHpYfUPjyACA "爱奇艺知识移动端组件化探索和实践")

### 阿里

公众号：**淘系技术**

综合技术公众号，输出稳定且高产，质量很高，覆盖面很广，排版也不错，在这几个技术公众号里我感觉是做的最用心也是最好的。

[移动前端开发和 Web 前端开发的区别是什么？](https://mp.weixin.qq.com/s/kPn-2y3Q_CMjwCB1c1yVTA "移动前端开发和 Web 前端开发的区别是什么？")

[一文读懂架构整洁之道](https://mp.weixin.qq.com/s/XAm1MO4RQYtkj3ay-2jT7A "一文读懂架构整洁之道")

公众号：**闲鱼技术**

综合技术公众号，纯移动端内容较少，闲鱼是较早使用Flutter的团队，这里有不少Flutter 相关的实战干货。

### 百度

公众号：**百度App技术**

偏前端的公众号，稳定输出，质量可以，但是选题较单一，排版有待提高。

[百度App Objective-C/Swift 组件化混编之路（一）](https://mp.weixin.qq.com/s/Vk6KNT_Ca_0se2eckYRuBg "百度App Objective-C/Swift 组件化混编之路（一）")

[百度App Objective-C/Swift 组件化混编之路（二）- 工程化](https://mp.weixin.qq.com/s/xA3g0GdNvfKNgfvG6imEvw "百度App Objective-C/Swift 组件化混编之路（二）- 工程化")

### 字节跳动

公众号：**字节跳动技术团队**

综合技术公众号，输出稳定，质量较高，感觉仅次于淘系技术。

[iOS性能优化实践：头条抖音如何实现OOM崩溃率下降50%+](https://mp.weixin.qq.com/s/4-4M9E8NziAgshlwB7Sc6g "iOS性能优化实践：头条抖音如何实现OOM崩溃率下降50%+")

[今日头条优化实践： iOS 包大小二进制优化，一行代码减少 60 MB 下载大小](https://mp.weixin.qq.com/s/TnqAqpmuXsGFfpcSUqZ9GQ "今日头条优化实践： iOS 包大小二进制优化，一行代码减少 60 MB 下载大小")

### 京东

公众号：**京东零售技术**

综合技术公众号，稳定输出，质量也可以，排版感觉一般，有待提高。

[带你深入了解OC对象的销毁过程](https://mp.weixin.qq.com/s/p8RRpuY2AgNc-lJ0NzG9bg "带你深入了解OC对象的销毁过程")

[iOS链接原理解析与应用实践](https://mp.weixin.qq.com/s/_3WXnDolNICs2euoJph44A "iOS链接原理解析与应用实践")

### 网易

公众号：**网易云音乐大前端团队**

大前端技术公众号，移动端相对较少，输出稳定，质量可以。从2020年5月份建立，排版不断在优化，最新一期挺不错，跟字节跳动技术团队风格一致了。

[网易云音乐 iOS 14 小组件实战手册](https://mp.weixin.qq.com/s/gFd8fkJBkQd5RpFSD0P8Ig "网易云音乐 iOS 14 小组件实战手册")

网易还有另外两个技术号，**网易传媒技术团队**，输出相对少，有兴趣的也可以看下。

### 拼多多

很抱歉，没有找到他们的技术公众号，只搜到一堆砍价群0。0，如果有了解的小伙伴可以告知下。

## 学习资料

### 《Flutter技术解析与实战》

咸鱼团队对Flutter技术的探索与实战分析，听说他们已经在准备写第二本Flutter书了。可以关注公众号：**咸鱼技术获取**，后台免费获取，另有实体书可以淘宝搜索购买。

![](https://cdn.zhangferry.com/Images/20210110171712.png)

### 《Flutter开发实站详解》

掘金作者 [恋猫的小郭](https://juejin.cn/user/817692379985752) 写的Flutter实战详解，可以在京东、当当搜索购买实体或者电子版图书阅读。另外作者本人还有一个介绍 Flutter 技术的文章合辑，其与实体书不同，但内容还是很详实的，对Flutter 感兴趣，想学习的话，可以点开阅读。

地址：[GSY Flutter](https://guoshuyu.cn/home/wx/ "GSY Flutter ")

![](https://cdn.zhangferry.com/Images/20210110172952.png)

## 工具推荐

推荐好用的开发工具。

### MacZip(原名eZip)

**推荐来源**：[zhangferry](https://github.com/zhangferry)

**下载地址**：https://ezip.awehunt.com/

**软件状态**：免费

**使用介绍**

Mac上非常好用的解压缩软件：

* 支持rar, zip, 7z, tar, gz, bz2, iso, xz, lzma, apk, lz4等超过二十种压缩格式。
* 支持批量文件加密。
* 支持压缩包预览

![](https://cdn.zhangferry.com/Images/20210110110014.png)

### uTools

**推荐来源**：[zhangferry](https://github.com/zhangferry)

**下载地址**：https://u.tools/

**软件状态**：免费（部分功能付费）

**使用介绍**

uTools是一个丰富的生产力工具集，支持将近百种的插件。它的使用方式和 Alfred 类似，通过快捷键调出输入框，并通过特殊指令执行结果。但它有比 Alfred 更简单的插件集成方式，在我看来它是更易用的。

![](https://cdn.zhangferry.com/Images/20210110110536.png)

## 联系我们

[摸鱼周报第一期](https://zhangferry.com/2020/12/20/iOSWeeklyLearning_1/)

[摸鱼周报第二期](https://zhangferry.com/2021/01/03/iOSWeeklyLearning_2/)

![](https://cdn.zhangferry.com/Images/wechat_official.png)
