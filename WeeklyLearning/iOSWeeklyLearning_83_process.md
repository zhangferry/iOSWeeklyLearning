# iOS 摸鱼周报 #80 |Developer 设计开发加速器话题，SwiftUI 中管理数据模型

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题



## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### iOS 堆栈调用理论回顾


## 内容推荐

整理编辑：[@远恒之义](https://github.com/eternaljust)



## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、最近 ChatGPT 好像又火了一下，随着新用户的不断涌入，官网已经停止用户登录了。

![](https://cdn.zhangferry.com/Images/20230207235606.png)

各大搜索引擎都看到人工智能对话能力的商业价值，纷纷计划推出类 ChatGPT 功能。

* [Google 宣布了 ChatGPT 的竞争对手 Bard](https://www.theverge.com/2023/2/6/23588033/google-chatgpt-rival-bard-testing-rollout-features "Google 宣布了 ChatGPT 的竞争对手 Bard")，一个基于 LaMDA 模型训练的智能对话服务。该服务正在做最后的测试，未来几周会更大范围的对外开放。

![](https://cdn.zhangferry.com/Images/20230207232302.png)

* 据报道，[微软正在将 ChatGPT 整合到 Bing 中](https://www.theverge.com/2023/2/3/23584675/microsoft-ai-bing-chatgpt-screenshots-leak "微软正在将 ChatGPT 整合到 Bing 中")，甚至有不少用户反馈已经看到了 「new Bing」的界面。OpenAI 对外开放的 ChatGPT 是基于 GPT 3.5 的，这个能力已经非常惊艳，Bing 则很有可能是使用训练量更大的 GPT-4 模型。「new Bing」 能否弯道加速，抢占一些 Google 的市场份额就看这次了。 

![](https://cdn.zhangferry.com/Images/20230207233017.png)

* [百度也宣称推出类 ChatGPT 服务](http://www.chinanews.com.cn/cj/2023/02-07/9949192.shtml "百度也宣称推出类 ChatGPT 服务")，即将上线聊天机器人「文心一言」，3 月完成内测。百度在人工智能方面布局还比较多，有可能是使用自己的训练模型来实现。

2、[diffusionbee-stable](https://github.com/divamgupta/diffusionbee-stable-diffusion-ui "diffusionbee-stable")：Stable Diffusion 是一个开源的人工智能模型，它可以根据文字描述生成一张图像。现在已经有不少图像类项目基于这个模型进行产品设计。如果你想本地跑这个模型的话，还需要租用 GPU，配置也比较麻烦。因为 PyTorch 对苹果的 ARM 芯片进行了完善的支持，已经完全可以用手头的 M1/M2 设备去运行 Stable Diffusion 了。Github 有一个开源项目 diffusionbee，把整个配置流程封装到了一个 Mac Applicaiton 上，我们可以更快速的体验这项功能。项目依赖模型将近 8 个 G，下载体验需要准备好足够的磁盘空间。

![](https://cdn.zhangferry.com/Images/20230206003633.png)

3、[技术三板斧：关于技术规划、管理、架构的思考](https://mp.weixin.qq.com/s/vL9_PQBCDxEgCyzh1lGFeQ)：最近关于技术规划写了不少，参考了团队内部其他人的技术规划文档，也查了一些技术规划相关的文章，对如何做技术规划有这些总结。

第一步：问题分析。如果是从零开始的项目，分析的是痛点，如果是已有项目分析的是现状。这里要结合数据指标，客户反馈，历史事件，并对未来有一定畅想。

第二步：目标制定。目标选择要结合上一步的问题分析，用于解决实际痛点。目标制定要具体明确可量化，对每个目标进行拆解，确定实现路径。

第三步：以终为始。以最终结果溯源开始，明确时间节点，设置可验收的 Milestone。项目结果从业务、平台、效能视角等视角审视结果。

4、[大厂项目复盘](https://www.yuque.com/wikidesign/ykf0s9/vki4ecckwzsqaky3 "大厂项目复盘")：UED 方向的各大厂项目复盘文档汇总。

![](https://cdn.zhangferry.com/Images/20230205233726.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

[iOS 摸鱼周报 #78 |  用 ChatGPT 做点好玩的事 ](https://mp.weixin.qq.com/s/27J4NguYRsxYWmff_6iDcg)

[iOS 摸鱼周报 #77 | 圣诞将至，请注意 App 审核进度问题](https://mp.weixin.qq.com/s/yYdGO1kRcwQJ3-z-aavHYA)

[iOS 摸鱼周报 #76 | 程序员提问的智慧](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
