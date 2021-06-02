## RN概念

React Native 是一个使用React和应用平台的原生功能来构建 Android 和 iOS 应用的开源框架。通过 React Native，可以使用 JavaScript 来访问移动平台的 API，以及使用 React 组件来描述 UI 的外观和行为：一系列可重用、可嵌套的代码。

- 诞生年份：2015 年 9 月
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
- 参考资料
	- React Native 中文网 ：https://reactnative.cn/docs/getting-started
	- React Native 原理与实践：https://zhuanlan.zhihu.com/p/343519887（十分推荐）
