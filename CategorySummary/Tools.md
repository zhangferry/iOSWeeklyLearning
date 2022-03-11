***
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

之前我的状态栏是这样的：

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20201219214427.png)

整理之后就变成了这样：

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20201219214453.png)



![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
***
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
***
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

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210110110014.png)

### uTools

**推荐来源**：[zhangferry](https://github.com/zhangferry)

**下载地址**：https://u.tools/

**软件状态**：免费（部分功能付费）

**使用介绍**

uTools是一个丰富的生产力工具集，支持将近百种的插件。它的使用方式和 Alfred 类似，通过快捷键调出输入框，并通过特殊指令执行结果。但它有比 Alfred 更简单的插件集成方式，在我看来它是更易用的。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210110110536.png)

***
推荐好用的开发工具。

### kaleidoscope

**推荐来源**：zhangferry

**下载地址**：https://kaleidoscope.app/

**软件状态**：付费，$69.99

**使用介绍**

kaleidoscope中文翻译是万花筒，它是一款颜值很高，专业性很强的diff工具。不光能查看文本的不同，还能识别图片和文件夹的不同。我们可以将它与 git 组合使用，使用它替换git的mergetool。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210124184141.png)

### Sherlock

**推荐来源**：zhangferry

**下载地址**：https://sherlock.inspiredcode.io/

**软件状态**：付费，$49

**使用介绍**

在iOS开发过程中的UI调试常常是让人痛苦的，因为不支持热更新，我们稍微改动一点地方就需要编译整个项目重新运行，这无疑很浪费时间。而Sherlock就是用于解决这个问题的工具（仅支持模拟器），我们可以实时修改各个控件的UI属性，并进行查看最终效果。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210124195019.png)

***
推荐好用的开发工具。

### Diagrams.net

**推荐来源**：[zhangferry](zhangferry.com)

**地址**：https://www.diagrams.net/

**软件状态**：免费，[开源](https://github.com/jgraph/drawio)

**使用介绍**

强大且方便的流程图绘制软件，同时支持Web端和桌面端。和[Processon的](https://www.processon.com/)免费版只能添加9个文件的限制，Diagrams.net的文件数量是无限制的，而且它支持的流程图控件比Processon还要更多。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210227191005.png)

* 支持几乎所有的主流流程图元素
* 远程存储，文件数量不限，可以存储至Github、Google Drive、Dropbox等地方
* 支持本地桌面端，可以离线绘制，本地存储
* 支持链接共享，通过链接查看我们当前绘制的流程图
* 可以导出为图片、HTML、PDF等多种格式

### Github1s.com

**推荐来源**：[zhangferry](zhangferry.com)

**地址**：https://github.com/conwnet/github1s

这个工具可以使我们访问github的仓库就像直接在VSCode中打开一样，使用方法非常简单，就是将网站域名换成github1s，以Swift仓库为例，访问：https://github1s.com/apple/swift，得到的结果如下。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210228152659.png)

我们可以像在VSCode里一样，直接在浏览器里查看仓库代码。

***
推荐好用的工具。

### F.lux

**推荐来源**：[zhangferry](zhangferry.com)

**地址**：https://justgetflux.com/

**软件状态**：免费

**使用介绍**

电脑的显示器亮度一般是全天保持不变的，这个亮度对于白天使用来说没有任何问题，但是对于夜间使用的话就会有些刺眼，出于对视力的保护，夜间应该让屏幕亮度低一些，暖一些。

F.lux就是处理这一问题的软件，他可以根据时间调节屏幕颜色，白天亮度像太阳光，在夜间时会让屏幕看着更像是室内光。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210314141348.png)



### Kap

**推荐来源**：[highway](https://github.com/HighwayLaw)

**地址**：https://getkap.co/

**软件状态**：免费，[开源](https://github.com/wulkano/kap "Kap开源地址")

**使用介绍**

一款开源且简洁高效的屏幕录制软件，可以导出为GIF，MP4，WebM，APNG等格式，而且会有很不错的压缩率。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210313211617.png)

鉴于微信公众号对GIF的两条限制：

1、不能超过300帧

2、大小不能超过2M

我们需要对一些GIF进行修剪和压缩才能上传。

删除帧数有一个简单的方法：用Mac自带的预览功能打开GIF，选中想要删除的帧，按Command + Delete即可删除指定帧。另外对于多个连续帧的选中，可以先单击选中第一帧，再按住Shift单击选中末尾帧，即可选中这个区间连续的所有帧。

对于GIF的压缩，推荐另一个工具：docsmall。

### docsmall

**推荐来源**：[zhangferry](zhangferry.com)

**地址**：https://docsmall.com/gif-compress

**软件状态**：免费，Web端

**使用介绍**

上传需要压缩的gif文件即可

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210313211739.png)

***
推荐好用的工具。

### P4Merge

**推荐来源**：zhangferry

**地址**：https://www.perforce.com/downloads/visual-merge-tool

**软件状态**：对开发者免费

**使用介绍**

非常强大的可视化diff工具，如果你嫌[Kaleidoscope](https://kaleidoscope.app/)太贵的话，可以用它做代替品。我们可以把它集成进git，通常diff工具有两个作用一个是作为difftool，一个是作为mergetool。配置流程如下：

```shell
# difftool
$ git config --global diff.tool p4merge
$ git config --global difftool.p4merge.cmd \
"/Applications/p4merge.app/Contents/Resources/launchp4merge \$LOCAL \$REMOTE"
# mergetool
$ git config --global merge.tool p4merge
$ git config --global mergetool.p4merge.cmd "/Applications/p4merge.app/Contents/MacOS/p4merge $PWD/$BASE $PWD/$LOCAL $PWD/$REMOTE"
```

以下是作为mergetool的界面，下面内容为最终合并的内容，我们可以通过右侧的扩展按钮选择当前应该选择哪个分支的内容。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210327200304.png)

***
推荐好用的工具。

### Cleaner for Xcode

**推荐来源**：zhangferry

**地址**：https://github.com/waylybaye/XcodeCleaner-SwiftUI

**软件状态**：开源版本免费，AppStore版本$0.99

**使用介绍**

这个应用可以帮助你清除遗留以及废弃文件，从而极大的节省硬盘空间。 你可以每月或者每周运行一次进行清理。

![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210410105340.png)

******
整理编辑：[zhangferry](https://zhangferry.com)

### SwitchHosts

**地址**：https://swh.app/zh/

**软件状态**：[开源](https://github.com/oldj/SwitchHosts)，免费

**使用介绍**

SwitchHosts 是一个管理、切换多个 Host 方案的工具。它支持多个 Host 方案的不同组合；支持导入导出，方便协作分享；还可以通过 Alfred 插件进行快速切换。
![SwitchHosts](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210430084948.png)

### DevUtils

**地址**：https://devutils.app/

**软件状态**：[开源](https://github.com/DevUtilsApp/DevUtils-app)，部分功能付费

**使用介绍**

DevUtils 是一个开源的开发工具聚合的应用。它包含了常用的时间戳解析，JSON 格式化，Base64 编解码，正则表达式测试等功能。有了它我们就可以放弃掉站长之家，各种 JSON 格式化网站的使用了。

大家如果不想付费，直接下源码，关掉付费验证就行。如果觉得软件有帮助且有支付能力的话希望还是可以支持下作者。

![DevUtils](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210430085707.png)

***
整理编辑：[zhangferry](https://zhangferry.com)

### Moment

**地址**：https://fireball.studio/moment

**软件状态**：￥30，可以试用7天

**使用介绍**

Moment 是一个存在于菜单栏和通知中心的倒计时应用程序，以帮助你记住最难忘的日子和生活。这个类似手机端的 Countdown。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/menubar-mockup.jpg)

### One Switch

**地址**：https://fireball.studio/oneswitch

**软件状态**：￥30，可以试用7天

**使用介绍**

One Switch 是一个聚合的开关控制软件，使用它可以在菜单控制栏直接配置桌面的隐藏显示、锁屏、暗黑模式、连接AirPods 等功能。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/mbp-mockup.png)

***
整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### SwiftFormat for Xcode

**地址**：https://github.com/nicklockwood/SwiftFormat

**软件状态**：免费 ，开源

**使用介绍**

SwiftFormat 是用于重新格式化 Swift 代码的命令行工具。它会在保持代码意义的前提下，将代码进行格式化

很多项目都有固定的代码风格，统一的代码规范有助于项目的迭代和维护，而有的程序员却无视这些规则。同时，手动强制的去修改代码的风格又容易出错，而且没有人愿意去做这些无聊的工作。

如果有自动化的工具能完成这些工作，那几乎是最完美的方案了。在代码 review 时就不需要每次都强调无数遍繁琐的代码格式问题了。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210522213832.png)

### Notion

**地址**: https://www.notion.so/desktop

**软件状态**：个人免费，团队收费

**使用介绍**

Notion 是一款极其出色的个人笔记软件，它将“万物皆对象”的思维运用到笔记中，让使用者可以天马行空地去创造、拖拽、链接；Notion 不仅是一款优秀的个人笔记软件，其功能还涵盖了项目管理、wiki、文档等等。

##### 核心功能

* 支持导入丰富的文件和内容 
* 内置丰富的模板
* 简洁的用户界面、方便的拖动和新建操作
* 支持 Board 视图，同时可以添加任意数量的其他类型视图并自定义相关的过滤条件
* 复制图片即完成上传，无需其他图床 
* 保存历史操作记录并记录相关时间
* 强大的关联功能，比如日历与笔记，笔记与文件以及网页链接

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210522213919.png)

***
整理编辑：[zhangferry](https://zhangferry.com)

### Whatpulse

**地址**：https://whatpulse.org/

**软件状态**：基础功能免费，高级功能付费

**使用介绍**

Whatpulse是一个电脑使用检测统计软件，它可以统计你每天的键盘、鼠标、网络等情况的使用详情并将其做成简单的统计表格，用于分析每天的电脑使用情况。

翻到一张之前公司电脑使用该软件将近一年的留存成果，100万+ 按键次数，使用最多的竟然是删除键。。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210529185605.png)

# OctoMouse

**地址**：https://konsomejona.github.io/OctoMouse/index.html

**软件状态**：免费，[开源](https://github.com/KonsomeJona/OctoMouse)

**使用介绍**

该软件主要用于统计键盘及鼠标的行为信息，比较有意思的是，它对鼠标的统计会包含移动距离参数。可以试试看多久才能让鼠标移动 5km。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210529191107.png)

***
### 柠檬清理
 整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

**地址**: https://lemon.qq.com/

**软件状态**: 免费 

**软件介绍**

腾讯柠檬清理 Lite 版-重点聚焦清理功能，包含系统/应用垃圾清理、大文件清理、重复文件清理、相似照片清理 4 个方面，当前还支持在状态栏上查看当前网速信息，帮助你实时了解 Mac 状况。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/16227749924686.jpg)

**核心功能**

* 便捷好用的状态栏清理：可直接在状态栏上查看实时网速，方便及时了解网速变化。支持快速清理，轻轻一点，不留垃圾。
* 系统/应用垃圾清理
* 大文件清理：帮你快速全面查找占用超过 50M 的大文件。
* 重复文件清理


***
整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### Diffchecker

**地址**：https://www.diffchecker.com/

**软件状态**：Web端免费，桌面端 $9/月

**介绍**

Diffchecker 是一款简单好用的差异比较工具，使用可帮助用户快速的比较您的文本文件、文档、PDF、照片、图形和扫描等，并且界面简单直观，输入两个文件的内容，然后单击“查找差异”即可，并且具有绝对的安全性，能够保障您的文件安全，具有统一差异、字符级差异、文件夹差异、导出为 PDF、语法高亮、文件导入、无广告等优势。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/1623388796593.jpg)


***
整理编辑：[zhangferry](https://zhangferry.com)

### WWDC

**地址**：https://wwdc.io/ 

**软件状态**：免费，[开源](https://github.com/insidegui/WWDC)

**介绍**

一个开源的非官方 WWDC 视频的应用，其支持视频下载、最高 5 分钟的视频切割、书签功能、iCloud 同步、Chromecast 投屏、画中画功能等等。相比于官方应用来说，其功能只多不少（官方新版的 Developer 应用添加了代码片段预览功能），而且更新比较迅速，已经发展到了 v7.3.3 版本，可以查看 2021 年的 Sessions。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210626230114.png)

### ScreenSize

**地址**：https://www.screensizes.app/

**介绍**

一个在线的 Apple 设备尺寸及设备内各组件的尺寸整理网站，非常之全。这里简要概括下其在 iPhone 设备包含的内容：

* 横竖屏状态的安全区域大小
* 三种 Widget 尺寸的大小
* 标准模式和系统放大模式的尺寸大小
* 各个设备之间的尺寸对比

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210626223430.png)

***
整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)，[zhangferry](https://zhangferry.com)

### Cakebrew

**地址**：https://www.cakebrew.com/

**软件状态**：免费，[开源](https://github.com/brunophilipe/Cakebrew)

**软件介绍**：

Homebrew 是 Mac 端常用的包管理工具，但其仅能通过命令行操作，对那些不擅长使用命令行的开发来说会是一种苦恼，而且命令行确实不够直观。Cakebrew 是一款桌面端的 Homebrew 管理工具，它包含常用的 Homebrew 功能，并将其可视化，像是已安装工具，可升级工具以及工具库等功能。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210704205546.png)

### Paste - Clipboard Manager

**地址**: https://apps.apple.com/us/app/paste-clipboard-manager/id967805235

**软件状态**: 收费 ¥98/年 

**软件介绍**：

Paste for Mac 是 Mac 平台上一款专业的剪切板记录增强工具，它能够为您储存您在设备上复制的所有内容，并将其储存在 Paste for Mac 的历史记录中。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210703184817.png)

***
整理编辑：[zhangferry](https://zhangferry.com)

### SnippetsLab

**地址**：http://www.renfei.org/snippets-lab/

**软件状态**：$9.99

**软件介绍**：

一款强大的代码片段管理工具，从此告别手动复制粘贴，SnippetsLab 的设计更符合 Apple 的交互习惯，支持导航栏快速操作。另外还可以同步 Github Gist 内容，使用 iCloud 备份。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210710232333.png)

### CodeExpander

**地址**：https://codeexpander.com/

**软件状态**：普通版免费，高级版付费

**软件介绍**：

专为开发者开发的一个集输入增强、代码片段管理工具，支持跨平台，支持云同步（Github/码云）。免费版包含 90% 左右功能，相对 SnippetsLab 来说其适用范围更广泛，甚至包括一些日常文本的片段处理。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210710231521.png)



***
整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

**地址**： https://github.com/huanxsd/LinkMap

**软件状态**： 免费 

**软件介绍**

iOS 包的大小，是每个开发必须关注的问题，对于大型项目来说，只是代码段就有可能超过 100M，算上 armv7 和 arm64 架构，会超过 200M。 LinkMap 工具通过分析项目的 LinkMap 文件，能够计算出各个类、各个三方库占用的空间大小（代码段+数据段），方便开发者快速定位需要优化的文件。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/linkmap.png)

***
整理编辑：[CoderStar](https://juejin.cn/user/588993964541288/posts)

### Snipaste

**地址**： https://zh.snipaste.com/

**软件状态**： 普通版免费，专业版收费，有 Mac、Windows 两个版本

**软件介绍**：

Snipaste 是一个简单但强大的截图工具，也可以让你将截图贴回到屏幕上！普通版的功能已经足够使用，笔者认为其是最好用的截图软件了！（下图是官方图）

![Snipaste](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/N3QEb3VA.png)

### LSUnusedResources

**地址**： https://github.com/tinymind/LSUnusedResources

**软件状态**： 免费

**软件介绍**：

一个 Mac 应用程序，用于在 Xcode 项目中查找未使用的图像和资源，可以辅助我们优化包体积大小。

![LSUnusedResources](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/LSUnusedResourcesExample.png)

***
整理编辑：[zhangferry](https://zhangferry.com)

### Messier

**地址**：https://messier-app.github.io/

**软件状态**：免费

**软件介绍**：

Messier 是基于 AppleTrace 开发的 Objective-C 方法耗时测量应用，其相对于 AppleTrace 更易用，且能更方便的在越狱设备上 Trace 任意应用。它由三部分组成：Tweak 插件，动态库（Messier.framework），桌面端应用。非越狱场景，我们使用后两个部分可完成对自己应用的耗时监控，输出为 json 文件，再使用 `chrome://tracing` 将 json 文件绘制为火焰图，效果如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/messier-content.gif)

***
整理编辑：[zhangferry](https://zhangferry.com)

### regex101

**地址**：https://regex101.com

一个正则表达式测试和分析网站，不仅可以将匹配结果进行输出，还会逐个分析表达式的含义。我们以摸鱼周报`关于我们`的文案进行测试，我们想匹配出 “iOS 摸鱼周报”（中间有空格），“iOS成长之路”，这两个字符串。文案特征为：”iOS“开头，不能紧跟其他字母，以逗号结尾但不包括逗号。测试结果如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210807164527.png)

观察右侧结果分析，示例中使用的 `*?` 非贪婪模式和 `(?=，)` 零宽度正预测先行断言，都有很详细的讲解。这对于我们理解他人写的正则表达式能起到很好的帮助作用。

***
整理编辑：[zhangferry](https://zhangferry.com)

### explainshell

**地址**：https://explainshell.com/

这个网站跟上期介绍的 [regex101](https://regex101.com) 很类似，一个用于解析正则表达式，一个用于解析 shell 指令。不常接触 shell 的小伙伴对于一个参数巨多，又巨长的指令可能会手足无措，没关系，这个网站来帮你😏。它会把主要命令和各个参数，传值进行详细的拆分讲解。比如这句列出所有包含 `1a1b1c` 这一 commit 的分支：

```bash
git branch -a -v --no-abbrev --contains 1a1b1c
```

解析结果：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210814184638.png)

***
整理编辑：[zhangferry](https://zhangferry.com)

# KeeWeb

**地址**：https://keeweb.info/

**软件状态**：免费，[开源](https://github.com/keeweb/keeweb)

**软件介绍**：

KeeWeb 是一个浏览器和桌面密码管理器，兼容 KeePass 数据库。它不需要任何服务器或额外的资源。该应用程序可以在浏览器中运行，也可以作为桌面应用程序运行。更重要的是它还可以利用 Dropbox、Google  Drive 进行远程同步。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210822081714.png)

***
整理编辑：[CoderStar](http://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18#wechat_redirect)

### OhMyStar

**地址**：https://ohmystarapp.com/

**软件状态**：普通版免费，Pro 版收费

**软件介绍**：

直接引用官方自己介绍的话吧：
> The best way to organise your GitHub Stars. Beautiful and efficient way to manage, explore and share your Github Stars.

其中 Pro 版增加的功能是设备间同步，不过软件本身也支持数据的导入导出，大家根据自己的情况进行选择。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210828101929.png)

***
整理编辑：[zhangferry](https://zhangferry.com)

### Wechatsync

**地址**：https://www.wechatsync.com/

**软件状态**：免费，[开源](https://github.com/wechatsync/Wechatsync)

**软件介绍**：

作为号主通常会将文章发布到多个平台，每个平台都重复地登录、复制、粘贴是一件很麻烦的事。Wechatsync就是这样一款解脱重复工作的神器。它是一款 Chrome 浏览器插件，支持多个平台的文章发布，这需要我们提前登录各个平台获得授权。它会自动识别公众号文章，弹出「同步该文章」按钮，然后点击就可以同步文章到我们授权的平台。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210904171532.png)

***

整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### XcodeProjects

**地址**： https://github.com/DKalachniuk/XcodeProjects

**软件状态**： 免费，开源

**软件介绍**

日常开发过程中，经常在终端中执行 pod install、pod update、或者 clear derived data 等操作，XcodeProjects 工具执行这些操作，只需要点击两下就能完成，还能为自己的项目自定义 command，很大程度的简化我们的操作步骤，节省开发时间。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/XcodeProjects.png)



***

整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### XcodesApp

**地址**： https://github.com/RobotsAndPencils/XcodesApp

**软件状态**： 免费，开源

**软件介绍**

AppStore 自带的升级功能经常因为某些奇怪的原因卡住而被吐槽，如果你也经历过这些事情可以试下 Xcodes。Xcodes 是一个 Xcode 下载管理器，支持下载不同版本的 Xcode，还可以切换默认版本。如果你喜欢命令行，还可以使用其[命令行版本](https://github.com/RobotsAndPencils/xcodes "xcodes")进行安装。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/xcodes.png)


***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18) 、[zhangferry](zhangferry.com)

### SCADE

**地址**：https://www.scade.io/

**软件状态** 
- SCADE Community：免费
- SCADE Professional：$29 per month / user

**软件介绍**：

利用 `SCADE` 我们可以使用 Swift 语言进行跨端原生开发。其描述特点如下：
- 跨平台：使用相同的源代码为 iOS 和 Android 开发
- 原生功能：不受限制地使用所有 iOS 和 Android 功能
- 无与伦比的速度：Swift 被编译为本机二进制代码以获得无与伦比的应用程序性能
- Swift 框架：在 iOS 和 Android 上使用流行的 Swift 框架，如 Swift Foundation，无需更改代码
- ...

![SCADE](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/SCD_Auora1-1-1-1240x791.png)

### Privacy-Insight

**地址**：https://github.com/Co2333/Privacy-Insight/releases

**软件状态** ：免费，开源

**软件介绍**：

解析 iOS 15 下格式为 `.ndjson` 的系统隐私报告，用 SwiftUI 写成。

隐私日志的生成为设置 -> 隐私 -> 打开记录 App 活动，等待一段时间之后点击下面的存储 App 活动按钮，即可收集这一段时间的隐私日志。存储会生成一个 `.ndjson` 格式的文件，导出使用 Privacy-Insight 打开即可查看。

以下为我使用 1 天的隐私请求记录：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/4301634041484_.pic_hd.jpg)

微信和今日头条的隐私权限获取频率均非常高，我是肯定没有那么频繁通过微信访问相册的。对于微信频繁获取相册权限的问题最近也在热议，希望不仅是微信，各个主流 App 都应该对于用户隐私问题予以重视。

作为使用者相对有效的保护隐私的方案是，关闭对应 App 的「后台刷新」，非必要情况下关闭蓝牙、定位等权限，并将相册调用权限改为「选中的照片」。

***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### wakapi

**地址**：https://wakapi.dev/

**软件状态**：免费，[开源](https://github.com/muety/wakapi)

**软件介绍**：

`Wakapi` 是一个开源工具，可帮助我们跟踪使用不同编程语言等在不同项目上编码所花费的时间，并使用图表等形式展现出来，支持 Xcode，值得一玩。

![wakapi](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/screenshot.png)

***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### fig

**地址**：https://fig.io/

**软件状态**：免费，[开源](https://github.com/Coder-Star/autocomplete)

**软件介绍**：

`fig` 是一个开源的终端自动补全工具，支持数百个 CLI 工具，如 `git`、`docker`、`npm `等等，并且可以无缝添加到你现有的终端，如 `iTerm`、`Hyper`、`VSCode` 和 `macOS 终端`，支持我们自己自定义一些补全规则。

![fig](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Snipaste_2021-10-27_21-04-03.png)
***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### ipatool

**地址**：https://github.com/majd/ipatool

**软件状态**：免费，[开源](https://github.com/majd/ipatool)

**软件介绍**：

`ipatool` 是一个允许你在 `App Store` 上搜索 iOS 应用程序并下载应用程序包的命令行工具。当然，这过程中需要你的账户以及密码，并且也只能下载账户过去已经下载过的应用程序。相对于使用 `Apple Configurator 2` 操作更加便捷一些。

![ipatool](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/demo.gif)
> 注意 gif 中的 `ipa` 命令实际使用中可能为 `ipatool`

***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### swiftenv

**地址**：https://github.com/kylef/swiftenv

**软件状态**：免费，[开源](https://github.com/kylef/swiftenv)

**软件介绍**：

`swiftenv` 允许您：
* 更改每个用户的全局 Swift 版本。
* 设置每个项目的 Swift 版本。
* 允许您使用环境变量覆盖 Swift 版本。

![swiftenv](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/swiftenv.png)

***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Mounty

**地址**：https://mounty.app/

**软件状态**：免费，[开源](https://mounty.app/)

**软件介绍**：

`Mounty` 是一个在 macOS 下以读写模式重新挂载写保护的 NTFS 卷的小工具，功能类似于 `NTFS For Mac`，最大也是最重要的区别是它是**免费**的。

![mounty](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/example.png)

***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### PhotoSweeper

**地址**：https://overmacs.com/

**软件状态**：$9.99，可以试用

**软件介绍**：

`PhotoSweeper` 是一款快速而强大的重复照片清理器，旨在帮助您在 Mac 上查找和删除重复和相似的照片。

我们可以考虑用在给应用瘦身时扫描相似图片资源场景下。

![PhotoSweeper](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/PhotoSweeper_MacBook.jpeg)

***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### 思源笔记

**地址**：https://github.com/siyuan-note/siyuan

**软件状态**：开源、免费

**软件介绍**：

思源笔记是一款本地优先的个人知识管理系统， 支持细粒度块级引用和 Markdown 所见即所得。

![siyuan-note](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/68747470733a2f2f63646e2e6a7364656c6976722e6e65742f67682f73697975616e2d6e6f74652f73697975616e40383438393339373430316366353032356561623834376466623236613466333839366265353336332f73637265656e73686f74732f66656174757265302e706e67.png)


***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### myyearwithgit

**地址**：https://github.com/Co2333/myyearwithgit

**软件状态**：开源、免费

**软件介绍**：

看名字大家就知道这个是干啥的，还是配上老王的描述吧：
> 本程序目前支持使用常见 Git 仓库托管提供商以及本地代码仓库进行分析。

![myyearwithgit](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Screenshot.png)


### 往期推荐

[iOS摸鱼周报 第三十六期](https://mp.weixin.qq.com/s/K_JHs1EoEn222huWIoJRmA)

[iOS摸鱼周报 第三十五期](https://mp.weixin.qq.com/s/fCEbYkAPlK0nm7UtLKFx5A)

[iOS摸鱼周报 第三十四期](https://mp.weixin.qq.com/s/P0HjLDCIM3T-hAgQFjO1mg)

[iOS摸鱼周报 第三十三期](https://mp.weixin.qq.com/s/nznnGmBsqsrWcvZ4XFMttg)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
***
推荐来源：[iOSleep](https://github.com/iOSleep)

### Dropshelf

**地址**：https://pilotmoon.com/dropshelf/

**软件状态**：之前付费但是目前下架了，可以使用上面链接免费使用。

**软件介绍**：

Dropshelf 是一款 Mac OS 下的拖拽效率应用。它提供了一个可以吸附在屏幕边缘的 Dock，你可以拖拽任何东西「图片、文件、文字、链接...」暂存到 Dock 中，方便你在其他 App 中来使用。

![Dropshelf](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/9964d0eee2c48e3d24ba63c09e25b10c_720w.jpeg)

***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### xcinfo

**推荐来源**：[faimin](https://github.com/faimin)

**地址**：https://github.com/xcodereleases/xcinfo

**软件状态**：开源、免费

**推荐语**：

`Xcodes` 的另一种选择，方便我们直接从苹果官网下载 Xcode。 据称下载速度比 `Xcodes` 更快。

![xcinfo](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/inf.png)

### Mark Text

**地址**：https://marktext.app/

**软件状态**：开源、免费

**软件介绍**：

一个简单而优雅的开源 `markdown` 编辑器，专注于速度和可用性，适用于 `Linux`, `macOS` 和  `Windows`。

其和 `Typora` 一样，也是单窗的形式。

![Mark Text](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/marktext.png)

***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Tig

**地址**：https://jonas.github.io/tig/

**软件状态**：开源、免费

**软件介绍**：

`Tig` 是一个 `git` 资源库浏览器，采用 `ncurses` 开发，很适合习惯使用命令行进行 `git` 操作的小伙伴们。

![Tig](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Snipaste_20220106.png)

***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### SwiftInfo

**地址**：https://github.com/rockbruno/SwiftInfo

**软件状态**：开源、免费

**软件介绍**：

`SwiftInfo` 是一个 `CLI` 工具，用于提取、跟踪和分析对 `Swift` 应用程序有用的指标。除了该工具附带的默认跟踪选项外，还支持自定义编写 `.Swift` 脚本来实现额外的功能。

默认支持的工具包括：

- IPASizeProvider
- WarningCountProvider
- LinesOfCodeProvider
- ...

更多细节请直接前往 repo homepage 查看。

![SwiftInfo](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220112183759.png)

***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### 摸鱼单词

**地址**：https://apps.apple.com/cn/app/id1488909953?mt=12

**软件状态**：免费

**软件介绍**：

软件作者自述：电脑大部分使用场景是用来办公，如果在办公之余可以背背单词就很好啦，于是就有了摸鱼单词。专注于利用碎片时间学习记忆英语单词。

> 和《摸鱼周报》相得益彰，作者也是一直在维护这个软件。

![摸鱼单词](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Snipaste_2022-01-18_20-46-39%E7%9A%84%E5%89%AF%E6%9C%AC.png)

***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Graphviz

**地址**：http://www.graphviz.org/

**软件状态**：免费

**软件介绍**：

贝尔实验室开发的有向图/无向图自动布局应用，支持 dot 脚本绘制结构图，流程图等。

![Graphviz](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220217174238.png)

对产物`.gz`文件进行解析查看的途径。

- 在线网站：[GraphvizOnline](http://dreampuf.github.io/GraphvizOnline "GraphvizOnline")
- vs 插件：Graphviz (dot) language support for Visual Studio Code


结合`cocoapods-dependencies`插件，我们可以解析`podfile`文件来分析项目的`pod`库依赖，生成`.gz`文件。

* 生成`.gz`文件：`pod dependencies --graphviz`
* 生成依赖图：`pod dependencies --image`
* 生成`.gz`文件及依赖图：`pod dependencies --graphviz --image`

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### EasyFind 

**地址**：https://easyfind.en.softonic.com/mac

**软件状态**：免费

**软件介绍**：

小而强大的文件搜索应用，媲美 `windows` 下的 `Everything`。

![EasyFind](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/easyfind-easyfind.png)



***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### nginxedit 

**地址**：https://www.nginxedit.cn/

**软件状态**：免费

**软件介绍**：

`Nginx`在线配置生成工具，配置高性能，安全和稳定的`Nginx`服务器的最简单方法。

![nginxedit](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Nginx%E5%9C%A8%E7%BA%BF%E9%85%8D%E7%BD%AE%E7%94%9F%E6%88%90%E5%B7%A5%E5%85%B7.png)

***
整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

本次推荐一系列关于 UI 调试的软件，包含电脑端以及 App 端两种类型；

**电脑端**

- [Reveal](https://revealapp.com/)：经典UI调试软件，但需要付费；
- [Lookin](https://lookin.work/)：腾讯出品的一款免费好用的 iOS UI 调试软件；

**App 端**

- [FLEX](https://github.com/FLEXTool/FLEX)：FLEX (Flipboard Explorer) 是一套用于 iOS 开发的应用内调试工具；
- [啄幕鸟iOS开发工具](https://github.com/alibaba/youku-sdk-tool-woodpecker)：阿里出品的一套用于 iOS 开发的应用内调试工具；

> 其中 Reveal、Lookin、FLEX 都有对应的`Tweak`，有越狱设备的小伙伴可以玩一玩；

