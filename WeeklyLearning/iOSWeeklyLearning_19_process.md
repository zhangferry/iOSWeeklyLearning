# iOS摸鱼周报 第十九期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

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




## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Combine Operators

链接：https://apps.apple.com/app/combine-operators/id1507756027

一个用来学习 Combine 的 App，他将一些 Combine 中的各种操作符用可视化的手段表达了出来，还附加了蠢萌蠢萌的动画效果，很适合刚接触的 Combine 的朋友尝试一下。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/co.png)

### Stanford CS193P 2021 SwiftUI 2.0 双语字幕

地址：https://www.bilibili.com/video/BV1q64y1d7x5

Stanford CS193P 2021 SwiftUI 2.0 课程，该课程的老师是 Paul Hegarty，在 Stanford 执教 10 年左右了。该课程创办了很多年，每当 Apple 推出了新技术，例如 Storyboard、SwiftUI，这个白胡子老爷爷就会迅速跟上，更新他的课程，实乃一 it 潮人。你可以去油管 Stanford 官方账号查看该课程，也可以看看 up 主转载的该课程，还上传了中文字幕、英文字幕、繁体字幕的双语版本。理论上来说，你只需要有面向对象编程及 Swift 语言的相关基础和了解，你就可以看懂该课程，适合想要学习 SwiftUI 入门的朋友。

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)



## 联系我们

[iOS摸鱼周报 第十一期](https://zhangferry.com/2021/05/16/iOSWeeklyLearning_11/)

[iOS摸鱼周报 第十二期](https://zhangferry.com/2021/05/22/iOSWeeklyLearning_12/)

[iOS摸鱼周报 第十三期](https://zhangferry.com/2021/05/30/iOSWeeklyLearning_13/)

[iOS摸鱼周报 第十四期](https://zhangferry.com/2021/06/06/iOSWeeklyLearning_14/)

[iOS摸鱼周报 第十五期](https://zhangferry.com/2021/06/14/iOSWeeklyLearning_15/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
