# iOS摸鱼周报 第十九期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 本期话题讲了关于学习和记忆的一些方法。
> * 开发 Tips 讲了一个统计图的设计思路，可以试下自己能否也实现一个；如何区分 minimumLineSpacing 和 minimumInteritemSpacing 这两个属性；本地化关于日期的注意事项。
> * 面试解析
> * 优秀博客整理了几篇卡顿优化的优质文章。
> * 学习资料有两个内容，Combine Operators：帮助理解 Combine 操作符的手机端App；还有Stanford 最新的SwiftUI 2.0 双语教程。
> * 开发工具带来了一个基于 linkmap 分析执行文件大小的工具：LinkMap。

## 本期话题

[@zhangferry](https://zhangferry.com)：本期讲下高效记忆这个话题，多数内容来源于《暗时间》。关于知识书中有句话是这样说的：

> 你所拥有的知识并不取决于你记得多少，而在于它们能否在恰当的时候被回忆起来。

这让我想起爱因斯坦的一句话：

> 教育就是忘记了在学校所学的一切之后剩下的东西。

两种说法很相似，都在强调为我所用才是知识的真正价值。而为我所用的前提就是记忆，记住了，才有可能在适当的时候被唤醒，记忆与学习也总是相辅相成的。关于记忆有一个被广泛认可的机制：我们在记忆的时候会将很多线索（例如当时的场景、语言环境等）一并编码进行记忆，事后能否快速提取出来主要就取决于这些线索有多丰富。

针对这一机制有以下方法可用于加深记忆并辅助学习：

* 过段时间尝试再回忆。它的作用一方面是转换为长时记忆，还有一方面可以通过当前掌握的知识体系重新整合原有知识，有时可以得到新的启发。
* 用自己的语言表述，书写下来，甚至讲给他人听。这个就是费曼学习法了，它的作用是确保不是我以为我理解了，而是我可以用自己的方式理解。
* 气味，背景音乐，天气等这些外接因素，都可以作为线索进行编码记忆。有时我们偶然听一首以前流行的歌曲，能一下子回忆起当时的场景和感受，感觉尘封记忆被打开，DNA 动了一样，这些都是基于记忆这个机制导致的。

* 对于经验知识的学习，光听别人说或者看着别人做还不够，我们可以努力设想自己处于别人的境地，感受它们，将它们和你的情绪记忆挂钩。

* 如果一件事情就是一件事情，那我们永远也无法学到“未来”的知识，所以我们还要剥去无关紧要的细节，抽象出那个关键点，这样才能进行知识的迁移与推广。

## 开发Tips

### 码一个高颜值统计图

整理编辑：[FBY展菲](https://github.com/fanbaoying)

**介绍**

项目开发中有一些需求仅仅通过列表展示是不能满足的，如果通过图表的形式来展示，就可以更快捷的获取到数据变化情况。下面给大家分享三类统计图：**折线统计图**、**柱状图**、**环形图**。

**项目展示**

<img src="https://mmbiz.qpic.cn/mmbiz_png/iabC3iaGjoCC1jkmpicIzNBCB7EBicUAfiaQaCNkiaK6aKxNyOdjGzgvHMvCa64ZTgoMsjZPHK3ict56dzFibu4tsQoziag/0?wx_fmt=png">

**折线统计图实现思路分析**

折线图基础框架包括Y轴刻度标签、x 轴刻度标签、与 x 轴平行的网格线的间距、网格线的起始点、x 轴长度、y 轴长度，折线图数据内容显示是继承 `FBYLineGraphBaseView` 类进行实现，其中主要包括，X轴最大值、数据内容来实现，核心源码如下：

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
        
        // 记录各点的坐标方便后边添加渐变阴影 和 点击层视图 等
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

**柱状图实现思路分析**

实现柱状图的核心代码是 `FBYBarChartView` 类，基础框架包括文字数组、树值数组、渐变色数组、标注值、间距、滑动、渐变方向。实现核心源码如下:

```objectivec
- (void)drawLine {
    CAShapeLayer *lineLayer= [CAShapeLayer layer];
    _lineLayer = lineLayer;
    [lineLayer setLineDashPattern:[NSArray arrayWithObjects:[NSNumber numberWithInt:1], [NSNumber numberWithInt:1.5], nil]];
    lineLayer.fillColor = [UIColor clearColor].CGColor;
    lineLayer.lineWidth = 0.5f;
    lineLayer.strokeColor = [UIColor grayColor].CGColor;
    _height = self.frame.size.height;
    _width = self.frame.size.width;
    _barMargin = 20.0;
    _lineHeight = _height - 20;
    if (_type == OrientationHorizontal) {
        _x = 60;
        _y = 0;
        _lineWidth = _width - _x - 20;
    } else{
        _x = 40;
        _y = 20;
        _lineWidth = _width - _x;
    }
    
    //参照线
    UIBezierPath *linePath = [UIBezierPath bezierPath];
    
    [linePath moveToPoint:CGPointMake(_x,_y)];
    [linePath addLineToPoint:CGPointMake(_x + _lineWidth,_y)];
    [linePath addLineToPoint:CGPointMake(_x + _lineWidth,_lineHeight)];
    [linePath addLineToPoint:CGPointMake(_x,_lineHeight)];
    [linePath addLineToPoint:CGPointMake(_x,_y)];
    if (_type == OrientationHorizontal) {
        for (int i = 1; i < _markLabelCount; i++) {
            [linePath moveToPoint:CGPointMake(_x + _lineWidth / _markLabelCount * i, 0)];
            [linePath addLineToPoint:CGPointMake(_x + _lineWidth / _markLabelCount * i,_lineHeight)];
        }
    } else{
        for (int i = 1; i < _markLabelCount; i++) {
            [linePath moveToPoint:CGPointMake(_x, (_lineHeight - _y) / _markLabelCount * i +_y)];
            [linePath addLineToPoint:CGPointMake(_x + _lineWidth,(_lineHeight - _y) / _markLabelCount * i + _y)];
        }
    }
    lineLayer.path = linePath.CGPath;
    [self.layer addSublayer:lineLayer];
}
```

**环形图实现思路分析**

实现环形图的核心代码是 `FBYRingChartView` 类，基础框架包括中心文字、标注值、颜色数组、值数组、图表宽度。实现核心源码如下:

```objectivec
-(void)drawChart {
    if (_markViewDirection) {
        CGFloat x = 0;
        CGFloat y = 0;
        CGFloat mvWidth = 100;
        CGFloat mvHeight = 12;
        CGFloat margin = 0;
        
        _mvArray = [NSMutableArray array];
        for (int i = 0; i < _valueArray.count; i++) {
            int indexX = i % 2;
            int indexY = i / 2;
            
            if (_markViewDirection == MarkViewDirectionLeft) {
                margin = (_radius * 2 - 12 * _valueArray.count) / 5;
                x = _width * 0.75 - _radius - mvWidth - 30;
                y = (_height - _radius * 2) / 2 + (margin + mvHeight) * i;
            } else if (_markViewDirection == MarkViewDirectionRight){
                margin = (_radius * 2 - 12 * _valueArray.count) / 5;
                x = _width * 0.25 + _radius + 30;
                y = (_height - _radius * 2) / 2 + (margin + mvHeight) * i;
            } else if (_markViewDirection == MarkViewDirectionTop){
                x = indexX == 0 ? _width / 2 - 15 - mvWidth : _width / 2 + 15;
                y = _height * 0.75 - _radius - 30 - (_valueArray.count / 2) * 12 - (_valueArray.count / 2 - 1) * 10 + indexY * (12 + 10);
            }  else if (_markViewDirection == MarkViewDirectionBottom){
                x = indexX == 0 ? _width / 2 - 15 - mvWidth : _width / 2 + 15;
                y = _height * 0.25 + _radius + 30 + indexY * (12 + 10);
            }
        }
    }
    
    [_layerArray enumerateObjectsUsingBlock:^(CAShapeLayer *  _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
        CABasicAnimation *ani = [CABasicAnimation animationWithKeyPath : NSStringFromSelector ( @selector (strokeEnd))];
        ani.fromValue = @0;
        ani.toValue = @1;
        ani.duration = 1.0;
        [obj addAnimation:ani forKey:NSStringFromSelector(@selector(strokeEnd))];
    }];
    
    [_mvArray enumerateObjectsUsingBlock:^(UIView *  _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
        [UIView animateWithDuration:1 animations:^{
            obj.alpha = 1;
        }];
    }];
}
```

**遇到的问题**（已解决）

reloadDatas 方法无效，title 没变，数据源没变，移除 layer 的时候还会闪退

解决方案，在 reloadData 时，需要将之前缓存的数组数据 pointArray 清空，不然数组中保存了上次的数据。


参考：[码一个高颜值统计图 - 展菲](https://mp.weixin.qq.com/s/pzfzqdh7Tko9mfE_cKWqmg)

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)

### UICollectionView 的 scrollDirection 对 minimumLineSpacing 和 minimumInteritemSpacing 影响

整理编辑：[人魔七七](https://github.com/renmoqiqi)

minimumLineSpacing 和 minimumInteritemSpacing 这两个值表示含义是受滚动方向影响的，不同滚动方向，行列的排列方式不同，我们仅需记住行间距为 lineSpace 即可。下图为可视化的描述：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210716180322.png)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/3162666d7fa108da73e6549aea9154cf.png)

### 本地化时一些需要注意的日期设置

不同地域会有不同的日期格式，一般而言，我们都默认使用 `[NSLocale defaultLocale]` 来获取存储在设备设置中 `Regional Settings` 的地域，而不是指定某个地域，该行为不需要显示设置。

默认的语言/区域设置会导致 `NSCalendar`，`NSDateFormatter` 等跟区域关联的类上存在不同的展示

#### **Calendar** 的 firstWeekday

> The firstWeekday property tells you what day of the week the week starts in your locale. In the US, which is the default locale, a week starts on Sun.

当我们使用 `Calendar` 的 `firstWeekday` 属性时，需要注意，这个世界上不是所有地域其 `firstWeekday`  值都是 `1`。比如，对莫斯科来说，其  `firstWeekday`   的值是 `2`。 

如果你的日历控件并没有考虑到这些，对于某一天具体排列在一周的哪天来说，其值是不同的。

笔者之前所做的日历头部是按照周一至周日固定展示的，然后用户在俄罗斯发现日期乱了，日期与周几错乱。

后续直接定死了`firstWeekday = 1` 来功能上解决了这个问题。

#### **DateFormatter**

目前部分地域（部分欧美国家）存在**夏令时**，其会在接近春季开始的时候，将时间调快一小时，并在秋季调回正常时间。

虽然目前现有的设备支持特定的夏令时的展示，但是存在某些历史原因，如俄罗斯：

```swift
let dFmt = DateFormatter()
dFmt.dateFormat = "yyyy-MM-dd"
dFmt.timeZone = TimeZone(identifier:"Europe/Moscow")
print(dFmt.date(from:"1981-04-01") as Any) // nil
print(dFmt.date(from:"1982-04-01") as Any) // nil
print(dFmt.date(from:"1983-04-01") as Any) // nil
print(dFmt.date(from:"1984-04-01") as Any) // nil
```

对于 1981 年-1984 年 4 个年度的俄罗斯来说，4 月 1 号当天没有零点，会导致转化出的 `Date` 为 nil。如果我们需要做类似转换，就需注意该特殊情况。

## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`卡顿优化`

1、[iOS卡顿监测方案总结](https://juejin.cn/post/6844903944867545096 "iOS卡顿监测方案总结")


文章总结了业界的很多卡顿监控技术。包括：FPS、runloop、子线程Ping、CPU占用率监测。文章中附带了作者参考和收集到的原文链接，以及部分相关上下游技术的文章。如果您想要做卡顿监控，阅读本文可以节省不少时间和精力。

2、[iOS 渲染原理解析](https://mp.weixin.qq.com/s/6ckRnyAALbCsXfZu56kTDw)


文章细致的介绍了图像渲染的流程。包括一些细小有趣的知识点，比如 CALayer 的 contents 保存了 bitmap 信息等。文中当然少不了对离屏渲染的介绍，包括离屏渲染的场景、离屏渲染的原因以及如何避免离屏渲染。文后附有小题目，可以让大家带着问题回顾文章，加深对知识的理解。

3、[UIView 动画降帧探究](https://mp.weixin.qq.com/s/EcVrrT1M4mI4f4d2b3qV0Q)


本文首先介绍为了降帧的目的：降低GPU的使用率，并介绍了为什么动画渲染对GPU有较大的影响。正文中主要介绍了降帧的方案：UIView animation 指定 UIViewAnimationOptionPreferredFramesPerSecond30 进行降帧、CADisplayLink 逐帧动画降帧。

4、[天罗地网？ iOS卡顿监控实战](https://juejin.cn/post/6844904005437489165 "天罗地网？ iOS卡顿监控实战") -- 来自掘金：进击的蜗牛君

本文利用"ping"方案，即每隔一段时间就去目标线程中检测状态，如果目标线程"运行良好"，则标记为正常，当一段时间"ping"均不正常时，上报目标线程的堆栈，此时认为目标线程发生了卡顿，作者已经做出了开源工具，方便大家深入研究。

5、[列表流畅度优化](https://juejin.cn/post/6844903656769208334 "列表流畅度优化") -- 来自掘金：Hello_Vincent

作者借鉴了WWDC18的相关session，从实际角度出发，进行一次列表优化的旅程，从原因到解决办法，最后提出意见，称得上是一篇佳作。

6、[WWDC2016 Session笔记 - iOS 10 UICollectionView新特性
](https://juejin.cn/post/6844903441416847374 "WWDC2016 Session笔记 - iOS 10 UICollectionView新特性
") -- 来自掘金：一缕殇流化隐半边冰霜

早在WWDC16，官方针对UICollectionView已经做过优化教程，如果你还不知道，可以看一看这篇文章。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Combine Operators

地址：https://apps.apple.com/app/combine-operators/id1507756027

一个用来学习 Combine 的 App，他将一些 Combine 中的各种操作符用可视化的手段表达了出来，还附加了蠢萌蠢萌的动画效果，很适合刚接触的 Combine 的朋友尝试一下。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/co.png)

### Stanford CS193P 2021 SwiftUI 2.0 双语字幕

地址：https://www.bilibili.com/video/BV1q64y1d7x5

Stanford CS193P 2021 SwiftUI 2.0 课程，该课程的老师是 Paul Hegarty，在 Stanford 执教 10 年左右了。该课程创办了很多年，每当 Apple 推出了新技术，例如 Storyboard、SwiftUI，这个白胡子老爷爷就会迅速跟上，更新他的课程，实乃一 it 潮人。你可以去油管 Stanford 官方账号查看该课程，也可以看看 up 主转载的该课程，还上传了中文字幕、英文字幕、繁体字幕的双语版本。理论上来说，你只需要有面向对象编程及 Swift 语言的相关基础和了解，你就可以看懂该课程，适合想要学习 SwiftUI 入门的朋友。

## 工具推荐

整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

**地址**： https://github.com/huanxsd/LinkMap

**软件状态**： 免费 

**软件介绍**

iOS 包的大小，是每个开发必须关注的问题，对于大型项目来说，只是代码段就有可能超过 100M，算上 armv7 和arm64 架构，会超过 200M。 LinkMap 工具通过分析项目的 LinkMap 文件，能够计算出各个类、各个三方库占用的空间大小（代码段+数据段），方便开发者快速定位需要优化的文件。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/linkmap.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十八期](https://mp.weixin.qq.com/s/JsGmu7pzYLI3Svrmk5i2cA)

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
