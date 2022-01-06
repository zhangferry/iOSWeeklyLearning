***
来源于我在开发交流群里的每日分享一个编程概念的内容整理，这些内容多参考主流网站介绍外加一些自己的理解。因为概念内容跨度较广，很多也是我不熟悉的领域，如果有解释不对的地方，欢迎大家指正。

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

***
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

***
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

***
本期概念围绕几个操作系统开展，系统能帮助大家了解各个操作系统之间的关系。

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


***
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

***
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

***
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


***
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

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)

### 什么是 Homebrew

[Homebrew](https://brew.sh/index_zh-cn "Homebrew") 是一款 Mac OS 平台下的软件包管理工具，拥有安装、卸载、更新、查看、搜索等很多实用的功能。简单的一条指令，就可以实现包管理，而不用你关心各种依赖和文件路径的情况，十分方便快捷。

安装方法：

```bash
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

国内镜像：

```bash
$ /bin/bash -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```

### 什么是 Ruby

![](https://gitee.com/zhangferry/Images/raw/master/gitee/ruby_image.png)

Ruby 是一种开源的面向对象程序设计的服务器端脚本语言，在 20 世纪 90 年代中期由日本的松本行弘设计并开发。在 Ruby 社区，松本也被称为马茨（Matz）。 

Ruby的设计和Objective-C有些类似，都是受Smalltalk的影响。而这也一定程度促进了iOS开发工具较为广泛的使用Ruby写成。

较为知名的几个由Ruby写成的iOS开发工具有：CocoaPods、Fastlane、xcpretty。那这些库为啥使用Ruby开来发呢？

来自CocoaPods的主要作者Eloy Duran的说法：

> Ruby和Objective-C具有很多来自Smalltalk的特性，有一定相似性；使用Ruby可以在Bundler和RubyGem之间分享代码；早期阶段MacRuby提供了很多解析Xcode projects的方法；作为CLI工具，Ruby具有强大的字符串处理能力。

来自Fastlane工具链的作者之一Felix的说法：

> 已经有部分iOS工具选择了Ruby，像是CocoaPods以及给Fastlane的开发带来灵感的nomad-cli。使用Ruby将会更容易与这些工具进行对接。

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

[参考：版本管理工具及 Ruby 工具链环境](https://mp.weixin.qq.com/s/s2yJEb2P0_Kk-rIpYBi_9A)

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

[参考：iOS开发进阶](https://t1.lagounews.com/kR50RoRgcj04C)

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)

本期选题来源于林永坚的 [iOS开发进阶](https://t8.lagounews.com/dR5FRrRtcO4F8) 课程里的「跨平台架构：如何设计 BFF 架构系统？」这一节内容。如有表述不准确的地方，欢迎指出，定会及时改正。

### 什么是 RESTful

RESTful 里的 REST 是 Representational State Transfer 的缩写，翻译过来就是：表现层状态转化。它是一种互联网软件架构，处理的问题是如何开发在互联网环境中使用的软件。

从含义入手：表现层状态转化。表现层是互联网资源呈现的形式，例如 HTML，JSON 等，转化就是资源等数据的变化，查询数据，更新数据。

RESTful 架构一般满足以下三点即可：

1、一个 URI 代表一种资源

2、客户端和服务器之间，传递这种资源的某种表现层

3、客户端通过 4 个 HTTP 动词，对服务器端资源进行操作，实现“表现层状态转化“。

参考：[理解 RESTful 架构 - 阮一峰](https://www.ruanyifeng.com/blog/2011/09/restful.html "理解 RESTful 架构")

### 什么是 SOAP

SOAP，全称是 Simple Object Access Protocol，即简单对象访问协议。从 W3C SOAP 1.2 版开始，SOAP 这一缩写不再代表 Simple Object Access Protocol，而是仅仅作为协议名称而已。

SOAP 是一种相对古老（比 REST 还要早）的网络通信协议，它主要是基于 XML 进行传输的。SOAP 和 REST 是早期互联网应用常用的两种方案。

对于应用程序开发来说，使程序之间进行因特网通信是很重要的。目前的应用程序通过使用远程过程调用（RPC）在诸如 DCOM 与 CORBA 等对象之间进行通信，但是 HTTP 不是为此设计的。RPC 会产生兼容性以及安全问题；防火墙和代理服务器通常会阻止此类流量。通过 HTTP 在应用程序间通信是更好的方法，因为 HTTP 得到了所有的因特网浏览器及服务器的支持。SOAP 就是被创造出来完成这个任务的。SOAP 提供了一种标准的方法，使得运行在不同的操作系统并使用不同的技术和编程语言的应用程序可以互相进行通信。

参考：[SOAP 简介 - 菜鸟](https://www.runoob.com/soap/soap-intro.html "SOAP 简介 - 菜鸟")

### 什么是 BFF

BFF，全称是 Backend For Frontend，即服务于前端的后端，它是一种解决 REST 接口数据冗余的架构模型。

在 REST 模型下每个接口都对于一个服务器请求，当出现多个端，接口越来越多的情况该架构会面临很多问题。而BFF 就是用于解决这类问题出现的。

你可以把 BFF 当作一个中间层，而引入 BBF 后，前端只需要向 BFF 发送一个请求，由 BFF 与后端进行交互，然后将返回值整合后返回给前端，降低前端与后端之间的耦合，方便前端接入。除了整合数据外，你还可以在 BFF 层对数据进行裁剪过滤，或者其他业务逻辑处理，而不用在多个前端中做相同的工作。当后端发生变化时，你只需要在 BFF 层做相应的修改，而不用修改多个前端，这极大地减少了的工作量。

随着业务的发展，单个 BFF 为了适配多端的差异可能会变得越来越臃肿，可维护性降低，开发成本也会越来越高。这时候就得考虑为对 BFF 层进行拆分，给每种用户体验不同的前端分别对应一个 BFF，比如 PC BFF、移动端 BFF（或者再细拆为 iOS BFF 和 Android BFF） 等等，所以 BFF 也称为面向特定用户体验的适配层。

![BFF](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210430111611.png)

参考：[BFF —— Backend For Frontend](https://www.jianshu.com/p/eb1875c62ad3 "BFF —— Backend For Frontend")

### 什么是 GraphQL

GraphQL（展开为 Graph Query Language）是 Facebook 开发的应用层查询语言，于 2015 年开源。注意这里是查询语言，跟 SQL 的 Structured Query Language 类似，也是一种 DSL。

>  GraphQL 的本质是程序员想对 JSON 使用 SQL。 —— 来自阮一峰的翻译

它是一种 BFF 的实现方案。REST 数据是通过一个个 URI 定位到的，而 GraphQL 的模型更像是对象模型。GraphQL 对你的 API 中的数据提供了一套易于理解的完整描述，使得客户端能够准确地获得它需要的数据，而且没有任何冗余，也让 API 更容易地随着时间推移而演进，还能用于构建强大的开发者工具。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/33034116-558F-40ED-B191-31D9E28715F2.png)

这里 GraphQL 起的是一个 API 网关的作用。

参考：[GraphQL](https://graphql.cn/ "GraphQL")

### 什么是 RPC

RPC，全称是 Remote Procedure Call，即远程过程调用。RPC 是一种进程间通信方式，它允许客户端应用直接调用另一台远程不同计算机上的服务端应用的方法，而不需要了解远程调用的实际通信细节实现。RPC 会做好数据的序列化和传输，使得远程调用就像本地调用一样方便，让创建分布式应用和服务变得更加简单。促使 RPC 诞生的领域既是分布式。

RPC 的工作流程大致是：客户端应用以本地调用的方式发起远程调用，将参数以及附加信息序列化为能够进行网络传输的消息体，并将消息发送给服务端。服务端对收到的消息进行反序列化后执行请求，然后将结果序列化为消息并返回给客户端。最后客户端接收到消息并反序列化得到数据。

![RPC](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210501090439.png)

> RPC 框架可以看作一种代理模式，GoF 的《设计模式》一书中把它称作远程代理。通过远程代理，将网络通信、数据编解码等细节隐藏起来。客户端在使用 RPC 服务的时候，就像使用本地函数一样，无需了解跟服务器交互的细节。除此之外，RPC 服务的开发者也只需要开发业务逻辑，就像开发本地使用的函数一样，不需要关注跟客户端的交互细节。 —— 来自王争的《设计模式之美》

常见的 RPC 框架有：gRPC、Dubbo、rpcx、Motan、thrift、brpc、Tars 等等。


### 什么是 gRPC

gRPC 是 Google 开发的一个高性能、通用的开源 RPC 框架。它使用 HTTP/2 作为传输协议，protocol buffers 作为底层传输格式（默认），protocol buffers 还可以作为接口描述语言。

在 gRPC 里客户端应用可以像调用本地对象一样直接调用另一台不同的机器上服务端应用的方法，使得您能够更容易地创建分布式应用和服务。与许多 RPC 系统类似，gRPC 也是基于以下理念：定义一个服务，指定其能够被远程调用的方法（包含参数和返回类型）。在服务端实现这个接口，并运行一个 gRPC 服务器来处理客户端调用。在客户端拥有一个存根能够像服务端一样的方法。

![gRPC](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210501090350.png)

gRPC 客户端和服务端可以在多种环境中运行和交互 -- 从 Google 内部的服务器到你自己的笔记本，并且可以用任何 gRPC 支持的语言来编写。所以，你可以很容易地用 Java 创建一个 gRPC 服务端，用 Go、Python、Ruby 来创建客户端。此外，Google 最新 API 将有 gRPC 版本的接口，使你很容易地将 Google 的功能集成到你的应用里。

Facebook 的调试工具 [idb](https://fbidb.io/)（作为 WebDriverAgent 的替代者）里的 `idb_companion` 就是一个 gRPC 服务器。

参考：[what-is-grpc](https://grpc.io/docs/what-is-grpc/introduction/ "what-is-grpc")




***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)

该期主题来源于对 [xuan总](https://github.com/crisxuan) 的那篇 [程序必知的硬核知识大全](https://github.com/zhangferry/iOSWeeklyLearning/tree/main/Resources/Books) 的部分总结，引用图片也来源于此，该文档已经过其本人授权放到了周报仓库里，有兴趣的读者可以去下载全文阅读。

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

当前常见的 CPU 位数是 32 位和 64 位，这里的位数是指 CPU 一次可以处理的数据位数，就效率上来说 64 位的 CPU 会比 32 位的 CPU 提高一倍。

架构指的是 CPU 的设计架构，目前主流的架构是 x86 和 ARM 两种。

* x86 是 Intel 芯片选用的架构，它包含 32 位和 64 位，通常 64 位的 x86 架构被表述为 x86_64。该架构芯片多用于 PC 机。
* ARM 架构是一个精简指令集（RISC）处理器架构家族，其多用于嵌入式操作系统及手机端。iPhone 上的 A 系列 CPU 就一直是 ARM 架构。ARM 的发展史从 ARMv1 一直到当前的 ARMv8。初代 iPhone 到 iPhone 3GS 之前使用的是 ARMv6；从 3GS 到 5s 之前使用的 ARMv7 架构，5s 开始使用的 ARMv8。但其实 ARMv8 这个叫法却很少出现，而更多的是 ARM64。这是因为从 v8 版本开始分 32 位和 64 位两种（在这之前没有 64 位），苹果使用的都是 64 位，所以就用 ARM64 代替了。

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

寄存器的命名是跟着 CPU 类型走的，ARM64 类型的 CPU 有 32 个寄存器，以下列出了部分寄存器的特殊作用：

| 寄存器                     | 作用                                 |
| ----------------------- | ---------------------------------- |
| x0、x1、x2、x3、x4、x5、x6、x7 | 保存函数参数及返回值                         |
| x29                     | lr（link register）寄存器，保存函数的返回地址     |
| x30                     | sp（stack pointer）寄存器，保存栈地址         |
| x31                     | pc（program counter）寄存器，指向下一条将执行的指令 |

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

我们都知道内存是用来存储数据的，那么这个 IC 中能存储多少数据呢？D0 - D7 表示的是数据信号，也就是说一次可以输入输出 1 byte = 8 bit 数据。A0 - A9 是地址信号，共10个，表示可以指定 2^10 = 1024 个地址。每个地址都都可存放 1 byte 数据，所以这个 IC 的容量就是 1KB。

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)

这期是对 [程序必知的硬核知识大全](https://github.com/zhangferry/iOSWeeklyLearning/blob/main/Resources/Books/xuan-computer-basic.pdf "程序必知的硬核知识大全") 的第二部分总结，有兴趣的读者可以下载全文阅读。

### 什么是二进制

计算机内部是由 IC 电子元件组成的，其中 CPU 和 内存 也是 IC 电子元件的一种。IC 内部由引脚组成，所有引脚只有两种电压：0V 和 5V，该特性决定了计算机的信息处理只能用 0 和 1 表示，也就是二进制来处理。二进制由几个重要的概念，这里简要介绍下：

**补数**

如果用8位表示一个有符号整数，最高位为符号位，1 的表示为`0000 0001`。那 -1 该如何表示呢？答案是：`1111 1111`。如果你首次看到这个表示法可能很奇怪，为什么不是`1000 0001`呢，其实它是基于加法运算推演出来的结果。我们用让计算机计算`1 - 1`，即`1 + (-1)`，即`0000 0001 + 1111 1111` 结果为 `1 0000 0000`，舍去溢出的高位 1，结果就是 0 。所以 -1 对应到二进制就成了`1111 1111`。从正数到负数的表示，产生了补数的概念，它的计算是这样的：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210522135424.png)

这个就是 1 到 -1 的计算方式。

**移位运算**

移位分两种，逻辑移位和算数移位，看下面示例：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210522223515.png)

逻辑移位会在空缺部分补 0，算数右移会在空缺部分补符号位。左移的话都是补 0，没有区别。

代码中通常使用的 `>>`、`<<`符号都是算数移位，因为右移一位会让数值缩小为原来的一半，所以某些二分查找的写法会使用该技巧。

### 什么是大端小端

计算机硬件主要有两种数据存储方式，大端字节序（Big-Endian）和小端字节序（Little-Endian），其实还有一个中端字节序（Middle- Endian），因为用的很少这里不再介绍。

大端和小端的差别是什么呢，看一个例子。比如 32bit 宽的数`0x12345678`在 小端模式内存中的存放方式（假设从地址0x4000开始存放）为：

| 内存地址 | 0x4000 | 0x4001 | 0x4002 | 0x4003 |
| ---- | ------ | ------ | ------ | ------ |
| 存放内容 | 0x78   | 0x56   | 0x34   | 0x12   |

而在大端模式内存中的存放方式则为：

| 内存地址 | 0x4000 | 0x4001 | 0x4002 | 0x4003 |
| ---- | ------ | ------ | ------ | ------ |
| 存放内容 | 0x12   | 0x34   | 0x56   | 0x78   |

他们的区别是，在低字节处，小端模式存储的是低位，而大端存储的是高位。因为我们的习惯是先看高位后看低位，所以大端更符合人们的直觉；但是处理器在处理数据时先从低位处理效率会更高一些。这就是存在大端小端两种模式的原因。

目前 iOS 和macOS应用都使用的小端模式，可以通过以下方法验证：

```objectivec
if (NSHostByteOrder() == NS_BigEndian) {
     NSLog(@"BigEndian");
} else if (NSHostByteOrder() == NS_LittleEndian) {
     NSLog(@"LittleEndian");
}
```

### 什么是缓存

内存的内部是由各种 IC 电路组成的，它的种类很庞大，但是其主要分为三种存储器：随机存储器（RAM）、只读存储器（ROM）和高速缓存（Cache）。高速缓存通常又会分为一级缓存（L1 Cache）、二级缓存（L2 Cache）、三级缓存（L3 Cache），它位于内存和 CPU 之间，是一个读写速度比内存更快的存储器。以上分类从前往后速度越来越快。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210522223549.png)

为什么会有这么多缓存呢？主要是有两方面的考虑：速度和成本。读取速度越高的设备成本也会越高，为了在这两者之间进行平衡才加入了各个缓存。后者都可以作为前者的缓存，比如可以把主存作为硬盘的缓存，也可以把高速缓存作为主存的缓存。

以下是各种设备的读取速度对比：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210522143424.png)

缓存的使用逻辑大致是，没有对应数据时向上一级寻找，如果找到了就在当级缓存下来，下次再寻找相同的内容就可以直接从当级的缓存调用了。因为作为缓存的部分一般都比其上一级容量更小，所以缓存内容就不可能一直存在，需要按照一定规则进行移除，这就引出了LRU（Least Recently Used，最近最少使用）算法，它是将最近一段时间内最少被访问过的数据淘汰出缓存，提高缓存的利用率。

图片来源：[bowdoin.edu lec18.pdf](https://www.bowdoin.edu/~sbarker/teaching/courses/systems/18spring/lectures/lec18.pdf "bowdoin.edu lec18.pdf")

### 什么是压缩算法

压缩算法 (compaction algorithm) 指的就是数据压缩的算法，主要包括压缩和还原 (解压缩) 的两个步骤。其实就是在不改变原有文件属性的前提下，降低文件字节空间和占用空间的一种算法。 

根据压缩算法的定义，我们可将其分成不同的类型： 

**有损和无损** 

无损压缩：能够无失真地从压缩后的数据重构，准确地还原原始数据。可用于对数据的准确性要求严格的场合，如可执行文件和普通文件的压缩、磁盘的压缩，也可用于多媒体数据的压缩。该方法的压缩比较小。如差分编码、RLE、Huffman 编码、LZW 编码、算术编码。 

有损压缩：有失真，不能完全准确地恢复原始数据，重构的数据只是原始数据的一个近似。可用于对数据的准确性要求不高的场合，如多媒体数据的压缩。该方法的压缩比较大。例如预测编码、音感编码、分形压缩、小波压缩、JPEG/MPEG。 

**对称性** 

如果编解码算法的复杂性和所需时间差不多，则为对称的编码方法，多数压缩算法都是对称的。但也有不对称的，一般是编码难而解码容易，如 Huffman 编码和分形编码。但用于密码学的编码方法则相反，是编码容易，而解码则非常难。 

**帧间与帧内** 

在视频编码中会同时用到帧内与帧间的编码方法，帧内编码是指在一帧图像内独立完成的编码方法，同静态图像的编码，如 JPEG；而帧间编码则需要参照前后帧才能进行编解码，并在编码过程中考虑对帧之间的时间冗余的压缩，如 MPEG。 

**RLE编码**

RLE 是 run-length encoding的缩写，中文翻译为游程编码，是一种根据编码字符次数进行统计的无损压缩算法。举例来说，一组资料串"AAAABBBCCDEEEE"，由4个A、3个B、2个C、1个D、4个E组成，经过 RLE 可将资料压缩为4A3B2C1D4E（由14个单位转成10个单位）。

**哈弗曼编码**

哈夫曼编码是一种使用变长编码表对源符号进行编码的无损压缩编码方式。其特征是对于出现频率较高的字符使用较短的编码符号。对于 AAAAAABBCDDEEEEEF 这几个字符使用哈夫曼编码的结果如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210522213007.png)

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)


### 什么是 BIOS

BIOS 全称为 Basic Input Output System，即基本输入输出系统。BIOS 是预先内置在计算机主机内部的程序，也是计算机开机后加载的第一个程序。BIOS 保存着计算机最重要的基本输入输出的程序、开机后自检程序和系统自启动程序，它可从 CMOS（是电脑主板上的一块可读写的 RAM 芯片）中读写系统设置的具体信息。

BIOS 除了键盘，磁盘，显卡等基本控制程序外，还有`引导程序`的功能。引导程序是存储在启动驱动器起始区域的小程序，操作系统的启动驱动器一般是硬盘。不过有时也可能是 CD-ROM 或软盘。

电脑开机后，BIOS 会确认硬件是否正常运行，没有异常的话就会直接启动引导程序，引导程序的功能就是把在硬盘等记录的 OS 加载到内存中运行，虽然启动应用是 OS 的功能，但 OS 不可以自己启动自己，而是通过引导程序来启动。

制作黑苹果的时候安装的 Clover 就是一个启动程序，它通过修改 BIOS 配置，让 BIOS 首先执行它，然后由它来引导至 MacOS 的启动。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210527232231.png)

严格意义来说 BIOS 是 IBM PC架构上的一种设计规范，Mac电脑，包括一些新型的主板都没有 BIOS 这一概念，取而代之的是 EFI/UEFI。


### 什么是汇编

汇编语言（Assembly Language）是任何一种用于电子计算机、微处理器、微控制器或其他可编程器件的低级语言，亦称为符号语言。在汇编语言中，用助记符代替机器指令的操作码，用地址符号或标号代替指令或操作数的地址。在不同的设备中，汇编语言对应着不同的机器语言指令集，通过汇编过程转换成机器指令。特定的汇编语言和特定的机器语言指令集是一一对应的，不同平台之间不可直接移植。

汇编语言比机器语言的可读性要好，但跟高级语言比较而言，可读性还是较差。不过采用它编写的程序具有存储空间占用少、执行速度快的特点，这些是高级语言所无法取代的。在实际应用中，是否使用汇编语言，取决于具体应用要求、开发时间和质量等方面作权衡。汇编常用的指令如下：

| 操作码 | 操作数 | 功能                          |
| ------ | ------ | ----------------------------- |
| mov    | A, B   | 把B的值赋给A                  |
| and    | A, B   | 把A和B同时相加，并把结果赋给A |
| push   | A      | 把A的值存储在栈中             |
| pop    | A      | 从栈中读出值，并将其赋值给A   |
| call   | A      | 调用函数A                     |
| ret    | 无     | 处理返回给调用源函数          |


### 什么是虚拟机

虚拟机（Virtual Machine）是指通过软件模拟的具有完整硬件系统功能的、运行在一个完全隔离环境中的完整计算机系统。在实体计算机中能够完成的工作在虚拟机中都能够实现。在计算机中创建虚拟机时，需要将实体机的部分硬盘和内存容量作为虚拟机的硬盘和内存容量。每个虚拟机都有独立的 CMOS、硬盘和操作系统，可以像使用实体机一样对虚拟机进行操作。

虚拟机的主要用处有：

1. 演示环境，可以安装各种演示环境，便于做各种例子
2. 保证主机的快速运行，减少不必要的垃圾安装程序，偶尔使用的程序，或者测试用的程序在虚拟机上运行
3. 避免每次重新安装，银行等常用工具，不经常使用，而且要求保密比较好的，单独在一个环境下面运行
4. 想测试一下不熟悉或者有风险的应用，在虚拟机中随便安装和彻底删除
5. 体验不同版本的操作系统，如 Linux、Mac 等。

虚拟机目前可分为三类：

* 系统虚拟机，例如：VMware
* 程序虚拟机，例如：JVM（Java Virtual Machine）
* 操作系统层虚拟化，例如：Docker


### 什么是外围中断

IRQ（Interrupt Request）代表的就是中断请求。IRQ 是用来暂停当前正在运行的程序，并跳转到其他程序运行的必要机制。该机制被称为处理中断。中断处理在硬件控制中担当着重要的角色。因为如果没有中断处理，就有可能无法顺畅进行处理的情况。

从中断处理开始到请求中断的程序（中断处理程序）运行结束之前，被中断的程序（主程序）的处理是停止的。这种情况就类似于在处理文档的过程中有电话打进来，电话就相当于是中断处理。假如没有中断处理的发生，就必须等到文档处理完成后才能够接听电话。由此可见，中断处理有着巨大的价值，就像是接听完电话后会返回原来的文档作业一样，中断程序处理完成后，也会返回到主程序中继续。

![中断请求示意图](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210526233248.png)

**实施中断请求的是连接外围设备的 I/O 控制器，负责实施中断处理的是 CPU。**

假如有多个外围设备进行中断请求的话， CPU 需要做出选择进行处理，为此，我们可以在 I/O 控制器和 CPU 中间加入名为中断控制器的 IC 来进行缓冲。中断控制器会把从多个外围设备发出的中断请求有序的传递给 CPU。中断控制器的功能相当于就是缓冲。下面是中断控制器功能的示意图

![中断控制器的功能](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210526233322.png)


### 什么是 DMA

DMA 全称为 Direct Memory Access，即直接存储器访问。DMA 是一种内存访问机制，它是指在不通过 CPU 的情况下，外围设备直接和主存进行数据传输。磁盘等硬件设备都用到了 DMA 机制，通过 DMA，大量数据就可以在短时间内实现传输，之所以这么快，是因为 CPU 作为中介的时间被节省了，下面是 DMA 的传输过程


![使用 DMA 的外部设备和不使用 DMA 的外部设备](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210527220519.png)


I/O 端口号、IRQ、DMA 通道可以说是识别外围设备的 3 点组合。不过，IRQ、DMA 通道并不是所有外围设备都具备的。计算机主机通过软件控制硬件时所需要的信息的最低限，是外围设备的 I/O 端口号。IRQ 只对需要中断处理的外围设备来说是必须的，DMA 通道则只对需要 DMA 机制的外围设备来说必须的。

***
从本期开始，编程概念模块将介绍前端相关的多个概念。本期带来的内容是对 `React`、`React Native`、`Vue` 的介绍。如有错误，欢迎指正。

### 关于前端

通常我们说的前端有两个含义，一个是特指 Web 前端，其跟移动端平级；另一个指大前端，其包含移动端。这里咱们取的含义是 Web 前端。

Web 前端的主要技术是围绕 HTML/CSS、 JavaScript 发展的。在过去的十年里，得益于 JS，网页变得更加动态化和强大，我们把很多的服务端代码放到了浏览器中，这样就产生了成千上万行的 JS 代码，它们链接了各式各样的 HTML 和 CSS 文件，但缺乏正规的组织形式，这就是为什么越来越多的开发者使用 JS 框架来组织代码，诸如 React、Vue、Angular 等。

### 什么是 React

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210605211826.png)

内容整理：[zhangferry](https://zhangferry.com)

[React](https://reactjs.org/) 是由 Facebook 开发的用于构建用户界面的 JavaScript 库，其已开源在 Github，拥有 169k 的超高 star 数，在前端领域使用极广泛。

它有这三大特性：

* 声明式：React 使创建交互式 UI 变得轻而易举，为你应用的每一个状态设计简洁的视图，当数据变动时 React 能高效更新并渲染合适的组件。
* 组件化：构建管理自身状态的封装组件，然后对其组合成复杂的 UI。
* 一次学习，扩平台编写：无论你现在使用什么技术栈，在无需重写现有代码的前提下，都可以通过引入 React 来开发新功能。React 还可以使用 Node 进行服务器渲染，或使用 [React Native](https://reactnative.dev/) 开发原生移动应用。

我们来看一个官网的例子来简单了解下 React 的使用，我们的目的是要实现一个前端 Markdown 渲染的效果，上面是输入框，下面是渲染的 HTML 效果，这里使用一个名为 **remarkable** 的外部库，代码如下：

```java
// React.Component 就是内置组件，其有一系列组件
class MarkdownEditor extends React.Component {
  // 构造函数，类似init
  constructor(props) {
    super(props);
    // 外部库
    this.md = new Remarkable();
    // 绑定自身变化
    this.handleChange = this.handleChange.bind(this);
    // 默认内容
    this.state = { value: 'Hello, **world**!' };
  }
	// 监听输入框的变化
  handleChange(e) {
    this.setState({ value: e.target.value });
  }
	// 渲染出的html
  getRawMarkup() {
    return { __html: this.md.render(this.state.value) };
  }
	// 界面
  render() {
    return (
      <div className="MarkdownEditor">
        <h3>Input</h3>
        <label htmlFor="markdown-content">
          Enter some markdown
        </label>
        <textarea
          id="markdown-content"
          onChange={this.handleChange}
          defaultValue={this.state.value}
        />
        <h3>Output</h3>
        <div
          className="content"
          dangerouslySetInnerHTML={this.getRawMarkup()}
        />
      </div>
    );
  }
}
// 渲染
ReactDOM.render(
  <MarkdownEditor />,
  document.getElementById('markdown-example')
);
```

### 什么是 React Native

内容整理：[我是熊大](https://juejin.cn/user/1151943916921885/posts)

[React Native](https://reactnative.dev/) 是一个使用 `React` 和应用平台的原生功能来构建 Android 和 iOS 应用的开源框架，其已经不是一个 Web 前端框架，而是一个移动端框架。通过 React Native，可以使用 JavaScript 来访问移动平台的 API，以及使用 React 组件来描述 UI 的外观和行为：一系列可重用、可嵌套的代码。通过一张图简单了解下 React Native 在移动开发中的架构：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210605200722.png)

其具有这些特点：跨平台（JavaScript 框架）虚拟 DOM、热更新，iOS 审核有限制、对 Web 开发者友好，上手快，性能几乎和原生相当。

React Native 的不足：
- 由于 React Native 和原生交互依赖的只有一个 Bridge，而且 JS 和 Native 交互是异步的，所以对于需要和 Native 大量实时交互的功能可能会有性能上的不足，比如动画效率，性能是不如原生的。
- React Native 始终是依赖原生的能力，所以摆脱不了对原生的依赖，相对 Flutter 的自己来画 UI 来说，React Native 显得有些尴尬。

引入 React Native 是基于 JavaScript 实现的，所以要在 iOS 端使用它的话，我们就需要安装 `Node.js`，并利用 Node 工具安装 React Native。以下介绍一个简单步骤：
```bash
# 使用 Homebrew 来安装 Node
brew install node

# 安装 yarn
npm install -g yarn

# 创建项目
npx react-native init MoyuDemo

cd MoyuDemo

yarn ios
```
参考资料：[React Native 中文网](https://reactnative.cn/docs/getting-started "React Native 中文网")，[React Native 原理与实践](https://zhuanlan.zhihu.com/p/343519887 "React Native 原理与实践")

### 什么是 Vue

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210605011045.png)

内容整理：[师大小海腾](https://juejin.cn/user/782508012091645)

[Vue](https://cn.vuejs.org/)（读音 /vjuː/）即 Vue.js。作者尤雨溪曾在知乎回答到，Vue 之所以叫 Vue，是因为它是个视图层库，而 vue 是 view 的法语。其是一套用于构建用户界面的**渐进式** JS 框架。

**渐进式的含义是它被设计为可以自底向上逐层应用。**

这是 Vue 与其他 JS 框架最大的不同。渐进式框架简单理解就是：你可以只用我的一部分，而非必须用我的全部；你可以仅将我作为应用的一部分嵌入，而非必须全部使用。Vue 支持你根据实际需求，在不同的阶段使用 Vue 中不同的功能，用最小最快的成本一步步搭建应用，不断渐进，而不是要求你一下子用上全家桶（vue-cli、vue-router、vuex 等）。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210605012155.png)

你可以看看：[Vue 作者尤雨溪：Vue 2.0，渐进式前端解决方案](https://mp.weixin.qq.com/s?__biz=MzUxMzcxMzE5Ng==&mid=2247485737&idx=1&sn=14fe8a5c72aaa98c11bf6fc57ae1b6c0&source=41#wechat_redirect "Vue作者尤雨溪：Vue 2.0，渐进式前端解决方案")

**Vue 的核心库只关注视图层，通过尽可能简单的 API 实现响应的数据绑定和组合的视图组件**

在 HTML 中，DOM 就是视图，我们把 HTML 中的 DOM 与其他的部分独立开来划分出一个层次，这个层次就叫做视图层。如果页面元素很多，数据和视图像传统开发一样全部混合在 HTML 中话就很难维护，因此我们要把视图层抽取出来并且单独去关注它。Vue 只关注视图层，是一个构建数据的视图集合。

Vue 支持数据的双向绑定。即数据变化驱动视图更新，视图更新也会驱动数据变化。而我们只需要通过简单的 API 即可实现这种绑定关系。

Vue 允许你将一个网页分割成多个可复用的组件，每个组件都包含属于自己的 HTML、CSS、JS 以用来渲染网页中相应的地方，然后将这些组件自由组合成完整的网页。

**Vue 具有易用、灵活、高效的特点**

- 易用：在有 HTML、CSS、JavaScript 的基础上，可以快速上手
- 灵活：不断繁荣的生态系统，可以在一个库和一套完整框架之间自如伸缩
- 高效：20kB min+gzip 运行大小，超快虚拟 DOM，最省心的优化

**一个例子**

我们来看一个使用 Vue 写出来的小例子：一个输入框，一个文本，文本能够根据输入框内容的变化而变化：

HTML代码：

```html
<div id="app-6">
  <p>{{ message }}</p>
 	<!-- Vue 提供了 v-model 指令，它能轻松实现表单输入和应用状态之间的双向绑定 -->
  <input v-model="message">
</div>
```

JS 代码：

```javascript
var app6 = new Vue({
  el: '#app-6',
  data: {
    message: 'Hello Vue!'
  }
})
```


***
### BootStrap

内容整理：[zhangferry](https://zhangferry.com)

目前 Web 应用广泛使用在 PC、Pad、移动端等多个平台，但各个端的布局样式相差较大，如果能使用统一的方式描述布局将是非常有必要的，而这就是 BootStrap 的主要功能之一。

BootStrap 最初由 Twitter 开发，后在Github [开源](https://github.com/twbs/bootstrap)。它除了解决不同端统一布局的问题，还封装了很多可重用的组件，例如下拉菜单，弹框等，可以直接调用。另外它还提供一套优雅的 HTML + CSS 规范，统一了代码风格。

前端框架很多，但即使再多也都是围绕 HTML + CSS + JavaScript 展开的。前一篇讲的 React、Vue 都是工作在 JavaScript 这一层的，BootStrap 则主要工作在 HTML、CSS 这一层。

这个网站整理了很多基于 BootStrap 建立的站点：https://www.youzhan.org/

### 什么是 Webpack

内容整理：[师大小海腾](https://juejin.cn/user/782508012091645)

近年来 Web 应用变得更加复杂与庞大，它们拥有着复杂的 JavaScript 代码和一大堆依赖包。为了简化开发的复杂度，前端社区涌现出很多好的实践方法：

* 模块化，让我们可以把复杂的程序细化为小的文件；
* 类似于 TypeScript 这种在 JavaScript 基础上拓展的开发语言：使我们能够实现目前版本的 JavaScript 不能直接使用的特性，并且之后还能能转换为 JavaScript 文件使浏览器可以识别；
* scss，less 等 CSS 预处理器；

这些改进确实大大的提高了我们的开发效率，但是利用它们开发的文件往往需要进行额外的处理才能让浏览器识别，而手动处理又是非常繁琐的，这就为 Webpack 这一类的工具的出现提供了需求。

其官网的首页图很形象的画出了 Webpack 是什么，如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210612002026.png)

其是一个用于现代 JavaScript 应用程序的 静态模块打包工具。当 Webpack 处理应用程序时，它会在内部构建一个 [依赖图(dependency graph)](https://webpack.docschina.org/concepts/dependency-graph/)，此依赖图对应映射到项目所需的每个模块，并生成一个或多个 bundle。

参考：[gwuhaolin/dive-into-webpack](https://github.com/gwuhaolin/dive-into-webpack "gwuhaolin/dive-into-webpack")，[什么是webpack打包工具以及其优点用法](https://blog.csdn.net/weixin_42941619/article/details/87706623 "什么是webpack打包工具以及其优点用法")

### 什么是 Flutter

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210613093819.png)

内容整理：[我是熊大](https://juejin.cn/user/1151943916921885/posts)

Flutter 是目前开发者首选的跨平台开发框架。Flutter 2.2在 Google I/O 2021 大会上正式发布，从移动设备扩展到 web、桌面设备以及嵌入式设备，真正实现了全端覆盖。

Flutter的核心原则是一切皆为 widget，与其他将视图、控制器、布局和其他属性分离的框架不同，Flutter具有一致的统一对象模型：widget。

> 当前iOS的界面元素由 UIView + UIViewController + AutoLayout 组合而成，到了 SwiftUI 则统一用 View 描述，类似 Flutter 的 widget。

其使用声明式语法，比如实现一个简单 widget padding 的功能：

```dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(
      title: Text("Sample App"),
    ),
    body: Center(
      child: CupertinoButton(
        onPressed: () {
          setState(() { _pressedCount += 1; });
        },
        child: Text('Hello'),
        padding: EdgeInsets.only(left: 10.0, right: 10.0),
      ),
    ),
  );
}
```

Flutter 拥有更优的性能，主要原因就是它用于一套自己独有的渲染引擎，其整理架构如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210613103605.png)

Flutter 仍有一些缺点，即导致包体变大，iOS 引入后，包体积增加 10MB 左右。

推荐文章：[Flutter实用教程](https://flutter.cn/docs/cookbook "Flutter实用教程")


***************************************************************************