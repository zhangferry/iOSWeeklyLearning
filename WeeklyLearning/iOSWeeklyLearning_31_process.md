# iOS摸鱼周报 第三十一期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：
> * Tips：
> * 面试模块：一道 RunLoop 相关题目。
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)



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

SIL：Swift Intermediate Language，SIL是高级别的中间语言，SIL由**SILGen**生成并由**IRGen**转为LLVM IR ，SIL会对Swift进行较高级别的语义分析和优化。我们看到的@开头修饰的代码基本都属于SIL范畴。

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

1、[Swift的高级中间语言：SIL](https://www.jianshu.com/p/c2880460c6cd "Swift的高级中间语言：SIL") -- 来自简书：sea_biscute

[@东坡肘子](https://www.fatbobman.com)：在LLVM的官方文档中对Swift的编译器设计描述如下： Swift编程语言是在LLVM上构建，并且使用LLVM IR和LLVM的后端去生成代码。但是Swift编译器还包含新的高级别的中间语言，称为SIL。SIL会对Swift进行较高级别的语义分析和优化。 本文将分析一下SIL设计的动机和SIL的应用，包括高级别的语义分析，诊断转换，去虚拟化，特化，引用计数优化，TBAA(Type Based Alias Analysis)等。并且会在某些流程中加入对SIL和LLVM IR对比。

2、[一文看破Swift枚举本质](https://mp.weixin.qq.com/s/Gx7L_Ev0DV19mLYMnH-R1Q "一文看破Swift枚举本质") -- 来自：狐友技术团队

[@东坡肘子](https://www.fatbobman.com)：SIL在实际工作中的应用举例。通过分析内存布局、查看SIL源码等方式来探索一下枚举的底层到底是什么样子的。在Swift中枚举不仅仅只是一个用来区分类型的常量了，枚举的功能被大大的加强。枚举可以设置原始值，添加关联值，甚至可以添加计算属性(不能添加存储属性)，定义方法，实现协议，其功能仅次于一个class对象了，那么Swift的枚举到底是怎样实现这些功能的呢？


3、[Swift Intermediate Language 初探](https://zhuanlan.zhihu.com/p/101898915 "Swift Intermediate Language 初探") -- 来自简书：sea_biscute

@[皮拉夫大王](https://www.jianshu.com/u/739b677928f7 "皮拉夫大王") 文章简单介绍了SIL以及SIL在LLVM架构中的位置。正文部分作者通过SIL分析来解释extension 中protocol 函数和对象中的protocol 函数调用选择的问题。

4、[Swift编译器中间码SIL](https://woshiccm.github.io/posts/Swift%E7%BC%96%E8%AF%91%E5%99%A8%E4%B8%AD%E9%97%B4%E7%A0%81SIL/ "Swift编译器中间码SIL") -- 来自博客：roy's blog

@[皮拉夫大王](https://www.jianshu.com/u/739b677928f7 "皮拉夫大王") 。作者首先介绍了SIL的设计初衷以及与LLVM IR的区别。文中还介绍了SSA（ static single-assignment）中“代”的概念以及SSA的益处。SIL是命名函数的集合，SIL源文件为Module，通过Module可以遍历Module中的函数。

5、[Swift Intermediate Language —— A high level IR to complement LLVM](https://llvm.org/devmtg/2015-10/slides/GroffLattner-SILHighLevelIR.pdf "Swift Intermediate Language —— A high level IR to complement LLVM") -- 来自：Joe Groff 和 Chris Lattner

[@我是熊大](https://github.com/Tliens)：在LLVM开发人员会议上 Groff 和 Chris Lattner通过简报的方式对 Swift Intermediate Language 进行了详细的介绍。内容包括：为什么要使用 SIL、SIL的设计逻辑、Swift对SIL的使用等内容。尽管简报为英文，但主要以代码和图表为主，对了解SIL的设计动机和设计原理有很大的帮助。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### fig

**地址**：https://fig.io/

**软件状态**：免费，[开源](https://github.com/Coder-Star/autocomplete)

**软件介绍**：

`fig` 是一个开源的终端自动补全工具，支持数百个CLI工具，如`git`、`docker`、`npm`等等，并且可以无缝添加到你现有的终端，如`iTerm`、`Hyper`、`VSCode` 和 `macOS 终端`，支持我们自己自定义一些补全规则。

![fig](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Snipaste_2021-10-27_21-04-03.png)
## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
