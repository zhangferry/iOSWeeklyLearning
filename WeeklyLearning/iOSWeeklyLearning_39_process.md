# iOS摸鱼周报 第三十九期

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

整理编辑：[zhangferry](https://zhangferry.com)

### HTTPS 建立的过程中客户端是如何保证证书的合法性的

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

要验证 *DigiCert Global Root CA*（简称A） 签发了 *TrustAsia TLS RSA CA*（简称B） ，可以利用 RSA 的非对称性。这里分两步：签发、验证。

签发：A 对 B 签发时，由 B 的内容生成一个 Hash 值，然后 A 使用它的私钥对这个 Hash 值进行加密，生成签名，放到B证书里。

验证：使用 A 的公钥（操作系统内置在钥匙串中）对签名进行解密，得到签发时的 Hash 值 H1，然后单独对 B 内容进行 Hash 计算，得到 H2，如果 H1== H2，那么就说明证书没有被篡改过，验证通过。

这些过程中使用到的对称加密算法和 Hash 算法都会在证书里说明。同理逐级验证，直到最终的证书节点，都没问题就算是证书验证通过了。流程如下：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20211223174908.png)

图片来源：https://cheapsslsecurity.com/blog/digital-signature-vs-digital-certificate-the-difference-explained/

## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

## 工具推荐

### xcinfo

推荐人：faimin

**地址**：https://github.com/xcodereleases/xcinfo

**软件状态**：开源、免费

**推荐语**：

`Xcodes` 的另一种选择，方便我们直接从苹果官网下载 Xcode。 据称下载速度比 `Xcodes` 更快。

![xcinfo](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/inf.png)

### Mark Text

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

**地址**：https://marktext.app/

**软件状态**：开源、免费

**软件介绍**：

一个简单而优雅的开源`markdown`编辑器，专注于速度和可用性，适用于`Linux`, `macOS`和 `Windows`。

其和`Typora`一样，也是单窗的形式。

![Mark Text](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/marktext.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
