# iOS摸鱼周报 第二十四期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：跟一位同学聊一下最近的面试感受。
> * Tips：设计 OC 版本的 defer 功能，使用现有证书创建 Fastlane match 格式加密文件。
> * 面试模块：离屏渲染相关知识点。
> * 优秀博客：整理了Swift 闭包相关的文章。
> * 学习资料：
> * 开发工具：一款免费开源的跨平台密码管理工具：KeeWeb。

## 本期话题

[@zhangferry](https://zhangferry.com)：本期访谈对象是 @七里香蛋炒饭，他也是交流群里的小伙伴。了解到他最近刚换工作，从某小公司入职某一线大厂，就邀请他来聊一聊面试的一些感想。

zhangferry：你面试准备了多久，大概的面试经历是怎样的？

> 整个面试过程大概有一个半月时间，前期是断断续续在看一些东西，后面有 3 周左右时间是重点准备。接到面邀的比较多，有些不感兴趣的就没去，实际参与面试的有 10 家，也都是一二线互联网公司。这侧面也说明了 iOS 没人要仅仅是个调侃而已，目前对 iOS 开发的需求还是不少的。

zhangferry：结合这些面试经历，有哪些高频题？遇到的算法考察多吗？

> 高频题的话内存管理和多线程肯定算是了，基本上每家面试都会问的。
>
> 另一个就是项目经历，也是必问的。这个一般会结合简历来问，特别是项目重点和难点，所以大家准备简历的时候一定要保证对所写的内容是很清楚的。对于非常喜欢的公司还可以根据他们业务需求有针对性的优化下简历。
>
> 另外，架构设计能力，封装能力，有时也会考察，这个短时间无法快速提升，需要平常工作过程有意培养一下。
>
> 算法的考察整体来看不算多，大概有 30% 的概率吧。那些考算法的也都是考察比较简单的题目，也可能跟我面试的岗位有关，这个仅供参考，面试之前，算法方面多少还是要准备的。

zhangferry：现在经常有人说面试八股文，结合面试经历，你怎么看待八股文这个事？

> 首先存在即合理吧，八股文的现象体现的是面试官自身准备的不足。可能来源于早期，大家技术水平都一般，没有太多可问的东西，也没有特意研究过哪些方面，所以就网上扒一扒拿来问。目前的经历来看到还好，被问的问题还算多元，可能这种现象之后会随着面试官水平的提升越来越少。
>
> 同时这也算是一种双向选择，如果某次面试全是那种眼熟的问题，毫无新意，大概率可以说明这家公司对技术的重视和钻研程度不高，可以降低其优先级。

zhangferry：对待参加面试的小伙伴有没有什么建议？

> 投递简历没有回复或者面试感觉还可以最后却没过，出现这些现象是有多种原因，比如岗位正好招满了、岗位需求有变等等，不要首先否定自己。面试过程一定要放平心态，不要有心理压力。
>
> 最后祝所有准备找和正在找工作的小伙伴都能拿到满意的 Offer。

## 开发Tips

### 在 Objective-C 中实现 Swift 中的 defer 功能

整理编辑：[RunsCode](https://github.com/RunsCode)、[zhangferry](zhangferry.com)

期望效果是下面这样，函数执行完出栈之前，要执行 defer 内定义的内容。

```objectivec
- (void)hello:(NSString *)str {
	defer {
    	// do something
	}
}
```

##### 准备工作

实现`defer`的前提是需要有指令能够让函数在作用域出栈的时候触发`defer`里的闭包内容，这里需要用到两个东西：

`__attribute__` ：一个用于在声明时指定一些特性的编译器指令，它可以让我们进行更多的错误检查和高级优化工作。

想了解更多，参考： https://nshipster.cn/__attribute__/

`cleanup(...)`：接受一个函数指针，在作用域结束的时候触发该函数指针。

#### 简单实践

到这一步，我们已经了解了大概功能了，那我们实战一下：

```cpp
#include <stdlib.h>
#include <stdio.h>

void free_buffer(char **buffer) { printf("3. free buffer\n"); }
void delete_file(int *value) { printf("2. delete file\n"); }
void close_file(FILE **fp) { printf("1. close file \n"); }

int main(int argc, char **argv) {
  // 执行顺序与压栈顺序相反
  char *buffer __attribute__ ((__cleanup__(free_buffer))) = malloc(20);
  int res __attribute__ ((__cleanup__(delete_file)));
  FILE *fp __attribute__ ((__cleanup__(close_file)));
  printf("0. open file \n");
  return 0;
}
```
输出结果：

```cpp
0. open file 
1. close file 
2. delete file
3. free buffer
[Finished in 683ms]
```

但是到这一步的话，我们使用不方便啊，何况我们还是iOSer，这个不友好啊。那么继续改造成`Objective-C`独有版本。

#### 实战优化

要做到上面那个理想方案，还需要什么呢？

* 代码块，那就只能是 `NSBlock`
```objectivec
typedef void(^executeCleanupBlock)(void);
```
* 宏函数 or 全局函数？想到 `Objective-C` 又没有尾随闭包这一说，那全局函数肯定不行，也就只能全局宏了
```objectivec
#ifndef defer
#define defer \
__strong executeCleanupBlock blk __attribute__((cleanup(deferFunction), unused)) = ^
#endif
...
// .m 文件
void deferFunction (__strong executeCleanupBlock *block) {
    (*block)();
}
```

OK 大功告成跑一下
```objectivec
defer {
    NSLog(@"defer 1");
};
defer { // error: Redefinition of 'blk'
    NSLog(@"defer 2");
};
defer { // error: Redefinition of 'blk'
    NSLog(@"defer 3");
};
NSLog(@"beign defer");
```
不好意思， 不行，报错 `error: Redefinition of 'blk'`，为什么？（想一想）

上最终解决版本之前还得认识两个东西

* `__LINE__` ：获取当前行号
* `##` ：连接两个字符
```objectivec
#define defer_concat_(A, B) A ## B
#define defer_concat(A, B) defer_concat_(A, B)
...
//为什么要多一个下划线的宏， 这是因为每次只能展开一个宏， __LINE__ 的正确行号在第二层才能被解开
```

#### 最终方案


好了，差不多了， 是时候展示真功夫了

```objectivec
#define defer_concat_(A, B) A ## B
#define defer_concat(A, B) defer_concat_(A, B)

typedef void(^executeCleanupBlock)(void);

#if defined(__cplusplus)
extern "C" {
#endif
void deferFunction (__strong executeCleanupBlock _Nonnull *_Nonnull block);
#if defined(__cplusplus)
}
#endif

#ifndef defer
#define defer \
__strong executeCleanupBlock defer_concat(blk, __LINE__) __attribute__((cleanup(deferFunction), unused)) = ^
#endif
// .m 文件
void deferFunction (__strong executeCleanupBlock *block) {
    (*block)();
}
```

总共就这么多代码，实现 OC 版本的`defer`。

其实到了这里已经结束了， 但是还要讲一句：这里与 Justin Spahr-Summers 在 [libextobj](https://github.com/jspahrsummers/libextobjc/blob/master/extobjc/EXTScope.h "libextobj") （`@onExit{}`）里的实现略有差异，当前实现更简单，libextobj 里的功能更丰富一些。

### 使用现有证书创建 Fastlane match 格式加密文件

简单说下 match 管理证书的工作流程，它将证书文件进行加密存放到 git 仓库，使用方 clone 这个仓库然后解密证书文件，再把证书安装到本机的 keychain 里。这样不同设备上就可以愉快的共享证书了。

match 创建证书有两种方式：

*  `fastlane match nuke`，对原证书 revoke 重新生成一份新的，这会导致原证书不可用，如果多APP账号，不建议这样。
* 通过已有证书导出为 `match` 格式加密文件，进行维护。

第二种方案不会影响原证书使用，比较推荐。但是看网上介绍这种方案的非常少，所以还是简单总结下：

1、导出文件

需要导出证书、p12两个文件，将他们放到一个特定文件夹，假定他们的命名分别为：cert.cer、cert.p12。

2、使用 openssl 进行加密

需要一个预设密码，这个可以自定义，作为加密和解密的一个特定参数。

```bash
$ openssl enc -aes-256-cbc -k {password} -in "cert.cer" -out "cert.enc.cer" -a -e -salt
$ openssl enc -aes-256-cbc -k {password} -in "cert.p12" -out "cert.enc.p12" -a -e -salt
```

3、推送证书到 git 仓库

每个证书文件都有特定的 ID，推送之前我们还需要修改加密证书的文件名。该 ID 在开发者网站证书详情那一页的网址最后面展示。就是下面码糊住的那一块：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210822095006.png)

然后我们将那两个文件放到 git 仓库的 certs 目录对应的类型（development/distribution）下，然后进行推送。

4、使用

还记得我们上面设计的加密参数吗，在使用的时候也是需要用到的，我们将其放到 `.env` 这个文件中作为全局变量，它有一个特定的变量名`MATCH_PASSWROD`。使用的时候用下面的语句就可以下载安装证书了：

```bash
$ fastlane match development
$ fastlane match adhoc
```

参考：https://docs.fastlane.tools/actions/match/

## 面试解析

整理编辑：[FBY展菲](https://github.com/fanbaoying)

本期面试解析讲解的是离屏渲染的相关知识点。

### 为什么圆角和裁剪后 iOS 绘制会触发离屏渲染？

默认情况下每个视图都是完全独立绘制渲染的。
而当某个父视图设置了圆角和裁剪并且又有子视图时，父视图只会对自身进行裁剪绘制和渲染。

当子视图绘制时就要考虑被父视图裁剪部分的绘制渲染处理，因此需要反复递归回溯和拷贝父视图的渲染上下文和裁剪信息，再和子视图做合并处理，以便完成最终的裁剪效果。这样势必产生大量的时间和内存的开销。

解决的方法是当父视图被裁剪和有圆角并且有子视图时，就单独的开辟一块绘制上下文，把自身和所有子视图的内容都统一绘制在这个上下文中，这样子视图也不需要再单独绘制了，所有裁剪都会统一处理。当父视图绘制完成时再将开辟的缓冲上下文拷贝到屏幕上下文中去。这个过程就是离屏渲染！！

所以离屏渲染其实和我们先将内容绘制在位图内存上下文然后再统一拷贝到屏幕上下文中的双缓存技术是非常相似的。使用离屏渲染主要因为 iOS 内部的视图独立绘制技术所导致的一些缺陷而不得不才用的技术。

推荐阅读：[关于iOS离屏渲染的深入研究](https://zhuanlan.zhihu.com/p/72653360 "关于iOS离屏渲染的深入研究")


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[FBY展菲](https://github.com/fanbaoying)

本期主题：`Swift 闭包`

1、[Swift 基于闭包的类型擦除](https://mp.weixin.qq.com/s/K1VfyOX96C4Hw2GxpcKnuw) -- 来自公众号：Swift社区

本文重点介绍在 Swift 中处理泛型时可能发生的一种情况，以及通常是如何使用基于**闭包的类型擦除技术**来解决这种情况。

2、[swift 闭包(闭包表达式、尾随闭包、逃逸闭包、自动闭包)](https://juejin.cn/post/6972560642427486238 "swift 闭包(闭包表达式、尾随闭包、逃逸闭包、自动闭包)") -- 来自掘金：NewBoy

关于 Swift 闭包的初级文章，内容整合了几乎所有 Swift 闭包的概念和用法。比较适合 Swift 初学者或者是从 OC 转向 Swift 的同学。

3、[Day6 - Swift 闭包详解 上](https://mp.weixin.qq.com/s/bE-Bt0VQ8aT3TtZz9EwfYg) -- 来自微信公众号： iOS成长指北

4、[Day7 - Swift 闭包详解 下](https://mp.weixin.qq.com/s/op8Kf3hOgmPHTXPiGioI0g) -- 来自微信公众号： iOS成长指北


Swift 闭包学习的两篇文章，也是包含了 Swift 的概念及用法，其中部分用法及概念更加细致。两篇文章是作者学习思考再输出的成果，因此在文章中有些作者的理解，这对我们学习是比较重要的，而且比较通俗易懂。

5、[Closures](https://docs.swift.org/swift-book/LanguageGuide/Closures.html "Apple Document - Closures") -- 来自：Swift Document

[@zhangferry](zhangferry.com)：对于概念的理解官方文档还是非常有必要看的。Swift 里的闭包跟 C/OC 中的 Block，其他语言中的 Lambda 含义是类似的。Swift 与 OC 混编时，闭包与 Block 是完全兼容的。但就含义来说两者仍有区别，Block 更多强调的是匿名代码块，闭包则是除这之外还有真正的一级对象的含义。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 中国程序员容易发音错误的单词

地址：https://github.com/shimohq/chinese-programmer-wrong-pronunciation

在担心和同事讨论代码的时念的单词同事听不懂？开会 review 代码的时候突然遇到不会读的单词？如果你遇到过这些问题，那来看看这个 github 仓库吧。它是一个收录了在编程领域容易发音错误单词的仓库，目前已经有 14.4k stars 了，他标注出了易错的读音和正确的读音，且支持在线听读音。

### IoT for Beginners

地址：https://github.com/microsoft/IoT-For-Beginners

这是来自微软 Azure 的物联网课程，是一个为期 12 周的 24 课时的课程，其中有所有关于物联网的基础知识，每节课都包括课前和课后测验、完成课程的书面说明、解决方案、作业等。其中每个项目都是适合学生或业余爱好者的、在真实世界可用的硬件，且每个项目都会提供相关的背景知识来研究具体的项目领域。

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

# KeeWeb

**地址**：https://keeweb.info/

**软件状态**：免费，[开源](https://github.com/keeweb/keeweb)

**软件介绍**：

KeeWeb 是一个浏览器和桌面密码管理器，兼容 KeePass 数据库。它不需要任何服务器或额外的资源。该应用程序可以在浏览器中运行，也可以作为桌面应用程序运行。更重要的是它还可以利用 Dropbox、Google  Drive 进行远程同步。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210822081714.png)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第二十三期](https://mp.weixin.qq.com/s/1Vs50Lbo0Z27dnU-ARQ96A)

[iOS摸鱼周报 第二十二期](https://mp.weixin.qq.com/s/JI5mlzX9cYhXJS81k1WE6A)

[iOS摸鱼周报 第二十一期](https://mp.weixin.qq.com/s/Hcd8CtkyqD8IXM0SbVJo-A)

[iOS摸鱼周报 第二十期](https://mp.weixin.qq.com/s/PjiZzx3VSAfAGHRJs160aQ)



![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
