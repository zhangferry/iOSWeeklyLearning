# iOS 摸鱼周报 #68 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：OC泛型中的  `__covariant`  与 `__contravariant`
> * 内容推荐：编译和热重载优秀文章推荐
> * 摸一下鱼：关于 iOS 开发国际化相关工具推荐

## 本期话题



## 本周学习

整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)

#### OC泛型中的  `__covariant`  与 `__contravariant`

 `__covariant` 与 `__contravariant` 分别是OC泛型当中的关键字

* `__covariant` 代表协变，子类转成父类，子类型可以和父类型一样使用。
* `__contravariant`  代表逆变，父类转成子类，父类型可以和子类型一样使用。

我们来看一下 `__covariant` 的作用：

```C++
@interface Car : NSObject 
@property (nonatomic, copy) NSString *name;
@end
  
@interface BMW : Car 
@end
  
@interface Person<__covariant T> : NSObject
@property (nonatomic, strong) T car;
@end  
...
Person<BMW *> * personBMW = [[Person alloc]init];;
BMW * bmw = [[BMW alloc]init];
personBMW.car = bmw;
personBMW.car.name = @"BMW";
      
Person<Car *> * pCar = [[Person alloc]init];  
pCar = personBMW;  
NSLog(@"%@",pCar.car.name); // BMW
```
我们可以看到上述实例当中，子类型 `BMW` 成功转换成了父类型 `Car`

我们再来看看 `__contravariant` 的作用：

```C++
  // 不使用__contravariant 的情况下
  Person<Car *> * PCar = [[Person alloc]init];
  Person<BMW *> * PBMW = [[Person alloc]init];
  BMW * bmw = [[BMW alloc]init];
  PBMW.car = bmw;
  PBMW.car.name = @"BMW";
  PBMW = PCar;  // ⚠️ 出现警告 Incompatible pointer types assigning to 'Person<BMW *> *' from 'Person<Car *> *'
```

```c++
@interface Person<__contravariant T> : NSObject
@property (nonatomic, strong) T car;
@end
...
Person<Car *> * PCar = [[Person alloc]init];
Person<BMW *> * PBMW = [[Person alloc]init];
BMW * bmw = [[BMW alloc]init];
PBMW.car = bmw;
PBMW.car.name = @"BMW";
PBMW = PCar; // 这时候再去赋值，不会出现警告
```

## 内容推荐

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1. [基于 LLVM 自制编译器——序](http://chuquan.me/2022/07/17/compiler-for-kaleidoscope-00/ "基于 LLVM 自制编译器——序")  -- 来自：楚权的世界

   [@夏天](https://juejin.cn/user/3298190611456638)：文章是基于官方教程 [《My First Language Frontend with LLVM Tutorial》](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/index.html "《My First Language Frontend with LLVM Tutorial》") 的翻译，有助于加深对编译原理的理解。

   这位大佬的其他内容也值得推荐。

2. [How to improve iOS build times with modularization](https://www.runway.team/blog/how-to-improve-ios-build-times-with-modularization "How to improve iOS build times with modularization") -- 来自：Bruno Rocha

   [@夏天](https://juejin.cn/user/3298190611456638)：文章分析了影响 iOS 构建的因素，以及当我们使用模块化后如何使用 **API/Impl** 技术更快地编译相互依赖的模块。

3. [ARC and Memory Management in Swift](https://www.raywenderlich.com/966538-arc-and-memory-management-in-swift "ARC and Memory Management in Swift") -- 来自：RayWenderlich

   [@夏天](https://juejin.cn/user/3298190611456638)：RayWenderlich 教程系列的文章质量都比较高，本文介绍了 ARC 的工作原理以及内存管理的最佳实践，顺便介绍了如何发现内存泄露，很完整的一个教程。

4. [Hot Reloading in Swift](https://www.merowing.info/hot-reloading-in-swift/ "Hot Reloading in Swift") —— Krzysztof Zabłocki

   [@夏天](https://juejin.cn/user/3298190611456638)：如同 Injection  一样的帮助热重载的工具[DyCI](https://github.com/DyCI/dyci-main "DyCI")，文章并没有涉足原理，但是讲述了一些设计历程。

5. [App 如何通过注入动态库的方式实现极速编译调试？](https://time.geekbang.org/column/article/87188 "App 如何通过注入动态库的方式实现极速编译调试？")—— 戴铭《iOS 开发高手课》

   [@夏天](https://juejin.cn/user/3298190611456638)：使用动态库加载方式进行极速调试，简单分析了 Flutter 和 Injection 的原理。

## 摸一下鱼

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

介绍几个关于iOS开发国际化的工具；

- genstrings：Xcode内置工具，从指定的 C 或者 Objective-C 源文件生成 `.strings` 文件；
- ibtool：Xcode内置工具，正如 `genstrings` 作用于源代码，而 `ibtool` 作用于 `XIB` 文件；
- bartycrouch：bartycrouch 可以依据 interfaces 文件( xib 文件) 和代码(swift 、m、h 文件)来增量更新 strings 文件。在这里 增量 是指 bartycrouch 会默认保留已经翻译的值及改变了的注释；
- Poedit：Poedit 是一款基于多语言的本地化工具，支持 Win/Mac/Linux 三大主流平台，经常被用于本地化各种计算机软件；


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #67 | Xcode Cloud 已支持订阅](https://mp.weixin.qq.com/s/8H7YnrVTubKvVnYJBXcF_A)

[iOS 摸鱼周报 #66 | Shazam 迎来问世 20 周年](https://mp.weixin.qq.com/s/LP1qNAgjzEiDwrR7I32kuA)

[iOS 摸鱼周报 #65 | 什么是精准测试](https://mp.weixin.qq.com/s/lvMHf5qQHpnDGLz1KY-2dg)

[iOS 摸鱼周报 #64 | 与 App Store 专家会面交流](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
