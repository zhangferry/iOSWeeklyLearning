# iOS摸鱼周报 第十九期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[FBY展菲](https://github.com/fanbaoying)

**介绍**

在项目中遇到数据展示需求时，往往会通过，以列表的形式展示出数据或者以表格的形式展示。但是并不能直观的观察数据的变化，如果通过图表的形式来展示，就可以更快捷的获取到数据变化情况。下面给大家分享统计图包括折线统计图、柱状图、环形图。

**项目展示**

<img src="https://mmbiz.qpic.cn/mmbiz_png/iabC3iaGjoCC1jkmpicIzNBCB7EBicUAfiaQaCNkiaK6aKxNyOdjGzgvHMvCa64ZTgoMsjZPHK3ict56dzFibu4tsQoziag/0?wx_fmt=png">

**折线统计图实现思路分析**

1、折线图基础框架实现 `FBYLineGraphBaseView`类

折线图基础框架包括Y轴刻度标签、x 轴刻度标签、与 x 轴平行的网格线的间距、网格线的起始点、x 轴长度、y 轴长度。

2、折线图数据内容显示 `FBYLineGraphContentView` 类

折线图数据内容显示是继承 `FBYLineGraphBaseView` 类进行实现，其中主要包括，X轴最大值、数据内容来实现。

3、折线图颜色控制类 `FBYLineGraphColorView` 类

折线图颜色控制类主要控制选中远点边框宽度和整体布局颜色

4、折线图核心代码类 `FBYLineGraphView` 类

折线图核心代码类主要给引用类提供配置接口和数据接口，其中包括表名、y 轴刻度标签 title、y 轴最大值、x 轴刻度标签的长度（单位长度）、设置折线图显示的数据和对应X坐标轴刻度标签

**柱状图实现思路分析**

实现柱状图的核心代码是 `FBYBarChartView` 类，基础框架包括文字数组、树值数组、渐变色数组、标注值、间距、滑动、渐变方向。

**环形图实现思路分析**

实现环形图的核心代码是 `FBYRingChartView` 类，基础框架包括中心文字、标注值、颜色数组、值数组、图表宽度。

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
