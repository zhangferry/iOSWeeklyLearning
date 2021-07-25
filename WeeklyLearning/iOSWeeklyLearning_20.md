# iOS摸鱼周报 第二十期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 为河南祈福，梳理了一些洪灾应对的指南，希望对大家有用。
> * Tips 部分介绍了如何绘制一个高颜值的统计图。
> * 面试解析模块本期讲的是深拷贝浅拷贝这个知识点。
> * 优秀博客汇总了不少包体积优化的优秀文章。
> * 学习资料推荐了 Better Explaine 这个网站，其用于帮助大家理解那些复杂的数学概念。
> * 截图工具 Snipaste，无用图片搜索工具 LSUnusedResources。

## 本期话题

[@zhangferry](https://zhangferry.com)：近期的河南洪灾一直牵动人心，较严重的有郑州、新乡、鹤壁等地，其他的一些非洪水直接侵犯的城市，所处形势也很严峻，比如承载泄洪重任的下游泄洪地带。泄洪是治理洪水的有效措施，但也有很大的风险，如果决堤，对两岸人民的生命和财产安全都会造成较大威胁，所以泄洪经常伴随着大量的人员撤离、财产损失。这次郑州泄洪的主要地方就有河南周口，为了承接上游颍河、贾鲁河的洪水，21 号周口市防汛等级升级为一级，截止 23 号 15 时，两大河流均未出现漫堤、决口现象。再下游是安徽的界首与阜阳，安徽省位置特殊，这里泄洪上保河南，下保江苏，绝对的舍小家为大家。我是河南周口的，我媳妇是安徽阜阳的，了解到各自家乡的贡献之后我们感到深深的自豪。

另一方面，一方有难八方支援，期间发生了太多感动人心的事情，为每一个参与到河南抗洪救灾的人员致以最高的敬意。截止目前洪灾还没有完全退去，还不能掉以轻心。以下是我从多处官方新闻报道中总结的一些防洪应对指南，希望对大家有所帮助。

### 洪灾前

* 根据当地电视台或广播指示，选取最佳撤离路线。
* 撤离时最好准备以下物品：
	* 食物：足够几天食用的速食食品、高热量食品。
	* 救生准备：救生衣、救生圈或者木盆、水盆等。
	* 通讯设备：保存好能使用的通讯设备，用于了解外界情况和发出求救信号。
	* 求救设备：手机可能会没电，有口哨的话也可以带一个。

### 洪灾期间

* 屋内积水加深，及时转移至高处，不要逗留。
* 尽量不要在有积水的道路行走，注意防汛标志，有旋涡的地方不要靠近。
* 尽量避开电线杆、变压器等有可能连线的地方。
* 如果水位快要超过自身，在没有救生衣的情况下，快速寻找木板，大块泡沫等能够漂浮的东西，防止溺水。

### 洪灾后

大灾之后防大疫，洪灾通常导致大量致病细菌、寄生虫、病毒等的大肆传播，再加上新冠疫情的影响，受灾区域人员一定要注意以下几点：

* 注意饮用水卫生，喝烧开的水或者瓶装水。洪灾通常会淹没自来水厂、厕所、垃圾堆从而污染清洁水源。
* 注意饮食卫生，饭前洗手，不吃污水浸泡过的食物。
* 尽量不要蹚水，如果无法避免，蹚水之后，用清水清洗干净，并检查有无刮伤，如果有伤口，使用碘酒或其他消毒用品对伤口消毒。
* 灾情过后的室内，先清理、后消毒、再回迁。
* 如果感觉身体不适，特别是发热、腹泻，应及时就医。
* 当前的新冠疫情仍未散去，还需要戴好口罩，避免人群聚集。

最后的最后，河南加油，安徽加油！

## 开发Tips

### 码一个高颜值统计图

整理编辑：[FBY展菲](https://github.com/fanbaoying)

项目开发中有一些需求仅仅通过列表展示是不能满足的，如果通过图表的形式来展示，就可以更快捷的获取到数据变化情况。大部分情况我们都是使用第三方图表工具，现在我们介绍一个手动绘制的简易统计图，目前支持三种类型：**折线统计图**、**柱状图**、**环形图**。

**效果展示**

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210724193757.png)

**折线统计图实现思路分析**

观察发现折线图包含这几部分：x轴、y轴及其刻度，背景辅助线，代表走势的折线及圆圈拐点，折线下部的整体渐变。

1、x轴、y轴使用 `UIBezierPath` 描绘路径，使用 `CAShapeLayer` 设置颜色及虚线样式，标签使用UILabel表示，需要注意每个标点的间距。

2、背景辅助线及走势线绘制同坐标轴，区别仅在于线段走势和样式稍微不同。

3、渐变方案整体渐变，然后让折线图下部作为 mask 遮罩即可实现。

柱状图和圆饼图设计思路相似，大家可以自行思考，完整代码可查看这里：[FBYDataDisplay-iOS](https://github.com/fanbaoying/FBYDataDisplay-iOS "FBYDataDisplay-iOS")。以下是折线走势的示例代码：

```objectivec
#pragma mark 画折线图
- (void)drawChartLine {
    UIBezierPath *pAxisPath = [[UIBezierPath alloc] init];
    
    for (int i = 0; i < self.valueArray.count; i ++) {
        
        CGFloat point_X = self.xScaleMarkLEN * i + self.startPoint.x;
        
        CGFloat value = [self.valueArray[i] floatValue];
        CGFloat percent = value / self.maxValue;
        CGFloat point_Y = self.yAxis_L * (1 - percent) + self.startPoint.y;
        
        CGPoint point = CGPointMake(point_X, point_Y);
        
        // 记录各点的坐标方便后边添加 渐变阴影 和 点击层视图 等
        [pointArray addObject:[NSValue valueWithCGPoint:point]];
        
        if (i == 0) {
            [pAxisPath moveToPoint:point];
        }
        else {
            [pAxisPath addLineToPoint:point];
        }
    }
    
    CAShapeLayer *pAxisLayer = [CAShapeLayer layer];
    pAxisLayer.lineWidth = 1;
    pAxisLayer.strokeColor = [UIColor colorWithRed:255/255.0 green:69/255.0 blue:0/255.0 alpha:1].CGColor;
    pAxisLayer.fillColor = [UIColor clearColor].CGColor;
    pAxisLayer.path = pAxisPath.CGPath;
    [self.layer addSublayer:pAxisLayer];
}
```

**遇到的问题**（已解决）

`reloadDatas` 方法无效，title 没变，数据源没变，移除 layer 的时候还会闪退

解决方案：在 `reloadData` 时，需要将之前缓存的数组数据 `pointArray` 清空，不然数组中保存了上次的数据。


参考：[码一个高颜值统计图 - 展菲](https://mp.weixin.qq.com/s/pzfzqdh7Tko9mfE_cKWqmg)

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析本期主题是**对深浅拷贝的理解**。文章将从深拷贝和浅拷贝的区别开始讲起，然后讲解在 iOS 中对 mutable 对象与 immutable 对象进行 copy 与 mutableCopy 的结果，以及如何对集合对象进行真正意义上的深拷贝，最后带你实现对自定义对象的深浅拷贝。

### 对深浅拷贝的理解

我们先要理解拷贝的目的是：产生一个副本对象，跟源对象互不影响。

#### 深拷贝和浅拷贝

拷贝类型|拷贝方式|特点
--|--|--
深拷贝|内存拷贝，让副本对象指针和源对象指针指向 `两片` 内容相同的内存空间。|1. 不会增加被拷贝对象的引用计数；<br>2. 产生了一个内存分配，出现了两块内存。
浅拷贝|指针拷贝，对内存地址的复制，让副本对象指针和源对象指针指向 `同一片` 内存空间。|1. 会增加被拷贝对象的引用计数；<br>2. 没有进行新的内存分配。<br>注意：如果是小对象如 NSString，可能通过 `Tagged Pointer` 来存储，没有引用计数。

简而言之：

* 深拷贝：内存拷贝，产生新对象，不增加被拷贝对象引用计数
* 浅拷贝：指针拷贝，不产生新对象，增加被拷贝对象引用计数
* 区别：1. 是否影响了引用计数；2. 是否开辟了新的内存空间

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210724043958.png)

#### 在 iOS 中对 mutable 对象与 immutable 对象进行 copy 与 mutableCopy 的结果

iOS 提供了 2 个拷贝方法：

* copy：不可变拷贝，产生不可变副本
* mutableCopy：可变拷贝，产生可变副本

对 mutable 对象与 immutable 对象进行 copy 与 mutableCopy 的结果：

源对象类型|拷贝方式|副本对象类型|拷贝类型（深/浅）
:--:|:--:|:--:|:--:
mutable 对象|copy|不可变|深拷贝
mutable 对象|mutableCopy|可变|深拷贝
immutable 对象|copy|不可变|`浅拷贝`
immutable 对象|mutableCopy|可变|深拷贝

>注：这里的 immutable 对象与 mutable 对象指的是系统类 NSArray、NSDictionary、NSSet、NSString、NSData 与它们的可变版本如 NSMutableArray 等。

一个记忆技巧就是：对 immutable 对象进行 copy 操作是 `浅拷贝`，其它情况都是 `深拷贝`。

我们还可以根据拷贝的目的加深理解：

* 对 immutable 对象进行 copy 操作，产生 immutable 对象，因为源对象和副本对象都不可变，所以进行指针拷贝即可，节省内存
* 对 immutable 对象进行 mutableCopy 操作，产生 mutable 对象，对象类型不同，所以需要深拷贝
* 对 mutable 对象进行 copy 操作，产生 immutable 对象，对象类型不同，所以需要深拷贝
* 对 mutable 对象进行 mutableCopy 操作，产生 mutable 对象，为达到修改源对象或副本对象互不影响的目的，需要深拷贝

#### 使用 copy、mutableCopy 对集合对象进行的深浅拷贝是针对集合对象本身的

使用 copy、mutableCopy 对集合对象（Array、Dictionary、Set）进行的深浅拷贝是针对集合对象本身的，对集合中的对象执行的默认都是浅拷贝。也就是说只拷贝集合对象本身，而不复制其中的数据。主要原因是，集合内的对象未必都能拷贝，而且调用者也未必想在拷贝集合时一并拷贝其中的每个对象。

如果想要深拷贝集合对象本身的同时，也对集合内容进行 copy 操作，可使用类似以下的方法，copyItems 传 YES。但需要注意的是集合中的对象必须都符合 NSCopying 协议，否则会导致 Crash。

```objectivec
NSArray *deepCopyArray = [[NSArray alloc]initWithArray:someArray copyItems:YES];
```

>注：`initWithArray:copyItems:` 方法不是所有情况下都深拷贝集合对象本身的。如果执行 `[[NSArray alloc]initWithArray:@[] copyItems:aBoolValue];`，也就是源对象为不可变的空数组的话，对源对象本身执行的是浅拷贝，苹果对 `@[]` 使用了享元。

但是，如果集合中的对象的 copy 操作是浅拷贝，那么对于集合来说还不是真正意义上的深拷贝。比如，你需要对一个 `NSArray<NSArray *>` 对象进行真正的深拷贝，那么内层数组及其内容也应该执行深拷贝，可以对该集合对象进行 `归档` 然后 `解档`，只要集合中的对象都符合 NSCoding 协议。而且，使用这种方式，无论集合中存储的模型对象嵌套多少层，都可以实现深拷贝，但前提是嵌套的子模型也需要符合 NSCoding 协议才行，否则会导致 Crash。

```objectivec
NSArray *trueDeepCopyArray = [NSKeyedUnarchiver unarchiveObjectWithData:[NSKeyedArchiver archivedDataWithRootObject:oldArray]];
```

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210724054744.png)


>需要注意的是，使用 `initWithArray:copyItems:` 并将 copyItems 传 YES 时，生成的副本集合对象中的对象（下一个级别）是不可变的，所有更深的级别都具有它们以前的可变性。比如以下代码将 Crash。
>
>```objectivec
>NSArray *oldArray = @[@[].mutableCopy];
>NSArray *deepCopyArray = [[NSArray alloc] initWithArray:oldArray copyItems:YES];
>NSMutableArray *mArray = deepCopyArray[0]; // deepCopyArray[0] 已经被深拷贝为 NSArray 对象
>[mArray addObject:@""]; // Crash
>```
>而 `归档解档集合` 的方式会保留所有级别的可变性，就像以前一样。

#### 实现对自定义对象的拷贝

如果想要实现对自定义对象的拷贝，需要遵守 `NSCopying` 协议，并实现 `copyWithZone:` 方法。

* 如果要浅拷贝，`copyWithZone:` 方法就返回当前对象：return self；
* 如果要深拷贝，`copyWithZone:` 方法中就创建新对象，并给希望拷贝的属性赋值，然后将其返回。如果有嵌套的子模型也需要深拷贝，那么子模型也需符合 NSCopying 协议，且在属性赋值时调用子模型的 copy 方法，以此类推。

如果自定义对象支持可变拷贝和不可变拷贝，那么还需要遵守 `NSMutableCopying` 协议，并实现 `mutableCopyWithZone:` 方法，返回可变副本。而 `copyWithZone:` 方法返回不可变副本。使用方可根据需要调用该对象的 copy 或 mutableCopy 方法来进行不可变拷贝或可变拷贝。

#### 以下代码会出现什么问题？

```objectivec
@interface Model : NSObject
@property (nonatomic, copy) NSMutableArray *array;
@end
```

不论赋值过来的是 NSMutableArray 还是 NSArray 对象，进行 copy 操作后都是 NSArray 对象（深拷贝）。由于属性被声明为 NSMutableArray 类型，就不可避免的会有调用方去调用它的添加对象、移除对象等一些方法，此时由于 copy 的结果是 NSArray 对象，所以就会导致 Crash。

参考：[iOS 面试解析 - 对深浅拷贝的理解](https://juejin.cn/post/6988858119182876680 "iOS 面试解析 - 对深浅拷贝的理解")

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)

本期主题：`包大小优化`

1、[今日头条 iOS 安装包大小优化—— 新阶段、新实践](https://mp.weixin.qq.com/s/oyqAa8wKdioI5ZDG5LjkfA) -- 来自微信公众号：字节跳动技术团队


在多个渠道多次推荐的老文章了，再次推荐还是希望能跟大家一块打开思路，尤其在二进制文件的控制上，目前还有很多比较深入的手段去优化，资源的优化可能并不是全部的手段。

2、[今日头条优化实践： iOS 包大小二进制优化，一行代码减少 60 MB 下载大小](https://mp.weixin.qq.com/s/TnqAqpmuXsGFfpcSUqZ9GQ) -- 来自微信公众号：字节跳动技术团队


上篇文章的姊妹篇，也是大家比较熟悉的文章了。总而言之段迁移技术效果很明显，但是段迁移会带来一些其他的问题，比如文中提到的日志解析问题。我们在实践过程中也遇到了各种各样的小问题，一些二进制分析工具会失效，需要针对段迁移的 ipa 做适配。

3、[基于mach-o+反汇编的无用类检测](https://www.jianshu.com/p/c41ad330e81c "基于mach-o+反汇编的无用类检测") -- 来自简书：皮拉夫大王


很少在周报中推荐自己的文章，尤其是自己 2 年前的老文章。推荐这篇文章的原因是我在文中列举了 58 各个业务线的包大小占比分析。从数据中可以看出我们经过多年包大小治理后，资源的优化空间并不大，只能从二进制文件的瘦身上入手。可能很多公司的 APP 也有同样的问题，就是资源瘦身已经没有太大的空间了，这时我们就应该从二进制层面寻找突破口。文中工具地址：[Github WBBlades](https://github.com/wuba/WBBlades "Github WBBlades")

4、[Flutter包大小治理上的探索与实践](https://tech.meituan.com/2020/09/18/flutter-in-meituan.html) -- 来自美团技术团队：艳东 宗文 会超


谈点新鲜的内容。作者首先对 Flutter 的包大小进行了细致的分析，并在双平台选择了不同的优化方案。在 Android 平台选择动态下发，而 iOS 平台则将部分非指令数据进行动态下发。通过修改 Flutter 的编译后端将 data 重定向输入到文件，从而实现了数据段与文本段的拆分。使用 Flutter 的团队可以关注下这个方案。

5、[iOS 优化 - 瘦身](https://mp.weixin.qq.com/s/wDcYvea5dTq0dh0PBwRu4A) -- 来自微信公众号：CoderStar


文章详细介绍了 APP 瘦身的技巧与方案，包括资源和代码层面。对图片压缩与代码的编译选项有深入的解释。方案比较全面，可以通过此文章检查 APP 瘦身是否还有哪些方案没有应用。

6、[科普：为什么iOS的APP比安卓大好几倍？](https://www.jianshu.com/p/6f2adc5aeb9a "科普：为什么iOS的APP比安卓大好几倍？") -- 来自简书：春暖花已开


前几篇文章已经将瘦身的技术介绍得比较完善了。接下来通过这篇文章回答下老板们经常会问到的问题：为什么 iOS 的包比安卓的大？是因为 iOS 的技术不如安卓吗？建议 iOS 程序员都看看这个问题，至少可以满足我们自己的好奇心。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Better Explaine

地址：https://betterexplained.com/

Better Explaine 是一个帮助你真正理解数学概念、使数学概念变得有趣的网站，在这个网站你可以看到很多复杂的概念被分解成图形、公式和通俗易懂的解释。网站的指导思想是爱因斯坦的这句话：“如果你不能简单地解释它，你就没有充分地理解它”，这里没有装腔作势，没有古板老师，只是一个兴奋的朋友在分享究竟是什么让一个想法变成了现实！

### 程序员可能必读书单推荐

地址：https://draveness.me//books-1

来自 [Draveness](https://draveness.me/) 的程序员书单，这是书单的系列一，应该还会有后续的推荐。这次的推荐中推荐了三本「大部头」：SICP、CTMCP 和 DDIA。即使你和小编一样感觉这些书晦涩难懂（苦笑），并不准备阅读，也可以从 Draveness 的这篇书单推荐中窥探一眼别人的编程世界是什么样的😉。

## 工具推荐

整理编辑：[CoderStar](https://juejin.cn/user/588993964541288/posts)

### Snipaste

**地址**： https://zh.snipaste.com/

**软件状态**： 普通版免费，专业版收费，有 Mac、Windows 两个版本

**软件介绍**：

Snipaste 是一个简单但强大的截图工具，也可以让你将截图贴回到屏幕上！普通版的功能已经足够使用，笔者认为其是最好用的截图软件了！（下图是官方图）

![Snipaste](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/N3QEb3VA.png)

### LSUnusedResources

**地址**： https://github.com/tinymind/LSUnusedResources

**软件状态**： 免费

**软件介绍**：

一个 Mac 应用程序，用于在 Xcode 项目中查找未使用的图像和资源，可以辅助我们优化包体积大小。

![LSUnusedResources](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/LSUnusedResourcesExample.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十九期](https://mp.weixin.qq.com/s/dtyozlqCO7PcpyGhx2qB5g)

[iOS摸鱼周报 第十八期](https://mp.weixin.qq.com/s/JsGmu7pzYLI3Svrmk5i2cA)

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
