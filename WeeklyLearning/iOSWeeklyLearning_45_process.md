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

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[FBY展菲](https://github.com/fanbaoying)

### Swift 实用工具 — SwiftLint 

#### SwiftLint 介绍

`SwiftLint` 是一个实用工具，用于实现 Swift 的风格。 在 Xcode 项目构建阶段，集成 SwiftLint 很简单，构建阶段会在编译项目时自动触发 SwiftLint。

遗憾的是，目前无法轻松地将 `SwiftLint` 与 `Swift Packages` 集成，Swift Packages 没有构建阶段，也无法自动运行脚本。

下面介绍如何在 Xcode 中使用 `post action` 脚本在成功编译 Swift Package 后自动触发 SwiftLint。

`SucceedsPostAction.sh` 是一个 bash 脚本，用作 Xcode 中的 “Succeeds” 发布操作。当你编译一个 Swift 包时，这个脚本会自动触发 `SwiftLint`。

#### SwiftLint 安装

1. 在 Mac 上下载脚本 `SucceedsPostAction.sh`。

2. 确保脚本具有适当的权限，即运行 `chmod 755 SucceedsPostAction.sh`。

3. 如果要使用自定义 SwiftLint 规则，请将 `.swiftlint.yml` 文件添加到脚本旁边。

4. 启动 Xcode 13.0 或更高版本

5. 打开 Preferences > Locations 并确保 `Command Line Tools` 设置为 Xcode 版本

6. 打开 Preferences > Behaviors > Succeeds

7. 选择脚本 `SucceedsPostAction.sh`

![](https://files.mdnice.com/user/17787/7cce4fc6-82bc-4c66-b499-6541b75ca08c.png)

就是这样：每次编译 Swift 包时，`SucceedsPostAction.sh` 都会运行 SwiftLint。

**演示**

![](https://files.mdnice.com/user/17787/89f7a065-f200-4158-a701-99b217c38a4a.gif)

#### 存在一些问题

在 Xcode 中运行的 `post action` 脚本无法向 Xcode 构建结果添加日志、警告或错误。因此，`SucceedsPostAction.sh` 在 Xcode 中以新窗口的形式打开一个文本文件，其中包含 SwiftLint 报告列表。没有深度集成可以轻松跳转到 SwiftLint 警告。

**Swift 5.6**

请注意，由于[SE-0303: Package Manager Extensible Build Tools](https://github.com/apple/swift-evolution/blob/main/proposals/0303-swiftpm-extensible-build-tools.md "Package Manager Extensible Build Tools")，Swift 5.6（在撰写本文时尚不可用）可能会有所帮助。集成 SE-0303 后，不再需要此脚本。

参考：[Swift 实用工具 — SwiftLint - Swift社区](https://mp.weixin.qq.com/s/WMCwt6KjiBV2ddES-rQtyw)


## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)




## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐


整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### nginxedit 

**地址**：https://www.nginxedit.cn/

**软件状态**：免费

**软件介绍**：

`Nginx`在线配置生成工具，配置高性能，安全和稳定的`Nginx`服务器的最简单方法。

![nginxedit](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Nginx%E5%9C%A8%E7%BA%BF%E9%85%8D%E7%BD%AE%E7%94%9F%E6%88%90%E5%B7%A5%E5%85%B7.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
