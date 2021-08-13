# iOS摸鱼周报 第二十三期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> 

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)
###  `PrioritySessionElement` 摊平复杂逻辑流程的设计

###### 用来解决什么问题

* 一开始是用来解决工作中运营活动优先级问题，简化逻辑代码，做到高可读，可扩展。
* 后续慢慢在使用过程中逐渐衍生新的功能（延时，轮询，条件校验等）
* 当然最大的特点就是把回调地狱展平把核心都放在同一层级

不知道说什么，以代码图示例，为改进之前 代码是这样写的
```swift
// 1
func function0() {
    obj0.closure { _ in
        // to do something
        obj1.closure { _ in
            // to do something                      
            obj2.closure { _ in
                ...
                objn.closure { _ in
                       ...
                }         
            }             
        }        
    }
}

or
// 2.
func function1 {
    if 满足活动0条件 {
        // to do something
    } else if 满足活动1条件 {
        // to do something
    } else if 满足活动2条件 {
        // to do something
    }
    ...
    else {
        // to do something
    }
}
```

###### 分析上面那种代码我们可以得出几点结论：

* 上面的代码不管怎么看都是按流程来的或者不同的条件走不同的条件流程
* 可读性与可维护性一般还行，二次修改错误率很高
* 扩展性一般几乎没有，只会无限增加代码的行数、条件分支以及回调更深层级
* 如果功能升级增加类似延迟、轮询，那完全不支持。
* 复用性可以说无

###### 所以就针对问题解决问题：

* 实现一个容器（`Element`）搭载所有外部实现逻辑
* 容器（`Element`）以单向链表的方式链接，执行完就自动执行下一个
* 容器内聚合一个抽象条件逻辑助手（`Promise`）,可随意扩展增加行为,用来检查外部实现是否可以执行链表下一个`Element`（可以形象理解为自来水管路的阀门，电路电气开关之类，当然会有更复杂的阀门与电气开关）
* 自己管理自己的生命周期，无需外部强引用
* 容器（`Element`）可以被继承实现，参考`NSOperation`设计

###### 详细的设计介绍这里语雀：https://www.yuque.com/runscode/ios-thinking/priority_element
###### 详细源码请参考，有`OC、Swift、Java`版本的具体实现 欢迎大家指正：https://github.com/RunsCode/PromisePriorityChain
#### Example
```swift
private func head() -> PriorityElement<String, Int> {
    return PriorityElement(id: "Head") {  (promise: PriorityPromise<String, Int>) in
        Println("head input : \(promise.input ?? "")")
        self.delay(1) { promise.next(1) }
    }.subscribe { i in
        Println("head subscribe : \(i ?? -1)")
    }.catch { err in
        Println("head catch : \(String(describing: err))")
    }.dispose {
        Println("head dispose")
    }
}
// This is a minimalist way to create element, 
// using anonymous closure parameters and initializing default parameters
private func neck() -> PriorityElement<Int, String> {
    return PriorityElement {
        Println("neck input : \($0.input ?? -1)")
        $0.output = "I am Neck"
        $0.validated($0.input == 1)
    }.subscribe { ... }.catch { err in ... }.dispose { ... }
}
// This is a recommended way to create element, providing an ID for debugging
private func lung() -> PriorityElement<String, String> {
    return PriorityElement(id: "Lung") { 
        Println("lung input : \($0.input ?? "-1")")
        self.count += 1
        //
        $0.output = "I am Lung"
        $0.loop(validated: self.count >= 5, t: 1)
    }.subscribe { ... }.catch { err in ... }.dispose { ... }
}
private func heart() -> PriorityElement<String, String> {}
private func liver() -> PriorityElement<String, String> {}
private func over() -> PriorityElement<String, String> {}
... ...
let head: PriorityElement<String, Int> = self.head()
head.then(neck())
    .then(lung())
    .then(heart())
    .then(liver())
    .then(over())
// nil also default value()
head.execute()
```

也许大家看到这里问到一个一股熟悉的`Goolge`开源的`Promises`&`mxcl`的`PromiseKit`或者`RAC`等的味道
那么为啥不用那些个神的框架来解决实际问题呢？
主要有一点：框架功能过于丰富复杂，而我呢，弱水三千我只要一瓢，越轻越好的原则！哈哈



## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

本期主题：`Swift 指针`

1、[Swift 中的指针使用]( https://onevcat.com/2015/01/swift-pointer/  "Swift 中的指针使用") -- 来自：onevcat

swift中指针使用场景并不常见，但是有些时候我们又不得不尝试去使用指针，因此还是需要对swift的指针运用有一定的了解。这篇文章是喵神15年写的，并在2020年做了更新。文章对C指针和swift的指针应用做了映射，对于有一定C指针基础的同学阅读比较友好。

2、[The 5-Minute Guide to C Pointers](https://denniskubes.com/2017/01/24/the-5-minute-guide-to-c-pointers/"C语言指针5分钟教程") -- 来自：Dennis Kubes

喵神文章中推荐的C语言指针教程，如果对C指针不了解的话，直接切入到swift的指针还是有一定的困难的。

3、[Swift5.1 - 指针Pointer](https://www.jianshu.com/p/8cff1ef20e8c "Swift5.1 - 指针Pointer") -- 来自简书：HChase

喵神在文章中做了很多的类比，这篇文章则根据swift的类型给出了多种使用方法，查找用法非常方便。例如malloc之后如何填充字节、如何根据地址创建指针、如何进行类型转换等。如果在开发中需要使用swift的指针，在不熟悉的情况下可以参考文中的小demo。




## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
