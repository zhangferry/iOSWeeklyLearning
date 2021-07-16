# iOS摸鱼周报 第十九期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 本期话题

[@zhangferry](https://zhangferry.com)：

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

**总结**

项目源码开源，有需要的小伙伴可以根据需求定制开发，对于折线统计图需要注意的是日期和数据的对应关系以及页面刷新时

**遇到的问题**（已解决）

reloadDatas 方法无效，title 没变，数据源没变，移除 layer 的时候还会闪退

解决方案，在 reloadData 时，需要将之前缓存的数组数据 pointArray 清空，不然数组中保存了上次的数据。


参考：[码一个高颜值统计图 - 展菲](https://mp.weixin.qq.com/s/pzfzqdh7Tko9mfE_cKWqmg "码一个高颜值统计图")


## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)




## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)



## 联系我们

[iOS摸鱼周报 第十一期](https://zhangferry.com/2021/05/16/iOSWeeklyLearning_11/)

[iOS摸鱼周报 第十二期](https://zhangferry.com/2021/05/22/iOSWeeklyLearning_12/)

[iOS摸鱼周报 第十三期](https://zhangferry.com/2021/05/30/iOSWeeklyLearning_13/)

[iOS摸鱼周报 第十四期](https://zhangferry.com/2021/06/06/iOSWeeklyLearning_14/)

[iOS摸鱼周报 第十五期](https://zhangferry.com/2021/06/14/iOSWeeklyLearning_15/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
