# iOS摸鱼周报 第三十二期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

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

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)



## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

本周博客主题：Swift 关键字

在还没有学习Swift时，听过好几次部门内关于Swift的分享。依稀记得在分享会上听到了各种各样的新颖的概念，见到一些在OC中没有见过的关键字。希望本次主题能为OC的同学扫清一些学习Swift的障碍。

1、[Swift-29个关键字，助力开发（万字长文）](https://juejin.cn/post/6844904112119611399 "Swift-29个关键字，助力开发（万字长文）") -- 来自掘金：SunshineBrother

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：推荐新手阅读，对Swift比较熟悉的同学可以简单浏览校验下是否有不清楚的概念。文中有对应的示例代码，帮助大家理解。


2、[Swift 的闭包为什么选用 in 关键字？](https://www.zhihu.com/question/53539254 "Swift 的闭包为什么选用 in 关键字？") -- 来自知乎

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：Swift 闭包为什么用 in 可能很多同学都没有思考过。这个问题比较有意思，信息量也不是很密集，也比较轻松。该话题有人列出了苹果工程师对此的解释。

3、[细说 Swift 4.2 新特性：Dynamic Member Lookup](https://juejin.cn/post/6844903621306351624 "细说 Swift 4.2 新特性：Dynamic Member Lookup") -- 来自掘金：没故事的卓同学

[@东坡肘子](https://www.fatbobman.com)：@dynamicMemberLookup 中文可以叫动态查找成员。在使用 @dynamicMemberLookup 标记了对象后（对象、结构体、枚举、protocol），实现了 subscript(dynamicMember member: String)方法后我们就可以访问到对象不存在的属性。如果访问到的属性不存在，就会调用到实现的 subscript(dynamicMember member: String)方法，key 作为 member 传入这个方法。

4、[解析 Swift 中的 @discardableResult](https://xie.infoq.cn/article/fef30fd533cdff4278f0a85ff "解析 Swift 中的 @discardableResult") -- 来自：SwiftMic

[@东坡肘子](https://www.fatbobman.com)：@discardableResult 属性可能很少被人熟知，但是对于想消除方法返回值未被使用的警告来说的话，该属性还是很有用的，只需要在对应方法前添加 @discardableResult 属性即可。但是，还是要考虑是否真的需要忽略该类警告，因为有些情况下及时处理返回结果可能是一种更好的解决方案。

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