# iOS摸鱼周报 第十四期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 开发Tips

### 包大小优化的一些方案

![包大小优化脑图](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/%E5%AE%89%E8%A3%85%E5%8C%85%E7%98%A6%E8%BA%AB.jpeg)

### 参考链接

- [头条包大小优化](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI1MzYzMjE0MQ==&action=getalbum&album_id=1665528287604817930&scene=173&from_msgid=2247487459&from_itemidx=1&count=3&nolastread=1#wechat_redirect)

- [Apple Build settings reference](https://help.apple.com/xcode/mac/current/#/itcaec37c2a6?sub=dev881878d77)

- [iOS IPA 包体积优化](https://blog.jonyfang.com/2019/11/10/2019-11-10-ios-ipa/)


整理编辑：[人魔七七](https://github.com/renmoqiqi)


## 那些Bug
整理编辑：[FBY展菲](https://github.com/fanbaoying)

### 1. 问题背景

iOS 开发者账号续费虽然流程有点繁琐且只支持信用卡付款，但是每年都能顺利的续费成功，今年续费磕磕绊绊试了很多次都不成功，总是提示“你的支付授权失败。请核对你的信息并重试，或尝试其他支付方式。请联系你的银行了解更多信息。”，如下图：

![](https://upload-images.jianshu.io/upload_images/2829694-884d5c88877beef7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下面主要分析如何解决 iOS 开发者账号续费时出现 “你的支付授权失败...” 的问题。

### 2. 问题分析

在网上寻找类似问题并做以下确认和尝试

1. 尝试其他不同银行的信用卡。因为公司只有一张支持外汇的信用卡并且都是往年续费使用的，结果不行换了其他的信用卡依旧不行。

2. 信用卡需要支持双币种。使用的每张信用卡都是 Visa + Mastercard，支持人民币和美元。

3. 确认账单地址和所使用信用卡信息一致。这个问题之前真的没有注意，于是每张卡都确认了账单地址然后重试，依然失败。

4. 可能是系统问题，换个时间重试。前后试了1个多星期，并且试了白天和晚上，加上试了vpn，都是一样的结果。

5. 电话联系 Apple 客服。给到的回复是苹果系统续费出现问题，建议有两个，一个是通过客服进行线下支付，另一个是尝试使用同时拥有银联 + Visa / Mastercard 的信用卡续费。

### 3. 问题解决

##### 3.1 线下支付

通过客服进行线下支付和自己在线上支付有以下几点不同：

1. 线上是688元人民币，线下订单因为是提到美国总部，所以支付99美元。

2. 线下支付无法提供发票。

3. 因为属于境外支付美元，信用卡的所属银行还会扣除相应的费用，但是根据银行和卡的类型不同，具体费用也不同。

##### 3.2 线下支付

1. 确保我们的信用卡，同时支持 银联和Visa 或者 银联和MasterCard。

![](https://upload-images.jianshu.io/upload_images/2829694-de2136e83232bbf0.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2. 确保信用卡开通了网上支付功能

3. 确保信用卡开通了境外支付功能，有的卡默认开通，有的没有开通（我的交行信用卡是默认开通了）

4. 账单联系人那里要和持卡人信息填写一致

参考：[解决 iOS 开发者账号续费 “你的支付授权失败...” 问题 - 展菲](https://mp.weixin.qq.com/s/P6itRl56QD3iRqNv92VXYQ "解决 iOS 开发者账号续费 “你的支付授权失败...” 问题")

## 编程概念

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)，[我是熊大](https://juejin.cn/user/1151943916921885/posts)

### React Native

React Native 是一个使用React和应用平台的原生功能来构建 Android 和 iOS 应用的开源框架。通过 React Native，可以使用 JavaScript 来访问移动平台的 API，以及使用 React 组件来描述 UI 的外观和行为：一系列可重用、可嵌套的代码。

- 诞生年份：2015 年 9 月
- 组织：Facebook 
- 口号：Learn Once,Write Anywhere.
- 本质：虽然使用的是 JavaScript 语言编写的代码，但是实际上是调用了原生的 API 和原生的 UI 组件
- 特点：
	- 跨平台（JavaScript框架）虚拟 DOM
	- 热更新，iOS审核有限制
	- 对web开发者友好，上手快
	- 性能几乎和原生相当
- React Native 的不足：
	- 由于 React Native 和原生交互依赖的只有一个 Bridge，而且 JS 和 Native 交互是异步的，所以对需要和 Native 大量实时交互的功能可能会有性能上的不足，比如动画效率，性能是不如原生的。

	- React Native 始终是依赖原生的能力，所以摆脱不了对原生的依赖，相对 Flutter 的自己来画 UI 来说，React Native 显得有些尴尬。
- RN vs Flutter
    - RN: 
        - star: 169k,  
        - issues: 10000+
        - fork: 34.1k
        - 生日：2015 年 9 月
        - 原作者：Facebook
        - 最底层依旧调用的是原生框架
        - 支持平台：iOS和Android
    - Flutter:
        - star: 121k,  
        - issues: 40000+
        - fork: 17.1k
        - 生日：2017 年 5 月
        - 原作者：Google
        - 自己的渲染引擎
        - 支持平台：iOS、Android、Windows、Web、macOS 和 Linux 
    点评：Flutter全平台制霸，RN局限于移动端；Flutter社区更活跃，RN更稳定；性能方面RN更依赖于iOS或Android的原生实现，Flutter则依赖自己的渲染框架；最后，跨平台方案需谨慎。
- RN集成方式：
    - 需要用到的工具或资源：Node、Watchman、Xcode 和 CocoaPods
    - 安装脚本（需耗时✨  Done in 178.50s.）： https://github.com/zhangferry/iOSWeeklyLearning/tree/main/Script/rn-setup.sh
    - 脚本执行完毕后，会自动打开Xcode以及模拟器

```
#使用Homebrew来安装 Node 和 Watchman
brew install node
brew install watchman

# 使用nrm工具切换淘宝源
npx nrm use taobao

# 如果之后需要切换回官方源可使用
npx nrm use npm

# 安装 yarn
npm install -g yarn

echo "--->>> 👍 下载完毕"

# 创建项目
npx react-native init MoyuDemo
echo "--->>> 👍 创建项目"

cd MoyuDemo

yarn ios
```
- 参考资料
	- React Native 中文网 ：https://reactnative.cn/docs/getting-started
	- React Native 原理与实践：https://zhuanlan.zhihu.com/p/343519887


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)

本期文章主题`APP性能`

[揭秘 APM iOS SDK 的核心技术](https://github.com/aozhimin/iOS-APM-Secrets "揭秘 APM iOS SDK 的核心技术") -- 来自github:aozhimin

[iOS-Monitor-Platform](https://github.com/aozhimin/iOS-Monitor-Platform "iOS-Monitor-Platform") -- 来自github:aozhimin

以上两篇文章来自aozhimin，作者在介绍性能监控方案的同时也透露了如何利用逆向技术分析他人的技术方案。

[美团外卖iOS App冷启动治理](https://tech.meituan.com/2018/12/06/waimai-ios-optimizing-startup.html "美团外卖iOS App冷启动治理") -- 来自美团技术团队

美团早些年的技术文章，文中的很多内容依旧不过时。

[抖音品质建设 - iOS启动优化《实战篇》](https://mp.weixin.qq.com/s/ekXfFu4-rmZpHwzFuKiLXw  "抖音品质建设 - iOS启动优化《实战篇》")-- 微信公众号：字节跳动技术团队

本文介绍的都是抖音遇到的具体问题，很具有参考性。

[从探索到实践，iOS动态库懒加载实录](https://mp.weixin.qq.com/s/g5FKnOcW6KonqBSW8XO9Jw "从探索到实践，iOS动态库懒加载实录") -- 微信公众号：58技术

上文中提到了非常规方案--动态库懒加载。本文则介绍了58同城APP中如何对部分代码修改为动态库并实现懒加载的。目前动态库懒加载在58集团有大量的应用。

[抖音品质建设 - iOS 安装包大小优化实践篇](https://mp.weixin.qq.com/s/LSP8kC09zjb-sDjgZaikbg "抖音品质建设 - iOS 安装包大小优化实践篇") -- 微信公众号：字节跳动技术团队

我们统计到58APP iOS12及以下还是有相当一部用户的。文中提到的段迁移实践后确实起到了不小的下载优化作用。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

## 工具推荐

### 柠檬清理
 整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

**地址**: https://lemon.qq.com/

**软件状态**: 免费 

**软件介绍**

腾讯柠檬清理Lite版-重点聚焦清理功能，包含系统/应用垃圾清理、大文件清理、重复文件清理、相似照片清理4个方面，当前还支持在状态栏上查看当前网速信息，帮助你实时了解Mac状况。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/16227749924686.jpg)


**核心功能**


* 便捷好用的状态栏清理

    * 可直接在状态栏上查看实时网速，方便及时了解网速变化。支持快速清理，轻轻一点，不留垃圾。

* 系统/应用垃圾清理

    * 磁盘空间将满，却无法区分垃圾和重要文件，想清理无从下手。腾讯柠檬清理帮你深度智能扫描分析各类文件，针对市面上微信、QQ、Xcode、Sketch等百款应用逐一定制清理方案，提供专业建议，贴心归类为易理解的选项，一键勾选清理。还支持强力删除废纸篓里的顽固文件，全面提升系统运行速度！
 
* 大文件清理
    * 帮你快速全面查找占用超过50M的大文件，支持预览图片、视频，一键定位文件位置，最大限度释放磁盘空间；
 
* 重复文件清理
    * 智能比对文件内容及信息，归类选出百分百相同的文件，支持预览，快速查看文件位置，高效清理重复文件，保持Mac持久清爽；


## 联系我们

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

[摸鱼周报第六期](https://zhangferry.com/2021/03/14/iOSWeeklyLearning_6/)

[摸鱼周报第七期](https://zhangferry.com/2021/03/28/iOSWeeklyLearning_7/)

[摸鱼周报第八期](https://zhangferry.com/2021/04/11/iOSWeeklyLearning_8/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
