# iOS 摸鱼周报 #98 | visionOS 模拟器体验

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：visionOS 模拟器体验；Safari Technology Preview 173 发布
> * 本周学习：React Hooks 相关的几个概念介绍
> * 内容推荐：mergeable libraries、Swift on Server、Observation 框架、通过 ReviewKit 获得更多好评、Apple AR 技术全景等博客推荐。
> * 摸一下鱼：Diffusion Bee 2 发布，致力于打造 Mac 端最优秀的 StableDiffusion 开源工具；GPT Engineer 项目来让 AI 来充当软件工程师；「三五环」一期关于投资、创业的播客分享

## 本期话题

### [Xcode 15 Beta 2](https://developer.apple.com/download/all/?q=xcode%2015 "Xcode 15 Beta 2")

[@zhangferry](zhangferry.com)：Xcode 15 beta 2 包含 visionOS，已经可以利用 visionOS 模拟器来运行系统或自己的 App 看一下它们在新系统上的运行状态了。模拟器无法模拟手势，所以所有操作都是通过鼠标和键盘完成，但主要的设计细节还是可以通过模拟器感受到的。少数派有一篇文章比较详细的介绍了各项体验：[visionOS beta 1 快速体验](https://sspai.com/post/80536 "visionOS beta 1 快速体验")

![](https://cdn.zhangferry.com/Images/202306300009456.png)

### [Safari Technology Preview 173 发布](https://developer.apple.com/safari/resources/ "Safari Technology Preview 173 发布")

[@zhangferry](zhangferry.com)：苹果推出 Safari Technology Preview 旨在从开发人员和用户那里收集关于其浏览器开发过程的反馈。173 版本会随 macOS Sonoma 一起发布，该版本更新了 Profiles、Web apps、Web Inspector、CSS、Media Queries、Rendering、Editing、JavaScript、Popover、Images、Media、Web API 和 SVG 等方面的功能。

## 本周学习

整理编辑：[zhangferry](https://zhangferry.com)

### React Hooks
在介绍 React Hooks 之前先了解下 React 类式组件的书写方式，比如实现一个记录点击计次数的组件：

```jsx
class Counter extends React.Component {
  // 构造方法
  constructor(props) {
    super(props);
    // state 初始化
    this.state = {
      count: 0
    };
  }
  
  // 组件完成加载
  componentDidMount() {
    document.title = `You clicked ${this.state.count} times`;
  }
  // 组件完成更新
  componentDidUpdate() {
    document.title = `You clicked ${this.state.count} times`;
  }
  // 渲染组件
  render() {
    return (
      <div>
        <p>You clicked {this.state.count} times</p>
    		{/* JSX注释：添加按钮及点击事件 */}
        <button onClick={() => this.setState({ count: this.state.count + 1 })}>
          Click me
        </button>
      </div>
    );
  }
}
```

这里使用到了 React 里的 `setState` 来记录状态，使用 `componentDidMount` 等几个生命周期的函数来在适当时机更新内容。想要用函数来实现组件的话面临的问题就是函数没有状态和生命周期，为了解决这个问题，React 引入了 React Hooks 方法。还是上面的功能，函数式实现代码为：

```jsx
function Counter() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    document.title = `You clicked ${count} times`;
  });
  
  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  );
} 
```

代码看着精简了很多，这种方式也是官方推荐的写法。回到函数式的两个问题，看函数式组件是如何解决的，无状态，无生命周期，在这里分别对应 `useState` 和 `useEffect `函数。

`useState` 函数可以赋值一个初始值，这里是 0，它有两个返回值，count 表示值变量，setCount 表示修改该变量的 setter 方法。

`useEffect` 函数表示 `componentDidMount` 那几个生命周期函数，它们都会统一走到 `useEffect` 里。这里有一个问题是如果想在 didMount 和 didUpdate 中做不同事情该如何处理呢？可以看下它在 TypeScript 下的定义：

```typescript
type EffectCallback = () => void | (() => void);
type Inputs = ReadonlyArray<unknown>;
/**
 * Accepts a function that contains imperative, possibly effectful code.
 * The effects run after browser paint, without blocking it.
 *
 * @param effect Imperative function that can return a cleanup function
 * @param inputs If present, effect will only activate if the values in the list change (using ===).
 */
export function useEffect(effect: EffectCallback, inputs?: Inputs): void;
```

它还有第二个可选参数 inputs，类型为数组，这个数组可以作为 effect 回调函数里的参数使用，当数组里的值变化时，回调函数就会被调用。通过这种方式可以实现不同场景下的回调，以下为 Glarity 里卡片手动刷新的逻辑：

```jsx
const onRefresh = useCallback(async () => {
  // 正在加载，直接返回
  if (loading) {
    return
  }
  setLoading(true)
	// 数据组合
  questionData = Object.assign(questionData, { currentTime: Date.now() })
  setQuestionProps({ ...props, ...questionData })
}, [props, loading]) // 供callback使用的两个参数
```

除了这两个 Hooks，还有用于实现其他特性的几个常用的内置 Hooks：

* useContext：共享上下文
* useCallback：返回缓存的回调函数，防止函数多次生成
* useMemo：返回缓存的计算结果，防止重复计算
* useLayoutEffect：与 useEffect 类型，但是在所有 DOM 变更之后同步调用 effect
* useReducer：状态管理，与useState类型，但可以管理更复杂的状态逻辑

这些 Hooks 均以 use 开头，同时你也可以定义自己的 Hooks。


## 内容推荐

推荐近期的一些优秀博文，内容涵盖可合并库、Swift on Server、Observation 框架、通过 ReviewKit 获得更多好评、Apple AR 技术全景等方面。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[了解可合并库](https://www.polpiella.dev/understanding-mergeable-libraries/ "了解可合并库") -- 作者：Pol Piella Abadia

[@东坡肘子](https://www.fatbobman.com/): 在 WWDC 2023 中，苹果推出了可合并的库。在此之前，开发者必须选择是将框架设置为静态库还是动态库。选择其中一种库类型可能会对应用程序的构建和启动时间性能产生连锁反应。但从 Xcode 15 开始，我们可以使用可合并的库，这是一种新类型的库，结合了动态库和静态库的优点，并且针对构建和启动时间性能进行了优化。在本文中，作者将向你展示可合并的库如何解决模块化代码库中的问题，以及使用方法。

2、[Swift on Server Tour](https://blog.kevinzhow.com/posts/why-swift-on-server/zh "Swift on Server Tour") -- 作者：Kevin

[@东坡肘子](https://www.fatbobman.com/): 作者将通过一系列文章，带领读者畅游 Swift on Server 的世界。这个系列主要面向服务器开发的初学者，因此除了功能实现外，还会写一些相关概念的内容。主题涉及：什么是 Server App、HTTP 请求的相关内容、选择你的框架 - Vapor、设计你的数据模型、设计你的 API、用户权限验证、测试你的 API、部署你的服务器、和其他语言一起工作等内容。目前已完成两章，敬请期待后续更新。

3、[深度解读 Observation —— SwiftUI 性能提升的新途径](https://www.fatbobman.com/posts/mastering-Observation/ "深度解读 Observation —— SwiftUI 性能提升的新途径") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 在 WWDC 2023 中，苹果介绍了 Swift 标准库中的新成员：Observation 框架。它的出现有望缓解开发者长期面临的 SwiftUI 视图无效更新问题。作者在文章中采取了问答的方式，全面而详尽地探讨了 Observation 框架，内容涉及其产生的原因、使用方法、工作原理以及注意事项等内容。

4、[ReviewKit：帮你的应用获得更多的 App Store 好评](https://www.fline.dev/introducing-reviewkit/ "ReviewKit：帮你的应用获得更多的 App Store 好评") -- 作者：Cihat Gündüz

[@东坡肘子](https://www.fatbobman.com/): 作为一名应用程序开发者，你应该知道用户评论对应用程序的成功和可信度有多重要。积极的评论不仅可以吸引更多用户，还可以帮助应用在 App Store 中获得更高的排名。然而，在不合适的时间或者向没有充分体验应用的用户要求评论可能会导致用户失望并获得负面反馈。ReviewKit 提供了一个简单而有效的解决方案，通过根据最近的使用记录智能地决定何时向用户请求应用程序评论。在本文中，作者介绍了如何使用 ReviewKit。

5、[掌握 Transaction，实现 SwiftUI 动画的精准控制](https://www.fatbobman.com/posts/mastering-transaction/ "掌握 Transaction，实现 SwiftUI 动画的精准控制") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): SwiftUI 因其简便的动画 API 与极低的动画设计门槛而广受欢迎。但是，随着应用程序复杂性的增加，开发者逐渐发现，尽管动画设计十分简单，但要实现精确细致的动画控制并非易事。同时，在 SwiftUI 的动画系统中，有关 Transaction 的解释很少，无论是官方资料还是第三方文章，都没有对其运作机制进行系统的阐述。文章将通过探讨 Transaction 的原理、作用、创建和分发逻辑等内容，告诉读者如何在 SwiftUI 中实现更加精准的动画控制，以及需要注意的其他问题。

6、[开发 visionOS 前，你需要了解的 Apple AR 技术全景](https://mp.weixin.qq.com/s/LTR9C2TmKVhuYgFpD5Bw1A "开发 visionOS 前，你需要了解的 Apple AR 技术全景") -- 作者：XR基地 XR 基地的小老弟

[@东坡肘子](https://www.fatbobman.com/): 自从 2017 年 Apple 推出 ARKit 以来，Apple AR 相关的技术已经发展了 6 年多了。在这个过程中，每年的 WWDC 都会有关于 AR 技术的 Sessions。然而，由于使用场景的限制，大多数开发者可能仅仅是知道 Apple 有 AR 相关的技术，但对这项技术并没有实际的上手或深入了解。因此，对于 iOS 开发者来说，它可能是一个“熟悉的陌生人”。本文作者将从以下方面出发，帮助读者对 Apple AR 技术有一个大致的了解：2017~2022 年 WWDC 的进展、从官方 30+ 个 Sample Code 中总结出的 AR 整体框架、所有 AR App 都会用到的最基础的代码和编程概念、精进 Apple AR 必须了解的其他技术，以及入门 Apple AR 的推荐资料。作者希望读者在阅读本文后能够更好地理解 Apple AR 技术，并成为与之可以进一步合作的同事。


## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

1、[Diffusion Bee](https://github.com/divamgupta/diffusionbee-stable-diffusion-ui "Diffusion Bee")：之前推荐过的一个项目，macOS 系统下的 Stable Diffusion GUI 应用。当时版本还比较早，只能使用内置模型，最近它发布了 2.2.1(Beta) 版本。全新 UI，可以直接制作视频内容，支持 Lora 模型，支持 ControlNet，支持无限 AI 画布，自由修改图片。基本是一个完整功能的 Stable Diffusion WebUI 了。而且该项目针对 Mac 系统做了很多参数调优，出图速度比直接搭建的 webui 快很多。

![](https://cdn.zhangferry.com/Images/202306292342223.png)

3、[GPT Engineer](https://github.com/AntonOsika/gpt-engineer "GPT Engineer")：这个项目使用结构化的方式让 GPT 来解决编程问题，它跟 AutoGPT 很像，是被用于专门解决编程问题的。使用流程是：

* 创建一个 prompt 文件，里面描述你要做的事情
* 读取这个文件，GPT 会根据不明确的信息再向你提问，你需要回答他的问题来消除所有的不确定性问题
* 执行编写任务

就是这么简单，编程的门槛正在不断被降低。

3、[三五环：老范聊创业：创业、投资就像酒，很讲究年份](https://www.xiaoyuzhoufm.com/episode/64911bd586eb9d7e47c627c3 "三五环：老范聊创业：创业、投资就像酒，很讲究年份")：最近听的一期质量还挺高的播客，主播是产品经理，嘉宾是一位天使投资人。

关于投资：不要听信专家的话，先信了再说，当有人开始劝你、甚至指导你该做什么的时候，说明已经过了它的红利期了。当一个人的经验越来越丰富时，很容易被经验主义束缚，对新事物的接受度变低，所以投资要找年轻人。这里还提到了 Vision Pro，从交互意义和长期价值来看，它被严重低估了，它成为 iPhone 时代的概率非常高。

关于创业：选择上的一些原则，新赛道、体量大、看最有力量的人、尽早切入。投资创业有黄金年份，如果错过，是很难弥补的，眼光的敏锐度非常重要。评估自己是进取型还是稳健性人格，进取型才适合创业。

关于职业发展：识天物，傍贵人。识天物是要知道什么是好东西，什么是有价值的东西，表示自己的判断力。傍贵人是拉杠杆，向优秀的人学习，借助他们的力量放大自己的价值，表示对外界资源的调动力。

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #97 | 智源大会线下参会体验](https://mp.weixin.qq.com/s/6HRxZXAJcTZKGZiNX2eBYQ)

[iOS 摸鱼周报 #96 | Vision Pro 打开空间计算的大门](https://mp.weixin.qq.com/s/BM3SucfO9yhQChIPbnuwrA)

[iOS 摸鱼周报 #95 | WWDC23 is coming](https://mp.weixin.qq.com/s/hi8Dy2H_iBFWeO0V_tQ5xw)

[iOS 摸鱼周报 #94 | 前端项目开发流程学习](https://mp.weixin.qq.com/s/f2Z1VRpk4Ehh3KxuY_NrvA)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
