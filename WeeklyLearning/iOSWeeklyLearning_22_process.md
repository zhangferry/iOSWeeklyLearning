# iOS摸鱼周报 第二十二期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> 

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) 、[zhangferry](https://zhangferry.com)

###  `Reachability` 类的实践准则

在网络请求实践中，常见的操作是监听 `Reachability` 的状态或变换来有选择的对网络的可达性进行判断，做出阻止或暂停请求的对应操作。

一直以来，受到监听网络状态这种手段的影响，当用户在执行某些操作时，会根据获取到的用户当前的网络状态，在网络不可达（**NotReachable**）的情况下会**阻止用户发起网络请求**。

直到我看到了 AFNetworking  Issues 中的 [Docs on Reachability contradict Apple's docs](https://github.com/AFNetworking/AFNetworking/issues/2701#issuecomment-99965186) 。

我们不应该使用 `Reachability` 作为网络是否可用的判断，因为在某些情况下，其返回的状态可能不那么准确。

在  AFNetworking 的定义了关于  `Reachability` 的最佳实践：

> Reachability can be used to determine background information about why a network operation failed, or to trigger a network operation retrying when a connection is established. It should not be used to prevent a user from initiating a network request, as it's possible that an initial request may be required to establish reachability.

请我们应该将其用于**网络请求后失败**的背景信息，或者在失败后用于**判断是否应该重试**。不应该用于阻止用户发起网络请求，因为可能需要初始化请求来建立**可达性**。

我们在网络请求中集成的 `Reachability` 应该用在**请求失败后**，无论是作为请求失败的提示，还是利用可达性状态的更改，作为请求重试的条件。

当我们使用 `AFNetworkReachabilityManager` 或者功能相似的 `Reachability` 类时，我们可基于此来获取当前的网络类型，如 4G 还是 WiFi。但是当我们监听到其状态变为不可达时，不应该立即弹出 `Toast` 来告诉用户当前网络不可用，而应该是当请求失败以后判断该状态是否是不可达，如果是，再提示没有网络。并且，如果该接口需要一定的连贯性的话，可以保留当前的请求参数，提示用户等待网络可达时再主动去请求。

### SQL 中的 JOIN 和 UNION

JOIN 作用是把多个表的行结合起来，各个表中对应的列有可能数据为空，就出现了多种结合关系：LEFT JOIN、RIGHT JOIN、INNER JOIN、OUTER JOIN。对应到集合的表示，它们会出现如下 7 种表示方法：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210807132907.png)

UNION 表示合并多个 SELECT 结果。UNION 默认会合并相同的值，如果想让结果逐条显示的话可以使用 UNION ALL。

有一个场景：三个表：table1、table2、table3，他们共用一个 id，table2 和 table3 为两个端的数据接口完全相同的数据，我现在要以table1 的某几个列为准，去查看对应到 table2 和 table3 与之关联的几个列的数据。SQL 语句如下：

```sql
select 
  t1.id
	t1.column_name1 as name1,
	t1.column_name2 as name2,
  t2.column_name3 as name3,
  t2.column_name4 as name4
from 
	(
	select 
    id,
		column_name1,
     column_name2
	from 
		table1_name
	) t1
left join 
	(
	select 
		union_table.* 
	from
		(
        select 
            id,
            column_name3,
            column_name4
        from 
            table2_name
        union all 
        select 
            id,
            column_name3,
            column_name4
        from 
            table3_name
        ) union_table 
	) t2 on t1.id = t2.id
```

### 在项目中区分 AppStore/Adhoc 包

在解决这个问题前，我们先要了解开发环境这个概念，看看你的理解和我下面说的是否一致。iOS 的开发环境通常涉及三个维度：项目，开发端服务器，AppStore服务器。

**项目**

即我们的 Xcode 项目，它由 Project 里的 Configuration管理，默认有两个开发环境：Debug、Release。而我们常用的控制开发环境的宏命令如 `DEBUG` 是Xcode帮我们预置的值，它的设置形式为`DEBUG=1`，这里的内容都是可以修改的。

我们新增一个名为 AppStore 的 Configuration，然后给其设置一个宏`APPSTORE=1`，然后将之前的 Release 设置为 `ADHOC=1`，即是为这两个项目环境指定了特定的宏。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210807151150.png)

**开发端服务器**

服务器环境由服务端管理，反应到项目里，我们通常将其跟项目环境保持一致。

**AppStore 服务器**

AppStore 的开发环境根据证书形式来定，在最后的封包环节决定，Xcode 将其分为以下四种场景：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210807151744.png)

可以看到 Configuration 设置和 封包环节是相互独立的，如果本地有三个 Configuration 的话，我们可导出的包类型数量最多为：3 x 4 = 12 种。所以如果仅仅用开发包和生成环境包描述一个包的类型肯定是不够用的，但全描述又不现实，又因封包环节在编译之后，所以我们没法提前决定包类型，所以就有了约定成俗的一些习惯。

开发包通常指：Debug + Development，

生产环境包通常指：Release + Ad Hoc 或 Release + App Store Conenct

如题目所说，如果我们要区分Ad Hoc 和 AppStore，就需要新增 Configuration：AppStore，这样的话：

Ad Hoc包：Release + Ad Hoc

AppStore包：AppStore + App Store Connect

## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`电量优化`


1、[iOS性能优化之耗电检测](https://www.diffit.cn/2020/09/03/EnergyDetection/) -- 来自：杂货铺

文章介绍了耗电量检测的三种方式：Energy impact、Energy Log、sysdiagnose。 每种方案详细介绍了检测步骤。在Energy Log中提到了“当前台三分钟或后台一分钟CPU线程连续占用80%以上就判定为耗电，同时记录耗电线程堆栈供分析”，这对我们日常分析有一定的帮助。

2、[Analyzing Your App’s Battery Use](https://developer.apple.com/documentation/xcode/analyzing-your-app-s-battery-use) -- 来自：Apple

苹果官方提供了一些性能监控的手段，通过Xcode Organizer可以查看24小时的性能数据，包括电量数据。

3、[iOS 性能优化：使用 MetricKit 2.0 收集数据](https://mp.weixin.qq.com/s/cbP0QlxVlr5oeTrf6yYfFw) -- 来自老司机周报：Jerry4me

既然提到了官方的方案就不得不提到MetricKit。本文介绍了什么是MetricKit，如何使用以及iOS 14之后的新的数据指标。另外需要注意的是MetricKit是iOS13之后才支持的，并且并不能搜集全部用户的数据，只有共享 iPhone 分析的用户数据才能被收集。

4、[iOS进阶--App功耗优化](http://www.cocoachina.com/articles/21428 "iOS进阶--App功耗优化") -- 来自cocoachina：yyuuzhu 

直观上耗电大户主要包括：CPU、设备唤醒、网络、图像、动画、视频、动作传感器、定位、蓝牙。测试工具：Energy Impact、Energy Log，更加具体的信息查看本文。

5、[iOS耗电量和性能优化的全新框架](https://punmy.cn/2019/06/16/wwdc_417_metrics.html "iOS耗电量和性能优化的全新框架") -- 来自博客：Punmy

在 Session 417 中，苹果推出了三项新的电量和性能监测工具，分别用于开发阶段、内测阶段、以及线上阶段。相信通过本文，你会对你的 App 接下去的耗电量和性能优化的方向，有更好的计划。

6、[耗电优化的几点建议](https://lizhaobomb.github.io/2020/03/02/iOS%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%9606%20-%20%E8%80%97%E7%94%B5%E4%BC%98%E5%8C%96/ "耗电优化的几点建议") -- 来自博客：Catalog

关于耗电优化的几点实操性的建议。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Seeing Theory

地址；https://seeing-theory.brown.edu/cn.html

由布朗大学的学生制作的「看见统计」课程，致力于用数据可视化的手段让数理统计概念更容易理解。其中的内容与国内本科的概率论与数理统计内容也大致相仿，且对于中文的本地化支持的非常好。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/%E6%88%AA%E5%B1%8F2021-08-06%20%E4%B8%8B%E5%8D%885.41.41.png)

### Hacker Laws

地址：https://github.com/dwmkerr/hacker-laws

我们常常会说「xx法则」、「xx定律」，如「摩尔定律」等。在 Hacker Laws 这个仓库中，我们可以找到在开发者群体比较有名或者是比较常见的法则和定律。但要注意：这个资源库包含了对一些法则、原则和模式的解释，**但并不提倡任何一种**。它们是否应该被应用在很大程度上取决于你正在做的事情，要根据情况来判断使用与否。

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

### regex101

**地址**：https://regex101.com

一个正则表达式测试和分析网站，不仅可以将匹配结果进行输出，还会逐个分析表达式的含义。我们以摸鱼周报`关于我们`的文案进行测试，我们想匹配出 “iOS 摸鱼周报”（中间有空格），“iOS成长之路”，这两个字符串，测试结果如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210807164527.png)

观察右侧结果分析，示例中使用的`*?`非贪婪模式和`(?=，)`零宽度正预测先行断言，都有很详细的讲解。所以该网站还可以作为一个很好的学习正则表达式的工具。

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第二十一期](https://mp.weixin.qq.com/s/Hcd8CtkyqD8IXM0SbVJo-A)

[iOS摸鱼周报 第二十期](https://mp.weixin.qq.com/s/PjiZzx3VSAfAGHRJs160aQ)

[iOS摸鱼周报 第十九期](https://mp.weixin.qq.com/s/dtyozlqCO7PcpyGhx2qB5g)

[iOS摸鱼周报 第十八期](https://mp.weixin.qq.com/s/JsGmu7pzYLI3Svrmk5i2cA)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
