# iOS 摸鱼周报 #80 | ChatGPT 的风又起来了

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：各大搜索引擎开始接入类 ChatGPT 功能
> * 本周学习：Python 中的匿名函数与闭包
> * 内容推荐：iOS 越狱检测、获取虚拟内存状态、使用 KeyChain 进行持久化等内容
> * 摸一下鱼：Stable Diffusion 功能尝鲜；关于技术规划的思考；大厂复盘文档

## 本期话题

整理编辑：[zhangferry](zhangferry.com)

### ChatGPT 的风又起来了

最近 ChatGPT 又火了一波，不仅搜索引擎纷纷引入类 ChatGPT 能力，就连各种跟 ChatGPT 沾边公司的公司股价都涨了一波。随着新用户的不断涌入，官网已经多次停止用户登录了。

![](https://cdn.zhangferry.com/Images/20230207235606.png)

搜索引擎盯上 ChatGPT 是自然而然的事情，早在 ChatGPT 开发之初就有它能否代替 Google 的讨论，因为它大多数使用场景跟搜索重叠很高。能否替换 Google 还有待验证，但 StackOverflow 受到的影响已经非常明显，根据报道 StackOverflow 一个月内访问量骤降 3200w。这已经促使大部分产品不得不考虑 ChatGPT 的影响，以及如何让自己的产品利用类似能力。

1、[Google 宣布了 ChatGPT 的竞争对手 Bard](https://www.theverge.com/2023/2/6/23588033/google-chatgpt-rival-bard-testing-rollout-features "Google 宣布了 ChatGPT 的竞争对手 Bard")，一个基于 LaMDA 模型训练的智能对话服务。该服务正在做最后的测试，未来几周会更大范围的对外开放。

![](https://cdn.zhangferry.com/Images/20230207232302.png)

2、微软的 「new Bing」 整合 ChatGPT 的能力已经可以尝试了，不过并没有全量放开。访问：https://www.bing.com/new，登录账号，可以加入候选等待名单，通过之后可以正常使用 new Bing。

![](https://cdn.zhangferry.com/Images/20230209200203.png)

OpenAI 对外开放的 ChatGPT 是基于 GPT 3.5 的，这个能力已经非常惊艳，Bing 则是使用训练量更大的 GPT-4 模型。根据训练模型评估，GPT 3.5 就已经超过了 Google 的 LaMDA，所以就回答准确性 new Bing 应该稳稳强于Bard 的。微软能否抢占一些搜索引擎的份额就看这次发挥了。

3、[百度也宣称推出类 ChatGPT 服务](http://www.chinanews.com.cn/cj/2023/02-07/9949192.shtml "百度也宣称推出类 ChatGPT 服务")，即将上线聊天机器人「文心一言」，3 月完成内测。未说明使用的技术，因为百度在人工智能方面布局还比较多，应该是使用自己的训练模型，具体效果如何要等上线之后来看了。

## 本周学习

整理编辑：[zhangferry](https://zhangferry.com)

### Python 中的匿名函数与闭包

Python 中正常的函数是这样的：

```python
# 函数名是 add
def add(x, y):
    return x + y
```

匿名函数是没有函数名的函数，但可以做一些函数做的事情，对应就指 Lambda 表达式。

```python
func = lambda x, y: x + y
    print(func(1, 2)) # 3
```

关于闭包可以先看一个计算平均数的例子：

```python
def make_averager():
    # 以下整体属于闭包 
    series = []  # 自由变量

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return averager

avg = make_averager() # 可调用对象
print(avg(10))  # 10.0
print(avg(11))  # 10.5
print(avg(12))  # 11.0
```

`make_averager()`创建了一个 `avg`，它表示内部函数`averager`。正常来说一个函数调用完之后就返回了，本地作用域数据也就释放了，为什么它还可以存储数据呢？数据是存在哪里了呢？

关键点就在于那个自由变量 `series`。Python 里的函数有几个内部属性，`avg.__code__`表示编译后的定义体：

```python
# 局部变量
avg.__code__.co_varnames
('new_value', 'total')
# 自由变量
avg.__code__.co_freevars
('series',)
```

再看闭包的内容`avg.__closure__`：

![](https://cdn.zhangferry.com/Images/20230210000433.png)

我们传入的值都存放到了闭包里。再说回闭包，**闭包也是一种函数，它会保留定义函数时存在的自由变量的绑定，这样调用函数时，虽然定义作用域不可用了，但是仍能使用那些绑定**。自由变量的生命周期是跟着闭包走的。

再稍微改下代码：

```python
def make_averager():
    count = 0
    total = 0
    def averager(new_value):
        count+= 1
        total+= new_value
        return total / count
    return averager
```

这个代码在 PyCharm 里会直接报编译错误，用命令行执行报 `UnboundLocalError: local variable 'count' referenced before assignment`，提示变量未定义，但实际问题是这里变量类型有冲突。默认闭包内部函数外的变量为自由变量，但内部函数里包含赋值语句，这样count 和 total 就应该是局部变量了，两者冲突引发问题。

修改方式是引入 `nolocal` 字段，告诉编译器它不是局部变量，而是自由变量，就可以正常赋值了。

```python
def make_averager():
    count = 0
    total = 0
    def averager(new_value):
    		nonlocal count, total
        count+= 1
        total+= new_value
        return total / count
    return averager
```


## 内容推荐

本期将推荐近期的一些优秀博文，涵盖 iOS 越狱检测、获取虚拟内存状态、使用 KeyChain 进行持久化 以及 SwiftGG 但新项目等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[iOS 数据持久化 —— KeyChain](https://juejin.cn/post/7195486949526732857 "iOS 数据持久化 —— KeyChain") -- 来自：庄周晓梦

[@东坡肘子](https://www.fatbobman.com/): 为了安全的在本地存储敏感数据，不少开发者都会采用系统提供的 KeyChain 框架。在本文中，作者将为你展示如何创建一个通用的同时适用于 iOS、 MacOS 的 keyChain 辅助类，以提高数据增删改查操作的便利性。

2、[2023 年 iOS 越狱检测](https://blog.eidinger.info/ios-jailbreak-detection-in-2023 "2023 年 iOS 越狱检测t") -- 来自：Marco Eidinger

[@东坡肘子](https://www.fatbobman.com/): 在这篇博文中，作者将展示现有的检测越狱的方法并分享代码示例。但更重要的是，通过讨论越狱检测的动机、分享相关实现并提供信息，方便开发者评估越狱检测在 2023 年（或总体上）是否仍是一个好主意。

3、[SwiftUI Layout](https://juejin.cn/post/7196952530256724023 "SwiftUI Layout") -- 来自：东吴贾诩

[@东坡肘子](https://www.fatbobman.com/): 本文作者对 SwiftUI 4 中提供的 Layout 协议做了比较详尽的说明。即使你目前仍使用老版本的 SwiftUI ，通过本文可以了解更多有关 SwiftUI 布局的内部逻辑。

4、[好久不见，SwiftGG](https://mp.weixin.qq.com/s/aK7L3MIyF_ftCh3gvrovuA "好久不见，SwiftGG") -- 来自：SwiftGG

[@东坡肘子](https://www.fatbobman.com/): SwiftGG 是国内知名的苹果生态开发社区，尽管它的公众号处于歇业状态已经很久了，但 SwiftGG 翻译组在这几年并没有处于停滞状态。在本文中，SwiftGG 对近两年的工作进行了总结，并介绍了接下来一些新的计划和打算。同时，也回答了一些网友提出的问题。

5、[iOS APP虚拟内存用量初探](https://mp.weixin.qq.com/s/aK7L3MIyF_ftCh3gvrovuA "iOS APP虚拟内存用量初探") -- 来自：呦呦君

[@东坡肘子](https://www.fatbobman.com/): 在作者当前的项目中有用于 APP 物理内存、系统物理内存等内存状态的获取 API，但是一直缺少获取虚拟内存的 API。由于之前业务上出现过因为虚拟内存耗尽所导致的 Crash，因此本文将基于以上的背景对虚拟内存进行一些调研与探讨。

## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[diffusionbee-stable](https://github.com/divamgupta/diffusionbee-stable-diffusion-ui "diffusionbee-stable")：Stable Diffusion 是一个开源的人工智能模型，它可以根据文字描述生成一张图像。现在已经有不少图像类项目基于这个模型进行产品设计。如果你想本地跑这个模型的话，还需要租用 GPU，配置也比较麻烦。因为 PyTorch 对苹果的 ARM 芯片进行了完善的支持，已经完全可以用手头的 M1/M2 设备去运行 Stable Diffusion 了。Github 有一个开源项目 diffusionbee，把整个配置流程封装到了一个 Mac Applicaiton 上，我们可以更快速的体验这项功能。项目依赖模型将近 8 个 G，下载体验需要准备好足够的磁盘空间。

![](https://cdn.zhangferry.com/Images/20230206003633.png)

2、[技术三板斧：关于技术规划、管理、架构的思考](https://mp.weixin.qq.com/s/vL9_PQBCDxEgCyzh1lGFeQ)：最近关于技术规划写了不少，参考了团队内部其他人的技术规划文档，也查了一些技术规划相关的文章，对如何做技术规划有这些总结。

第一步：问题分析。如果是从零开始的项目，分析的是痛点，如果是已有项目分析的是现状。这里要结合数据指标，客户反馈，历史事件，并对未来有一定畅想。

第二步：目标制定。目标选择要结合上一步的问题分析，用于解决实际痛点。目标制定要具体明确可量化，对每个目标进行拆解，确定实现路径。

第三步：以终为始。以最终结果溯源开始，明确时间节点，设置可验收的 Milestone。项目结果从业务、平台、效能视角等视角审视结果。

3、[大厂项目复盘](https://www.yuque.com/wikidesign/ykf0s9/vki4ecckwzsqaky3 "大厂项目复盘")：UED 方向的各大厂项目复盘文档汇总。

![](https://cdn.zhangferry.com/Images/20230205233726.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #82 | 去中心化社交软件 Damus](https://mp.weixin.qq.com/s/ck4Jn4Cq-yOs_mjAO-WacA)

[iOS 摸鱼周报 #81 | Apple 推出 Apple Business Connect](https://mp.weixin.qq.com/s/Ek6W0MTBDP6PN1uxWQ5M_A)

[iOS 摸鱼周报 #80 | 开发加速器 SwiftUI 中管理数据模型](https://mp.weixin.qq.com/s/eIQLuAIsRQ7eeEnsrL5QuA)

[iOS 摸鱼周报 #79 | Freeform上线 & D2 本周开始](https://mp.weixin.qq.com/s/HdEhmXt60853tzM6xiVUwA)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
