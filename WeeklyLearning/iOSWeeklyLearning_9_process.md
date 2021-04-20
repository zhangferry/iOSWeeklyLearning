# iOS摸鱼周报 第九期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享大家开发过程遇到的经验教训及学习内容。虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug经历。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips

### 关于Xcode 12的Tab
不知道有多少同学困惑于Xcode 12的新tab模式，反正我是觉得这种嵌套的tab形式还不如旧版简洁明了。

![](https://www.jessesquires.com/img/xcode12-tabs-with-tabs.png)

想切回旧版本tab模式的，可以按照此文操作：
[How to fix the incomprehensible tabs in Xcode 12](https://www.jessesquires.com/blog/2020/07/24/how-to-fix-the-incomprehensible-tabs-in-xcode-12/)
![](https://www.jessesquires.com/img/xcode12-tabs-prefs.png)

通过实验发现，Xcode 12下的“子tab”有以下几个特点：
> A.当单击文件打开时，tab将显示为斜体，如果双击，则以普通字体显示。斜体表示为“临时”tab，普通字体表示为“静态”tab；
>
> B.双击tab顶部文件名，或者对“临时”tab编辑后，“临时”tab将切换为“静态”tab；
>
> C.如果当前位于“静态”tab，新打开的文件会新起一个tab，并排在当前tab之后；
>
> D.新打开的“临时”文件会在原有的“临时”tab中打开，而不会新起一个“临时”tab；
>
> E.使用Command + Shift + O打开的是“临时”文件。



## 那些Bug

### fishhook在某些场景下只生效一次

**问题背景**

之前我们监控到钥匙串的API在主线程访问时存在卡死的情况，因此hook 相关API，将访问移到子线程。因此使用到fishook，当时测试并没有发现异常。

**问题描述**

前段时间在做技术优化时发现我们的hook代码只生效了一次，下次访问API时变成了直接访问系统原方法。

**问题原因**

由于hook之前没有调用过钥匙串API，因此可能此时并没有做bind，在我们hook后bind信息被替换成我们的函数，因此首次调用hook成功。但是在hook方法中我们又调用了原函数，此时触发了bind，内存中的函数地址又被替换成系统函数，因此第二次调用时hook失败。
解决方案：见https://github.com/facebook/fishhook/issues/36

## 编程概念

### 什么是 Homebrew

Homebrew 是一款 Mac OS 平台下的软件包管理工具，拥有安装、卸载、更新、查看、搜索等很多实用的功能。简单的一条指令，就可以实现包管理，而不用你关心各种依赖和文件路径的情况，十分方便快捷。

你可以在这里获取安装脚本：[https://zhuanlan.zhihu.com/p/111014448](https://zhuanlan.zhihu.com/p/111014448)

![](https://cdn.nlark.com/yuque/0/2021/png/12376889/1618642506356-a9d7bd46-0104-4124-a44c-73f50ad76581.png#clientId=uf4f204d0-23e1-4&from=paste&height=253&id=u3fa0f3bb&margin=%5Bobject%20Object%5D&originHeight=253&originWidth=420&originalType=binary&size=80150&status=done&style=none&taskId=u9d2e2517-8f7f-4b0a-8d0f-919a130320d&width=420)

参考资料：[https://brew.sh/index_zh-cn](https://brew.sh/index_zh-cn)

### 什么是 Ruby

![](https://gitee.com/zhangferry/Images/raw/master/gitee/ruby_image.png)

Ruby 是一种开源的面向对象程序设计的服务器端脚本语言，在 20 世纪 90 年代中期由日本的松本行弘设计并开发。在 Ruby 社区，松本也被称为马茨（Matz）。 

Ruby的设计和Objective-C有些类似，都是受Smalltalk的影响。而这也一定程度促进了iOS开发工具较为广泛的使用Ruby写成。

较为知名的几个由Ruby写成的iOS开发工具有：CocoaPods、Fastlane、xcpretty。那这些库为啥使用Ruby开来发呢？

CocoaPods的主要作者Eloy Duran说除了上面提到的Smalltalk影响，还有就是使用Ruby可以在Bundler和RubyGem之间分享代码，早起阶段MacRuby提供了很多解析Xcode projects的方法，作为CLI工具，Ruby具有强大的字符串处理能力。

Fastlane工具链的作者之一Felix考虑的则是，已经有部分iOS工具选择了Ruby，像是CocoaPods以及给Fastlane开发带来灵感的nomad-cli。使用Ruby将会更容易与这些工具进行对接。

[参考来源：A History of Ruby inside iOS Development](https://medium.com/xcblog/a-history-of-ruby-inside-ios-development-427b5a09f91e "A History of Ruby inside iOS Development")

### 什么是 Rails

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210419223057.png)

Rails（也叫Ruby on Rails）框架首次提出是在 2004 年 7 月，它的研发者是 26 岁的丹麦人 David Heinemeier Hansson。Rails 是使用 Ruby 语言编写的 Web 应用开发框架，目的是通过解决快速开发中的共通问题，简化 Web 应用的开发。与其他编程语言和框架相比，使用 Rails 只需编写更少代码就能实现更多功能。有经验的 Rails 程序员常说，Rails 让 Web 应用开发变得更有趣。

Rails的两大哲学是：不要自我重复（DRY），多约定，少配置。

松本行弘说过：Ruby能拥有现在的人气，基本上都是Ruby on Rails所作出的贡献。

### 什么是 rbenv 

![](https://gitee.com/zhangferry/Images/raw/master/gitee/rbenv_image.png)

[rbenv](https://github.com/rbenv/rbenv "rbenv") 和 RVM 都是目前流行的 Ruby 环境管理工具，它们都能提供不同版本的 Ruby 环境管理和切换。

进行 Ruby 版本管理的时候更推荐 rbenv 的方式，你也可以参考 rbenv 官方的 [Why choose rbenv over RVM?](https://github.com/rbenv/rbenv/wiki/Why-rbenv%3F "Why choose rbenv over RVM?")，当前 rbenv 有两种安装方式：

**手动安装**

```bash
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
# 用来编译安装 ruby
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
# 用来管理 gemset, 可选, 因为有 bundler 也没什么必要
git clone git://github.com/jamis/rbenv-gemset.git  ~/.rbenv/plugins/rbenv-gemset
# 通过 rbenv update 命令来更新 rbenv 以及所有插件, 推荐
git clone git://github.com/rkh/rbenv-update.git ~/.rbenv/plugins/rbenv-update
# 使用 Ruby China 的镜像安装 Ruby, 国内用户推荐
git clone git://github.com/AndorChen/rbenv-china-mirror.git ~/.rbenv/plugins/rbenv-china-mirror
```

**homebrew安装**

```bash
$ brew install rbenv
```

**配置**

安装完成后，把以下的设置信息放到你的 Shell 配置文件里面，以保证每次打开终端的时候都会初始化 rbenv。

```bash
export PATH="$HOME/.rbenv/bin:$PATH" 
eval "$(rbenv init -)"
# 下面这句选填
export RUBY_BUILD_MIRROR_URL=https://cache.ruby-china.com
```

配置Ruby 环境，需重开一个终端。

```bash
$ rbenv install --list  			 # 列出所有 ruby 版本
$ rbenv install 2.7.3     		 # 安装 2.7.3版本
$ rbenv versions               # 列出安装的版本
$ rbenv version                # 列出正在使用的版本
# 下面三个命令可以根据需求使用
$ rbenv global 2.7.3      		 # 默认使用 1.9.3-p392
$ rbenv shell 2.7.3       # 当前的 shell 使用 2.7.3, 会设置一个`RBENV_VERSION` 环境变量
$ rbenv local 2.7.3  					 # 当前目录使用 2.7.3, 会生成一个 `.rbenv-version` 文件
```

### 什么是 RubyGems 

> The RubyGems software allows you to easily download, install, and use ruby software packages on your system. The software package is called a “gem” which contains a packaged Ruby application or library.

RubyGems 是 Ruby 的一个依赖包管理工具，管理着 Gem。用 Ruby 编写的工具或依赖包都称为 Gem。

RubyGems 还提供了 Ruby 组件的托管服务，可以集中式的查找和安装 library 和 apps。当我们使用 gem install 命令安装 Gem 时，会通过 rubygems.org 来查询对应的 Gem Package。而 iOS 日常中的很多工具都是 Gem 提供的，例如 Bundler，fastlane，jazzy，CocoaPods 等。

在默认情况下 Gems 总是下载 library 的最新版本，这无法确保所安装的 library 版本符合我们预期。因此还需要 Gem Bundler 配合。

![](https://cdn.nlark.com/yuque/0/2021/png/12376889/1618646566177-110f87c1-d2a4-4ef0-b7ee-b9a6b09c389d.png#clientId=uf4f204d0-23e1-4&from=paste&height=200&id=u9b1b0575&margin=%5Bobject%20Object%5D&originHeight=200&originWidth=200&originalType=binary&size=69528&status=done&style=none&taskId=uc8a57254-3e9e-4af4-b745-b9dc43a502f&width=200)

### 什么是 Bundler

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210419225753.png)

[Bundler](https://www.bundler.cn/ "Bundler") 是一个管理 Gem 依赖的 Gem，用来检查和安装指定 Gem 的特定版本，它可以隔离不同项目中 Gem 的版本和依赖环境的差异。

你可以执行 `gem install bundler` 命令安装 Bundler，接着执行 `bundle init` 就可以生成一个 Gemfile 文件，你可以在该文件中指定 CocoaPods 和 fastlane 等依赖包的特定版本号，比如：

```
source "https://rubygems.org"
gem "cocoapods", "1.10.0"
gem "fastlane", "> 2.174.0"
```

然后执行 `bundle install` 来安装 Gem。 Bundler 会自动生成一个 Gemfile.lock 文件来锁定所安装的 Gem 的版本。

这一步只是安装指定版本的 Gem，使用的时候我们需要在 Gem 命令前增加 `bundle exec`，以保证我们使用的是项目级别的 Gem 版本（也就是 Gemfile.lock 文件中锁定的 Gem 版本），而不是操作系统级别的 Gem 版本。

```bash
$ bundle exec pod install
$ bundle exec fastlane beta
```



## 优秀博客
1、[我在Uber亲历的最严重的工程灾难](https://mp.weixin.qq.com/s/O1haH28cTr0tkhRAnVZQ6g "我在Uber亲历的最严重的工程灾难") -- 来自公众号：infoQ

>准备或者已经接入Swfit可以先了解下

2、[美团 iOS 工程 zsource 命令背后的那些事儿](https://mp.weixin.qq.com/s/3qcv1NW4-ce87cvAS4Jsxg "美团 iOS 工程 zsource 命令背后的那些事儿") -- 来自公众号： 美团技术团队

>美团技术团队历史文章，对DWARF文件的另一种应用。文章还原了作者解决问题的思路历程，除了技术本身外，解决问题的思路历程也是值得借鉴的。

3、[NSObject方法调用过程详细分析](https://juejin.cn/post/6844904000450478087 "NSObject方法调用过程详细分析") -- 来自掘金：maniac_kk

>字节跳动maniac_kk同学的一篇优质文章，无论深度还是广度都是非常不错的，很多底层知识融会贯通，值得细细品味

4、[iOS疑难Crash的寄存器赋值追踪排查技术](https://www.jianshu.com/p/958d4f109bb0 "iOS疑难Crash的寄存器赋值追踪排查技术") -- 来自简书：欧阳大哥

>在缺少行号信息时如何通过寄存器赋值推断出具体的问题代码，具有很高的参考价值，在遇到疑难问题时可以考虑是否能借鉴此思路

5、[抖音 iOS 工程架构演进](https://juejin.cn/post/6950454120826765325 "抖音 iOS 工程架构演进") -- 来自掘金：字节跳动技术团队

>业务的发展引起工程架构做出调整，文章介绍了抖音的工程架构演进历程。作为日活过亿的产品，其工程架构的演变对多数APP来说都具有一定的借鉴意义。


## 学习资料

1、[CS-Notes](http://www.cyc2018.xyz/ "CS-Notes")

> 该「Notes」包含技术面试必备基础知识、Leetcode、计算机操作系统、计算机网络、系统设计、Java、Python、C++等内容，知识结构简练，内容扎实。该仓库的内容皆为作者及 Contributors 的原创，目前在 Github 上获 126k Stars。

2、[Learn Git Branching](https://oschina.gitee.io/learn-git-branching/ "Learn Git Branching")

> 入门级的 Git 使用教程，用图形化的方式来介绍 Git 的各个命令，每一关都有一个小测试来巩固知识点。编者自己过了一遍了，体验很不错，同时填补了我自己一些 Git 知识上的漏洞和误区。

## 工具推荐

### OpenInTerminal
**推荐来源**：brave723

**地址**：https://github.com/Ji4n1ng/OpenInTerminal

**软件状态**：免费 

**使用介绍**

OpenInTerminal 是一款开发辅助工具，可以增强 Finder 工具栏以及右键菜单增加在当前位置打开终端的功能。另外还支持：在编辑器中打开当前目录以及在编辑器中打开选择的文件夹或文件
![](https://user-images.githubusercontent.com/11001224/78589385-b797b880-7872-11ea-9062-c11a49461598.gif)
##### 核心功能
* 在终端（或编辑器）中打开目录或文件
* 打开自定义应用
* 支持 终端iTerm

### SnippetsLib
**推荐来源**：brave723

**地址**: https://apps.apple.com/cn/app/snippetslab/id1006087419?mt=12

**软件状态**：$9.99

**使用介绍**

SnippetsLab是一款mac代码片段管理工具，使用SnippetsLab可以提高工作效率。它可以帮助您收集和组织有价值的代码片段，您可以随时轻松访问它们

![](https://www.renfei.org/snippets-lab/images/Landing/themes/mojave-dark.jpg)



## 联系我们

[摸鱼周报第三期](https://zhangferry.com/2021/01/10/iOSWeeklyLearning_3/)

[摸鱼周报第四期](https://zhangferry.com/2021/01/24/iOSWeeklyLearning_4/)

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

[摸鱼周报第六期](https://zhangferry.com/2021/03/14/iOSWeeklyLearning_6/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
