# iOS摸鱼周报 第十五期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 开发Tips
整理编辑：[FBY展菲](https://github.com/fanbaoying)

### 去掉 iOS 导航栏返回按钮文本三种方案

**方案一**

1. 自定义 `UINavigationController`
2. 遵守 `<UINavigationBarDelegate>` 协议
3. 实现下面方法：

```objectivec
#pragma mark --------- UINavigationBarDelegate

- (BOOL)navigationBar:(UINavigationBar *)navigationBar shouldPushItem:(UINavigationItem *)item {
    
    //设置导航栏返回按钮文字
    UIBarButtonItem *back = [[UIBarButtonItem alloc] initWithTitle:nil style:UIBarButtonItemStylePlain target:nil action:nil];
    /*
    NSMutableDictionary *textAttrs = [NSMutableDictionary dictionary];
    textAttrs[UITextAttributeTextColor] = [UIColor whiteColor];
    [back setTitleTextAttributes:textAttrs forState:UIControlStateNormal];
    */
    item.backBarButtonItem = back;
    
    return YES;
}
```

> **注意：该方法会出现部分子控制器页面的返回按钮文字出现的bug，需要在其子控制器页面的父控制器里再次如上设置返回按钮才行**

```objectivec
子控制器页面的父控制器

#pragma mark -------- 生命周期函数

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    self.view.backgroundColor = [UIColor whiteColor];
    
    //重新设置下级子页面导航栏返回按钮文字
    UIBarButtonItem *item = [[UIBarButtonItem alloc] initWithTitle:nil style:UIBarButtonItemStylePlain target:nil action:nil];
    self.navigationItem.backBarButtonItem = item;

}
```

**方案二**

1. 自定义 `UINavigationController`
2. 遵守 `<UINavigationBarDelegate>` 协议
3. 实现下面方法:

```objectivec
#pragma mark --------- UINavigationBarDelegate

- (BOOL)navigationBar:(UINavigationBar *)navigationBar shouldPushItem:(UINavigationItem *)item {
    
    //设置导航栏返回按钮文字为透明的，可能造成导航标题不居中的问题
    [[UIBarButtonItem appearance] setTitleTextAttributes:@{NSForegroundColorAttributeName: [UIColor clearColor]} forState:UIControlStateNormal];
    [[UIBarButtonItem appearance] setTitleTextAttributes:@{NSForegroundColorAttributeName: [UIColor clearColor]} forState:UIControlStateHighlighted];
    
    return YES;
}
```

**方案三（推荐）**

1. 给 `UIViewController` 添加类别（这里的类别不需要导入可直接使用）
2. 然后在 `load` 方法里面用 `Method Swzilling` 方法替换交换 `ViewDidAppear` 方法，代码如下：

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

参考：[去掉 iOS 导航栏返回按钮文本三种方案 - 展菲](https://mp.weixin.qq.com/s/VoVzBNlqWkk522t_aLC35A "去掉 iOS 导航栏返回按钮文本三种方案")


## 那些Bug
整理编辑：[FBY展菲](https://github.com/fanbaoying)

###  排查 iOS 国际化文本格式报错

**问题背景**

项目实现国际化功能，编译时遇到错误，read failed: Couldn't parse property list because the input data was in an invalid format

![](https://upload-images.jianshu.io/upload_images/2829694-32beb8f3d6c7d838.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

根据错误提示告诉我们是数据格式的问题。具体问题出现在那里下面分析一下

**问题分析**

数据格式错误一般会有下面几种情况：

* 末尾少了分号
* 字符使用了全角字符（中文字符）
* 中间少了 =
* 少了双引号或者引号没有成对出现
* 文本中出现了不必要的特殊字符

这是个小问题，主要看怎么快速查找出问题，下面给出三种方法

**问题解决**

1、肉眼检索

最简单最直接的方式，肉眼检索，找到问题改正。

这种方式一般适用于文件小，内容少的情况。

如果内容多，有十几个国家的翻译文件，这种方法显然不合适。

2、减半筛查

把翻译文件中的内容每次注释掉一半，再编译，如果没有报错，问题就出现另外一半。将另外一半再注释掉一半，再编译，如此重复也能快速的排查出问题所在。

3、借助工具 Localizable

Localizable 是 Mac 上的一款桌面工具，在商店搜索 Localizable 就可以找到，使用方式也很简单，只需要将  Localizable.strings 文件拖到对应区域就可以，然后会反馈哪一行格式有问题，对应解决就好，非常方便。

![](https://upload-images.jianshu.io/upload_images/2829694-2d5c9279f35f29d3.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

参考：[iOS 国际化文本格式报错 - 展菲](https://mp.weixin.qq.com/s/qFfXwI9sLqxm9wTpsSS6rQ "iOS 国际化文本格式报错")

## 编程概念

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)

### 什么是 Webpack

近年来 Web 应用变得更加复杂与庞大，Web 前端技术的应用范围也更加广泛。 从复杂庞大的管理后台到对性能要求苛刻的移动网页，再到类似 ReactNative 的原生应用开发方案，Web 前端工程师在面临更多机遇的同时也会面临更大的挑战。 通过直接编写 JavaScript、CSS、HTML 开发 Web 应用的方式已经无法应对当前 Web 应用的发展。近年来前端社区涌现出许多新思想与框架，比如使用模块化把一个复杂的系统分解到多个模块以方便编码，使用 React、Vue、Angular2 等 JS 框架，以及一些新语言的诞生如 ES6、TypeScript、Flow、SCSS 等。

Webpack 是一个打包模块化 JavaScript 的工具，在 Webpack 里一切文件皆模块，通过 Loader 转换文件，通过 Plugin 注入钩子，最后输出由多个模块组合成的文件。Webpack 专注于构建模块化项目。

其官网的首页图很形象的画出了 Webpack 是什么，如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210612002026.png)

一切文件：JavaScript、CSS、SCSS、图片、模板，在 Webpack 眼中都是一个个模块，这样的好处是能清晰的描述出各个模块之间的依赖关系，以方便 Webpack 对模块进行组合和打包。 经过 Webpack 的处理，最终会输出浏览器能使用的静态资源。

Webpack 具有很大的灵活性，能配置如何处理文件，大致使用如下：

```
module.exports = {
  // 所有模块的入口，Webpack 从入口开始递归解析出所有依赖的模块
  entry: './app.js',
  output: {
    // 把入口所依赖的所有模块打包成一个文件 bundle.js 输出 
    filename: 'bundle.js'
  }
}
```

Webpack 的优点是：

* 专注于处理模块化的项目，能做到开箱即用一步到位；
* 通过 Plugin 扩展，完整好用又不失灵活；
* 使用场景不仅限于 Web 开发；
* 社区庞大活跃，经常引入紧跟时代发展的新特性，能为大多数场景找到已有的开源扩展；
* 良好的开发体验。

Webpack 的缺点是只能用于采用模块化开发的项目。

参考：[gwuhaolin/dive-into-webpack](https://github.com/gwuhaolin/dive-into-webpack "gwuhaolin/dive-into-webpack")


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


这篇文章对签名校验讲述的很详细，使用xnuspy可以hook系统缺页中断函数，这可能对我们日后的性能分析有帮助。


[iOS LLDB中反反调试分析与实现](https://mp.weixin.qq.com/s/egrQxxJSympB-L6BdVDQVA "iOS LLDB中反反调试分析与实现")  -- 来自公众号：看雪学院


__TEXT段是只读的，到底能不能在运行期间修改呢？可以看看这篇文章。


## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

## SwiftLee

链接：https://www.avanderlee.com/

一个分享关于 Swift、iOS 和 Xcode 技巧和窍门的每周博客，博客的文章写得清晰易懂，排版、配图和动画质量也很高。值得关注一下。同时作者也是 [Swift for Good](https://www.swiftforgood.com/) 的联合作者，是一本将所有全部收入将用于慈善的 Swift 学习书籍，有兴趣也可以看一下😺。

## WWDC21 内参

链接：https://xiaozhuanlan.com/wwdc21

一年一度的 WWDC 又来啦！今年官方一共会放出 200 个 Session，内参作者们会根据必要性和实际情况选择合适的内容进行深度解读，让大家快速了解 WWDC21 中那些值得关注的 Session。现在也开放了今年 《WWDC21 内参》 [购买链接](https://xiaozhuanlan.com/wwdc21)，目前限时售价是 9.9 元。所有的《WWDC 内参》的收入，都会归为参与的作者所有。摸鱼周报的多位编辑们也会作为内参作者参与其中😁。

## 工具推荐

整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### Diffchecker

**地址**：https://www.diffchecker.com/

**软件状态**：收费

**介绍**
Diffchecker 是一款简单好用的差异比较工具，使用可帮助用户快速的比较您的文本文件、文档、PDF、照片、图形和扫描等，并且界面简单直观，输入两个文件的内容，然后单击“查找差异”即可，并且具有绝对的安全性，能够保障您的文件安全，具有统一差异、字符级差异、文件夹差异、导出为PDF、语法高亮、文件导入、无广告等优势

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/1623388796593.jpg)


## 联系我们

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

[摸鱼周报第六期](https://zhangferry.com/2021/03/14/iOSWeeklyLearning_6/)

[摸鱼周报第七期](https://zhangferry.com/2021/03/28/iOSWeeklyLearning_7/)

[摸鱼周报第八期](https://zhangferry.com/2021/04/11/iOSWeeklyLearning_8/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
