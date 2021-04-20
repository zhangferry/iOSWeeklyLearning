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

> B.双击tab顶部文件名，或者对“临时”tab编辑后，“临时”tab将切换为“静态”tab；

> C.如果当前位于“静态”tab，新打开的文件会新起一个tab，并排在当前tab之后；

> D.新打开的“临时”文件会在原有的“临时”tab中打开，而不会新起一个“临时”tab；

> E.使用Command + Shift + O打开的是“临时”文件。



## 那些Bug



## 编程概念

### 什么是 Homebrew

Homebrew 是一款 Mac OS 平台下的软件包管理工具，拥有安装、卸载、更新、查看、搜索等很多实用的功能。简单的一条指令，就可以实现包管理，而不用你关心各种依赖和文件路径的情况，十分方便快捷。

你可以在这里获取安装脚本：[https://zhuanlan.zhihu.com/p/111014448](https://zhuanlan.zhihu.com/p/111014448)

![](https://cdn.nlark.com/yuque/0/2021/png/12376889/1618642506356-a9d7bd46-0104-4124-a44c-73f50ad76581.png#clientId=uf4f204d0-23e1-4&from=paste&height=253&id=u3fa0f3bb&margin=%5Bobject%20Object%5D&originHeight=253&originWidth=420&originalType=binary&size=80150&status=done&style=none&taskId=u9d2e2517-8f7f-4b0a-8d0f-919a130320d&width=420)

参考资料：[https://brew.sh/index_zh-cn](https://brew.sh/index_zh-cn)

### 什么是 Ruby

Ruby 是一种纯粹的面向对象编程语言。它由日本的松本行弘创建于 1993 年。 
 
您可以在 www.ruby-lang.org 的 Ruby 邮件列表上找到松本行弘的名字。在 Ruby 社区，松本也被称为马茨（Matz）。 

Ruby 是“程序员的最佳朋友”。 Ruby 的特性与 Smalltalk、Perl 和 Python 类似。Perl、Python 和 Smalltalk 是脚本语言。Smalltalk 是一个真正的面向对象语言。Ruby，与 Smalltalk 一样，是一个完美的面向对象语言。使用 Ruby 的语法比使用 Smalltalk 的语法要容易得多。

Ruby 的特性有：

- Ruby 是开源的，在 Web 上免费提供，但需要一个许可证。
- Ruby 是一种通用的、解释的编程语言。
- Ruby 是一种真正的面向对象编程语言。
- Ruby 是一种类似于 Python 和 Perl 的服务器端脚本语言。
- Ruby 可以用来编写通用网关接口（CGI）脚本。
- Ruby 可以被嵌入到超文本标记语言（HTML）。
- Ruby 语法简单，这使得新的开发人员能够快速轻松地学习 Ruby。
- Ruby 与 C++ 和 Perl 等许多编程语言有着类似的语法。
- Ruby 可扩展性强，用 Ruby 编写的大程序易于维护。
- Ruby 可用于开发的 Internet 和 Intranet 应用程序。
- Ruby 可以安装在 Windows 和 POSIX 环境中。
- Ruby 支持许多 GUI 工具，比如 Tcl/Tk、GTK 和 OpenGL。
- Ruby 可以很容易地连接到 DB2、MySQL、Oracle 和 Sybase。
- Ruby 有丰富的内置函数，可以直接在 Ruby 脚本中使用。

![](https://cdn.nlark.com/yuque/0/2021/png/12376889/1618649107486-fc8f3ab1-93bb-41b6-ba93-1dfbc6d86c4f.png#clientId=uf4f204d0-23e1-4&from=paste&height=336&id=udb4b1396&margin=%5Bobject%20Object%5D&originHeight=336&originWidth=800&originalType=binary&size=135412&status=done&style=none&taskId=u57f6c6ee-35f5-47f1-bbbd-1ecd5a0be0d&width=800)

### 什么是 rails

Rails 框架首次提出是在 2004 年 7 月，它的研发者是 26 岁的丹麦人 David Heinemeier Hansson。不同于已有复杂的 Web 开发框架，Rails 是一个更符合实际需要而且更高效的 Web 开发框架。Rails 结合了 PHP 体系的优点（快速开发）和 Java 体系的优点（程序规整），因此，Rails 在其提出后不长的时间里就受到了业内广泛的关注。
 
Ruby on Rails 是一个用于开发数据库驱动的网络应用程序的完整框架。Rails 基于 MVC 设计模式。从视图中的 Ajax 应用，到控制器中的访问请求和反馈，到封装数据库的模型，Rails 为你提供一个纯Ruby的开发环境。发布网站时，你只需要一个数据库和一个网络服务器即可。

Ruby On Rails 是一个用于编写网络应用程序的软件包.它基于一种计算机软件语言 Ruby，给程序开发人员提供了强大的框架支持。你可以用比以前少的多的代码和短的多的时间编写出一流的网络软件。

Ruby On Rails 的指导原则是“不要重复你自己”(Don’t Repeat Yourself, 或DRY)。意思是说你写的代码不会有重复的地方.比如以往数据库的接口往往是类似的程序代码但是在很多地方都要重复用到.这无论是给编写还是维护都造成了很大的代价。相反，Ruby On Rails 给你提供了绝大多数的支持，让你只需要短短的几行代码就可以实现强大的功能。而且，Rails 提供了代码生成工具，让你甚至不需要编写一行代码就实现强大的管理程序.

Ruby On Rails 通过 reflection 和 runtime extension 减少了对 configuration 文件的依靠，这和 Java，C# 语言的方向有很大不同，让你减少了很多配置和部署的麻烦，但是性能上却完全可以应付一般网站的需求.
 
Rails 支持各类网络服务器和数据库。在服务器方面，我们推荐 Apache、 lighttpd 或 nginx 代理至 Mongrel （或者使用 FastCGI）。数据库方面，你可以采用 MySQL、PostgreSQL、SQLite、Oracle、SQL Server、DB2、或其他任何我们支持的系统。 Rails 可以在各类操作系统上运行，不过我们建议采用基于 unix 的系统进行开发。

### 什么是 rbenv 和 RVM

rbenv 和 RVM 都是目前流行的 Ruby 环境管理工具，它们都能提供不同版本的 Ruby 环境管理和切换，用来保持整个项目团队所使用的 Ruby 版本一致，以便于自动化安装和管理 CocoaPods 等第三方 Ruby 工具。

至于选择哪个看个人习惯，你可以参考 rbenv 官方的 [Why choose rbenv over RVM?](https://github.com/rbenv/rbenv/wiki/Why-rbenv%3F)

你可以使用 Homebrew 来安装 rbenv。

```
brew install rbenv ruby-build rbenv-vars
```

安装完成后，把以下的设置信息放到你的 Shell 配置文件里面，以保证每次打开终端的时候都会初始化 rbenv。

```
export PATH="$HOME/.rbenv/bin:$PATH" 
eval "$(rbenv init -)"
```

接着安装和设置项目的 Ruby 环境

```
$ cd $(PROJECT_DIR)
$ rbenv install 2.7.1
$ rbenv local 2.7.1
```

设置完成后会生成一个 .ruby-version 文件，该文件中保存了 Ruby 环境版本号。你可以将该文件用 Git 进行管理，这样团队内就可以使用同一版本的 Ruby 开发环境了。

![](https://cdn.nlark.com/yuque/0/2021/png/12376889/1618645160650-7f239c58-41bd-4f2d-847d-3635c1b3e5b0.png#clientId=uf4f204d0-23e1-4&from=paste&height=474&id=u69bd018e&margin=%5Bobject%20Object%5D&originHeight=474&originWidth=1080&originalType=binary&size=213165&status=done&style=none&taskId=u8b2c7050-b464-4287-a6c4-ffe943e245c&width=1080)

参考资料：[https://github.com/rbenv/rbenv](https://github.com/rbenv/rbenv)

### 什么是 RubyGems 

> The RubyGems software allows you to easily download, install, and use ruby software packages on your system. The software package is called a “gem” which contains a packaged Ruby application or library.

RubyGems 是 Ruby 的一个依赖包管理工具，管理着 Gem。用 Ruby 编写的工具或依赖包都称为 Gem。

RubyGems 还提供了 Ruby 组件的托管服务，可以集中式的查找和安装 library 和 apps。当我们使用 gem install 命令安装 Gem 时，会通过 rubygems.org 来查询对应的 Gem Package。而 iOS 日常中的很多工具都是 Gem 提供的，例如 Bundler，fastlane，jazzy，CocoaPods 等。

在默认情况下 Gems 总是下载 library 的最新版本，这无法确保所安装的 library 版本符合我们预期。因此还需要 Gem Bundler 配合。

![](https://cdn.nlark.com/yuque/0/2021/png/12376889/1618646566177-110f87c1-d2a4-4ef0-b7ee-b9a6b09c389d.png#clientId=uf4f204d0-23e1-4&from=paste&height=200&id=u9b1b0575&margin=%5Bobject%20Object%5D&originHeight=200&originWidth=200&originalType=binary&size=69528&status=done&style=none&taskId=uc8a57254-3e9e-4af4-b745-b9dc43a502f&width=200)

### 什么是 Bundler

Bundler 是一个管理 Gem 依赖的 Gem，用来检查和安装指定 Gem 的特定版本，它可以隔离不同项目中 Gem 的版本和依赖环境的差异。

你可以执行 gem install bundler 命令安装 Bundler，接着执行 bundle init 就可以生成一个 Gemfile 文件，你可以在该文件中指定 CocoaPods 和 fastlane 等依赖包的特定版本号，比如：

```
source "[https://rubygems.org"](https://rubygems.org")
gem "cocoapods", "1.10.0"
gem "fastlane", "> 2.174.0"
```

然后执行 bundle install 来安装 Gem。 Bundler 会自动生成一个 Gemfile.lock 文件来锁定所安装的 Gem 的版本。

如果你需要保证团队成员都使用版本号一致的 Gem，就把 Gemfile 和 Gemfile.lock 一同保存到 Git 里面统一管理起来。

![](https://cdn.nlark.com/yuque/0/2021/png/12376889/1618646866624-0a6506e9-5cd5-49c7-8fb1-f201dc89db81.png#clientId=uf4f204d0-23e1-4&from=paste&height=150&id=u902ac39b&margin=%5Bobject%20Object%5D&originHeight=150&originWidth=253&originalType=binary&size=7594&status=done&style=none&taskId=u74d2d4d5-2081-4229-aabc-224ffc84fb3&width=253)

参考资料：[https://www.bundler.cn/](https://www.bundler.cn/)


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

推荐好用的工具。

### Application Name

**推荐来源**：

**地址**：

**软件状态**：

**使用介绍**



## 联系我们

[摸鱼周报第三期](https://zhangferry.com/2021/01/10/iOSWeeklyLearning_3/)

[摸鱼周报第四期](https://zhangferry.com/2021/01/24/iOSWeeklyLearning_4/)

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

[摸鱼周报第六期](https://zhangferry.com/2021/03/14/iOSWeeklyLearning_6/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
