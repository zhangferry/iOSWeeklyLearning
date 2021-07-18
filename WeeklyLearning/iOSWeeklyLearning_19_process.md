# iOS摸鱼周报 第十九期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> 

## 本期话题

[@zhangferry](https://zhangferry.com)：本期讲下如何学习这个话题，多数内容来源于《暗时间》。书中有句话：

> 你所拥有的知识并不取决于你记得多少，而在于它们能否在恰当的时候被回忆起来。

想起来爱因斯坦的另一句话：

> 教育就是忘记了在学校所学的一切之后剩下的东西。

两种说法非常相似，都在强调使用的重要性。但这些的前提都是我们首先要记住它，然后适当的时候才有可能被唤醒。有效的记忆方法有这些呢，其中最重要的一点就是，记忆存在于大脑是碎片化的，要想记忆某个内容，需要给它提供尽可能多的线索。有以下方法可以提供多线索：过段时间尝试再回忆、通过旧知识的迁移，用自己的语言表述，讲给他人听，书写下来，甚至气味、背景音乐这些都会作为线索进行编码记忆。

对于经验知识的学习来说，光听别人说或者看着别人做还不够，我们可以设法努力设想自己处于别人的境地，感受它们，是他们和你的情绪记忆挂钩。

另一点，如果一件事情就是一件事情，那永远也无法学到“未来”的知识，所以我们还要抓住核心关键点，剥去无关紧要的细节，抽象出那个核心点，然后进行知识的迁移推广。

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
- (void)drawChartLine
{
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
- (void)drawLine{
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
-(void)drawChart
{
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


参考：[码一个高颜值统计图 - 展菲](https://mp.weixin.qq.com/s/pzfzqdh7Tko9mfE_cKWqmg "码一个高颜值统计图")

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)

### UICollectionView 的scrollDirection 对 minimumLineSpacing 和 minimumInteritemSpacing 影响


滚动方向垂直方向时候原理图

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210716180322.png)

滚动方向水平方向时候原理图

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/3162666d7fa108da73e6549aea9154cf.png)

### 基于不同语言环境下的日期

如果我们的程序存在日期相关操作，并且开发者是一个地域的开发者但是其开发的程序面向全世界时，需要注意一些事情。

例如，中文和英文的阅读方式是从左往右的，排版也是从左往右，我们以左箭头表示前一个，以右箭头表示下一个。而当你面向阿拉伯语、维吾尔语使用者时，这些都是相反的，这就是**LTR（left to right）** 和 **RTL（right to left）**。

除了语言环境的不同，不同的地域也会存在不同的日期格式。一般而言，我们都默认使用 `[NSLocale defaultLocale]` 来获取存储在设备设置中 `Regional Settings` 的地域，而不是指定某个地域 —— 不需要显示设置。

默认的语言/区域设置会导致 `NSCalendar`，`NSDateFormatter` 等类似的跟区域关联类上存在不同的展示

#### **Calendar** 的 firstWeekday

> The firstWeekday property tells you what day of the week the week starts in your locale. In the US, which is the default locale, a week starts on Sun.

当我们使用 `Calendar` 的 `firstWeekday` 属性时，需要注意，这个世界上不是所有地域其 `firstWeekday`  值都是 `1`。比如，对莫斯科来说，其  `firstWeekday`   的值是 `2`。 

如果你的日历控件并没有考虑到这些，对于某一天具体排列在一周的哪天来说，其值是不同的。

笔者之前所做的日历头部是按照周一至周日固定展示的，然后用户在俄罗斯发现日期乱了，日期与周几错乱。

后续直接定死了`firstWeekday = 1` 来功能上解决了这个问题。

#### **DateFormatter**

目前部分地域（部分欧美国家）存在**夏令时**，其会在接近春季开始的时候，将时间调快一小时，并在秋季调回正常时间。

虽然目前现有的设备支持特定的夏令时的展示，但是存在某些历史原因，又是俄罗斯：

```swift
let dFmt = DateFormatter()
dFmt.dateFormat = "yyyy-MM-dd"
dFmt.timeZone = TimeZone(identifier:"Europe/Moscow")
print(dFmt.date(from:"1981-04-01") as Any) // nil
print(dFmt.date(from:"1982-04-01") as Any) // nil
print(dFmt.date(from:"1983-04-01") as Any) // nil
print(dFmt.date(from:"1984-04-01") as Any) // nil
```

对于 1981 年-1984 年 4 个年度的俄罗斯来说，4 月 1 号当天没有零点。

如果后台返回给你字符串需要你转换 1981 年-1984 年 4 个年度 4 月 1 号的零点的话，需要注意其日期格式化之后值为 `nil`。

## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`卡顿优化`

1、[iOS卡顿监测方案总结](https://juejin.cn/post/6844903944867545096 "iOS卡顿监测方案总结")


文章总结了业界的很多卡顿监控技术。包括：FPS、runloop、子线程Ping、CPU占用率监测。文章中附带了作者参考和收集到的原文链接，以及部分相关上下游技术的文章。如果您想要做卡顿监控，阅读本文可以节省不少时间和精力。

2、[iOS 渲染原理解析](https://mp.weixin.qq.com/s/6ckRnyAALbCsXfZu56kTDw)


文章细致的介绍了图像渲染的流程。包括一些细小有趣的知识点，比如CALayer的contents保存了 bitmap信息等。文中当然少不了对离屏渲染的介绍，包括离屏渲染的场景、离屏渲染的原因以及如何避免离屏渲染。文后附有小题目，可以让大家带着问题回顾文章，加深对知识的理解。

3、[UIView 动画降帧探究](https://mp.weixin.qq.com/s/EcVrrT1M4mI4f4d2b3qV0Q)


本文首先介绍为了降帧的目的：降低GPU的使用率，并介绍了为什么动画渲染对GPU有较大的影响。正文中主要介绍了降帧的方案：UIView animation 指定 UIViewAnimationOptionPreferredFramesPerSecond30进行降帧、CADisplayLink逐帧动画降帧。

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

整理编辑：[zhangferry](https://zhangferry.com)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
