# iOS摸鱼周报 第三十四期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * 话题：Apple 宣布推出自助维修计划。
> * Tips：混编｜NS_SWIFT_NAME。
> * 面试模块：二叉树的三序遍历。
> * 优秀博客：几个 Swift 三方库的解析文章。
> * 学习资料：棒棒彬·技术参考周刊。
> * 开发工具：Mounty：一个在 macOS 下以读写模式重新挂载写保护的 NTFS 卷的免费的小工具。

## 本期话题

[@zhangferry](https://zhangferry.com)：Apple 宣布推出自助维修计划。Apple 将面向个人消费者提供零件、工具与维修手册，从 iPhone 12 与 iPhone 13 开始。搭载 M1 芯片的 Mac 电脑也将很快加入。自助维修计划将从明年初开始在美国率先启动，并在 2022 年或更晚推广到其他国家。

这跟苹果的环保政策相符，可以预料到本来就很能打的 iPhone 更换原装部件之后再多用个 1-2 年也不是啥难事。虽然惠及的用户不会特别多，但是苹果的做法还是值得点赞的。

同时这也带来一个问题，自助维修算是一件有一些技术操作的事情，如何保证操作的正确性？

想起之前我自己给 iPhone 换电池的经历，前两次换 iPhone6SP 电池成功。对自己有了一定的信心，结果，第三次给 iPhone7P 换电池就失手了，不仅因为电池排线插的错位导致一块电路板烧掉，还扯断了连接 Home 键的一根线。有一部分原因是手机屏和后盖的链接方式从之前的前后变成了左右，操作空间变小了，但更主要的还是相应知识的缺乏。这还只是简单的电池，像是摄像头的更换将会更复杂。所以这个自助维修计划比较重要的是应该允许哪些人能够自助维修，如何评估这些人。

题外话：如果自己修坏了，肯定还是算到自己头上的吧🤔。

信息来源：[Apple 宣布将推出自助维修计划](https://www.apple.com.cn/newsroom/2021/11/apple-announces-self-service-repair/ "Apple 宣布将推出自助维修计划")

## 开发Tips

### 混编｜NS_SWIFT_NAME

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

`NS_SWIFT_NAME` 宏用于在混编时为 Swift 重命名 Objective-C API，它可用在类、协议、枚举、属性、方法或函数、类型别名等等之中。通过 Apple 举的一些例子，我们可以学习到它的一些应用场景：

* 重命名与 Swift 风格不符的 API，使其在 Swift 中有合适的名称；
* 将与类 A 相关联的类/枚举作为内部类/枚举附属于类 A；
* 重命名 “命名去掉完整前缀后以数字开头的” 枚举的 case，改善所有 case 导入到 Swift 中的命名；
* 重命名 “命名不满足自动转换为构造器导入到 Swift 中的约定的” 工厂方法，使其作为构造器导入到 Swift 中（不能用于协议中）；
* 在处理全局常量、变量，特别是在处理全局函数时，它的能力更加强大，能够极大程度地改变 API。比如可以将 `全局函数` 转变为 `静态方法`，或是 `实例⽅法`，甚至是 `实例属性`。如果你在 Objective-C 和 Swift 里都用过 Core Graphics 的话，你会深有体会。Apple 称其把 `NS_SWIFT_NAME` 用在了数百个全局函数上，将它们转换为方法、属性和构造器，以更加方便地在 Swift 中使用。

你可以在 [iOS 混编｜为 Swift 重命名 Objective-C API](https://juejin.cn/post/7022302122867687454 "iOS 混编｜为 Swift 重命名 Objective-C API") 中查看上述示例。

## 面试解析

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) 

**树**作为最常见的数据结构之一，在算法中有举足轻重的地位。

理解树有助于我们理解很多其他的数据结构，例如**图**，**栈**等。也有助于我们理解一些算法类型，例如，**回溯算法**和**动态规划**。当然在练习关于树的解题过程中，也能够加深我们对**深度优先**及**广度优先**算法的理解。

今天我们以二叉树的**三序遍历**为题，来开启我们二叉树的学习。

### 题目

给定一个二叉树，返回他的 _**前序**_ _**中序**_ _**后序**_ 三种遍历

> 输入: [4,2,6,1,3,5,7]
>     4
>    /   \
>   2     6
>  / \   / \ 
> 1  3 5  7

#### 输出

前序遍历：首先访问根结点，然后遍历左子树，最后遍历右子树（根->左->右）

> 顺序：访问根节点->前序遍历左子树->前序遍历右子树
>
> 前序遍历: [4, 2, 1, 3, 6, 5, 7]

中序遍历：首先遍历左子树，然后访问根节点，最后遍历右子树（左->根->右）

> 顺序：中序遍历左子树->访问根节点->中序遍历右子树
>
> 中序遍历: [1, 2, 3, 4, 5, 6, 7]

后序遍历：首先遍历左子树，然后遍历右子树，最后访问根节点（左->右->根）

> 顺序：后序遍历左子树->后序遍历右子树->访问根节点
>
> 后续遍历: [1, 3, 2, 5, 7, 6, 4]

二叉树的遍历方法一般有三种

* 递归
* 迭代（常规迭代加**颜色标记法**）
* 莫里斯遍历（今天暂时不涉及）

### 递归

在树的深度优先遍历中（包括前序、中序、后序遍历），递归方法最为直观易懂，但考虑到效率，我们通常不推荐使用递归。

递归步骤一般需要遵循以下三种：

1. 确定递归的参数以及返回值
2. 确定递归的终止条件，**递归算法一定有终止条件**，避免死循环。
3. 确定单次递归的逻辑

```swift
/// traversals 为输出的数组
func preorder(_ node: TreeNode?) {
    guard let node = node else {
        return
    }
    /// 前序遍历
    traversals.append(node.val) 
    preorder(node.left)
    preorder(node.right)
    /// 中序遍历
    preorder(node.left)
    traversals.append(node.val) 
    preorder(node.right)
    /// 后序遍历
    preorder(node.left)
    preorder(node.right)
    traversals.append(node.val) 
}
```

#### 迭代

二叉树的迭代步骤一般是将节点加入到一个 `栈` 中，然后通过访问栈头/栈尾，根据遍历顺序访问所有的符合的节点。

##### 前序遍历

```swift
func preorderIteration(_ root: TreeNode?) {
    var st:[TreeNode?] = [root]
    while !st.isEmpty {
        let node = st.removeFirst()
        if node != nil {
            traversals.append(node!.val)
        } else {
            continue
        }
        st.insert(node?.right, at: 0)
        st.insert(node?.left, at: 0)
    }
}
```

##### 中序遍历

```swift
func inorderIteration(_ root: TreeNode?) {
    var st:[TreeNode?] = []
    var cur:TreeNode? = root
    while cur != nil || !st.isEmpty {
        if cur != nil {
            st.insert(cur, at: 0)
            cur = cur?.left
        } else {
            cur = st.removeFirst()
            traversals.append(cur!.val)
            cur = cur?.right
        }
    }
}
```

##### 后序遍历

后序遍历其遍历步骤是 `左→右→中`，但是这个代码实现起来不简单。 所以我们可以先访问依次访问 `中→右→左` 的节点，最后将得到结果进行 `reversed`，其结果最终变成 `左→右→中` 。

```swift
func postorderIteration(_ root: TreeNode?) {
    var st:[TreeNode?] = [root]
    while !st.isEmpty {
        let node = st.removeFirst()
        if node != nil {
            print(node!.val)
            traversals.append(node!.val)
        } else {
            continue
        }
        st.insert(node?.left, at: 0)
        st.insert(node?.right, at: 0)
    }
    traversals = traversals.reversed()
}
```

#### 颜色标记法

传统的迭代由上述代码可知，比较繁琐，而且迭代过程中易错。参照 [颜色标记法-一种通用且简明的树遍历方法](https://leetcode-cn.com/problems/binary-tree-inorder-traversal/solution/yan-se-biao-ji-fa-yi-chong-tong-yong-qie-jian-ming/ "颜色标记法-一种通用且简明的树遍历方法") ，利用一个**兼具栈迭代方法的高效，又像递归方法一样简洁易懂的方法，更重要的是，这种方法对于前序、中序、后序遍历，能够写出完全一致的代码**。

其核心方法如下：

* 标记节点的状态，已访问的节点标记为 **1**，未访问的节点标记为 **0**

* 遇到未访问的节点，将节点标记为 **0**，然后根据三序排序的要求，按照特定的顺序入栈

  >  // 前序 `中→左→右` 按照 `右→左→中`
  >
  >  // 中序 `左→中→右` 按照 `右→中→左`
  > 
  >  // 后序 `左→右→中` 按照 `中→右→左`

* 结果数组中加入标记为 **1** 的节点的值

```swift
    func tuple(_ root: TreeNode?) -> [Int] {
        var traversals = [Int]()
        var statck = [(0, root)]
        while !statck.isEmpty {
            let (isVisted, node) = statck.removeLast()
            if node == nil {
                continue
            }
            if isVisted == 0 {
//                ///前序遍历
//                statck.append((0, node?.right))
//                statck.append((0, node?.left))
//                statck.append((1, node))
//                ///中序遍历
//                statck.append((0, node?.right))
//                statck.append((1, node))
//                statck.append((0, node?.left))
                ///后序遍历
                statck.append((1, node))
                statck.append((0, node?.right))
                statck.append((0, node?.left))
            } else {
                traversals.append(node!.val)
            }
        }
        return traversals
    }
```

利用颜色标记法可以简单的理解迭代的方法，并写出模板代码。

#### 莫里斯遍历

作为兼具性能及低空间复杂度的**莫里斯遍历**，可以在线下讨论。

## 优秀博客

整理编辑：[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com/)

1、[Alamofire的基本用法](https://juejin.cn/post/6875140053635432462 "Alamofire 的使用 - 基本用法") -- 来自掘金：Lebron

[@我是熊大](https://github.com/Tliens)：Alamofire 是 AFNetWorking 原作者写的，Swift 版本相比 AFN 更加完善，本文介绍了 Alamofire 基本用法，很全面，适合精读；作者还有一篇[高级用法](https://juejin.cn/post/6875140780680282125 "Alamofire 高级用法")，推荐阅读。

2、[Kingfisher源码解析](https://juejin.cn/post/6844904015738699790 "Kingfisher源码解析") -- 来自掘金：李坤

[@我是熊大](https://github.com/Tliens)：Kingfisher 对标 OC 中的 SDWebImage，作者是大名鼎鼎的王巍，本文是 Kingfisher 源码解析系列的总结，推荐阅读。

3、[iOS SnapKit架构之道](https://rimson.top/2019/09/04/ios-snapkit-1/ "iOS SnapKit架构之道") -- 来自博客：Rimson

[@我是熊大](https://github.com/Tliens)：SnapKit 在 Swift 中的页面布局的地位，相当于 OC 中的 Masonry，使用起来几乎一模一样，本文作者详细梳理了 Snapkit 布局的过程和原理。

4、[第三方图表库Charts使用详解](https://www.hangge.com/blog/cache/detail_2116.html "第三方图表库Charts使用详解") -- 来自航歌：hangge

[@东坡肘子](https://www.fatbobman.com/)：Charts 是一个功能强大的图表框架，使用 Swift 编写。是对 Android 上大名鼎鼎的图表库 MPAndroidChart 在苹果生态上的移植。作者 hangge 通过大量的范例代码对 Charts 的使用进行了相近地说明。

5、[访问 SwiftUI 内部的 UIKit 组件](https://mp.weixin.qq.com/s/xYKGs3FkrlI_9pq1cdnC5Q "访问 SwiftUI 内部的 UIKit 组件") -- 来自 Swift花园：猫克杯

[@东坡肘子](https://www.fatbobman.com/)：抛开 SwiftUI 尚不完备的工具不说，SwiftUI 的确因其构建 UI 的便捷性给开发者带来了兴奋。有一个令人欣慰的事实是，许多 SwiftUI 组件实际上是基于 UIKit 构建的。本文将带你探索一个令人惊讶的 SwiftUI 库，它叫 Introspect 。利用它，开发者能够访问 SwiftUI 组件底层的 UIKit 视图。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 棒棒彬·技术参考周刊

地址：https://www.yuque.com/binboy/increment-magzine

这是一份由 [Binboy👻棒棒彬](https://www.yuque.com/binboy) 在语雀上梳理总结的技术参考周刊。这份周刊是作者学习与生活的沉淀和思考，既有广度，也有深度，还有态度。就像其发刊词的标题：「与技术世界保持链接」，在周刊中你可以看到作者学习技术的过程和经验，也能看到科技与生活的一些新鲜事，这里可能有你正在关注的，亦或者是从来没听说过的技术信息，这些信息既是作者与他自己「第二大脑」的链接，也是作者与读者交流的媒介，同时推动着作者与读者一起前进。这里改编引用一段[发刊词](https://www.yuque.com/binboy/increment-magzine/sno2ef)中的一段话来抛砖引玉 ：

> 做技术，追求深度无可厚非，只是无需厚此薄彼，我个人而言倾向于「修学储能，先博后渊」的。技术世界的开源、互联网的开放更是给了见多识广一片良好的土壤，我们可以了解了技术、工具现状，将其充分地应用、解决现实世界中的普通问题，并在过程中不断完善。当真正遇到边界时，再结合对已有技术和工具的融会贯通去创造真正的新技术、新工具，也不迟。
>
> *朝一个方向看得再远，你也未必能看到新方向*
>
> *———— 修学储能，先博后渊*

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Mounty

**地址**：https://mounty.app/

**软件状态**：免费，[开源](https://mounty.app/)

**软件介绍**：

`Mounty` 是一个在 macOS 下以读写模式重新挂载写保护的 NTFS 卷的小工具，功能类似于 `NTFS For Mac`，最大也是最重要的区别是它是**免费**的。

![mounty](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/example.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第三十三期](https://mp.weixin.qq.com/s/nznnGmBsqsrWcvZ4XFMttg)

[iOS摸鱼周报 第三十二期](https://mp.weixin.qq.com/s/6CyL0B6Zkf6KXRrfocohoQ)

[iOS摸鱼周报 第三十一期](https://mp.weixin.qq.com/s/DQpsOw90UsRg6A5WDyT_pg)

[iOS摸鱼周报 第三十期](https://mp.weixin.qq.com/s/KNyIcOKGfY5Ok-oSQqLs6w)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
