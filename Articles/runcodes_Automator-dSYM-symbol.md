# 利用 Automator 快速符号化 Crash 文件

![](http://cdn.zhangferry.com/Images/automator-unsplash.jpg)

## 背景

起因是最近有接到一个临时协助任务，其中有几个重要的流程：

* `QA` 方导出 `.crash` 文件（必要的）
* 我方要根据测试提供的 crash 文件的`build number`，去下载对应的 `xx.app.dSYM`
* 把下载的`dSYM`给合作方
* 合作方解析`crash`文件

从上的步骤可以看出第一步不可省略。第二、三步完全可以干掉，流程越多越浪费时间。
第四步也可以我们自己做，就可以优化成 QA 直接解析好 crash 文件然后给合作方。

那么就提效了提效 50% 是不是，两个人的事情一个人搞定 （那么就可以卷点别的）

![](http://cdn.zhangferry.com/Images/automator_twodog.png)

## 初版方案

### 小插曲

> 一开始第一周我写了个`Shell`，调试通过之后就没继续，就干其他大活了（这里有个有悲剧）
> ......
> 第二周的时候，不知怎的崩溃出奇的多（应该是合作方更新SDK之后导致的）
> 当时我正`Coding`热火朝天，`QA`和合作方夺命的`Call`
> 我就去找那个当时写好的`shell`脚本，一通翻箱倒柜之后，我悟了，悲剧来了，找不到了
> 呵呵，被自己强迫症日常清理垃行为给清理了（自己有个日常清理的垃圾的行为，无奈Mac配置就这样）
> <img src="https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/automator_renzhubuku.png" width="120" height="120"/>
> 打工人不得不含着泪重新写了一份 (源码在下面)，快速应付下那边的夺命`Call`
> 然后我就在想这个事，为啥要我来做，也没啥技术含量，为啥不可自动化？
> Bingo~ 说来就来

### Shell 源码

```bash
crash_txt=$1
crash_log=${crash_txt%%.*}.log
# find /Applications/Xcode.app -name symbolicatecrash -type f
# cp /Applications/Xcode.app/Contents/SharedFrameworks/DVTFoundation.framework/Versions/A/Resources/symbolicatecrash symbolicatecrash
export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
./symbolicatecrash $1 $2 > $crash_log
open $crash_log -a sublime
```
具体如何符号化解析这里就不再唠叨了，网上一大堆：[附一个参考链接](https://gsl201600.github.io/2020/04/29/iOSCrash%E6%96%87%E4%BB%B6%E8%8E%B7%E5%8F%96%E5%8F%8A%E7%AC%A6%E5%8F%B7%E5%8C%96/ "iOS Crash文件获取及符号化")

## 使用 Automator 的自动化方案

要使用 Automator 还需要编写 AppleScript 代码。

###  工具 & 语言

* 工具：`Automator Service`， 脚本编辑器
* 语言：`AppleScript`，`Shell`

![automator](http://cdn.zhangferry.com/Images/automator_app.png)

![automator script editor](http://cdn.zhangferry.com/Images/automator_scipt_editor.png)

脚本编辑器，`AppleScript`调试用。

### 好玩的 AppleScript

下面是一些好玩的 `AppleScript` 代码，唤起你的好奇心：

```bash
display dialog "你说假如地球没有了空气，我们会怎样...
那么没有工程目录，后面该怎么办?" default answer "会死" buttons {"我知道了"} ¬
	default button "我知道了" with title "Handsome ERROR"
set theInput to text returned of the result
--display dialog text returned of the result
if theInput is equal to "会死" then
	display dialog "没救了" with title "ERROR" buttons {"我知道了"} ¬
		default button "我知道了"
end if
--忽略下面部分
```

```bash
say "Hello world"

display dialog "Hello World" with title "Alert"

display notification "Hello World" with title "Notification"
```

或者直接在终端里面跑

```bash
osascript -e "display notification \"Hello World\" with title \"Notification\""
```

> `-- single comment`， `# single comment` 是单行注释
>
> `(* this mutli comment *)` 是多行注释
>
> `Markdown`问题`AppleScript`脚本里意外出现`<p data-line`这种代码忽略

### AppleScript 需要注意的问题

主要还是路径问题 ApeleScript 获取的路径如下：

```
Macintosh HD:Users:xxxxxxx:Documents:xxxxx.app_副本_2.dSYM:
```

这种冒号的路径在`shell`命令行根本没法用，所以下面代码成了常客：

冒号字符串 打包成数组 `set my_array to split(input as string, ":")`

```bash
on split(the_string, the_delimiter)
	set old_delimiters to AppleScript's text item delimiters
	set AppleScript's text item delimiters to the_delimiter
	set the_array to every text item of the_string
	set AppleScript's text item delimiters to old_delimiters
	return the_array
end split
```

字符串 `set target_path to join(my_array, "/")`，这里要注意拼接文件与文件夹用的`index`下标不同：

```bash
on join(the_array, the_delimiter)
	set split_str to the_delimiter
	set target to " "
	set list_length to the length of the_array
	set list_length to list_length - 1
	set short_list to items 2 through list_length of the_array
	
	repeat with dir in short_list
		set target to target & split_str & dir
	end repeat
	return target
end join
```

## 实现过程

### 思路分析

1、定位`dSYM`路径

2、定位`xx.crash`件路径

3、唤起终端，切入指定路径

4、`symbolicatecrash`解析并重定向输入结果

5、自动打开展示结果

其实这前两步有个大坑：重复下载 dSYM 文件以及导出的 `xxx.crash` 文件路径会存在空格。在`AppleScript`调用`Shell`的时候路径有空格，会报错找不到对应的文件。

**解决办法**

* 利用 `AppleScript` 给文件重命名
* 借助`Automator` 现有的快捷操作修改

期间有周报群群主指点使用 `AppleScript` 借助 `quoted` 这个 `API` 来转义引用空格。
结果是终端识别了，但是`symbolicatecrash`还是不识别，虽然结果不尽人意，但是学到了新技能。

如果你看过`AppleScript API`，除了想哭就没别的，上面说的很清楚干啥用，但是不知道语法该咋写。因为没写过这种自然语法，每次都是不停的尝试、失败，尝试、失败，尝试、失败。
`AppleScript`小众到谷歌都没有，大部分都是查阅`Stack Overflow`。

**我这边选择是第二种**

`xxx.crash` 文件名有空格的解决办法是直接重命名，查找之后直接把空格替换成下划线。`dSYM` 父目录路径空格，这边多次导出之后会导致父目录存在空格，这个相对上面就比较复杂。
这里有几点思考：

> 在事物本身很难解决问题时，我们就需要放开视野，跳出事物本身，提升更高的角度去思考
> 当你这么想了，你思考问题的维度和角度就变了
> 在我们这个问题上，既然它的路径上存在空格，我给它换个不存在的路径不就好了
> 是不是一个很简单的解决办法，所以有时候不要太局限一点一面

### 一点瞎扯淡

其实日常编码或者修复 BUG 的过程中也会遇到类似情况，我们在一个问题上纠结好久好久到快死了吧！但是问题还没能解决，这个时候就可以尝试：

* 冷静下来 
* 刻意放慢节奏
* 全身心放松下来
* 想点别的换换脑子或者睡一觉（我通常就是睡觉）
* 冥想（这个相对高级 需要练习）

不去想这个问题一段时间之后，慢慢就会发现脑子开始活络起来，之前的问题解决办法好像一下子思路如泉涌，睡一觉精神也恢复了，思路也有了，简直两全其美是不是，比死磕一天啥都没有强千百倍吧，最后还得被喷延误工期，拉胯身体，最后无奈身不由己加入`996.icu` 这个 `Big Party`。


### 工程创建

1、选中dSYM文件 -> 右键 -> 服务 -> 创建服务

2、弹出一个快捷操作的模板空工程，可以配置参数入口（因为第一步选中了，参数就不需要配置了）

3、然后就可以拖拽你要的操作（类似于`storyboard`，`xib`操作）

4、保存 -> 命名，就会自动存储到本机的`~/Libray/Services`目录

_所有的快捷操作，工作流都会在这个目录，就是说你想用别人写好的最后安装的也是这个目录_

示例图：

![](http://cdn.zhangferry.com/Images/automator_services.png)

![](http://cdn.zhangferry.com/Images/automator_demo.png.png)

#### 完整的操作步骤

![](http://cdn.zhangferry.com/Images/automator_proj.png)

#### 脚本交互

* `Shell` 调用 `AppleScript`可以用`osascript -e`
* `AppleScript`调用`Shell`可以用`do shell script` & `do script`
* `do script`需要配合终端

示例：

```bash
tell application "Terminal"
	activate
	--set new_tab to do script "echo fire"
	delay 1
	do script "pwd" in front window
	do script "ls" in front window
end tell
```

### 演示

![gif](http://cdn.zhangferry.com/Images/automator_dsym.gif)
*模糊了点，为了加载快，压缩的有点狠，但是也能看大概流程就OK了*

有两种使用方式启动 dSYM 自动化服务：

* 首先选中 dSYM 文件，然后右键 -> 快捷操作 -> dSYM
* 首先选中 dSYM文件，快捷键即可（这里需要到 Finder -> Service 偏好设置里面配置好按键）

![automator rightkey](http://cdn.zhangferry.com/Images/automator_rightkey.png)

执行流程如下：

1、启动之后就自动去`/Users/$(whoami)/Downloads/`目录文件下搜索`.carsh`文件

这里写死`Downloads`目录的原因是想提高搜索速度，所有导出的时候选择的就是`Downloads`目录。如果你想要全局搜索也不是不是可以， 但是你得等等`Spotlight`

2、搜索完毕之后会列出该目录下所有的 `.crash` 文件。

3、选择对应的文件（`build number` 一致），就会打开一个终端进入解析流程。

4、解析完毕之后会通过 `sublime` 打开。没有`sublime`会怎样? 就去掉 `-a sublime`

`ApplesScript` 代码负责的部分：

- 冒号`:`转斜杠`/`
- 调用了剪切板做缓存
- `display dialog` 显示`.crash`文件的搜索结果
- 唤起终端，执行解析

## 总结

这里本来想在`Automator`里面加一个调用`Shell`脚本的的服务，这样就可以静默解析不用唤起终端，调试过程中解析一直失败，因为运行解析的 `symbolicatecrash` 需要的环境变量报错，也在对应的目录进行了`export`，但是最终还是不行，最后还是选择唤起终端来执行操作，或许看起来更酷一点吧 哈哈哈。

**其他文件读取/拷贝/搜索/重命名都是`Automator`提供现成服务。`Automator`真的很强大，但是你要发现它的美，学会使用它。**

最后就是要告诫自己：该做的事还得及时做出来， 不然就是午饭没吃 午休没睡。

![](http://cdn.zhangferry.com/Images/automator_meiyou.png)
