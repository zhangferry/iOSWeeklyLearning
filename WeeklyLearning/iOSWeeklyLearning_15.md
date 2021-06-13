# iOS摸鱼周报 第十五期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 开发Tips
### 几个有用的 SQL 函数

内容整理：[zhangferry](https://zhangferry.com)

SQL 提供了很多用于计数和计算的内建函数，被称为 Aggregate 函数，它们会返回一个单一值：

| 函数名  | 函数功能       |
| ------- | -------------- |
| AVG()   | 返回平均值     |
| COUNT() | 返回行数       |
| SUM()   | 返回对应值总和 |
| MAX()   | 返回最大值     |
| MIN()   | 返回最小值     |
| FIRST() | 返回第一条     |
| LAST()  | 返回最后一条   |

我们以 SUM 为例讲几个示例。

计算某一列值的总和：

```sql
SELECT SUM(score) AS total_score FROM students_table;
```

SUM 还可以结合条件语句计算自定义值，比如一场比赛，result 里分别用 win 和 loss 代表赢和输，赢加一分，输减一分，我们需要计算总得分：

```sql
SELECT SUM(case when result = 'win' then 1 else -1 end) as result_score FROM game_table;
```

其中 when 语句还可以简写为：`if(result = 'win', 1, -1)`

### 去掉 iOS 导航栏返回按钮文本两种方案

内容整理：[FBY展菲](https://github.com/fanbaoying)

**方案一**

1. 自定义 `UINavigationController`
2. 遵守 `<UINavigationBarDelegate>` 协议
3. 实现下面方法：

```objectivec
#pragma mark --------- UINavigationBarDelegate
- (BOOL)navigationBar:(UINavigationBar *)navigationBar shouldPushItem:(UINavigationItem *)item {
    
    //设置导航栏返回按钮文字，Title不要设置为nil
    UIBarButtonItem *back = [[UIBarButtonItem alloc] initWithTitle:@"" style:UIBarButtonItemStylePlain target:nil action:nil];
    item.backBarButtonItem = back;
    
    return YES;
}
```

**方案二**

设置全局的 UIBarButtonItem 样式，将返回按钮的文案设置为透明不可见。

```objectivec
//设置导航栏返回按钮文字为透明的，可能造成导航标题不居中的问题
[[UIBarButtonItem appearance] setTitleTextAttributes:@{NSForegroundColorAttributeName: [UIColor clearColor]} forState:UIControlStateNormal];
[[UIBarButtonItem appearance] setTitleTextAttributes:@{NSForegroundColorAttributeName: [UIColor clearColor]} forState:UIControlStateHighlighted];
```

**方案三**

给 `UIViewController` 添加类别，然后在 `load` 方法里面用 `Method Swzilling` 将 `ViewDidAppear` 方法与我们的 Hook 方法进行交换。该方案需要注意与其他 Hook 方案是否冲突，特别是三方库，不是很推荐。其代码如下：

```objectivec
#import "UIViewController+HideNavBackTitle.h"
#import <objc/runtime.h>


@implementation UIViewController (HideNavBackTitle)

+(void)load {
    swizzleMethod([self class], @selector(viewDidAppear:), @selector(ac_viewDidAppear));
}
 
//设置导航栏返回按钮文字
- (void)ac_viewDidAppear{
    self.navigationItem.backBarButtonItem = [[UIBarButtonItem alloc]
                                              initWithTitle:@""
                                              style:UIBarButtonItemStylePlain
                                              target:self
                                              action:nil];
    [self ac_viewDidAppear];
}

void swizzleMethod(Class class, SEL originalSelector, SEL swizzledSelector)
{
    // the method might not exist in the class, but in its superclass
    Method originalMethod = class_getInstanceMethod(class, originalSelector);
    Method swizzledMethod = class_getInstanceMethod(class, swizzledSelector);
     
    // class_addMethod will fail if original method already exists
    BOOL didAddMethod = class_addMethod(class, originalSelector, method_getImplementation(swizzledMethod), method_getTypeEncoding(swizzledMethod));
     
    // the method doesn’t exist and we just added one
    if (didAddMethod) {
        class_replaceMethod(class, swizzledSelector, method_getImplementation(originalMethod), method_getTypeEncoding(originalMethod));
    }
    else {
        method_exchangeImplementations(originalMethod, swizzledMethod);
    }
}

@end
```

参考：[去掉 iOS 导航栏返回按钮文本三种方案 - 展菲](https://mp.weixin.qq.com/s/VoVzBNlqWkk522t_aLC35A)


## 那些Bug
整理编辑：[FBY展菲](https://github.com/fanbaoying)

###  排查 iOS 国际化文本格式报错

**问题背景**

项目实现国际化功能，编译时遇到错误，`read failed: Couldn't parse property list because the input data was in an invalid format`

![](https://upload-images.jianshu.io/upload_images/2829694-32beb8f3d6c7d838.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

根据错误提示告诉我们是数据格式的问题。具体问题出现在那里下面分析一下

**问题分析**

数据格式错误一般会有下面几种情况：

* 末尾少了分号
* 字符使用了全角字符（中文字符）
* 中间少了 =
* 少了双引号或者引号没有成对出现
* 文本中出现了不必要的特殊字符

这是个小问题，主要看怎么快速查找出问题，下面给出两种方法：

1、使用系统自带的命令行工具： `plutil` 

plutil 多用于处理 plist 文件的校验和修改，其还可以用用于校验多语言文件 `.strings` 的格式问题：

```bash
$ plutil -lint path/Localizable.strings
```

因为是脚本工具，其可以很方便的进行批量处理。

2、借助 GUI 工具：Localizable

Localizable 是 Mac 上的一款桌面工具，在商店搜索 Localizable 就可以找到，使用方式也很简单，只需要将  Localizable.strings 文件拖到对应区域就可以，然后会反馈哪一行格式有问题，对应解决就好，非常方便。

![](https://upload-images.jianshu.io/upload_images/2829694-2d5c9279f35f29d3.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

参考：[iOS 国际化文本格式报错 - 展菲](https://mp.weixin.qq.com/s/qFfXwI9sLqxm9wTpsSS6rQ)

## 编程概念

### BootStrap

内容整理：[zhangferry](https://zhangferry.com)

目前 Web 应用广泛使用在 PC、Pad、移动端等多个平台，但各个端的布局样式相差较大，如果能使用统一的方式描述布局将是非常有必要的，而这就是BootStrap的主要功能之一。

BootStrap 最初由 Twitter 开发，后在Github [开源](https://github.com/twbs/bootstrap)。它除了解决不同端统一布局的问题，还封装了很多可重用的组件，例如下拉菜单，弹框等，可以直接调用。另外它还提供一套优雅的 HTML + CSS 规范，统一了代码风格。

前端框架很多，但即使再多也都是围绕 HTML + CSS + JavaScript 展开的。前一篇讲的 React、Vue 都是工作在 JavaScript 这一层的，BootStrap 则主要工作在 HTML、CSS 这一层。

这个网站整理了很多基于 BootStrap 建立的站点：https://www.youzhan.org/

### 什么是 Webpack

内容整理：[师大小海腾](https://juejin.cn/user/782508012091645)

近年来 Web 应用变得更加复杂与庞大，它们拥有着复杂的 JavaScript 代码和一大堆依赖包。为了简化开发的复杂度，前端社区涌现出很多好的实践方法：

* 模块化，让我们可以把复杂的程序细化为小的文件；
* 类似于 TypeScript 这种在 JavaScript 基础上拓展的开发语言：使我们能够实现目前版本的 JavaScript 不能直接使用的特性，并且之后还能能转换为JavaScript文件使浏览器可以识别；
* scss，less 等 CSS 预处理器；

这些改进确实大大的提高了我们的开发效率，但是利用它们开发的文件往往需要进行额外的处理才能让浏览器识别，而手动处理又是非常繁琐的，这就为 WebPack 这一类的工具的出现提供了需求。

其官网的首页图很形象的画出了 Webpack 是什么，如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210612002026.png)

其是一个用于现代 JavaScript 应用程序的 静态模块打包工具。当 webpack 处理应用程序时，它会在内部构建一个 [依赖图(dependency graph)](https://webpack.docschina.org/concepts/dependency-graph/)，此依赖图对应映射到项目所需的每个模块，并生成一个或多个 bundle。

参考：[gwuhaolin/dive-into-webpack](https://github.com/gwuhaolin/dive-into-webpack "gwuhaolin/dive-into-webpack")，[什么是webpack打包工具以及其优点用法](https://blog.csdn.net/weixin_42941619/article/details/87706623 "什么是webpack打包工具以及其优点用法")

### 什么是 Flutter

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210613093819.png)

内容整理：[我是熊大](https://juejin.cn/user/1151943916921885/posts)

Flutter 是目前开发者首选的跨平台开发框架。Flutter 2.2在 Google I/O 2021 大会上正式发布，从移动设备扩展到 web、桌面设备以及嵌入式设备，真正实现了全端覆盖。

Flutter的核心原则是一切皆为widget，与其他将视图、控制器、布局和其他属性分离的框架不同，Flutter具有一致的统一对象模型：widget。

> 当前iOS的界面元素由 UIView + UIViewController + AutoLayout 组合而成，到了 SwiftUI 则统一用 View 描述，类似 Flutter 的widget。

其使用声明式语法，比如实现一个简单 widget padding 的功能：

```dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(
      title: Text("Sample App"),
    ),
    body: Center(
      child: CupertinoButton(
        onPressed: () {
          setState(() { _pressedCount += 1; });
        },
        child: Text('Hello'),
        padding: EdgeInsets.only(left: 10.0, right: 10.0),
      ),
    ),
  );
}
```

Flutter 拥有更优的性能，主要原因就是它用于一套自己独有的渲染引擎，其整理架构如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210613103605.png)

Flutter 仍有一些缺点，即导致包体变大，iOS引入后，包体积增加10MB左右。

推荐文章：[Flutter实用教程](https://flutter.cn/docs/cookbook "Flutter实用教程")


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)

本期周报主题：`逆向原理篇`

[iosre](https://iosre.com "iosre") -- 来自网站：https://iosre.com


一个活跃逆向论坛。

[iOS逆向(11)-砸壳原理剖析，主动加载所有framework](https://juejin.cn/post/6844904006024691726 "iOS逆向(11)-砸壳原理剖析，主动加载所有framework") -- 来自掘金：一缕清风扬万里

[砸壳这件破事](https://mp.weixin.qq.com/s/xFHA2tlc6HCLti_ihlrsZA "砸壳这件破事") -- 来自：非尝咸鱼贩


谈到逆向首先需要来了解下砸壳。到底什么是“壳”，砸壳到底砸的是什么？

[iOS App 签名的原理](http://blog.cnbang.net/tech/3386/ "iOS App 签名的原理") -- 来自：bang's blog


这篇文章是我经常拿出来翻看的，每次谈到签名流程都需要查看下。

[Code Signing - iOS 代码段的校验机制分析](https://mp.weixin.qq.com/s/msUwo3YUcfHXkuAp5wRfyQ "Code Signing - iOS 代码段的校验机制分析") -- 来自公众号：高级页面仔


这篇文章对签名校验讲述的很详细，使用 xnuspy 可以 hook 系统缺页中断函数，这可能对我们日后的性能分析有帮助。


[iOS LLDB中反反调试分析与实现](https://mp.weixin.qq.com/s/egrQxxJSympB-L6BdVDQVA "iOS LLDB中反反调试分析与实现")  -- 来自公众号：看雪学院


__TEXT段是只读的，到底能不能在运行期间修改呢？可以看看这篇文章。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### SwiftLee

链接：https://www.avanderlee.com/

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210613155259.png)

一个分享关于 Swift、iOS 和 Xcode 技巧和窍门的每周博客，博客的文章写得清晰易懂，排版、配图和动画质量也很高。值得关注一下。同时网站作者也是 [《Swift for Good》](https://www.swiftforgood.com/ "Swift for Good") 的联合作者之一。《Swift for Good》是由20位顶级作家和演讲者撰写的新书，其所有收入将100%捐给慈善机构，有兴趣也可以看一下😺。

### WWDC21 内参

链接：https://xiaozhuanlan.com/wwdc21

一年一度的 WWDC 又来啦！由**老司机周报**牵头开展的WWDC 21内参活动，目前已经有100多名开发者报名参与其中，也包括多名摸鱼周报的编辑。我们会根据必要性和实际情况选择合适的内容进行深度解读，让大家快速了解 WWDC21 中那些值得关注的 Session。

现在也开放了今年 《WWDC21 内参》的[购买](https://xiaozhuanlan.com/wwdc21)，限时售价 9.9 元，之后会提高为 29.9 元，明年的WWDC 前夕会改为免费领取。所有的《WWDC 内参》的收入，都会归参与的作者所有。

## 工具推荐

整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### Diffchecker

**地址**：https://www.diffchecker.com/

**软件状态**：Web端免费，桌面端 $9/月

**介绍**

Diffchecker 是一款简单好用的差异比较工具，使用可帮助用户快速的比较您的文本文件、文档、PDF、照片、图形和扫描等，并且界面简单直观，输入两个文件的内容，然后单击“查找差异”即可，并且具有绝对的安全性，能够保障您的文件安全，具有统一差异、字符级差异、文件夹差异、导出为 PDF、语法高亮、文件导入、无广告等优势。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/1623388796593.jpg)


## 联系我们

[摸鱼周报第十一期](https://zhangferry.com/2021/05/16/iOSWeeklyLearning_11/)

[摸鱼周报第十二期](https://zhangferry.com/2021/05/22/iOSWeeklyLearning_12/)

[摸鱼周报第十三期](https://zhangferry.com/2021/05/30/iOSWeeklyLearning_13/)

[摸鱼周报第十四期](https://zhangferry.com/2021/06/06/iOSWeeklyLearning_14/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)