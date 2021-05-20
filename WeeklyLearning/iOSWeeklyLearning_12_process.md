# iOS摸鱼周报 第十二期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 开发Tips

1、[普通技术人的成长路径 - 一位客户端老兵的经验之谈](https://mp.weixin.qq.com/s/IrSQyyc0J3SXBuWs9M3SYA "普通技术人的成长路径 - 一位客户端老兵的经验之谈") -- 来自公众号： 老司机周报

青衫不负踏歌行，莫忘曾经是书生。很认同其中的一些观点和思考。不知道大家是否跟我一样，存在各种各样的焦虑：客三消、内卷、35岁危机... 抽空可以读读此文，让内心的焦躁得到暂时的缓解。

2、[Swift 汇编（一）Protocol Witness Table 初探](https://mp.weixin.qq.com/s/lRKVZk5c1tX7AtWVgD56OA "Swift 汇编（一）Protocol Witness Table 初探") -- 来自公众号：Swift 社区

之前关注过Protocol Witness Table，但是没有抽时间去了解。很有深度的一篇文章，值得阅读，如果有时间可以跟着作者的思路亲自动手调试下。

3、[Wakeup in XNU](https://mp.weixin.qq.com/s/8OBAmyCLa6_eFYqIJgoCQw "Wakeup in XNU") -- 来自公众号： 网易云音乐大前端团队

去年年底的时候在群里帮一位同学解析了一个weakup日志。weakup日志看起来比较奇怪，可能很多同学并没有遇到类似的问题。通过这篇专业的文章可以让大家对weakup有个初步了解。

4、[快手客户端稳定性体系建设](https://blog.csdn.net/Kwai_tech/article/details/107964806 "快手客户端稳定性体系建设") -- 来自CSDN：快手技术团队

这里面就提到了快手遇到了weakup崩溃以及如何定位相关问题的。

5、[iOS技能拓展 初识符号与链接](https://juejin.cn/post/6961576195332309006 "iOS技能拓展 初识符号与链接") -- 来自掘金：我是好宝宝

熟悉Mach-O与链接会成为面试的加分项，正在面试的同学可以关注下。

6、[了解和分析iOS Crash](https://segmentfault.com/a/1190000016411126 "了解和分析iOS Crash") -- 来自segmentfault：腾讯WeTest


iOS crash相关很好很全面的文章，作者加了注解帮助我们理解，已收藏。


## 那些Bug

### 解决 iOS 14.5 UDP 广播 sendto 返回 -1

整理编辑：[FBY展菲](https://juejin.cn/user/3192637497025335/posts)

### 1. 问题背景

1. 手机系统升级到 iOS 14.5 之后，UDP 广播发送失败
2. 项目中老版本使用到 socket 
3. 项目中新版本使用 CocoaAsyncSocket
4. 两种 UDP 发包方式都会报错 No route to host

**报错具体内容如下：**

```
sendto: -1
client: sendto fail, but just ignore it
: No route to host
```

### 2. 问题分析

##### 2.1  sendto 返回 -1 问题排查

我们知道发送广播 sendto 返回 -1，正常情况sendto 返回值大于 0 。
首先判断 socket 连接是否建立

```
self._sck_fd4 = socket(AF_INET,SOCK_DGRAM,0);
if (DEBUG_ON) {
     NSLog(@"client init() _sck_fd4=%d",self._sck_fd4);
}
```
self._sck_fd4 打印：

```
server init(): _sck_fd4=12
```

socket 连接正常，接下来判断数据发包

```
sendto(self._sck_fd4, bytes, dataLen, 0, (struct sockaddr*)&target_addr, addr_len) = -1
```

数据发送失败

##### 2.2  增加 NSLocalNetworkUsageDescription 权限

1. Info.plist 添加 `NSLocalNetworkUsageDescription`

2. 发送一次UDP广播，触发权限弹框，让用户点击好，允许访问本地网络。

发现问题依旧存在

##### 2.3 发送单播排查

由于项目中发送广播设置的 hostName 为 255.255.255.255，为了排查决定先发送单播看是否能成功。

将单播地址改为 192.168.0.101 之后发现是可以发送成功的，然后在新版本 CocoaAsyncSocket 库中发送单播也是可以成功的。

UDP 广播推荐使用 192.168.0.255 ，将广播地址改了之后，问题解决了，设备可以收到 UDP 广播数据。

### 3. 问题解决

由于 192.168.0.255 广播地址只是当前本地地址，App 中需要动态改变前三段 192.168.0 本地地址，解决方法如下：

```
NSString *localInetAddr4 = [ESP_NetUtil getLocalIPv4];
NSArray *arr = [localInetAddr4 componentsSeparatedByString:@"."];
NSString *deviceAddress4 = [NSString stringWithFormat:@"%@.%@.%@.255",arr[0], arr[1], arr[2]];
```

发包过滤，只需要过滤地址最后一段是否为 255

```
bool isBroadcast = [targetHostName hasSuffix:@"255"];
```


参考：[解决 iOS 14.5 UDP 广播 sendto 返回 -1 - 展菲](https://mp.weixin.qq.com/s/2SmIYq6qCTFXHDL3j6LoeA "解决 iOS 14.5 UDP 广播 sendto 返回 -1")

## 编程概念

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)




## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)



## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### [Swift by Sundell](https://www.swiftbysundell.com/)

[John Sundell](https://twitter.com/johnsundell) 的博客网站（同时他也是 [Publish](https://github.com/JohnSundell/Publish) 的作者），网站主要的内容是关于 `Swift` 开发的文章、播客和新闻。其文章清晰易懂，难度范围也比较广，各个水平的开发者应该都能找到适合自己水平的文章。其网站上部分关于 `SwiftUI` 的文章中，还能实时预览 `SwiftUI` 代码所对应的运行效果，贼舒服😈。

### [100 Days of SwiftUI from Paul Hudson](https://www.hackingwithswift.com/100/swiftui)

[Paul Hudson](https://twitter.com/twostraws) 的一个免费的 `SwiftUI` 课程，比较基础，是一个绝佳的新手教程。他会简单教一下 `Swift` 语言，然后用 `SwiftUI` 开始构建 iOS App。课程对应的网站 [Hacking with Swift](https://www.hackingwithswift.com/) 上也有很多 `iOS` 开发中比较基础的教程和解答，总的来说比较适合刚接触 `iOS` 开发的人群🤠。



## 工具推荐
 
### SwiftFormat for Xcode
整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

**地址**：https://github.com/nicklockwood/SwiftFormat

**软件状态**：免费 

**使用介绍**

SwiftFormat 是用于重新格式化 Swift 代码的命令行工具。它会在保持代码意义的前提下，将代码进行格式化

很多项目都有固定的代码风格，统一的代码规范有助于项目的迭代和维护，而有的程序员却无视这些规则。同时，手动强制的去修改代码的风格又容易出错，而且没有人愿意去做这些无聊的工作。

如果有自动化的工具能完成这些工作，那几乎是最完美的方案了。在代码 review 时就不需要每次都强调无数遍繁琐的代码格式问题了

 

 ![](https://github.com/nicklockwood/SwiftFormat/blob/master/EditorExtension/Application/Assets.xcassets/AppIcon.appiconset/icon_256x256.png)

### Notion
整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

**地址**: https://www.notion.so/desktop

**软件状态**：个人免费，团队收费

**使用介绍**

Notion是一款极其出色的个人笔记软件，它将“万物皆对象”的思维运用到笔记中，让使用者可以天马行空地去创造、拖拽、链接；Notion不仅是一款优秀的个人笔记软件，其功能还涵盖了项目管理、wiki、文档等等

##### 核心功能
* 支持导入丰富的文件和内容 
* 内置丰富的模板
* 简洁的用户界面、方便的拖动和新建操作
* 支持Board视图，同时可以添加任意数量的其他类型视图并自定义相关的过滤条件
* 复制图片即完成上传，无需其他图床 
* 保存历史操作记录并记录相关时间
* 强大的关联功能，比如日历与笔记，笔记与文件以及网页链接

![](https://www.notion.so/cdn-cgi/image/f=auto,w=3840,q=100/front-static/pages/work/carousel-desktop/tasks-v5/en-US.png)



## 联系我们

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

[摸鱼周报第六期](https://zhangferry.com/2021/03/14/iOSWeeklyLearning_6/)

[摸鱼周报第七期](https://zhangferry.com/2021/03/28/iOSWeeklyLearning_7/)

[摸鱼周报第八期](https://zhangferry.com/2021/04/11/iOSWeeklyLearning_8/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
