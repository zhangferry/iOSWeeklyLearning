# iOS 摸鱼周报 #58 | 周报改版，WWDC22 讲座集锦

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：在您的 App 中提供帐户删除选项
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：
> * 岗位推荐：

## 本期话题

### [在您的 App 中提供帐户删除选项](https://developer.apple.com/cn/support/offering-account-deletion-in-your-app "在您的 App 中提供帐户删除选项")

[@远恒之义](https://github.com/eternaljust)：苹果要求，自 2022 年 6 月 30 日起，如果您的 App 支持帐户创建，提交到 App Store 审核，必须支持用户在 App 中发起帐户删除，以避免审核延迟。

⚠️ 注意事项：
* 支持“通过 Apple 登录”的 App 应使用 Sign in with Apple REST API 来[撤销用户令牌](https://www.yuque.com/eternaljust/rpmt31/bxmc3d#khpAl "撤销用户令牌")。
* 如果 App 帐户删除流程是手动的（如在应用内申请删除账号，需要管理员后台审核），请告知用户删除帐户需要多长时间，并在删除完成时提供一条确认信息。
* 如何避免拥有自动续期订阅的用户在删除帐户后意外被 Apple 继续扣款？可提供[链接](https://apps.apple.com/account/subscriptions "打开用户管理订阅链接")来让用户管理取消自己的订阅。

## 本周学习

整理编辑：[JY](https://juejin.cn/user/1574156380931144)



## 内容推荐

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

1、[What’s the difference between any and some in Swift 5.7?](https://www.donnywals.com/whats-the-difference-between-any-and-some-in-swift-5-7/ "What’s the difference between any and some in Swift 5.7?") -- 来自：Donny Wals

[@Mimosa](https://juejin.cn/user/1433418892590136)：作者通过举例来说明了在 Swift 5.7 中你该如何选择 some 还是 any 关键词，阐述了他们之间的不同，同时谈了一下该如何正确的使用它们，以及未来可能在 Swift 6 中的表现。在作者的另一篇文章 [What are primary associated types in Swift 5.7?](https://www.donnywals.com/what-are-primary-associated-types-in-swift-5-7/) 中它也谈到了，在实际使用场景，例如关联类型的使用中，some 和 any 关键词对程序的影响。

2、[深入理解 Git 底层实现原理](http://chuquan.me/2022/05/21/understand-principle-of-git/ "深入理解 Git 底层实现原理") -- 来自：楚权

[@Mimosa](https://juejin.cn/user/1433418892590136)：大家平时都在使用 Git，但是其中的底层实现原理大家了解么？该文章作者从 Git 整体的架构出发，分层讲解了各层作用，主要谈了对象数据库的设计等。同时也给出了基于其原理的一个设计案例 —— CocoaPods Source 管理机制。文章整体写的通俗易懂，配图也简洁大方。

## 摸一下鱼

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

## 岗位推荐


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #57 | 周报改版，WWDC22 讲座集锦](https://mp.weixin.qq.com/s/e4ZbFBPqclgy7KyfxVyQZA)

[iOS 摸鱼周报 #56 | WWDC 进行时](https://mp.weixin.qq.com/s/ZyGV6WlFsZOX6Aqgrf1QRQ)

[iOS 摸鱼周报 #55 | WWDC 码上就位](https://mp.weixin.qq.com/s/zDhnOwOiLGJ_Nwxy5NBePw)

[iOS 摸鱼周报 #54 | Apple 辅助功能持续创新](https://mp.weixin.qq.com/s/6jdqa143Y5yr6lbjCuzlqA)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
