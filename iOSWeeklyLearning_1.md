# iOS摸鱼周报 第一期
iOS摸鱼周报，分享大家开发过程遇到的经验教训及学习内容。成立的目的一个是开发知识碎片化，需要有一个地方去总结并用于回顾；另一个是为了逼迫自己不断学习，内卷日益严重的开发环境下，不进则退。

虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug遭遇。

如果你感觉这期内容对你有帮助（不用一键三连），欢迎贡献你自己的开发小技巧和解bug遭遇，让下期周报可以如约发出。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips

开发小技巧收录。

### IAP内购管理

推荐来源：[zhangferry](https://github.com/zhangferry)

处理内购时，如果我们需要应用内增加取消内购的入口，因为我们无法直接取消内购，只能将用户指引至苹果的内购管理界面，由用户在那里操作。管理内购的链接有两个：

* https://buy.itunes.apple.com/WebObjects/MZFinance.woa/wa/manageSubscriptions

* https://apps.apple.com/account/subscriptions

前者是旧版链接，mac端能正常访问，但部分iPhone机型访问不了；后者为新版链接，多端都可以访问，最新版苹果文档标注推荐使用第二个链接。

### 除数为0的情况

推荐来源：[zhangferry](https://github.com/zhangferry)

```swift
var num1: Int = 0
var re1 = 10 / num1
print(re1)
```

这里会crash，出错信息为：`Fatal error: Division by zero`

```swift
var num2: Double = 0
var re2 = 10.0 / num2
print(re2)
```

将Int改为Double则不会crash，输出结果为`inf`，代表无限大

```swift
var re3 = Int(re2)
print(re3)
```

将`re2`转成Int还是会crash，出错信息为：`Fatal error: Double value cannot be converted to Int because it is either infinite or NaN`

为什么在数学中无意义的除0操作，用Int除时会crash，在Double除时不crash呢，还得到了一个inf。

首先说Double，它有两个特殊的值，inf和nan，前者代表无限大，后者代表无意义，nan是0/0的结果。

那为什么Int会crash呢，甚至在显式地将0作为除数时会被编译器识别并报错。这是因为Int不能代表无限大，Int根据CPU是32还是64位会有对应最大值 2^31-1 和 2^63-1 。所以它不能表示所有自然数，也就没有无限大的概念，所以在做除数会出现崩溃。

除了Swift，OC，C，C++，Java都是这样设计的设计，其他语言没验证，但我估计应该也应该沿用这个思路，0不能做Int的除数但可以做Float和Double这种浮点型的除数。

### 使用altool上传IPA至AppStore脚本

推荐来源：[tzqiang](https://github.com/tzqiang)

脚本主要功能为以下内容：

```shell
validate_upload_ipa() {
  validate=`xcrun altool --validate-app -f ${ipa_file} -t ios --apiKey ${api_key} --apiIssuer ${api_issuer} --verbose ;echo $?`
  echo -e "\033[34m 校验结果: ${validate} \033[0m"
  validate_code=${validate:0-1}
  
  if [[ ${validate_code} == 1 ]]; then
    echo -e "\033[31m 校验ipa文件失败！请排查错误日志进行调整 \033[0m"
  else
    echo -e "\033[32m ipa文件校验成功！准备上传中...... \033[0m"
    
    upload=`xcrun altool --upload-app -f ${ipa_file} -t ios --apiKey ${api_key} --apiIssuer ${api_issuer} --verbose ;echo $?`
    echo -e "\033[34m 上传结果: ${upload} \033[0m"
    upload_code=${upload:0-1}

    if [[ ${upload_code} == 1 ]]; then
      echo -e "\033[31m 上传ipa文件失败！请排查错误日志进行调整 \033[0m"
    else
      echo -e "\033[32m ipa文件上传成功！ \033[0m"
    fi
  fi
}
```

完整内容可以查看这里：https://github.com/tzqiang/iOS_Shell/blob/main/upload_ipa.sh

## 那些bug

### UITableview刷新导致的问题偏移错误

推荐来源：[once-liu](https://github.com/once-liu)

**bug现象**

UITableView本身未设置`estimatedRowHeight`，Cell固定高度，在执行`deleteRowsAtIndexPaths`、`reloadRows`或者`realodData`等刷新方法时，在部分系统版本会导致一定程度的异常偏移，即contentOffset.y偏移异常。

**解决方案**

该bug与 `estimatedRowHeight` 有关，尝试设置了 `estimatedRowHeight`与 `rowHeight`值相同，问题得以解决。

**bug解释**

查看官方文档中对于`estimatedRowHeight`的解释：

> Providing a nonnegative estimate of the height of rows can improve the performance of loading the table view. If the table contains variable height rows, it might be expensive to calculate all their heights when the table loads. Estimation allows you to defer some of the cost of geometry calculation from load time to scrolling time.
> The default value is UITableViewAutomaticDimension, which means that the table view selects an estimated height to use on your behalf. Setting the value to 0 disables estimated heights, which causes the table view to request the actual height for each cell. If your table uses self-sizing cells, the value of this property must not be 0.
> When using height estimates, the table view actively manages the contentOffset and contentSize properties inherited from its scroll view. Do not attempt to read or modify those properties directly.

`estimatedRowHeight`默认值为`UITableViewAutomaticDimension`，它会自动计算出行高，并会影响contentOffset和 contentSize。而对于特定系统版本才出问题这一现象推测是苹果本身的系统bug，在自动预估高度时会出现偏差导致的。

### cURL上传脚本问题排查

推荐来源：[zhangferry](https://github.com/zhangferry)

**bug现象**

工程的shell脚本里有一个函数是使用cURL上传文件，原来的机器（MacOS 10.15.5）执行这段代码可以正常工作，更换为一台新设备(MacOS 10.15.7)时就出现上传失败的情况。经过后端同学的测试（Windows和Linux），脚本没有问题，只是在我那台Mac上会上传失败，提示的是找不到文件，但文件的写法经过反复检查是没问题的。

**解决方案**

在设置header时`-H 'content-type: multipart/form-data;’ ` 最后的分号需要去掉。

**bug解释**

正常在curl里header设置就应该是key value的形式，不能有分号。但带分号的写法在`windows`和`linux`电脑都可以正常执行，部分macOS，测试过的机型好像只有10.15.5版本是可以执行的。带分号的写法在出问题的mac电脑上好像影响了后面的参数，致使文件参数读取失效，导致了提示文件找不到。

关于-H的规范设置可以参考这个：https://catonmat.net/cookbooks/curl/add-http-headers

## 编程概念

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

## 优秀博客

[UIView动画降帧探究](https://mp.weixin.qq.com/s/QVvrgWpjY6mxAqjkrRapPw "UIView动画降帧探究") -- 来自公众号：一瓜技术

[llvm 编译器高级用法：第三方库插桩](https://mp.weixin.qq.com/s/RKg8f6B2jSNuFEImtMnq2Q "llvm 编译器高级用法：第三方库插桩") -- 来自公众号：搜狐技术产品

[你不好奇 Linux 是如何收发网络包的？](https://mp.weixin.qq.com/s/ISQ2qutpJjYOdtM3taeO_A "你不好奇 Linux 是如何收发网络包的？") -- 来自公众号：小林coding

[App 启动提速实践和一些想法](https://mp.weixin.qq.com/s/v2Ym9GPU4J8xCFFNYcpJhg "App 启动提速实践和一些想法") -- 来自公众号：starming

[iOS Forensic Toolkit破解iPhone 5和5c密码](https://mp.weixin.qq.com/s/rFkYFJnIbRf0N-7kBlbzXA "iOS Forensic Toolkit破解iPhone 5和5c密码") -- 来自公众号：iOS进阶宝典

[iOS 性能监控：Runloop 卡顿监控的坑](https://mp.weixin.qq.com/s/vMRQ0VuHLxpaY9oCNd5G8w "iOS 性能监控：Runloop 卡顿监控的坑")  -- 来自公众号：老司机技术周报

[漫画：什么是红黑树？](https://juejin.cn/post/6844903519632228365 "漫画：什么是红黑树？") -- 来自掘金：程序员小灰

[iOS编译速度如何稳定提高10倍以上之一](https://juejin.cn/post/6903407900006449160#heading-19 "iOS编译速度如何稳定提高10倍以上之一") -- 来自掘金：Mr_Coder

[我看技术人的成长路径](https://juejin.cn/post/6906006025925558279 "我看技术人的成长路径") -- 来自掘金：阿里巴巴云原生

[App Store App隐私保护问卷填写指引](https://info.umeng.com/detail?id=398&cateId=1 "App Store App隐私保护问卷填写指引") -- 来自友盟：最新资讯

## 学习资料

### [iOS面试资料总结](http://note.youdao.com/s/SvA1l4Gy)

地址：http://note.youdao.com/s/SvA1l4Gy

推荐来源：[pengwj](https://github.com/pengwj)

来自`岁寒啊`的整理，基本涵盖iOS各个方面的知识点，熟练掌握在这内容，再也不怕iOS”八股文“了。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20201220131223.png)

每个章节都会有展开内容，多为直接整，少部分为链接内容。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20201220131326.png)

### [SwiftUI官方教程](https://developer.apple.com/tutorials/app-dev-training)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20201219201033.png)

地址：https://developer.apple.com/tutorials/app-dev-training

苹果官方制作的SwiftUI教程，使用最新的SwiftUI2.0语法，更新了用例，也带来了更多典型功能介绍。教程共分为8个章节，包括语法介绍、页面跳转、数据传递、状态管理、图形绘制等核心知识点。如果你想学习SwiftUI，这绝对是最有用的教程。

### [Bash脚本教程](https://wangdoc.com/bash/)

地址：https://wangdoc.com/bash/

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20201219202410.png)

阮一峰老师制作的Bash脚本教程，主要介绍Linux命令行Bash的基本用法和脚本编程。Bash脚本应该是少有的一个横跨前端、后端及移动端，很多场景都有使用的语言工具。在移动端即使你没有编写Bash脚本的需求，也免不了会需要分析一些脚本的功能。

之前有段时间想系统学习Bash脚本，翻阅很多网站都没有找到满意的文档资料，直到看到这份教程，快快学起来吧。

## 开发利器

较少好用的开发工具。

### Vimac App - control macOS UI with the keyboard only

推荐来源：[beatman423](https://github.com/beatman423)

下载地址：https://vimacapp.com

软件状态：免费、开源

一款Mac上的键盘效率工具，通过用键盘代替鼠标操作从而提高电脑使用效率，非常适合程序员使用。
功能简介：

* 快捷键“Ctrl+Space”激活点击模式，输入提示字母完成鼠标单击操作，按住“Shift”键输入提示字母完成鼠标右键单击操作，按住“Command”键输入提示字母完成鼠标双击操作
* 快捷键“Ctrl+S”激活滚动模式，使用HJKL+DU键进行滚动操作，按“TAB”键即可循环选择滚动区域

### Xnip - Mac上简单好用的截图工具

推荐来源：[once-liu](https://github.com/once-liu)

下载地址：https://zh.xnipapp.com/

软件状态：免费

为什么有微信或QQ的默认截图，还推荐这个？
因为好用。相比于微信或QQ的截图，还有几个好用功能：

- 滚动截图
- 贴图
- 可漂浮与桌面，多桌面切换时也会存在
  在一些需要局部数据对比时尤其好用。比如服务端的接口API，截图漂浮后，可以方便的撸代码。

### Dozer -  Mac端的状态栏管理工具

推荐来源：[zhangferry](https://github.com/zhangferry)

下载地址：https://github.com/Mortennn/Dozer/releases

软件状态：免费、开源

当在Mac上开较多软件时，会发现状态栏总是满满当当，看着很不舒服，也降低我们需要选择特定软件的效率，而Dozer就是为解决这种问题而生的。Dozer可以将系统状态栏按照两个小点分为三部分，对于不想让一直显示的图标，我们可以按住Command拖动图标至第一个小圆点的左侧，之后点击第二个小圆点就可以实现隐藏状态栏的功能了。

之前我的状态栏时这样的：

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20201219214427.png)

整理之后就变成了这样：

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20201219214453.png)