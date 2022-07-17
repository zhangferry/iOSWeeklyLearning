本文档为周报协作指导，只要介绍协作时用到的Markdown语法、图片引用及渲染美化操作。

## Markdown

Markdown 是一个 Web 上使用的文本到HTML的转换工具，可以通过简单、易读易写的文本格式生成结构化的HTML文档。目前 github、Stackoverflow 等网站均支持这种格式。

Markdown的运用对应两项内容：Markdown语法 + Markdown工具。

### Markdown语法

Markdown语法分两部分：

* [Markdown基本语法](http://markdown.p2hp.com/basic-syntax/)

* [Markdown扩展语法](http://markdown.p2hp.com/extended-syntax/)

几乎所有Markdown应用程序都支持John Gruber原始设计文档中概述的基本语法，我们可以放心使用。扩展语法则视不同程序解析程度而定，并不一定都支持。

### Markdown工具

有以下工具可供选择：[Markdown工具](http://markdown.p2hp.com/tools/)

本地应用：推荐使用[Typora](https://typora.io/)，它支持单界面实时渲染，对于扩展语法也全部支持。

云端平台：推荐[掘金](https://juejin.cn/)，我们可以点击写文章，进入一个Markdown写作界面，如果不想发布，只保存到草稿箱就可以了。

服务器工具：推荐使用[Hexo](https://hexo.io/)，[Jekyll](https://jekyllrb.com/)。当前 https://zhangferry.com 使用的就是Hexo。

## 图片

博客写作免不了展示一些图片，对于一些云端平台，像是掘金，简书都提供有自己的图床服务，当我们使用外部图片时它会自动转存至自己的图床，并更换图片链接。但对于自己搭建的服务，就需要自己准备图床了。另外，对于一些本地引用的图片，我们也有上传至图床的需求。如果考虑到文章迁移到微信公众号的情况，我们还需要注意只能使用服务器在国内的图床，国外服务会被微信屏蔽。

图床的要求是：国内服务器、价格便宜（最好免费）、访问速度稳定。最终选择了 Gitee 图床服务。

> ![](http://cdn.zhangferry.com/Images/20220327111414.png)
>
> 因为在网站访问量过大的情况 Gitee 图床遭遇了封禁，所以现将图床更换为七牛云。

图床使用还需要搭配一个上传工具，选择了[PicGo](https://molunerfinn.com/PicGo/)，它提供了直接上传七牛图床的插件。

### 配置过程

1、安装 PicGo

2、配置七牛云

![](https://cdn.zhangferry.com/Images20220717141216.png)

AccessKey 和 SecretKey 内容需要跟 @zhangferry 索取，其他内容均如图填写即可。

5、PicGo使用

本地图片复制到剪切板之后会被PicGo获取，点击工具栏图片，再点击对应图片即会开始上传。

对于网络图片，可以右键选复制图片，然后点击工具栏进行上传。

上传成功会有通知提示，对应的Markdown链接也会直接复制到剪切板，这时可以直接在编辑工具里粘贴使用。

### 图片规范

1、命名规范（非必要，对于一些配图可以带上）

Mardown的图片写法是这样的

```
![ImageName](http://cdn.zhangferry.com/Images/000.png)
```

前面中括号里的内容对应图片名称，会作为标注显示。

2、图片大小限制

图片大小不能超过1M，Gif的话也一样，超过的话可以上传成功但不会被显示。

如果出现了大小超限的情况就需要进行压缩处理。

普通图片可以降低图片尺寸：预览打开，调整大小。

Gif图片比较麻烦：

微信的限制是：不能超过300帧、不能大于2M。可以把这个当做最大限制，但这个只能本地上传，无法通过图床直接导入。

Gif的压缩可以从两个方面入手：删帧和压缩。

删帧的话，使用预览打开，选中对应帧按Common + Delete

压缩的话，使用线上工具[docsmall](https://docsmall.com/gif-compress)

## 渲染

Markdown的渲染通常都是转成HTML，相同的语法可以对应不同的显示效果。通常我们使用的都是Github样式，即Github里对Markdown的渲染效果。对于博客这类需要在电脑端阅读的场景，通常选择这个样式就行了，对于微信公众号这类一般都在移动端阅读的场景，最好使用一些美化渲染效果。

当前周报选择的是 [mdnice](https://mdnice.com/) 提供的渲染功能，当前渲染的有两部分：

* 主题渲染，选择自定义模式，然后增加[该文件](https://github.com/zhangferry/iOSWeeklyLearning/tree/main/Resources/Style)内的代码即可。
* 代码主题，选择的是atom-one-dark，勾选 Mac 风格

### 注脚

另外mdnice还提供了一些Markdown扩展功能，针对微信公众号不能添加外部链接的情况，支持文档引用。写法为：

```
[摸鱼周报](https://github.com/zhangferry/iOSWeeklyLearning "摸鱼周报")
```

链接后面引号跟着的内容为参考链接的标题。所有引用的内容会统一归为二级目录的参考资料，并按顺序标记序号。

该功能未mdnice支持，非原生Markdown功能。

### 代码块

代码块可以指定编程语言，写法如下：

```
```swift
let name = "iOSWeeklyLearning"
​```
```

首行的swift标记代码块的语言，其可以根据不同语言的语法特性进行渲染。

常用的几种语言对应的标记有：objectivec、swift、c、c++、bash、python、java等。

该功能为Markdown原生扩展功能。



