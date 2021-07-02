# iOS摸鱼周报 第十七期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

###  从一个 bug 引发的关于 Swift 中 String.count 和 NSString.length 的探究

#### 什么样的 bug

在为 `NSMutableAttributedString` 添加 attribuites 的时候需要传入相应的属性的字典以及最终需要应用的范围（NSRange）, 当使用Swift 的 `String.count` 创建 `NSRange` 时，发现在某些语言下（印度语言，韩语）对应位置的文字没有应用预期的显示效果

#### 如何解决

通过打印同一个字符串在 NSString 类型下的 **length** 和在 Swift 类型下的 **count** 发现二者的值并不相等，**length** 比 **count** 要大一些。也就是说，在创建 NSRange 时，Swift 的 `String.count` 并不可靠，我们可以使用 `NSString.length` 解决这个问题。

#### `length` 和 `count` 的不同

那么，为什么同一个字符串的 `长度` 在 String 与 NSString 中会得到不同的值呢？我们来看一下 `String.count` 与 `NSString.length` 各自的官方定义：

> String.count: The number of characters in a string.
>
> NSString.length: The length property of an NSString returns the number of UTF-16 code units in an NSString

通过上述官方文字，我们隐约能察觉到一丝不同而继续发出疑问🤔️：

- 这个 `characters` 与 `UTF-16 code units` 是一回事么？
- 如果不是的话那各自的定义又是什么呢？

在 [Swift doc](https://docs.swift.org/swift-book/LanguageGuide/StringsAndCharacters.html#ID290) 中对 Swift 中的 Character 有如下说明：

> Every instance of Swift’s Character type represents a single **extended grapheme cluster**. An extended grapheme cluster is a sequence of one or more Unicode scalars that (when combined) produce a single human-readable character.

在 Swift 1.0 版本的 [Swift String Design](https://github.com/apple/swift/blob/7123d2614b5f222d03b3762cb110d27a9dd98e24/docs/StringDesign.rst#id35) 中，也找到了相关描述：

> `Character`, the element type of `String`, represents a **grapheme cluster**, as specified by a default or tailored Unicode segmentation algorithm. This term is [precisely defined](http://www.unicode.org/glossary/#grapheme_cluster) by the Unicode specification, but it roughly means [what the user thinks of when she hears "character"](http://useless-factor.blogspot.com/2007/08/unicode-implementers-guide-part-4.html). For example, the pair of code points "LATIN SMALL LETTER N, COMBINING TILDE" forms a single grapheme cluster, "ñ".

所以我们可以粗略的理解为一个 Character 表示一个人类可读的字符，举个官方的例子：

```
let eAcute: Character = "\u{E9}"                         // é
let combinedEAcute: Character = "\u{65}\u{301}"          // e followed by ́
// eAcute is é, combinedEAcute is é
```

`é` 在 unicode 中由一个标量（unicode scalar value）表示，也有由两个标量组合起来表示的，不论哪种在 Swift 的 String 中都表示为**一个** Character。
那我们再返回来看 Swift `String.count` 的定义就好理解了，**count** 表示的是 Character 的数量，而 NSString 的 **length** 表示的是实际 unicode 标量（code point）的数量。所以在某些有很多组合标量字符的语言中（或者 emoji 表情）一个 `Character` 与一个 unicode 标量并不是一一对应的，也就造成了同一个字符 `NSString.length` 与 `String.count` 值可能不相等的问题，其实这个问题在 [Swift doc](https://docs.swift.org/swift-book/LanguageGuide/StringsAndCharacters.html#ID290) 中早有提示：

> The count of the characters returned by the **count** property isn’t always the same as the **length** property of an **NSString** that contains the same characters. The length of an NSString is based on the number of 16-bit code units within the string’s UTF-16 representation and not the number of Unicode extended grapheme clusters within the string.

我们可以看到对于字符串 Character 这样 **grapheme cluster** 式的分割字符的方式，更符合我们人类看到文字时的预期的，可以很方便的遍历真实字符，且包容多种多样的语言。但在带来便利的同时也增加了实现上的复杂度。由于每个 `Character` 长度不尽相同，`String.count` 无法像 `NSString.length` 那样使用 `O(1)` 复杂度的情况简单计算固定长度的个数，而是需要遍历每一个字符，在确定每个 Character 的边界和长度后才能推算出总个数。所以当你使用 `String.count` 时，也许要注意一下这是一个 `O(n)` 的调用。


## 面试解析

整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)




## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Swift Algorithm Club

地址：https://github.com/raywenderlich/swift-algorithm-club

由 [raywenderlich](https://www.raywenderlich.com/whats-new) 创立的 Swift 算法俱乐部，在这里会用 Swift 来解释和实现大部分常见的数据结构和算法，例如栈、队列、快速排序、BFS、KMP 等等，如果按照他的学习路线来学习的话，难度由浅入深，循序渐进，很适合入门选手。另外你也可以自己选择感兴趣的内容来查看，适合想要温习算法和数据结构或者温习 Swift 语法的朋友👍。

## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)



## 联系我们

[iOS摸鱼周报 第十一期](https://zhangferry.com/2021/05/16/iOSWeeklyLearning_11/)

[iOS摸鱼周报 第十二期](https://zhangferry.com/2021/05/22/iOSWeeklyLearning_12/)

[iOS摸鱼周报 第十三期](https://zhangferry.com/2021/05/30/iOSWeeklyLearning_13/)

[iOS摸鱼周报 第十四期](https://zhangferry.com/2021/06/06/iOSWeeklyLearning_14/)

[iOS摸鱼周报 第十五期](https://zhangferry.com/2021/06/14/iOSWeeklyLearning_15/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
