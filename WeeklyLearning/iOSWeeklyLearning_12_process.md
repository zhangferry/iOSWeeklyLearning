# iOS摸鱼周报 第十二期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 开发Tips




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

整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### Application Name

**地址**：

**软件状态**：

**使用介绍**



## 联系我们

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

[摸鱼周报第六期](https://zhangferry.com/2021/03/14/iOSWeeklyLearning_6/)

[摸鱼周报第七期](https://zhangferry.com/2021/03/28/iOSWeeklyLearning_7/)

[摸鱼周报第八期](https://zhangferry.com/2021/04/11/iOSWeeklyLearning_8/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)