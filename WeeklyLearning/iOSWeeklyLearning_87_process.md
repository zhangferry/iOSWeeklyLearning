# iOS 摸鱼周报 #87

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：Apple 公布 iOS 16 的普及率已达 81%
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题



## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

整理编辑：[@远恒之义](https://github.com/eternaljust)



## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[OpenAI：通用人工智能规划及未来](https://mp.weixin.qq.com/s/Ku97-qx0EGnV9NVU20LyAA)：这是 OpenAI 发布的文章[Planning for AGI and beyond](https://openai.com/blog/planning-for-agi-and-beyond "Planning for AGI and beyond")的翻译版。人工智能的等级分三级：

* ANI（Artificial Narrow Intelligence，弱人工智能），像是 Alpha Go，只能应用在单一领域。
* AGI（Artificial General Intelligence，强人工智能，也叫通用人工智能），可以胜任人类几乎所有工作。目前还没有达到，随着 ChatGPT 的问世，这种能力应该很快就会到来。
* ASI（Artificial Superintelligence，超人工智能）。超越人类智慧的人工智能，拥有任何人都无法企及的智慧，这个会更远一些。

技术的发展通常都是一把双刃剑，这篇文章主要就在讲 OpenAI 在考虑和规划 AGI 到来所面临的一系列问题。这个问题不只是 OpenAI 所面临的，而是整个社会都将面临的。

> 我们希望就三个关键问题展开全球性对话：如何管理这些系统，如何公平分配收益，以及如何公平使用。
>
> 随着我们的系统越来越接近 AGI，我们对模型的创建和部署变得越来越谨慎。

2、[GPT4 发布](https://openai.com/research/gpt-4 "GPT4 发布")：GPT 4 相比 3.5 训练量大幅提升，训练参数已超万亿，这使其在多种自然语言处理任务上更加强大。它现在可以识别图像含义，可以快速创建一个完成程序，在多项人类的考试中均获得非常好的成绩。它能做的事情更多，做的速度也更快了。从 3.5 到 4.0 已经是一个非常快的发展，而传言 GPT5 会在年底发布，相比于 GPT 4 它的训练量是这样的：

![](https://cdn.zhangferry.com/Images/202303152247544.png)

那时它会理解视频、声音和对话，AI 的 进化是飞速的，人类有认知上限，AI 则没有，想想都有点让人惊惶失措。

3、[stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui "stable-diffusion-webui")：Stable-diffusion 的 WebUI 版本，支持 Apple Silicon 设备，参考地址：[Installation on Apple Silicon](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Installation-on-Apple-Silicon "Installation on Apple Silicon")。通常运行起来遇到最多的问题就是环境的安装，大部分参照 Issues 都能解决。运行前给 `webui-user.sh`文件添加一个环境变量：

```bash
export COMMANDLINE_ARGS="--skip-torch-cuda-test --upcast-sampling --no-half-vae --use-cpu interrogate --xformers --disable-nan-check"
```

这表示运行 `webui.sh` 命令时填写的参数，以适用于 mac 设备。

运行起来需要现配置模型，再输入关键字。模型有两类，一类叫 base model，像 SD v1.5 、chilloutmix，这类模型通常比较大，一般几个 G。一类叫「修正模型」，像 Lora 就属于修正模型，还会有很多 Lora 的变体模型，这类文件比较小，一般 1 百多 M。模型可以在这个网站下载：[civitai](https://civitai.com/ "civitai")，下面是我跑出来的几张效果图，一张耗时大概 50s。

![](https://cdn.zhangferry.com/Images/00003-1295391836.png)

![](https://cdn.zhangferry.com/Images/00007-3265905480.png)

4、[AJTools - 开发工具](https://github.com/kaqijiang/AJTools-AlfredWorkflowa "AJTools - 开发工具")：一个 Alfred Workflow 工具集，用 Python 实现，封装了一系列开发常用功能。包含：时间戳转换、URL 解析、copy SHH Key、打开当前窗口在iTerm2中、当前文件夹下快速新建文件、ChatGPT聊天等。

5、[苹果内购录：关于新定价规则的理解与思考](https://mp.weixin.qq.com/s/ZQlBFHuRoDYmYpMfgnsp2Q)：苹果在 3 月 9 号 发布了[新的定价规则](https://developer.apple.com/cn/news/?id=dbrszv62 "Apple 新的定价规则")，其中有一些修改点可能会对现有业务逻辑带来一些影响。本文对历史规则进行了回顾，同时也对新的定价规则进行了分析解读。

除此之外，推荐需要处理内购的同学可以关注一下该 `#苹果内购录` 系列文章。



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
