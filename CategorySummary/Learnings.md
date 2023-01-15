***
开发小技巧收录。

### IAP内购管理

推荐来源：[zhangferry](https://github.com/zhangferry)

处理内购时，如果我们需要应用内增加取消内购的入口，因为我们无法直接取消内购，只能将用户指引至苹果的内购管理界面，由用户在那里操作。管理内购的链接有两个：

* https://buy.itunes.apple.com/WebObjects/MZFinance.woa/wa/manageSubscriptions

* https://apps.apple.com/account/subscriptions

前者是旧版链接，mac端能正常访问，但部分iPhone机型访问不了；后者为新版链接，多端都可以访问，最新版苹果文档标注推荐使用第二个链接。

### 除数为0的情况

推荐来源：[zhangferry](https://github.com/zhangferry)

```swift
var num1: Int = 0
var re1 = 10 / num1
print(re1)
```

这里会crash，出错信息为：`Fatal error: Division by zero`

```swift
var num2: Double = 0
var re2 = 10.0 / num2
print(re2)
```

将Int改为Double则不会crash，输出结果为`inf`，代表无限大

```swift
var re3 = Int(re2)
print(re3)
```

将`re2`转成Int还是会crash，出错信息为：`Fatal error: Double value cannot be converted to Int because it is either infinite or NaN`

为什么在数学中无意义的除0操作，用Int除时会crash，在Double除时不crash呢，还得到了一个inf。

首先说Double，它有两个特殊的值，inf和nan，前者代表无限大，后者代表无意义，nan是0/0的结果。

那为什么Int会crash呢，甚至在显式地将0作为除数时会被编译器识别并报错。这是因为Int不能代表无限大，Int根据CPU是32还是64位会有对应最大值 2^31-1 和 2^63-1 。所以它不能表示所有自然数，也就没有无限大的概念，所以在做除数会出现崩溃。

除了Swift，OC，C，C++，Java都是这样设计的设计，其他语言没验证，但我估计应该也应该沿用这个思路，0不能做Int的除数但可以做Float和Double这种浮点型的除数。

### 使用altool上传IPA至AppStore脚本

推荐来源：[tzqiang](https://github.com/tzqiang)

脚本主要功能为以下内容：

```bash
validate_upload_ipa() {
  validate=`xcrun altool --validate-app -f ${ipa_file} -t ios --apiKey ${api_key} --apiIssuer ${api_issuer} --verbose ;echo $?`
  echo -e "\033[34m 校验结果: ${validate} \033[0m"
  validate_code=${validate:0-1}
  
  if [[ ${validate_code} == 1 ]]; then
    echo -e "\033[31m 校验ipa文件失败！请排查错误日志进行调整 \033[0m"
  else
    echo -e "\033[32m ipa文件校验成功！准备上传中...... \033[0m"
    
    upload=`xcrun altool --upload-app -f ${ipa_file} -t ios --apiKey ${api_key} --apiIssuer ${api_issuer} --verbose ;echo $?`
    echo -e "\033[34m 上传结果: ${upload} \033[0m"
    upload_code=${upload:0-1}

    if [[ ${upload_code} == 1 ]]; then
      echo -e "\033[31m 上传ipa文件失败！请排查错误日志进行调整 \033[0m"
    else
      echo -e "\033[32m ipa文件上传成功！ \033[0m"
    fi
  fi
}
```

完整内容可以查看这里：https://github.com/tzqiang/iOS_Shell/blob/main/upload_ipa.sh

***
开发小技巧收录。

### 几个有用的git命令

**覆盖最近一次commit**

当我们开发完一部分功能时，会提交commit，如果这时发现对应的功能少改了一些东西，我们可以单独提一个commit标记这个小改动，但更推荐的做法是将这两次改动合并为同一个，对应的命令是：

```bash
$ git commit --amend -m "message"
```

**合并多个commit**

如果想将已经生成的多个commit进行合并，可以使用：

```bash
$ git rebase -i [startpoint] [endpoint]
$ git rebase -i HEAD~2 # 合并最近两次提交
```

endpoint默认为当前分支指向的HEAD节点。参数-i表示interactive(交互)，该命令执行之后会进入一个vim的交互编辑界面，下面会有一些参数的说明：

```
pick：保留该commit（缩写:p）
reword：保留该commit，但我需要修改该commit的注释（缩写:r）
edit：保留该commit, 但我要停下来修改该提交(不仅仅修改注释)（缩写:e）
squash：将该commit和前一个commit合并（缩写:s）
fixup：将该commit和前一个commit合并，但我不要保留该提交的注释信息（缩写:f）
exec：执行shell命令（缩写:x）
drop：我要丢弃该commit（缩写:d）
```

**永久删除git内二进制**

如果我们开发中忘了把某二进制文件加入`.gitignore`，而放入了git文件，那它就会一直存在。比如Pod目录，当引入很多库时，git文件会越来越大，即使后面再加入到`.gitignore`，git历史里也会存有记录，这个是无法删除的。好在git给我们提供了一个补救措施：

```
git filter-branch --tree-filter 'rm -f target.file'
```

后面的命令里可以执行删除语句。注意该命令会重写整个git历史，多人协作时更应该慎用。

**git仓库迁移**

git仓库的迁移，在一些git管理平台像是gitlab和github是有的，推荐使用平台提供的方法，如果没有的话我们则可以使用git语句操作：

```bash
git clone --bare git@host/old.git # clone原仓库的裸仓库
cd old.git
git push --mirror git@host/new.git # 使用mirror参数推送至新仓库
```

### 国际化/本地化注意事项

国际化和本地化之间的区别虽然微妙，但却很重要。国际化意味着产品有适用于任何地方的“潜力”；本地化则是为了更适合于“特定”地方的使用，而另外增添的特色。用一项产品来说，国际化只需做一次，但本地化则要针对不同的区域各做一次。这两者之间是互补的，并且两者合起来才能让一个系统适用于各地。

除了大头的语言本地化，还有布局、字符、日期、数字等本地化工作，更多了解可以参考[iOS国际化及本地化（一）不同语言的差异处理及测试](https://zhangferry.com/2019/08/19/localization_guide/ "iOS国际化及本地化（一）不同语言的差异处理及测试")。

这里讲两点，日期格式和数字表示：

#### 日期格式

日期格式在国内的通常记法是yyyy-mm-dd，年月日的格式，但是不同地区它们的习惯会有所不同，以下按地区划分：

![](https://cdn.zhangferry.com/Images/image.png)

参考：https://zh.wikipedia.org/wiki/%E5%90%84%E5%9C%B0%E6%97%A5%E6%9C%9F%E5%92%8C%E6%97%B6%E9%97%B4%E8%A1%A8%E7%A4%BA%E6%B3%95

### 数字表示

**千分符**在不同地区会有三种写法，逗号`,`、句号`.`、空格` ` ，**小数点**的写法有句号`.`、逗号`,`两种。通常为了便于区分，同一符号不会既做千分符，又做小数点。为了避免歧义，国际标准建议使用空格作为千分符，而不是空格或者小数点。

比如对「一百二十三万四千五百六十七点八九」进行表示：

中国、美国、澳大利亚：1,234,567**.**89

德国、荷兰：1 234 567,89或1**.**234**.**567,89

法国、意大利：1 234 567,89

各个地区对小数点的使用可以看这张图的总结：

![](https://cdn.zhangferry.com/Images/20210101223402.png)

参考资料：https://zh.wikipedia.org/wiki/%E5%B0%8F%E6%95%B8%E9%BB%9E

***
开发小技巧收录。

### 关于dateFormat

在程序开发过程中如果想将字符串和`Date`类型进行互转，就需要借助于dateFormat进行格式指定。关于dateFormat有两个国际标准，一个是[ISO8601](https://www.iso.org/iso-8601-date-and-time-format.html "ISO8601")，一个是[RFC3339](https://www.ietf.org/rfc/rfc3339.txt "RFC3339")，这两个标准基本一致，但有一处不同是ISO允许24点，而 RFC3339 为了减少混淆，限制小时必须在0至23之间。23:59过1分钟，是第二天的0:00。

| 符号  | 含义         |
| ----- | ------------ |
| YYYY  | 按周算的年份 |
| yyyy  | 自然年       |
| MM    | 月           |
| DD/dd | 天           |
| hh    | 小时         |
| mm    | 分           |
| ss    | 秒           |

其中比较特殊的YYYY，举个例子：

```swift
let dateForamtter_yyyy = DateFormatter()
dateForamtter_yyyy.timeZone = TimeZone.init(secondsFromGMT: 8)
dateForamtter_yyyy.dateFormat = "yyyy-MM-dd"

let dateString = "2015-12-31"//2015-12-30
let date = dateForamtter_yyyy.date(from: dateString)!
print(date)//2015-12-31 00:00:00 +0000

let dateForamtter_YYYY = DateFormatter()
dateForamtter_YYYY.timeZone = TimeZone.init(secondsFromGMT: 8)
dateForamtter_YYYY.dateFormat = "YYYY-MM-dd"

let dateString_YYYY = dateForamtter_YYYY.string(from: date)
print(dateString_YYYY)//2016-12-31
```

会发现使用YYYY会多出一年，这是因为YYYY是按周定义的年，即系统认为，2015年12月31号这天是2016年的第一周。测试发现1月1号所在的那周被称为新年第一周，注意是按周日为新一周第一天算的。

这与ISO8601定义的不同，它的定义为1月4号所在那一周为新年第一周，注意这里是以周一为新一周第一天算的。同时它还可以表述为新旧年交替周四在哪一年，则该周为哪一年的周。有一个`ISO8601DateFormatter`类，可以进行验证：

```swift
let dateForamtter_iso8601 = ISO8601DateFormatter()
dateForamtter_iso8601.timeZone = TimeZone.init(secondsFromGMT: 8)
dateForamtter_iso8601.formatOptions = [.withYear, .withMonth, .withDay, .withWeekOfYear]

let isoDateString = dateForamtter_iso8601.string(from: date)
print(isoDateString)//201512W5304
```

由此可以看出苹果的日期格式并没有完全遵守ISO8601规范，但它提供了特定类进行标准转换。

对于RFC 3339 格式，可以指定dateFormat和locale进行转换：

```swift
let RFC3339DateFormatter = DateFormatter()
RFC3339DateFormatter.locale = Locale(identifier: "en_US_POSIX")
RFC3339DateFormatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ssZZZZZ"
RFC3339DateFormatter.timeZone = TimeZone(secondsFromGMT: 0)
 
/* 39 minutes and 57 seconds after the 16th hour of December 19th, 1996 with an offset of -08:00 from UTC (Pacific Standard Time) */
let string = "1996-12-19T16:39:57-08:00"
let date = RFC3339DateFormatter.date(from: string)
```

参考：

https://en.wikipedia.org/wiki/ISO_week_date

https://developer.apple.com/documentation/foundation/dateformatter

***
开发小技巧收录。

### 定时清理脚本

iOS里面经常打包的机器会产生很多xcarchive文件，该文件用于生成最终的ipa，它除了包含应用外还包含dsym文件，所以一般都比较大。如果构建次数很多，他们会很容易就填满磁盘空间，导致后续的构建任务失败。针对这种现象我们可以写一个定时任务用于清除这类文件。

该过程分为两步：

**1、编写清理脚本**

这里也可以写别的你想定时执行的任务

```bash
#!/bin/sh
# 扫描文件路径
targePath=~/Library/Developer/Xcode/Archives

# 清楚文件特征，可以用正则语法
rule="*.xcarchive"

# 删除7天之前的文件
find ${targePath} -mtime +7 -name ${rule} -**exec** rm -rf {} \;
```

**2、将脚本添加到系统定时任务中**

添加定时任务需要用到cron工具，cron是一款类Unix的操作系统下的基于时间的任务管理系统。用户们可以通过cron在固定时间、日期、间隔下，运行定期任务（可以是命令和脚本）。我们在mac系统也可以使用cron。

需要注意的是由于在macOS Catalina下系统对 cron的权限进行了限制，我们需要给该执行文件添加完全磁盘访问权限才可以使用。

步骤是：

1、执行`whereis cron`，查看cron所在目录，通常它在`/usr/sbin/cron`下。

2、使用Finder 跳转到该目录

3、打开系统设置 > 安全与隐私 > 完全磁盘访问权限，打开加锁。

4、将cron程序拖入到完全磁盘访问权限右侧的程序目录。

然后将脚本设置为可执行文件：

```bash
$ chmod +x [corn_clean_file.sh](http://corn_clean_file.sh/)
```
进入crontab编辑界面
```bash
$ crontab -e
```
输入如下内容，其表示每天凌晨三点执行对应任务，保存并退出。
```
00 03 * * * /path/clean_script.sh
```

### 苹果家庭里的儿童账号退登问题

苹果有项功能是家庭账号，可以为子女设置独立的儿童账号，用于实现使用时长管理、支付管理等功能。

在测试儿童账号的使用场景时发现一个问题，如果登录了不满13周岁的儿童账号，会无法退出，即使家长端也是无法退出的。退出按钮置灰，提示“由于访问限制，无法退出登录”。联系了苹果客服才知道需要关掉家长端对于儿童账号的所有限制才可以退出账号，因为设置儿童账号时会有一个引导开启屏幕时长管理的设置，所以关掉它就可以正常退出了。

***
开发小技巧收录。

### UML图关系

UML图中的关系表达形式很容易记混，这里参照下图可以便于我们记忆：

![](https://cdn.zhangferry.com/Images/20210228170958.png)

实现关系：描述接口和类之间的关系，对应Java里interface的实现，在Swift里就是protocol的实现。

泛化关系又叫继承关系：由子类指向父类

关联关系：指对象与对对象之间的连接，一个对象包含另一个对象的引用（一般为属性）。用实心单或者双箭头表示。有时需要表示关联一个或者多个。

关联关系其他几种特殊类型：

聚合关系：体现了整体与部分的拥有关系，汽车`has a`轮胎、发动机，发动机没有汽车无法单独存在，这里轮胎和发动机通常是封装在汽车内不可见的。

组合关系：体现了整体与部分的包含关系，班级`contains a`学生，学生和班级可以独立存在，学生和班级可以单独存在，学生依赖班级，这里的关系通常两者都是可见的。

依赖关系：是一种弱关联关系（非属性），常见的局部变量，静态方法，方法参数、返回值等都是依赖关系。

### 个人开发者账号的限制

部门申请了一个备用的个人开发者账号，发现邀请别人加入时无法分配证书管理权限，经过调研发现不同类型的开发者账号权限是不同的。它们区别大致如下：

|          | 注册是否需要邓白氏码 | 费用 | 是否可以上架App Store | 支持证书类型       | 测试设备 | 协作人数   |
| -------- | -------------------- | ---- | --------------------- | ------------------ | -------- | ---------- |
| 个人账号 | 否                   | $99  | 可以                  | Ad Hoc + App Store | 100      | 开发者自己 |
| 公司账号 | 是                   | $99  | 可以                  | Ad Hoc + App Store | 100      | 多人       |
| 企业账号 | 是                   | $299 | 不可以                | In-Hourse & Ad Hoc | 无限制   | 多人       |

个人账号和公司账号功能基本一样，不同之处就在于协作人数，这里协作人数可以理解为证书的管理权限。在个人开发者账号下，我们可以在AppStoreConnect里邀请开发者，并可以选择提供给他们管理者、开发者等身份，但是在开发者资源一栏的选项却是置灰不可选的。

![](https://cdn.zhangferry.com/Images/reliao_img_1613815285985.png)



也就是说个人开发者只能由账号购买者单独管理证书。

### Swift类型的Framework合并

对于使用Objective-C开发的Framework，在真机和模拟器两种类型下，他们的区别就在于编译出的执行文件是适合于何种CPU架构。而对于Swift开发的Framework，区别则不仅限于执行文件。比如我们用真机（arm64 & armv7）编译出SnapKit这个Framework，它的目录是这样的：

```
├── Headers
│   └── SnapKit-Swift.h
├── Info.plist
├── Modules
│   ├── SnapKit.swiftmodule
│   │   ├── Project
│   │   │   ├── arm.swiftsourceinfo
│   │   │   ├── arm64-apple-ios.swiftsourceinfo
│   │   │   ├── arm64.swiftsourceinfo
│   │   │   ├── armv7-apple-ios.swiftsourceinfo
│   │   │   └── armv7.swiftsourceinfo
│   │   ├── arm.swiftdoc
│   │   ├── arm.swiftmodule
│   │   ├── arm64-apple-ios.swiftdoc
│   │   ├── arm64-apple-ios.swiftmodule
│   │   ├── arm64.swiftdoc
│   │   ├── arm64.swiftmodule
│   │   ├── armv7-apple-ios.swiftdoc
│   │   ├── armv7-apple-ios.swiftmodule
│   │   ├── armv7.swiftdoc
│   │   └── armv7.swiftmodule
│   └── module.modulemap
└── SnapKit
```

再用模拟器编译一个x86版本的SnapKit.framework。它跟上面真机版本的目录结构一样，两者除了可执行文件的区别还有Modules文件内容的区别。

`modulemap`文件是对Framework的描述，只要是Framework就必须配套一个`module.modulemap`文件。

`swiftmodule`文件用于描述Swift内部的方法声明，它是二进制格式的，会根据不同的架构生成不同的版本。该文件用于方法查找，如果缺少对应架构的swiftmodule文件，会被编译器直接识别出来。

`swiftdoc`文件是一种描述Swift注释的二进制文件，也会根据架构生成。

`swiftsourceinfo`文件是作为Swift源码的补充信息存在的，它的作用是用于定位Swift代码的行和列信息。同样，他也是二进制格式存在的。参考：https://forums.swift.org/t/proposal-emitting-source-information-file-during-compilation/28794

由此可知对于，对于多架构的合并除了目标执行文件，还至少需要合入swiftmodule，而另外两种文件可以根据需要决定是否合入。

***
开发小技巧收录。

### YYModel解析数据提供默认值

当在OC中使用YYModel解析JSON数据时，对于不存在或者返回`null`的数据都会按照`nil`处理。而有些时候我们可能不希望该字段被置为nil，而是希望提供一个默认值，比如NSString类型，如果无法解析就返回`@""`，空字符串。这在一些需要把特定参数包到NSDictionary或者NSArray里的场景不会引起崩溃，也省去了一些判断判空的代码。

实现这个目的需要两个步骤：

**1、找到特性类型的属性**

可以使用runtime提供的`property_copyAttributeList`方法，主要代码是：

```objectivec
static const char *getPropertyType(objc_property_t property) {
    //这里也可以利用YYClassPropertyInfo获取对应数据
    unsigned int attrCount;
    objc_property_attribute_t *attrs = property_copyAttributeList(property, &attrCount);
    if (attrs[0].name[0] == 'T') {
        return attrs[0].value;
    }
    return "";
}
```

通过`attrs[0].name[0] == 'T'`找到对应属性的编码类型，取出value，NSString对应的`value`是`@"NSString"`。

其他的编码类型可以参考[这里](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html#//apple_ref/doc/uid/TP40008048-CH100-SW1 "Objective-TypeEncodings")。

找到需要替换的属性就可以替换了，使用KVC的形式：

```objectivec
[self setValue:obj forKey:propertyName];
```

**2、在JSON换Model完成的时候进行默认值替换**

这段函数写到哪里合适呢，在NSObject+YYModel.h里找到了这个方法：

```objectivec
- (BOOL)modelCustomTransformFromDictionary:(NSDictionary *)dic;
```

该方法用于校验转成的Model是否符合预期，执行到这里时Model已经完成了转换，我们就可以在这里调用上面写的默认值替换方法。

**封装使用**

我已经写好了一个实现，代码在[这里](https://github.com/zhangferry/YYModel/blob/master/YYModel/NSObject%2BDefaultValue.m "NSObject+DefaultValue")。

使用的时候我们只需在Model类里引用`NSObject+DefaultValue.h`这个头文件，然后实现这个方法即可：

```objectivec
- (YYPropertyType)provideDefaultValueType {
    return YYPropertyTypeNSString;
}
```

表明我们需要将类中的所有属性在不存在的时候用空字符串代替。

**备注**：YYModel有个[issue](https://github.com/ibireme/YYModel/issues/66 "YYModel issue 66")是讨论这个问题的，但是听作者的意思，这个扩展不应该放到这个库里，所以也就没有当做PR提过去。

### iOS11支持的架构调整

i386架构现在已经用的很少了，它是intel的32位架构，对于iPhone5及以下的模拟器会使用到。虽然用的不多但很多脚本（例如CocoaPods）还是需要这个架构的支持。Xcode12已经移除了iPhone5的模拟器，如果想打出这个架构的包，默认情况是不可行的。我们可以将Build Setting里`Build Active Architecture Only`里的Debug选项置为NO，这样编译出的包是带所有架构的，包括i386。

但是当我们把包的最低支持版本设置为iOS11及以上，这时编译的包就没有i386了，应该是苹果做了移除该架构的处理。如果我们仍需要导出这个架构，就需要用`xcodebuild`命令指定架构实现了，实现命令如下：

```shell
$ xcodebuild -project ProjectName.xcodeproj -target TargetName -sdk iphonesimulator -arch i386 -configuration Debug -quiet BUILD_DIR=build
```

***
开发小技巧收录。

### 文件夹命名

最近执行shell脚本时，发生了奇怪的问题，很简单的`rm`命令却一直执行出错。看了日志发现是文件路径路径中包含`&`符号，其中某个文件夹的命名带有这个与符号。执行命令时这被作为特殊符号，被拆成了两条命令，导致出错。

所以之后文件或者文件夹命名切记不要用`&`、`|` 这些特殊字符。

### 动态库vs静态库

使用Swift的第三方库的时候我们可以选择静态或者动态库，那它们之间有什么区别呢？可以参考这篇文章

[Static VS dynamic frameworks in Swift: an in-depth analysis](https://acecilia.medium.com/static-vs-dynamic-frameworks-in-swift-an-in-depth-analysis-ff61a77eec65 "Static VS dynamic frameworks in Swift: an in-depth analysis")

测试项目有27个动态库，其中6个是用Carthage集成的，21个是用CocoaPods集成的。把他们全部转成静态库之后，软件Size降低了14.55%，启动时间降低了35%左右，主要是降低了动态库的加载时间，以下是各阶段详细的时间对比：

![](https://cdn.zhangferry.com/Images/20210328160207.png)

这里启动时间降低好理解，大小降低是因为啥呢，是因为静态库时编译器移除了无用的符号表。

因为应用内的动态库，不像系统动态库一样可以供别的App共享，所以它无法起到减少包体的作用。所以通常情况下我们都应该考虑优先使用静态库。

另外静态库可以依赖动态库，但是动态库是不能依赖静态库的。

***
开发小技巧收录。

### Github的仓库操作需求token验证

今天使用一个旧仓库访问Github时，收到一个Deprecation Notice的邮件，说是基于用户名密码的登录方式之后将不再支持，[官方通告](https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/ "2020-12-15-token-authentication-requirements-for-git-operations")可以看这里。

当前对于放在github的仓库有两种访问方式：用户名密码、Token。

用户名密码就是使用https访问git仓库。

Token是指私有访问（SSH）、OAuth、GitHub App这三种情况。

在**2021年8月13号**之后，github将不再接受用户名密码的访问形式。受影响的流程包含：

* 命令行访问
* 桌面应用访问（Github Desktop不受影响）
* 其他App或者服务使用用户名密码访问直接访问github的情况

不受影响的情况：

* 账号具有双重验证功能、SSH访问
* 使用GitHub Enterprise Server，没有收到Github的更改通知。
* 其他不支持用户名密码访问的Github App

### 配置Entitlements

entitlements是一种授权文件，用于配置相应的操作是否被允许。这个文件会在我们增加Capability的时候自动生成，它的实体是一个plist文件，用于记录我们增加的Capability。打包时entitlements会被放置到MachO文件的Code Signature段中，系统会根据这里的值判断当前应用的权限。

通常一个Target只会有一个entitlements，当如果我们想要根据不同configuration对应不同bundleId时，可能由于某些限制，他们之间的权限能力不同，这时就需要他们拥有不同的entitlements。

我们可以Copy原来的授权文件，重命名，然后在`Build Setting > Signing > Code Signing Entitlements `中配置刚才新增的entitlements文件。

![](https://cdn.zhangferry.com/Images/20210410115024.png)

### would clobber existing tag

在拉取远程tag时会报这种错误，含义是远程tag跟本地有tag冲突。解决方案是找出这个冲突的本地tag，删除掉。

可以通过`git ls-remote -t `和`git tag -l`结果进行比对，也可以直接删除本地仓库，重新拉取。

***
### 关于Xcode 12的Tab

贡献者：[highway](https://www.jianshu.com/u/1e59b1fe9df8)

不知道有多少同学困惑于Xcode 12的新tab模式，反正我是觉得这种嵌套的tab形式还不如旧版简洁明了。

![](https://cdn.jsdelivr.net/gh/zhangferry/Images/blog/xcode12-tabs-with-tabs.png)

想切回旧版本tab模式的，可以按照此文操作：
[How to fix the incomprehensible tabs in Xcode 12](https://www.jessesquires.com/blog/2020/07/24/how-to-fix-the-incomprehensible-tabs-in-xcode-12/ "How to fix the incomprehensible tabs in Xcode 12")
![](https://cdn.jsdelivr.net/gh/zhangferry/Images/blog/xcode12-tabs-prefs.png)

通过实验发现，Xcode 12下的“子tab”有以下几个特点：
> A.当单击文件打开时，tab将显示为斜体，如果双击，则以普通字体显示。斜体表示为“临时”tab，普通字体表示为“静态”tab；
>
> B.双击tab顶部文件名，或者对“临时”tab编辑后，“临时”tab将切换为“静态”tab；
>
> C.如果当前位于“静态”tab，新打开的文件会新起一个tab，并排在当前tab之后；
>
> D.新打开的“临时”文件会在原有的“临时”tab中打开，而不会新起一个“临时”tab；
>
> E.使用Command + Shift + O打开的是“临时”文件。

### modalPresentationCapturesStatusBarAppearance

贡献者：[beatman423](https://github.com/beatman423)

这边遇到的问题是非全屏present一个导航控制器的时候，咋也控制不了这个导航控制器以及其子控制器的状态栏的style和hidden。后来找到了UIViewController的这个属性，将其设置为YES就可以了。

该属性的描述是：

> Specifies whether a view controller, presented non-fullscreen, takes over control of status bar appearance from the presenting view controller. Defaults to NO.

******
### 如何通过 ASWebAuthenticationSession 获取身份验证

整理编辑：[FBY展菲](https://juejin.cn/user/3192637497025335/posts)

一般获取第三方平台身份验证的途径就是接入对应平台的 SDK，但通常接入 SDK 会伴随各种问题，包体增大，增加潜在bug等。其实大部分的服务商都有实现一种叫做 OAuth 的开放授权机制，我们可以不通过SDK，直接利用该机制完成授权流程。

符合OAuth2.0 标准的 Authorization Code 授权流程如下：

![](https://cdn.zhangferry.com/Images/20210515192755.png)

图片参考：[用iOS 内建的ASWebAuthenticationSession 实作OAuth 2.0 授权流程！](https://appcoda.com.tw/ios-oauth/ "用iOS 内建的ASWebAuthenticationSession 实作OAuth 2.0 授权流程！")

苹果把 OAuth 流程进行了封装，就是 `ASWebAuthenticationSession` 。该API 最低支持到 iOS 12.0，在这之前可以使用 `SFAuthenticationSession` ，该API 只存在于 iOS 11.0 和 iOS 12.0，目前已被废弃。使用方法如下：

```swift
func oauthLogin(type: String) {
    // val GitHub、Google、SignInWithApple
    let redirectUrl = "配置的 URL Types"
    let loginURL = Configuration.shared.awsConfiguration.authURL + "/authorize" + "?identity_provider=" + type + "&redirect_uri=" + redirectUri + "&response_type=CODE&client_id=" + Configuration.shared.awsConfiguration.appClientId
    session = ASWebAuthenticationSession(url: URL(string: loginURL)!, callbackURLScheme: redirectUri) { url, error in
        print("URL: \(String(describing: url))")
        // The callback URL format depends on the provider.
        guard error == nil, let responseURL = url?.absoluteString else {
            return
        }
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

### 使用 Charles 为 Apple TV 抓包

因为 Apple TV 没法直接设置代理，抓包的话需要借助于 [Apple Configurator 2](https://apps.apple.com/nz/app/apple-configurator-2/id1037126344?mt=12 "Apple Configurator 2") 。

在 Apple Configurator 2 里创建一个描述文件，填入电脑端的 IP 地址和端口号。按 Command + S 即可保存当前的描述文件。

![](https://cdn.zhangferry.com/Images/20210515201316.png)

到这时还无法抓包 HTTPS 请求，需要导入一个 Charles 的证书。在Charles 里 Help > SSL Proxying > Save Charles Root Certificate，选择cer格式保存起来。在 Apple Configurator 2 里创建一个证书文件，描述文件里选证书即可，配置的时候添加刚才保存的cer文件。

![](https://cdn.zhangferry.com/Images/20210515201530.png)

将这个两个文件通过 Configurator 2 安装到Apple TV里，并在 TV 端的 Settings > About 里的证书选项里进行信任。之后在 Charles 里加入对 443 端口的监听，并保持 TV 和 电脑处在同一Wifi 下即可进行抓包。

参考：https://www.charlesproxy.com/documentation/using-charles/ssl-certificates/

***
### Xcode统计耗时的几个小技巧

收集几个分析项目耗时的统计小技巧。

**统计整体编译耗时**

在命令行输入以下命令：

```bash
$ defaults write com.apple.dt.Xcode ShowBuildOperationDuration -bool YES
```

此步骤之后需要重启 Xcode 才能生效，之后我们可以在 Xcode 状态栏看到整个编译阶段的耗时。

**关键阶段耗时统计**

上面的耗时可能不够详细，Xcode 还提供了一个专门用于分析各阶段耗时的功能。

菜单栏：Product > Perform Action > Build with Timing Summary

此步骤会自动触发编译，耗时统计在编译日志导航的最底部。

其还对应一个 xcodebuild 参数`-buildWithTimingSummary`，使用该参数，编译日志里也会带上个阶段耗时的统计分析。

![](https://cdn.zhangferry.com/Images/20210522134121.png)

**Swift 耗时阈值设置**

Swift 编译器提供了以下两个参数：

- `-Xfrontend -warn-long-function-bodies=<millisecond>`
- `-Xfrontend -warn-long-expression-type-checking=<millisecond>`

配置位置如下：

![](https://cdn.zhangferry.com/Images/20210522133914.png)

分别对应了长函数体编译耗时警告和长类型检查耗时警告。

一般这里输入 100 即可，表示对应类型耗时超过 100ms 将会提供警告。

### Include of non-modular header inside framework module

在组件 Framework 化的时候，如果在 public 头文件引入了另一个未 Framework 化的组件（.a静态库）时就会触发该问题。报错日志提示 Framework 里包含了非 modular 的头文件，也就是说如果我们要做 Framework 化的话，其依赖的内容也都应该是 Framework 化的，所以这个过程应该是一个从底层库到高层逐步进行的过程。如果底层依赖无法轻易修改，可以使用一些别的手段绕过这个编译错误。

Build Settings 里搜索 non-modular，将以下`Allow Non-modular Includes In Framework Modules`选项设置为 Yes。

![](https://cdn.zhangferry.com/Images/20210522133020.png)

该选项进对 OC 模块代码有作用，对于 Swift 的引用还需要加另外一个编译参数：`-Xcc -Wno-error=non-modular-include-in-framework-module`。添加位置为：

![](https://cdn.zhangferry.com/Images/20210522133508.png)

注意这两处设置均是对项目的设置，而非组件库。另外这些方案均是临时方案，最好还是要将所有依赖库全部 modular 化。

***
整理编辑：[人魔七七](https://github.com/renmoqiqi)

### CocoaPods 常见操作

#### pod install

当我们的工程首次使用 Cocoapods 管理第三方库的时候或者当我们每次编辑 Podfile 文件的时候比如：添加，删除或者编辑一个 pod 库的时候，都需要执行该命令。

* 首次执行 `pod install` 命令，会下载安装新的 pod，并把每个 pod 的版本写到 Podfile.lock 文件里。这个文件跟踪所有的 pod 库及其依赖的版本并锁定他们的版本号。
* 在存在 Podfile.lock 的情况下执行 `pod install` 的时候，只解析 Podfile.lock 中没有列出的pod依赖项。1. 对于Podfile.lock 列出的版本，不需要检查 pods 是否有更新直接使用既有的版本安装。2. 对于Podfile.lock 未列出的版本，会根据Podfile 描述的版本安装。

Podfile 文件是 pod 执行的核心文件，它的解析逻辑推荐看这篇：[Podfile 的解析逻辑](https://www.desgard.com/2020/09/16/cocoapods-story-4.html "Podfile 的解析逻辑")。

#### pod update

pod update 可以全局升级，也可以指定 podName 单个升级。当我们执行 `pod update podName` 的时候，会忽略 Podfile.lock 文件的版本，根据 Podfile 的定义尽可能更新到最新的版本，并更新 Podfile.lock 文件。该命令会同样适配于 pod 库 podspec文件内部定义的依赖。 可以通过`pod outdated` 检测出过期的依赖版本和可升级版本。

对于 install 和 update 有两个常用参数：

* --repo-update：该参数会更新所有的 repo，例如该更新了一个私有库版本，直接 install 是找不到对应版本的，我们不想更新所有的依赖库，只想更新 对应的 repo，就可以使用该指令。该参数还对应一个特有命令：`pod repo update`。
* --no-repo-update：update 操作会默认更新所有 repo，有时这并不是必须的，且该步骤会同步 pod 公有 repo，导致比较耗时，这时就可以增加该参数，用于关闭该更新操作。

### CocoaPods 使用建议

* 推荐使用 Gemfile 管理 pod 版本，每次执行 pod 通过 bundle 进行，例如： `bundle exec pod install` 。

* 工程持有管理者对项目进行 CocoaPods 初始化的时候会有一个 Podfile.lock 这个文件我们需要纳入版本控制里。

* 如果需要更新某个库到某一个版本，由项目持有管理者采用 `pod update podName` 的方式更新某个库到一定的版本。然后提交 Podfile.lock 和 Podfile 文件。


***
### 包大小优化的一些方案

整理编辑：[人魔七七](https://github.com/renmoqiqi)

![包大小优化脑图](https://cdn.zhangferry.com/Images/%E5%AE%89%E8%A3%85%E5%8C%85%E7%98%A6%E8%BA%AB.jpeg)

因篇幅问题仅展示一张梳理过后的图片，完整文章可以查看小专栏的这篇：https://xiaozhuanlan.com/topic/6147250839。

***### 几个有用的 SQL 函数

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

给 `UIViewController` 添加类别，然后在 `load` 方法里面用 `Method Swzilling` 将 `ViewDidAppear` 方法与我们的 Hook 方法进行交换。其代码如下：

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


***
整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### 图片压缩

在 iOS 减包的 Tip 中，我们了解到资源问题是影响包大小的主要部分，而图片资源是开发过程中最常见的。使用正确的图片压缩工具能够有效的进行减包。

#### 有损压缩和无损压缩

常见的压缩工具有 TinyPNG，pngquant，ImageAlpha、ImageOptim、pngcrush、optipng、pngout、pngnq、advpng 等，根据其压缩方式分成两大阵营：有损压缩和无损压缩。

根据资料显示，TinyPNG、pngquant、ImageAlpha、pngnq 都是有损压缩，基本采用的都是 quantization 算法，将 24 位的 PNG 图片转换为 8 位的 PNG 图片，减少图片的颜色数；pngcrush、optipng、pngout、advpng 都是无损压缩，采用的都是基于 LZ/Huffman 的 DEFLATE 算法，减少图片 IDAT chunk 区域的数据。一般有损压缩的压缩率会大大高于无损压缩。

#### 压缩工具

对于项目中常见的背景图、占位图和大的标签图来说，推荐使用以下两种工具

* [TinyPNG4Mac](https://github.com/kyleduo/TinyPNG4Mac)：利用 [tinify](https://tinify.cn) 提供的 API，目前 tinify 的免费版压缩数量是单次不超过 20 张且大小不超过 5M。对于一般的 iOS 应用程序来说，足够日常开发的使用；
* [ImageOptim-CLI](https://github.com/JamieMason/ImageOptim-CLI)：自动先后执行压缩率较高的为 [ImageAlpha](http://pngmini.com/) 的有损压缩 加上 [ImageOptim](https://imageoptim.com/) 的无损压缩。

可以通过查看[这个表格](http://jamiemason.github.io/ImageOptim-CLI/comparison/png/photoshop/desc/ "压缩对比表格")对比 TinyPng 和 ImageOptim-CLI 。

对于小图来说，例如我们常见的 icon 图标来说，我们通过改变其编码方式为 `RGB with palette` 来达到图片压缩效果。你可以使用 ImageOptim 改变图片的编码方式为 `RGB with palette`。

```shell
imageoptim -Q --no-imageoptim --imagealpha --number-of-colors 16 --quality 40-80 ./1.png
```

通过 [Palette Images](http://www.manifold.net/doc/mfd9/palette_images.htm "Palette Images") 深入了解 `palette`。

这里的压缩是指使用 Xcode 自带的压缩功能。

#### Xcode `负优化`

我们一般使用  Assets Catalogs 对图片资源进行管理。其会存在对应的优化方式

![](https://cdn.zhangferry.com/Images/20210626221623.png)

在构建过程中，Xcode 会通过自己的压缩算法重新对图片进行处理。在构建 Assets Catalogs 的编译产物 Assest.car 的过程中，Xcode 会使用 `actool` 对  Assets Catalogs  中的 png 图片进行解码，由此得到 Bitmap 数据，然后再运用 actool 的编码压缩算法进行编码压缩处理。所以不改变编码方式的无损压缩方法对最终的包大小来说，可能没有什么作用。

对同一张图片，在不同设备、不同 iOS 系统上 Xcode 采用了不同的压缩算法这也导致了下载时不同的设备针对图片出现大小的区别。

可以利用 `assetutil` 工具分析 `Assest.car` 来得到其具体的压缩方法：

```shell
assetutil --info ***.app/Assets.car > ***.json
```

需要注意 Json 文件中这几个参数的值 `Compression` 、`Encoding`、`SizeOnDisk`。

```json
 {
    "AssetType" : "Image",
    "BitsPerComponent" : 8,
    "ColorModel" : "RGB",
    "Colorspace" : "srgb",
    "Compression" : "deepmap2",
    "Encoding" : "ARGB",
    "Name" : "image",
    "NameIdentifier" : 51357,
    "Opaque" : false,
    "PixelHeight" : 300,
    "PixelWidth" : 705,
    "RenditionName" : "image.png",
    "Scale" : 1,
    "SHA1Digest" : "294FEE01362591334E3C3B4ECE54AF0EA8491781",
    "SizeOnDisk" : 113789,
    "Template Mode" : "automatic"
  }
```

如果启用  APP Thinning 来生成不同设备的 ipa 包，然后针对每个 ipa 包都进行一次解压缩，并获取其中的 Assets.car 导出对应的 assets.json 似乎有些冗余，你也可以利用 [京东商城的 APP 瘦身实践](https://mp.weixin.qq.com/s/xzlFQJ2b-rrw5QIszSLXXQ) 中提及的  `assetutil`  的方法从通用包的 Assets.car 文件导出指定设备的 Assets.car 文件：

```shell
assetutil --idiom phone --subtype 570 --scale 3 --display-gamut srgb --graphicsclass MTL2,2 --graphicsclassfallbacks MTL1,2:GLES2,0 --memory 1 --hostedidioms car,watch xxx/Assets.car -o xxx/thinning_assets.car
```

#### 压缩的`危害`

不要盲目的追求最大的压缩比，既需要考虑压缩出图片的质量，也需要考虑经过 Xcode 最终构成文件的真实大小。

压缩完成的图片尽量在高分辨率的设备上看看会不会有什么问题，让 UI 妹子好好看看，会不会出现噪点、毛边等现象。

如果一个图片经过有损压缩最终导致其在 Assets.car 中 `SizeOnDisk` 值变得很大的话，但其在各个设备上的表现情况又挺好，你可以尝试将其加到 bundle 中使用，并将其图片格式修改为 `Data`，这样 Xcode 就不会对其进行压缩处理了。不过不要忘记将调用方法改为 `imageWithContentOfFile:`。

***
内容贡献：[HansZhang](https://github.com/HansZhang)，校验整理：[夏天](https://juejin.cn/user/3298190611456638)

###  关于 String.count 和 NSString.length 的探究

在开发过程中使用 Swift 的 `String.count` 创建 `NSRange` 时，发现在某些语言下（印度语言，韩语）对应位置的文字没有应用预期的显示效果。通过打印同一个字符串在 NSString 类型下的 `length` 和在 Swift 的 String 类型下的 `count` 发现二者的值并不相等，`length` 比 `count` 要大一些。也就是说，在创建 NSRange 时，Swift 的 `String.count` 并不可靠，我们可以使用 `NSString.length` 解决这个问题。

#### `length` 和 `count` 的不同

那么，为什么同一个字符串的 `长度` 在 String 与 NSString 中会得到不同的值呢？我们来看一下 `String.count` 与 `NSString.length` 各自的官方定义：

> * String.count: The number of characters in a string.
> * NSString.length: The length property of an NSString returns the number of UTF-16 code units in an NSString

通过上述官方文字，我们隐约能察觉到一丝不同而继续发出疑问🤔️：

- 这个 `characters` 与 `UTF-16 code units` 是一回事么？
- 如果不是的话那各自的定义又是什么呢？

在 [Swift doc](https://docs.swift.org/swift-book/LanguageGuide/StringsAndCharacters.html#ID290 "Swift doc") 中对 Swift 中的 Character 有如下说明：

> Every instance of Swift’s Character type represents a single **extended grapheme cluster**. An extended grapheme cluster is a sequence of one or more Unicode scalars that (when combined) produce a single human-readable character.

在 Swift 1.0 版本的 [Swift String Design](https://github.com/apple/swift/blob/7123d2614b5f222d03b3762cb110d27a9dd98e24/docs/StringDesign.rst#id35 "Swift String Design") 中，也找到了相关描述：

> `Character`, the element type of `String`, represents a **grapheme cluster**, as specified by a default or tailored Unicode segmentation algorithm. This term is [precisely defined](http://www.unicode.org/glossary/#grapheme_cluster) by the Unicode specification, but it roughly means [what the user thinks of when she hears "character"](http://useless-factor.blogspot.com/2007/08/unicode-implementers-guide-part-4.html). For example, the pair of code points "LATIN SMALL LETTER N, COMBINING TILDE" forms a single grapheme cluster, "ñ".

所以我们可以粗略的理解为一个 Character 表示一个人类可读的字符，举个例子：

```swift
let eAcute: Character = "\u{E9}"                         // é
let combinedEAcute: Character = "\u{65}\u{301}"          // e followed by ́
// eAcute is é, combinedEAcute is é

let eAcute: String = "\u{E9}"
let combinedEAcute: String = "\u{65}\u{301}"
// eAcute is é, combinedEAcute is é
print(eAcute.count) // 1
print(combinedEAcute.count) // 1
print((eAcute as NSString).length) // 1
print((combinedEAcute as NSString).length) // 2
```

`é` 在 unicode 中由一个标量（unicode scalar value）表示，也有由两个标量组合起来表示的，不论哪种在 Swift 的 String 中都表示为**一个** Character。

那我们再返回来看 Swift `String.count` 的定义就好理解了，**count** 表示的是 Character 的数量，而 NSString 的 **length** 表示的是实际 unicode 标量（code point）的数量。所以在某些有很多组合标量字符的语言中（或者 emoji 表情）一个 `Character` 与一个 unicode 标量并不是一一对应的，也就造成了同一个字符 `NSString.length` 与 `String.count` 值可能不相等的问题，其实这个问题在 [Swift doc](https://docs.swift.org/swift-book/LanguageGuide/StringsAndCharacters.html#ID290) 中早有提示：

> The count of the characters returned by the **count** property isn’t always the same as the **length** property of an **NSString** that contains the same characters. The length of an NSString is based on the number of 16-bit code units within the string’s UTF-16 representation and not the number of Unicode extended grapheme clusters within the string.

我们可以看到对于字符串 Character 这样 **grapheme cluster** 式的分割字符的方式，更符合我们人类看到文字时的预期的，可以很方便的遍历真实字符，且包容多种多样的语言。但在带来便利的同时也增加了实现上的复杂度。由于每个 `Character` 长度不尽相同，`String.count` 无法像 `NSString.length` 那样使用 `O(1)` 复杂度的情况简单计算固定长度的个数，而是需要遍历每一个字符，在确定每个 Character 的边界和长度后才能推算出总个数。所以当你使用 `String.count` 时，也许要注意一下这是一个 `O(n)` 的调用。


***
整理编辑：[zhangferry](https://juejin.cn/user/3298190611456638)

### Fastlane 用法总结

图片来源：[iOS-Tips](https://github.com/awesome-tips/iOS-Tips/blob/master/resources/fastlane.png)

![](https://cdn.zhangferry.com/Images/fastlane.png)

### React Native 0.59.9 引发手机发烫问题解决思路

内容贡献：[yyhinbeijing](https://github.com/yyhinbeijing)

问题出现的现象是：RN 页面放置久了，或者反复操作不同的 RN 页面，手机会变得很烫，并且不会自动降温，要杀掉进程才会降温，版本是 0.59.9，几乎不同手机不同手机系统版本均遇到了这个问题，可以确定是 RN 导致的，但具体哪里导致的呢，以下是通过代码注释定位问题的步骤，后面数值为 CPU 占用率：

1、原生：7.2%

2、无网络无 Flatlist：7.2%

3、网络 + FlatList ：100%+

4、网络 + 无 FlatList：100%+

5、去掉 loading：2.6% — 30%，会降低

6、网络和 FlatList 全部放开，只关闭 loading 最低 7.2%，能降低，最高 63%

首先是发现网络导致 CPU 占用率很高，然后网络注释掉 RNLoading （我们自写的 loading 动画），发现内存占用不高了。就断定是 RNLoading 问题，查询发现：我们每次点击 tab 都会加载 loading，而 loading 又是动画，这样大量的动画引发内存问题。虽不是特例问题，但发现、定位、解决问题的过程仍然是有借鉴意义的，即确定范围，然后不断缩小范围。


***
### UICollectionView 的 scrollDirection 对 minimumLineSpacing 和 minimumInteritemSpacing 影响

整理编辑：[人魔七七](https://github.com/renmoqiqi)

`minimumLineSpacing` 和 `minimumInteritemSpacing` 这两个值表示含义是受滚动方向影响的，不同滚动方向，行列的排列方式不同，我们仅需记住行间距为 lineSpace 即可。下图为可视化的描述：

![](https://cdn.zhangferry.com/Images/20210716180322.png)

![](https://cdn.zhangferry.com/Images/3162666d7fa108da73e6549aea9154cf.png)

### 本地化时一些需要注意的日期设置

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

不同地域会有不同的日期格式，一般而言，我们都默认使用 `[NSLocale defaultLocale]` 来获取存储在设备设置中 `Regional Settings` 的地域，而不是指定某个地域，该行为不需要显示设置。

默认的语言/区域设置会导致 `NSCalendar`，`NSDateFormatter` 等跟区域关联的类上存在不同的展示

#### **Calendar** 的 firstWeekday

> The firstWeekday property tells you what day of the week the week starts in your locale. In the US, which is the default locale, a week starts on Sun.

当我们使用 `Calendar` 的 `firstWeekday` 属性时，需要注意，这个世界上不是所有地域其 `firstWeekday`  值都是 `1`。比如，对莫斯科来说，其  `firstWeekday`   的值是 `2`。 

如果你的日历控件并没有考虑到这些，对于某一天具体排列在一周的哪天来说，其值是不同的。

笔者之前所做的日历头部是按照周一至周日固定展示的，然后用户在俄罗斯发现日期乱了，日期与周几错乱。

后续直接定死了`firstWeekday = 1` 来功能上解决了这个问题。

#### **DateFormatter**

目前部分地域（部分欧美国家）存在**夏令时**，其会在接近春季开始的时候，将时间调快一小时，并在秋季调回正常时间。

虽然目前现有的设备支持特定的夏令时的展示，但是存在某些历史原因，如俄罗斯：

```swift
let dFmt = DateFormatter()
dFmt.dateFormat = "yyyy-MM-dd"
dFmt.timeZone = TimeZone(identifier:"Europe/Moscow")
print(dFmt.date(from:"1981-04-01") as Any) // nil
print(dFmt.date(from:"1982-04-01") as Any) // nil
print(dFmt.date(from:"1983-04-01") as Any) // nil
print(dFmt.date(from:"1984-04-01") as Any) // nil
```

对于 1981 年 - 1984 年 4 个年度的俄罗斯来说，4 月 1 号当天没有零点，会导致转化出的 `Date` 为 nil。如果我们需要做类似转换，就需注意该特殊情况。

***
### 码一个高颜值统计图

整理编辑：[FBY展菲](https://github.com/fanbaoying)

项目开发中有一些需求仅仅通过列表展示是不能满足的，如果通过图表的形式来展示，就可以更快捷的获取到数据变化情况。大部分情况我们都是使用第三方图表工具，现在我们介绍一个手动绘制的简易统计图，目前支持三种类型：**折线统计图**、**柱状图**、**环形图**。

**效果展示**

![](https://cdn.zhangferry.com/Images/20210724193757.png)

**折线统计图实现思路分析**

观察发现折线图包含这几部分：x 轴、y 轴及其刻度，背景辅助线，代表走势的折线及圆圈拐点，折线下部的整体渐变。

1、x 轴、y 轴使用 `UIBezierPath` 描绘路径，使用 `CAShapeLayer` 设置颜色及虚线样式，标签使用 UILabel 表示，需要注意每个标点的间距。

2、背景辅助线及走势线绘制同坐标轴，区别仅在于线段走势和样式稍微不同。

3、渐变方案整体渐变，然后让折线图下部作为 mask 遮罩即可实现。

柱状图和圆饼图设计思路相似，大家可以自行思考，完整代码可查看这里：[FBYDataDisplay-iOS](https://github.com/fanbaoying/FBYDataDisplay-iOS "FBYDataDisplay-iOS")。以下是折线走势的示例代码：

```objectivec
#pragma mark 画折线图
- (void)drawChartLine {
    UIBezierPath *pAxisPath = [[UIBezierPath alloc] init];
    
    for (int i = 0; i < self.valueArray.count; i ++) {
        
        CGFloat point_X = self.xScaleMarkLEN * i + self.startPoint.x;
        
        CGFloat value = [self.valueArray[i] floatValue];
        CGFloat percent = value / self.maxValue;
        CGFloat point_Y = self.yAxis_L * (1 - percent) + self.startPoint.y;
        
        CGPoint point = CGPointMake(point_X, point_Y);
        
        // 记录各点的坐标方便后边添加 渐变阴影 和 点击层视图 等
        [pointArray addObject:[NSValue valueWithCGPoint:point]];
        
        if (i == 0) {
            [pAxisPath moveToPoint:point];
        }
        else {
            [pAxisPath addLineToPoint:point];
        }
    }
    
    CAShapeLayer *pAxisLayer = [CAShapeLayer layer];
    pAxisLayer.lineWidth = 1;
    pAxisLayer.strokeColor = [UIColor colorWithRed:255/255.0 green:69/255.0 blue:0/255.0 alpha:1].CGColor;
    pAxisLayer.fillColor = [UIColor clearColor].CGColor;
    pAxisLayer.path = pAxisPath.CGPath;
    [self.layer addSublayer:pAxisLayer];
}
```

**遇到的问题**（已解决）

`reloadDatas` 方法无效，title 没变，数据源没变，移除 layer 的时候还会闪退

解决方案：在 `reloadData` 时，需要将之前缓存的数组数据 `pointArray` 清空，不然数组中保存了上次的数据。


参考：[码一个高颜值统计图 - 展菲](https://mp.weixin.qq.com/s/pzfzqdh7Tko9mfE_cKWqmg)

***### 关于 `UserDefaults` 你应该这么用
整理编辑：[CoderStar](https://juejin.cn/user/588993964541288)
#### 构造器的选用
`UserDefaults` 生成对象实例大概有以下三种方式：

```swift
open class var standard: UserDefaults { get }

public convenience init()

@available(iOS 7.0, *)
public init?(suiteName suitename: String?)
```

平时大家经常使用的应该是第一种方式，第二种方式和第一种方式产生的结果是一样的，实际上操作的都是 **APP 沙箱中 `Library/Preferences` 目录下的以 `bundle id` 命名的 `plist` 文件**，只不过第一种方式获取到的是一个单例对象，而第二种方式每次获取到都是新的对象，从内存优化来看，很明显是第一种方式比较合适，其可以避免对象的生成和销毁。

如果一个 APP 使用了一些 SDK，这些 SDK 或多或少的会使用 `UserDefaults` 来存储信息，如果都使用前两种方式，这样就会带来一系列问题：

- 各个 SDK 需要保证设置数据 KEY 的唯一性，以防止存取冲突；
- `plist` 文件越来越大造成的读写效率问题；
- 无法便捷的清除由某一个 SDK 创建的 `UserDefaults` 数据；

针对上述问题，我们可以使用第三种方式。

第三种方式根据传入的 `suiteName` 的不同会产生四种情况：

- 传入 `nil`：跟使用 `UserDefaults.standard` 效果相同；
- 传入 `bundle id`：无效，返回 nil；
- 传入 `App Groups` 配置中 `Group ID`：会操作 APP 的共享目录中创建的以 `Group ID` 命名的 `plist` 文件，方便宿主应用与扩展应用之间共享数据；
- 传入其他值：操作的是沙箱中 `Library/Preferences` 目录下以 `suiteName` 命名的 `plist` 文件。

#### `UserDefaults` 的统一管理
经常会在一些项目中看到 `UserDefaults` 的数据存、取操作，`key` 直接用的字符串魔法变量，搞到最后都不知道项目中 `UserDefaults` 到底用了哪些 key，对 key 的管理没有很好的重视起来。下面介绍两种 `UserDefaults` 使用管理的方式，一种是通过 `protocol` 及其默认实现的方式，另一种是通过 `@propertyWrapper` 的方式，因第一种方式涉及代码比较多，不便在周报中展示，这里就只介绍第二种方式。

Swift 5.1 推出了为 SwiftUI 量身定做的 `@propertyWrapper` 关键字，翻译过来就是 `属性包装器`，有点类似 java 中的元注解，它的推出其实可以简化很多属性的存储操作，使用场景比较丰富，用来管理 `UserDefaults` 只是其使用场景中的一种而已。

先上代码，相关说明请看代码注释。

```swift
@propertyWrapper
public struct UserDefaultWrapper<T> {
    let key: String
    let defaultValue: T
    let userDefaults: UserDefaults

    /// 构造函数
    /// - Parameters:
    ///   - key: 存储 key 值
    ///   - defaultValue: 当存储值不存在时返回的默认值
    public init(_ key: String, defaultValue: T, userDefaults: UserDefaults = UserDefaults.standard) {
        self.key = key
        self.defaultValue = defaultValue
        self.userDefaults = userDefaults
    }

    /// wrappedValue 是 @propertyWrapper 必须需要实现的属性
    /// 当操作我们要包裹的属性时，其具体的 set、get 方法实际上走的都是 wrappedValue 的 get、set 方法
    public var wrappedValue: T {
        get {
            return userDefaults.object(forKey: key) as? T ?? defaultValue
        }
        set {
            userDefaults.setValue(newValue, forKey: key)
        }
    }
}

// MARK: - 使用示例

enum UserDefaultsConfig {
    /// 是否显示指引
    @UserDefaultWrapper("hadShownGuideView", defaultValue: false)
    static var hadShownGuideView: Bool

    /// 用户名称
    @UserDefaultWrapper("username", defaultValue: "")
    static var username: String

    /// 保存用户年龄
    @UserDefaultWrapper("age", defaultValue: nil)
    static var age: Int?
}

func test() {
  /// 存
  UserDefaultsConfig.hadShownGuideView = true
  /// 取
  let hadShownGuideView = UserDefaultsConfig.hadShownGuideView
}
```
`UserDefaults` 的一些相关问题以及第一种利用 `protocol` 及其默认实现的管理方式的详细描述可以前往 [UserDefaults 浅析及其使用管理](https://mp.weixin.qq.com/s/Xlph6pkR8ZV02D7VYVWlOw)查看。

***
整理编辑：[夏天](https://juejin.cn/user/3298190611456638) 、[zhangferry](https://zhangferry.com)

###  `Reachability` 类的实践准则

在网络请求实践中，常见的操作是监听 `Reachability` 的状态或变换来有选择的对网络的可达性进行判断，做出阻止或暂停请求的对应操作。

一直以来，受到监听网络状态这种手段的影响，当用户在执行某些操作时，会根据获取到的用户当前的网络状态，在网络不可达（**NotReachable**）的情况下会**阻止用户发起网络请求**。

直到我看到了 AFNetworking  Issues 中的 [Docs on Reachability contradict Apple's docs](https://github.com/AFNetworking/AFNetworking/issues/2701#issuecomment-99965186) 。

我们不应该使用 `Reachability` 作为网络是否可用的判断，因为在某些情况下，其返回的状态可能不那么准确。

在  AFNetworking 的定义了关于  `Reachability` 的最佳实践：

> Reachability can be used to determine background information about why a network operation failed, or to trigger a network operation retrying when a connection is established. It should not be used to prevent a user from initiating a network request, as it's possible that an initial request may be required to establish reachability.

我们应该将其用于**网络请求后失败**的背景信息，或者在失败后用于**判断是否应该重试**。不应该用于阻止用户发起网络请求，因为可能需要初始化请求来建立**可达性**。

我们在网络请求中集成的 `Reachability` 应该用在**请求失败后**，无论是作为请求失败的提示，还是利用可达性状态的更改，作为请求重试的条件。

当我们使用 `AFNetworkReachabilityManager` 或者功能相似的 `Reachability` 类时，我们可基于此来获取当前的网络类型，如 4G 还是 WiFi。但是当我们监听到其状态变为不可达时，不应该立即弹出 `Toast` 来告诉用户当前网络不可用，而应该是当请求失败以后判断该状态是否是不可达，如果是，再提示没有网络。并且，如果该接口需要一定的连贯性的话，可以保留当前的请求参数，提示用户等待网络可达时再主动去请求。

### SQL 中的 JOIN 和 UNION

JOIN 作用是把多个表的行结合起来，各个表中对应的列有可能数据为空，就出现了多种结合关系：LEFT JOIN、RIGHT JOIN、INNER JOIN、OUTER JOIN。对应到集合的表示，它们会出现如下 7 种表示方法：

![](https://cdn.zhangferry.com/Images/20210807132907.png)

UNION 表示合并多个 SELECT 结果。UNION 默认会合并相同的值，如果想让结果逐条显示的话可以使用 UNION ALL。

有一个场景：三个表：table1、table2、table3，他们共用一个 id，table2 和 table3 为两个端的数据接口完全相同的数据，我现在要以table1 的某几个列为准，去查看对应到 table2 和 table3 与之关联的几个列的数据。SQL 语句如下：

```sql
select 
  t1.id
	t1.column_name1 as name1,
	t1.column_name2 as name2,
  t2.column_name3 as name3,
  t2.column_name4 as name4
from 
	(
	select 
    id,
		column_name1,
     column_name2
	from 
		table1_name
	) t1
left join 
	(
	select 
		union_table.* 
	from
		(
        select 
            id,
            column_name3,
            column_name4
        from 
            table2_name
        union all 
        select 
            id,
            column_name3,
            column_name4
        from 
            table3_name
        ) union_table 
	) t2 on t1.id = t2.id
```

### 在项目中区分 AppStore/Adhoc 包

在解决这个问题前，我们先要了解开发环境这个概念，iOS 的开发环境通常涉及三个维度：项目，开发端服务器，AppStore 服务器。

**项目**

即我们的 Xcode 项目，它由 Project 里的 Configuration 管理，默认有两个开发环境：Debug、Release。而我们常用的控制开发环境的宏命令如 `DEBUG` 是 Xcode 帮我们预置的值，它的设置形式为 `DEBUG=1`，这里的内容都是可以修改的。

我们新增一个名为 AppStore 的 Configuration，然后给其设置一个宏 `APPSTORE=1`，然后将之前的 Release 设置为 `ADHOC=1`，即是为这两个项目环境指定了特定的宏。

![](https://cdn.zhangferry.com/Images/20210807151150.png)

**开发端服务器**

服务器环境由服务端管理，反应到项目里，我们通常将其跟项目环境保持一致。

**AppStore 服务器**

AppStore 的开发环境根据证书形式来定，其决定了 IAP 和推送的使用场景，在最后的封包环节决定，Xcode 将其分为以下四种场景：

![](https://cdn.zhangferry.com/Images/20210807151744.png)

可以看到 Configuration 设置和封包环节是相互独立的，如果本地有三个 Configuration 的话，我们可导出的包类型数量最多为：3 x 4 = 12 种。所以如果仅仅用开发包和生成环境包描述一个包的类型肯定是不够用的，但全描述又不现实，又因封包环节在编译之后，所以我们没法提前决定包类型，所以就有了约定成俗的一些习惯。

开发包通常指：Debug + Development，

生产环境包通常指：Release + Ad Hoc 或 Release + App Store Conenct

如题目所说，如果我们要区分 Ad Hoc 和 AppStore，就需要新增 Configuration：AppStore，这样的话：

Ad Hoc 包：Release + Ad Hoc

AppStore 包：AppStore + App Store Connect

这样代码里我们就可以使用我们上面定义的宏对 Ad Hoc 和 AppStore 进行单独配置了。

既然是约定所以他们之间是不存在强关联的，所以推荐使用脚本进行打包，以避免人为导致的错误。

> 备注：经[@iHTCboy](https://ihtcboy.com/) 建议，还可以通过非 Configuration 的形式区分包类型，部分内容还未实践，测试完毕之后会将方案放到下一期内容。

***
整理编辑：[RunsCode](https://github.com/RunsCode)、 [zhangferry](https://zhangferry.com)
###  如何摊平复杂逻辑流程的设计

开发中我们通常会遇到以下问题：

* 运营活动优先级问题
* 后续慢慢在使用过程中逐渐衍生新的功能（延时，轮询，条件校验等）
* 逐级递增的回调地狱

#### Talk is cheap, show code

```swift
// 1
func function0() {
    obj0.closure { _ in
        // to do something
        obj1.closure { _ in
            // to do something                      
            obj2.closure { _ in
                ...
                objn.closure { _ in
                       ...
                }         
            }             
        }        
    }
}

or
// 2.
func function1 {
    if 满足活动0条件 {
        // to do something
    } else if 满足活动1条件 {
        // to do something
    } else if 满足活动2条件 {
        // to do something
    }
    ...
    else {
        // to do something
    }
}
```

分析上面那种代码我们可以得出以下几点结论：

* 不管怎么看都是按流程或者条件设计的
* 可读性还行，但可维护性较差，二次修改错误率较高
* 无扩展性，只能不断增加代码的行数、条件分支以及更深层级的回调
* 如果功能升级增加类似延迟、轮询，那完全不支持
* 复用性可以说无

#### 解决方案

* 实现一个容器 `Element` 搭载所有外部实现逻辑
* 容器 `Element` 以单向链表的方式链接，执行完就自动执行下一个
* 容器内聚合一个抽象条件逻辑助手 `Promise`，可随意扩展增加行为，用来检查外部实现是否可以执行链表下一个 `Element`（可以形象理解为自来水管路的阀门，电路电气开关之类，当然会有更复杂的阀门与电气开关）
* 自己管理自己的生命周期，无需外部强引用
* 容器 `Element` 可以被继承实现，参考 `NSOperation` 设计

#### Example
```swift
private func head() -> PriorityElement<String, Int> {
    return PriorityElement(id: "Head") {  (promise: PriorityPromise<String, Int>) in
        Println("head input : \(promise.input ?? "")")
        self.delay(1) { promise.next(1) }
    }.subscribe { i in
        Println("head subscribe : \(i ?? -1)")
    }.catch { err in
        Println("head catch : \(String(describing: err))")
    }.dispose {
        Println("head dispose")
    }
}
// This is a minimalist way to create element, 
// using anonymous closure parameters and initializing default parameters
private func neck() -> PriorityElement<Int, String> {
    return PriorityElement {
        Println("neck input : \($0.input ?? -1)")
        $0.output = "I am Neck"
        $0.validated($0.input == 1)
    }.subscribe { ... }.catch { err in ... }.dispose { ... }
}
// This is a recommended way to create element, providing an ID for debugging
private func lung() -> PriorityElement<String, String> {
    return PriorityElement(id: "Lung") { 
        Println("lung input : \($0.input ?? "-1")")
        self.count += 1
        //
        $0.output = "I am Lung"
        $0.loop(validated: self.count >= 5, t: 1)
    }.subscribe { ... }.catch { err in ... }.dispose { ... }
}
private func heart() -> PriorityElement<String, String> {}
private func liver() -> PriorityElement<String, String> {}
private func over() -> PriorityElement<String, String> {}
// ... ...
let head: PriorityElement<String, Int> = self.head()
head.then(neck())
    .then(lung())
    .then(heart())
    .then(liver())
    .then(over())
// nil also default value()
head.execute()
```

也许大家看到这里闻到一股熟悉的 [Goolge/Promises](https://github.com/google/promises)、[mxcl/PromiseKit](https://github.com/mxcl/PromiseKit) 或者 [RAC](https://github.com/ReactiveCocoa/ReactiveCocoa) 等味道，那么为啥不用这些个大神的框架来解决实际问题呢？

主要有一点：框架功能过于丰富而复杂，而我呢，弱水三千我只要一瓢，越轻越好的原则！哈哈

这里可以看到[详细的设计介绍](https://www.yuque.com/runscode/ios-thinking/priority_element "PrioritySessionElement设计与使用")，目前有 `OC、Swift、Java` 三个版本的具体实现。仓库地址：https://github.com/RunsCode/PromisePriorityChain 欢迎大家指正。

### 项目中区分 AppStore/Adhoc 包（二）

上期介绍了一种约定 `Configuration`，自定义预编译宏进行区分 AppStore/Adhoc 包的方法。后来尝试发现还可以通过应用内配置文件（embedded.mobileprovision）和 IAP 收据名区分包类型。

embedded.mobileprovison 仅在非 AppStore 环境存在，而且它里面还有一个参数 `aps-environment` 可以区分证书的类型是 `development` 还是 `production`，这两个值就对应了 Development 和 AdHoc 包。

另外 IAP 在非上架场景都是沙盒环境（上线 AppStoreConnect 的 TestFlight 包也是沙盒环境），是否为支付的沙盒环境我们可以用 `Bundle.main.appStoreReceiptURL?.lastPathComponent` 是否为 `sandboxReceipt` 进行判断。

所以使用上面两项内容我们可以区分：Development、AdHoc、TestFlight、AppStore。

#### 读取 embedded.mobileprovision

在命令行中我们可以利用 `security` 读取：

```bash
$ security cms -D -i embedded.mobileprovision
```

在开发阶段读取方式如下：

```swift
struct MobileProvision: Decodable {
    var name: String
    var appIDName: String
    var platform: [String]
    var isXcodeManaged: Bool? = false
    var creationDate: Date
    var expirationDate: Date
    var entitlements: Entitlements
    
    private enum CodingKeys : String, CodingKey {
        case name = "Name"
        case appIDName = "AppIDName"
        case platform = "Platform"
        case isXcodeManaged = "IsXcodeManaged"
        case creationDate = "CreationDate"
        case expirationDate = "ExpirationDate"
        case entitlements = "Entitlements"
    }
    
    // Sublevel: decode entitlements informations
    struct Entitlements: Decodable {
        let keychainAccessGroups: [String]
        let getTaskAllow: Bool
        let apsEnvironment: Environment
        
        private enum CodingKeys: String, CodingKey {
            case keychainAccessGroups = "keychain-access-groups"
            case getTaskAllow = "get-task-allow"
            case apsEnvironment = "aps-environment"
        }
        // Occasionally there will be a disable
        enum Environment: String, Decodable {
            case development, production, disabled
        }
    }
}

class AppEnv {
    
    enum AppCertEnv {
        case devolopment
        case adhoc
        case testflight
        case appstore
    }
    
    var isAppStoreReceiptSandbox: Bool {
        return Bundle.main.appStoreReceiptURL?.lastPathComponent == "sandboxReceipt"
    }
    
    var embeddedMobileProvisionFile: URL? {
        return Bundle.main.url(forResource: "embedded", withExtension: "mobileprovision")
    }
    
    var appCerEnv: AppCertEnv!
    
    init() {
      	// init or other time
        assemblyEnv()
    }
    
    func assemblyEnv() {
        if let provision = parseMobileProvision() {
            switch provision.entitlements.apsEnvironment {
            case .development, .disabled:
                appCerEnv = .devolopment
            case .production:
                appCerEnv = .adhoc
            }
        } else {
            if isAppStoreReceiptSandbox {
                appCerEnv = .testflight
            } else {
                appCerEnv = .appstore
            }
        }
    }
    
    /// ref://gist.github.com/perlmunger/8318538a02166ab4c275789a9feb8992
    func parseMobileProvision() -> MobileProvision? {
        guard let file = embeddedMobileProvisionFile,
              let string = try? String.init(contentsOf: file, encoding: .isoLatin1) else {
            return nil
        }
        
        // Extract the relevant part of the data string from the start of the opening plist tag to the ending one.
        let scanner = Scanner.init(string: string)
        guard scanner.scanUpTo("<plist", into: nil) != false  else {
            return nil
        }
        var extractedPlist: NSString?
        guard scanner.scanUpTo("</plist>", into: &extractedPlist) != false else {
            return nil
        }
        
        guard let plist = extractedPlist?.appending("</plist>").data(using: .isoLatin1) else { return nil}
        
        let decoder = PropertyListDecoder()
        do {
            let provision = try decoder.decode(MobileProvision.self, from: plist)
            return provision
        } catch let error {
            // TODO: log / handle error
            print(error.localizedDescription)
            return nil
        }
    }
}
```

***
### 在 Objective-C 中实现 Swift 中的 defer 功能

整理编辑：[RunsCode](https://github.com/RunsCode)、[zhangferry](zhangferry.com)

期望效果是下面这样，函数执行完出栈之前，要执行 defer 内定义的内容。

```objectivec
- (void)hello:(NSString *)str {
		defer {
    		// do something
		}
}
```

##### 准备工作

实现 `defer` 的前提是需要有指令能够让函数在作用域出栈的时候触发 `defer` 里的闭包内容，这里需要用到两个东西：

`__attribute__` ：一个用于在声明时指定一些特性的编译器指令，它可以让我们进行更多的错误检查和高级优化工作。

想了解更多，参考： https://nshipster.cn/__attribute__/

`cleanup(...)`：接受一个函数指针，在作用域结束的时候触发该函数指针。

#### 简单实践

到这一步，我们已经了解了大概功能了，那我们实战一下：

```cpp
#include <stdlib.h>
#include <stdio.h>

void free_buffer(char **buffer) { printf("3. free buffer\n"); }
void delete_file(int *value) { printf("2. delete file\n"); }
void close_file(FILE **fp) { printf("1. close file \n"); }

int main(int argc, char **argv) {
  	// 执行顺序与压栈顺序相反
  	char *buffer __attribute__ ((__cleanup__(free_buffer))) = malloc(20);
  	int res __attribute__ ((__cleanup__(delete_file)));
  	FILE *fp __attribute__ ((__cleanup__(close_file)));
 	  printf("0. open file \n");
  	return 0;
}
```
输出结果：

```cpp
0. open file 
1. close file 
2. delete file
3. free buffer
[Finished in 683ms]
```

但是到这一步的话，我们使用不方便啊，何况我们还是 iOSer，这个不友好啊。那么继续改造成 `Objective-C` 独有版本。

#### 实战优化

要做到上面那个理想方案，还需要什么呢？

* 代码块，那就只能是 `NSBlock`
```objectivec
typedef void(^executeCleanupBlock)(void);
```
* 宏函数 or 全局函数？想到 `Objective-C` 又没有尾随闭包这一说，那全局函数肯定不行，也就只能全局宏了
```objectivec
#ifndef defer
#define defer \
__strong executeCleanupBlock blk __attribute__((cleanup(deferFunction), unused)) = ^
#endif
...
// .m 文件
void deferFunction (__strong executeCleanupBlock *block) {
    (*block)();
}
```

OK 大功告成跑一下
```objectivec
defer {
    NSLog(@"defer 1");
};
defer { // error: Redefinition of 'blk'
    NSLog(@"defer 2");
};
defer { // error: Redefinition of 'blk'
    NSLog(@"defer 3");
};
NSLog(@"beign defer");
```
不好意思， 不行，报错 `error: Redefinition of 'blk'`，为什么？（想一想）

上最终解决版本之前还得认识两个东西

* `__LINE__` ：获取当前行号
***
### 如何清除 iOS APP 的启动屏幕缓存

整理编辑：[FBY展菲](https://github.com/fanbaoying)

每当我在我的 `iOS` 应用程序中修改了 `LaunchScreen.storyboad` 中的某些内容时，我都会遇到一个问题：

**系统会缓存启动图像，即使删除了该应用程序，它实际上也很难清除原来的缓存。**

有时我修改了 `LaunchScreen.storyboad`，删除应用程序并重新启动，它显示了新的 `LaunchScreen.storyboad`，但 `LaunchScreen.storyboad` 中引用的任何图片都不会显示，从而使启动屏显得不正常。

今天，我在应用程序的沙盒中进行了一些挖掘，发现该 `Library` 文件夹中有一个名为 `SplashBoard` 的文件夹，该文件夹是启动屏缓存的存储位置。

因此，要完全清除应用程序的启动屏幕缓存，您所需要做的就是在应用程序内部运行以下代码（已将该代码扩展到 `UIApplication` 的中）：

```swift
import UIKit

public extension  UIApplication {

    func clearLaunchScreenCache() {
        do {
            try FileManager.default.removeItem(atPath: NSHomeDirectory()+"/Library/SplashBoard")
        } catch {
            print("Failed to delete launch screen cache: \(error)")
        }
    }

}
```

在启动屏开发过程中，您可以将其放在应用程序初始化代码中，然后在不修改启动屏时将其禁用。

这个技巧在启动屏出问题时为我节省了很多时间，希望也能为您节省一些时间。

**使用介绍**

```swift
UIApplication.shared.clearLaunchScreenCache()
```

* 文章提到的缓存目录在沙盒下如下图所示：

![](https://cdn.zhangferry.com/Images/20210828174459.png)

* OC 代码,创建一个 `UIApplication` 的 `Category`

```objectivec
#import <UIKit/UIKit.h>

@interface UIApplication (LaunchScreen)
- (void)clearLaunchScreenCache;
@end
  
#import "UIApplication+LaunchScreen.h"
  
@implementation UIApplication (LaunchScreen)
- (void)clearLaunchScreenCache {
    NSError *error;
    [NSFileManager.defaultManager removeItemAtPath:[NSString stringWithFormat:@"%@/Library/SplashBoard", NSHomeDirectory()] error:&error];
    if (error) {
        NSLog(@"Failed to delete launch screen cache: %@",error);
    }
}
@end
```

OC 使用方法

```objectivec
#import "UIApplication+LaunchScreen.h"

[UIApplication.sharedApplication clearLaunchScreenCache];
```

参考：[如何清除 iOS APP 的启动屏幕缓存](https://mp.weixin.qq.com/s/1esgRgu1iqFwB1Wv8-GlEQ "如何清除 iOS APP 的启动屏幕缓存")

### 优化 SwiftLint 执行

整理编辑：[zhangferry](https://zhangferry.com)

很多 Swift 项目里都集成了 SwiftLint 用于代码检查。SwiftLint 的执行通常在编译的早期且全量检查的，目前我们项目的每次 lint 时间在 12s 左右。但细想一下，并没有改变的代码多次被 lint 是一种浪费。顺着这个思路在官方的 [issues](https://github.com/realm/SwiftLint/issues/413 "SwiftLint issue 413") 里找到了可以过滤非修改文件的参考方法，其是通过 `git diff` 查找到变更的代码，仅对变更代码进行 lint 处理。使用该方案后，每次 lint 时长基本保持在 2s 以内。

下面附上该脚本，需要注意的是 `SWIFT_LINT` 要根据自己的集成方式进行替换，这里是 CocoaPods 的集成方式：

```bash
# Run SwiftLint
START_DATE=$(date +"%s")

SWIFT_LINT="${PODS_ROOT}/SwiftLint/swiftlint"

# Run SwiftLint for given filename
run_swiftlint() {
    local filename="${1}"
***
整理编辑：[夏天](https://juejin.cn/user/3298190611456638)、[zhangferry](https://zhangferry.com)

### 节流、防抖再讨论

在之前的分享中，我们介绍了[函数节流(Throttle)和防抖(Debounce)解析及其OC实现](https://mp.weixin.qq.com/s/h1MYGTYtYo9pcHmqw6tHBw)。部分读者会去纠结节流和防抖的概念以至于执拗于其中的区别，想在节流和防抖之间找到一个交接点，通过这个交接点进行区分，其究竟是节流(**Throttle**)还是防抖(**Debounce**)。

容易让人理解混乱的还有节流和防抖中的 **Leading** 和 **Trailing** 模式，这里我们试图通过更直白的语言来解释这两个概念的区别。

#### 概念解释

以下是正常模式，当我们移动发生位移修改时，执行函数回调。

![](https://cdn.zhangferry.com/Images/callback.gif)

这个执行明显太频繁了，所以需要有一种方法来减少执行次数，节流和防抖就是这样的方法。

**节流**：在一定周期内，比如 200ms ，**每** 200ms 只会执行一次函数回调。

**防抖**：在一定周期内，比如 200ms，任意两个**相邻**事件间隔超过 200ms，才会执行一次函数调用。

注意上面两个方法都是把原本密集的行为进行了分段处理，但分段就分头和尾。比如每 200ms 触发一次，是第 0ms 还是第 200ms？相邻间隔超过 200ms，第一个事件算不算有效事件呢？这就引来了 Leading 和 Trailing，节流和防抖都有 Leading 和 Trailing 两种模式。

**Leading**：在时间段的开始触发。

**Trailing**：在时间段的结尾触发。

> 备注：leading 和 trailing 是更精确的概念区分，有些框架里并没有显性声明，只是固定为一个较通用的模式。比如 RxSwift， `throttle` 只有 leading 模式，`debounce` 只有 trailing 模式。

#### 典型应用场景

通过对比文本输入校验和提供一个模糊查询功能来加深节流和防抖的理解。

在校验输入文本是否符合某种校验规则，我们可以在用户停止输入的 200ms 后进行校验，期间无论用户如果输入 是增加还是删减都不影响，这就是防抖。

而模糊查询则，用户在输入过程中我们每隔 200ms 进行一次模糊匹配避免用户输入过程中查询列表为空，这就是 节流。

#### 拓展

如果你项目中有存在这样的高频调用，可以尝试使用该理念进行优化。

这些文章：[彻底弄懂函数防抖和函数节流](https://segmentfault.com/a/1190000018445196 "彻底弄懂函数防抖和函数节流")，[函数防抖与函数节流](https://zhuanlan.zhihu.com/p/38313717 "函数防抖与函数节流")和 [Objective-C Message Throttle and Debounce](http://yulingtianxia.com/blog/2017/11/05/Objective-C-Message-Throttle-and-Debounce/ "Objective-C Message Throttle and Debounce") 都会对你理解有所帮助。

### 关于 TestFlight 外部测试

TestFlight 分为内部和外部测试两种。内部测试需要通过邮件邀请制，对方同意邀请才可以参与到内部测试流程，最多可邀请 100 人。每次上传应用到 `AppStore Connect`，内部测试人员就会自动收到测试邮件的通知。

外部测试可以通过邮件邀请也可以通过公开链接的形式直接参与测试，链接生成之后就固定不变了，其总是指向当前最新版本。外部测试最多可邀请 10000 人。

与内测不同的是，外测每个版本的首次提交都需要经过苹果的审核。比如应用新版本为 1.0.0，首次提交对应的 build 号为 100，这个 100 的版本无法直接发布到外部测试，需要等待 TestFlight 团队的审核通过。注意这个审核不同于上线审核，AppStore 和 TestFlight 也是两个不同的团队。外测审核条件较宽泛，一般24小时之内会通过。通过之后点击公开连接或者邮件通知就可以下载 100 版本包。后面同属 1.0.0 的其他 build 号版本，无需审核，但需要每次手动发布。（Apple 帮助文档里有提，后续版本还会有基本审核，但遇到的场景都是可以直接发布的。）

采用公开链接的形式是无法看到测试者的信息的，只能查看对应版本的安装次数和崩溃测试。

***
整理编辑：[FBY展菲](https://github.com/fanbaoying)、[zhangferry](https://zhangferry.com)

### iOS 识别虚拟定位调研

#### 前言

最近业务开发中，有遇到我们的项目 App 定位被篡改的情况，在 `Android` 端表现的尤为明显。为了防止这种黑产使用虚拟定位薅羊毛，`iOS` 也不得不进行虚拟定位的规避。

#### 第一种：使用越狱手机

一般 App 用户存在使用越狱苹果手机的情况，一般可以推断用户的行为存在薅羊毛的嫌疑（也有 App 被竞品公司做逆向分析的可能），因为买一部越狱的手机比买一部正常的手机有难度，且在系统升级和 `Appstore` 的使用上，均不如正常手机，本人曾经浅浅的接触皮毛知识通过越狱 `iPhone5s` 进行的 App 逆向。

**代码实现**

```swift
/// 判断是否是越狱设备
/// - Returns: true 表示设备越狱
func isBrokenDevice() -> Bool {

    var isBroken = false

    let cydiaPath = "/Applications/Cydia.app"

    let aptPath = "/private/var/lib/apt"

    if FileManager.default.fileExists(atPath: cydiaPath) {
        isBroken = true
    }

    if FileManager.default.fileExists(atPath: aptPath) {
        isBroken = true
    }

    return isBroken
}
```

#### 第二种：使用爱思助手

对于使用虚拟定位的场景，大多应该是司机或对接人员打卡了。而在这种场景下，就可能催生了一批专门以使用虚拟定位进行打卡薅羊毛的黑产。对于苹果手机，目前而言，能够很好的实现的，当数爱思助手的虚拟定位功能了。

**使用步骤：** 下载爱思助手 Mac 客户端，连接苹果手机，工具箱中点击虚拟定位，即可在地图上选定位，然后点击修改虚拟定位即可实现修改地图的定位信息。

**原理：** 在未越狱的设备上通过电脑和手机进行 `USB` 连接，电脑通过特殊协议向手机上的 `DTSimulateLocation` 服务发送模拟的坐标数据来实现虚假定位，目前 `Xcode` 上内置位置模拟就是借助这个技术来实现的。

**识别方式**

一、通过多次记录爱思助手的虚拟定位的数据发现，其虚拟的定位信息的经纬度的高度是为 0 且经纬度的数据位数也是值得考究的。

二、把定位后的数据的经纬度上传给后台，后台再根据收到的经纬度获取详细的经纬度信息，对司机的除经纬度以外的地理信息进行深度比较，优先比较 `altitude`、`horizontalAccuracy`、`verticalAccuracy` 值，根据值是否相等进行权衡后确定。

三、具体识别流程

* 通过获取公网 `ip`，大概再通过接口根据 `ip` 地址可获取大概的位置，但误差范围有点大。
* 通过 `Wi-Fi` 热点来读取 `App` 位置
* 利用 `CLCircularRegion` 设定区域中心的指定经纬度和可设定半径范围，进行监听。
* 通过 `IBeacon` 技术，使用 `CoreBluetooth` 框架下的 `CBPeripheralManager` 建立一个蓝牙基站。这种定位直接是端对端的直接定位，省去了 `GPS` 的卫星和蜂窝数据的基站通信。

四、[iOS 防黑产虚假定位检测技术](https://cloud.tencent.com/developer/article/1800531 "iOS 防黑产虚假定位检测技术")

文章的末尾附的解法本人有尝试过，一层一层通过 KVC 读取 CLLocation 的 _internal 的 fLocation，只能读取到此。

参考：[iOS 识别虚拟定位调研](https://mp.weixin.qq.com/s/ZbZ4pFzzyfrQifmLewrxsw "iOS 识别虚拟定位调研")

### Fastlane 使用 App Store Connect API Key 解决双重验证问题

现在申请的 AppleId 都是要求必须要有双重验证的，这在处理 CI 问题时通常会引来麻烦，之前的解决方案使用 `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD` 和 `FASTLANE_SESSION`，但 `FASTLANE_SESSION` 具有时效性，每过一个月就需要更新一次，也不是长期方案。Fastlane 在 2.160.0 版本开始支持 Apple 的 App Store Connect API 功能。App Store Connect API 由苹果提供，需登录 App Store Connect 完成授权问题。使用方法如下：

1、在 [这里](https://appstoreconnect.apple.com/access/shared-secret) 创建共享秘钥。

请求权限：

![](https://cdn.zhangferry.com/Images/1_request_access-2.png)

创建秘钥：

![](https://cdn.zhangferry.com/Images/2_create_key-1.png)

这里的 `.p8` 秘钥文件只能下载一次，注意保存。

2、fastfile 的配置。

可以直接用 `app_store_connect_api_key` 对象配置，也可以写成 json 供多个 `lane` 共享，这里推荐使用 json 形式管理，新建一个json文件，配置如下内容：

```json
{
  "key_id": "D383SF739",
  "issuer_id": "6053b7fe-68a8-4acb-89be-165aa6465141",
  "key": "-----BEGIN PRIVATE KEY-----\nMIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHknlhdlYdLu\n-----END PRIVATE KEY-----",
  "duration": 1200, 
  "in_house": false
}
```

前面三项都是对秘钥文件的描述，可以根据自己的项目进行修改。这里需注意 `key` 的内容，原始 `.p8` 文件是带换行的，转成字符串时用 `\n` 表示换行。注意这里的值为 `key`，官网写法是 `key_content`，这是官网的错误，我开始也被坑了，已经有人提出了 [issues 19341](https://github.com/fastlane/fastlane/issues/19341 "issues 19341")。

基本所有需要登录 App Store Conenct 的命令都包含 api_key_path 这个参数，传入 json 文件路径即可：

```json
lane :release do
  pilot(api_key_path: "fastlane/D383SF739.json" )
end
```

参考：[fastlane app-store-connect-api documents](https://docs.fastlane.tools/app-store-connect-api/ "app-store-connect-api documents")

***
整理编辑：[zhangferry](https://zhangferry.com)

### 缓动函数

很多动画为了效果更加自然，通常都不是线性变化的，而是先慢后快，或者先慢后快再慢的速度进行的。在 iOS 开发里会用 `UIView.AnimationOptions` 这个枚举值进行描述，它有这几个值：

```swift
public struct AnimationOptions : OptionSet {
	public static var curveEaseInOut: UIView.AnimationOptions { get } // default
	public static var curveEaseIn: UIView.AnimationOptions { get }
	public static var curveEaseOut: UIView.AnimationOptions { get }
	public static var curveLinear: UIView.AnimationOptions { get }
}
```

ease 表示减缓，所以 easeInOut 表示，进入和完成都是减缓的，则中间就是快速的，就是表示先慢后快再慢。那这个先慢后快，或者先快后慢的过程具体是如何描述的呢？这里就引入了缓动函数，缓动函数就是描述这一快慢过程的函数，其对应三种状态：easeIn、easeOut、easeInOut。

缓动函数并非特定的某一个函数，它有不同的拟合方式，不同形式的拟合效果可以参看[下图](https://easings.net/ "easings.net")：

![](https://cdn.zhangferry.com/Images/20210920125221.png)

缓动函数名例如 easeInSine 后面的 Sine 就是拟合类型，其对应的就是三角函数拟合。常见的还有二次函数 Quad，三次函数 Cubic 等。以上函数有对应的 [TypeScript 源码](https://github.com/ai/easings.net/blob/33774b5880a787e467d6f4f65000608d17b577e2/src/easings/easingsFunctions.ts "easingsFunctions.ts")，有了具体的计算规则，我们就可以将缓动效果应用到颜色渐变等各个方面。以下是三角函数和二次函数拟合的 Swift 版本：

```swift
struct EasingsFunctions {
    /// sine
    static func easeInSine(_ x: CGFloat) -> CGFloat {
        return 1 - cos((x * CGFloat.pi) / 2)
    }
    static func easeOutSine(_ x: CGFloat) -> CGFloat {
        return sin((x * CGFloat.pi) / 2)
    }
    static func easeInOutSine(_ x: CGFloat) -> CGFloat {
        return -(cos(CGFloat.pi * x) - 1) / 2
    }
    /// quad
    static func easeInQuad(_ x: CGFloat) -> CGFloat {
        return x * x
    }
    static func easeOutQuad(_ x: CGFloat) -> CGFloat {
        return 1 - (1 - x) * (1 - x)
    }
    static func easeInOutQuad(_ x: CGFloat) -> CGFloat {
        if x < 0.5 {
           return 2 * x * x
        } else {
           return 1 - pow(-2 * x + 2, 2) / 2
        }
    }
}
```

***
整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### 低电量模式

从 iOS 9 开始，Apple 为 iPhone 添加了低电量模式（**Low Power Mode**）。用户可以在 **设置 -> 电池** 启用低电量模式。在低电量模式下，iOS 通过制定某些节能措施来延长电池寿命，包括但不限于以下措施：

* 降低 CPU 和 GPU 性能，降低屏幕刷新率
* 包括联网在内的主动或后台活动都将被暂停
* 降低屏幕亮度
* 减少设备的自动锁定时间
* 邮件无法自动获取，陀螺仪及指南针等动态效果将被减弱，动态屏保将会失效
* 对于支持 5G 的 iPhone 设备来说，其 5G 能力将被限制，除非你在观看流媒体

上述节能措施是否会影响到你的应用程序，如果有的话，你可能需要针对低电量模式来适当采取某些措施。

#### lowPowerModeEnabled

我们可以通过 **NSProcessInfo** 来获取我们想要的进程信息。这个**线程安全**的单例类可以为开发人员提供与当前进程相关的各种信息。

一个值得注意的点是，NSProcessInfo 将尝试将环境变量和命令行参数解释为 Unicode，以 UTF-8 字符串返回。如果该进程无法成功转换为 Unicode 或随后的 C 字符串转换失败的话 —— 该进程将被**忽略**。

当然，我们还是需要关注于低电量模式的标志，一个表示设备是否启用了低电量模式的布尔值 —— `lowPowerModeEnabled`。

```swift
if NSProcessInfo.processInfo().lowPowerModeEnabled {
    // 当前用户启用低电量模式
} else {
    // 当前用户未启用低电量模式
}
```

#### NSProcessInfoPowerStateDidChangeNotification

为了更好的响应电量模式的切换——**当电池充电到 80% 时将退出低电量模式**，Apple 为我们提供了一个全局的通知`NSProcessInfoPowerStateDidChangeNotification`。

```swift
NSNotificationCenter.defaultCenter().addObserver(
    self,
    selector: "yourMethodName:",
    name: NSProcessInfoPowerStateDidChangeNotification,
    object: nil
)

func yourMethodName:(note:NSNotification) {  
    if (NSProcessInfo.processInfo().isLowPowerModeEnabled) {  
      // 当前用户启用低电量模式
      // 在这里减少动画、降低帧频、停止位置更新、禁用同步和备份等
    } else {  
      // 当前用户未启用低电量模式
      // 在这里恢复被禁止的操作
    }  
}
```

#### 总结

通过遵守 **iOS 应用程序能效指南** 推荐的方式，为平台的整体能效和用户体验做出改变。

#### 参考

* [在 iPhone 上启用低电量模式将丢失 15 项功能](https://igamesnews.com/mobile/15-functions-you-will-lose-by-activating-low-power-mode-on-iphone/ "在 iPhone 上启用低电量模式将丢失 15 项功能" )
* [iOS 应用程序能效指南](https://developer.apple.com/library/watchos/documentation/Performance/Conceptual/EnergyGuide-iOS/index.html "iOS 应用程序能效指南")
* [响应 iPhone 设备的低电量模式](https://developer.apple.com/library/archive/documentation/Performance/Conceptual/EnergyGuide-iOS/LowPowerMode.html#//apple_ref/doc/uid/TP40015243-CH31-SW1 "响应 iPhone 设备的低电量模式" )
* [WWDC 2015 Session 707 Achieving All-day Battery Life](https://developer.apple.com/videos/play/wwdc2015/707 "WWDC 2015 Session 707 Achieving All-day Battery Life")

***
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

当 WKWebView 中的 URL 需要用户授权时，我们需要实现以下方法：

```swift
func webView(_ webView: WKWebView, didReceive challenge: URLAuthenticationChallenge, completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        
    let authenticationMethod = challenge.protectionSpace.authenticationMethod
    if authenticationMethod == NSURLAuthenticationMethodDefault || authenticationMethod == NSURLAuthenticationMethodHTTPBasic || authenticationMethod == NSURLAuthenticationMethodHTTPDigest {
        //Do you stuff
    }
    completionHandler(NSURLSessionAuthChallengeDisposition.UseCredential, credential)
}
```

收到身份验证质询后，我们可以确定所需的身份验证类型（用户凭据或证书），并相应地使用提示或预定义凭据来处理条件。

**3. 多个 WKWebView 共享 Cookie**

WKWebView 的每个实例都有其自己的 cookie 存储。为了在 WKWebView 的多个实例之间共享 cookie，我们需要使用 `WKHTTPCookieStore`，如下所示：

```swift
let cookies = HTTPCookieStorage.shared.cookies ?? []
for (cookie) in cookies {
    webView.configuration.websiteDataStore.httpCookieStore.setCookie(cookie)
}
```

**4. 获取加载进度**

WKWebView 的其他功能非常普遍，例如显示正在加载的 URL 的进度更新。

可以通过监听以下方法的 `estimatedProgress` 的 keyPath 值来更新 ProgressViews：

```swift
override func observeValue(forKeyPath keyPath: String?, of object: Any?, change: [NSKeyValueChangeKey : Any]?, context: UnsafeMutableRawPointer?)
```

**5. 配置 URL 操作**

使用 decisionPolicyFor 函数，我们不仅可以通过电话，Facetime 和邮件等操作来控制外部导航，还可以选择限制某些 URL 的打开。以下代码展示了每种情况：

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
            } else{
                decisionHandler(.allow)
            }
        }
    }
}
```

参考：[WKWebView 几个不常用的特性](https://mp.weixin.qq.com/s/FFZMz9Yc2Bm6-gAnCBsUZw)


***
### Xcode 增量编译优化

整理编辑：[zhangferry](https://zhangferry.com)

相对于全量编译，增量编译才是平常开发使用最多的场景，所以这方面提升所带来的好处往往更可观。参考苹果文档 [Improving the Speed of Incremental Builds](https://developer.apple.com/documentation/xcode/improving-the-speed-of-incremental-builds "Improving the Speed of Incremental Builds") ，我们可以从多个方面入手优化增量编译。

在开始优化之前更重要的是对编译时间的测量，有衡量指标才能准确分析出我们的优化效果。时间测量可以通过 Xcode 的 `Product > Perform Action > Build With Timing Summary`，然后在编译日志的底部查看各阶段耗时统计。

以下为优化建议：

#### 声明脚本构建阶段脚本和构建规则的 Inputs 和 Outputs

New Build System 每次编译准备执行 Build Phase 中的脚本时，会根据 inputs 和 outputs 的状态来确定是否执行该脚本。以下情况会执行脚本：

* 没有 input 文件
* 没有 output 文件
* input 文件发生变化
* output 丢失

最近遇到一个问题刚好跟这有关，该问题导致增量编译时间很长，耗时主要集中在 CompileAsseetCatalog 阶段。

正常 CocoaPods 在处理资源 Copy 的时候是带有 input 和 output 的，用于减少资源的导入和编译行为，如下图：

![](https://cdn.zhangferry.com/Images/20211027225406.png)

我们项目中有很多私有库，里面引用图片使用了 `Assets.xcassets` 的形式（未封装 Bundle，静态库），这导致一个编译错误：

```
Targets which have multiple asset catalogs that aren't in the same build phase may produce an error regarding a "duplicate output file"
```

这个错误正是 New Build System 带来的，[Build System Release Notes for Xcode 10](https://developer.apple.com/documentation/xcode-release-notes/build-system-release-notes-for-xcode-10 "Build System Release Notes for Xcode 10") 里有说明：

> Targets which have multiple asset catalogs that aren't in the same build phase may produce an error regarding a "duplicate output file". (39810274)
>
> Workaround: Ensure that all asset catalogs are processed by the same build phase in the target.

上面给出了临时的解决方案，就是将所有 asset catalogs 在同一个构建过程处理。对应到 CocoaPods 就是在 Podfile 里添加下面这句：

```ruby
install! 'cocoapods', :disable_input_output_paths => true
```

该设置会关闭资源 Copy 里的 input 和 output，如上面所说，没有 input 和 output，每次都会执行资源的 Copy。因为 Pod 里的`Assets.scassets` 最终会和主项目的 `Assets.scassets `  合到一起编译成 car 文件，所以每次主项目都要等 Pods 的 Copy 完再编译，即使资源文件没有任何变更，这就导致了增量时长的增加。

******
### 使用 os_signpost 标记函数执行和测量函数耗时

整理编辑：[zhangferry](zhangferry.com)

os_signpost 是 iOS12 开始支持的一个用于辅助开发调试的轻量工具，它跟 Instruments 的结合使用可以发挥很大作用。os_signpost API 较简单，其主要有两大功能：做标记、测量函数耗时。

首先我们需要引入 os_signpost 并做一些初始化工作：

```swift
import os.signpost

// test function
func bindModel {
  let log = OSLog(subsystem: "com.ferry.app", category: "SignLogTest")
  let signpostID = OSSignpostID(log: log)
  // ...
}
```

其中 subsystem 用于标记应用，category 用于标记调试分类。

后面试下它标记和测量函数的功能。

#### 做标记

```swift
let functionName: String = #function
os_signpost(.event, log: log, name: "Complex Event", "%{public}s", functionName)
```

注意这个 API 中的 `name` 和后面的 `format` 都是 StaticString 类型（format 是可选参数）。StaticString 与 String 的区别是前者的值是由编译时确认的，其初始化之后无法修改，即使是使用 var 创建。系统的日志库 OSLog 也是选择 StaticString 作为参数类型，这么做的目的一部分在于编译器可采取一定的优化，另一部分则是出于对隐私的考量。

> The unified logging system considers dynamic strings and complex dynamic objects to be **private**, and does not collect them automatically. To ensure the privacy of users, it is recommended that log messages consist strictly of **static strings** and **numbers**. In situations where it is necessary to capture a dynamic string, you may **explicitly** declare the string public using the keyword **public**. For example, `%{public}s`.

对于调试期间我们需要使用 String 附加参数的话，可以用 `%{public}s` 的形式格式化参数，以达到捕获动态字符串的目的。

#### 测量函数耗时

```swift
os_signpost(.begin, log: log, name: "Complex calculations", signpostID: signpostID)
/// Complex Event
os_signpost(.end, log: log, name: "Complex calculations", signpostID: signpostID)
```

将需要测量的函数包裹在 begin 和 end 两个 os_signpost 函数之间即可。

#### 使用

打开 Instruments，选择创建 Blank 模板，点击右上角，添加 "+" 号，双击选择添加 os_signpost 和 Time Profiler 两个模板。运行应用直到触发标记函数时停止，我们展开 os_signpost，找到我们创建的 SignLogTest，将其加到下方。调整 Time Profiler 的 Call Tree 之后就可以看到下图样式。

![](https://cdn.zhangferry.com/Images/20211107192353.png)

event 事件被一个减号所标记，鼠标悬停可以看到标记的函数名，begin 和 end 表示那个耗时函数执行的开始和结束用一个区间块表示。

其中 event 事件可以跟项目中的打点结合起来，例如应用内比较重要的几个事件之间发生了什么，他们之间的耗时是多少。

### 混编｜将 Objective-C typedef NSString 作为 String 桥接到 Swift 中

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

在 Objective-C 与 Swift 混编的过程中，我遇到了如下问题：

我在 Objective-C Interface 中使用 typedef 为 NSString * 取了一个有意义的类型别名 TimerID，但 Generated Swift Interface 却不尽如人意。在方法参数中 TimerID 类型被转为了 String，而 TimerID 却还是 NSString 的类型别名。

```swift
// Objective-C Interface
typedef NSString * TimerID;

@interface Timer : NSObject
+ (void)cancelTimer:(TimerID)timerID NS_SWIFT_NAME(cancel(timerID:));

@end

// Generated Swift Interface
public typealias TimerID = NSString

open class Timer : NSObject {
     open class func cancel(timerID: String)
}
```

这在 Swift 中使用的时候就遇到了类型冲突问题。由于 TimerID 是 NSString 的类型别名，而 NSString 又不能隐式转换为 String。

```swift
// Use it in Swift
let timerID: TimerID = ""
Timer.cancel(timerID: timerID) // Error: 'TimerID' (aka 'NSString') is not implicitly convertible to 'String'; did you mean to use 'as' to explicitly convert? Insert ' as String'
```

可以通过以下方式解决该问题：

1. 在 Swift 中放弃使用 TimerID 类型，全部用 String 类型
2. 在 Swift 中使用到 TimerID 的地方显示转化为 String 类型

```swift
Timer.cancel(timerID: timerID as String)
```

但这些处理方式并不好。如果从根源上解决该问题，也就是在 Generate Swift Interface 阶段将 `typedef NSString *TimerID` 转换为 `typealias TimerID = String`，那就很棒。宏 `NS_SWIFT_BRIDGED_TYPEDEF` 就派上用场了。

```swift
// Objective-C Interface
typedef NSString * TimerID NS_SWIFT_BRIDGED_TYPEDEF;

@interface Timer : NSObject
+ (void)cancelTimer:(TimerID)timerID NS_SWIFT_NAME(cancel(timerID:));

@end

// Generated Swift Interface
public typealias TimerID = String // change: NSString -> String

open class Timer : NSObject {
    open class func cancel(timerID: TimerID) // change:  String -> TimerID
}
```

现在，我可以在 Swift 中愉快地使用 TimerID 类型啦！

```swift
let timerID: TimerID = ""
Timer.cancel(timerID: timerID) 
```

除了 NSString，`NS_SWIFT_BRIDGED_TYPEDEF` 还可以用在 NSDate、NSArray 等其它 Objective-C 类型别名中。

***
### 混编｜NS_SWIFT_NAME

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

`NS_SWIFT_NAME` 宏用于在混编时为 Swift 重命名 Objective-C API，它可用在类、协议、枚举、属性、方法或函数、类型别名等等之中。通过 Apple 举的一些例子，我们可以学习到它的一些应用场景：

* 重命名与 Swift 风格不符的 API，使其在 Swift 中有合适的名称；
* 将与类 A 相关联的类/枚举作为内部类/枚举附属于类 A；
* 重命名 “命名去掉完整前缀后以数字开头的” 枚举的 case，改善所有 case 导入到 Swift 中的命名；
* 重命名 “命名不满足自动转换为构造器导入到 Swift 中的约定的” 工厂方法，使其作为构造器导入到 Swift 中（不能用于协议中）；
* 在处理全局常量、变量，特别是在处理全局函数时，它的能力更加强大，能够极大程度地改变 API。比如可以将 `全局函数` 转变为 `静态方法`，或是 `实例⽅法`，甚至是 `实例属性`。如果你在 Objective-C 和 Swift 里都用过 Core Graphics 的话，你会深有体会。Apple 称其把 `NS_SWIFT_NAME` 用在了数百个全局函数上，将它们转换为方法、属性和构造器，以更加方便地在 Swift 中使用。

你可以在 [iOS 混编｜为 Swift 重命名 Objective-C API](https://juejin.cn/post/7022302122867687454 "iOS 混编｜为 Swift 重命名 Objective-C API") 中查看上述示例。

***
整理编辑：[zhangferry](zhangferry.com)

### count vs isEmpty

通常在判断一个字符串或者数组是否为空的时候有两种方式：`count == 0` 或者 `isEmpty`。我们可能会认为两者是一样的，`isEmpty` 内部实现就是 `count == 0`。但在 SwiftLint 的检验下，会强制要求我们使用使用 isEmpty 判空。由此可以判断出两者肯定还是存在不同的，今天就来分析下两者的区别。

count 和 isEmpty 这两个属性来源于 `Collection`，count 表示数量，这个没啥特别的，需要注意的是isEmpty的实现。在标准库中，它的定义是这样的：

```swift
extension Collection {
    var isEmpty: Bool { startIndex == endIndex }
}
```

集合的首索引和尾索引相等，则表示为空，这里只有一个比较，复杂度为 O(1)。

大部分集合类型都是走的该默认实现，但也有一些特定的集合类型会重写该方法，比如 `Set`：

```swift
extension Set {
    var isEmpty: Bool { count == 0 }
}
```

那为啥会出现两种不同的情况呢，我们再看 Collection 里对 count 的说明。

> **Complexity**: O(1) if the collection conforms to `RandomAccessCollection`; otherwise, O(**n**), where **n** is the length of the collection.

所以对于遵循了`RandomAccessCollection` 协议的类型，其count获取是 O(1) 复杂度，像是 Array；对于未遵循的类型，比如 String，其 count 复杂度就是 O(n)，但是isEmpty 却还是 O(1)。

这里的 Set 还要再特殊一些，因为其没有实现 `RandomAccessCollection` 却还是用 count 的方式判定是否为空，这是因为 Set 的实现方式不同，其 count 的获取就是 O(1) 复杂度。

当然为了简化记忆，我们可以总是使用 isEmpty 进行判空处理。

因为涉及多个协议和具体类型，这里放一张表示这几个协议和类型之间的关系图。

![](https://cdn.zhangferry.com/Images/20211126004620.png)

[图片来源](https://itwenty.me/2021/10/understanding-swifts-collection-protocols/ "图片来源")

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

### 混编｜为 Objective-C 添加枚举宏，改善混编体验

* `NS_ENUM`。用于声明简单枚举，将作为 `enum` 导入到 Swift 中。建议将使用其它方式来声明的 Objective-C 简单枚举进行改造，使用 `NS_ENUM` 来声明，以更好地在 Swift 中使用。
* `NS_CLOSED_ENUM`。用于声明不会变更枚举成员的简单枚举（简称 “冻结枚举” ），例如 NSComparisonResult，将作为 `@frozen enum` 导入到 Swift 中。冻结枚举以降低灵活性的代价，换取了性能上的提升。
* `NS_OPTIONS`。用于声明选项枚举，将作为 `struct` 导入到 Swift 中。
* `NS_TYPED_ENUM`。用于声明类型常量枚举，将作为 `struct` 导入到 Swift 中。可大大改善 Objective-C 类型常量在 Swift 中的使用方式。
* `NS_TYPED_EXTENSIBLE_ENUM`。用于声明可扩展的类型常量枚举。与 `NS_TYPED_ENUM` 的区别是生成的 `struct` 多了一个忽略参数标签的构造器。
* `NS_STRING_ENUM` / `NS_EXTENSIBLE_STRING_ENUM`。用于声明字符串常量枚举，建议弃用，使用 `NS_TYPED_ENUM` / `NS_TYPED_EXTENSIBLE_ENUM` 替代。在 Xcode 13 中，Apple 已经将原先使用 `NS_EXTENSIBLE_STRING_ENUM` 声明的 NSNotificationName 等常量类型改为使用 `NS_TYPED_EXTENSIBLE_ENUM` 来声明。

可以看看：

* [@师大小海腾：iOS 混编｜为 Objective-C 添加枚举宏，改善混编体验](https://juejin.cn/post/6999460035508043807 "@师大小海腾：iOS 混编｜为 Objective-C 添加枚举宏，改善混编体验")
* [@Apple：Grouping Related Objective-C Constants](https://developer.apple.com/documentation/swift/objective-c_and_c_code_customization/grouping_related_objective-c_constants "@Apple：Grouping Related Objective-C Constants")

***
整理编辑：[zhangferry](zhangferry.com)

### 设备启动流程

我们对 App 的启动流程通常会关注比较多，而忽视设备的启动流程，这次来梳理一下设备的启动流程。设备的启动流程分两类：OS X 和 iOS 等 i系列设备，过程大致如下图所示：

![](https://cdn.zhangferry.com/Images/20211209233126.png)

#### 开机

按开机键，激活设备，此时硬件通电，CPU 就可以开始工作了。

#### 启动引导

启动引导即是引导至系统内核的加载。

OS X 通过 EFI 进行引导，EFI 是相对 BIOS 的一种升级版设计，它有多种功能，像是引导加载器、驱动程序等。OS X 中的 `boot.efi` 就是一个引导加载器，由它激活 OS 的内核程序。

i 系列设备没有采用 EFI 的方案，而使用了一种更加注重安全性的设计。i 系列设备内部有一个引导 ROM，这个 ROM 是设备本身的一部分。引导 ROM 会激活 LLB（Low Level Bootloader 底层加载器），LLB 这一步开始就有了签名校验。这一步完成之后会进入 iBoot 阶段。iBoot 是内核的引导加载器，由它来加载内核。

（iOS 系列设备的升级其实还有一个 DFU 升级的流程，为了简化这里略过。）

#### launchd

Launchd 是用户态的第一个进程，由内核直接启动，其 pid=1，位于如下路径，该路径会被硬编码到内核中：

```bash
$ ll /sbin/launchd
-rwxr-xr-x  1 root  wheel   857K Jan  1  2020 /sbin/launchd
```

launchd 的主要任务就是按照预定的设置加载其他启动需要的程序。这类预定的任务分为守护进程（daemon）和代理进程（agent）。

launchd 不仅是负责这些启动必备进程，很多用户使用中的进程，像是我们点击应用图标所创建的进程也是由它处理的。

#### 守护进程 & 代理进程

守护进程是与用户登录无关的程序。代理进程是用户登录之后才加载的程序。

iOS 没有用户登录的概念，所以只有守护进程。这些启动进程会被放到 plist 文件里：

```
/System/Library/LaunchDaemons #系统守护进程plist文件
/System/Library/LaunchAgents  #系统代理进程plist文件
/Library/LaunchDaemons #第三方守护进程plist文件
/Library/LaunchAgents  #第三方代理进程plist文件
~/Library/LaunchAgents #用户自由的代理程序plist文件,用户登录时启动
```

`Finder` 是 OS X 的代理进程，用于提供图形功能，配合 `Dock` 我们就能看到 Mac 的桌面了。

在 iOS 上与之对应的就是 `SpringBoard`，它就是 iPhone 的桌面进程。

到这一步就算是设备启动完成了！

参考：《深入解析 MAC OS X & IOS 操作系统》

***
整理编辑：[zhangferry](zhangferry.com)

### 内存相关的一些机制

#### 虚拟内存寻址

为了安全性，防止物理内存被篡写（还有其他很多优势），操作系统引入了虚拟内存机制，虚拟内存是对物理内存的映射，操作系统会为每个进程提供一个连续并且私有的虚拟内存空间。

实际的数据读写首先要通过虚拟地址找到对应的物理地址，这个过程就是 CPU 寻址，CPU 寻址由位于 CPU 的 MMU（Memory Management Unit 内存管理单元）负责。

为了便于管理，虚拟内存被分割为大小固定的虚拟页（Virtual Page, VP）。程序加载过程中，虚拟内存由磁盘到内存的映射是以页为单位进行处理的。每次映射完成都会对应一个关联的物理内存地址，为了管理这个映射关系出现了页表条目（Page Table Entry）PTE 的一个数据表。这个页表条目里有一个标记位比特位，0 表示还未加载到内存，1 表示已经加载到内存。当访问到 0 就出产生缺页（Page Fault），之后会填充数据到内存，并修改这个标记位。

这个 PTE 通常是位于高速缓存或者内存中的，但即使是高速缓存它相对于 CPU 的读取速度仍然是很慢的。后来又引入了后备缓冲器（Translation Lookaside Buffer，TLB），这个缓存器位于 CPU 内部，其存储了 PTE 内容。虽然它的存储空间较小，但因为在 CPU 内部访问很快，由局部性原理来说这个处理仍是非常值得的。

汇总一下寻址流程如下图所示：

![](https://cdn.zhangferry.com/Images/20211216194314.png)

#### 内存不足的处理

在 Linux 中虚拟内存空间是大于实际物理内存地址的，这就会出现一个状况，当内存物理地址不够用时会发生什么？实际操作系统会将物理内存中的部分内容迁移到磁盘中，然后腾出地方给申请内存方使用，这个过程叫 Swap Out。当又要使用那部分内存时会触发 Swap Int，再移出部分内存，将需要的内容映射到空缺内存空间里。这个机制的好处是可以使用更大的内存地址，但坏处也很明显就是 Swap 会造成较大性能损耗。

##### iOS 处理机制

iOS 没有 Disk Swap 机制，因为其本身磁盘空间相对电脑是比较小的，而且频繁读取闪存会影响闪存寿命。基于此 iOS 设备可申请内存地址是有限度的，关于各个设备所能允许申请的最大内存，[Stack OverFlow](https://stackoverflow.com/questions/5887248/ios-app-maximum-memory-budget/15200855#15200855 "ios-app-maximum-memory-budget") 有人做过测试：

```
device: (crash amount/total amount/percentage of total)

iPhone5: 645MB/1024MB/62%
iPhone5s: 646MB/1024MB/63%
iPhone6: 645MB/1024MB/62% (iOS 8.x)
iPhone6+: 645MB/1024MB/62% (iOS 8.x)
iPhone6s: 1396MB/2048MB/68% (iOS 9.2)
iPhone6s+: 1392MB/2048MB/68% (iOS 10.2.1)
iPhoneSE: 1395MB/2048MB/69% (iOS 9.3)
iPhone7: 1395/2048MB/68% (iOS 10.2)
iPhone7+: 2040MB/3072MB/66% (iOS 10.2.1)
iPhone8: 1364/1990MB/70% (iOS 12.1)
iPhone X: 1392/2785/50% (iOS 11.2.1)
iPhone XS: 2040/3754/54% (iOS 12.1)
iPhone XS Max: 2039/3735/55% (iOS 12.1)
iPhone XR: 1792/2813/63% (iOS 12.1)
iPhone 11: 2068/3844/54% (iOS 13.1.3)
iPhone 11 Pro Max: 2067/3740/55% (iOS 13.2.3)
```

以 iPhone 11 Pro Max 为例，应用可申请内存为 2067M，占系统内容的 55%，这已经是很高了。但即使这样，仍会出现内存过高的情况，iOS 系统的处理主要是清理 + 压缩这两个方案。

**Clean Page & Dirty Page**

iOS 将内存页分为 Clean Page 和 Dirty Page，Clean Page 一般是固定内容，可以被系统回收，需要时从磁盘再加载回来。

![](https://cdn.zhangferry.com/Images/20211216191758.png)

上图可以看出，写入数据前申请内存为 Clean 内存，使用的部分就变成了 Dirty 内存。

**Compressed Memory**

iOS 还有另一种机制是压缩内存（Compressed Memory），这也是一种 Swap 机制。举个例子，某个 Dictionary 使用了 3 个 Page 的内存，如果一段时间没有被访问同时内存吃紧，则系统会尝试对它进行压缩从 3 个 Page 压缩为 1 个 Page 从而释放出 2 个 Page 的内存。但是如果之后需要对它进行访问，则它占用的 Page 又会变为 3 个。

这部分内存可以被 Instrument 统计到，对应的就是 VM Tracker 里的 Swapped Size：

![](https://cdn.zhangferry.com/Images/20211216193218.png)

参考：

* [jonyfang-iOS 内存相关梳理](https://blog.jonyfang.com/2020/04/08/2020-04-08-about-ram/ "jonyfang-iOS 内存相关梳理")
* [Reducing Your App's Memory Use](https://developer.apple.com/documentation/metrickit/improving_your_app_s_performance/reducing_your_app_s_memory_use "Reducing Your App's Memory Use")
* 《深入理解计算机系统》

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

### 混编｜为 Swift 改进 Objective-C API

宏 `NS_REFINED_FOR_SWIFT` 于 Xcode 7 引入，它可用于在 Swift 中隐藏 Objective-C API，以便在 Swift 中提供相同 API 的更好版本，同时仍然可以使用原始 Objective-C 实现。具体的应用场景有：

- 你想在 Swift 中使用某个 Objective-C API 时，使用不同的方法声明，但要使用类似的底层实现。你还可以将 Objective-C 方法在 Swift 中变成属性，例如将 Objective-C 的
  
  ```objectivec
  + (instancetype)sharedInstance;
  ```
  
  方法在 Swift 中的变为 `shared` 属性。

- 你想在 Swift 中使用某个 Objective-C API 时，采用一些 Swift 的特有类型，比如元组。例如，将 Objective-C 的  
  
  ```objectivec
  - (void)getRed:(nullable CGFloat *)red green:(nullable CGFloat *)green blue:(nullable CGFloat *)blue alpha:(nullable CGFloat *)alpha;
  ```
  
    方法在 Swift 中变为一个只读计算属性，其类型是一个包含 rgba 四个元素的元组 
  
  ```swift
  var rgba: (red: CGFloat, green: CGFloat, blue: CGFloat, alpha: CGFloat)
  ```
  
  以更方便使用。

- 你想在 Swift 中使用某个 Objective-C API 时，重新排列、组合、重命名参数等等，以使该 API 与其它 Swift API 更匹配。 

- 利用 Swift 支持默认参数值的优势，来减少导入到 Swift 中的一组 Objective-C API 数量。例如，SDWebImage 的 UIImageView (WebCache) 分类中扩展的方法，在导入到 Swift 中时，方法数量从 9 个减少到 5 个。

- 解决 Swift 调用 Objective-C 的 API 时可能由于数据类型等不一致导致无法达到预期的问题。例如，Objective-C 里的方法采用了 C 风格的多参数类型；或者 Objective-C 方法返回 NSNotFound，在 Swift 中期望返回 nil 等等。

`NS_REFINED_FOR_SWIFT` 可用于方法和属性。添加了 `NS_REFINED_FOR_SWIFT` 的 Objective-C API 在导入到 Swift 时，具体的 API 重命名规则如下：

* 对于初始化方法，在其第一个参数标签前面加 "__"
* 对于其它方法，在其基名前面加 "__"
* 下标方法将被视为任何其它方法，在方法名前面加 "__"，而不是作为 Swift 下标导入
* 其他声明将在其名称前加上 "__"，例如属性

注意：`NS_REFINED_FOR_SWIFT` 和 `NS_SWIFT_NAME` 一起用的话，`NS_REFINED_FOR_SWIFT` 不生效，而是以 `NS_SWIFT_NAME` 指定的名称重命名 Objective-C API。

可以看看：

* [@师大小海腾：iOS 混编｜为 Swift 改进 Objective-C API](https://juejin.cn/post/7024572794943832101 "@师大小海腾：iOS 混编｜为 Swift 改进 Objective-C API")
* [@Apple：Improving Objective-C API Declarations for Swift](https://developer.apple.com/documentation/swift/objective-c_and_c_code_customization/improving_objective-c_api_declarations_for_swift "@Apple：Improving Objective-C API Declarations for Swift")

***
整理编辑：[zhangferry](https://zhangferry.com)

### Swift 中的预编译

Clang 中有预编译宏的概念，在 Xcode 中其对应的是 Build Setting -> Apple Clang - Preprocessing 中的 Preprocessor Macros。这里可以根据不同的 Configuration 设置不同的预编译宏命令，其中 Debug 环境下的 DEBUG=1 就是内置的宏命令，我们通常使用的以下写法就是对应的这个配置：

```objectivec
#if DEBUG
// debug action
#end
```

如果需要新增 Configuration，比如 Stage，我们想要一个新的预编译宏比如 STAGE 表示它，如果这么做：

![](https://cdn.zhangferry.com/Images/20220106190930.png)

在 Objective-C 的代码中是可行的，对于 Swift 代码则无效。这是因为 Swift 使用的编译器是 swiftc，它无法识别 clang 里定义的预编译宏。

解决方案是利用 `SWIFT_ACTIVE_COMPILATION_CONDITIONS` 这个配置变量，它对应 Build Setting 里的 Active Compilation Conditions。做如下设置即可让 STAGE 宏供 Swift 代码使用：

![](https://cdn.zhangferry.com/Images/20220106192217.png)

*********
整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### iOS12 libswift_Concurrency.dylib crash 问题修复
最近很多朋友都遇到了 iOS12 上 libswift_Concurrency 的 crash 问题，Xcode 13.2 release notes 中有提到是 Clang 编译器 bug，13.2.1 release notes 说明已经修复，但实际测试并没有。

crash 的具体原因是 Xcode 编译器在低版本  iOS12 上没有将 libswift_Concurrency.dylib 库剔除，反而是将该库嵌入到 ipa 的 Frameworks 路径下，导致动态链接时 libswift_Concurrency 被链接引发 crash。

#### 问题分析

通过报错信息 `Library not loaded: /usr/lib/swift/libswiftCore.dylib` 分析是动态库没有加载，提示是 libswift_Concurrency.dylib 引用了该库。iOS12 本不该链接这个库，崩溃后通过 `image list` 查看加载的镜像文件会找到 libswift_Concurrency 的路径是 ipa/Frameworks 下的，查询资料了解到是 Xcode13.2 及其以上版本在做 Swift Concurrency 向前兼容时出现的 bug

#### 问题定位

在按照 Xcode 13.2 release notes 提供的方案，将 libswiftCore 设置为 weak 并指定 rpath 后，crash 信息变更，此时 error 原因是 `___chkstk_darwin` 符号找不到；根据 error Referenced from 发现还是 libswift_Concurrency 引用的，通过：

```bash
$ nm -u xxxAppPath/Frameworks/libswift_Concurrency.dylib
```
查看所有未定义符号（类型为 U）， 其中确实包含了 `___chkstk_darwin`，13.2 release notes 中提供的解决方案只是设置了系统库弱引用，没有解决库版本差异导致的符号解析问题。

error 提示期望该符号应该在 libSystem.B.dylib 中，但是通过找到 libSystem.B.dylib 并打印导出符号：

```bash
$ nm -gAUj libSystem.B.dylib
```
发现即使是高版本的动态库中也并没有该符号，那么如何知道该符号在哪个库呢？这里用了一个取巧的方式，run iOS13 以上真机，并设置 symbol 符号 `___chkstk_darwin`， Xcode 会标记所有存在该符号的库，经过前面的思考，认为是在查找 libswiftCore 核心库时 crash 的可能性更大。

> libSystem.B.dylib 路径在 ~/Library/Developer/Xcode/iOS DeviceSupport/xxversion/Symbols/usr/lib/ 目录下

如何校验呢，通过 Xcode 上 iOS12 && iOS13 两个不同版本的 libswiftCore.dylib 查看导出符号，可以发现，iOS12 上的 Core 库不存在，对比组 iOS13 上是存在的，所以基本可以断定 symbol not found 是这个原因造成的；当然你也可以把其他几个库也采用相同的方式验证。

> 通过在 ~/Library/Developer/Xcode/iOS DeviceSupport/xxversion/Symbols/usr/lib/swift/libswiftCore.dylib 不同的 version 路径下找到不同系统对应的 libswiftCore.dylib 库，然后用 `nm -gUAj libswiftCore.dylib` 可以获取过滤后的全局符号验证。
> 
> 库的路径，可以通过 linkmap 或者运行 demo 打个断点，通过LLDB的image list查看。

分析总结：无论是根据 Xcode 提供的解决方案亦或是 error 分析流程，发现根源还是因为在 iOS12 上链接了 libswift_Concurrency 造成的，既然问题出在异步库，解决方案也很明了，移除项目中的 libswift_Concurrency.dylib 库即可。

#### 解决方案

**方案一：使用 Xcode13.1 或者 Xcode13.3 Beta 构建**

使用 Xcode13.1 或者 Xcode13.3 Beta 构建，注意 beta 版构建的 ipa 无法上传到 App Store。
该方法比较麻烦，还要下载 Xcode 版本，耗时较多，如果有多版本 Xcode 的可以使用该方法。

**方案二：添加 Post-actions 脚本移除**

添加  Post-actions 脚本，每次构建完成后移除嵌入的libswift_Concurrency.dylib。同时配合 `-Wl,-weak-lswift_Concurrency -Wl,-rpath,/usr/lib/swift` 设置到`Other Linker Flags`。添加流程： Edit Scheme -> Build -> Post-actions -> Click '+' to add New Run Script。脚本内容为：

```bash
rm "${BUILT_PRODUCTS_DIR}/${FRAMEWORKS_FOLDER_PATH}/libswift_Concurrency.dylib" || echo "libswift_Concurrency.dylib not exists"
```
<img src="https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/weekly_43_tips_04.jpeg" style="zoom:50%;" />

**方案三：降低或移除使用 libswift_Concurrency.dylib 的三方库**

查找使用 concurrency 的三方库，降低到未引用 libSwiftConcurrency 前的版本，后续等 Xcode 修复后再升级。如果是通过 cocoapods 管理三方库，只需要指定降级版本即可。但是需要解决一个问题，如何查找三方库中有哪些用到 concurrency 呢？

如果是源码，全局搜索相关的 `await & async` 关键字可以找到部分 SDK，但如果是二进制 SDK 或者是间接使用的，则只能通过符号查找。

查找思路：

1. 首先明确动态库的链接是依赖导出符号的，即 xxx 库引用了 target_xxx 动态库时，xxx 是通过调用 target_xxx 的导出符号（全局符号）实现的，全局符号的标识是大写的类型，U 表示当前库中未定义的符号，即 xxx 需要链接其他库动态时的符号，符号操作可以使用 `llvm nm` 命令

2. 如何查看是否引用了指定动态库 target_xxx 的符号？可以通过 linkmap 文件查找，但是由于 libswift_Concurrency 有可能是被间接依赖的，此时 linkmap 中不存在对这个库的符号记录，所以没办法进行匹配，换个思路，通过获取 libswift_Concurrency 的所有符号进行匹配，libswift_Concurrency 的路径可以通过上文提到的 `image list` 获取， 一般都是用的 /usr/lib/swift 下的。

3. 遍历所有的库，查找里面用到的未定义符号（ U ）, 和 libswift_Concurrency 的导出符号进行匹配，重合则代表有调用关系。

为了节省校验工作量，提供 [findsymbols.sh](https://gist.github.com/71f8d3fade74903cae443a3b50c2807f.git "findsymbols.sh") 脚本完成查找，构建前可以通过指定项目中 SDK 目录查找，或者也可以指定构建后 .app 包中的 Frameworks 查找。

使用方法：

1. 下载后进行权限授权， `chmod 777 findsymbols.sh`
2. 指定如下参数：
	- -f：指定单个二进制 framework/.a 库进行检查
    - -p：指定目录，检查目录下的所有 framework/.a 二进制 SDK
    - -o： 输出目录，默认是 `~/Desktop/iOS12 Crash Result` 

参考：
* [如何检测哪些三方库用了 libstdc++ ](https://www.jianshu.com/p/8de305624dfd?utm_campaign=hugo&utm_medium=reader_share&utm_content=note&utm_source=weixin-friends "如何检测哪些三方库用了 libstdc++ ")
* [After upgrading to Xcode 13.2.1, debugging with a lower version of the iOS device still crashes at launching](https://developer.apple.com/forums/thread/696960 "After upgrading to Xcode 13.2.1, debugging with a lower version of the iOS device still crashes at launching")


***
整理编辑：[FBY展菲](https://github.com/fanbaoying)

### 解决 iOS 15 上 APP 莫名其妙地退出登录

#### 复现问题

在 iOS 15 正式版推出后， 我们开始收到用户的反馈：在打开我们的App (Cookpad) 时，用户莫名其妙地被强制退出帐号并返回到登录页。非常令人惊讶的是，我们在测试 iOS 15 beta 版的时候并没有发现这个问题。

我们没有视频，也没有具体的步骤来重现这个问题，所以我努力尝试以各种方式启动应用程序，希望能亲手重现它。我试着重新安装应用程序，我试着在有网络连接和没有网络连接的情况下启动，我试着强制退出，经过 30 分钟的努力，我放弃了，我开始回复用户说我没找到具体问题。

直到我再次解锁手机，没有做任何操作，就启动了 Cookpad，我发现 APP 就像我们的用户所反馈的那样，直接退出到了登录界面！

在那之后，我无法准确的复现该问题，但似乎与暂停使用手机一段时间后再次使用它有关。

#### 缩小问题范围
我担心从 Xcode 重新安装应用程序可能会影响问题的复现，所以我首先检查代码并试图缩小问题的范围。根据我们的实现，我想出了三个怀疑的原因。

- 1、`UserDefaults` 中的数据被清除。
- 2、一个意外的 API 调用返回 HTTP 401 并触发退出登录。
- 3、`Keychain` 抛出了一个错误。

我能够排除前两个怀疑的原因，这要归功于我在自己重现该问题后观察到的一些微妙行为。

- 登录界面没有要求我选择地区 —— 这表明 `UserDefaults` 中的数据没有问题，因为我们的 "已显示地区选择 "偏好设置仍然生效。
- 主用户界面没有显示，即使是短暂的也没有 —— 这表明没有尝试进行网络请求，所以 API 是问题原因可能还为时过早。

这就把`Keychain`留给了我们，指引我进入下一个问题。是什么发生了改变以及为什么它如此难以复现？

#### 寻找根本原因
我的调试界面很有用，但它缺少了一些有助于回答所有问题的重要信息：**时间**。

我知道在 `AppDelegate.application(_:didFinishLaunchingWithOptions:)` 之前，“受保护的数据” 是不可用的，但它仍然没有意义，因为为了重现这个问题，我正在执行以下操作：

1、启动应用程序
2、简单使用
3、强制退出应用
4、锁定我的设备并将其放置约  30 分钟
5、解锁设备
6、再次启动应用

每当我在第 6 步中再次启动应用程序时，我 100% 确定设备已解锁，因此我坚信我应该能够从 `AppDelegate.init() ` 中的 `Keychain ` 读取数据。

直到我看了所有这些步骤的时间，事情才开始变得有点意义。

![](https://images.xiaozhuanlan.com/photo/2021/ffa4e4a3730d3fd5ed1891fa73539f24.png)

再次仔细查看时间戳：
- `main.swift` — 11:38:47
- `AppDelegate.init()` — 11:38:47
- `AppDelegate.application(_:didFinishLaunchingWithOptions:)` — 12:03:04
- `ViewController.viewDidAppear(_:)` — 12:03:04

在我真正解锁手机并点击应用图标之前的 25 分钟，应用程序本身就已经启动了！

现在，我实际上从未想过有这么大的延迟，实际上是 [@_saagarjha](https://twitter.com/_saagarjha) 建议我检查时间戳，之后，他指给我看这条推特。

![](https://images.xiaozhuanlan.com/photo/2021/6ea72a16b7326fe97fcdfd33c4758f6d.png)

> 推特翻译：
> 有趣的 iOS 15 优化。Duet 现在试图先发制人地 "预热" 第三方应用程序，在你点击一个应用程序图标前几分钟，通过 dyld 和预主静态初始化器运行它们。然后，该应用程序被暂停，随后的 "启动" 似乎更快。

现在一切都说得通了。我们最初没有测试到它，因为我们很可能没有给 iOS 15 beta 版足够的时间来 "学习" 我们的使用习惯，所以这个问题只在现实生活的场景中再现，即设备认为我很快就要启动应用程序。我仍然不知道这种预测是如何形成的，但我只想把它归结为 "Siri 智能"，然后就到此为止了。

#### 结论

从 iOS 15 开始，系统可能决定在用户实际尝试打开你的应用程序之前对其进行 "预热"，这可能会增加受保护的数据在你认为应该无法使用的时候的被访问概率。

通过等待 `application(_:didFinishLaunchingWithOptions:)` 委托回调来避免App 受此影响，如果可以的话，留意 `UIApplication.isProtectedDataAvailable`（或对应委托的回调/通知）并相应处理。

我们仍然发现了极少数的非致命问题，在 `application(_:didFinishLaunchingWithOptions:)` 中属性 `isProtectedDataAvailable` 值为 false，我们现在除了推迟从钥匙串读取数据之外，没有其它好方法，因为它是系统原因导致，不值得进行进一步研究。

参考：[解决 iOS 15 上 APP 莫名其妙地退出登录 - Swift社区](https://mp.weixin.qq.com/s/_a5DddYgQHKREi5VoEeJyg)


***
### 获取 Build Setting 对应的环境变量 Key

整理编辑：[zhangferry](zhangferry.com)

Xcode 的 build setting 里有很多配置项，这些配置项都有对应的环境变量，当我们要用脚本自定义的话就需要知道对应的环境变量 Key是哪个才好设置。比如下面这个 Header Search Paths

![](https://cdn.zhangferry.com/Images/20220220215645.png)

其对应的 Key 是 `HEADER_SEARCH_PATHS`。那如何或者这个 Key 呢，除了网上查相关资料我们还可以通过 Xcode 获取。

**方法一（由@CodeStar提供）**

选中该配置项，展开右部侧边栏，选中点击帮助按钮就能够看到这个配置的说明和对应的环境变量名称。

![](https://cdn.zhangferry.com/Images/20220220220200.png)

**方法二**

选中该配置，按住 Option 键，双击该配置，会出现一个描述该选项的帮助卡片，这个内容与上面的帮助侧边栏内容一致。

![](https://cdn.zhangferry.com/Images/20220220220534.png)

### 在 SPM 集成 SwiftLint

整理编辑：[FBY展菲](https://github.com/fanbaoying)

#### SwiftLint 介绍

`SwiftLint` 是一个实用工具，用于实现 Swift 的风格。 在 Xcode 项目构建阶段，集成 SwiftLint 很简单，构建阶段会在编译项目时自动触发 SwiftLint。

遗憾的是，目前无法轻松地将 `SwiftLint` 与 `Swift Packages` 集成，Swift Packages 没有构建阶段，也无法自动运行脚本。

下面介绍如何在 Xcode 中使用 `post action` 脚本在成功编译 Swift Package 后自动触发 SwiftLint。

`SucceedsPostAction.sh` 是一个 bash 脚本，用作 Xcode 中的 “Succeeds” 发布操作。当你编译一个 Swift 包时，这个脚本会自动触发 `SwiftLint`。

#### SwiftLint 安装

1. 在 Mac 上下载脚本 `SucceedsPostAction.sh`。

2. 确保脚本具有适当的权限，即运行 `chmod 755 SucceedsPostAction.sh`。

3. 如果要使用自定义 SwiftLint 规则，请将 `.swiftlint.yml` 文件添加到脚本旁边。

4. 启动 Xcode 13.0 或更高版本

5. 打开 Preferences > Locations 并确保 `Command Line Tools` 设置为 Xcode 版本

6. 打开 Preferences > Behaviors > Succeeds

7. 选择脚本 `SucceedsPostAction.sh`

![](https://files.mdnice.com/user/17787/7cce4fc6-82bc-4c66-b499-6541b75ca08c.png)

就是这样：每次编译 Swift 包时，`SucceedsPostAction.sh` 都会运行 SwiftLint。

**演示**

![](https://files.mdnice.com/user/17787/89f7a065-f200-4158-a701-99b217c38a4a.gif)

#### 存在一些问题

在 Xcode 中运行的 `post action` 脚本无法向 Xcode 构建结果添加日志、警告或错误。因此，`SucceedsPostAction.sh` 在 Xcode 中以新窗口的形式打开一个文本文件，其中包含 SwiftLint 报告列表。没有深度集成可以轻松跳转到 SwiftLint 警告。

**Swift 5.6**

请注意，由于[SE-0303: Package Manager Extensible Build Tools](https://github.com/apple/swift-evolution/blob/main/proposals/0303-swiftpm-extensible-build-tools.md "Package Manager Extensible Build Tools")，Swift 5.6（在撰写本文时尚不可用）可能会有所帮助。集成 SE-0303 后，不再需要此脚本。

参考：[Swift 实用工具 — SwiftLint - Swift社区](https://mp.weixin.qq.com/s/WMCwt6KjiBV2ddES-rQtyw)


************************************
整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Xcode Playground Tips

`Playground` 是学习 Swift 和 SwiftUI 的必不可少的工具，这里总结一些可能涉及到的 Tips，方便更好的学习和使用。

#### 模块化

`Playground` 中也是支持模块化管理的，主要涉及辅助代码和资源两部分：

- 辅助代码(位于 Sources 目录下的代码)：

    辅助代码只在编辑内容并保存后才会编译，运行时不会每次都编译。辅助代码编译后是以 module 形式引入到 Page 中的。所以被访问的符号都需要使用 `public` 修饰。

    添加到 Playground Sources 下的辅助代码，所有 Page 主代码和辅助代码 都可使用。区别在于 Page 辅助代码如果未 import 导入 module, 则不会有代码提示，主代码无需 import。

    添加到 Page Sources 下的辅助代码，只有当前的 Page 可用（Apple 文档）。module 命名格式为 **xxx(PageName)_PageSources**。

    > 实际测试，如果在其他 Page 主代码中和辅助代码中同时 `import` 当前 Sources Module 也是可用的，但是只在辅助代码中 `import`，则不生效。如果有不同测试结果的同学可以交流下

- 资源（位于 Resources）：

使用时作用域同辅助代码基本相同，由于无法作为 module 被 `import` 到 Page 主代码，所以跨 Page 之间的资源是无法访问的。

`Playground` 编译时将当前 Page 和 `Playground` 项目的资源汇总到 Page 项目路径下，因此无论是项目资源还是 Page 专属资源，在 Page 主代码或 Page 的辅助代码中，都可以使用 `Bundle.main` 来访问。

#### 运行方式

`Playground` 可以修改运行方式，分别是 `Automatically Run` 和 `Manually Run`，区别就是自动模式在每次键入后自动编译。调整方式为长按运行按钮，如图：

![](https://cdn.zhangferry.com/Images/weekly_57_weeklyStudy_01.png)

另外，通过快捷键 `shift-回车` 可以只运行到当前鼠标所在位置代码，作用同直接点击代码所在行的运行按钮一致。

#### PlaygroundSupport

`PlaygroundSupport` 是用于扩展 Playground 的框架，在使用上主要有两个作用：

- 执行一些延迟、异步操作、或者存在交互的视图时，这时需要 `Playground` 在执行完最后代码后不会直接 Finish，否则一些回调和交互不会生效。需要设置属性 `needsIndefiniteExecution == true`。

    ```swift
    // 需要无限执行
    PlaygroundPage.current.needsIndefiniteExecution = true
    // 终止无限执行
    PlaygroundPage.current.finishExecution()
    ```

- 使用 `Playground` 展示实时视图时，需要将视图添加到属性 `liveView` 上。如果设置了 `liveView` 则系统会自动设置 `needsIndefiniteExecution`，无需重复设置。

    > 如果是 `UIKit` 视图则通过 `liveView` 属性赋值或者 `setLiveView()` 函数调用都可以，但是 `SwiftUI` 只支持 `setLiveView()` 函数调用方式。

    ```swift
    struct contentView: View {...}
    let label = UILabel(frame: .init(x: 0, y: 0, width: 200, height: 100))
    PlaygroundPage.current.setLiveView(label) // PlaygroundPage.current.liveView = label
    PlaygroundPage.current.setLiveView(contentView)
    ```

#### markup 注释

根据文档，markup 支持标题、列表、代码、粗体、斜体、链接、资产、转移字符等，目的是在 `Quick Help` 和代码提示中显示更丰富的描述信息

书写格式分两种，单行使用 `//: 描述区` 多行使用 `/*: 描述区 */`

源码/渲染模式切换方式：`Editor -> Show Rendered Markup` 或者设置右侧扩展栏的 `Playground Settings ->Render Documentation`。

由于大部分格式都是和 markdown 类似的，这里只学习一个特殊的特性，即导航。

导航可以实现在不同的 Page 页之间跳转，有三种跳转方式：previous、next、指定页

```swift
[前一页](@previous)、[下一页](@next)、[指定页](name)
```

> 指定具体页时，页面名称去掉扩展名，并且编码替换空格和特殊字符。不需要使用 `@` 符号

Markup 更多格式可以查看官方文档 [markup-apple](https://developer.apple.com/library/archive/documentation/Xcode/Reference/xcode_markup_formatting_ref/index.html#//apple_ref/doc/uid/TP40016497-CH2-SW1 "markup-apple")，另外 `Playground` 还支持和框架或者工程结合使用，可以通过另一位主编的博客内容了解学习 [玩转 Xcode Playground（下）- 东坡肘子](https://www.fatbobman.com/posts/xcodePlayground2/ "玩转 Xcode Playground（下）- 东坡肘子")

***
整理编辑：[夏天](https://juejin.cn/user/3298190611456638) 
### 如何配置合适的 ATS（App Transport Security）配置

为了增强应用与网络交互的安全，从 **iOS 9** 开始，苹果开启了称为应用传输安全 (ATS) 的网络功能用于提高所有应用和应用扩展的隐私和数据完整性。

**ATS 会阻止不符合最低安全规范的连接**

![Apps-Transport-Security~dark@2x](https://cdn.zhangferry.com/Images/Apps-Transport-Security_dark@2x.png)

<center> 图片来源于开发者官网</center>

#### 为什么需要进行 ATS 配置

ATS 为我们的应用安全增加了保护，但是由于某些原因，我们不得不需要某些手段来*规避* ATS 规则

在 `info.plist` 中提供了 ATS 配置信息允许用户自定义规则

**最新完整**的 ATS 配置键值如下：

```objectivec
NSAppTransportSecurity : Dictionary {
    NSAllowsArbitraryLoads : Boolean
    NSAllowsArbitraryLoadsForMedia : Boolean
    NSAllowsArbitraryLoadsInWebContent : Boolean
    NSAllowsLocalNetworking : Boolean
    NSExceptionDomains : Dictionary {
    	<domain-name-string> : Dictionary {
      	  NSIncludesSubdomains : Boolean
        	NSExceptionAllowsInsecureHTTPLoads : Boolean
        	NSExceptionMinimumTLSVersion : String
        	NSExceptionRequiresForwardSecrecy : Boolean
    	}
		}
}
```
> 如果你现有的ATS 配置存在冗余的键值，证明其已被摒弃。你可以查看[Document Revision History](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/RevisionHistory.html#//apple_ref/doc/uid/TP40016535-SW1 "Document Revision History") 明确相关键值的信息 

#### 如何挑选合适的 ATS 配置

但是由于各种键值的组合分类繁杂，为了确保连通性，我们需要一个简单的方法，来寻找到我们最适合的 ATS 配置

>  `nscurl --ats-diagnostics --verbose https://developer.apple.com`

上述命令会模拟我们 ATS 中配置规则对项目中使用`URLSession:task:didCompleteWithError:`是否能够请求成功，也就是我们发起网络请求的结果。

>  受限于篇幅，我们就不展示命令运行的结果

从 ATS 默认的空字典开始，共计 16 种组合

* `Result : PASS` 说明该配置可以连接到域名服务器成功

* `Result : FAIL` 说明请求域名服务器失败，当前配置无法组合成功

> **注：**虽然其列举的结果不包括    `NSAllowsArbitraryLoadsForMedia` ,`NSAllowsArbitraryLoadsInWebContent `, `NSAllowsLocalNetworking` ，但是这三个是针对特定的文件的，所以不会影响配置

基于**最小最适用**原则选择对应的 ATS 配置。

#### 参考资料

[NSAppTransportSecurity](https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity?language=objc "NSAppTransportSecurity")

[NSExceptionDomains](https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity/nsexceptiondomains?language=objc "NSExceptionDomains")

[Preventing Insecure Network Connections](https://developer.apple.com/documentation/security/preventing_insecure_network_connections?language=objc "Preventing Insecure Network Connections") 


***
整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)
### OC所使用的类信息存储在哪？ 如何从Macho中找到？

首先我们需要读取到 `__DATA,__objc_classlist` 的信息，存储结构是8个字节指针，读取到对应的指针数据 `data`  

`data` 数据是 `VM Address` 地址，我们需要通过转换拿到对应的 `offset`


* 需要判断是否在对应的 `segmentCommand` 当中

`offset = address - (segmentCommand.vmaddr - segmentCommand.fileoff)`


拿到偏移地址之后，我们就可以根据 `Class64` 的数据结构，在 `machoData` 当中找到对应的数据 `Class` 数据，其中的 `data` 数据才是真正 `Class` 信息的数据

```C++
struct Class64 {
    let isa: UInt64
    let superClass: UInt64
    let cache: UInt64
    let vtable: UInt64
    let data: UInt64
}
```

---
`Class64.data` 数据是 `VM Address` 地址，我们需要通过转换后拿到 `offset` ，在 `machData` 当中找到对应的 `ClassInfo64` 数据，然后其中 `name` 就是对应的 `className`

```C++
struct Class64Info
{
    let flags: Int32 //objc-runtime-new.h line:379~460
    let instanceStart: Int32
    let instanceSize: Int32
    let reserved: Int32
    let instanceVarLayout: UInt64
    let name: UInt64
    let baseMethods: UInt64
    let baseProtocols: UInt64
    let instanceVariables: UInt64
    let weakInstanceVariables: UInt64
    let baseProperties: UInt64
};

```
![](http://cdn.zhangferry.com/Images/20220707210722.png)

如果想要了解具体源码实现，可以通过另一位主编皮拉夫大王的开源项目 [WBBlades](https://github.com/wuba/WBBlades) 学习


***
整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Swift 5.7 中的 opaque parameter 和 primary associated types

熟悉 Swift 的读者都知道，如果你将存在关联类型或者 `Self` 的协议当做类型使用，编译器会报错 `Protocol 'X' can only be used as a generic constraint because it has Self or associated type requirements.`。表示该协议只能用作泛型协议。

Swift 5.1 为了解决这个问题引入了不透明返回类型的概念，即在函数返回值的位置使用 `some` 修饰协议，整体作为一个类型使用。这也是支持 SwiftUI 的核心特性之一。现在 Swift 5.7 扩展了这一功能。

####  opaque parameter

现在 `some` 关键字不仅可以用在函数返回值位置，也支持用来修饰函数参数。表示的含义和修饰返回值类型时是一致的。示例如下：

```swift
class BookRender {
    ...
    func bookArticles(_ articles: [Article]) {
        ...
    }
}
```

`BookRender` 是一个渲染文章的对象，`bookArticles `接收一个文章数组来渲染。上文代码中入参仅支持数组类型，如果我们想同时支持 `Array` 和` Set`类型，Swift 5.7 之前我们一般使用泛型来处理：

```swift
func bookArticlesGeneric<T: Collection>(_ articles: T) where T.Element == Article {}
```

通过泛型来约束入参为集合类型，这样写是没有问题的，但更简洁的编写方式在 Swift 5.7 中出现了，我们可以使用 `some` 修饰参数入参从而实现将 `Collection`协议用做类型约束的目的。如下：

```swift
func bookArticlesOpaque(_ articles: some Collection) {}
```

这样编写的代码同样支持入参为集合类型 `Array` 和 `Set`。Swift 5.7 允许我们使用 `some` 修饰存在关联类型或者 `Self`的协议直接当做参数类型使用，而不仅限于不透明返回类型。这一特性可称为不透明参数。更详细可以参考 [SE-0341](https://github.com/apple/swift-evolution/blob/main/proposals/0341-opaque-parameters.md "SE-0341")。

对比以上泛型和 `some` 两种实现方式可以发现，不透明参数写法暂时还不能完全等价于泛型的方式。原因在于泛型函数不仅限制了入参类型为 `Collection` 集合类型，同时限制了元素 `Element` 类型为 `Article` 。而 `some`仅仅是限制了 `Collection`集合类型，对于元素类型却没有限制。这其实是不完整的功能替换，所以 Swift 5.7 中又新增了另一项特性来解决该问题。就是接下来的 **primary associated types**。

#### primary associated types

[SE-0346](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fapple%2Fswift-evolution%2Fblob%2Fmain%2Fproposals%2F0346-light-weight-same-type-syntax.md "SE-0346") 中引入了更简洁的语法来实现特定场景下指明协议关联类型的需求。该特性是对泛型协议能力的扩展。继续上文的示例，如果我们仍然想用 `some`替代泛型，同时保留指明 `Collection` 元素类型的需求。那么我们不得不在 `Collection` 协议本身上下功夫。

```swift
func bookArticlesOpaque(_ articles: some Collection) where Collection.Element == Article {} // Error
```

我们没有办法使用类似上面代码中的 `where`来约束关联类型，因为这里的 `Collection` 代表的仍然是协议而非是具体类型。所以我们的实际需求转为了 “需要在使用协议时，有一种途径可以指明约束的关联类型”。这就是 **primary associated types**。

Swift 5.7 中 `Collection` 的定义由 `public protocol Collection : Sequence {}` 变为了 `public protocol Collection<Element> : Sequence {}`，注意对比，这里多出的 `<Element>`实际就是所谓的 primary associated types。它即像协议又类似泛型的语法。

之所以叫做 **primary**，是因为并不是所有的关联类型都应该在这里声明。相反。应该只列出最关心的那些关联类型，剩余的关联类型仍然由编译器推断决定。

在使用该协议时，可以直接通过类似泛型的语法来指明该关联类型的具体类型。例如我们上面的例子：

```swift
func bookArticlesOpaque(_ articles: some Collection<Article>) {}
```

此时通过 `some` 实现的 `bookArticlesOpaque` 才和泛型的函数 `bookArticlesGeneric`完全等价。

Swift 标准库的部分协议已经改写为 **primary associated types**，同样这一特性也支持我们自定义的协议，语法是相同的。

> 另外相关联的特性还包括泛型和 `some`、`any`之间的实现异同。以及如何取舍的问题。

* [What’s new in Swift 5.7](https://www.hackingwithswift.com/articles/249/whats-new-in-swift-5-7  "What’s new in Swift 5.7")
* [What are primary associated types in Swift 5.7?](https://www.donnywals.com/what-are-primary-associated-types-in-swift-5-7/  "What are primary associated types in Swift 5.7?")

***
### 解决使用 AVAudioRecorder 录音保存 .WAV 文件遇到的问题

整理编辑：[FBY 展菲](https://github.com/fanbaoying)

#### 问题背景

App 实现录音保存音频文件，并实现本地语音识别匹配功能。

通过网络请求上传完成语音匹配的音频文件。

服务器接收到文件并进行语音识别，使用的是第三方微软语音识别，只支持 `PCM` 数据源的 `WAV` 格式。

本地识别没有任何问题，上传到服务器的文件无法识别，微软库直接报错。猜测上传的音频格式有误，导致的问题。

#### 问题代码

```objectivec
- (NSDictionary *)getAudioSetting {NSMutableDictionary *dicM=[NSMutableDictionary dictionary];
    // 设置录音格式
    [dicM setObject:@(kAudioFormatLinearPCM) forKey:AVFormatIDKey];
    // 设置录音采样率，8000 是电话采样率，对于一般录音已经够了
    [dicM setObject:@(16000) forKey:AVSampleRateKey];
    // 设置通道, 这里采用单声道 1 2
    [dicM setObject:@(2) forKey:AVNumberOfChannelsKey];
    // 每个采样点位数, 分为 8、16、24、32
    [dicM setObject:@(16) forKey:AVLinearPCMBitDepthKey];
    // 是否使用浮点数采样
    [dicM setObject:@(NO) forKey:AVLinearPCMIsFloatKey];
    //.... 其他设置等
    return dicM;
}
```

在没有使用微软语音识别库之前，使用上面的代码没有任何问题。识别库更新之后，不识别上传的的音频文件。

一开始以为是因为没有使用浮点数采样导致音频文件被压缩。修改后依然没有解决问题。

经过和服务器的联调，发现 .wav 音频文件的头部信息服务区无法识别。

#### 解决方案

当音频文件保存为 `.wav` 格式的时候，`iOS11` 以下的系统，`.wav` 文件的头部信息是没问题，但是在 `iOS11+` `.wav` 文件的头部信息服务区识别不了。

需要设置 `AVAudioFileTypeKey` 来解决这个问题。代码如下：

```objectivec
- (NSDictionary *)getAudioSetting {NSMutableDictionary *dicM=[NSMutableDictionary dictionary];
    // 设置录音格式
    [dicM setObject:@(kAudioFormatLinearPCM) forKey:AVFormatIDKey];
    if (@available(iOS 11.0, *)) {[dicM setObject:@(kAudioFileWAVEType) forKey:AVAudioFileTypeKey];
    } else {// Fallback on earlier versions}
    // 设置录音采样率，8000 是电话采样率，对于一般录音已经够了
    [dicM setObject:@(16000) forKey:AVSampleRateKey];
    // 设置通道, 这里采用单声道 1 2
    [dicM setObject:@(2) forKey:AVNumberOfChannelsKey];
    // 每个采样点位数, 分为 8、16、24、32
    [dicM setObject:@(16) forKey:AVLinearPCMBitDepthKey];
    // 是否使用浮点数采样
    [dicM setObject:@(NO) forKey:AVLinearPCMIsFloatKey];
    //.... 其他设置等
    return dicM;
}
```

参考：[解决使用 AVAudioRecorder 录音保存 .WAV 文件遇到的问题 - Swift 社区](https://mp.weixin.qq.com/s/MZqpzCAkWE9gGpsAYyo_aw "解决使用 AVAudioRecorder 录音保存 .WAV 文件遇到的问题 - Swift 社区")

***
整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### iOS 使用 Pod 在现有项目上集成 React Native

#### 问题背景

现有前端开发人员的技术栈为 React，在实践中尝试集成 RN

原生项目与 RN 项目为双独立项目，互不干预

现有项目较小，未涉及到组件化，且暂时未有相关沉淀

#### 解决方案

首先，获取 React Native  项目：我们将 RN 项目作为子项目集成现有原生项目中，利用 Git 提供的子模块功能，将一个 、RN  仓库作为 iOS 仓库的子目录。 子模块能让你将另一个仓库克隆到自己的项目中，同时还保持提交的独立。

> git submodule add <url> <repo_name>

其次，搭建 RN 开发环境，进入到 RN  的子目录中，参照[搭建开发环境](https://www.react-native.cn/docs/environment-setup)完成 [Node](http://nodejs.cn)、[Watchman](https://facebook.github.io/watchman)、[Yarn](http://yarnpkg.com/) 的安装，并通过命令安装 RN

> yarn add react-native

这里需要注意的是，我们是根据已有的子某块来创建的，所以我们还需要安装指定版本的 React

> yarn add react@xx.xx.xx

再次，安装成功之后，我们通过 CocoaPods 来完成相关依赖的安装。建议使用官方推荐 Podfile 完成安装

```ruby
require_relative '../node_modules/react-native/scripts/react_native_pods'
require_relative '../node_modules/@react-native-community/cli-platform-ios/native_modules'

platform :ios, '12.4'
install! 'cocoapods', :deterministic_uuids => false

production = ENV["PRODUCTION"] == "1"

target 'HelloWorld' do
  config = use_native_modules!

  # Flags change depending on the env values.
  flags = get_default_flags()

  use_react_native!(
    :path => config[:reactNativePath],
    # to enable hermes on iOS, change `false` to `true` and then install pods
    :production => production,
    :hermes_enabled => flags[:hermes_enabled],
    :fabric_enabled => flags[:fabric_enabled],
    :flipper_configuration => FlipperConfiguration.enabled,
    # An absolute path to your application root.
    :app_path => "#{Pod::Config.instance.installation_root}/.."
  )

  target 'HelloWorldTests' do
    inherit! :complete
    # Pods for testing
  end
  
end
```

你可以将 `react_native_pods` 文件移到原生项目目录，移除 `hermes` 和 `fabric` 这两个三方库，其余为 RN 必备的核心库。`native_modules` 中对应的是项目中添加的其他三方依赖的内容，你也可以手动安装。

最后，新增官网项目中的两个 `Build Phase` 用于启动 RN 服务。分别是

```bash
export RCT_METRO_PORT="${RCT_METRO_PORT:=8081}"
echo "export RCT_METRO_PORT=${RCT_METRO_PORT}" > "${SRCROOT}/../node_modules/react-native/scripts/.packager.env"
if [ -z "${RCT_NO_LAUNCH_PACKAGER+xxx}" ] ; then
  if nc -w 5 -z localhost ${RCT_METRO_PORT} ; then
    if ! curl -s "http://localhost:${RCT_METRO_PORT}/status" | grep -q "packager-status:running" ; then
      echo "Port ${RCT_METRO_PORT} already in use, packager is either not running or not running correctly"
      exit 2
    fi
  else
    open "$SRCROOT/../node_modules/react-native/scripts/launchPackager.command" || echo "Can't start packager automatically"
  fi
fi
```

和

```bash
set -e

WITH_ENVIRONMENT="../node_modules/react-native/scripts/xcode/with-environment.sh"
REACT_NATIVE_XCODE="../node_modules/react-native/scripts/react-native-xcode.sh"

/bin/sh -c "$WITH_ENVIRONMENT $REACT_NATIVE_XCODE"
```

至此，完成了在 iOS 中使用 Pod 在现有项目上集成 RN

以上就是单应用集成 RN 的方式，建议可以比对 CLI 自动化处的 iOS 项目来创造属于自己的脚本。

### 参考资料

[iOS 已有项目利用 Pod 集成 RN](https://blog.csdn.net/ljmios/article/details/119451577 "iOS 已有项目利用 Pod 集成 RN")

[git-submodules](https://git-scm.com/docs/git-submodule "git-submodules")

***
整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)

### 什么是 Sequence？
`Sequence` 协议是集合类型的基础，`Swift` 中的 `Sequence` 协议为序列提供了迭代能力。 `Sequence` 协议只要求实现 `makeIterator()` 方法，该方法会返回一个迭代器 `Iterator`，我们来看一下 `Sequence` 源码实现:

```Swift
public protocol Sequence {
  /// 元素类型
  associatedtype Element 
  
  /// 迭代器
  associatedtype Iterator: IteratorProtocol where Iterator.Element == Element
  
  /// 子序列
  associatedtype SubSequence : Sequence = AnySequence<Element>
    where Element == SubSequence.Element,
          SubSequence.SubSequence == SubSequence
  
  /// 返回当前迭代器
  __consuming func makeIterator() -> Iterator
  ///...
}
```

子序列 `subSequence`  是 `Sequence` 的另一个关联类型，通过切片操作（`split`,`prefix`,`suffix`,`drop`等）会返回 `subSequence` 类型



首先我们先看下 `IteratorProtocol` 的源码:

```Swift
public protocol IteratorProtocol {
  
  associatedtype Element

  mutating func next() -> Element?
}
```

`IteratorProtocol` 的核心是 `next()`  方法，这个方法在每次被调用时返回序列中的下一个值。当序列下一个值为空时，`next()` 则返回 `nil` 



`IteratorProtocol` 协议与 `Sequence` 协议是一对紧密相连的协议。序列通过创建一个提供对其元素进行访问的迭代器，它通过跟踪迭代过程并在调用 `next()` 时返回一个元素。

`for-in` 访问序列或者集合时，`Swift` 底层则是通过迭代器来循环遍历数据

```Swift
let numbers = ["1", "2", "3"]
for num in numbers {
    print(num)
}

/// 底层代码
let numbers = ["1", "2", "3"]
var iterator = numbers.makeIterator()
while let num = iterator.next() {
    print(num)
}
```



我们可以实现一个自己的序列，实现一个输出 0..n 的平方数的序列

```Swift
struct SquareIterator: IteratorProtocol {
    typealias Element = Int
    var state = (curr: 0, next: 1)
    mutating func next() -> SquareIterator.Element? {
        let curr = state.curr
        let next = state.next
        state = (curr: next, next: next + 1)
        if curr == 0 {
            return 0
        }
        return curr * curr
    }
}

struct Square: Sequence {
    typealias Element = Int
    func makeIterator() -> SquareIterator {
        return SquareIterator()
    }
}

// 通过实现了 Sequence 与 IteratorProtocol 两个协议，就可以实现我们的自定义序列
let square = Square()
var iterator = square.makeIterator()
while let num = iterator.next(), num <= 100 {
    print(num) // 0,1,4,9,16,25,36,49,64,81,100
}
```

 我们实现了一个自定义的序列，它支持通过迭代器遍历序列的所有元素，但是无法通过索引下标的方式来访问序列元素，想要实现下标访问，就需要 `Collection` 协议了



### Collection
`Collection` 继承自 `Sequence` ，是一个元素可以反复遍历并且可以通过索引的下标访问的有限集合。我们来看一下 `Collection` 源码实现：

```Swift
public protocol Collection: Sequence {
  /// 重写 Sequence 的 Element 
  override associatedtype Element
  associatedtype Index : Comparable
  
  /// 非空集合中第一个、最后一个元素的位置；
  var startIndex: Index { get }
  var endIndex: Index { get }
  associatedtype Iterator = IndexingIterator<Self>
  
  /// 重写 Sequence 的 makeIterator 
  override __consuming func makeIterator() -> Iterator

  associatedtype SubSequence: Collection = Slice<Self>
  where SubSequence.Index == Index,
        Element == SubSequence.Element,
        SubSequence.SubSequence == SubSequence
  
  /// 下标访问集合元素
  @_borrowed
  subscript(position: Index) -> Element { get }
  subscript(bounds: Range<Index>) -> SubSequence { get }

  associatedtype Indices : Collection = DefaultIndices<Self>
    where Indices.Element == Index, 
          Indices.Index == Index,
          Indices.SubSequence == Indices
   /// 集合的索引    
  var indices: Indices { get }
}
```



通过源码解析，我们可以发现 `Collection` 与 `Sequence` 最大的不同点是提供了索引能力，提供了通过下标访问元素的能力。 `Collection` 的自定义了迭代器 `IndexingIterator` , 我们来看一下 `IndexingIterator` 的源码实现：

 ```Swift
public struct IndexingIterator<Elements : Collection> {
  /// 需要迭代的集合
  internal let _elements: Elements
  
  /// 记录遍历的index
  internal var _position: Elements.Index
  
  init(_elements: Elements) {
    self._elements = _elements
    self._position = _elements.startIndex
  }
  init(_elements: Elements, _position: Elements.Index) {
    self._elements = _elements
    self._position = _position
  }
}
extension IndexingIterator: IteratorProtocol, Sequence {
  public typealias Element = Elements.Element
  public typealias Iterator = IndexingIterator<Elements>
  public typealias SubSequence = AnySequence<Element>
  
  public mutating func next() -> Elements.Element? {
    if _position == _elements.endIndex { return nil }
    let element = _elements[_position]
    _elements.formIndex(after: &_position)
    return element
  }
}
 ```

从源码可以看出，`IndexingIterator` 的主要作用就是在迭代器执行 `next()`方法时，记录了当前的 `position`，从而实现了记录索引，以及当 `position `等于 `elements.endIndex` 时，返回 `nil`


这只是 `Collection` 的冰山一角，还有`LazySequence`、高阶函数实现等， 如果感兴趣的同学，可以深入研究研究


***
整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Swift 闭包中的变量捕获

熟悉 OC 的读者都了解，OC 中 `Block`变量捕获根据变量的类型不同和修饰符的不同，有引用和拷贝两种方式。然而这套逻辑直接套用到 Swift 的闭包捕获中是不成立的。Swift 捕获方式有两种：捕获列表、隐式捕获。

#### 隐式捕获

隐式捕获即直接引用变量，这种方式是对变量指针的捕获，使其引用计数增加，在闭包作用域期间指针不会被释放。这类似于 `Block `中对引用类型变量的捕获。区别在于 Swift 中即使是值类型的变量，捕获的也是该变量的指针而非值的拷贝，即闭包中执行时是变量改变后的新值。

```swift
var value = 10
    delay(seconds: 1) {
        print("value : \(value)")
    }
    value = 20

// 打印结果为 value: 20
```

简单理解就是，直接捕获捕获到的是变量指针，无论该指针指向的是引用类型变量，还是值类型变量，都是在闭包执行时再通过指针去获取最终的值。所以在闭包执行之前改变变量值都会生效。

#### 捕获列表

捕获列表又称为显式捕获，这种方式是对变量指针指向的值进行捕获。形式上表现出的特征是在闭包创建时就立即捕获指针的值，后续即使改变指针的指向，也不会影响闭包内的值 **注意这里改变的是指针指向，而非指针指向的值更新**。

```swift
var value = 10
    delay(seconds: 1) { [vle = value] in
        print("value : \(vle)")
    }

    value = 20

// 打印结果为 value: 10
```

**需要注意的是：当使用捕获列表时，针对变量是引用类型还是值类型，结果是不一样的，会涉及到拷贝还是引用，这里是和直接捕获有所差异的地方。**

```swift
var per = PersonClosure(name: "哈哈", age: 10)
    
    delay(seconds: 1) { [per = per] in
        print("name: \(per.name) age: \(per.age)")
    }

    per.name = "xxi"
```

当 `PersonClosure` 是值类型，则改变 `per.name`的值不会影响闭包创建时捕获到的值。原因是值类型创建时是拷贝方式捕获的。后续改变不影响拷贝的值。

当 `PersonClosure`是引用类型，则闭包创建时对该 `PersonClosure`对象只是引用计数增加，`per.name` 会改变闭包执行时的值。 但是如果是 `per = PersonClosure(name: "xxi", age: 10)` 改变指针指向，则不会改变闭包内的捕获的变量值。（这里就是上文所提到的：改变指针指向不会影响值，而改变指针指向的值更新会影响闭包执行）

#### 弱引用捕获

弱引用捕获是捕获列表的一种特殊情况，不会导致引用计数的增加。由于变量类型是值类型时，捕获列表是直接拷贝，所以无法针对值类型的捕获列表使用弱引用。

弱引用捕获用来处理闭包的循环引用，类似 OC 中的 weak 修饰符的作用。

最后以一道测试题，来测试下是否理解了闭包的捕获方式：

```swift
class Pokemon: CustomDebugStringConvertible {
  let name: String
  init(name: String) {
    self.name = name
  }
  var debugDescription: String { return "<Pokemon \(name)>" }
  deinit { print("\(self) escaped!") }
}

func delay(seconds: Int, closure: @escaping ()->()) {
  let time = DispatchTime.now() + .seconds(seconds)
    DispatchQueue.main.asyncAfter(deadline: time, execute: DispatchWorkItem(block: {
        print("🕑")
        closure()
    }))
}

func demo7() {
  var pokemon = Pokemon(name: "Mew")
  print("➡️ Initial pokemon is \(pokemon)")
  delay(1) { [capturedPokemon = pokemon] in
    print("closure 1 — pokemon captured at creation time: \(capturedPokemon)")
    print("closure 1 — variable evaluated at execution time: \(pokemon)")
    pokemon = Pokemon(name: "Pikachu")
    print("closure 1 - pokemon has been now set to \(pokemon)")
  }
  pokemon = Pokemon(name: "Mewtwo")
  print("🔄 pokemon changed to \(pokemon)")
  delay(2) { [capturedPokemon = pokemon] in
    print("closure 2 — pokemon captured at creation time: \(capturedPokemon)")
    print("closure 2 — variable evaluated at execution time: \(pokemon)")
    pokemon = Pokemon(name: "Charizard")
    print("closure 2 - value has been now set to \(pokemon)")
  }
}

输出结果为：
➡️ Initial pokemon is <Pokemon Mew>
🔄 pokemon changed to <Pokemon Mewtwo>
🕑
closure 1 — pokemon captured at creation time: <Pokemon Mew>
closure 1 — variable evaluated at execution time: <Pokemon Mewtwo>
closure 1 - pokemon has been now set to <Pokemon Pikachu>
<Pokemon Mew> escaped!
🕑
closure 2 — pokemon captured at creation time: <Pokemon Mewtwo>
closure 2 — variable evaluated at execution time: <Pokemon Pikachu>
<Pokemon Pikachu> escaped!
closure 2 - value has been now set to <Pokemon Charizard>
<Pokemon Mewtwo> escaped!
<Pokemon Charizard> escaped!
```

- [Closures Capture Semantics: Catch them all!](https://alisoftware.github.io/swift/closures/2016/07/25/closure-capture-1/ "Closures Capture Semantics: Catch them all!")

***
整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)
### iOS Memory 内存

iOS 是基于 `BSD` 发展而来，所以理解一般的桌面操作系统的内存机制是非常有必要的，这期我们就来梳理一下，内存的基础八股。

#### 交换空间

手机的物理内存比较小，如果遇到不够用的情况怎么办？， 像一些桌面操作系统，会有内存交换空间，在 `window` 上称为虚拟内存。它的机制是，在需要时能将物理内存中的一部分交换到硬盘上去，利用硬盘空间扩展内存空间。但是 `iOS` 并不支持交换空间，大多数的移动设备都不支持交换空间，移动设备的存储器通常都是闪存，它的读写速度远远小于电脑所使用的硬盘，这就导致在移动设备上就算使用了交换空间，其性能也是非常低效的。移动设备的容量本身就经常短缺、内存的读写寿命也有限，所以不适合内存交换的方案。

#### Compressed Memory

由于闪存容量和读写寿命的限制，iOS 上没有交换空间机制，取而代之使用 `Compressed memory`内存压缩

`Compressed memory` 是在内存紧张时能够将最近使用过的内存占用压缩至原有大小的一半以下，并且能够在需要时解压复用。它在节省内存的同时提高了系统的响应速度，减少了不活跃内存占用，通过压缩减少磁盘IO带来的性能损耗，而且支持多核操作，例如，假设现在已经使用了4页内存，当不访问的时候可能会被压缩为1页，再次使用到时候又会解压成4页。

#### 内存分页

虚拟内存和物理内存建立了映射的关系。为了方便映射和管理，虚拟内存和物理内存都被分割成相同大小的单位，物理内存的最小单位被称为帧（Frame），而虚拟内存的最小单位被称为页（Page）。

内存分页最大的意义在于，支持了物理内存的离散使用。由于存在映射过程，所以虚拟内存对应的物理内存可以任意存放，这样就方便了操作系统对物理内存的管理，也能够可以最大化利用物理内存。同时，也可以采用一些页面调度算法，来提高翻译的效率。

#### Page out 与 Page In

当内存不足的时候，系统会按照一定策略来腾出更多空间供使用，比较常见的做法是将一部分低优先级的数据挪到磁盘上，这个操作称为 `Page Out` 。之后当再次访问到这块数据的时候，系统会负责将它重新搬回内存空间中，这个操作称为 `Page In`

#### Clean Memory

`Clean Memory` 是指那些可以用以 `Page Out` 的内存，只读的内存映射文件，或者是`frameworks` ,每个 `frameworks` 都有 `_DATA_CONST` 段，通常他们都是 `Clean` 的，但如果用 `runtime` 进行 `swizzling` ，那么他们就会变`Dirty Memory` 

#### Dirty Memory

`Dirty Memory` 是指那些被App写入过数据的内存，包括所有堆区的对象、图像解码缓冲区。所有不属于 `clean memory` 的内存都是 `dirty memory`。这部分内存并不能被系统重新创建，所以 `dirty memory` 会始终占据物理内存，直到物理内存不够用之后，系统便会开始清理。


***
整理编辑：[FBY 展菲](https://github.com/fanbaoying)

### 如何将 NSImage 转换为 PNG

首先创建 `NSBitmapImageRep` 尺寸，并在上面绘制 `NSImage`。`NSBitmapImageRep` 需要专门构建，不是直接使用 `NSBitmapImageRep(data:)` 初始化，`NSBitmapImageRep(cgImage:)` 可以避免一些分辨率问题。

```Swift
extension NSImage {
    func pngData(
        size: CGSize,
        imageInterpolation: NSImageInterpolation = .high
    ) -> Data? {
        guard let bitmap = NSBitmapImageRep(
            bitmapDataPlanes: nil,
            pixelsWide: Int(size.width),
            pixelsHigh: Int(size.height),
            bitsPerSample: 8,
            samplesPerPixel: 4,
            hasAlpha: true,
            isPlanar: false,
            colorSpaceName: .deviceRGB,
            bitmapFormat: [],
            bytesPerRow: 0,
            bitsPerPixel: 0
        ) else {
            return nil
        }

        bitmap.size = size
        NSGraphicsContext.saveGraphicsState()
        NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
        NSGraphicsContext.current?.imageInterpolation = imageInterpolation
        draw(
            in: NSRect(origin: .zero, size: size),
            from: .zero,
            operation: .copy,
            fraction: 1.0
        )
        NSGraphicsContext.restoreGraphicsState()

        return bitmap.representation(using: .png, properties: [:])
    }
}
```

来源：[如何将 NSImage 转换为 PNG - Swift 社区](https://blog.csdn.net/qq_36478920/article/details/126182661?spm=1001.2014.3001.5501 "如何将 NSImage 转换为 PNG - Swift 社区")

### 如何在 macOS 中找到以前最前沿的应用程序

监听 `didActivateApplicationNotification` 并过滤结果获取希望找到的应用程序。

```Swift
NSWorkspace.shared.notificationCenter
    .publisher(for: NSWorkspace.didActivateApplicationNotification)
    .sink(receiveValue: { [weak self] note in
        guard
            let app = note.userInfo?[NSWorkspace.applicationUserInfoKey] as? NSRunningApplication,
            app.bundleIdentifier != Bundle.main.bundleIdentifier
        else { return }
        
        self?.frontMostApp = app
    })
    .store(in: &bag)
```

来源：[如何在 macOS 中找到以前最前沿的应用程序 - Swift 社区](https://blog.csdn.net/qq_36478920/article/details/126504375?spm=1001.2014.3001.5501 "如何在 macOS 中找到以前最前沿的应用程序 - Swift 社区")


***
整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### 移动网络的优化方向

移动网络的优化方向一般从下面三个方面考量：

1. 速度：网络请求的速度怎样能进一步提升？
2. 弱网：移动端网络环境随时变化，经常出现网络连接很不稳定可用性差的情况，怎样在这种情况下最大限度最快地成功请求？
3. 安全：怎样防止被第三方窃听/篡改或冒充，防止运营商劫持，同时又不影响性能？

#### 如何提升速度

不考虑服务器响应时间及基于 TCP 协议，网络请求的流程可以简单分为下面 3 步：

1. DNS 解析，请求 DNS 服务器，获取域名对应的 IP 地址
2. 与服务端建立连接，包括 TCP 三次握手，安全协议同步流程
3. 连接建立完成，发送和接收数据，解码数据

我们可以通过下面三个方面来优化网络速度

1. 直接使用 IP 地址，去除 DNS 解析步骤（一般使用 `HTTPDNS`）
2. 不要每次请求都重新建立连接，复用连接或一直使用同一条连接（长连接）
3. 压缩数据，减小传输的数据大小

### DNS 解析的相关问题

DNS（Domain Name System，域名系统），DNS 服务用于在网络请求时，将域名转为 IP 地址。能够使用户更方便的访问互联网，而不用记住能够被机器直接读取的 IP。

> 域名到 IP 地址的映射，DNS 解析请求采用 UDP 数据报，且明文

DNS 解析的查询方式分为递归查询`和`迭代查询`

* 递归查询：如果主机所询问的本地域名服务器不知道被查询域名的 IP 地址，那么本地域名服务器就以 DNS 客户的身份，向其他根域名服务器继续发出查询请求报文，而不是让该主机自己进行下一步的查询。
* 迭代查询：当根域名服务器收到本地域名服务器发出的迭代查询请求报文时，要么给出所要查询的 IP 地址，要么告诉本地域名服务器：你下一步应当向哪一个域名服务器进行查询。然后让本地域名服务器进行后续的查询，而不是替本地域名服务器进行后续的查询。

#### DNS 解析存在哪些常见问题

DNS 完整的解析流程很长，会先从本地系统缓存取，若没有就到最近的 DNS 服务器取，若没有再到主域名服务器取，每一层都有缓存，但为了域名解析的实时性，每一层缓存都有过期时间，这种 DNS 解析机制有几个缺点：

##### 解析问题

DNS 解析过程不受控制，无法保证解析到最快的 IP。而且一次请求只能解析**一个**域名，大量请求会阻塞流程。

##### 时效问题

缓存时间设置得长，域名更新不及时，设置得短，大量 DNS 解析请求影响请求速度

##### 域名劫持

**域名劫持**，容易被中间人攻击，或被运营商劫持，把域名解析到第三方 IP 地址

#### HTTPDNS

为了解决 DNS 解析的问题，于是有了 HTTPDNS。

HTTPDNS 利用 HTTP 协议与 DNS 服务器交互，代替了传统的基于 UDP 协议的 DNS 交互，绕开了运营商的 Local DNS，有效防止了域名劫持，提高域名解析效率。另外，由于 DNS 服务器端获取的是真实客户端 IP 而非 Local DNS 的 IP，能够精确定位客户端地理位置、运营商信息，从而有效改进调度精确性。


***
整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)

#### OC泛型中的  `__covariant`  与 `__contravariant`

 `__covariant` 与 `__contravariant` 分别是OC泛型当中的关键字

* `__covariant` 代表协变，子类转成父类，子类型可以和父类型一样使用。
* `__contravariant`  代表逆变，父类转成子类，父类型可以和子类型一样使用。

我们来看一下 `__covariant` 的作用：

```objectivec
@interface Car : NSObject 
@property (nonatomic, copy) NSString *name;
@end
  
@interface BMW : Car 
@end
  
@interface Person<__covariant T> : NSObject
@property (nonatomic, strong) T car;
@end  
...
Person<BMW *> * personBMW = [[Person alloc]init];;
BMW * bmw = [[BMW alloc]init];
personBMW.car = bmw;
personBMW.car.name = @"BMW";
      
Person<Car *> * pCar = [[Person alloc]init];  
pCar = personBMW;  
NSLog(@"%@",pCar.car.name); // BMW
```
我们可以看到上述实例当中，子类型 `BMW` 成功转换成了父类型 `Car`

我们再来看看 `__contravariant` 的作用：

```C++
  // 不使用__contravariant 的情况下
  Person<Car *> * PCar = [[Person alloc]init];
  Person<BMW *> * PBMW = [[Person alloc]init];
  BMW * bmw = [[BMW alloc]init];
  PBMW.car = bmw;
  PBMW.car.name = @"BMW";
  PBMW = PCar;  // ⚠️ 出现警告 Incompatible pointer types assigning to 'Person<BMW *> *' from 'Person<Car *> *'
```

```objectivec
@interface Person<__contravariant T> : NSObject
@property (nonatomic, strong) T car;
@end
...
Person<Car *> * PCar = [[Person alloc]init];
Person<BMW *> * PBMW = [[Person alloc]init];
BMW * bmw = [[BMW alloc]init];
PBMW.car = bmw;
PBMW.car.name = @"BMW";
PBMW = PCar; // 这时候再去赋值，不会出现警告
```

***
整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### 符号 Symbol 了解

#### 符号定义

开发过程中经常遇到一类 error 提示： `Symbol not found:xxx`， 我们都知道这是存在未定义的类、变量、方法等。这里的  `Symbol`可以理解为一种数据结构，包含类型和名称等数据信息。对应一个类或者方法的地址。编译过程中不同文件之间接就是靠 `Symbol`正确的拼合到一起的。它可以是方法定义、类型定义或者数据定义。二进制文件中会存在特定的区间用于存储符号，称为符号表，根据作用的不同分为符号表和间接符号表。

#### 符号的分类

符号可以简单的分为全局符号（Global）、本地符号（Local）和调试符号。

- 全局符号： 目标文件外可见的符号，可以被其他目标文件引用，或者自己使用但是需要在其他目标文件定义的符号。
- 本地符号： 只有目标文件内可见的符号，一般只在目标文件内部引用，例如私有的方法等。
- 调试符号： 调试符号不涉及引用权限概念，它是为了做 `debug` 存在的符号，包括行号信息等调试阶段需要的数据。行号信息记录了函数或者变量的所在文件以及对应行号。一般调试符号会在 `release`阶段被移除，也就是常说的 `Strip` 符号裁剪。可以在 `Xcode Build Setting`中找到相关配置。

> 可以通过 `LLVM` 的 `nm`工具直观的查看二进制文件中的符号信息。具体可以通过 `man nm` 来查看相关指令

通过 `nm` 直观的看到符号信息中，例如图片所示

![](https://cdn.zhangferry.com/Images/weekly_69_study_01.jpg)

第一列为符号地址，第二列为符号类型，第三列为符号名称。第二列符号类型中大写字母代表是全局符号，小写字母代表本地符号。又根据不同的类型，使用不同的字母表示，这里列出常见的几种：

- U: undefined（未定义符号）
- A: absolute（绝对符号）
- T: text section symbol(\__Text.__text)
- D: data section symbol（\__DATA.__data）
- B: bss section symbol（\__DATA.__bss）
- C: common symbol（只能出现在MH_OBJECT类型的Mach-O⽂件中）
- S: 除了上⾯所述的，存放在其他section的内容，例如未初始化的全局变量存放在（\__DATA,__common）中
- -: debugger symbol table

上面提到了全局符号和本地符号的不同点，可能会好奇有没有办法在开发阶段人工干预呢。

其实是可以的。实际开发过程中，可以通过 `__attribute__((visibility("default")))` 和 `__attribute__((visibility("hidden")))`分别修饰符号，达到控制符号类型的目的。例如

```c++
__attribute__((visibility("default"))) void MyFunction1() {} 
__attribute__((visibility("hidden"))) void MyFunction2() {}
```

`default`默认可见，`hidden`则不可见。

Xcode 中 `Build Setting -> Symbols Hidden by Default`也可以设置默认配置。

另外在针对动态库还可以通过编译参数 `-exported_symbols_list`和 `-unexported_symbols_list` 设置导出符号文件和非导出符号文件。

`exported_symbols_list`设置的导出符号可以理解为全局符号，未指定的符号默认是本地符号不可访问。`unexported_symbols_list`同理。

#### 符号生成规则

- C 语言： 比较简单，一般就是在函数或者变量的前面加下划线`_`

- C++: 因为支持 namespace、函数重载等高级特性，所以采用了 `Symbol Mangling`，不同编译器可能规则不同。

    例如

    ```c++
    namespace MyNameSpace {
        class MyClass{
        public:
            static int myFunc(int);
            static double myFunc(double);
        };
    }
    
    // 0000000000000008 T __ZN11MyNameSpace7MyClass6myFuncEd
    // 0000000000000000 T __ZN11MyNameSpace7MyClass6myFuncEi
    ```

    - 以_Z开头
    - C语言的保留字符串N
    - 对于 `namespace` 等嵌套的名称，接下依次拼接名称长度，名称
    - 然后是结束字符E
    - 最后是参数的类型，比如int是i，double是d

- OC: 格式一般是 `+/-[Class_name(category_name) method:name:]`。`+/-`表示类方法或者实例方法。然后依次是类名（分类名），方法名。

- Swift: 采用了类似于 `c++`的 `name mangling`, 暂时不太了解 Swift实际规则，但是可以使用 `xcrun swift-demangle `来反解析一个符号到对应的信息。

篇幅原因， Symbol 的一些应用场景以及存储相关信息后续更新。

- [iOS强化 : 符号 Symbol](https://www.jianshu.com/p/4493ab03d5b2 "iOS强化 : 符号 Symbol")
- [深入理解 Symbol](https://mp.weixin.qq.com/s/uss-RFgWhIIPc6JPqymsNg "深入理解 Symbol")


***
整理编辑：[FBY 展菲](https://github.com/fanbaoying)

### App Store 已上架项目打开瞬闪问题

#### 1. 问题背景

用户反馈 iPhone11 iOS14.7 下载安装 App 后，点击图标，App 闪一下就回到了桌面。

收到问题反馈之后，使用手上测试机测试，iPhone11 iOS15.5 和 iPhone12 iOS15.0 均没有复现问题。

一时没有找到和用户相同的版本的测试手机，找到一台 iPhone11 iOS13.6 的手机。复现了问题。

后面使用 iPhone7 iOS13.6 也复现了问题。iPhoneX iOS16.0 没有问题。

#### 2. 问题分析

问题分析使用的是 iPhone11 iOS13.6 和 iPhone7 iOS13.6 两部手机。

App 安装版本限制是 iOS13 及以上版本。

**怀疑一：** 是项目中引入的音频动态库版本太老不兼容导致。

检查之后发现虽然和最新版本差了2个小版本，并且文档中没有更新提示相关兼容性问题。并且项目打包上架，经过了 `Validate App`。排除怀疑。

**怀疑二：** 系统 Api 在 iOS15.0 以下版本不兼容 。

如果是系统 Api 不兼容，不管是直接在 App store 下载安装，还是直接编译到手机，都会有问题。实际测试，直接编译到手机没有复现问题。

**怀疑三：** 群友提出可能是因为 Xcode 版本太老导致的问题

我目前的 Xcode 版本是 13.3.1，最新版本是 13.4.1，只差了一个小版本。

**怀疑四：** 群友提出可能电脑是 M1 芯片导致

感觉关系不大。

#### 3. 问题调试

根据以上的四个疑问，逐个排查。

在调试之前，已经清除掉手机上已经存在的 App，并且卸载清除掉所有缓存。

**1. 联机调试**

手机连接电脑，直接编译到手机中。App 正常使用，没有闪退问题

**2. Crashes**

Xcode 中的 Crashes 也没有收到任何崩溃信息。

**3. TestFlight**

通过 TestFlight 的内外部测试，收集闪退的问题。

**4. 升级 Xcode**

申请使用备用电脑，进行 Xcode 升级，项目打包上架。在 Xcode 升级到 13.4.1 后打包上架的项目，闪退的问题消失。


来源：[App Store 已上架项目打开瞬闪问题 - Swift 社区](https://mp.weixin.qq.com/s/QOB5alijsV5Gg8pi4lg03g "App Store 已上架项目打开瞬闪问题 - Swift 社区")

***
整理编辑：[FBY 展菲](https://github.com/fanbaoying)

### iOS Xcode 解决 Showing Recent Messages :-1: Unable to load contents of file list

Xcode 运行 pod 项目报错 Showing Recent Messages :-1: Unable to load contents of file list

```
Showing Recent Messages
:-1: Unable to load contents of file list: '/Users/fanbaoying/Desktop/AWSDemo/amazon-freertos-ble-ios-sdk/Example/AmazonFreeRTOSDemo/Pods/Target Support Files/Pods-AmazonFreeRTOSDemo/Pods-AmazonFreeRTOSDemo-frameworks-Debug-output-files.xcfilelist' (in target 'AmazonFreeRTOSDemo')
```

导致原因：
因为是下载的第三方的项目 cocoapods 的版本不同导致

解决方法：

重新安装或者升级一下就好

```
sudo gem install cocoapods
```

然后把工程里面的 Pod 文件夹和 Podfile.lock 文件删掉，然后 cd 到项目根目录，然后重新运行一下 pod install 命令，重新编译即可。

使用上面重新安装命令时可能会报下面的错

```
ERROR:  While executing gem ... (Gem::FilePermissionError)
    You don't have write permissions for the /usr/bin directory.
```

解决方法：

执行下面命令

```
sudo gem install cocoapods -n /usr/local/bin
```

来源：[iOS Xcode 解决 Showing Recent Messages :-1: Unable to load contents of file list - Swift社区](https://blog.csdn.net/qq_36478920/article/details/90207331 "iOS Xcode 问题解决 - Swift 社区")

### 在 iOS 16 中更改文本编辑器背景

从iOS 16开始，我们可以使用 [scrollContentBackground()](https://developer.apple.com/documentation/swiftui/view/scrollcontentbackground%28_%3A%29) 和 [background()](https://developer.apple.com/documentation/swiftui/view/background%28_%3Aignoressafeareaedges%3A%29) 视图修饰符的组合在SwiftUI中为 [TextEditor](https://developer.apple.com/documentation/swiftui/texteditor) 设置自定义背景。我们首先必须通过应用 `scrollContentBackground(.hidden)` 来隐藏 `TextEditor` 上的默认背景，否则我们的自定义背景将不可见。然后，我们可以轻松地使用 `background()` 方法设置新的背景。

```Swift
struct ContentView: View {
    @State private var text = "Some text"
    
    var body: some View {
        TextEditor(text: $text)
            .frame(width: 300, height: 200)
            .scrollContentBackground(.hidden)
            .background(.indigo)
    }
}
```

来源：[在 iOS 16 中更改文本编辑器背景 - Swift社区](https://blog.csdn.net/qq_36478920/article/details/127302530 "在 iOS 16 中更改文本编辑器背景 - Swift 社区")

***
整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### 当设置 `UIImageView` 高亮时，会暂停当前的动画

#### 问题背景

项目通过配置 `UIImageView` 的 `animationImages` 实现 `loading` 动画。项目基于 `UICollectionView` 实现分页组件。当  `loading` 动画时，双击图片，动画会暂停。

#### 问题描述

通过 `hook``UIImageView` 的 `stopAnimating` 方法并添加断点，查看当动画停止时的调用栈，发现正在设置当前 `imageView` 为高亮。

这是因为当我们双击`UICollectionView` 时，`UICollectionView` 会高亮展示当前的 `CollectionViewCell`，此行为会将当前 `CollectionViewCell`上支持高亮展示的 `subview` 的显示状态成高亮。

 `UIImageView` 在设置高亮状态时，会先调用 `stopAnimating`。

#### 解决方案

禁止 `UICollectionView` 高亮行为, `UICollectionView` 的代理方法`shouldHighlightItemAt` 返回 `false`。

```swift
optional func collectionView(
    _ collectionView: UICollectionView,
    shouldHighlightItemAt indexPath: IndexPath
) -> Bool
```

### Xcode 14 编译包在 iOS 12.2 以下设备崩溃

由于项目支持 iOS 12.0 以上，最新版本测试时发现 iOS 12.1.4 的系统无法打开安装包，而 12.4 的设备可以正常打开。

Xcode 14 的编译包会多出一些系统库，你需要添加 `libswiftCoreGraphics.tbd` ，否则在 iOS 12.2 以下的系统找不到 `libswiftCoreGraphics.tbd`  而发生崩溃。

![](https://cdn.zhangferry.com/Images/add.png)

来源：[iOS小技能：Xcode14新特性(适配）](https://juejin.cn/post/7150842048944767006 "iOS小技能：Xcode14新特性(适配）")

***
整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)

#### Swift 函数派发方式总结

`Swift` 当中主要有三种派发方式
- sil_witness_table/sil_vtable：函数表派发
- objc_method：消息机制派发
- 不在上述范围内的属于直接派发



这里总结了一份 `Swift` 派发方式的表格

|            |                         **直接派发**                         |  **函数表派发**  |                   **消息派发**                   |
| :--------: | :----------------------------------------------------------: | :--------------: | :----------------------------------------------: |
|  NSObject  |                @nonobjc 或者 final 修饰的方法                | 声明作用域中方法 |         扩展方法及被 dynamic 修饰的方法          |
|   Class    |        不被 @objc 修饰的扩展方法及被 final 修饰的方法        | 声明作用域中方法 |  dynamic 修饰的方法或者被 @objc 修饰的扩展方法   |
|  Protocol  |                           扩展方法                           | 声明作用域中方法 | @objc 修饰的方法或者被 objc 修饰的协议中所有方法 |
| Value Type |                           所有方法                           |        无        |                        无                        |
|    其他    | 全局方法，staic 修饰的方法；使用 final 声明的类里面的所有方法；使用 private 声明的方法和属性会隐式 final 声明； |                  |                                                  |

##### 协议 + 拓展

由上表我们可以得知，在 `Swift` 中，协议声明作用域中的方法是函数表派发，而拓展则是直接派发，当协议当中实现了 `print` 函数，那么最后调用会根据当前对象的实际类型进行调用 

```Swift
protocol testA{
  func print()
}

extension testA{
  func print(){
    print("print A")
  }
}

struct testStruct:testA {
  func print(){
    print("print B")
  }
}

let one:testA = testStruct()
let two:testStruct = testStruct()
one.print() // print B
two.print() // print B
```

**追问：如果 `protocol` 没有实现 `print()` 方法，又出输出什么？**

```swift
protocol testA{}

extension testA{
  func print(){
    print("print A")
  }
}

struct testStruct:testA {
  func print(){
    print("print B")
  }
}

let one:testA = testStruct()
let two:testStruct = testStruct()
one.print() // print A
two.print() // print B
```

因为协议中没有声明 `print` 函数，所以这时，`one` 被声明成`testA` ， 只会按照拓展中的声明类型去进行直接派发

而 `two` 被声明成为 `testStruct`，所用调用的是 `testStruct` 当中的 `print` 函数


***
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


***
整理编辑：[FBY 展菲](https://github.com/fanbaoying)

### iOS16 中的 3 种新字体宽度样式

在 iOS 16 中，Apple 引入了三种新的宽度样式字体到 SF 字体库。

1.   Compressed 

2.   Condensed 

3.   Expend

![](https://images.xiaozhuanlan.com/photo/2022/f9a30607ad412d7b23ba4e43f5396ade.png)

### UIFont.Width

Apple 引入了新的结构体 `UIFont.Width`，这代表了一种新的宽度样式。

目前已有的四种样式。

* standard：我们总是使用的默认宽度。

* compressed：最窄的宽度样式。

* condensed：介于压缩和标准之间的宽度样式。

* expanded：最宽的宽度样式。

![](https://images.xiaozhuanlan.com/photo/2022/0a80f9d3f6deb35081eb1e6ce611ab62.png)

### SF 字体和新的宽度样式

如何将 SF 字体和新的宽度样式一起使用

为了使用新的宽度样式，Apple 有一个新的 `UIFont` 的类方法来接收新的 `UIFont.Width` 。

```swift
class UIFont : NSObject {
    class func systemFont(
        ofSize fontSize: CGFloat,
        weight: UIFont.Weight,
        width: UIFont.Width
    ) -> UIFont
}
```

你可以像平常创建字体那样来使用新的方法。

```swift
let condensed = UIFont.systemFont(ofSize: 46, weight: .bold, width: .condensed)
let compressed = UIFont.systemFont(ofSize: 46, weight: .bold, width: .compressed)
let standard = UIFont.systemFont(ofSize: 46, weight: .bold, width: .standard)
let expanded = UIFont.systemFont(ofSize: 46, weight: .bold, width: .expanded)
```

来源：[iOS16 中的 3 种新字体宽度样式 - Swift 社区](https://mp.weixin.qq.com/s/84TG_7yFxpsXF7cHTbVbFw)

***
整理编辑：[阿拉卡](https://github.com/readyhe)

### 面向程序员，如何智慧提问？

在平时的工作中，相信很多的程序员小伙伴都面临两个问题：

- 经常不知道如何提出自己的问题
- 经常被其他同学打断自己的编码思路

这两个问题曾也久久困扰着小编。那么如何提升提问和被提问的能力？我们今天就聊聊**智慧的提问**这个很虚但很实用的话题，它适用于开发，产品，运营等同学

#### 提问前需要做什么？

在你准备提问时，你应该是有做过思考和前期准备的。对于程序员来说，当你遇到业务问题或者是技术问题。那么你应该有如下几点需要做到：

>尝试在旧的问题列表找到答案。
>
>尝试上网搜索以找到答案。
>
>尝试阅读手册以找到答案。
>
>尝试阅读常见问题文件（FAQ）以找到答案。
>
>尝试自己检查或试验以找到答案。
>
>尝试阅读源码找到答案。

当你提出问题的时候，请先表明你已经做了上述的努力；这将有助于树立你并不是一个不劳而获且浪费别人的时间的提问者。如果你能一并表达在做了上述努力的过程中所**学到**的东西会更好，因为我们更乐于回答那些表现出能从答案中学习的人的问题。

**准备好你的问题，再将问题仔细的思考过一遍，然后开始提问**

#### 提问时如何描述问题？

如何很好的提问，这也是我们常见的一些问题。下面是常用的一些手段：

> 使用有意义且描述明确的标题
>
> 精确地描述问题并言之有物
>
> 话不在多而在精
>
> 别动不动就说自己找到了 Bug
>
> 描述实质问题而不是你的猜测问题
>
> 按发生时间先后列出问题症状
>
> 询问有关代码的问题时，不要直接粘贴几百行代码
>
> 去掉无意义的提问句，减少无效内容
>
> 即使你很急也不要在标题写`紧急`，你可能直接都不知道是否紧急

#### Bad Question（蠢问题）

以下是几个经典蠢问题：

问题：我能在哪找到 X 程序或 X 资源？

问题：我怎样用 X 做 Y?

问题：我的程序/设定/SQL 语句没有用?

问题：我的 Mac 电脑有问题，你能帮我吗?

问题：我的程序不会动了，我认为系统工具 X 有问题

问题：我在安装 Linux（或者 X ）时有问题，你能帮我吗？

问题：你的程序有Bug，能帮我解决吗？

来源：[How To Ask Questions The Smart Way](http://www.catb.org/~esr/faqs/smart-questions.html "How To Ask Questions The Smart Way")和[提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md "提问的智慧")

***
整理编辑：[宁静致远](https://github.com/byshb)

### class_rw_t 与 class_ro_t 的区别

这两个结构体类型在苹果 opensource 的源码中定义的，于是直接打开源代码（[objc4-838](https://github.com/apple-oss-distributions/objc4/tree/objc4-838)）进行分析：

```c++
struct class_rw_t {
    ...
    const class_ro_t *ro();
    const method_array_t methods(){ ... };
    const property_array_t properties(){ ... };
    const protocol_array_t protocols(){ ... };
    ...
}
```

```c++
struct class_ro_t {
    ...
    union {
        const uint8_t * ivarLayout;
        Class nonMetaclass;
    };
    explicit_atomic<const char *> name;
    WrappedPtr<method_list_t, method_list_t::Ptrauth> baseMethods; // 方法列表
    protocol_list_t * baseProtocols; // 协议列表
    const ivar_list_t * ivars; // 成员变量列表
    const uint8_t * weakIvarLayout; 
    property_list_t *baseProperties; // 属性列表
    ...
};
```

从代码中可见 `class_ro_t` 结构体存在于 `class_rw_t` 结构体当中，下文使用 `ro` 和 `rw` 替代。

苹果 WWDC 曾经介绍过 `ro `  和 `rw` ，并引出了两个概念，clean memory 和 dirty memory。

clean memory 是指加载后不会发生改变的内存。它可以进行移除来节省更多的内存空间，需要时再从磁盘加载。

dirty memory 是指在运行时会发生改变的内存。当类开始使用时，系统会在运行时为它分配一块额外的内存空间，也就是 dirty memory，只要进程在运行，它就会一直存在，因此使用代价很高。

`ro` 放在纯净的内存空间，是只读的，对于没有使用到的 `ro`，可以进行移除，需要时再分配。

`rw` 在运行生成，可读可写，属于脏内存。

`ro` 在编译阶段创建，将类的属性，方法，协议和成员变量添加到 `ro` 中，编译后就已经确定了。

`rw` 运行的时候创建，首先会将 `ro` 中的内容**剪切**到 `rw` 中，分类中的方法会在运行时，添加到 `rw` 的 `method_array_t` 结构的 `methods` 中，由于是放到了数组的前面部分，可达到类似**覆盖**的效果。

我们分析 `rw` 的源码时，可见 methods、properties、protocols 其实是可能存在 一个叫做 `ro_or_rw_ext`变量当中，举例如下：

```c++
const method_array_t methods() const {
    auto v = get_ro_or_rwe();
    if (v.is<class_rw_ext_t *>()) {
        return v.get<class_rw_ext_t *>(&ro_or_rw_ext)->methods;
    } else {
        return method_array_t{v.get<const class_ro_t *>(&ro_or_rw_ext)->baseMethods};
    }
}
```

之所以这样设计，是由于 `rw` 属于脏内存，使用开销大，苹果在 WWDC ⾥⾯说过，只有⼤约 10% 左右的类需要动态修改。所以只有 10% 左右的类⾥⾯需要⽣成 `class_rw_ext_t` 这个结构体。把一些类的信息分离出来，这样的话，可以节约很⼤⼀部分内存。

`class_rw_ext_t` 的⽣成的条件：

1. ⽤过 Runtime 的 Api 进⾏动态修改的时候。
2. 有分类的时候，且分类和本类都为⾮懒加载类的时候。实现了 `+load` ⽅法即为⾮懒加载类。

还有就是经上述分析，成员变量是存在于 `ro` 当中的，一经编译就不能修改了，那是不是所有的类都不能运行时添加实例变量了呢？答案是运行时创建的类，可以在 `objc_allocateClassPair` 方法之后，`objc_registerClassPair` 方法之前，通过 `class_addIvar()` 添加实例变量，除此之外已经创建的类的实例变量内存布局是不能被修改的。


***
整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### 解决 Mac Intel 转 Apple Silicon 开发环境配置问题

越来越多的开发者已经使用 Apple Silicon 芯片的 mac 作为开发工具，笔者近期也更换了 M2 作为主力机，记录一下从 Intel 切换到 M2 过程中遇到的环境配置问题。

我使用 **迁移助理** 工具做的整个开发环境的拷贝，用时 1~2 小时完成了大约 250G 内容的传输，这种切换方式优势在于整个开发环境完全保持一致，不会丢失现有环境配置导致项目开发运行时才发现问题。可以快速投入开发，但也为后续的环境兼容带来了一些麻烦。所以如果你的开发机环境配置不复杂，建议重新安装开发环境。

1. 先从简单的项目适配说起，由于 Apple Silicon 是 arm 架构，如果工程 debug 环境暂未支持 arm 架构并且需要使用模拟器运行项目，有两种办法：使用 Rosetta 模式运行模拟器、或者更新 SDK 以适配 arm 架构

    建议优先工程适配 arm 架构，因为目前 Rosetta 模式运行模拟器会存在一些问题，例如列表滚动阻尼效果缺失，xcode 14 后模拟器二次 build 会黑屏卡在 `launching $(projectname)` 阶段等各种使用问题。

    > 但是一些引入的二进制 SDK 暂不支持 debug 模式的 arm架构，例如微信的 SDK。只能退而求其次通过 Rosetta 模式运行模拟器。需要设置 `Build Setting => Architectures =>Excluded Architectures` 在 debug 模式设置 `arm64` 以此移除工程 debug 模式对 arm 架构的支持，模拟器会自动切换到 Rosetta 模式。

2. 从 Intel 切换过来时 Mac 上安装的 app 大部分都是基于 Intel 架构的，在 Apple Silicon 上使用不存在问题，但是性能效率会有影响，部分软件使用时会有明显卡顿。所以建议如果软件有arm 架构或者通用架构的版本，重新安装即可。这里推荐一个应用[iMobie M1 App Checker](https://www.imobie.com/m1-app-checker/ "iMobie M1 App Checker")可以快速查询所有安装的 app 架构，如图所示：

    ![](https://cdn.zhangferry.com/Images/weekly_78_study_01.png)

3. 如果有使用 `Homebrew` 管理工具，重新安装 arm 版本后，管理的包路径发生了变更，新路径为 **/opt/homebrew/bin**，如果脚本或者配置中使用了 `Homebrew` 管理命令的绝对路径，则需要修改，例如我们工程中有引入过 `Carthage`，该工具需要在项目`Build Phases`中添加执行命令 `/usr/local/bin/carthage copy-frameworks`，编译会报错找不到 `carthage` 执行文件。

4. 更新 `Homebrew` 后建议重新安装所有已安装的库，否则后续会遇到各种离奇的问题。例如在使用 `Rbenv` 管理安装 `Ruby` 时会各种报错，因为 `Ruby`依赖 `ruby-build、readline、openssl`等工具，如果这些工具仍然是旧版本，可能会不兼容，需要重新安装最新版本。

    > `homebrew` 没有提供实现重新安装所有库的命令，可以使用管道结合`xargs`命令: `brew list | xargs brew reinstall`
    >
    > **Tips**: `shell` 中 `|` 表示管道，可以将左侧命令的标准输出转换为标准输入，提供给右侧命令。而   `xargs` 是将标准输入转为命令行参数，更多内容参考 [xargs 命令教程](https://www.ruanyifeng.com/blog/2019/08/xargs-tutorial.html "xargs 命令教程")

5. `Rbenv` 可以直接安装 `Ruby`**3.x** 版本，**2.7.1**版本则需要使用 `RUBY_CFLAGS="-w" rbenv install 2.7.1` 参数禁止所有warring 和 error，安装 **2.7.2** 及更高版本在环境中做以下配置即可（验证成功）：

    ![](https://cdn.zhangferry.com/Images/weekly78_study_02.png)

暂时遇到以上问题，如果有更多问题和疑问，可以留言讨论。

* [Installation issues with Arm Mac](https://github.com/rbenv/ruby-build/issues/1691 "Installation issues with Arm Mac")


***
整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)
#### Xcode 僵尸对象 Zombie Objects

Zombie Objects 是用来调试与内存有关的问题，跟踪对象的释放过程的工具，通常用来排查野指针问题。

在 `Xcode` -> `Edit Scheme` -> `Memory Management` -> `Zombie Objects` 

#### 僵尸对象的生成过程：

```C++
// 获取到即将deallocted对象所属类（Class）
Class cls = object_getClass(self);
    
// 获取类名
const char *clsName = class_getName(cls)
    
// 生成僵尸对象类名
const char *zombieClsName = "_NSZombie_" + clsName;
    
// 查看是否存在相同的僵尸对象类名，不存在则创建
Class zombieCls = objc_lookUpClass(zombieClsName);
if (!zombieCls) {
    // 获取僵尸对象类 _NSZombie_
    Class baseZombieCls = objc_lookUpClass(“_NSZombie_");
        
    // 创建zombieClsName类
    zombieCls = objc_duplicateClass(baseZombieCls, zombieClsName, 0);
}
// 在对象内存未被释放的情况下销毁对象的成员变量及关联引用。
objc_destructInstance(self);
    
// 修改对象的isa指针，令其指向特殊的僵尸类
objc_setClass(self, zombieCls);
```

#### Zombie Object 触发时做了什么？

```C++
// 获取对象class
Class cls = object_getClass(self);
    
// 获取对象类名
const char *clsName = class_getName(cls);
    
// 检测是否带有前缀_NSZombie_
if (string_has_prefix(clsName, "_NSZombie_")) {
    // 获取被野指针对象类名
    const char *originalClsName = substring_from(clsName, 10);
     
    // 获取当前调用方法名
    const char *selectorName = sel_getName(_cmd);
    　　
    // 输出日志
    print("*** - [%s %s]: message sent to deallocated instance %p", originalClsName, selectorName, self);
        
    // 结束进程
    abort();
}
```

系统修改对象的 `isa` 指针，令其指向特殊的僵尸类，使其变为僵尸对象，并且打印一条包含该对象的日志，然后终止应用程序。

***
整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### iOS 堆栈调用理论回顾

我们都知道程序的函数调用利用的是栈结构，每嵌套调用一次函数，就执行一次压栈操作，函数执行完毕后，执行出栈操作回到栈底(也就是函数调用处)，继续执行后续指令。
大部分操作系统栈的增长方向都是从高往低(包括 iOS / Mac OS)，意味着每次函数调用栈开辟都是在做内存地址的减法，`Stack Pointer` 指向栈顶，`Frame Pointer` 指向上一个栈帧的 `Stack Pointer`的地址值，通过 `Frame Pointer` 就可以递归回溯获取整个调用栈。 
每一次压栈时的数据结构被称为**栈帧**(Stack Frame)，里面存储了当前函数的栈顶指针以及栈底指针，如果我们能拿到每一次压栈的数据结构, 则可以根据这两个指针来递归回溯整个调用栈。

对于 x86_64或者 arm64 架构, 函数调用的汇编指令 `call/bl` 做法都是类似的：

1. 先将函数调用的下一条指令地址入栈，这一条指令是被调用函数执行结束后需要跳转执行的指令，一般存储到 `LR`寄存器中。如果后续还有其他函数调用，则会把`LR`存入栈帧进行保存。
2. 然后保存调用函数 `caller` 的 `FP` 指针，保存位置紧邻 `LR` 存储的内存地址。
3. 开辟新的栈空间，重新赋值 `FP` 指向新的栈的栈底，即被调用函数的栈帧的栈底。

![](https://cdn.zhangferry.com/Images/weekly_80_study_01.png)

通过上面的操作，我们已经可以实现串起整个函数调用链。但是由于我们只获取到 `LR`的值，它记录的是 `caller` 函数中的某一条指令地址，而我们的二进制文件存储的都是函数调用的首地址，所以要如何通过 `LR` 对应到具体的函数是下一步要做的事情。采用的方法也很好理解，即通过遍历 `MachO`的符号表，找到每个栈帧中存储的 `LR`的值最相近的高地址的函数，认为该函数是 `Caller`调用函数。

上面针对的是普通的函数调用，在实际情况下会有一些特殊的函数调用，例如内联或者尾调用等。这些都是没有办法通过上面的方式获取到调用栈的。

另外 x86_64 和 arm64 还有一些不同之处在于，arm64 下编译器可能会做一个优化：即针对叶子节点函数会优化栈帧结构，不再入栈保存 `FP`，这时读取到的 `FP`指针实际是 `Caller` 函数的 `FP`。

这个优化只针对 `FP`指针，叶子节点函数的`LR`指针还是会保存的（因为需要出栈继续执行下条指令）。所以我们可以通过线程上下文获取当前的 `LR` 对比`FP`计算得到的`LR` 是否是同一个地址，来判断最后一次的 `FP`是叶子节点函数的 `FP` 还是它的调用方的 `FP`。相同表示未优化 `FP`，不同表示已优化，则需要记录本次的 `LR`。

具体实现代码可以参考 [BSBacktraceLogger](https://github.com/bestswifter/BSBacktraceLogger "BSBacktraceLogger")，简化的核心代码如下：

```objectivec
NSString *_bs_backtraceOfThread(thread_t thread) {
  // 初始化50长度的指针数组
  uintptr_t backtraceBuffer[50];
  int i = 0;
// ...
  const uintptr_t instructionAddress = bs_mach_instructionAddress(&machineContext);
  backtraceBuffer[i] = instructionAddress;
  ++i;
  // 通过线程上下文获取 LR 地址 
  uintptr_t linkRegister = bs_mach_linkRegister(&machineContext);
  if(instructionAddress == 0) {
​    return @"Fail to get instruction address";
  }
  // 自定义的帧实体链表, 存储上一个调用栈以及返回地址(lr)
  BSStackFrameEntry frame = {0};
    
  // fp指针
  const uintptr_t framePtr = bs_mach_framePointer(&machineContext);
  if(framePtr == 0 ||
​    // 将fp存储的内容 (pre fp指针)存储到previous, fp+1 存储的内容(lr)存储到return_address
​    bs_mach_copyMem((void *)framePtr, &frame, sizeof(frame)) != KERN_SUCCESS) {
​    return @"Fail to get frame pointer";
  }
  // lr和fp读取的数据不相等, 是因为arm64下 编译器做的优化处理,即叶子函数复用调用函数的调用栈fp, 但是lr和sp是没有复用的, 所以为了避免丢帧,使用lr填充
  if (linkRegister != 0 && frame.return_address != linkRegister)  {
​    backtraceBuffer[i] = linkRegister;
​    i++;
  }
    
  // 原理就是通过当前栈帧的fp读取下一个指针数据,记录的是上一个栈帧的fp数据, fp + 2,存储的是lr数据, 即当前栈退栈后的返回地址(bl的下一条指令地址)
  for(; i < 50; i++) {
​    backtraceBuffer[i] = frame.return_address;
      // ... 容错处理
  }
  // 开始符号化，这里就是文中说的通过 lr 获取最近的函数首地址进行符号化
  int backtraceLength = i;
  Dl_info symbolicated[backtraceLength]；
  bs_symbolicate(backtraceBuffer, symbolicated, backtraceLength, 0);
    // ... 打印结果
  return [resultString copy];
}
```

代码中的 ` if (linkRegister != 0 && frame.return_address != linkRegister) ` 片段 `BSBacktraceLogger` 中是没有的，当根据打印堆栈将调用栈数调整到恰好 50 个时，会发现最后一个叶子节点函数栈帧丢失，也就是文中说的针对 arm64的优化。

以上代码仅是 `FP`和 `LR`的递归回溯的实现，符号化部分参考函数 `bs_symbolicate()`。

也可以查看 `BSBacktraceLogger` 的 [fork](https://github.com/talka123456/BSBacktraceLogger "BSBacktraceLogger fork") 版本代码，增加了核心代码逻辑注释方便学习。


