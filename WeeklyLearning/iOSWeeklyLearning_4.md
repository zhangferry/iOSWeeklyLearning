# iOS摸鱼周报 第四期

![](http://cdn.zhangferry.com/Images/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享大家开发过程遇到的经验教训及学习内容。虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug经历。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips

开发小技巧收录。

### 定时清理脚本

iOS里面经常打包的机器会产生很多xcarchive文件，该文件用于生成最终的ipa，它除了包含应用外还包含dsym文件，所以一般都比较大。如果构建次数很多，他们会很容易就填满磁盘空间，导致后续的构建任务失败。针对这种现象我们可以写一个定时任务用于清除这类文件。

该过程分为两步：

**1、编写清理脚本**

这里也可以写别的你想定时执行的任务

```bash
#!/bin/sh
# 扫描文件路径
targePath=~/Library/Developer/Xcode/Archives

# 清楚文件特征，可以用正则语法
rule="*.xcarchive"

# 删除7天之前的文件
find ${targePath} -mtime +7 -name ${rule} -**exec** rm -rf {} \;
```

**2、将脚本添加到系统定时任务中**

添加定时任务需要用到cron工具，cron是一款类Unix的操作系统下的基于时间的任务管理系统。用户们可以通过cron在固定时间、日期、间隔下，运行定期任务（可以是命令和脚本）。我们在mac系统也可以使用cron。

需要注意的是由于在macOS Catalina下系统对 cron的权限进行了限制，我们需要给该执行文件添加完全磁盘访问权限才可以使用。

步骤是：

1、执行`whereis cron`，查看cron所在目录，通常它在`/usr/sbin/cron`下。

2、使用Finder 跳转到该目录

3、打开系统设置 > 安全与隐私 > 完全磁盘访问权限，打开加锁。

4、将cron程序拖入到完全磁盘访问权限右侧的程序目录。

然后将脚本设置为可执行文件：

```bash
$ chmod +x [corn_clean_file.sh](http://corn_clean_file.sh/)
```
进入crontab编辑界面
```bash
$ crontab -e
```
输入如下内容，其表示每天凌晨三点执行对应任务，保存并退出。
```
00 03 * * * /path/clean_script.sh
```

### 苹果家庭里的儿童账号退登问题

苹果有项功能是家庭账号，可以为子女设置独立的儿童账号，用于实现使用时长管理、支付管理等功能。

在测试儿童账号的使用场景时发现一个问题，如果登录了不满13周岁的儿童账号，会无法退出，即使家长端也是无法退出的。退出按钮置灰，提示“由于访问限制，无法退出登录”。联系了苹果客服才知道需要关掉家长端对于儿童账号的所有限制才可以退出账号，因为设置儿童账号时会有一个引导开启屏幕时长管理的设置，所以关掉它就可以正常退出了。

## 那些bug

**问题现象**

在执行`bundle exec`命令时遇到`/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX11.1.sdk/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/include/ruby-2.6.0/ruby/ruby.h:24:10: fatal error: 'ruby/config.h' file not found #include "ruby/config.h"`

的错误。

执行环境如下：

> OS 版本：macOS Catalina
>
> Xcode 版本：12.3
>
> ruby 版本：2.6.0 （系统内置）

**是如何解决的？**

在这里找到了问题讨论：https://github.com/CocoaPods/CocoaPods/issues/10286

可以通过rvm安装ruby2.7.2或者3.0.0版本，然后使用新安装的ruby版本即可。

简单回顾下rvm管理ruby版本的用法:

```bash
$ ruby --version #查看当前ruby版本

$ rvm list known #列出当前可用ruby版本

$ rvm install 2.7.2 #安装对应版本的ruby

$ rvm use 2.7.2 --defualt #设置当前使用版本，且设置为默认值

#如果想切回系统版本可以：
$ rvm use system --defualt
```

**bug引发的反思**

不管任何bug都可以从报错的日志里找到一些蛛丝马迹。该错误描述为`ruby/config.h`头文件找不到，该头文件所在的目录是系统自带的`Ruby.frameowrk`框架，所以大概率可以推测是该系统版本自带的Ruby没有内置这个文件，可以推测是系统的问题。管理Ruby版本，推荐使用rvm，当安装了2.7.2版本之后，确实可以正常执行bundle命令了，说明确实是系统包的问题。

## 编程概念

本期概念围绕几个操作系统开展，系统能帮助大家了解各个操作系统之间的关系。

### 什么是GNU

![](http://cdn.zhangferry.com/Images/20210124145056.png)

GNU是一个自由的操作系统，名字是一个递归 GNU’s Not Unix!的缩写。

它出现的原因是Unix被发明后，开始收费和商业闭源，Richard Matthew Stallman觉得很不爽。于是发起了GNU计划：创造一个仿Unix并与之兼容的自由开源操作系统。

为此Stallman还创建了FSF（自由软件基金会）和GPL（GNU通用公共许可协议），在GNU项目里开发的软件都遵循GPL协议。

在打造操作系统的过程中，GNU开发出了编辑器Emacs，编译器（GCC），shell等很牛叉的东西，但唯独操作系统内核Hurd因为种种原因一直无法完成。

这时出现了Linux，它就是一个操作系统内核，不仅开源还被广泛追捧。Linux和GNU像是天生一对，一个万事具备只缺内核，一个只专注做内核，于是一拍即合，很多Linux发行版开始接入GNU的组件，Linux也遵循了GPL协议。

所以Stallman主张Linux使用了很多GNU组件应该叫GNU/Linux，但是并没有得到Linux设计的一致认同，所以该名称仍有争议。

但Hurd的开发并没有因此结束，目前还在进行中。

### 什么是GCC

早期 GCC 的全拼为 GNU C Compiler，即 GUN 计划诞生的 C 语言编译器，显然最初 GCC 的定位确实只用于编译 C 语言。但经过这些年不断的迭代，GCC 的功能得到了很大的扩展，它不仅可以用来编译 C 语言程序，还可以处理 C++、Go、Objective -C 等多种编译语言编写的程序。与此同时，由于之前的 GNU C Compiler 已经无法完美诠释 GCC 的含义，所以其英文全称被重新定义为  GNU Compiler Collection，即 GNU 编译器套件。

GCC 编译器从而停止过改进。截止到今日（2020 年 5 月），GCC 已经从最初的 1.0 版本发展到了 10.1 版本，期间历经了上百个版本的迭代。作为一款最受欢迎的编译器，GCC 被移植到数以千计的硬件/软件平台上，几乎所有的 Linux 发行版也都默认安装有 GCC 编译器。

补充一句，早期OC项目都是通过GCC编译的，因为不满足于GCC的性能，Chris Lattner开发了Clang。

### 什么是XNU
XNU是一个由苹果电脑开发用于macOS操作系统的操作系统内核。它是Darwin操作系统的一部分，跟随着Darwin一同作为自由及开放源代码软件被发布。它还是iOS、tvOS和watchOS操作系统的内核。XNU是X is Not Unix的缩写。这一点跟GNU一样。

XNU最早是NeXT公司为了NeXTSTEP操作系统而发展的，在苹果电脑收购NeXT公司之后，XNU的Mach微内核被升级到Mach 3.0。

需要注意区分的概念是操作系统内核，操作系统，桌面操作系统。

Mach是一个微内核

XNU是一个混合操作系统内核，包含Mach

Darwin是以XNU为内核发布的开源操作系统

macOS是以Darwin为核心的桌面操作系统

Darwin地址：https://github.com/apple/darwin-xnu

### 什么是FreeBSD

![](http://cdn.zhangferry.com/Images/20210124145432.png)

在此之前先说下BDS（Berkeley Software Distribution 伯克利软件套装），它是Unix的衍生系统，在1977至1995年由伯克利大学分校开发和发布，其是去除SyStem V 删除了AT&T专利代码的。

随着该系统的发展，还提出了新的许可协议：BSD License，它在软件使用上提供了最小限度的限制，它允许遵循该协议的软件被二次开发，且开发之后的版本可以闭源。

所以基于BSD发展出了很多类Unix系统，被称为BSD家族，其中最著名的当属FreeBSD。直到现在FreeBSD仍然在很多网站的服务器上运行着。

乔帮主在NextStep时开发了基于FreeBSD的后端Darwin，回归Apple就给带过去了，而这个就是MacOS的内核，之后的iOS，watchOS也都是基于Darwin构建的。

索尼用FreeBSD创造了PS3，PS4。

任天堂用FreeBSD创造了Nintendo Swiftch。

BSD的发展历史：

![](http://cdn.zhangferry.com/Images/20210124145540.png)

### 什么是POSIX

POSIX是Portable Operation System Interface的缩写，即可移植操作系统接口，它是由IEEEE为了在Unix上运行软件提出的一系列标准，X表明其对Unix API的传承。

类Unix系统像Linux、MacOS中均实现了对POSIX接口的兼容，其中我们在多线程使用过程中创建的pthread（前面的p即POSIX），就是基于POSIX里的线程标准设计的。


## 优秀博客
### 搜狐
公众号：**搜狐技术产品**
综合性技术公众号，输出稳定，质量也不错。偏重运营一些，会有很多转载内容。

[带你实现完整的视频弹幕系统](https://mp.weixin.qq.com/s/Y0L1d124V9tWoJA7hYNRMQ "带你实现完整的视频弹幕系统")

[iOS插件化架构探索](https://mp.weixin.qq.com/s/QJ9YHX-Uy6lDIhJe_5wPGw "iOS插件化架构探索")

### 腾讯
公众号：**腾讯音乐技术团队**
腾讯音乐开发团队公众号，更新不稳定，可能一两个月才会有一篇文章，但质量还是不错的。

[Q音直播编译优化与二进制集成方案](https://mp.weixin.qq.com/s/5q_PLdLeuuuQnsLrbzaOeQ "Q音直播编译优化与二进制集成方案")

腾讯还有个号是**腾讯技术工程**，综合性技术公众号，更新较稳定。
另外有点奇怪的是，微信团队和QQ团队竟然没有单独的技术公众号。微信团队之前有个博客：https://wereadteam.github.io/ ，但看了下2020年只发过一篇文章。

### 美团
公众号：**美团技术团队**
综合性技术公众号，输出稳定，质量很高，原创文章数量已达358篇，都是团队内部人员写的，非常不错。

[移动端UI一致性解决方案](https://mp.weixin.qq.com/s/oq7ylltdRIdJuSlL7EIiNA "移动端UI一致性解决方案")

[Flutter包大小治理上的探索与实践](https://mp.weixin.qq.com/s/adC-YUWd-xuUlzeAPHzJoQ "Flutter包大小治理上的探索与实践")

### 滴滴
公众号：**滴滴技术**
综合性技术公众号，但是移动端内容真的很少。不过滴滴在开源社区的贡献还是挺大的，DoraemonKit和chameleon都有很高的star数。

[滴滴开源 DoraemonKit：一款像哆啦A梦般全能的App研发工具](https://mp.weixin.qq.com/s/FXATxeEoRMdKzFRDg-zPFg "滴滴开源 DoraemonKit：一款像哆啦A梦般全能的App研发工具")

### 即刻
公众号：**即刻技术团队**
综合技术公众号，移动端内容也不少。整理来看即刻做的还是挺不错的。

[iOS中的网络调试](https://mp.weixin.qq.com/s/K0_3efxXKJM3fU-Icyh7Hg "iOS中的网络调试")

### 其他公司

还有很多科技公司在维护技术公众号，不再过多展开了，大家有兴趣可以自行查找。

| 公司名   | 公众号名     | 说明                 |
| -------- | ------------ | -------------------- |
| 小米     | 小米科技     | 无移动端内容         |
| 贝壳找房 | 贝壳产品技术 | 综合号，有移动端内容 |
| 快手     | 快手Ytech    | 无移动端内容         |
| 360      | 360技术      | 综合号，有移动端内容 |
| 携程     | 携程技术     | 综合号，有移动端内容 |


## 学习资料

### [Refactoring.Guru](https://refactoringguru.cn/ "Refactoring.Guru")

一个非常有趣的讲解设计模式、SOLID原则、重构原则的网站。支持八种语言，有很多丰富的配图帮助我们理解这些重要的编程概念。

![](http://cdn.zhangferry.com/Images/20210124190413.png)

## 工具推荐

推荐好用的开发工具。

### kaleidoscope

**推荐来源**：zhangferry

**下载地址**：https://kaleidoscope.app/

**软件状态**：付费，$69.99

**使用介绍**

kaleidoscope中文翻译是万花筒，它是一款颜值很高，专业性很强的diff工具。不光能查看文本的不同，还能识别图片和文件夹的不同。我们可以将它与 git 组合使用，使用它替换git的mergetool。

![](http://cdn.zhangferry.com/Images/20210124184141.png)

### Sherlock

**推荐来源**：zhangferry

**下载地址**：https://sherlock.inspiredcode.io/

**软件状态**：付费，$49

**使用介绍**

在iOS开发过程中的UI调试常常是让人痛苦的，因为不支持热更新，我们稍微改动一点地方就需要编译整个项目重新运行，这无疑很浪费时间。而Sherlock就是用于解决这个问题的工具（仅支持模拟器），我们可以实时修改各个控件的UI属性，并进行查看最终效果。

![](http://cdn.zhangferry.com/Images/20210124195019.png)

## 联系我们

[摸鱼周报第一期](https://zhangferry.com/2020/12/20/iOSWeeklyLearning_1/)

[摸鱼周报第二期](https://zhangferry.com/2021/01/03/iOSWeeklyLearning_2/)

[摸鱼周报第三期](https://zhangferry.com/2021/01/10/iOSWeeklyLearning_3/)

![](http://cdn.zhangferry.com/Images/wechat_official.png)
