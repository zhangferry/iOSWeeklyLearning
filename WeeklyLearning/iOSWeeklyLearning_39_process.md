# iOS摸鱼周报 第三十九期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

### 本期概要

> * Tips：混编｜为 Swift 改进 Objective-C API。
> * 面试模块：HTTPS 证书有效性的验证过程。
> * 优秀博客：Core Data、Realm、MMKV 这几个库相关的一些介绍。
> * 学习资料：一个学习正则表达式的网站。
> * 开发工具：一个安装 Xcode 的 CLI 工具 `xcinfo`，一款开源的 Markdown 编辑工具 Mark Text。

## 开发Tips

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

### 混编｜为 Swift 改进 Objective-C API

宏 `NS_REFINED_FOR_SWIFT` 于 Xcode 7 引入，它可用于在 Swift 中隐藏 Objective-C API，以便在 Swift 中提供相同 API 的更好版本，同时仍然可以使用原始 Objective-C 实现。具体的应用场景有：

- 你想在 Swift 中使用某个 Objective-C API 时，使用不同的方法声明，但要使用类似的底层实现。你还可以将 Objective-C 方法在 Swift 中变成属性，例如将 Objective-C 的 `+ (instancetype)sharedInstance;` 方法在 Swift 中的变为 `shared` 属性。
- 你想在 Swift 中使用某个 Objective-C API 时，采用一些 Swift 的特有类型，比如元组。例如，将 Objective-C 的  `- (void)getRed:(nullable CGFloat *)red green:(nullable CGFloat *)green blue:(nullable CGFloat *)blue alpha:(nullable CGFloat *)alpha;` 方法在 Swift 中变为一个只读计算属性，其类型是一个包含 rgba 四个元素的元组 `var rgba: (red: CGFloat, green: CGFloat, blue: CGFloat, alpha: CGFloat)`，以更方便使用。
- 你想在 Swift 中使用某个 Objective-C API 时，重新排列、组合、重命名参数等等，以使该 API 与其它 Swift API 更匹配。 
- 利用 Swift 支持默认参数值的优势，来减少导入到 Swift 中的一组 Objective-C API 数量。例如，SDWebImage 的 UIImageView (WebCache) 分类中扩展的方法，在导入到 Swift 中时，方法数量从 9 个减少到 5 个。
- 解决 Swift 调用 Objective-C 的 API 时可能由于数据类型等不一致导致无法达到预期的问题。例如，Objective-C 里的方法采用了 C 风格的多参数类型；或者 Objective-C 方法返回 NSNotFound，在 Swift 中期望返回 nil 等等。

`NS_REFINED_FOR_SWIFT` 可用于方法和属性。添加了 `NS_REFINED_FOR_SWIFT` 的 Objective-C API 在导入到 Swift 时，具体的 API 重命名规则如下：

* 对于初始化方法，在其第一个参数标签前面加 "__"
* 对于其它方法，在其基名前面加 "__"
* 对于属性，在其名称前加上 "__"

注意：`NS_REFINED_FOR_SWIFT` 和 `NS_SWIFT_NAME` 一起用的话，`NS_REFINED_FOR_SWIFT` 不生效，而是以 `NS_SWIFT_NAME` 指定的名称重命名 Objective-C API。

可以看看：

* [@师大小海腾：iOS 混编｜为 Swift 改进 Objective-C API](https://juejin.cn/post/7024572794943832101 "@师大小海腾：iOS 混编｜为 Swift 改进 Objective-C API")
* [@Apple：Improving Objective-C API Declarations for Swift](https://developer.apple.com/documentation/swift/objective-c_and_c_code_customization/improving_objective-c_api_declarations_for_swift "@Apple：Improving Objective-C API Declarations for Swift")

## 面试解析

整理编辑：[zhangferry](https://zhangferry.com)

### HTTPS 建立的过程中客户端是如何保证证书的合法性的？

HTTPS 的建立流程大概是这样的：

1、Client -> Server: 支持的协议和加密算法，随机数 A

2、Server -> Client: 服务器证书，随机数 B

3、Client -> Server: 验证证书有效性，随机数 C

4、Server -> Client: 生成秘钥，SessionKey = f(A + B + C)

5、使用 SessionKey 进行对称加密沟通

其中第 3 步，就需要客户端验证证书的有效性。有效性的验证主要是利用证书的信任链和签名。

#### 证书信任链

我们以 `zhangferry.com`这个网站的 HTTPS 证书为例进行分析：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20211223165541.png)

`zhangferry.com` 的证书里有一个 Issuer Name 的分段，这里表示的是它的签发者信息。其签发者名称是 *TrustAsia TLS RSA CA*，而我们可以通过上面的链式结构发现，其上层就是*TrustAsia TLS RSA CA*。再往上一层是 *DigiCert Global Root CA*，所以证书签发链就是：*DigiCert Global Root CA* -> *TrustAsia TLS RSA CA* -> *zhangferry.com*。其中 *DigiCert Global Root CA* 是根证书，它的签发者是它自己。根证书由特定结构办法，被认为是可信的。

我们的电脑在安装的时候都会预装一些 CA 根证书，查看钥匙串能够找到刚才的根证书：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20211223170915.png)

如果能够验证签发链是没有篡改的，那就可以说明当前证书有效。

#### 签发有效

要验证 *DigiCert Global Root CA*（简称 A） 签发了 *TrustAsia TLS RSA CA*（简称 B） ，可以利用 RSA 的非对称性。这里分两步：签发、验证。

签发：A 对 B 签发时，由 B 的内容生成一个 Hash 值，然后 A 使用它的私钥对这个 Hash 值进行加密，生成签名，放到 B 证书里。

验证：使用 A 的公钥（操作系统内置在钥匙串中）对签名进行解密，得到签发时的 Hash 值 H1，然后单独对 B 内容进行 Hash 计算，得到 H2，如果 H1== H2，那么就说明证书没有被篡改过，验证通过。

这些过程中使用到的对称加密算法和 Hash 算法都会在证书里说明。同理逐级验证，直到最终的证书节点，都没问题就算是证书验证通过了。流程如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20211223174908.png)

图片来源：https://cheapsslsecurity.com/blog/digital-signature-vs-digital-certificate-the-difference-explained/

### Hash 冲突的解决方案

当两个不同的内容使用同一个 Hash 算法得到相同的结果，被称为发生了 Hash 冲突。Hash 冲突通常有两种解决方案：开放定址法、链地址法。

#### 开放定址法

开放定址法的思路是当地址已经被占用时，就再重新计算，直到生成一个不被占用地址。对应公式为：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20211223221219.png)

其中 di 为增量序列，m 为散列表长度， i 为已发生的冲突次数。根据 di 序列的内容不同又分为不同的处理方案：

di = 1, 2, 3...(m-1)，为线性数列，就是线性探测法。

di = 1^2, 2^2, 3^2...k^2，为平方数列，就是平法探测法。

di = 伪随机数列，就是伪随机数列探测法。

#### 链地址法

链地址法是用于解决开放定址法导致的数据聚集问题，它是采用一个链表将所有冲突的值一一记录下来。

#### 其他方法

再哈希法：设置多个哈希算法，如果冲突就更换算法，重新计算。

建立公共溢出区：将哈希表和溢出数据分开存放，冲突内容填入溢出表中。

参考：[wiki-散列表](https://zh.wikipedia.org/wiki/%E5%93%88%E5%B8%8C%E8%A1%A8 "wiki-散列表")

## 优秀博客

整理编辑：[我是熊大](https://juejin.cn/user/1151943916921885)、[东坡肘子](https://www.fatbobman.com)

1、[数据库的设计：深入理解 Realm 的多线程处理机制](https://academy.realm.io/cn/posts/threading-deep-dive/ "数据库的设计：深入理解 Realm 的多线程处理机制") -- 来自：Realm

[@我是熊大](https://github.com/Tliens)：Realm 是一个跨平台的移动数据库引擎，性能优于 Core Data 和 FMDB；接口十分人性化，使用很方便。本文能快速加深你对 Realm 的理解，并学习到更多有用的技巧，篇幅较长，耐心读下来，定会有所收获。每当我在 Realm 遇到问题时，本文几乎都能为我解惑。

2、[如何降低Realm数据库的崩溃](https://juejin.cn/post/6844904143501557773 "如何降低Realm数据库的崩溃") -- 来自掘金：我是熊大

[@我是熊大](https://github.com/Tliens)：Realm 的崩溃，猝不及防，不仅仅是 Realm，任何数据库导致的奔溃总是个难题，总有那么零星几个让人没有头绪的 bug，本文总结了我在实际工作中遇到的问题和解决办法。

3、[MMKV--基于 mmap 的 iOS 高性能通用 key-value 组件](https://cloud.tencent.com/developer/article/1066229 "MMKV--基于 mmap 的 iOS 高性能通用 key-value 组件") -- 来自掘金：我是熊大

[@我是熊大](https://github.com/Tliens)：在开发中是否真的需要沉重的数据库？还是需要一个好用的 NSUserDefaults。如果 app 中只是简单的存储，那么基于 mmap 内存映射的 MMKV 可能更适合你，他比 NSUserDefaults 快 100 倍。

4、[iOS 数据库比较：SQLite vs. Core Data vs. Realm](https://www.oschina.net/translate/ios-databases-sqllite-vs-core-data-vs-realm?cmp "iOS 数据库比较：SQLite vs. Core Data vs. Realm") -- 来自 OSCHINA：由 我是菜鸟我骄傲、theDoctor 翻译

[@东坡肘子](https://www.fatbobman.com/)：在 iOS 中，除了官方提供的 Core Data 外，还有很多其他的持久化方案可供选择。每种方案都有其各自的特点及适用场景。本文对 Core Data、SQLite 以及 Realm 进行了横向比较，并讨论了从 SQLite 或 Core Data 转换到 Realm 的路径及注意事项。

5、[Core Data with CloudKit](https://www.fatbobman.com/posts/coreDataWithCloudKit-1/ "Core Data with CloudKit") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：Core Data with CloudKit 是苹果为 Core Data 推出的网络同步解决方案，通过将 Core Data 同 CloudKit 进行结合，仅需使用少量代码，便可实现在苹果生态内跨设备、跨平台的数据实时同步。本系列文章一共 6 篇，详细介绍了有关如何进行私有数据库同步、公共数据库同步以及在不同用户间共享数据等内容。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 学习正则表达式

**地址**：https://regexlearn.com/zh-cn

这是一个学习正则表达式的网站。它从零开始，可以让不懂正则表达式的小白简单入门，比较特别的是，它采用答题的方式，一步一步的带你了解正则表达式的工作方式以及原理，每一个小关卡都有对应的知识点和实时匹配展示，当你边写表达式的时候你就能看到对应的结果。另外这种关卡的方式也让人很有成就感，让你闯关欲罢不能！相信对不是很熟悉了解正则表达式的朋友来说是很好的学习材料。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### xcinfo

**推荐来源**：[faimin](https://github.com/faimin)

**地址**：https://github.com/xcodereleases/xcinfo

**软件状态**：开源、免费

**推荐语**：

`Xcodes` 的另一种选择，方便我们直接从苹果官网下载 Xcode。 据称下载速度比 `Xcodes` 更快。

![xcinfo](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/inf.png)

### Mark Text

**地址**：https://marktext.app/

**软件状态**：开源、免费

**软件介绍**：

一个简单而优雅的开源 `markdown` 编辑器，专注于速度和可用性，适用于 `Linux`, `macOS` 和  `Windows`。

其和 `Typora` 一样，也是单窗的形式。

![Mark Text](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/marktext.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第三十八期](https://mp.weixin.qq.com/s/a1aOOn1sFh5EaxISz5tAxA)

[iOS摸鱼周报 第三十七期](https://mp.weixin.qq.com/s/PwZ2nIHRo0GDsjMx7lSFLg)

[iOS摸鱼周报 第三十六期](https://mp.weixin.qq.com/s/K_JHs1EoEn222huWIoJRmA)

[iOS摸鱼周报 第三十五期](https://mp.weixin.qq.com/s/fCEbYkAPlK0nm7UtLKFx5A)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
