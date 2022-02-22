# iOS摸鱼周报 第四十二期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * Tips：
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：Apple 将在 iPhone 上推出 Tap to Pay 功能，即可以通过简单的操作行为 -- 轻触，完成在商户端的付款过程。该功能通过 NFC 实现，非常安全，支持 Apple Pay、非接触式信用卡、借记卡以及其他数子钱包，这意味着 iPhone 将具备类似 POS 的功能，客户可以直接在商户的 iPhone 上刷信用卡进行消费。该功能仅 iPhone XS 及之后的机型支持。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Apple_Apple-Pay_Payment_inline.jpg.large_2x.jpg)

Stripe 将成为第一个在 iPhone 上向其商业客户提供 Tap to Pay 的支付平台。其他支付平台和应用程序将在今年晚些时候推出。

## 开发Tips

整理编辑：[zhangferry](https://zhangferry.com)

### 获取 Build Setting 对应的环境变量 Key

Xcode 的 build setting 里有很多配置项，这些配置项都有对应的环境变量，当我们要用脚本自定义的话就需要知道对应的环境变量 Key是哪个才好设置。比如下面这个 Header Search Paths

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220220215645.png)

其对应的 Key 是 `HEADER_SEARCH_PATHS`。那如何或者这个 Key 呢，除了网上查相关资料我们还可以通过 Xcode 获取。

#### 方法一（由@CodeStar提供）

选中该配置项，展开右部侧边栏，选中点击帮助按钮就能够看到这个配置的说明和对应的环境变量名称。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220220220200.png)

#### 方法二

选中该配置，按住 Option 键，双击该配置，会出现一个描述该选项的帮助卡片，这个内容与上面的帮助侧边栏内容一致。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220220220534.png)

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)




## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐


整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### EasyFind 

**地址**：https://easyfind.en.softonic.com/mac

**软件状态**：免费

**软件介绍**：

小而强大的文件搜索应用, 媲美`windows`下的`Everything`。

![EasyFind](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/easyfind-easyfind.png)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
