
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


整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### OpenInTerminal

**地址**：https://github.com/Ji4n1ng/OpenInTerminal

**软件状态**：免费，开源

**使用介绍**

OpenInTerminal 是一款开发辅助工具，可以增强 Finder 工具栏以及右键菜单增加在当前位置打开终端的功能。另外还支持：在编辑器中打开当前目录以及在编辑器中打开选择的文件夹或文件
![](https://user-images.githubusercontent.com/11001224/78589385-b797b880-7872-11ea-9062-c11a49461598.gif)

##### 核心功能
* 在终端（或编辑器）中打开目录或文件
* 打开自定义应用
* 支持 终端iTerm

### SnippetsLib
**地址**：https://apps.apple.com/cn/app/snippetslab/id1006087419?mt=12

**软件状态**：$9.99

**使用介绍**

SnippetsLab是一款mac代码片段管理工具，使用SnippetsLab可以提高工作效率。它可以帮助您收集和组织有价值的代码片段，您可以随时轻松访问它们

![](https://cdn.jsdelivr.net/gh/zhangferry/Images/blog/mojave-dark.jpg)



