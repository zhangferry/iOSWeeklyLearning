# iOS摸鱼周报 第三十一期

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/iOS摸鱼周报模板.png)

### 本期概要

> * 本期话题：关于 In-App Events 的一些介绍。
> * Tips：优化 Xcode 增量编译的几个小技巧。
> * 面试模块：一道 RunLoop 相关题目。
> * 优秀博客：本期博客主题是 Swift 的高级中间语言：SIL。
> * 学习资料：raywenderlich 新出的 Flutter 教程；一份认知者偏差手册。
> * 开发工具：一个终端命令补全工具：fig。

## 本期话题

本期访谈内容准备有些晚了，暂停一期，下次一定😅。

苹果官网经常会更新一些活动或者开发相关的一些资讯，我们打算定期做一些整理和筛选，以帮助大家了解相关信息。

### In-App Events（App 内活动）

整理编辑：[iHTCboy](https://ihtcboy.com/)

App 内活动是指 App 和游戏内的时效性活动，例如游戏竞赛、电影首映和直播体验等。用户能够直接在 iOS 和 iPadOS 上的 App Store 中探索您的 App 内活动。无论您是想吸引新用户，还是向当前用户提供最新信息，或是与以前的用户重建联系，这项功能都能够助您以全新的方式展示您的活动并扩大其触及的用户群。

苹果在 10 月 22 日开放后台，可以上传活动素材提交审核。需要注意的是，此功能目前是测试阶段，需要开发者接受此协议才生效。

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/WechatIMG312.png)

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/WechatIMG313.png)

2021 年 10 月 27 日起，在 iOS 15 以上设备的 App Store 上，用户可以看到 App 内活动。

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/WechatIMG314.jpeg)


详细，参见：https://developer.apple.com/cn/app-store/in-app-events/

## 开发Tips

### Xcode 增量编译优化

整理编辑：[zhangferry](https://zhangferry.com)

相对于全量编译，增量编译才是平常开发使用最多的场景，所以这方面提升所带来的好处往往更可观。参考苹果文档 [Improving the Speed of Incremental Builds](https://developer.apple.com/documentation/xcode/improving-the-speed-of-incremental-builds "Improving the Speed of Incremental Builds") ，我们可以从多个方面入手优化增量编译。

在开始优化之前更重要的是对编译时间的测量，有衡量指标才能准确分析出我们的优化效果。时间测量可以通过 Xcode 的 `Product > Perform Action > Build With Timing Summary`，然后在编译日志的底部查看各阶段耗时统计。

以下为优化建议：

#### 声明脚本构建阶段脚本和构建规则的 Inputs 和 Outputs

New Build System 每次编译准备执行 Build Phase 中的脚本时，会根据 inputs 和 outputs 的状态来确定是否执行该脚本。以下情况会执行脚本：

* 没有 input 文件
* 没有 output 文件
* input 文件发生变化
* output 丢失

最近遇到一个问题刚好跟这有关，该问题导致增量编译时间很长，耗时主要集中在 CompileAsseetCatalog 阶段。

正常 CocoaPods 在处理资源 Copy 的时候是带有 input 和 output 的，用于减少资源的导入和编译行为，如下图：

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20211027225406.png)

我们项目中有很多私有库，里面引用图片使用了 `Assets.xcassets` 的形式（未封装 Bundle，静态库），这导致一个编译错误：

```
Targets which have multiple asset catalogs that aren't in the same build phase may produce an error regarding a "duplicate output file"
```

这个错误正是 New Build System 带来的，[Build System Release Notes for Xcode 10](https://developer.apple.com/documentation/xcode-release-notes/build-system-release-notes-for-xcode-10 "Build System Release Notes for Xcode 10") 里有说明：

> Targets which have multiple asset catalogs that aren't in the same build phase may produce an error regarding a "duplicate output file". (39810274)
>
> Workaround: Ensure that all asset catalogs are processed by the same build phase in the target.

上面给出了临时的解决方案，就是将所有 asset catalogs 在同一个构建过程处理。对应到 CocoaPods 就是在 Podfile 里添加下面这句：

```ruby
install! 'cocoapods', :disable_input_output_paths => true
```

该设置会关闭资源 Copy 里的 input 和 output，如上面所说，没有 input 和 output，每次都会执行资源的 Copy。因为 Pod 里的`Assets.scassets` 最终会和主项目的 `Assets.scassets `  合到一起编译成 car 文件，所以每次主项目都要等 Pods 的 Copy 完再编译，即使资源文件没有任何变更，这就导致了增量时长的增加。

CocoaPods 仓库里有一个 Issue 在讨论这个问题：[Issue #8122](https://github.com/CocoaPods/CocoaPods/issues/8122 "Issue #8122") 。但该回答下的方案均不适用，后来将私有库中资源引用的方式改为 Bundle，去掉 `disable_input_output_paths` 的设置，增量编译效果得到大幅提升：

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/compile_optimize_timing.png)

其中主要占用编译耗时的 CompileAssetCatalog 阶段直接没有了。

#### 将自己的模块应用 Module Maps

Module Maps 主要缩短的是头文件的引用问题，未 Module 化的时候，编译器会为每一个源文件预处理 `.h` 头文件，Module 之后，不会再预处理，而是为对应的库单独建一个缓存，之后编译重用缓存内容。在制作仓库时只要需要确保 DEFINES_MODULE 为 Yes 就可以了，剩余的工作全都可以 Xcode 代劳。

需要注意，要发挥 Module Maps 的功能，还需要确保在头文件引用时增加库的名字，这样编译器才会知道你有 Module Map。

推荐： `#import <FrameworkName/Header.h>` 

不推荐：`#import <Header.h> ` 或者 `#import "Header.h"`

#### 明确的项目依赖

对于非必要的依赖进行移除，因为过时或多余的依赖关系可能会迫使 Xcode 在并行构建时变成顺序构建。

通常当项目引入新的 Framework 时，Xcode 会自动添加对应依赖，这种是隐式的。比较推荐显示的依赖：在 Build Phases -> Dependencies -> 点加号。

#### 重构 Target 以提高并发能力

分析原有的构建流程，将一些额外的依赖去掉。这个改造成本稍微有点高，但某些情况下应该也能带来较大的提升。

举个例子：当一个 target 依赖多个子 targets 时，Xcode 必须等待所有子 targets 完成才能继续编译当前 target。我们可以考虑分拆依赖关系，最大化利用 Xcode 的并发能力。

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/20211027234051.png)

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

Q：执行以下代码，打印结果是什么？

```objectivec
dispatch_async(dispatch_get_global_queue(0, 0), ^{
    NSLog(@"1");
    [self performSelector:@selector(test) withObject:nil afterDelay:.0];
    NSLog(@"3");
});

- (void)test {
    NSLog(@"2");
}
```

打印结果为 1、3。原因是：

1. `performSelector:withObject:afterDelay:` 的本质是拿到当前线程的 RunLoop 往它里面添加 timer
2. RunLoop 和线程是一一对应关系，子线程默认没有开启 RunLoop
3. 当前 `performSelector:withObject:afterDelay:` 在子线程执行

所以 2 不会打印。


## 优秀博客

SIL：Swift Intermediate Language，SIL 是高级别的中间语言，SIL 由 **SILGen** 生成并由 **IRGen** 转为 LLVM IR ，SIL 会对 Swift 进行较高级别的语义分析和优化。我们看到的 @ 开头修饰的代码基本都属于 SIL 范畴。

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

1、[Swift的高级中间语言：SIL](https://www.jianshu.com/p/c2880460c6cd "Swift的高级中间语言：SIL") -- 来自简书：sea_biscute

[@东坡肘子](https://www.fatbobman.com)：在 LLVM 的官方文档中对 Swift 的编译器设计描述如下： Swift 编程语言是在 LLVM 上构建，并且使用 LLVM IR 和 LLVM 的后端去生成代码。但是 Swift 编译器还包含新的高级别的中间语言，称为 SIL。SIL 会对 Swift 进行较高级别的语义分析和优化。 本文将分析一下 SIL 设计的动机和 SIL 的应用，包括高级别的语义分析，诊断转换，去虚拟化，特化，引用计数优化，TBAA（Type Based Alias Analysis）等。并且会在某些流程中加入对 SIL 和 LLVM IR 对比。

2、[一文看破Swift枚举本质](https://mp.weixin.qq.com/s/Gx7L_Ev0DV19mLYMnH-R1Q "一文看破Swift枚举本质") -- 来自：狐友技术团队

[@东坡肘子](https://www.fatbobman.com)：SIL 在实际工作中的应用举例。通过分析内存布局、查看 SIL 源码等方式来探索一下枚举的底层到底是什么样子的。在 Swift 中枚举不仅仅只是一个用来区分类型的常量了，枚举的功能被大大的加强。枚举可以设置原始值，添加关联值，甚至可以添加计算属性（不能添加存储属性），定义方法，实现协议，其功能仅次于一个 Class 对象了，那么 Swift 的枚举到底是怎样实现这些功能的呢？

3、[Swift Intermediate Language 初探](https://zhuanlan.zhihu.com/p/101898915 "Swift Intermediate Language 初探") -- 来自简书：sea_biscute

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：文章简单介绍了 SIL 以及 SIL 在 LLVM 架构中的位置。正文部分作者通过 SIL 分析来解释 extension 中 protocol 函数和对象中的 protocol 函数调用选择的问题。

4、[Swift编译器中间码SIL](https://woshiccm.github.io/posts/Swift%E7%BC%96%E8%AF%91%E5%99%A8%E4%B8%AD%E9%97%B4%E7%A0%81SIL/ "Swift编译器中间码SIL") -- 来自博客：roy's blog

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：作者首先介绍了 SIL 的设计初衷以及与 LLVM IR 的区别。文中还介绍了 SSA（ static single-assignment）中“代”的概念以及 SSA 的益处。SIL 是命名函数的集合，SIL 源文件为 Module，通过 Module 可以遍历 Module 中的函数。

5、[Swift Intermediate Language —— A high level IR to complement LLVM](https://llvm.org/devmtg/2015-10/slides/GroffLattner-SILHighLevelIR.pdf "Swift Intermediate Language —— A high level IR to complement LLVM") -- 来自：Joe Groff 和 Chris Lattner

[@我是熊大](https://github.com/Tliens)：在 LLVM 开发人员会议上 Groff 和 Chris Lattner 通过简报的方式对 SIL 进行了详细的介绍。内容包括：为什么要使用 SIL、SIL 的设计逻辑、Swift 对 SIL 的使用等内容。尽管简报为英文，但主要以代码和图表为主，对了解 SIL 的设计动机和设计原理有很大的帮助。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Flutter Apprentice from raywenderlich

地址：https://www.raywenderlich.com/books/flutter-apprentice

raywenderlich 新出的 Flutter 教程，该网站的教程一直以简单易懂、清晰明了为特点，如果是想入门 Flutter 的话，这本书将会是不错的选择。另外该网站的 Swift Apprentice 也出了新的版本，有兴趣重温一下的小伙伴也可以阅读一下。

### 认知偏差知识手册

地址：https://s75w5y7vut.feishu.cn/docs/doccn3BatnScBJe7wD7K3S5poFf

一份心理学知识词条的普及手册，无关乎代码，但是对互联网工作者来说，阅读之后也许可以让你更加了解产品与用户之间的关系，能够提升产品的细节，用户的体验等等。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### fig

**地址**：https://fig.io/

**软件状态**：免费，[开源](https://github.com/Coder-Star/autocomplete)

**软件介绍**：

`fig` 是一个开源的终端自动补全工具，支持数百个 CLI 工具，如 `git`、`docker`、`npm `等等，并且可以无缝添加到你现有的终端，如 `iTerm`、`Hyper`、`VSCode` 和 `macOS 终端`，支持我们自己自定义一些补全规则。

![fig](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/Snipaste_2021-10-27_21-04-03.png)
## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第三十期](https://mp.weixin.qq.com/s/KNyIcOKGfY5Ok-oSQqLs6w)

[iOS摸鱼周报 第二十九期](https://mp.weixin.qq.com/s/TVBQgYuycelGBwTaCSfmxQ)

[iOS摸鱼周报 第二十八期](https://mp.weixin.qq.com/s/dKOkF_P5JvQnDLq09DOzaQ)

[iOS摸鱼周报 第二十七期](https://mp.weixin.qq.com/s/WvctY6OG1joJez2g6owroA)

![](http://r9ccmp2wy.hb-bkt.clouddn.com/Images/WechatIMG384.jpeg)
