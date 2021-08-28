# iOS摸鱼周报 第二十五期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：本期跟竹立交流一下关于求职和学习方法的话题。
> * Tips：如何清除启动图的缓存；如何优化SwiftLint流程。
> * 面试模块：
> * 优秀博客：整理了 Swift 泛型相关的几篇文章。
> * 学习资料：Adobe 的调色板网站：Adobe Color Wheel；知识小集的 Tips 汇总：Awesome-tips。
> * 开发工具：管理 Github 项目 Star 的工具：OhMyStar。

## 本期话题

[@zhangferry](https://zhangferry.com)：本期交流的小伙伴是摸鱼周报的另一位编辑：竹立。这个名字大家可能比较陌生，但是他的 ID 应该有很多人都听过：[皮拉夫大王](https://www.jianshu.com/u/739b677928f7)。竹立是一位非常资深的 iOS 开发，本期围绕职场和学习主题，跟他进行了一些交流。大家如果还有其他问题想问竹立的，可以留言区告诉我们。

zhangferry：简单介绍下自己吧。

> 大家好，我是来自 58 同城的邓竹立，目前在团队中主要负责 iOS 的性能优化及稳定性建设。

zhangferry：你对二进制的研究很深入，还在社区做过一次玩转二进制的直播分享，为什么会对这一领域感兴趣？能讲一些想要学好这方面内容的几点建议吗？

> 我对二进制的研究还远远算不上深入，可能在个别细分的领域有一点探索，但是从整体来说二进制涉及的知识太庞大，因此还算不上深入。对二进制的探索主要是之前的技术项目所引导的。当时在做技术项目时遇到了一个问题：“如何动态调用项目中的static C 函数？”，当时感觉研究的方向应该为mach-o文件，最终随着调研的慢慢深入，也就对二进制文件有了一定的了解。
>
> 想要学习二进制相关的内容其实我没有特别好的建议，因为我并没有成体系的去学习这方面内容，更多的是利用空闲时间凭借个人的兴趣去探索。有兴趣才会在探索过程中感受到有所收获，在其他技术方向上也是这样。如果大家对二进制文件解析感兴趣，58 同城近期会有一次线上技术沙龙，主要介绍58如何打造集团内 Swift 混编生态的。我会借助沙龙的机会介绍下 Swift 的二进制解析。

zhangferry：作为一位资深开发，能讲下你认为的高级开发和资深开发之间的区别吗？在你看来要达到资深开发需要具备哪些素质？

> 可能各家公司对高级和资深的定义不太一致。我理解资深开发相对于高级开发更具备触类旁通的能力，或者说是能根据以往的经验提取方法论应用到其他领域。因此从高级到资深可能需要在多个方向上有较好的理解。资深开发更应该从公司和产品的角度考虑问题，多问几个为什么，多关注事后的结果，而不是产品安排什么就做什么。另外，在沟通能力上的对资深开发的要求也会更高一些。

zhangferry：你具有多年面试官的经历，能简单总结下你认为的什么才是好的候选人以及他们需要具备哪些素质吗？

> 由于团队职责可能不同，因此每个团队招人的标准存在一些差异。比如有些团队可能对 RN/Flutter 等技术的应用比较看重，有些团队对底层技术比较看重，但是这些差异都是表象的差异。优秀的团队更注重候选人更深层的东西，这些东西可能在短期内无法突击弥补的，比如对技术探索的欲望、思维的灵活性、学习能力、抗压能力、责任心等等。就我所在的团队而言，在技术上，我们更关心的是候选人是否已经找到技术成长的第二曲线。（第二曲线摘自于《第二曲线：跨越“S 型曲线”的二次增长》，书我没看过，图与我脑海中的模型很像，所以在此引用）
> 
>![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210828093945.png)
>
> 或者通过面试能让我们看到即使候选人目前还处于成长期，但是经过培养是可以有更长远成长的。很多团队招人不外乎就这两种：要么候选人现在很厉害，要么候选人将来很厉害。
>
> 一些场景比较复杂的大型APP，有些问题比较复杂，不是特别好定位，这需要一定的技术基础，灵活的思维，甚至要求心理素质过硬。大家可以看下我的[2019年终总结](https://www.jianshu.com/p/0a4831219cba "皮拉夫大王 2019年终总结")中提到的**<工作篇>**，我整理了日常工作中遇到的部分问题记录到总结中，这也是 58 T5级别工程师的日常工作内容和要求。
>
> 如果作为团队的老板，你肯定希望自己的属下能够具备打硬仗的实力，而不仅仅是写写需求做做任务，在关键的时刻能够攻坚克难才是团队价值的体现。以上几点要求如果只是看看面经，刷刷算法可能还不够。因此在日常工作中，我们就应该养成良好的习惯，多问几个为什么，多做探索调研和储备，不要放过一些细节。
>
> 回到正题，我们从简历和面试的实际情况来看下有哪些是被鼓励的：
>
>（1）项目经历（这里不是指写了哪些APP）比较匹配。比如团队目前的重点在与包大小治理，如果你的简历中有相关实践并且做的比较深入，那这就是加分项。
>
>（2）令人耳目一新的技术。有些技术比较前沿或者并未广泛被大家所熟知，在这个领域候选人有较深入的研究。（这表明候选人已经找到了第二曲线）
>
>（3）能证明自己探索和专研能力的经历。简历中有具体的事件能体现出候选人的这方面优势。（具备找到第二曲线的潜力）
>
>（4）灵活的思维能力。算法或者临场方案设计比较完善，考虑的比较完备。
>
>（5）良好的抗压能力。如果在高压的面试情况下，不烦躁不放弃，依旧能保持冷静思考。
>
>（6）能体现出良好的学习习惯。高质量的博客文章、开源代码等都是加分项。临时凑数的可能起不到作用，我一般会留意内容质量和发布时间密度。
>
>（7）业界视野。能关注业界的一些动态，对业界的一些热点技术比较熟悉。
>
>（8）坦诚而良好的沟通。
>
>（9）有足够的入职意愿。
>
>（10）最后就是稳定性、工作背景、学历等条件。

zhangferry：如何保持学习热情，给我们分享一些你的学习方法吧。

> 学习主要还是需要制定大的方向，然后在具体实施时会对自己做一些鼓励。这些鼓励的行为包括：写文章、在团队内做技术分享、对外交流等等。在团队内我的文章数和分享数常年领先，因为写文章和分享会促使我重新审视和思考，对成长有极大的好处。对外交流获得的成就感会更大一些，但是需要更谨慎，尽量保证自己输出的内容是准确的，一旦内容有明显纰漏，丢自己脸事小。。。

zhangferry：个人有什么想法，可以借助于摸鱼周报进行宣传的。

> （1）希望大家多多关注WBBlades开源项目： https://github.com/wuba/WBBlades ，觉得OK的话给我个 star 鼓励一下。
>
> （2）58主APP、人人车、到家精选等团队正在招人，简历可以投递到zhulideng@yeah.net。秋天到了，我想赚点内推费填几件衣服。

## 开发Tips

### 如何清除 iOS APP 的启动屏幕缓存

整理编辑：[FBY展菲](https://github.com/fanbaoying)

每当我在我的 `iOS` 应用程序中修改了 `LaunchScreen.storyboad` 中的某些内容时，我都会遇到一个问题：

**系统会缓存启动图像，即使删除了该应用程序，它实际上也很难清除原来的缓存。**

有时我修改了 `LaunchScreen.storyboad`，删除应用程序并重新启动，它显示了新的 `LaunchScreen.storyboad`，但 `LaunchScreen.storyboad` 中引用的任何图片都不会显示，从而使启动屏显得不正常。

今天，我在应用程序的沙盒中进行了一些挖掘，发现该 `Library` 文件夹中有一个名为 `SplashBoard` 的文件夹，该文件夹是启动屏缓存的存储位置。

因此，要完全清除应用程序的启动屏幕缓存，您所需要做的就是在应用程序内部运行以下代码（已将该代码扩展到 `UIApplication` 的中）：

```swift
import UIKit

public extension  UIApplication {

    func clearLaunchScreenCache() {
        do {
            try FileManager.default.removeItem(atPath: NSHomeDirectory()+"/Library/SplashBoard")
        } catch {
            print("Failed to delete launch screen cache: \(error)")
        }
    }

}
```

在启动屏开发过程中，您可以将其放在应用程序初始化代码中，然后在不修改启动屏时将其禁用。

这个技巧在启动屏出问题时为我节省了很多时间，希望也能为您节省一些时间。

**使用介绍**

```swift
UIApplication.shared.clearLaunchScreenCache()
```

* 文章提到的缓存目录在沙盒下如下图所示：

![](https://user-images.githubusercontent.com/24238160/131212546-3ac9cf3c-cad5-48c5-913a-3e1408595e44.png)

* OC 代码,创建一个 `UIApplication` 的 `Category`

```objectivec
#import <UIKit/UIKit.h>

@interface UIApplication (LaunchScreen)
- (void)clearLaunchScreenCache;
@end
#import "UIApplication+LaunchScreen.h"

@implementation UIApplication (LaunchScreen)
- (void)clearLaunchScreenCache {
    NSError *error;
    [NSFileManager.defaultManager removeItemAtPath:[NSString stringWithFormat:@"%@/Library/SplashBoard",NSHomeDirectory()] error:&error];
    if (error) {
        NSLog(@"Failed to delete launch screen cache: %@",error);
    }
}
@end
```

OC使用方法

```objectivec
#import "UIApplication+LaunchScreen.h"

[UIApplication.sharedApplication clearLaunchScreenCache];
```

参考：[如何清除 iOS APP 的启动屏幕缓存](https://mp.weixin.qq.com/s/1esgRgu1iqFwB1Wv8-GlEQ)

### 优化 SwiftLint 执行

整理编辑：[zhangferry](https://zhangferry.com)

很多 Swift 项目里都集成了 SwiftLint 用于代码检查。SwiftLint 的执行通常在编译的早期且全量检查的，目前我们项目的每次 lint 时间在 12s 左右。但细想一下，并没有改变的代码多次被 lint 是一种浪费。顺着这个思路在官方的 [issues](https://github.com/realm/SwiftLint/issues/413 "SwiftLint issue 413") 里找到了可以过滤非修改文件的参考方法，其是通过 `git diff` 查找到变更的代码，仅对变更代码进行 lint 处理。使用该方案后，每次 lint 时长基本保持在 2s 以内。下面附上该脚本，需要注意的是 `SWIFT_LINT` 要根据自己的集成方式进行替换，这里是 CocoaPod 的集成方式：

```bash
# Run SwiftLint
START_DATE=$(date +"%s")

SWIFT_LINT="${PODS_ROOT}/SwiftLint/swiftlint"

# Run SwiftLint for given filename
run_swiftlint() {
    local filename="${1}"
    if [[ "${filename##*.}" == "swift" ]]; then
        # ${SWIFT_LINT} autocorrect --path "${filename}"
        ${SWIFT_LINT} lint --path "${filename}"
    fi
}

if [[ -e "${SWIFT_LINT}" ]]; then
    echo "SwiftLint version: $(${SWIFT_LINT} version)"
    # Run for both staged and unstaged files
    git diff --name-only | while read filename; do run_swiftlint "${filename}"; done
    git diff --cached --name-only | while read filename; do run_swiftlint "${filename}"; done
else
    echo "${SWIFT_LINT} is not installed."
    exit 0
fi

END_DATE=$(date +"%s")

DIFF=$(($END_DATE - $START_DATE))
echo "SwiftLint took $(($DIFF / 60)) minutes and $(($DIFF % 60)) seconds to complete."
```


## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[FBY展菲](https://github.com/fanbaoying)

本期主题：`Swift 泛型`

1、[Swift 进阶： 泛型](https://mp.weixin.qq.com/s/WOPbESx7YIAUes_1y3wyMw) -- 来自公众号：Swift社区

泛型是 Swift 最强大的特性之一，很多 Swift 标准库是基于泛型代码构建的。你可以创建一个容纳  Int 值的数组，或者容纳 String 值的数组，甚至容纳任何 Swift 可以创建的其他类型的数组。同样，你可以创建一个存储任何指定类型值的字典，而且类型没有限制。

2、[Swift 泛型解析](https://juejin.cn/post/7000916678150193159/ "Swift 泛型解析") -- 来自掘金：我是熊大

本文通俗易懂的解析了什么是泛型，泛型的应用场景，泛型和其他Swift特性摩擦出的火花，最后对泛型进行了总结。

3、[WWDC2018 - Swift 泛型 Swift Generics](https://juejin.cn/post/6844903623185399822/ "WWDC2018 - Swift 泛型 Swift Generics") -- 来自掘金：西野圭吾

本文回顾了 Swift 中对于泛型支持的历史变更，可以了解下泛型不同版本的历史以及特性。

4、[Swift 性能优化(2)——协议与泛型的实现](http://chuquan.me/2020/02/19/swift-performance-protocol-type-generic-type/ "Swift 性能优化(2)——协议与泛型的实现") -- 来自博客：楚权的世界

本文探讨了协议和泛型的底层实现原理，文中涉及到编译器对于 Swift 的性能优化，十分推荐阅读。

5、[Swift 泛型底层实现原理](http://chuquan.me/2020/04/20/implementing-swift-generic/ "Swift 泛型底层实现原理") -- 来自博客：楚权的世界

本文介绍了swift相关的底层原理，干货较多。例如VWT的作用、什么是Type Metadata、Metadata Pattern等等。如果有些概念不是很清楚的话可以阅读文章下面的参考文献。

6、[Generics Manifesto](https://github.com/apple/swift/blob/main/docs/GenericsManifesto.md "Generics Manifesto") -- 来自 Github：Apple/Swift

[@zhangferry](https://zhangferry.com)：[四娘](https://kemchenj.github.io/)对这篇官方说明进行了翻译，也可以直接阅读翻译版：[【译】Swift 泛型宣言](https://kemchenj.github.io/2017-11-26/?highlight=%E6%B3%9B%E5%9E%8B "[译]Swift 泛型宣言")。这份文档介绍了如何建立一个完善的泛型系统，以及 Swift 语言在发展过程中，不断补充的那些泛型功能。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Adobe Color Wheel

地址：https://color.adobe.com/zh/create/color-wheel

来自 Adobe 的调色盘网站，可以选择不同的色彩规则，例如：类比、分割辅色、三元色等等方案来生成配色，也可以通过导入照片来提取颜色，并且可以通过辅助工具例如对比度检查器来，确认文字和图案在底色上的预览情况。另外，你也可以通过 Adobe 的「探索」和「趋势」社区来学习如何搭配颜色，或者是寻找配色灵感。

### Awesome-tips

地址：https://awesome-tips.gitbook.io/ios/

来自知识小集整理的 iOS 开发 tip，已经整合成了 gitbook。虽然时间稍稍有点久了，但其中的文章都比较优质，在遇到的问题的时候可以翻阅一下，讲不定会有新的收获。

## 工具推荐

整理编辑：[CoderStar](http://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18#wechat_redirect)

# OhMyStar

**地址**：https://ohmystarapp.com/

**软件状态**：普通版免费，Pro版收费

**软件介绍**：

直接引用官方自己介绍的话吧：
> The best way to organise your GitHub Stars. Beautiful and efficient way to manage, explore and share your Github Stars.

其中Pro版增加的功能是设备间同步，不过软件本身也支持数据的导入导出，大家根据自己的情况进行选择。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210828101929.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第二十四期](https://mp.weixin.qq.com/s/vXyD_q5p2WGdoM_YmT-iQg)

[iOS摸鱼周报 第二十三期](https://mp.weixin.qq.com/s/1Vs50Lbo0Z27dnU-ARQ96A)

[iOS摸鱼周报 第二十二期](https://mp.weixin.qq.com/s/JI5mlzX9cYhXJS81k1WE6A)

[iOS摸鱼周报 第二十一期](https://mp.weixin.qq.com/s/Hcd8CtkyqD8IXM0SbVJo-A)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
