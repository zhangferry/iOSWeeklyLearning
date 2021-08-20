# iOS摸鱼周报 第二十四期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> 

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)
### `Objective-C defer` VS `Swift defer`


###### 背景
- - -


如果`Swift`写久了，突然转到`Objective-C`是不是有种不知所措的感觉？是不是有以下几点？
* **泛型** `OC`这个泛型写着很鸡肋，但是也不是毫无是处，至少有编码类型提示

* **协议**
`Objective-C`协议与`Swift`协议，一个比较明显的区别语法区别就是 `extension`
习惯了`extension`之后， 写`Objective-C`的时候就不知道咋办了，难道要我写继承？不存在的
经过摸索一番之后，偶然发现有`GitHub`大佬在11年后， 用`Objective-C`的`Runtime`实现了`extension`，后续有机会在讲

* **枚举** em......算了，当我没说，不是一个东西，也不在一个维度

所以就有了后面的事情了，尽可能在`Objective-C`里面实现`Swift`的语法糖
`Swift defer` 这个语法糖多好用不用多说，直接来`Objective-C`实现

######准备工作
- - -

* <font color=#FF0000 size=4>`__attribute__` </font>：是一个用于在声明时指定一些特性的编译器指令，它可以让我们进行更多的错误检查和高级优化工作

    ```swift
    struct __attribute__ ((__packed__)) sc3 {
        char a;
        char *b;
    };
    ...// 使用方式
    __attribute__ ((attribute-list))
    ```
    想了解更多，参考： https://nshipster.cn/__attribute__/
    
* <font color=#FF0000 size=4>`cleanup(...)`</font>：接受一个函数指针，在作用域结束的时候触发该函数指针

###### 简单实践
- - -


到这一步，我们已经了解了大概功能了，那我们实战一下

```cpp
# include <stdlib.h>
# include <stdio.h>

void free_buffer(char **buffer) { printf("3. free buffer\n"); }
void delete_file(int *value) { printf("2. delete file\n"); }
void close_file(FILE **fp) { printf("1. close file \n"); }

int main(int argc, char **argv) {
  //  执行顺序与压栈顺序相反
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
但是到这一步的话，我们使用不方便啊，何况我们还是iOSer，这个不友好啊
那么继续改造成`Objective-C`独有版本

###### 实战优化
- - -

```objectivec
- (void)hello:(NSString *)str {
	defer {
    	// do something
	}
}
```
要做到这个形式，那需要什么呢？
* 代码块，那就只能是 `NSBlock`
```objectivec
typedef void(^executeCleanupBlock)(void);
```
* 宏函数 or 全局函数？想到`Objective-C`又没有尾随闭包这一说，那全局函数肯定不行，也就只能全局宏了
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
不好意思， 不行，报错 <font color=#FF0000 size=4>`error: Redefinition of 'blk'`</font>，为什么？（想一想）
上最终解决版本之前还得认识两个东西
* <font color=#FF0000 size=4>`__LINE__` </font>：获取当前行号
* <font color=#FF0000 size=4> `##` </font>：连接两个字符
```objectivec
#define defer_concat_(A, B) A ## B
#define defer_concat(A, B) defer_concat_(A, B)
...
//为什么要多一个下划线的宏， 这是因为每次只能展开一个宏， `__LINE__` 的正确行号在第二层才能被解开
```

###### 最终方案
- - - -


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
总共就这么多代码，满足你要的`defer`

其实到了这里已经结束了， 但是还要讲一句：
这里的实现与原作者`Justin Spahr-Summers` https://github.com/jspahrsummers/libextobjc/blob/master/extobjc/EXTScope.h
略有差异，原作更丰富，这边只是拆分一步步分析得到结果， 原版有 `autoreleasepool` and `try {} @catch (...) {}`

## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)、[FBY展菲](https://github.com/fanbaoying)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

**为什么圆角和裁剪后 iOS 绘制会触发离屏渲染？**

默认情况下每个视图都是完全独立绘制渲染的。
而当某个父视图设置了圆角和裁剪并且又有子视图时，父视图只会对自身进行裁剪绘制和渲染。

当子视图绘制时就要考虑被父视图裁剪部分的绘制渲染处理，因此需要反复递归回溯和拷贝父视图的渲染上下文和裁剪信息，再和子视图做合并处理，以便完成最终的裁剪效果。这样势必产生大量的时间和内存的开销。

解决的方法是当父视图被裁剪和有圆角并且有子视图时，就单独的开辟一块绘制上下文，把自身和所有子视图的内容都统一绘制在这个上下文中，这样子视图也不需要再单独绘制了，所有裁剪都会统一处理。当父视图绘制完成时再将开辟的缓冲上下文拷贝到屏幕上下文中去。这个过程就是离屏渲染！！

所以离屏渲染其实和我们先将内容绘制在位图内存上下文然后再统一拷贝到屏幕上下文中的双缓存技术是非常相似的。使用离屏渲染主要因为iOS内部的视图独立绘制技术所导致的一些缺陷而不得不才用的技术。


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[FBY展菲](https://github.com/fanbaoying)

1、[Swift 基于闭包的类型擦除](https://mp.weixin.qq.com/s/K1VfyOX96C4Hw2GxpcKnuw) -- 来自公众号：Swift社区

本文重点介绍在 Swift 中处理泛型时可能发生的一种情况，以及通常是如何使用基于**闭包的类型擦除技术**来解决这种情况。



## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
