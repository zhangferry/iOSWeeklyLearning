# iOS摸鱼周报 第十四期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 开发Tips

### 包大小优化的一些方案

整理编辑：[人魔七七](https://github.com/renmoqiqi)

![包大小优化脑图](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/%E5%AE%89%E8%A3%85%E5%8C%85%E7%98%A6%E8%BA%AB.jpeg)

因篇幅问题仅展示一张梳理过后的图片，完整文章可以查看小专栏的这篇：https://xiaozhuanlan.com/topic/6147250839。

参考链接：[头条包大小优化](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI1MzYzMjE0MQ==&action=getalbum&album_id=1665528287604817930&scene=173&from_msgid=2247487459&from_itemidx=1&count=3&nolastread=1#wechat_redirect "头条包大小优化")、[Apple Build settings reference](https://help.apple.com/xcode/mac/current/#/itcaec37c2a6?sub=dev881878d77 "Apple Build settings reference")、[iOS IPA 包体积优化](https://blog.jonyfang.com/2019/11/10/2019-11-10-ios-ipa/ "iOS IPA 包体积优化")


## 那些Bug
整理编辑：[FBY展菲](https://github.com/fanbaoying)

###  iOS 开发者账号续费 “你的支付授权失败...” 问题

**问题背景**

iOS 开发者账号续费虽然流程有点繁琐且只支持信用卡付款，但是每年都能顺利的续费成功，今年续费磕磕绊绊试了很多次都不成功，总是提示“你的支付授权失败。请核对你的信息并重试，或尝试其他支付方式。请联系你的银行了解更多信息。”，如下图：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210605174833.png)

下面主要分析如何解决 iOS 开发者账号续费时出现 “你的支付授权失败...” 的问题。

**问题分析**

在网上寻找类似问题并做以下确认和尝试：

1. 尝试其他不同银行的信用卡。因为公司只有一张支持外汇的信用卡并且都是往年续费使用的，结果不行换了其他的信用卡依旧不行。
2. 信用卡需要支持双币种。使用的每张信用卡都是 Visa + Mastercard，支持人民币和美元。
3. 确认账单地址和所使用信用卡信息一致。这个问题之前真的没有注意，于是每张卡都确认了账单地址然后重试，依然失败。
4. 可能是系统问题，换个时间重试。前后试了 1 个多星期，并且试了白天和晚上，加上试了 vpn，都是一样的结果。
5. 电话联系 Apple 客服。给到的回复是苹果系统续费出现问题，建议有两个，一个是通过客服进行线下支付，另一个是尝试使用同时拥有银联 + Visa / Mastercard 的信用卡续费。

**两种解决方案**

1、线下支付

通过客服进行线下支付和自己在线上支付有以下几点不同：

* 线上是 688 元人民币，线下订单因为是提到美国总部，所以支付 99 美元。
* 线下支付无法提供发票。
* 因为属于境外支付美元，信用卡的所属银行还会扣除相应的费用，但是根据银行和卡的类型不同，具体费用也不同。

2、线上支付

* 确保我们的信用卡，同时支持银联 + Visa / Mastercard。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210605174707.png)

* 确保信用卡开通了网上支付功能
* 确保信用卡开通了境外支付功能，有的卡默认开通，有的没有开通（我的交行信用卡是默认开通了）
* 账单联系人那里要和持卡人信息填写一致

参考：[解决 iOS 开发者账号续费 “你的支付授权失败...” 问题 - 展菲](https://mp.weixin.qq.com/s/P6itRl56QD3iRqNv92VXYQ "解决 iOS 开发者账号续费 “你的支付授权失败...” 问题")

## 编程概念

从本期开始，编程概念模块将介绍前端相关的多个概念。本期带来的内容是对 `React`、`React Native`、`Vue` 的介绍。如有错误，欢迎指正。

### 关于前端

通常我们说的前端有两个含义，一个是特指 Web 前端，其跟移动端平级；另一个指大前端，其包含移动端。这里咱们取的含义是 Web 前端。

Web 前端的主要技术是围绕 HTML/CSS、 JavaScript 发展的。在过去的十年里，得益于 JS，网页变得更加动态化和强大，我们把很多的服务端代码放到了浏览器中，这样就产生了成千上万行的 JS 代码，它们链接了各式各样的 HTML 和 CSS 文件，但缺乏正规的组织形式，这就是为什么越来越多的开发者使用 JS 框架来组织代码，诸如 React、Vue、Angular 等。

### 什么是 React

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210605211826.png)

内容整理：[zhangferry](https://zhangferry.com)

[React](https://reactjs.org/) 是由 Facebook 开发的用于构建用户界面的 JavaScript 库，其已开源在 Github，拥有 169k 的超高 star 数，在前端领域使用极广泛。

它有这三大特性：

* 声明式：React 使创建交互式 UI 变得轻而易举，为你应用的每一个状态设计简洁的视图，当数据变动时 React 能高效更新并渲染合适的组件。
* 组件化：构建管理自身状态的封装组件，然后对其组合成复杂的 UI。
* 一次学习，扩平台编写：无论你现在使用什么技术栈，在无需重写现有代码的前提下，都可以通过引入 React 来开发新功能。React 还可以使用 Node 进行服务器渲染，或使用 [React Native](https://reactnative.dev/) 开发原生移动应用。

我们来看一个官网的例子来简单了解下 React 的使用，我们的目的是要实现一个前端 Markdown 渲染的效果，上面是输入框，下面是渲染的 HTML 效果，这里使用一个名为 **remarkable** 的外部库，代码如下：

```java
// React.Component 就是内置组件，其有一系列组件
class MarkdownEditor extends React.Component {
  // 构造函数，类似init
  constructor(props) {
    super(props);
    // 外部库
    this.md = new Remarkable();
    // 绑定自身变化
    this.handleChange = this.handleChange.bind(this);
    // 默认内容
    this.state = { value: 'Hello, **world**!' };
  }
	// 监听输入框的变化
  handleChange(e) {
    this.setState({ value: e.target.value });
  }
	// 渲染出的html
  getRawMarkup() {
    return { __html: this.md.render(this.state.value) };
  }
	// 界面
  render() {
    return (
      <div className="MarkdownEditor">
        <h3>Input</h3>
        <label htmlFor="markdown-content">
          Enter some markdown
        </label>
        <textarea
          id="markdown-content"
          onChange={this.handleChange}
          defaultValue={this.state.value}
        />
        <h3>Output</h3>
        <div
          className="content"
          dangerouslySetInnerHTML={this.getRawMarkup()}
        />
      </div>
    );
  }
}
// 渲染
ReactDOM.render(
  <MarkdownEditor />,
  document.getElementById('markdown-example')
);
```

### 什么是 React Native

内容整理：[我是熊大](https://juejin.cn/user/1151943916921885/posts)

[React Native](https://reactnative.dev/) 是一个使用 `React` 和应用平台的原生功能来构建 Android 和 iOS 应用的开源框架，其已经不是一个 Web 前端框架，而是一个移动端框架。通过 React Native，可以使用 JavaScript 来访问移动平台的 API，以及使用 React 组件来描述 UI 的外观和行为：一系列可重用、可嵌套的代码。通过一张图简单了解下 React Native 在移动开发中的架构：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210605200722.png)

其具有这些特点：跨平台（JavaScript 框架）虚拟 DOM、热更新，iOS 审核有限制、对 Web 开发者友好，上手快，性能几乎和原生相当。

React Native 的不足：
- 由于 React Native 和原生交互依赖的只有一个 Bridge，而且 JS 和 Native 交互是异步的，所以对于需要和 Native 大量实时交互的功能可能会有性能上的不足，比如动画效率，性能是不如原生的。
- React Native 始终是依赖原生的能力，所以摆脱不了对原生的依赖，相对 Flutter 的自己来画 UI 来说，React Native 显得有些尴尬。

引入 React Native 是基于 JavaScript 实现的，所以要在 iOS 端使用它的话，我们就需要安装 `Node.js`，并利用 Node 工具安装 React Native。以下介绍一个简单步骤：
```bash
# 使用 Homebrew 来安装 Node
brew install node

# 安装 yarn
npm install -g yarn

# 创建项目
npx react-native init MoyuDemo

cd MoyuDemo

yarn ios
```
参考资料：[React Native 中文网](https://reactnative.cn/docs/getting-started "React Native 中文网")，[React Native 原理与实践](https://zhuanlan.zhihu.com/p/343519887 "React Native 原理与实践")

### 什么是 Vue

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210605011045.png)

内容整理：[师大小海腾](https://juejin.cn/user/782508012091645)

[Vue](https://cn.vuejs.org/)（读音 /vjuː/）即 Vue.js。作者尤雨溪曾在知乎回答到，Vue 之所以叫 Vue，是因为它是个视图层库，而 vue 是 view 的法语。其是一套用于构建用户界面的**渐进式** JS 框架。

**渐进式的含义是它被设计为可以自底向上逐层应用。**

这是 Vue 与其他 JS 框架最大的不同。渐进式框架简单理解就是：你可以只用我的一部分，而非必须用我的全部；你可以仅将我作为应用的一部分嵌入，而非必须全部使用。Vue 支持你根据实际需求，在不同的阶段使用 Vue 中不同的功能，用最小最快的成本一步步搭建应用，不断渐进，而不是要求你一下子用上全家桶（vue-cli、vue-router、vuex 等）。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210605012155.png)

你可以看看：[Vue 作者尤雨溪：Vue 2.0，渐进式前端解决方案](https://mp.weixin.qq.com/s?__biz=MzUxMzcxMzE5Ng==&mid=2247485737&idx=1&sn=14fe8a5c72aaa98c11bf6fc57ae1b6c0&source=41#wechat_redirect "Vue作者尤雨溪：Vue 2.0，渐进式前端解决方案")

**Vue 的核心库只关注视图层，通过尽可能简单的 API 实现响应的数据绑定和组合的视图组件**

在 HTML 中，DOM 就是视图，我们把 HTML 中的 DOM 与其他的部分独立开来划分出一个层次，这个层次就叫做视图层。如果页面元素很多，数据和视图像传统开发一样全部混合在 HTML 中话就很难维护，因此我们要把视图层抽取出来并且单独去关注它。Vue 只关注视图层，是一个构建数据的视图集合。

Vue 支持数据的双向绑定。即数据变化驱动视图更新，视图更新也会驱动数据变化。而我们只需要通过简单的 API 即可实现这种绑定关系。

Vue 允许你将一个网页分割成多个可复用的组件，每个组件都包含属于自己的 HTML、CSS、JS 以用来渲染网页中相应的地方，然后将这些组件自由组合成完整的网页。

**Vue 具有易用、灵活、高效的特点**

- 易用：在有 HTML、CSS、JavaScript 的基础上，可以快速上手
- 灵活：不断繁荣的生态系统，可以在一个库和一套完整框架之间自如伸缩
- 高效：20kB min+gzip 运行大小，超快虚拟 DOM，最省心的优化

**一个例子**

我们来看一个使用 Vue 写出来的小例子：一个输入框，一个文本，文本能够根据输入框内容的变化而变化：

HTML代码：

```html
<div id="app-6">
  <p>{{ message }}</p>
 	<!-- Vue 提供了 v-model 指令，它能轻松实现表单输入和应用状态之间的双向绑定 -->
  <input v-model="message">
</div>
```

JS 代码：

```javascript
var app6 = new Vue({
  el: '#app-6',
  data: {
    message: 'Hello Vue!'
  }
})
```


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)

本期文章主题 `APP 性能`

[揭秘 APM iOS SDK 的核心技术](https://github.com/aozhimin/iOS-APM-Secrets "揭秘 APM iOS SDK 的核心技术") -- 来自 github:aozhimin

[iOS-Monitor-Platform](https://github.com/aozhimin/iOS-Monitor-Platform "iOS-Monitor-Platform") -- 来自 github:aozhimin

以上两篇文章来自 aozhimin，作者在介绍性能监控方案的同时也透露了如何利用逆向技术分析他人的技术方案。

[美团外卖iOS App冷启动治理](https://tech.meituan.com/2018/12/06/waimai-ios-optimizing-startup.html "美团外卖iOS App冷启动治理") -- 来自美团技术团队

美团早些年的技术文章，文中的很多内容依旧不过时。

[抖音品质建设 - iOS启动优化《实战篇》](https://mp.weixin.qq.com/s/ekXfFu4-rmZpHwzFuKiLXw  "抖音品质建设 - iOS启动优化《实战篇》")-- 微信公众号：字节跳动技术团队

本文介绍的都是抖音遇到的具体问题，很具有参考性。

[从探索到实践，iOS动态库懒加载实录](https://mp.weixin.qq.com/s/g5FKnOcW6KonqBSW8XO9Jw "从探索到实践，iOS动态库懒加载实录") -- 微信公众号：58技术

上文中提到了非常规方案--动态库懒加载。本文则介绍了 58同城APP 中如何对部分代码修改为动态库并实现懒加载的。目前动态库懒加载在 58集团 有大量的应用。

[抖音品质建设 - iOS 安装包大小优化实践篇](https://mp.weixin.qq.com/s/LSP8kC09zjb-sDjgZaikbg "抖音品质建设 - iOS 安装包大小优化实践篇") -- 微信公众号：字节跳动技术团队

我们统计到 58APP iOS12 及以下还是有相当一部分用户的。文中提到的段迁移实践后确实起到了不小的下载优化作用。

[揭秘苹果应用审核团队（史上最全版）](https://juejin.cn/post/6970363897668698148/ "揭秘苹果应用审核团队（史上最全版）") -- 掘金：37手游iOS技术运营团队

[@iHTCboy](https://github.com/iHTCboy)：史上最全版：揭秘苹果应用审核团队，告诉你 App Store 的由来，是怎样发展到今天这样辉煌，如何自动化：机器审核+人工审核？审核速度是怎么从 7-10 天，提升到如今只需要 48 小时的？

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### WWDC NOTES

地址：https://www.wwdcnotes.com/

这是国外一个记录 WWDC 笔记的社区，致力于收集所有苹果的 WWDC 视频的笔记和文章。每年 WWDC 的新内容数量惊人，观看所有 WWDC 视频需要数百个小时。但有时观看这些视频也是了解某些新技术如何运作、如何使用的唯一途径。WWDC NOTES 网站可以作为对所展示内容的快速回顾、作为参考、甚至单纯是作为一种节省时间的方法。欢迎每个人对 WWDC NOTES 做出贡献👏！

### Newbie Security List

地址：https://github.com/findneo/Newbie-Security-List

一个关于网络安全学习资料的 github 仓库。其中包含网络安全相关的博客、工具、电子书籍资料、在线知识库、在线漏洞库、本地搭建教学、相关文档以及相关练习平台，目前已经获 430 🌟了。

## 工具推荐

### 柠檬清理
 整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

**地址**: https://lemon.qq.com/

**软件状态**: 免费 

**软件介绍**

腾讯柠檬清理 Lite 版-重点聚焦清理功能，包含系统/应用垃圾清理、大文件清理、重复文件清理、相似照片清理 4 个方面，当前还支持在状态栏上查看当前网速信息，帮助你实时了解 Mac 状况。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/16227749924686.jpg)

**核心功能**

* 便捷好用的状态栏清理：可直接在状态栏上查看实时网速，方便及时了解网速变化。支持快速清理，轻轻一点，不留垃圾。
* 系统/应用垃圾清理
* 大文件清理：帮你快速全面查找占用超过 50M 的大文件。
* 重复文件清理


## 联系我们

[iOS摸鱼周报 第九期](https://zhangferry.com/2021/04/24/iOSWeeklyLearning_9/)

[iOS摸鱼周报 第十期](https://zhangferry.com/2021/05/05/iOSWeeklyLearning_10/)

[iOS摸鱼周报 第十一期](https://zhangferry.com/2021/05/16/iOSWeeklyLearning_11/)

[iOS摸鱼周报 第十二期](https://zhangferry.com/2021/05/22/iOSWeeklyLearning_12/)

[iOS摸鱼周报 第十三期](https://zhangferry.com/2021/05/30/iOSWeeklyLearning_13/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
