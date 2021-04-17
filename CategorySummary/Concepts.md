# 开发概念

### 什么是Makefile

一个工程中的源文件不计其数，其按类型、功能、模块分别放在若干个目录中，而编译通常是一个文件一个文件进行的，对于多文件的情况，又该如何编译呢？

这就是makefile的作用，它就像一个shell脚本（里面也可以执行系统的shell命令），定义了一系列的规则，用于指定哪些文件需要编译，编译顺序，库文件的引用，及一些更复杂的编译操作。

makefile只是定义编译规则，执行这些规则的指令是make命令。

makefile和make常用于Linux及类Unix环境下。

### 什么是CMake

Make工具有很多种，比较出名的有GNU Make（昨天介绍的Make命令通常指GNU Make），QT 的qmake，微软的MS nmake，BSD Make（pmake）等等。

这些 Make 工具遵循着不同的规范和标准，所要求的 Makefile 格式也千差万别。这样就带来了一个严峻的问题：如果软件想跨平台，必须要保证能够在不同平台编译。

这种环境下就诞生了CMake，其通过CMakeList.txt文件来定制整个编译流程，然后根据目标用户的平台进一步生成所需的Makefile和工程文件。达到「Write once, run everywhere」的效果。

Swift的编译过程即是通过CMake定制的，我们可以在源码里发现多个CMakeList.txt文件。

https://github.com/apple/swift/blob/main/CMakeLists.txt

### 什么是xcodebuild

xcodebuild类似GNU里的make，它是一套完整的编译工具，其包括在命令行工具包（Command Line Tools）中。苹果做了很多简化编译的操作，使得开发者不需要像使用make一样编写makefile，仅需根据实际情况指定workspace、project、target、scheme（这几项概念要分清分别指什么东西）即可完成工程的编译。使用`man xcodebuild`可以查看xcodebuild所支持的功能以及使用说明。

其主要有以下功能：

1、build：构建（编译），生成build目录，将构建过程中的文件存放在这个目录下。

2、clean：清除build目录下的文件

3、test：测试某个scheme，scheme必须指定 

4、archive：执行archive，导出ipa包

5、analyze：执行analyze操作

### 什么是xcrun

xcrun 是 Command Line Tools中的一员。它的作用类似RubyGem里的bundle，用于控制执行环境。

xcrun会根据当前的Xcode版本环境执行命令，该版本是通过`xcode-select`设置的，如果系统中安装了多个版本的Xcode，推荐使用xcrun。

xcrun的使用是直接在其后增加命令，比如：`xcrun xcodebuild`，`xcrun altool`。当然xcodebuild和altool也是可以单独运行的，只不过对于多Xcode的环境他们的执行环境究竟使用的哪个版本无法保证。

### 什么是launchd

launchd是一套统一的开源服务管理框架，它用于启动、停止以及管理后台程序、应用程序、进程和脚本。其由苹果公司的Dave Zarzycki编写，在OS X Tiger系统中首次引入并获得Apache授权许可证。

launchd是macOS第一个启动的进程，它的pid为1，整个系统的其他进程都是由它创建的。

当launchd启动后，它会扫描`/System/Library/LaunchDaemons`和`/Library/LaunchDaemons`里的plist文件，并加载他们。

当你输入密码，登录系统之后，launchd会扫描`/System/Library/LaunchAgents`和`/Library/LaunchAgents、~/Library/LaunchAgents`里的plist文件，并加载。

这些plist文件代表启动任务，也叫`Job`，它里面配置了启动任务启动形式的描述信息。

### 什么是Clang

![](https://gitee.com/zhangferry/Images/raw/master/gitee/clang.png)

Clang 是一个C、C++、Objective-C和Objective-C++编程语言的编译器前端。它的目标是提供一个GNU编译器套装（GCC）的替代品，支持了GNU编译器大多数的编译设置以及非官方语言的扩展。作者是克里斯·拉特纳（Chris Lattner）。

clang项目包括clang前端和clang静态分析器。编译器前端的含义是clang不能直接将源码编译成机器码，clange能输出源码的抽象语法树，并将代码编译成LLVM bitcode。

Clang本身性能优异，其生成的AST所耗用掉的内存仅仅是GCC的20%左右，Clang编译Objective-C代码时速度为GCC的3倍，还能针对用户发生的编译错误准确地给出建议。

### 什么是LLVM

LLVM（Low Level Virtual Machine）是一个自由软件项目，它是一种编译器基础设施，以C++写成，包含一系列模块化的编译器组件和工具链，用来开发编译器前端和后端。它是为了任意一种编程语言而写成的程序，利用虚拟技术创造出编译时期、链接时期、运行时期以及“闲置时期”的最优化。

LLVM有两层含义，广义的LLVM是指一个完整的编译器架构，包括前端、后端、优化器等。

狭义的LLVM仅指编译器后端功能的一些列模块和库，由Clange编译出的中间件经过LLVM后端处理变成对应机器码。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/llvm.png)

### 什么是ld

链接器（Linker）是一个程序，它可以将一个或多个由编译器或汇编器生成的目标文件外加库链接为一个可执行文件。

ld是GNU的链接器，llvm4中有了自己的链接器lld，但是lld在macOS上运行还有问题 (http://lists.llvm.org/pipermail/cfe-dev/2019-March/061666.html)，所以当前Xcode使用的链接器仍是ld。

Build Setting里的Other Linker Flags就是制定ld命令的参数。

在Xcode中，它有三个常用的参数：

`-Objc`:链接器就会把静态库中所有的 Objective-C Class 和 Category 都加载到最后的可执行文件中

`-all_load`:会让链接器把所有找到的目标文件都加载到可执行文件中，但有可能会遇到`duplicate symbol`错误

`-fore_load`:需要指定加载库文件的路径，然后将目标文件全部加载到可执行文件中。

### 什么是dyld

dyld（the dynamic link editor）是苹果的动态链接器，负责程序的链接及加载工作，是苹果操作系统的重要组成部分。

dyld跟ld不同点在于它主要是用于加载系统动态库的，在MachO内记录了所依赖的动态库，像是Foundation、UIKit等，应用启动时由dyld进行加载。首次加载会将动态库放至共享缓存，之后需要加载的应用就可以直接访问共享缓存加载这些动态库了，之后链接至主程序。

dyld属于开源项目，地址:https://opensource.apple.com/tarballs/dyld/

### 什么是bitcode

bitcode是编译后的程序的中间表现，在Xcode中bitcode对应的是一个配置，意为是否开启bitcode。

包含bitcode并上传到App Store Connect的Apps会在App Store Connect上编译和链接。包含bitcode可以在不提交新版本App的情况下，允许Apple在将来的时候再次优化你的App 二进制文件。 对于iOS Apps，Enable bitcode 默认为YES，是可选的（可以改为NO）。对于WatchOS和tvOS，bitcode是强制的。如果你的App支持bitcode，App Bundle（项目中所有的target）中的所有的Apps和frameworks都需要包含bitcode。

苹果推荐iOS项目开启bitcode，且强制watchOS必须开启bitcode。

因为包含bitcode的项目会在App Store Connect重新编译，所以其符号表文件依赖编译后的结果，这时就需要从App store connect下载对应dSYM文件。

### 什么是linkmap

我们编写的源码需要经过编译、链接，最终生成一个可执行文件。在编译阶段，每个类会生成对应的`.o`文件（目标文件）。在链接阶段，会把.o文件和动态库链接在一起。

linkmap（Link Map File）指的就是记录链接相关信息的纯文本文件，包含可执行文件的路径、CPU架构、目标文件、符号等信息。其可用于分析iOS编译后各个模块的大小，网上也有一些现成的工具帮助我们直接分析该文件。

在Build Setting里搜map，可以看到`write link map file`选项，里面设置了linkmap文件的导出路径。

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

### 什么是GNU

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210124145056.png)

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

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210124145432.png)

在此之前先说下BDS（Berkeley Software Distribution 伯克利软件套装），它是Unix的衍生系统，在1977至1995年由伯克利大学分校开发和发布，其是去除SyStem V 删除了AT&T专利代码的。

随着该系统的发展，还提出了新的许可协议：BSD License，它在软件使用上提供了最小限度的限制，它允许遵循该协议的软件被二次开发，且开发之后的版本可以闭源。

所以基于BSD发展出了很多类Unix系统，被称为BSD家族，其中最著名的当属FreeBSD。直到现在FreeBSD仍然在很多网站的服务器上运行着。

乔帮主在NextStep时开发了基于FreeBSD的后端Darwin，回归Apple就给带过去了，而这个就是MacOS的内核，之后的iOS，watchOS也都是基于Darwin构建的。

索尼用FreeBSD创造了PS3，PS4。

任天堂用FreeBSD创造了Nintendo Swiftch。

BSD的发展历史：

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210124145540.png)

### 什么是POSIX

POSIX是Portable Operation System Interface的缩写，即可移植操作系统接口，它是由IEEEE为了在Unix上运行软件提出的一系列标准，X表明其对Unix API的传承。

类Unix系统像Linux、MacOS中均实现了对POSIX接口的兼容，其中我们在多线程使用过程中创建的pthread（前面的p即POSIX），就是基于POSIX里的线程标准设计的。



### 什么是DevOps

DevOps[/de'vɒps/]是Development（开发） + Operations（运维）的组合，其实它还包含了测试的环节。DevOps是一组过程，方法和系统的统称，突出重视软件开发人员和运维人员的沟通合作，通过自动化流程来使得软件构建、测试、发布更加快捷、频繁和可靠。

DevOps 希望做到的是软件产品交付过程中IT工具链的打通，使得各个团队减少时间损耗，更加高效地协同工作。

DevOps 通常需要很多工具的介入，Jira、GitLab、Jenkins、Docker、fastlane等。它是CI/CD的延伸，CI/CD是实现DevOps的基础核心。DevOps的实践可以用于增强敏捷开发。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/devops.png)

### 什么是敏捷开发
敏捷开发（Agile software development）是一种应对快速变化的需求的一种软件开发能力。相对于“非敏捷”，更强调程序员团队与业务专家之间的紧密协作、面对面的沟通（认为比书面的文档更有效）、频繁交付新的软件版本、紧凑而自我组织型的团队、能够很好地适应需求变化的代码编写和团队组织方法，也更注重软件开发过程中人的作用。

其描述的是整体软件开发的过程，包含以下几个关键点：

• 迭代、渐进和进化：周期控制在一到四周，迭代的目标要达到一个可用的发行版

• 工作软件是进化的主要手段：合适的工程管理软件Jira、Tower等

• 高效率的面对面沟通：明确一个产品负责人；消息发布，包含最新产品信息，通常依托于大屏显示器，路人可以看到

• 非常短的反馈回路和适应周期：每日立会

• 质量焦点：推荐使用TDD方式开发，使用CI提速开发流程

### 什么是Scrum

Scrum是敏捷开发中的一种方法学。它是用于开发、交付和持续支持复杂产品的一个框架，是一个增量的、迭代的开发过程。

在这个框架中，整个开发过程由若干个短的迭代周期组成，一个短的迭代周期称为一个Sprint，每个Sprint的建议长度是一至四周。在Scrum中，使用产品Backlog来管理产品的需求，产品backlog是一个按照商业价值排序的需求列表，列表条目的体现形式通常为用户故事。Scrum团队总是先开发对客户具有较高价值的需求。在Sprint中，Scrum团队从产品Backlog中挑选最高优先级的需求进行开发。挑选的需求在Sprint计划会议上经过讨论、分析和估算得到相应的任务列表，我们称它为Sprint backlog。在每个迭代结束时，Scrum团队将递交潜在可交付的产品增量。 Scrum起源于软件开发项目，但它适用于任何复杂的或是创新性的项目。Scrum 目前已被用于开发软件、硬件、嵌入式软件、交互功能网络、自动驾驶、学校、政府、市场、管理组织运营，以及几乎我们（作为个体和群体）日常生活中所使用的一切。

Scrum中有三个重要角色：

1. Scrum Master是Scrum教练和团队带头人，确保团队合理的运作Scrum，并帮助团队扫除实施中的障碍；
2. 产品负责人，确定产品的方向和愿景，定义产品发布的内容、优先级及交付时间，为产品投资报酬率负责；
3. 开发团队，一个跨职能的小团队，人数5-9人，团队拥有交付可用软件需要的各种技能。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/scrumcn.png)

### 什么是极限编程

极限编程（英语：Extreme programming，缩写为XP），是一种软件工程方法学，是敏捷软件开发中应用最为广泛和最富有成效的几种方法学之一。如同其他敏捷方法学，极限编程和传统方法学的本质不同在于它更强调可适应性而不是可预测性。

极限编程的支持者认为软件需求的不断变化是很自然的现象，是软件项目开发中不可避免的、也是应该欣然接受的现象；他们相信，和传统的在项目起始阶段定义好所有需求再费尽心思的控制变化的方法相比，有能力在项目周期的任何阶段去适应变化，将是更加现实更加有效的方法。

极限编程包含几个重要的实践：结对编程、编码规范、TDD、重构、持续集成等。

极限编程有5个重要原则：快速反馈、假设简单、增量变化、拥抱变化、高质量工作。

### 什么是结对编程

结对编程（英语：Pair programming）是一种敏捷软件开发的方法，两个程序员在一个计算机上共同工作。一个人输入代码，而另一个人审查他输入的每一行代码。输入代码的人称作驾驶员，审查代码的人称作观察员（或导航员）。两个程序员经常互换角色。

结对编程的理想情况是：在结对编程中，观察员同时考虑工作的战略性方向，提出改进的意见，或将来可能出现的问题以便处理。这样使得驾驶者可以集中全部注意力在完成当前任务的“战术”方面。观察员当作安全网和指南。

但为什么结对编程没有流行开来？这是因为它的优点不好发挥，缺点有着诸多不可控因素。

结对编程中希望达成的：驾驶者可以集中全部注意力在完成当前任务的“战术”方面，观察员当作安全网和指南，这需要很高的配合度才能达成。而合作所产生的交流成本和个性差异也不可忽略。

我想到的结对编程可以发挥的场景有这么两个：

1、对于一些复杂问题的攻坚，两人合作，利用不同思路可能快速解决问题。

2、适合帮助开发者快速熟悉自己所不熟悉的领域，类似老人带新人的模式，它有利于知识的分享和传递。

参考资料：https://blog.csdn.net/csdnnews/article/details/105259918

### 什么是元编程

元编程（Metaprogramming）是计算机编程里一个非常重要、有趣的概念，维基百科中的定义是将元编程描述成一种计算机程序可以将代码看待成数据的能力。简单理解就是，其表达的是一种使用代码生成代码的能力。

现代的编程语言大都会为我们提供不同的元编程能力，从总体来看，根据『生成代码』的时机不同，我们将元编程能力分为两种类型，其中一种是编译期间的元编程，例如：宏和模板；另一种是运行期间的元编程，也就是运行时，它赋予了编程语言在运行期间修改行为的能力，当然也有一些特性既可以在编译期实现，也可以在运行期间实现。

元编程可用于解决通用型的问题，减少样板代码，比如常见的字典和模型的互转问题，它存在很多固定样式，我们期望编写一个方法让它实现自动匹配，即编写一个可以自调整的方法，这个行为就是元编程，而用到的方案是反射。

跟元编程相关的还有一个概念是元类（Metaclass），它是代表构建类对象的类，在这些语言中例如OC，Ruby，Java，Python等都有元类的概念。

还有个为了保持继承关系闭环的概念叫根元类（Root metaclass），这个在OC和Ruby中都要对应概念。

扩展文章：https://onevcat.com/2018/03/swift-meta/

### 什么是关系型数据库

关系型数据库，是指采用了关系模型来组织数据的数据库。

关系模型是在1970年由IBM的研究员E.F.Codd博士首先提出的，在之后的几十年中，关系模型的概念得到了充分的发展并逐渐成为主流数据库结构的主流模型。

简单来说，关系模型指的就是二维表格模型，而一个关系型数据库就是由二维表及其之间的联系所组成的一个数据组织。

关系型数据库的代表是：SQL Server、Oracle、Mysql

他们的优点是容易理解，二维表结构也更贴近现实世界，使用起来也很方便，使用通用的SQL语句就可以完成增删改查等操作。关系型数据库另一个比较大的优势是它的完整可靠，大大降低了数据冗余和数据不一致的概率。

但很多事物都用两面性，关系数据库也不例外，它在处理高并发，通常每秒在上万次的读写请求时，硬盘I/O就会面临很大的瓶颈问题。

### 什么是非关系型数据库
非关系型数据库也叫NoSQL，用于区别依赖SQL语句的关系数据库，NoSQL还有另一层解读：Not only SQL。

非关系型数据库主要是用于解决关系型数据库面临的高并发读写瓶颈，这个类型数据库种类繁多，但都有一个共同点，就是去掉关系数据库的关系型特性，使得数据库的扩展更加容易。

但它也有一定的缺点就是无事务处理，数据结构相对复杂，处理复杂查询时相对欠缺。

非关系数型数据库分为4大类：

文档型：常用于Web应用，典型的有MongoDB、CouchDB

Key-Value型：处理大量数据的高访问负载，内容缓存，典型的有Redis、Oracle BDB

列式数据库：处理分布式的文件系统，典型的有Cassandra、HBase

图形数据库：用于社交网络，推荐系统，典型的有Neo4J、InfoGrid

SQL和NoSQL没有孰强孰弱，NoSQL也并不会代替SQL，只有结合自身的业务特点才能发挥出这两类数据库的优势。

### 什么是ACID
ACID是指数据库管理系统在写入或者更新资料时，为保证事务可靠性，所必须具有的四个特性。
A（atomicity）指原子型：一个事务里的所有操作，要么全部完成，要么全部不完成，不存在中间状态，如果中间过程出错，就回滚到事务开始前的状态。

C（consistency）一致性：在事务开始之前和结束之后，数据库完整性没有被破坏。

I（isolation）隔离性：数据库允许多个并发事务同时对其数据进行读写和修改的能力，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致。

D（durability）持久性：事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。
通常关系型数据库都是遵守这四个特性的，而非关系型数据库通常是打破了四个特性的某几条用于实现高并发、易扩展的能力。

### 什么是数据库范式
简单的说，范式是为了消除重复数据减少冗余数据，从而让数据库内的数据更好的组织，让磁盘空间得到更有效利用的一种标准化规范，满足高等级的范式的先决条件是满足低等级范式。(比如满足2nf一定满足1nf)。

范式只是针对关系型数据库的规范，当前有六种范式：第一范式（1NF）、第二范式（2NF）、第三范式（3NF）、巴斯-科德范式（BCNF），第四范式（4NF）和第五范式（5NF）又被称为完美范式。这里的NF是Normal form的缩写，翻译为范式。

1NF就是每一个属性都不可再分。不符合第一范式则不能称为关系数据库。

2NF要求数据库表中的每个实例或记录必须可以被唯一地区分。

3NF要求一个关系中不包含已在其它关系已包含的非主关键字信息。

BCNF是在3NF基础上，任何非主属性不能对主键子集依赖（在3NF基础上消除对主码子集的依赖）

4NF是消除表中的多值依赖，也就是说可以减少维护数据一致性的工作。

如果它在4NF 中并且不包含任何连接依赖关系并且连接应该是无损的，则关系在5NF 中。

使用的范式越高则表越多，表多就会带来更高的查询复杂度，使用何种范式需跟实际情况而定，通常满足BCNF即可。

### 什么是ER图
ER图是 Entity Relationship Diagram 的简写，也叫实体关系图，它主要应用于数据库设计的概念设计阶段，用于描述数据之间的关系。

它有三种主要元素：

1、实体：表示数据对象，使用矩形表示

2、属性：表示对象具有的属性，使用椭圆表示

3、联系：表示实体之间的关系，使用菱形表示，关联关系有三种：1:1 表示一对一，1：N表示一对多，M : N表示多对多。

使用直线将联系的各方进行连接。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210314140748.png)

横线表示键，双矩形表示弱实体，成绩单依赖于学生而不可单独存在。

### 什么是数据库索引
索引是对数据库表中一列或者多列的值进行排序的一种数据接口。使用索引可以加快数据的查找，但设置索引也是有一定代价的，它会增加数据库存储空间，增加插入，删除，修改数据的时间。

数据库索引能够提高查找效率的原因是索引的组织形式使用B+树（也可能是别的平衡树），B+树是一种多叉平衡树，查找数据时可以利用类似二分查找的原则进行查找，对于大量的数据的查找，它可以显著提高查找效率。

因为使用平衡树的缘故对于删除和新增数据都可能打破原有树的平衡，就需要重新组织数据结构，维持平衡，这就是增加索引耗时的原因。

对于非聚集索引（非主键字段索引），字段数据会被复制一份出来，用于生成索引，所以会增加存储空间。对非聚集索引的查找是先查找到指定值，然后通过附加的主键值，再使用主键值通过聚集索引查找到需要的数据。

参考：[B+树详解](https://ivanzz1001.github.io/records/post/data-structure/2018/06/16/ds-bplustree#1-b%E6%A0%9 "B+树详解") 

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

![](https://gitee.com/zhangferry/Images/raw/master/gitee/nginx.png)

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

![](https://gitee.com/zhangferry/Images/raw/master/gitee/apache.png)

Apache有多个含义：

一是Apache基金会，它是专门为支持开源软件项目而创办的一个非营利性组织，它所发行的软件都遵循Apache协议。

二是Apache服务器，即httpd，它是Apache团队最早开发的项目，由于它的跨平台和安全性的特点，它成为了世界上最流行的Web服务器软件之一。Apache作为服务器跟Nginx是一样的东西，他们都只支持静态网页，Nginx更轻量，Apache则更稳定。

三是Apache协议（Apache Licence），Apache协议的目的是为了鼓励代码共享，并达到尊重原作者的著作权的作用。你可以使用遵循Apache协议的开源框架并投入商用，但要保留其原有协议声明，如果进行了修改也需要进行说明。

### 什么是Tomcat

![](https://gitee.com/zhangferry/Images/raw/master/gitee/tomcat.png)

Tomcat是由Apache基金会推出的一款开源的可实现JavaWeb程序的Web服务器框架，它是配置JSP（Java Server Page）和JAVA系统必备的一款环境。

它与Apache服务器的区别在于，Apache只支持静态网页，比如博客网站，而Tomcat支持JSP，Servlet，可以实现动态的web应用，像是图书管管理系统。两者也可以结合，处理既有动态又有静态的网站。

### 什么是Docker 

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210326231951.png)

理解Docker之前需要知道容器的概念，容器就是一个封闭的开发环境，类似移动端的沙盒，每个沙盒都可以配置不同的程序，甚至相同程序的不同版本，我在沙盒做的操作不会影响别的沙盒程序。

虚拟机也是一种容器，我可以在不同虚拟机的配置里运行不同的程序，他们互不影响。但是虚拟机太占用系统资源了，不同虚拟机占用不同的内核资源，能否把其中一些共性的东西进行共享？当然是可以的，这就是Docker做的事情。

Docker是一家公司，它还做了一个好事情，就是供了很多配置好的镜像资源（一整套的环境搭建），存储在公共的镜像仓库，大大简化了应用的分发，部署流程。

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

### 什么是 SwiftLint

SwiftLint 是 Realm 推出的一款 Swift 代码规范检查工具，可以用来在团队中实施统一编码规范。

SwiftLint 基于 GitHub 公布的 [GitHub Swift Style Guide](https://github.com/github/swift-style-guide) 规则对 Swift 代码进行检查，支持禁用或启用某一些规则，也支持开发者自定义规则。

配置好 SwiftLint 之后，在 Xcode 中直接编译代码，SwiftLint 就会按照预先设置好的代码规范自动检查代码，不符合规范的代码就会通过警告或错误的形式指示给开发者，从而对开发者的代码进行规范。

参考资料：[https://github.com/realm/SwiftLint](https://github.com/realm/SwiftLint)

### 什么是 XCFramework

Apple 在 [WWDC19 - Binary Frameworks in Swift](https://developer.apple.com/videos/play/wwdc2019/416/) 上提出了 XCFramework，它是一种可分发的二进制包，你需要使用 Xcode11+ 创建。XCFramework 包含 framework 或 library 的变体，以便可以在多个平台（iOS、macOS、tvOS 和 watchOS）包括在模拟器上使用。XCFramework 可以是静态的，也可以是动态的，并且可以包含头文件。

有了 XCFramework，你就可以用单个 .xcframework 文件提供多个平台的分发二进制包，构建更方便，不用再通过 lipo 合并出一个通用的 fat framework，且不需要再考虑存在重复架构指令而导致合并失败的问题。

你可以使用 xcodebuild -create-xcframework 命令将多个 framework 或 library 变体合成一个 xcframework。在为 Swift 库构建时，你还需要将 Build Libraries for Distribution 设置为 YES，以便以一种可分发的方式构建库，它告诉编译器在构建库时去生成一个稳定的接口 Switf Module Interface。

```shell
xcodebuild -create-xcframework -framework <path> [-framework <path>...] -output <path> 
xcodebuild -create-xcframework -library <path> [-headers <path>] [-library <path> [-headers <path>]...] -output <path>
```

xcframework 的文件形式如下：

```shell
|____xxx.xcframework
| |____Info.plist
| |____ios-arm64_armv7
| | |____xxx.framework
| |____ios-arm64_i386_x86_64-simulator
| | |____xxx.framework
| |____ios-arm64_x86_64-maccatalyst
| | |____xxx.framework
```

![](https://user-images.githubusercontent.com/76877122/115015504-58896c80-9ee6-11eb-934f-9ef8709958c1.jpeg#id=wuSoh&originHeight=634&originWidth=2918&originalType=binary&status=done&style=none)

参考资料：[https://developer.apple.com/videos/play/wwdc2019/416/](https://developer.apple.com/videos/play/wwdc2019/416/)



