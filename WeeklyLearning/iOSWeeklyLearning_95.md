# iOS 摸鱼周报 #95 | WWDC23 is coming

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：WWDC23 定档；Xcode 14.3.1 RC 版本已修复打包导致的崩溃问题
> * 本周学习：Python 导入时运行时、跨文件引用、导入 C 语言库时的几个开发知识点
> * 内容推荐：关于在 App Store 推广应用的技巧、SwiftUI 预览的工作原理、离屏渲染等方面的内容
> * 摸一下鱼：WWDC23 内参招募；微软 Build 大会一些让人惊艳的 AI 产品；让 AI 玩Minecraft；一个易使用的 AI 程序创建平台；Apple Design Awards 决赛名单公布
> * iOS 招聘：抖音外卖方向 - 北京

## 本期话题

### [WWDC23 定档](https://developer.apple.com/wwdc23/ "WWDC23 定档")

![](https://cdn.zhangferry.com/Images/202305250758432.png)

WWDC23 时间公布，北京时间 6 月 6 号凌晨一点。

根据外网信息，本次发布会会有常规系统升级： iOS/iPadOS 17、macOS 14、watchOS 10；15'' Macbook Air；头显设备及对应的 xrOS。是否真的会发布头显设备？头显设备有哪些亮点，能否激起用户的购买欲望？让我们拭目以待吧。

![](https://cdn.zhangferry.com/Images/202305312354111.png)

对于当前非常火的 AI 能力，Google IO 和 Microsoft Build 都已经发布了很多重量更新，不知道 Apple 在这方面有没有相应产品发布。

### [Xcode 14.3.1 RC 版本已修复打包导致的崩溃问题](https://developer.apple.com/forums/thread/727680#753414022 "Xcode 14.3.1 RC 版本已修复打包导致的崩溃问题")

[@远恒之义](https://github.com/eternaljust)：Apple 于 2023 年 5 月 17 日发布 Xcode 14.3.1 RC 版本，修复了在 Xcode 14.3 打包导致 iOS 13 系统上的崩溃问题。根据最新的版本发行说明，该问题表现为：用 Xcode 14.3 打包 Swift 项目混编 OC 协议，会导致在 iOS 13 系统出现启动崩溃：

``` 
(When targeting devices running iOS 13, apps built with Xcode 14.3 and using Objective-C protocols from Swift, sometimes crash at launch)。
```

Apple 已从 2023 年 4 月 25 日起，限制了最新提交至 App Store 的 App 必须使用 Xcode 14.1 或更高版本构建，还在使用低版本 Xcode 的同学，建议下载最新的 [Xcode 14.3.1 RC 版本](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_14.3.1_Release_Candidate/Xcode_14.3.1_Release_Candidate.xip "Xcode 14.3.1 RC 版本")来打包。

## 本周学习

整理编辑：[zhangferry](https://zhangferry.com)

本期分享几个 Python 相关的小知识。

### 导入时与运行时

Python 作为解释型语言，没有编译时，但会有导入时和运行时。但所有编程语言的执行最终也是需要转成机器码的，在 Python 里这个过程就发生在导入时，即解释 `import xx` 语言的时候。这时 Python 源码会被转成字节码，存储在 `.pyc`文件中，后续再执行相应的语句，就不再有转码过程，而是直接读取`.pyc`文件以提高速度。只有相应源码被修改才会再重新生成 `.pyc`文件。运行时则表示实际执行到对应的代码时。

因为这些特性会出现一个常见的状况，我们在一个文件里，先后定义了基类Base和子类AImp和BImp，当我们想要在Base中使用BImp时，考虑到执行顺序，我们只能在运行时进行导入。

```python
print(f"Outer: {AImp()}") # 引用时执行 error

class Base:
    print(f"Base {AImp()}") # 引用时执行 error
    def factory(self):
        print(f"Base: {AImp()}") # 运行时执行
        pass

class AImp(Base):
    def do_things(self):
        pass
```

### 跨文件引用

下面是一个 Python 项目，src 存放源码，tests 存放单测文件。

```python
- ExamplePackage
  - src  
      - src_1.py
      - src_2.py
  - tests
      - tests_1.py  
      - tests_2.py
```

会出现如何引用关系：

1、同文件夹引用

src_1.py 引用 src_2.py 里的内容。可以使用 `from src_2 import *`或者`from .src_2 import *`两种方案。差别是前者为绝对路径，后者为相对路径，相对路径，只能整体当做一个包才能运行。在有相对应用的情况下，直接调用：`python package/src/src1.py`，会报 `ImportError: attempted relative import with no known parent package`。

2、跨文件引用

让 tests_1.py 去使用 src_2.py 里的类或函数进行测试，如果src_2里没有任何引用，我们使用 `from src.src_2 import *`总是没问题的。而如果 src_2 里又引用了 src_1则可能出问题，这取决于我们在上一步同文件夹引用里 src 文件如何相互引用。相对引用不会有问题，绝对引用则会报异常：`ModuleNotFoundError: No module named 'src_1'`，因为处理 tests_1.py 时所有的引用关系都是基于其所在文件的。此时的解决方案是手动添加 src_1 这个 module，要在引用语句之前这样处理：

```python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
```

sys.path 相当于 iOS 中的 `DYLD_LIBRARY_PATH` ，它可以指定查找 module 的路径，打印该变量：

```python
[
  'path/to/ExamplePackage/src', 
  'path/to/ExamplePackage/tests',
  'path/to/ExamplePackage',
  'path/to/ExamplePackage/venv/lib/python3.9/site-packages'
]
```

除了我们往第一个位置插入的 src 目录外，执行时还会把test_1.py 所在目录，以及工程目录导进去。最后那个 venv 目录是 Python 的虚拟环境，它是环境创建时添加的，所以放在 site-packages 目录下的 module，我们都可以直接使用。

### Python 中调用 C 语言的库提示依赖找不到

我们可以在依赖搜索的环境变量 `DYLD_FRAMEWORK_PATH`里加入对应的路径，后来遇到一个问题，导致仍会出现问题。后来直接引用该依赖库，这样它也可以直被检索出来。

```python
modules = ctypes.CDLL('path/to/depsmodules.dylib')
```

后来又想到 `DYLD_LIBRARY_PATH`这个环境变量，才理解当时依赖找不到是因为其中包含了一个 dylib 后缀的动态库。`DYLD_FRAMEWORK_PATH` 和 `DYLD_FRAMEWORK_PATH` 这俩环境变量的区别是，前者用于检索 .framework 结尾的动态库，后者用于检索 .dylib 结尾的动态库。

Xcode 的编译选项还有很多以 LIBRARY 和 FRAMEWORK 区分的同类型环境变量，它们的作用也都是类似的。

## 内容推荐

推荐近期的一些优秀博文，涵盖：在 App Store 推广应用的技巧、SwiftUI 预览的工作原理、离屏渲染等方面的内容。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[在 App Store 中推广你的应用的 10 个技巧](https://www.avanderlee.com/optimization/getting-app-featured-app-store/ "在 App Store 推广你的应用的 10 个技巧") -- 作者：Antoine Van Der Lee

[@东坡肘子](https://www.fatbobman.com/): Antoine Van Der Lee 是一位知名博主，同时也开发了大量应用程序。在这篇文章中，他分享了一些获得苹果推荐的技巧和诀窍，有助于提高你的应用在 App Store 特色推荐中的曝光率。主要建议包括：告知苹果你的应用的存在、从苹果编辑团队的角度思考、优化你的 App Store 页面、本地化你的应用、获取更多评分、成为一个好的应用公民、让你的应用更无障碍、降低崩溃率、创新和采用最新功能、让你的应用更独特。提高应用的整体质量、经常填写推广表格告知苹果应用的新功能，可以增加推荐机会。

2、[在 CI/CD 中使用私有 Swift 包](https://www.polpiella.dev/private-swift-packages-on-ci-cd/ "在 CI/CD 中使用私有 Swift 包") -- 作者：Pol Piella Abadia

[@东坡肘子](https://www.fatbobman.com/): 这篇文章探讨了如何在持续集成环境下安全使用私有代码包,特别是 Swift 包。通过配置 Git 和访问令牌管理，作者设计了一种机制，可以在构建流程中临时获取访问权限，并在流程结束后立即撤销，保证私有包的安全与隐私。这种方法不但可以在本地开发环境和 CI、CD 环境保持一致的包依赖配置，还可以根据需要灵活地控制私有包的访问时长，值得 iOS 开发者学习和运用。除 Swift 包外，该方法也可以应用于其他语言和构建工具，对保护私有代码仓库安全至关重要。

3、[构建稳定的预览视图 —— SwiftUI 预览的工作原理](https://www.fatbobman.com/posts/how-SwiftUI-Preview-works/ "构建稳定的预览视图 —— SwiftUI 预览的工作原理") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 在这篇文章中，作者通过分析一段会导致预览视图崩溃的代码，向读者揭示了 SwiftUI 预览的工作原理和流程，包括生成衍生代码、准备项目资源、启动预览线程、加载衍生代码库、通过 XPC 进行通讯等操作。通过对原理的探讨，让读者认识到预览功能客观存在的局限性：虽然 Xcode 预览功能在视图开发流程中极为方便，但它仍处在一个功能受限的环境中。开发者使用预览时需要清醒地认识到其局限性，并避免在预览中实现超出其能力范围的功能。在下一篇文章中，作者还将会从开发者的角度来审视预览功能：它的设计目的、最适宜的使用场景以及如何构建稳定高效的预览。

4、[​一文学会 iOS 画中画浮窗](https://mp.weixin.qq.com/s/SDasEZ2cYmm9Kim0KlHicw) -- 作者：王德亮 搜狐技术产品

[@东坡肘子](https://www.fatbobman.com/): 在这篇文章中，作者详细介绍了两种实现 iOS 画中画浮动窗口的方法：将视图转换为视频并播放，以及播放空白视频并在窗口中显示视图。这两种方法都可以实现自定义画中画显示的效果。第一种方法提供了更多自定义显示的灵活性，但消耗更多 CPU 资源；第二种方法更轻量级，但需要依赖空白视频文件。因此，开发者应根据具体需求，选择方法时应考虑灵活性和资源消耗之间的平衡。

5、[离屏渲染](https://juejin.cn/post/7214018170833928250 "离屏渲染") -- 作者：Jony唐

[@东坡肘子](https://www.fatbobman.com/): 在 iOS 开发中，避免离屏渲染是提高应用性能的重要方法之一。离屏渲染会增加 GPU 的工作量和内存消耗，甚至可能降低性能。因此，重要的是要理解什么是离屏渲染及其影响因素。本文作者通过两篇文章深入探讨了离屏渲染，以及 UIKit 下常见的触发离屏渲染的操作。同时，作者也介绍了对应的优化技巧，以帮助开发者避免这些潜在的性能陷阱。这些知识不仅适用于 UIKit，也同样适用于 SwiftUI 开发。掌握它们可以更高效地开发出性能卓越的 iOS 应用。

## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[《WWDC23 内参》免费领取及作者&审核招募](https://mp.weixin.qq.com/s/S04VnQRDNIcjZUJ8xCrQBg)：WWDC 大会即将到来，老司机技术将继续创作《WWDC23 内参》，并**免费**提供给所有关注者。关注「老司机技术」公众号，回复「2023」，免费领取。同时也欢迎有相应经验或资深的开发者一起创作 《WWDC23 内参》。

2、[微软 Build 2023](https://news.microsoft.com/build-2023/ "微软 Build 2023")，我只看了 Keynote 里的内容，已经被震撼到了，微软太强了，对 AI 能力的规划超出了绝大数人的想象。本次 Build 大会会公布 50+ new updates，本节视频只列出了 5 个：

* Bring Bing to ChatGPT：之前是把 GPT4 迁移至 Bing，面对的是搜索场景；现在把 Bing 迁移至 GPT-4，双向合作，这个场景不仅仅是聊天了，还有一系列围绕 ChatGPT 搭建的产品体系，将都可以访问 ChatGPT 和 Bing 这两个庞大的数据信息，这个增强会是大杀器。
* Windows Copilot：  Windows 11 菜单栏将会有一个常驻的 AI 交互入口，你可以随时唤起它，提出自己的诉求，像是系统配置、文件分析、推荐音乐、设计Logo等等，并直接在交互框里完成相应的功能唤出，演示的效果贼酷。把 AI 入口嵌入到操作系统，真的太绝了，macOS 啥时候才能享受这样的功能啊🙃
* Copilot Stacks：微软致力于打造一个基于 AI Plugin 的 Copilot 生态，通过 Azure 提供一系列基础能力供开发者使用，微软系产品的插件标准也将跟 ChatGPT 的插件保持一致。以后没有 AI 能力的应用就像现在没有联网的应用一样。
	![](https://cdn.zhangferry.com/Images/202305252317906.png)
* Azure AI Studio：为 Copilot 生态提供支持的一整套开发基建服务，包含创建、自定义模型、训练、评估、发布等环节，以创建新一代的 AI 应用。
* Mrcrosoft Fabric：一个为 AI 应用配套的数据分析平台，既有用于监控和分析当前应用的使用情况。

3、[Voyager](https://github.com/MineDojo/Voyager "Voyager")：一个应用到 Minecraft 的开放式大语言模型代理。它通过不断探索世界、获取多样化技能和进行新的发现，可以实现无人操作，并完成高分。Voyager 通过黑盒查询与 GPT-4 进行交互，避免了模型参数微调的需要。实证结果显示，Voyager 在上下文中具有强大的终身学习能力，并在玩 Minecraft 方面表现出色。

![](https://cdn.zhangferry.com/Images/202305271338022.png)

![](https://cdn.zhangferry.com/Images/202305271338598.png)

4、[Dify](https://dify.ai/ "Dify")：Dify 是一个易于使用的 LLMOps 平台，旨在赋予更多人创建可持续的 AI 原生应用程序的能力。Dify 提供可视化编排支持各种应用类型，提供开箱即用的应用程序，也可以作为后端服务API使用。通过一个API整合插件和数据集，使用单一界面进行提示工程、可视化分析和持续改进，统一开发流程。Dify 兼容 Langchain，逐步支持多个 LLM，目前支持的有：GPT 3 (text-davinci-003)、GPT 3.5 Turbo(ChatGPT)、GPT-4。

![](https://cdn.zhangferry.com/Images/202305271349547.png)

5、[Apple Design Awards](https://developer.apple.com/design/awards/ "Apple Design Awards") 设计奖决赛产品名单公布，WWDC 期间将公布决胜者。

![](https://cdn.zhangferry.com/Images/202305252206602.png)

6、[WWDC23 随堂小测](https://www.swiftjectivec.com/wwdc-2023-the-pregame-quiz/ "WWDC23 随堂小测")：Swiftjective-C 做的一个 WWDC 小测试，里面有历年的 WWDC 知识点合集，试一下你能答多少分。

![](https://cdn.zhangferry.com/Images/202306010005211.png)

## iOS 招聘 - 抖音外卖方向

### 岗位要求

* 负责抖音App内生活服务业务研发, 编写高质量的代码；

- 熟悉 React Native、小程序等 Hybrid 技术开发，掌握跨端渲染框架开发，或相关优化经验优先。
- 熟悉 APP 性能优化手段和工具，在首屏渲染、流畅度、网络、内存、功耗等方面有过研究，主导过体验优化项目者优先。
- 良好的协调和推动能力，有技术方案的能独立规划、落地、沉淀、输出经验，了组织过（iOS、Android、FE、Server）多端参与技术项目者优先。

工作地点：北京

联系微信号：zhangferry

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #94 | 前端项目开发流程学习](https://mp.weixin.qq.com/s/f2Z1VRpk4Ehh3KxuY_NrvA)

[iOS 摸鱼周报 #93 | AIGC 尝试](https://mp.weixin.qq.com/s/ios0QYKmnYtJ8URvZLJ1TA)

[iOS 摸鱼周报 #92 | Swift Foundation 预览版发布](https://mp.weixin.qq.com/s/AQaY2DA2h8S-XEYoQ0u7Ew)

[iOS 摸鱼周报 #91 | 免费的网站托管平台 Vercel](https://mp.weixin.qq.com/s/93YLa8ankkEVcp4pop2A6A)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
