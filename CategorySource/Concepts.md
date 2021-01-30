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