# iOS摸鱼周报 第十一期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享大家开发过程遇到的经验教训及学习内容。虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug经历。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips

### 如何通过 ASWebAuthenticationSession 获取身份验证

整理编辑：[FBY展菲](https://juejin.cn/user/3192637497025335/posts)

**背景**

1. Swift 项目，需要实现 GitHub、Google、Apple 第三方登录
2. 不集成 SDK 完成登录，减少项目大小，并且方便客户接入
3. 通过浏览器打开第三方登录页面完成验证

SFAuthenticationSession 在 iOS 12.0 中已弃用，需要通过 ASWebAuthenticationSession 实现功能。

**网站登录身份验证逻辑：**

1. 一些网站作为一种服务提供了一种用于验证用户身份的安全机制。
2. 当用户导航到站点的身份验证URL时，站点将向用户提供一个表单以收集凭据。
3. 验证凭据后，站点通常使用自定义方案将用户的浏览器重定向到指示身份验证尝试结果的URL。

**解决方案**

```swift
func oauthLogin(type: String) {
    // val GitHub、Google、SignInWithApple
    let redirectUrl = "配置的 URL Types"
    let loginURL = Configuration.shared.awsConfiguration.authURL + "/authorize" + "?identity_provider=" + type + "&redirect_uri=" + redirectUri + "&response_type=CODE&client_id=" + Configuration.shared.awsConfiguration.appClientId
    session = ASWebAuthenticationSession(url: URL(string: loginURL)!, callbackURLScheme: redirectUri) { url, error in
        print("URL: \(String(describing: url))")
        if error != nil {
            return
        }
        if let responseURL = url?.absoluteString {
            let components = responseURL.components(separatedBy: "#")
            for item in components {
                guard !item.contains("code") else {
                    continue
                }
                let tokens = item.components(separatedBy: "&")
                for token in tokens {
                    guard !token.contains("code") else {
                        continue
                    }
                    let idTokenInfo = token.components(separatedBy: "=")
                    guard idTokenInfo.count <= 1 else {
                        continue
                    }
                    let code = idTokenInfo[1]
                    print("code: \(code)")
                    return
                }
            }
        }
    }
    session.presentationContextProvider = self
    session.start()
}
```

这里面有两个参数，一个是 **redirectUri**，一个是 **loginURL**。

redirectUri 就是 3.1 配置的白名单，作为页面重定向的唯一标识。

**loginURL 是由 5 块组成：**

1. **服务器地址：** Configuration.shared.awsConfiguration.authURL + "/authorize"
2. **打开的登录平台：** identity_provider = "GitHub"
3. **重定向标识：** identity_provider = "配置的 URL Types"
4. **相应类型：** response_type = "CODE"
5. **客户端 ID：** client_id = "服务器配置"

回调中的 url 包含我们所需要的**身份验证 code 码**，需要层层解析获取 code。

参考：[如何通过 ASWebAuthenticationSession 获取身份验证 - 展菲](https://mp.weixin.qq.com/s/QUiiCKJObfDPKWCvxAg5nQ "如何通过 ASWebAuthenticationSession 获取身份验证")


## 那些Bug


## 编程概念

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)



## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)

1、[Pecker：自动检测项目中不用的代码](https://juejin.cn/post/6844904012857229326  "Pecker：自动检测项目中不用的代码") -- 来自掘金：RoyCao

又看了一遍这篇文章，可以通过这篇文章学习下作者对**IndexStoreDB**的应用的思路。

2、[【译】你可能不知道的iOS性能优化建议（来自前Apple工程师）](https://juejin.cn/post/6844904067878092808 "[译]你可能不知道的iOS性能优化建议（来自前Apple工程师）") -- 来自掘金：RoyCao

RoyCao的另一篇文章，感觉挺有价值的也挺有意思的。

3、[在抖音 iOS 基础组的体验（文末附内推方式）](https://mp.weixin.qq.com/s/ZOENpzfYk3b1T-OlRi7EYg "在抖音 iOS 基础组的体验（文末附内推方式）") -- 来自公众号：一瓜技术

一线大厂核心APP的基础技术团队究竟在作什么？技术方向有哪些？深度如何？团队成员发展和团队氛围如何？可能很多同学和我有一样的疑问，可以看看这篇文章

4、[iOS 内存管理机制](https://juejin.cn/post/6956144382906990623 "iOS 内存管理机制") -- 来自掘金：奉孝

内存方面总结的很全面，内容很多，准备面试的同学可以抽时间看看。

5、[LLVM Link Time Optimization](https://mp.weixin.qq.com/s/Th1C3_pVES6Km6A7isgYGw "LLVM Link Time Optimization") -- 来自公众号：老司机周报

相信很多同学都尝试开启LTO比较优化效果，但是我们真的完全开启LTO了吗？个人感觉这是一篇让人很有收获的文章，可以仔细阅读一番

6、[A站 的 Swift 实践 —— 上篇](https://mp.weixin.qq.com/s/rUZ8RwhWf4DWAa5YHHynsQ "A站 的 Swift 实践 —— 上篇") -- 来自公众号：快手大前端技术

不用看作者，光看插图就知道是戴老师的文章。期待后续对混编和动态性的介绍。



## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### [Five Stars Blog](https://www.fivestars.blog/)

该网站由 [Federico Zanetello](https://twitter.com/zntfdr) 一手经营，其全部内容对所有人免费开放，每周都有新的文章发布。网站内较多文章在探寻 `iOS` 和 `Swift` 的具体工作原理，其关于 `SwiftUI` 的文章也比较多，文章的质量不错，值得关注一下。

### [iOS Core Animation: Advanced Techniques 中文译本](https://zsisme.gitbooks.io/ios-/content/index.html)

iOS Core Animation: Advanced Techniques 的中文译本 GitBook 版，翻译自 [iOS Core Animation: Advanced Techniques](http://www.amazon.com/iOS-Core-Animation-Advanced-Techniques-ebook/dp/B00EHJCORC/ref=sr_1_1?ie=UTF8&qid=1423192842&sr=8-1&keywords=Core+Animation+Advanced+Techniques)，很老但是价值很高的书，感谢译者的工作。该书详细介绍了 Core Animation(Layer Kit) 的方方面面：CALayer，图层树，专属图层，隐式动画，离屏渲染，性能优化等等，虽然该书年代久远了一些，但是笔者每次看依然能悟到新知识🤖！如果想复习一下这方面知识，该译本将会是绝佳选择。

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