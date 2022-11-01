# iOS 摸鱼周报 #64 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：iOS NSDateFormatter 设置问题 & iOS 16 部分 pods 库提示签名问题
> * 内容推荐：
> * 摸一下鱼：

## 本期话题



## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### iOS NSDateFormatter 设置问题

最近在项目里遇到了一些时间格式的问题，场景是用户在关闭了系统时间 24 小时制的时候，以下代码会表现出不一样的执行结果：

```objective-c
NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
dateFormatter.dateFormat = @"yyyyMMddHH";
dateFormatter.timeZone = [NSTimeZone timeZoneWithName:@"Asia/Shanghai"];
NSString *dateString = [dateFormatter stringFromDate:[NSDate date]];

// 开启 24 ： 2022110123
// 关闭 24： 2022110111 PM
```

即使 `Formatter` 设置了 `HH` 格式，仍然按照 12 小时制打印结果。并没有强制 24 时间制输出。

问题原因总结为：用户的时间设置对 `Formatter`格式产生了影响。

通过查阅资料 [NSDateFormatter-Apple Developer](https://developer.apple.com/documentation/foundation/nsdateformatter "NSDateFormatter-Apple Developer")  有这样一段描述：

> When working with fixed format dates, such as RFC 3339, you set the [`dateFormat`](https://developer.apple.com/documentation/foundation/nsdateformatter/1413514-dateformat) property to specify a format string. For most fixed formats, you should also set the [`locale`](https://developer.apple.com/documentation/foundation/nsdateformatter/1411973-locale) property to a POSIX locale (`"en_US_POSIX"`), and set the [`timeZone`](https://developer.apple.com/documentation/foundation/nsdateformatter/1411406-timezone) property to UTC.

当需要设置自定义格式时，除了需要设置 `dateFormat`属性，还需要设置时区 `timeZone`和环境 `locale`属性。`locale`属性可以强制指定环境变量，避免用户自定义的系统设置对时间格式造成影响。

另外 [qa1480-apple](https://developer.apple.com/library/archive/qa/qa1480/_index.html "qa1480-apple") 中也明确说明了，自定义格式会被用户设置影响，诸如日历、小时制等本地环境。

该 QA 中还明确指导了`NSDateFormatter`的使用场景：

- 用于用户可见的时间显示
- 用于配置和解析固定格式的时间数据

对于前者，苹果不建议自定义 `dateFormat`，因为不同的地区用户，时间格式习惯是不同的，建议使用系统的预留格式，例如`setDateStyle` 和 `setTimeStyle`等。

如果是后者，则建议明确指定 `locale`属性，并且还就 `en_US`和 `en_US_POSIX`两个 **LocaleIdentifier** 的区别做了解释。

最终解决方案也就确定了，指定 `locale`属性即可。

```objective-c
  dateFormatter.locale = [NSLocale localeWithLocaleIdentifier:@"en_US_POSIX"];
```

总结：该类问题都是对 API 使用不规范导致的，类似前几年的`yyyy `和 `YYYY`的问题。大部分场景结果是一致的，特定 case 才会触发不一样的结论，导致日常很难发现这类问题。

### iOS 16 部分 pods 库提示签名问题

在最近通过 `cocoapods`导入部分库的时候，会提示签名的 error，以我业务中使用的 Google SDK 为例：

**xxx/Pods/Pods.xcodeproj: error: Signing for "GoogleSignIn-GoogleSignIn" requires a development team. Select a development team in the Signing & Capabilities editor. (in target 'GoogleSignIn-GoogleSignIn' from project 'Pods')**

解决方案也很简单，可以手动选择一下签名证书，这种需要每次 install 后手动更改，比较繁琐，另外一种方式是通过 `pod hook`关闭该签名配置项:

```ruby
post_install do |installer|
  installer.pods_project.targets.each do |target|
    target.build_configurations.each do |config|
      config.build_settings['CODE_SIGNING_ALLOWED'] = "NO"
    end
  end
end
 
```

目前该问题只出现在Xcode 14及以上的版本中，最新的 Xcode 14.1 release 仍未解决该问题。


## 内容推荐

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)


## 摸一下鱼

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #63 | Apple 企业家培训营已开放申请](https://mp.weixin.qq.com/s/nAMshUG4AjWLAAHOFPVqXg)

[iOS 摸鱼周报 #62 |  Live Activity 上线 Beta 版 ](https://mp.weixin.qq.com/s/HySX4Yaf3Zxy8Wn-LyUO0A)

[iOS 摸鱼周报 #61 |  Developer 设计开发加速器](https://mp.weixin.qq.com/s/WfwqRhC-9-isUanv8ZnvMQ)

[iOS 摸鱼周报 #60 | 2022 Apple 高校优惠活动开启](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
