# iOS摸鱼周报 第三十期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * Tips：分享 WKWebView 几个不常用的特性
> * 面试模块：
> * 优秀博客：本期博客整理了 Codable 在一些特殊场景的处理方式，Swift 处理 JSON 解析时的一些技术细节。
> * 学习资料：Xcode Build Settings 的参数说明网站；来自 Microsoft 的 Data Science 基础课程。
> * 开发工具：免费且开源的 Coding 时间追踪工具：wakapi。

## 开发Tips

### WKWebView 几个不常用的特性

整理编辑：[FBY展菲](https://github.com/fanbaoying)

**1. 截获 Web URL**

通过实现 `WKNavigationDelegate` 协议的 `definePolicyFor` 函数，我们可以在导航期间截获 URL。以下代码段显示了如何完成此操作：

```swift
func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
  let urlString = navigationAction.request.url?.absoluteString ?? ""
  let pattern = "interceptSomeUrlPattern"
  if urlString.contains(pattern){
     var splitPath = urlString.components(separatedBy: pattern)
  }
}
```

**2. 使用 WKWebView 进行身份验证**

当 WKWebView 中的 URL 需要用户授权时，您需要实现以下方法：

```swift
func webView(_ webView: WKWebView, didReceive challenge: URLAuthenticationChallenge, completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        
        let authenticationMethod = challenge.protectionSpace.authenticationMethod
        if authenticationMethod == NSURLAuthenticationMethodDefault || authenticationMethod == NSURLAuthenticationMethodHTTPBasic || authenticationMethod == NSURLAuthenticationMethodHTTPDigest {
            //Do you stuff
        }
        completionHandler(NSURLSessionAuthChallengeDisposition.UseCredential, credential)
}
```

收到身份验证质询后，您可以确定所需的身份验证类型（用户凭据或证书），并相应地使用提示或预定义凭据来处理条件。

**3. 多个 WKWebView 共享 Cookie**

WKWebView 的每个实例都有其自己的 cookie 存储。为了在 WKWebView 的多个实例之间共享 cookie，我们需要使用 WKHTTPCookieStore，如下所示：

```swift
let cookies = HTTPCookieStorage.shared.cookies ?? []
for (cookie) in cookies {
   webView.configuration.websiteDataStore.httpCookieStore.setCookie(cookie)
}
```

**4. 获取加载进度**

WKWebView 的其他功能非常普遍，例如显示正在加载的 URL 的进度更新。

可以通过侦听以下方法的 estimatedProgress 的 keyPath 值来更新 ProgressViews：

```swift
override func observeValue(forKeyPath keyPath: String?, of object: Any?, change: [NSKeyValueChangeKey : Any]?, context: UnsafeMutableRawPointer?)
```

**5. 配置 URL 操作**

使用 decisionPolicyFor 函数，您不仅可以通过电话，facetime 和邮件等操作来控制外部导航，还可以选择限制某些 URL 的打开。以下代码展示了每种情况：

```swift
func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {

guard let url = navigationAction.request.url else {
            decisionHandler(.allow)
            return
        }

 if ["tel", "sms", "mailto"].contains(url.scheme) && UIApplication.shared.canOpenURL(url) {
            UIApplication.shared.open(url, options: [:], completionHandler: nil)
            decisionHandler(.cancel)
        } else {
            if let host = navigationAction.request.url?.host {
               if host == "www.notsafeforwork.com" {
                  decisionHandler(.cancel)
               }
               else{
                   decisionHandler(.allow)
               }
            }
        }
  }
}
```

参考：[WKWebView 几个不常用的特性](https://mp.weixin.qq.com/s/FFZMz9Yc2Bm6-gAnCBsUZw)


## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

1、[或许你并不需要重写 init(from:) 方法](https://kemchenj.github.io/2018-07-09/ "或许你并不需要重写 init(from:) 方法") -- 来自：kemchenj

[@东坡肘子](https://www.fatbobman.com)：Codable 作为 Swift 的特性之一是很注重安全，也很严谨的，这就导致了它在实际使用时总会有这样那样的磕磕绊绊，我们不得不重写 `init` 方法去让它跟外部环境融洽地共存。本文介绍了一种通过重载 `decodeIfPresent` 方法以实现应对特殊类型的思路。从某种程度上来说，作者认为这甚至是比 Objective-C 的消息机制更加灵活的一种函数声明机制，而且它的影响范围是有限的，不容易对外部模块造成破坏（别声明为 open 或者 public 就没问题）。

2、[使用 Property Wrapper 为 Codable 解码设定默认值](https://onevcat.com/2020/11/codable-default/ "使用 Property Wrapper 为 Codable 解码设定默认值") -- 来自：onevcat

[@东坡肘子](https://www.fatbobman.com)：本文介绍了一个使用 Swift Codable 解码时难以设置默认值问题，并利用 Property Wrapper 给出了一种相对优雅的解决方式，来在 key 不存在时或者解码失败时，为某个属性设置默认值。这为编解码系统提供了更好的稳定性和可扩展性。最后，对 enum 类型在某些情况下是否胜任进行了简单讨论。

3、[2021 年了，Swift 的 JSON-Model 转换还能有什么新花样](https://zhuanlan.zhihu.com/p/351928579?ivk_sa=1024320u "2021 年了，Swift 的 JSON-Model 转换还能有什么新花样") -- 来自知乎：非著名程序员，作者 明林清

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：本文主要介绍 `ExCodable` 的特性和使用方法。在文章开头先介绍了常见的 json 转模型的几种方式，并对这些方式各自的优缺点进行了总结，随后引出 `ExCodable` 的特性及使用方法。

4、[json 解析有什么可说道的](https://mp.weixin.qq.com/s/_jFHgAP0vKx1Cv9XGkh_DA "json 解析有什么可说道的") -- 来自公众号：码农哈皮

[@皮拉夫大王](https://www.jianshu.com/u/739b677928f7)：文章开头先介绍了什么是 JSON。正文主要篇幅在介绍 SwiftyJSON 和 YYModel 的实现方案。文章最后引出了 HandyJSON，HandyJSON 是基于借助 `metadata` 结构来实现 JSON 转 Model 的。在这里额外提一句，如何推断 `metadata` 的结构，可以参考[GenMeta.cpp ](https://github.com/apple/swift/blob/main/lib/IRGen/GenMeta.cpp "GenMeta.cpp ")中每个结构的 layout 函数

5、[Swift中Json转Model的便捷方式](https://juejin.cn/post/7019910939340193805/ "Swift中Json转Model的便捷方式") -- 来自掘金：我是熊大

[@我是熊大](https://github.com/Tliens)：本文介绍 JSON、Model、Data、Dict 相互转换的小技巧和代码段，适合在实际工作中使用。

6、[Swift 码了个 JSON 解析器(一)](https://zhuanlan.zhihu.com/p/364032254 "Swift 码了个 JSON 解析器(一)") -- 来自知乎：OldBirds

[@我是熊大](https://github.com/Tliens)：正如作者所言，码了个 JSON 解析器,感兴趣的可以看一下。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Xcode Build Settings

地址：https://xcodebuildsettings.com/

顾名思义，这个网站的作用是展示 Xcode 所有的 Build Settings。你可以在这里按分类查看所有的设置项，搜索你想要的设置项，或查询某个设置项的值类型及其默认值。对于常常要和 Build Settings 打交道的开发者来说，这个网站很实用。

### Data-Science-For-Beginners

地址：https://github.com/microsoft/Data-Science-For-Beginners

来自 Microsoft 的 Data Science 基础课程，为期 10 周，有 20 节课。这是一个基于项目的课程，配套 40 多个小测试，通过该课程你可以学习到关于数据科学的基础知识。每节课程还有精美的插画配图，有兴趣学习 Data Science 的朋友可以尝试一下。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Data-Science-For-Beginners.png)

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### wakapi

**地址**：https://wakapi.dev/

**软件状态**：免费，[开源](https://github.com/muety/wakapi)

**软件介绍**：

Keep Track of Your Coding Time!
Wakapi is an open-source tool that helps you keep track of the time you have spent coding on different projects in different programming languages and more. Ideal for statistics freaks and anyone else.

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/screenshot.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第二十九期](https://mp.weixin.qq.com/s/TVBQgYuycelGBwTaCSfmxQ)

[iOS摸鱼周报 第二十八期](https://mp.weixin.qq.com/s/dKOkF_P5JvQnDLq09DOzaQ)

[iOS摸鱼周报 第二十七期](https://mp.weixin.qq.com/s/WvctY6OG1joJez2g6owroA)

[iOS摸鱼周报 第二十六期](https://mp.weixin.qq.com/s/PnUZLoyKr8i_smi0H-pQgQ)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
