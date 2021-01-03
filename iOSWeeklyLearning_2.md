# iOS摸鱼周报 第二期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享大家开发过程遇到的经验教训及学习内容。成立的目的一个是开发知识碎片化，需要有一个地方去总结并用于回顾；另一个是为了提醒自己不断学习，内卷日益严重的开发环境下，不进则退。

虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug遭遇。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips

开发小技巧收录。

### 几个有用的git命令

**覆盖最近一次commit**

当我们开发完一部分功能时，会提交commit，如果这时发现对应的功能少改了一些东西，我们可以单独提一个commit标记这个小改动，但更推荐的做法是将这两次改动合并为同一个，对应的命令是：

```bash
$ git commit --amend -m "message"
```

**合并多个commit**

如果想将已经生成的多个commit进行合并，可以使用：

```bash
$ git rebase -i [startpoint] [endpoint]
$ git rebase -i HEAD~2 # 合并最近两次提交
```

endpoint默认为当前分支指向的HEAD节点。参数-i表示interactive(交互)，该命令执行之后会进入一个vim的交互编辑界面，下面会有一些参数的说明：

```
pick：保留该commit（缩写:p）
reword：保留该commit，但我需要修改该commit的注释（缩写:r）
edit：保留该commit, 但我要停下来修改该提交(不仅仅修改注释)（缩写:e）
squash：将该commit和前一个commit合并（缩写:s）
fixup：将该commit和前一个commit合并，但我不要保留该提交的注释信息（缩写:f）
exec：执行shell命令（缩写:x）
drop：我要丢弃该commit（缩写:d）
```

**永久删除git内二进制**

如果我们开发中忘了把某二进制文件加入`.gitignore`，而放入了git文件，那它就会一直存在。比如Pod目录，当引入很多库时，git文件会越来越大，即使后面再加入到`.gitignore`，git历史里也会存有记录，这个是无法删除的。好在git给我们提供了一个补救措施：

```
git filter-branch --tree-filter 'rm -f target.file'
```

后面的命令里可以执行删除语句。注意该命令会重写整个git历史，多人协作时更应该慎用。

**git仓库迁移**

git仓库的迁移，在一些git管理平台像是gitlab和github是有的，推荐使用平台提供的方法，如果没有的话我们则可以使用git语句操作：

```bash
git clone --bare git@host/old.git # clone原仓库的裸仓库
cd old.git
git push --mirror git@host/new.git # 使用mirror参数推送至新仓库
```

### 国际化/本地化注意事项

国际化和本地化之间的区别虽然微妙，但却很重要。国际化意味着产品有适用于任何地方的“潜力”；本地化则是为了更适合于“特定”地方的使用，而另外增添的特色。用一项产品来说，国际化只需做一次，但本地化则要针对不同的区域各做一次。这两者之间是互补的，并且两者合起来才能让一个系统适用于各地。

除了大头的语言本地化，还有布局、字符、日期、数字等本地化工作，更多了解可以参考[iOS国际化及本地化（一）不同语言的差异处理及测试](https://zhangferry.com/2019/08/19/localization_guide/ "iOS国际化及本地化（一）不同语言的差异处理及测试")。

这里讲两点，日期格式和数字表示：

#### 日期格式

日期格式在国内的通常记法是yyyy-mm-dd，年月日的格式，但是不同地区它们的习惯会有所不同，以下按地区划分：

![](https://gitee.com/zhangferry/Images/raw/master/gitee/image.png)

参考：https://zh.wikipedia.org/wiki/%E5%90%84%E5%9C%B0%E6%97%A5%E6%9C%9F%E5%92%8C%E6%97%B6%E9%97%B4%E8%A1%A8%E7%A4%BA%E6%B3%95

### 数字表示

**千分符**在不同地区会有三种写法，逗号`,`、句号`.`、空格` ` ，**小数点**的写法有句号`.`、逗号`,`两种。通常为了便于区分，同一符号不会既做千分符，又做小数点。为了避免歧义，国际标准建议使用空格作为千分符，而不是空格或者小数点。

比如对「一百二十三万四千五百六十七点八九」进行表示：

中国、美国、澳大利亚：1,234,567**.**89

德国、荷兰：1 234 567,89或1**.**234**.**567,89

法国、意大利：1 234 567,89

各个地区对小数点的使用可以看这张图的总结：

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210101223402.png)

参考资料：https://zh.wikipedia.org/wiki/%E5%B0%8F%E6%95%B8%E9%BB%9E

## 那些bug

### Cateogry和Extension使用相同名称扩展的问题

**bug出现的现象是什么样的？**

对SDK的一个类扩展时，使用了相同的名称扩展

Extension扩展

```
@interface LSDeviceInfo (LSWatch)
@property(nonatomic, assign) LSWatchType type;
@end
```

Cateogry扩展，并实现了type的getter方法

```
@interface LSDeviceInfo (LSWatch)
- (LSWatchType)type;
@end
```

错误不是每次都会出现，Xcode12.3一开始是偶现，出现后就一直是报错。

> Unable to execute command: Segmentation fault: 11
> Clang frontend command failed due to signal (use -v to see invocation)
> Diagnostic msg: PLEASE submit a bug report to http://developer.apple.com/bugreporter/ and include the crash backtrace, preprocessed source, and associated run script.
> Diagnostic msg:
PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
Preprocessed source(s) and associated run script(s) are located at:
Diagnostic msg: /var/folders/tp/4kw93qbn7tb20cbpn14fmwk00000gn/T/RLWifiConfigFailedViewController-243a91.m

**是如何解决的？**

将Cateogry扩展和Extension扩展的扩展名设置为不同的，这个错误就解决了。

**bug引发的反思**

extension在编译期决议，它就是类的一部分，在编译期和头文件里的[@interface](https://github.com/interface)以及实现文件里的。
然后category是在运行期加入hashTable表，extension扩展的名称和category一样，这个时候可能在hashTable表上已经有了对应名称的数据，category在加入时就会出错。Xcode这时候也可能错以为维护hashTable表出错，让提交对应的bug到http://developer.apple.com/bugreporter/。

## 编程概念

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

## 优秀博客

[GitHub 2020 报告：全球开发者工作与生活的平衡情况](https://juejin.cn/post/6908880779963695118 "GitHub 2020 报告：全球开发者工作与生活的平衡情况") -- 来自掘金：LeviDing

[2020 腾讯Techo Park - Flutter与大前端的革命](https://juejin.cn/post/6908357007749693454 "2020 腾讯Techo Park - Flutter与大前端的革命") -- 来自掘金：恋猫de小郭

[WWDC20 iOS14 Runtime优化](https://mp.weixin.qq.com/s/opD__14wpHL06VKPtXeM4g "WWDC20 iOS14 Runtime优化") -- 来自公众号：知识小集

[使用 Swift 编写 CLI 工具的入门教程](https://mp.weixin.qq.com/s/V4IdsYUouKGr68ULyb88Qw "使用 Swift 编写 CLI 工具的入门教程") -- 来自公众号：一瓜技术

[阿里 10 年：一个普通技术人的成长之路](https://juejin.cn/post/6908569967289958408 "阿里 10 年：一个普通技术人的成长之路") -- 来自掘金：阿里巴巴云原生

2020年刚过完，有挺多写的非常好的年终总结可以看看：

[写在2020最后一天](https://mp.weixin.qq.com/s/bHcXtxheajtpzPvnPqmHRw) -- 来自公众号：iOS成长之路

[如何持续的自我提升](https://mp.weixin.qq.com/s/ysvDfhF-ckKu2qEZTQSb1A) -- 来自公众号：酷酷的哀殿

[2020 的 cxuan 在掘金 | 掘金年度征文](https://juejin.cn/post/6902212510527520775 "2020 的 cxuan 在掘金 | 掘金年度征文") -- 来自掘金：cxuan

[中年裸辞，我的2020 | 掘金年度征文](https://juejin.cn/post/6901709371294613512 "中年裸辞，我的2020 | 掘金年度征文") -- 来自掘金：Semo

[2020：非适应性完美主义、存在主义哲学、架构、基金翻倍、有效休息｜掘金年度征文](https://juejin.cn/post/6913418068953661448 "2020：非适应性完美主义、存在主义哲学、架构、基金翻倍、有效休息｜掘金年度征文") -- 来自掘金：FeelsChaotic

## 学习资料

### [提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way "提问的智慧")

开发过程中遇到问题是非常常见的，解决问题的过程免不了要向别人或者社区论坛提问，而提问方式的好坏通常决定了你能否获得想要的答案。有这么一个github仓库：[How-To-Ask-Questions-The-Smart-Way](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way) star数高达13.7k，专门讲述如何更有效的提问，很多论坛也将这个作为提问准则，用于提醒大家有效提问的重要性。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210103203707.png)

一个好的提问，即表达了自己对问题答案的渴望，也表达了对解答者的尊重。

### [LeetCode Cookbook](https://books.halfrost.com/leetcode/ "leetcode cookbook")

[halfrost ](https://github.com/halfrost)总结的leetcode算法题解，使用go语言完成，书中各个题目代码都已经beats 100% 了。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210103211318.png)

## 开发利器

推荐好用的开发工具。

### A Companion for SwiftUI

推荐来源：[AlleniCode](https://github.com/AlleniCode)

下载地址：https://apps.apple.com/cn/app/a-companion-for-swiftui/id1485436674?mt=12

软件状态：付费￥328.00

作者的 [SwiftUI 实验室](https://swiftui-lab.com)，A Companion for SwiftUI 是一款可以记录 iOS 和 macOS 平台的 SwiftUI 视图，形状，协议，场景和属性包装的应用程序。该应用程序还包含每种方法的示例，其中有许多都是交互式的，并且嵌入在应用程序中运行。通过使用关联的控件，你可以看到它们对视图的直接影响，以及如何修改你的代码以产生这样的效果。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210103204133.png)



### Go2Shell - 在终端中打开当前Finder目录

推荐来源：[RayLeeBoy](https://github.com/RayLeeBoy)

下载地址：https://zipzapmac.com/go2shell

软件状态：免费

使用介绍：

1. 双击下载的文件, 将Go2Shell拖入Applications目录中
2. 在Applications中, 双击打开Go2Shell, 出现下面的窗口
   ![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210103221327.png)
3. 点击Install Go2Shell to Finder完成安装
4. 打开Finder窗口, 在工具栏中出现Go2Shell图标
5. 点击Go2Shell图标, 就会在终端中打开当前Finder目录

#### 使用 Alfred 制作打开终端的快捷键

这是我目前在用的一种形式，前提是需要安装Alfred：选中某一文件，按下`Command+ T`，就可以打开终端并定位到该文件夹路径。它和Go2Shell实现效果类似，但它可以不依赖Finder，对于桌面文件的操作更友好一些。

实现方式如下：

1、在Workflows里新建HotKeys，编辑快捷键`Command + T`

2、右键该HotKeys > Insert After > Actions > Run Script 新建脚本

3、脚本编辑窗口选择脚本语言：/usr/bin/osascript(AS)，意为Apple Script

4、在脚本框输入如下脚本，保存即可：

```
tell application "Finder"
    -- get selection path
    set pathFile to selection as text
    set pathFile to get POSIX path of pathFile
    -- fix space problem in the directory
    set pathFile to quoted form of pathFile
    tell application "iTerm"
	   create window with default profile
	   tell current session of current window
		  write text pathFile
	   end tell
    end tell
end tell
```

该脚本是针对`iTerm`终端设置的。