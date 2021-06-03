# iOS摸鱼周报 第十四期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 开发Tips

### 包大小优化的一些方案

![包大小优化脑图](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/%E5%AE%89%E8%A3%85%E5%8C%85%E7%98%A6%E8%BA%AB.jpeg)

参考链接：

[头条包大小优化](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI1MzYzMjE0MQ==&action=getalbum&album_id=1665528287604817930&scene=173&from_msgid=2247487459&from_itemidx=1&count=3&nolastread=1#wechat_redirect)

[Apple Build settings reference](https://help.apple.com/xcode/mac/current/#/itcaec37c2a6?sub=dev881878d77)

[iOS IPA 包体积优化](https://blog.jonyfang.com/2019/11/10/2019-11-10-ios-ipa/)


整理编辑：[人魔七七](https://github.com/renmoqiqi)


## 那些Bug


## 编程概念

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)

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
	- 性能和几乎和原生相当
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
    点评：Flutter全平台制霸，RN局限于移动端；Flutter社区更活跃，RN更稳定；性能方面RN更依赖于iOS或android的原生实现，Flutter则依赖自己的渲染框架；最后，跨平台方案需谨慎。
- RN集成方式：
    - 需要用到的工具或资源：Node、Watchman、Xcode 和 CocoaPods
    - 安装脚本（需耗时✨  Done in 178.50s.）： https://github.com/zhangferry/iOSWeeklyLearning/tree/main/Script/rn-setup.sh

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



## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

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
