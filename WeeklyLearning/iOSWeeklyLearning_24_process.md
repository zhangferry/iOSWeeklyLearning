# iOS摸鱼周报 第二十四期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：跟一位同学聊一下蚂蚁的面试经历。
> * Tips：设计 OC 版本的 defer 功能。
> * 面试模块：离屏渲染。
> * 优秀博客：整理了Swift 闭包相关的文章。
> * 学习资料：
> * 开发工具：一款免费开源的跨平台密码管理工具：KeeWeb。

## 本期话题

[@zhangferry](https://zhangferry.com)：本期访谈对象是 [@拉布拉卡]()，他最近换工作刚入职了蚂蚁金服，今天跟他聊一下最近市场的面试状况和一些面试经历。（部分内容待晚上补充，先略过）

1、简单介绍下自己吧

> 

2、面试准备了多久？重点准备了哪些东西？

> 重点准备有3周左右，但之前也有陆陆续续在看一些东西。重点内容：

3、对目前市面上的公司面试的感受有哪些？有没有什么难忘的经历？

> 虽然我们总是调侃 iOS 没人要了，但市面上对 iOS 需要还是挺多的。相对来说，它不只要求你的基础要牢固，还有就是项目经验，重难点，框架设计能力，封装能力，这些都会考察。

4、准备面试有哪些好的建议

> 对 iOS 整个基础知识要有一个全面的理解，因为很多知识并非单点，很多内容是互通的，所以理解记忆的时候可以发散一下，尝试把一些内容串起来。另外就是项目这块，项目有哪些难点，这个要提前准备，面熟的时候思路要清晰。

5、能说下蚂蚁大致的面试思路和考察重点吗？

> 

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


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[FBY展菲](https://github.com/fanbaoying)

本期主题：`Swift 闭包`

1、[Swift 基于闭包的类型擦除](https://mp.weixin.qq.com/s/K1VfyOX96C4Hw2GxpcKnuw) -- 来自公众号：Swift社区

本文重点介绍在 Swift 中处理泛型时可能发生的一种情况，以及通常是如何使用基于**闭包的类型擦除技术**来解决这种情况。

2、[swift 闭包(闭包表达式、尾随闭包、逃逸闭包、自动闭包)](https://juejin.cn/post/6972560642427486238 "swift 闭包(闭包表达式、尾随闭包、逃逸闭包、自动闭包)") -- 来自掘金：NewBoy

关于 Swift 闭包的初级文章，内容整合了几乎所有 Swift 闭包的概念和用法。比较适合 Swift 初学者或者是从 OC 转向 Swift 的同学。

3、[Day6 - Swift 闭包详解 上](https://mp.weixin.qq.com/s/bE-Bt0VQ8aT3TtZz9EwfYg) -- 来自微信公众号： iOS成长指北

4、[Day7 - Swift 闭包详解 下](https://mp.weixin.qq.com/s/op8Kf3hOgmPHTXPiGioI0g) -- 来自微信公众号： iOS成长指北


Swift 闭包学习的两篇文章，也是包含了 Swift 的概念及用法，其中部分用法及概念更加细致。两篇文章是作者学习思考再输出的成果，因此在文章中有些作者的理解，这对我们学习是比较重要的，而且比较通俗易懂。

5、[Closures](https://docs.swift.org/swift-book/LanguageGuide/Closures.html) -- 来自：Swift Document

[@zhangferry](zhangferry.com)：对于概念的理解官方文档还是非常有必要看的。闭包跟 C/OC 中的 Block，其他语言中的 Lambda 含义是类似的。Swift 与 OC 混编时，闭包与 Block 是完全兼容的。但就含义来说两者仍有区别，Block 更多强调的是匿名代码块，闭包则是除这之外还有真正的一级对象的含义。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



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

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
