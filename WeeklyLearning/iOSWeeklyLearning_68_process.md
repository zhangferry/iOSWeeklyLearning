# iOS 摸鱼周报 #64 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

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

```C++
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

[iOS 摸鱼周报 #63 | Apple 企业家培训营已开放申请](https://mp.weixin.qq.com/s/nAMshUG4AjWLAAHOFPVqXg)

[iOS 摸鱼周报 #62 |  Live Activity 上线 Beta 版 ](https://mp.weixin.qq.com/s/HySX4Yaf3Zxy8Wn-LyUO0A)

[iOS 摸鱼周报 #61 |  Developer 设计开发加速器](https://mp.weixin.qq.com/s/WfwqRhC-9-isUanv8ZnvMQ)

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
