# 苹果审核注意事项

![](https://cdn.zhangferry.com/Images/isaac-smith-6EnTPvPPL6I-unsplash.jpg)

本篇内容是关于苹果审核条款的说明，也会涉及到一部分 iOS 开发过程中的技术代码，适合项目组的运营和开发人员来了解熟悉苹果审核的整体内容。

## 苹果审核

一次完整的苹果审核流程，通常会经历这几个阶段：打包上传应用、IPA 文件包构建处理完成、准备提交、可供审核、正在等待审核、正在审核、等待开发者发布（手动发布的方式，选择自动发布会在审核过后自动更新版本）、正在为 App Store 进行处理、可供销售。其中每个阶段处理需要的时间不定，打包上传的时长取决于包体大小和网络速度，上传完成后的构建等待也与安装包大小成正比。

点击苹果后台应用“iOS App”旁边的 “+” 按钮，创建一个“准备提交”的新版本。选择合适的构建版本，提交审核后，当前 App 状态为“可供审核”，需要再次选择 “提交至 App 审核”来确认提交内容。接着便是漫长的等待，App 活动状态从“正在等待审核”到“正在审核”，一般需要一到两天的时间（快的话今天下午提交审核，几个小时内完成审核，通常是半夜一两点苹果开始审核），苹果审核时间大约是半个小时到几个小时之间。其他异常情况下时间会加长，有问题的包可能还会被延迟审核（时长随着提交次数增加：一天、两天、一周、两周、一个月，时间不固定，逐步加长），遇到这种情况大概率可以放弃了。

审核被拒有两大类情况：元数据被拒和二进制数据被拒。元数据被拒问题较小，一般只需要修改苹果后台 App 的标题、副标题、描述、关键词或者市场截图，不需要重新打包，你可以直接邮件回复苹果审核团队，再重新提交一次审核。二进制数据被拒问题较大，你需要根据被拒邮件列出的条款一一解决，代码修改完成后，最好也邮件回复苹果，再重新打包提审。

本文关注苹果开发者生态中的[审核 App Review](https://developer.apple.com/cn/app-store/review/ "苹果 App 审核")，了解常见的 App 被拒绝原因，以提高应用的审核通过率，避免 App 被苹果下架，同时防止开发者账号被封。详细的审核条款请访问查看[官方 App Store 审核指南](https://developer.apple.com/cn/app-store/review/guidelines/ "官方 App Store 审核指南")。

## 特别提醒

以下内容需要特别关注：

* 儿童应用。专门为 11 周岁及以下儿童设计的 App，类别为“儿童”。开发此类 App 需要关注儿童隐私和家长控制。相关的审核条款有儿童类别和儿童隐私，具体内容可参考[构建面向儿童的 App](https://developer.apple.com/cn/app-store/kids-apps/ "构建面向儿童的 App")（一般都不考虑做这方面的应用）。
* 确保接入的第三方 SDK 合规。对于 App 接入依赖的三方库，尽量保存更新对应 SDK 到最新的版本。 
* 关注 App 在 iPad 上的使用体验。App 在 iPhone 上正常运行，部分功能有可能会在 iPad 上会发生崩溃（苹果使用 iPad 进行审核）。
* 保证上架的 App 信息及元数据完整且正确。App 中有订阅服务，需要在描述中加上自动续费会员说明，同时写上会员服务协议与自动续费服务协议的网页地址。
* 详细的 App 审核备注。苹果审核你的 App 是否需要登录账号才能进行？留下你最新的联系信息，在审核备注中详细说明一些特别声明的事项，你也可以上传视频图片附件来帮助苹果团队进行审核。
* 禁止欺骗苹果，请不要在审核流程中作假，禁止抄袭侵权。这些行为被苹果发现后 App 会面临下架，严重的还会造成封号。

## 审核指南

对照官方的审核指南，针对 App 常见的被拒条款进行说明。

### 虚假内容

[1.1.6](https://developer.apple.com/cn/app-store/review/guidelines/#1.1.6) 条款是常见的被拒情况。应用的元数据不应包含误导用户的内容，或者有意图欺骗用户的内容。一般的问题都与 logo、截屏预览、标题副标题、关键字和描述信息相关，比如截屏不规范，蹭关键词等。

### UGC 内容

[1.2.1 用户生成的内容](https://developer.apple.com/cn/app-store/review/guidelines/#1.2.1)，社区 App 需提供用户相关的功能，如过滤屏蔽敏感信息，举报违规内容，管理员可对违规的内容或者用户进行删除。同时 App 内需提供反馈方式来方便用户联系。
有社区发帖评论相关功能的 App 必须重点关注这个条款，浏览帖子前先弹框让用户同意条款，同时做好内容审核。

### 儿童类别

[儿童类别](https://developer.apple.com/cn/app-store/review/guidelines/#1.3)的应用特别关注隐私，此类别的 App 不得向第三方发送个人身份识别信息或设备信息，同时不应包含第三方数据分析或第三方广告。

### 医疗相关

[1.4.1 医疗](https://developer.apple.com/cn/app-store/review/guidelines/#1.4.1)服务相关的应用，涉及到医疗服务相关的应用，必须提供监管文件。医疗健康，烟草电子烟等可能对他人造成人身伤害的方式，会面临更加严格的审核。

### App 完成度

“[**2.1 大礼包**](https://developer.apple.com/cn/app-store/review/guidelines/#2.1)”是常见被拒条款，需重点关注。提供的 App 最终版本应包含所有必要的元数据和有效网址。占位符文本、空白网站和其他临时内容应在提交前移除。其他类似申请了一些权限，在项目中却并没有对应的使用场景，苹果团队在审核的时候没有发现这个功能，这也会被拒（比如申请后台播放权限，需要在审核备注中注明在哪些页面或者功能上用到了）。需要登录才能进行相关操作的 App，必须在 App 审核信息初提供登录帐户。如果你创建了 App 内购买项目，请确保审核人员能够看到这些内容，否则在审核备注中说明相关原因。

### Beta 测试

对于“测试内容”、“demo”、“试用”、“该功能暂未提供”等提示内容，禁止在上线的 App 中显示，打包的时候必须要注意区分测试服和正式服！请注意，[TestFlight 测试](https://www.yuque.com/eternaljust/rpmt31/pg9siv "TestFlight 测试") 与 App Store 正式环境在内购订阅上也有一定的差异。

### 准确的元数据

2.3 也是常见的被拒条款，内容较多，有几个重点需关注：

* 隐藏功能是禁止的。确保上线的 App 功能清晰，不要欺骗苹果的审核。正常的运营配置是可以的，类似隐藏微信支付宝第三方 SDK 支付，或者网页支付都是禁止的。**重复或恶劣的违规行为会导致开发者从 Apple Developer Program 中被除名（封号）**。
* 创建正确的项目订阅产品。确保购买项目的描述、截屏和预览清晰明确。如果是包年包月这种订阅项目，建议你在同一个订阅群组里创建产品 ID，方便订阅同一的 VIP 服务升级和降级（同一群组只能订阅一个产品），参考自动续期订阅官方文档。创建产品 ID 唯一，不可重复使用。做好本地化的相关工作，填写好订阅产品的标题和描述，上传该产品的截屏（如当前订阅会员界面）审核，并写好审核备注。
* 市场图截屏和预览。一个单独尺寸的市场图最大支持 10 张截屏和 3 个预览。iPhone 手机截屏必须提供 6.5 尺寸（竖屏 1284 x 2778 像素或者横屏 2778 x 1284 像素）和 5.5 尺寸（竖屏 1242 x 2208 像素或者横屏 2208 x 1242 像素），App 视频预览为可选项，具体的格式分辨率可参考截屏规范和 App 预览规范。
* 元数据准确。关注 App 标题、副标题和关键字。不要试图用商标术语、流行 App 的名称、定价信息或其他不相关的短语来包装任何元数据。

元数据详情查看 [App Store 后台管理](https://www.yuque.com/eternaljust/rpmt31/wfzu9t "App Store 后台管理")。

### 私有 API

[2.5.1](https://developer.apple.com/cn/app-store/review/guidelines/#2.5.1) 条款规定开发的苹果 App 仅可使用[公共 API](https://developer.apple.com/cn/documentation/)，禁止使用私有 API。私有 API 相关的内容可以参考：“[关于 iOS 私有 API 扫描](https://www.jianshu.com/p/24026b30975f "关于 iOS 私有 API 扫描")”。

### 禁止热更新

针对 2.5.2 条款，类似 JSPatch 这种热更新修复技术是禁止使用的。新版本如何保证线上没有比较严重的崩溃 bug？你可以在苹果后台提审的时候选择手动发布版本更新，同时选择 7 天分阶段更新，最大支持 30 天内暂停。

### IPv6 支持

针对 2.5.5 条款，你的 App 必须支持在仅支持 IPv6 的网络上使用。苹果会在仅 IPv6 的网络环境下测试审核，如果你的服务器不支持 IPv6 ，那么发生了网络错误就会被拒。

### 内购

3.1.1 内购也是常见被拒条款。几乎所有的虚拟物品（游戏中的金币充值、解锁 VIP 高级会员、直播平台的礼物打赏），都要通过[苹果的 IAP](https://developer.apple.com/cn/in-app-purchase/ "App 内购买项目")（In-App-Purchase）来完成支付购买，并且给苹果 30% 的抽成（苹果税），除了实物可用微信支付宝购买（淘宝、京东、美团等购物）。通过技术手段进行网页 H5 支付也是被禁止的。

建议 App 中提供订阅相关的服务，同时要支持游客订阅，加入恢复订阅的功能。开启订阅服务的 App，不支持游客购买或者没有恢复功能，审核也会被苹果拒绝。在 App 应用描述中加上自动续费会员说明，同时写上会员服务协议与自动续费服务协议的网页地址。

关于 App 内购，还有一种情况是不要套路用户，比如用户在首次安装使用 App 时，欢迎页最后一页的“立即使用”变成“立即订阅”。用户一般都不会看具体的欢迎页内容详情，直接滑动到最后一页点击按钮进入 App。这种误导用户去订阅的行为是禁止的，这种套路被用户发现后会去找苹果投诉，你的 App 很有可能会被苹果下架。

### 商业资质

3.2.1 条款，没有相关的资质不要开展此类业务。比如特定租借内容 (例如电影、电视节目、音乐、图书)，保险类、金融交易、投资或资金管理的 App。

### 抄袭

4.1 条款也是被拒常客，App 的名字和图标，不能与 App Store 上的主流应用有较高的相似度，这样的问题一般会直接卡在机审元数据这一步。不要侵权，比如设计素材，字体使用了商用没有版权的。侵权被发现举报给苹果后，App 有下架的风险。

### 最低功能要求

4.2 条款，对于一个网页的简单包装是被禁止的。你的 App 必须提供自己的核心功能，同时也需要能展示出来，让苹果的审核人员看到。对于资讯新闻类 App，不能只有简单的网页链接内容展示，你可以加上登录、收藏、分享、评论、视频播放、上传图片等相关的功能。

### 马甲包

4.3 条款为重复的 App，不要大量复用了其他已上线项目中的代码，也不要做代码混淆加密，这种情况一般直接卡在机审。就算你这次侥幸通过了审核，苹果后面也会进行复查，秋后算账的代价就是影响线上项目的正常运营，或者 App 直接被下架。

### 拓展功能

项目中有键盘拓展功能需要键盘支持无网络环境下使用。使用表情贴纸不能侵权。

### App 图标更换

项目运营中如果有切换 App 图标的需求，最好的方案是设计几套 Icon，让用户在 App 设置中手动切换图标。尽量避免后台动态配置切换图标，一是所有的图标资源都需要提前打包进入 App 安装包，二是自动切换图标成功的弹窗提示需要自己 hook 代码来隐藏处理。

苹果 4.6 条款说明：

> 这项功能不可用于动态、自动或连续性更改，例如用于反映最新天气信息和日历通知等。

### 隐私

隐私保护是苹果注重的内容。在“隐私协议”中列出收集个人信息的《第三方 SDK 目录》，用户首次安装打开 App 时，必须先同意“隐私政策”和“用户协议”，然后才能进入 App 主页。

用户首次安装打开 App，应按照最小权限原则，非必要的权限不要申请，操作到指定页面，需要的时候再引导提示权限申请。不要一打开 App ，多个权限连续申请轰炸用户，必须申请的权限如定位，需要描述清楚定位功能的使用场景，同时做好用户拒绝权限后的对应逻辑，避免未处理被拒。

在设置页面提供一个列表，用户能查看到 App 可能涉及到的所有权限。用户可点击对应权限跳转设置页面中，自主选择是否开启或关闭 App 的权限。如果 App 集成来广告服务，可在隐私权限列表后面加上一个开关，显示是否关闭个性化推荐（开启关闭不影响广告收益，就是一个心理暗示作用）。再补充具体的描述信息，比如：选择关闭个性化推荐，你将不能再获得专属内容推荐服务。同时我们将不会使用你的个人信息，进行定向广告投放，但你任会收到同等数量的广告。

### 知识产权

5.2.1 是常见被拒的条款。不要在 App 中使用受保护的第三方材料 (例如商标、版权作品、专利设计）。App 访问第三方服务必须获得相关的授权许可。

如果 App 内有任何形式的抽奖活动，那么必须在活动页面底部明确表示 Apple 不是赞助者，同时表明苹果没有以任何形式参与活动。

[5.2.5 条款](https://developer.apple.com/cn/app-store/review/guidelines/#5.2.5)为 2022 年 6 月 6 日新增，如果您的 App 会显示 Apple “天气”App 的数据，则应遵循 [WeatherKit 文档](https://developer.apple.com/weatherkit/get-started/index.html#attribution-requirements "WeatherKit Documents")中的归因要求。

### 账号调查

账号被查的情况就是收到 Other - Other 的邮件。

> Apple
> Other - Other
> Hello, The review of your app is taking longer than expected. Once we have completed our review, we will notify you via Resolution Center. If you would like to inquire about the status of this review, you may file a request via the Apple Developer Contact Us page. 
> Best regards, App Store Review

触发的原因有很多，比如开始进入审核几分钟立马被拒，元数据有问题或者代码有问题。还有类似账号关联，IP 地址关联，黑卡支付账号等。详情查看[苹果审核被拒后的解决方案](https://www.yuque.com/eternaljust/rpmt31/bfnvau "苹果审核被拒后的解决方案")。

## 项目开发

一些在项目开发中需要注意的问题。

### 好评弹窗

项目中应该避免使用自己维护的好评弹框逻辑，这样会有较大的风险。禁止强制弹出好评弹窗来做任务解锁功能以及送会员。最好使用系统提供的方法，打开 App 间隔几次触发一次好评弹窗。该功能支持 iOS 10.3  系统及以上，一年内大约弹出三次左右，不要短时间内重复触发就好。

```swift
if #available(iOS 10.3, *) {
    let checkCount = UserDefaults.standard.integer(forKey: "kCheckCountKey")
    let count = 10 // 可在线配置间隔的次数
    
    UserDefaults.standard.setValue(checkCount + 1, forKey: "kCheckCountKey")
    UserDefaults.standard.synchronize()
    
    if checkCount.isMultiple(of: count) {
        SKStoreReviewController.requestReview()
    }
}
```

### 应用评价

App 内的评价弹框也尽量避免。如果你需要关注用户使用的反馈意见，可在设置中加入客服咨询。你也可以在 App 设置中引导用户点击「评价应用」，然后直接跳转到 App Store 撰写评论。

```swift
// id 后面改成对应的 Apple ID
if let url = URL(string: "https://apps.apple.com/app/id1234567890?action=write-review") {
    UIApplication.shared.open(url)
}
```

### 版本更新

App 内禁止弹出强制更新的弹窗，如「发现新版本」、「更新到最新版本」。你可以在设置列表中添加显示当前 App 版本号，引导用户点击跳转到 App Store 更新应用。跳转链接最好做成动态配置，如果应用不小心被封，用户还能通过新的链接来下载 App 替代品。如果项目新功能需要部分用户进行内测，你可以判断用户设备是否安装了 TestFlight，再弹框引导用户点击打开公开链接加入内测。

```swift
// 检测是否安装了 TestFlight，打开公开链接加入内测
if let url = URL(string: "itms-beta://"),
   let joinURL = URL(string: "https://testflight.apple.com/join/xxxxxx"),
   UIApplication.shared.canOpenURL(url) {
       UIApplication.shared.open(joinURL)
 }

// 版本更新，id 后面改成对应的 Apple ID，可动态配置链接
if let url = URL(string: "https://apps.apple.com/app/id1234567890") {
    UIApplication.shared.open(url)
}
```

### Apple 登录

App 支持微信、QQ、微博等三方登录，必须同时支持 Apple 登录，不支持会被苹果拒绝。Apple 登录按钮设计需采用苹果提供的规范，可参考 [Sign in with Apple 的设计准则和功能实现](https://steppark.net/15676959360699.html "Sign in with Apple 的设计准则和功能实现")。 

**注销删除账号说明：**

⚠️ [在您的 App 中提供帐户删除选项](https://developer.apple.com/cn/support/offering-account-deletion-in-your-app "在您的 App 中提供帐户删除选项")，2022 年 6 月 30 日起，提交审核需要支持该功能（重点是撤销令牌，注销删除账号相关的问题，请点击链接查看详情）。

如果 App 帐户删除流程是手动的（如在应用内申请删除账号，需要管理员后台审核），请告知用户删除帐户需要多长时间，并在删除完成时提供一条确认信息。

项目中集成 Sign in with Apple 登录，需要服务器与苹果验证 token，App 注销用户账号的时候再撤销令牌。对于正在订阅自动续费的用户，弹框提示相关的扣款说明，并提供以下链接以让用户管理自己的订阅：https://apps.apple.com/account/subscriptions ，防止用户删除帐户后意外被 App Store 继续扣款。

```swift
// 跳转 App Store 订阅管理
private func showManageSubscriptions() {
    if let url = URL(string: "https://apps.apple.com/account/subscriptions") {
        UIApplication.shared.open(url)
    }
}

// 或者在 App 中直接弹出当前订阅的弹窗
@available(iOS 15.0, *)
private func iOS15ShowManageSubscriptions() async {
    if let windowScene = UIApplication.shared.delegate?.window??.windowScene {
        do {
            try await AppStore.showManageSubscriptions(in: windowScene)
        } catch {
            print(error)
        }
    }
}

private func cancellation() {
    // 用户正在订阅自动续费中
    if #available(iOS 15.0, *) {
        Task {
            await iOS15ShowManageSubscriptions()
        }
    }
}
```

**准备服务器后台需要的参数：**

* 参数 clientID：Bundle ID
* 参数 teamID：Team ID
* 参数 keyID：Key ID
* p8 证书：只能下载一次，丢失后需重新配置

选择对应的项目 Identifier，在苹果开发者后台配置生成参数。

![后台需要的参数](https://cdn.zhangferry.com/Images/bundle-team-id.png)

![选择 App ID，需要先开启 Sign in with Apple 功能](https://cdn.zhangferry.com/Images/configure-key.png)

![证书只能下载一次，丢失后需重新配置](https://cdn.zhangferry.com/Images/key-id.png)

**客户端代码：**

```swift
import AuthenticationServices

// 验证 authorizationCode
@available(iOS 13.0, *)
func authorizationController(controller: ASAuthorizationController, didCompleteWithAuthorization authorization: ASAuthorization) {
    if authorization.credential is ASAuthorizationAppleIDCredential {
        if let appleIDCredential = authorization.credential as? ASAuthorizationAppleIDCredential {
            let user = appleIDCredential.user
            var params = [String : String]()
            params["type"] = "apple"
            params["openid"] = user
            if let code = appleIDCredential.authorizationCode {
                // 服务器与苹果验证
                params["apple_authcode"] = String(data: code, encoding: .utf8)
            }
//          也可验证 identityToken
//                if let token = appleIDCredential.identityToken {
//                    params["apple_identity_token"] = String(data: token, encoding: .utf8)
//                }
            login(params: params)
        }
    }
}

/*
服务器调用苹果撤销令牌接口，不管结果成功与否，苹果都返回 200，不包含其他的数据（非常坑），所以需要客户端监听注销账号后撤销令牌的通知。
服务器调用苹果撤销接口成功，苹果会发送一条通知，本地收到通知表明令牌已被撤销成功。
流程：1.服务器后台调用苹果撤销令牌接口 2.客户端本地监听并收到撤销成功的通知 3.本地再调用接口告诉服务器该令牌撤销成功了（这一步可以不做）
 */
private func addNotification() {
    if #available(iOS 13.0, *) {
        self.ex_addNotificationForName(ASAuthorizationAppleIDProvider.credentialRevokedNotification.rawValue) { _ in
            print("苹果登录已撤销令牌")
        }
    }
}
```

**PHP 服务器：**

可参考：[苹果第三方登录 Sign in with Apple 服务端验证](https://www.albinwong.com/P7q15vDYQZDBbR0o.html "苹果第三方登录 Sign in with Apple 服务端验证")，[调用苹果 API 来撤销用户令牌](https://developer.apple.com/documentation/sign_in_with_apple/revoke_tokens "调用苹果 API 来撤销用户令牌")

### 隐私协议

“隐私协议”和“用户协议”相同，在用户首次安装 App 打开使用时弹框展示。点击链接建议使用 `SafariViewController` 来打开网页，当然也可以用 `WKWebView`。

### 权限申请

以下是 info 配置文件几种常用的权限申请描述，你需要详细描述权限的使用场景，不然也很容易被拒。

> 定位
>
> Privacy - Location When In Use Usage Description：我们需要通过您的地理位置信息获取您周边的天气数据
> Privacy - Location Always Usage Description：我们需要通过您的地理位置信息获取您周边的天气数据
> Privacy - Location Always and When In Use Usage Description：我们需要通过您的地理位置信息获取您周边的天气数据
>
> 相册
>
> Privacy - Photo Library Additions Usage Description：保存图片到手机需要访问您的媒体资料库
> Privacy - Photo Library Usage Description：照片上传头像需要访问您的相册
>
> 广告标识符跟踪
>
> Privacy - Tracking Usage Description：请允许“天气预报”获取并使用您的活动跟踪，以便于向您进行个性化推送服务，从而减少无关服务对您造成的打扰

如果项目中需要申请后台播放权限，请在审核备注中注明在哪些页面或功能上用到了，最好也通过附件上传使用操作视频来帮助苹果进行审核。

### 唯一标识

项目中涉及到给服务器上传唯一标识 udid，你可以使用第三方 `ZKUDID` 封装好的 keychain 存储标识，基本上是唯一值不会改变

```swift
params["udid"] = ZKUDID.value()
```

### 数据收集

首次安装 App，打开使用时必须全屏弹框“隐私协议”，在用户点击同意后再申请系统相关权限。项目中集成的第三方 SDK 服务也必须在用户点击同意才能进行初始化，同时把用到的第三方 SDK 列表加入到用户协议中。

### 转让 App

转让 App 必须满足“该 App 的任何版本都未使用 iCloud 权限”这一条件（WWDC22 提到将移除这一限制）。项目中注意非必要不申请 iCloud 权限，防止开发者账号出问题后不能正常转让出 App。

### 通用链接

如果项目中集成微信登录 SDK，那么最新版本需要配置通用链接（Universal Link）。具体参考[微信开发文档](https://developers.weixin.qq.com/doc/oplatform/Mobile_App/Access_Guide/iOS.html "微信开发文档 Universal Links")。

## 其他事项

### IPA 包上传

平时开发测试可以直接上传或者导出 ipa 文件上传到苹果后台。如果上传遇到网络问题，可以尝试拔掉网线，同时切换无限网络到手机热点，再通过 Transporter（对于较大的安装包而言，这种方式上传快一点） 来上传。

### 账号关联

隔离开发环境，涉及马甲包或者违规应用的开发电脑或者测试手机需要更换。绑定支付被封开发者账号的银行卡也要避免再次使用。相关内容查看[苹果开发者账号](https://www.yuque.com/eternaljust/rpmt31/uzg3w5 "苹果开发者账号")。

### [开发者新闻](https://developer.apple.com/cn/news/ "苹果开发者新闻")

你可以关注苹果开发者新闻的最新动态（支持 RSS 订阅），及时了解苹果相关政策的调整。例如 App Store Cnnect 后台的更新，从 2022 年 4 月 25 日开始上传 IPA 必须使用 Xcode 13 来构建，关于从 2022 年 6 月 30 日起在 App 内需支持用户删除帐户等相关审核条款的更新。