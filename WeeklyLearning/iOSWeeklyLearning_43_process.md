# iOS摸鱼周报 第四十二期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：dyld4 开源了。
> * Tips：Fix iOS12 libswift_Concurrency.dylib crash bug 
> * 面试模块：
> * 优秀博客：Swift Protocol 进阶
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：Apple 最近开源了 [dyld4](https://github.com/apple-oss-distributions/dyld/ "dyld4") 的代码。通过阅读它的 Readme 文档，我们可以大致了解到dyld4的相对dyld3做的改进有哪些。dyld3 出于对启动速度的优化，增加了启动闭包。应用首启和发生变化时将一些启动数据创建为闭包存到本地，下次启动将不再重新解析数据，而是直接读取闭包内容。这种方法的理想情况是应用程序和系统应很少发生变化，因为如果这两者经常变化，即意味着闭包可能面临失效。为了因对这类场景，dyld4 采用了 Prebuilt + JustInTime 的双解析模式，Prebuild 对应的就是 dyld3 中的启动闭包场景，JustInTime 大致对应 dyld2 中的实时解析，JustInTime 过程是可以利用 Prebuild 的缓存的，所以性能也还可控。应用首启、包体或系统版本更新、普通启动，dyld4 将根据缓存有效与否选择合适的模式进行解析。所以 dyld4 的设计目标不是更快，而是更灵活。

还有一点，细心的开发者还在 dyld4 源码里发现了 realityOS 及 realityOS_Sim 相关的代码注释。很大可能苹果的 VR/AR 设备已经准备差不多了，静待今年的 WWDC 吧。

## 开发Tips

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Fix iOS12 libswift_Concurrency.dylib crash bug 
最近很多朋友都遇到了iOS12上libswift_Concurrency的crash问题, xcode 13.2 release notes中有提到是Clang编译器bug, 13.2.1 release notes说明已经修复, 但实际测试并没有.

crash的具体原因是xcode编译器在低版本(12)上没有将libswift_Concurrency.dylib库剔除, 反而是将该库嵌入到ipa的Frameworks路径下, 导致动态链接时libswift_Concurrency被链接引发crash

#### error分析过程:
1. 通过报错信息Library not loaded: /usr/lib/swift/libswiftCore.dylib 分析是动态库没有加载, 提示是libswift_Concurrency.dylib引用了该库, 但是libswift_Concurrency只有在iOS15系统上才会存在, iOS12本该不链接这个库, 猜测是类似swift核心库嵌入的方式,内嵌在了ipa包中; 校验方式也很简答, 通过iOS12真机run一下, 崩溃后通过`image list`查看加载的镜像文件会找到libswift_Concurrency的路径是ipa/Frameworks下的, 通过解包ipa也证实了这一点

2. 在按照xcode 13.2 release notes提供的方案, 将libswiftCore设置为weak并指定rpath后, crash信息变更, 此时error原因是`___chkstk_darwin`符号找不到; 根据error Referenced from 发现还是libswift_Concurrency引用的, 通过`nm -u xxxAppPath/Frameworks/libswift_Concurrency.dylib`查看所有未定义符号(类型为U), 其中确实包含了`___chkstk_darwin`, 13.2 release notes中提供的解决方案只是设置了系统库弱引用, 没有解决库版本差异导致的符号解析问题

3. error 提示期望该符号应该在libSystem.B.dylib中, 但是通过找到libSystem.B.dylib并打印导出符号`nm -gAUj libSystem.B.dylib`  发现即使是高版本的动态库中也并没有该符号, 那么如何知道该符号在哪个库呢,  这里用了一个取巧的方式, run iOS13以上真机, 并设置symbol符号`___chkstk_darwin`, xcode会标记所有存在该符号的库, 经过第1&2步骤思考, 认为是在查找libswiftCore核心库时crash的可能性更大

    > libSystem.B.dylib 路径在~/Library/Developer/Xcode/iOS DeviceSupport/xxversion/Symbols/usr/lib/目录下

4. 如何校验呢, 通过xcode上iOS12 && iOS15两个不同版本的libswiftCore.dylib查看导出符号,可以发现, 12上的Core库不存在, 对比组15上是存在的, 所以基本可以断定symbol not found是这个原因造成的; 当然你也可以把其他几个库也采用相同的方式验证

> 通过在 ~/Library/Developer/Xcode/iOS DeviceSupport/xxversion/Symbols/usr/lib/swift/libswiftCore.dylib 不同的version路径下找到不同系统对应的libswiftCore.dylib库, 然后用`nm -gUAj libswiftCore.dylib`可以获取过滤后的全局符号验证
> 
> 库的路径,可以通过linkmap或者运行demo打个断点, 通过LLDB的image list查看

分析总结: 无论是根据xcode提供的解决方案亦或是error分析流程, 发现根源还是因为在iOS12上链接了libswift_Concurrency造成的,既然问题出在异步库, 解决方案也很明了,移除项目中的libswift_Concurrency.dylib库即可

#### 解决方案
##### 使用xcode13.1或者xcode13.3 Beta构建

使用xcode13.1或者xcode13.3 Beta构建, 注意beta版构建的ipa无法上传到App Store
该方法比较麻烦, 还要下载xcode版本, 耗时较多,如果有多版本xcode的可以使用该方法

##### 添加Post-actions 脚本移除

添加脚本,每次构建完成后移除嵌入的libswift_Concurrency.dylib
添加流程: `Edit Scheme... -> Build -> Post-actions -> Click '+' to add New Run Script`, 脚本内容为`rm "${BUILT_PRODUCTS_DIR}/${FRAMEWORKS_FOLDER_PATH}/libswift_Concurrency.dylib" || echo "libswift_Concurrency.dylib not exists"`

  <img src="https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/weekly_43_tips_04.jpeg" style="zoom:50%;" />

##### 降低/移除 使用libswift_Concurrency.dylib的三方库

**查找使用concurrency的三方库, 降低到未引用Concurrency前的版本,后续等xcode修复后再升级**
如果是通过cocoapods管理三方库, 只需要指定降级版本即可.
但是需要解决一个问题,查找三方库中有哪些用到concurrency呢,

如果是源码, 全局搜索相关的`await & async`关键字可以找到部分SDK, 但如果是二进制SDK或者是间接使用的, 则只能通过符号查找
**查找思路:**

1. 首先明确动态库的链接是依赖导出符号的, 即xxx库引用了target_xxx动态库时, xxx是通过调用target_xxx的导出符号(全局符号)实现的, 全局符号的标识是大写的类型, U表示当前库中未定义的符号, 即xxx需要链接其他库动态时的符号, 符号操作可以使用`llvm nm`命令
2. 如何查看是否引用了指定动态库target_xxx的符号? 可以通过linkmap文件查找, 但是由于libswift_Concurrency有可能是被间接依赖的, 此时linkmap中不存在对这个库的符号记录, 所以没办法进行匹配, 换个思路, 通过获取libswift_Concurrency的所有符号进行匹配, libswift_Concurrency的路径可以通过上文提到的`image list`获取, 一般都是用的/usr/lib/swift下的
2. 遍历所有的库, 查找里面用到的未定义符号(U), 和libswift_Concurrency的导出符号进行匹配, 重合则代表有调用关系

​		为了节省校验工作量, 提供`findsymbols.sh`脚本完成查找, 构建前可以通过指定项目中SDK目录查找,或者也可以指定构建后.app包中的Frameworks查找

**使用方法:**

1. 下载后进行权限授权, `chmod 777 findsymbols.sh`
2. 指定如下参数:
	- -f: 指定单个二进制framework/.a库进行检查
    - -p: 指定目录,检查目录下的所有framework/.a二进制SDK
    - -o 输出目录, 默认是`~/Desktop/iOS12 Crash Result`

* [如何检测哪些三方库用了libstdc++](https://www.jianshu.com/p/8de305624dfd?utm_campaign=hugo&utm_medium=reader_share&utm_content=note&utm_source=weixin-friends "如何检测哪些三方库用了libstdc++")
* [After upgrading to Xcode 13.2.1, debugging with a lower version of the iOS device still crashes at launching](https://developer.apple.com/forums/thread/696960 "After upgrading to Xcode 13.2.1, debugging with a lower version of the iOS device still crashes at launching")
* [findsymbols.sh](https://gist.github.com/71f8d3fade74903cae443a3b50c2807f.git "findsymbols.sh")


## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 优秀博客

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[在已实现协议要求方法的类型中如何调用协议中的默认实现](https://holyswift.app/conforming-to-a-protocol-and-using-default-function-implementation-at-the-same-time-in-swift "在已实现协议要求方法的类型中如何调用协议中的默认实现") -- 来自：Leonardo Maia Pugliese

[@东坡肘子](https://www.fatbobman.com/)：能够提供默认实现是 Swift 协议功能的重要特性。本文介绍了在已实现协议要求方法的类型中继续调用协议的默认实现的三种方式。解决的思路可以给读者不小的启发。在每篇博文中附带介绍一副绘画作品也是该博客的特色之一。

2、[通过 Swift 代码介绍 24 种设计模式](https://oldbird.run/design-patterns/ "通过 Swift 代码介绍 24 种设计模式") -- 来自：oldbird

[@东坡肘子](https://www.fatbobman.com/)：设计模式是程序员必备的基础知识，但是没有点年份，掌握也不是这么容易，所以例子就非常重要。概念是抽象的，例子是具象的。具象的东西，记忆和理解都会容易些。该项目提供了 24 种设计模式的 Swift 实现范例，对于想学习设计模式并加深理解的朋友十分有帮助。

3、[Combining protocols in Swift](https://www.swiftbysundell.com/articles/combining-protocols-in-swift/ "Combining protocols in Swift") -- 来自：Sundell

[@东坡肘子](https://www.fatbobman.com/)：组合和扩展均为 Swift 协议的核心优势。本文介绍了如何为组合后的协议添加具有约束的扩展。几种方式各有利弊，充分掌握后可以更好地理解和发挥 Swift 面向协议编程的优势。

4、[Swift Protocol 背后的故事](https://zxfcumtcs.github.io/2022/02/01/SwiftProtocol1/ "Swift Protocol 背后的故事") -- 来自： 赵雪峰

[@东坡肘子](https://www.fatbobman.com/)：本文共分两篇。上篇中，以一个 Protocol 相关的编译错误为引，通过实例对 Type Erasure、Opaque Types 、Generics 以及 Phantom Types 做了较详细的讨论。下篇则主要讨论 Swift Protocol 实现机制，涉及 Type Metadata、Protocol 内存模型 Existential Container、Generics 的实现原理以及泛型特化等内容。

5、[不透明类型](https://blog.mzying.com/index.php/archives/307/ "不透明类型") -- 来自：Mzying

[@东坡肘子](https://www.fatbobman.com/)：不透明类型是指我们被告知对象的功能而不知道对象具体是什么类型。作者通过三个篇章详细介绍了 Swift 的不透明类型功能，包括：不透明类型解决的问题（上）、返回不透明类型（中）、不透明类型和协议类型之间的区别 （下）。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Graphviz

**地址**：http://www.graphviz.org/

**软件状态**：免费

**软件介绍**：

贝尔实验室开发的有向图/无向图自动布局应用, 支持dot脚本绘制结构图, 流程图等。

![Graphviz](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220217174238.png)

对产物`.gz`文件进行解析查看的途径。

- 在线网站：[GraphvizOnline](http://dreampuf.github.io/GraphvizOnline)
- vs 插件：`Graphviz (dot) language support for Visual Studio Code`


结合`cocoapods-dependencies`插件，我们可以解析`podfile`文件来分析项目的`pod`库依赖，生成`.gz`文件。

* 生成`.gz`文件：`pod dependencies --graphviz`
* 生成依赖图：`pod dependencies --image`
* 生成`.gz`文件及依赖图：`pod dependencies --graphviz --image`

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
