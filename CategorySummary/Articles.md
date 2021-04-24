
整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)

1、[我在Uber亲历的最严重的工程灾难](https://mp.weixin.qq.com/s/O1haH28cTr0tkhRAnVZQ6g "我在Uber亲历的最严重的工程灾难") -- 来自公众号：infoQ

准备或者已经接入Swfit可以先了解下

2、[美团 iOS 工程 zsource 命令背后的那些事儿](https://mp.weixin.qq.com/s/3qcv1NW4-ce87cvAS4Jsxg "美团 iOS 工程 zsource 命令背后的那些事儿") -- 来自公众号： 美团技术团队

美团技术团队历史文章，对DWARF文件的另一种应用。文章还原了作者解决问题的思路历程，除了技术本身外，解决问题的思路历程也是值得借鉴的。

3、[NSObject方法调用过程详细分析](https://juejin.cn/post/6844904000450478087 "NSObject方法调用过程详细分析") -- 来自掘金：maniac_kk

字节跳动maniac_kk同学的一篇优质文章，无论深度还是广度都是非常不错的，很多底层知识融会贯通，值得细细品味

4、[iOS疑难Crash的寄存器赋值追踪排查技术](https://www.jianshu.com/p/958d4f109bb0 "iOS疑难Crash的寄存器赋值追踪排查技术") -- 来自简书：欧阳大哥

在缺少行号信息时如何通过寄存器赋值推断出具体的问题代码，具有很高的参考价值，在遇到疑难问题时可以考虑是否能借鉴此思路

5、[抖音 iOS 工程架构演进](https://juejin.cn/post/6950454120826765325 "抖音 iOS 工程架构演进") -- 来自掘金：字节跳动技术团队

业务的发展引起工程架构做出调整，文章介绍了抖音的工程架构演进历程。作为日活过亿的产品，其工程架构的演变对多数APP来说都具有一定的借鉴意义。

6、[Swift的一次函数式之旅](https://mp.weixin.qq.com/s/yiF0NwXffrkunGOieWbIRA "Swift的一次函数式之旅") -- 来自公众号：搜狐技术产品

编程本身是抽象的，编程范例就是我们如何抽象这个世界的方法，而函数式编程就是其中一个编程范例。在函数式编程的世界里一切皆函数，那如何利用这个思想解决实际问题呢？文中给出了两个有趣的例子，希望可以帮你解决对函数式编程的疑惑。

7、[Category无法覆写系统方法？](https://zhangferry.com/2021/04/21/overwrite_system_category/) -- 来自公众号：iOS成长之路

这是一次非常有趣的解决问题经历，以至于我认为解决方式可能比问题本身更有意思。解决完全没有头绪的问题，我们应该避免陷入不断的猜测和佐证中。深挖问题，找到正确方向才更容易出现转机。


1、[我离职了](https://juejin.cn/post/6943384976909942815 "我离职了") -- 来自掘金：敖丙

敖丙还在B站录了[视频](https://www.bilibili.com/video/BV1cp4y1a7DW "我离职了 B站")，看视频可能更有感染力。

2、[我的玩具——乐高魔方机器人](http://xelz.info/blog/2017/02/18/lego-cube-solver/ "我的玩具——乐高魔方机器人") -- 来自博客：xelz's blog

这个真的非常有意思，有理工科思维做一件具体有趣的事情非常酷。大概思路是这样的;

- 手机与LEGO通过蓝牙连接
- LEGO检测到魔方放入之后通知手机开始扫描
- 手机扫描完一个面之后，通知LEGO将魔方翻转到下一个面
- 扫描完毕后，手机开始计算还原步骤
- 手机通过蓝牙将还原公式发送给LEGO
- LEGO按照公式将魔方还原

3、[关于bitcode, 知道这些就够了](http://xelz.info/blog/2018/11/24/all-you-need-to-know-about-bitcode/ "关于bitcode, 知道这些就够了") -- 来自博客：xelz's blog

4、[哈啰出行iOS App首屏秒开优化](https://mp.weixin.qq.com/s/5Ez2BrsyBgQ8aHZqlYtAjg "哈啰出行iOS App首屏秒开优化") -- 来自公众号：哈罗技术团队

5、[SwiftUI: Text 中的插值](https://mp.weixin.qq.com/s/PX8bXSFXgJWMgHqien85jQ "SwiftUI: Text 中的插值") -- 来自公众号：老司机技术周报

6、[深入理解MachO数据解析规则](https://mp.weixin.qq.com/s/z8s4urq_KCf2ny5kKOYMHA) -- 来自公众号：iOS成长之路

7、[MacBook 升级 SSD 硬盘指北](https://mp.weixin.qq.com/s/LMeO6chdac65JQu1Yy2-Iw) -- 来自公众号：iOS成长之路

8、[DWARF文件初探——提取轻量符号表](https://mp.weixin.qq.com/s/s8iwQLNtla5nxF_Tmj2wJg "DWARF文件初探——提取轻量符号表") -- 来自公众号：皮拉夫大王在此





这期博客推荐顺带考察了一下各大厂的技术公众号运营情况（仅限移动端），虽然技术号不能反映一个公司的全貌，但多少还是能够体现出该公司的开源分享精神的，顺道推荐几篇高质量的文章。内容较多，还会再有一期，先后顺序不代表排名。


[翻译-为什么objc_msgSend必须用汇编实现](http://tutuge.me/2016/06/19/translation-why-objcmsgsend-must-be-written-in-assembly/ "翻译-为什么objc_msgSend必须用汇编实现") -- 来自博客：土土哥的blog

[深度长文：细说iOS代码签名](http://xelz.info/blog/2019/01/11/ios-code-signature/ "深度长文：细说iOS代码签名") -- 来自博客：xelz's blog

[从Mach-O角度谈谈Swift和OC的存储差异](https://www.jianshu.com/p/ef0ff6ee6bc6 "从Mach-O角度谈谈Swift和OC的存储差异") -- 来自简书：皮拉夫大王在此

[一种Swift Hook新思路——从Swift的虚函数表说起](https://www.jianshu.com/p/0cbbbe783ac9 "一种Swift Hook新思路——从Swift的虚函数表说起") -- 来自简书：皮拉夫大王在此

[Swift5.0 的 Runtime 机制浅析](https://juejin.cn/post/6844903889523884039 "Swift5.0 的 Runtime 机制浅析") -- 来自掘金：欧阳大哥2013

[编译原理初学者入门指南](https://mp.weixin.qq.com/s/ZTxVG6KG-4vzbvclC_Q1LQ "编译原理初学者入门指南") -- 来自公众号：腾讯技术工程

[神秘！申请内存时底层发生了什么？](https://mp.weixin.qq.com/s/DN-ckM1YrPMeicN7P9FvXg "神秘！申请内存时底层发生了什么？") -- 来自公众号：码农的荒岛求生

[推荐收藏 | 美团技术团队的书单](https://tech.meituan.com/2020/04/23/read-book-2020-04-23.html "推荐收藏 | 美团技术团队的书单") -- 来自博客：美团技术团队

[青年人在美团是怎样成长的？](https://tech.meituan.com/2020/05/04/meituan-0504-young-people.html "青年人在美团是怎样成长的？") -- 来自博客：美团技术团队



[函数节流（Throttle）和防抖（Debounce）解析及其OC实现](https://mp.weixin.qq.com/s/h1MYGTYtYo9pcHmqw6tHBw "函数节流（Throttle）和防抖（Debounce）解析及其OC实现")  -- 来自公众号：iOS成长之路

[2021阿里淘系工程师推荐书单](https://mp.weixin.qq.com/s/zi7qWTg8xGf3GaxW6Czj2A "2021阿里淘系工程师推荐书单") -- 来自公众号：淘系技术

[分析字节跳动解决OOM的在线Memory Graph技术实现](https://juejin.cn/post/6895583288451465230 "分析字节跳动解决OOM的在线Memory Graph技术实现") -- 来自掘金：有点特色

[iOS 稳定性问题治理：卡死崩溃监控原理及最佳实践](https://juejin.cn/post/6937091641656721438 "iOS 稳定性问题治理：卡死崩溃监控原理及最佳实践") -- 来自掘金：字节跳动技术团队

[一个iOS流畅性优化工具](https://juejin.cn/post/6934720152546050078 "一个iOS流畅性优化工具") -- 来自掘金：BangRaJun

[iOS防黑产虚假定位检测技术](https://juejin.cn/post/6938197133908672519 "iOS防黑产虚假定位检测技术") -- 来自掘金：欧阳大哥2013

[【译】Flutter 2.0 正式版发布，全平台 Stable](https://juejin.cn/post/6935621027116531720 "[译]Flutter 2.0 正式版发布，全平台 Stable") -- 来自掘金：恋猫de小郭

[如何做一场高质量的分享](https://juejin.cn/post/6938208336802217991 "如何做一场高质量的分享") -- 来自掘金：相学长



[GitHub 2020 报告：全球开发者工作与生活的平衡情况](https://juejin.cn/post/6908880779963695118 "GitHub 2020 报告：全球开发者工作与生活的平衡情况") -- 来自掘金：LeviDing

[2020 腾讯Techo Park - Flutter与大前端的革命](https://juejin.cn/post/6908357007749693454 "2020 腾讯Techo Park - Flutter与大前端的革命") -- 来自掘金：恋猫de小郭

[WWDC20 iOS14 Runtime优化](https://mp.weixin.qq.com/s/opD__14wpHL06VKPtXeM4g "WWDC20 iOS14 Runtime优化") -- 来自公众号：知识小集

[使用 Swift 编写 CLI 工具的入门教程](https://mp.weixin.qq.com/s/V4IdsYUouKGr68ULyb88Qw "使用 Swift 编写 CLI 工具的入门教程") -- 来自公众号：一瓜技术

[阿里 10 年：一个普通技术人的成长之路](https://juejin.cn/post/6908569967289958408 "阿里 10 年：一个普通技术人的成长之路") -- 来自掘金：阿里巴巴云原生

2020年刚过完，有挺多写的非常好的年终总结可以看看：

[写在2020最后一天](https://mp.weixin.qq.com/s/bHcXtxheajtpzPvnPqmHRw) -- 来自公众号：iOS成长之路

[如何持续的自我提升](https://mp.weixin.qq.com/s/ysvDfhF-ckKu2qEZTQSb1A) -- 来自公众号：酷酷的哀殿

[2020 的 cxuan 在掘金 | 掘金年度征文](https://juejin.cn/post/6902212510527520775 "2020 的 cxuan 在掘金 | 掘金年度征文") -- 来自掘金：cxuan

[中年裸辞，我的2020 | 掘金年度征文](https://juejin.cn/post/6901709371294613512 "中年裸辞，我的2020 | 掘金年度征文") -- 来自掘金：Semo

[2020：非适应性完美主义、存在主义哲学、架构、基金翻倍、有效休息｜掘金年度征文](https://juejin.cn/post/6913418068953661448 "2020：非适应性完美主义、存在主义哲学、架构、基金翻倍、有效休息｜掘金年度征文") -- 来自掘金：FeelsChaotic


来自字节跳动技术团队的三篇包体优化文章，涵盖了几乎所有可行且有效的包体优化方案：

[抖音品质建设 - iOS安装包大小优化实践篇](https://juejin.cn/post/6916317500992913421 "抖音品质建设 - iOS安装包大小优化实践篇") -- 来自掘金：字节跳动技术团队

[今日头条iOS安装包大小优化-新阶段、新实践](https://juejin.cn/post/6924107853141655565 "今日头条iOS安装包大小优化-新阶段、新实践") -- 来自掘金：字节跳动技术团队

[今日头条优化实践：iOS包大小二进制优化，一行代码减少60MB下载大小](https://juejin.cn/post/6911121493573402638 "今日头条优化实践：iOS包大小二进制优化，一行代码减少60MB下载大小") -- 来自掘金：字节跳动技术团队



启动优化：

[抖音品质建设 - iOS启动优化《实战篇》](https://juejin.cn/post/6921508850684133390 "抖音品质建设 - iOS启动优化《实战篇》") -- 来自掘金：字节跳动技术团队

[iOS 性能优化：优化App启动速度](https://mp.weixin.qq.com/s/h3vB_zEJBAHCfGmD5EkMcw "iOS 性能优化：优化App启动速度") -- 来自公众号：老司机技术周报



iOS签名及证书的几篇文章：

[iOS证书幕后原理](http://chuquan.me/2020/03/22/ios-certificate-principle/ "iOS证书幕后原理") -- 来自博客：楚权的世界

[iOS App 签名的原理](http://blog.cnbang.net/tech/3386/ "iOS App 签名的原理") -- 来自博客：bang's blog



介绍Swift与OC混编机制的文章：

[从预编译的角度理解Swift与Objective-C及混编机制](https://mp.weixin.qq.com/s/gI9vL1KlHuMzMoWWf2tnIw "从预编译的角度理解Swift与Objective-C及混编机制") -- 来自公众号：美团技术团队





[UIView动画降帧探究](https://mp.weixin.qq.com/s/QVvrgWpjY6mxAqjkrRapPw "UIView动画降帧探究") -- 来自公众号：一瓜技术

[llvm 编译器高级用法：第三方库插桩](https://mp.weixin.qq.com/s/RKg8f6B2jSNuFEImtMnq2Q "llvm 编译器高级用法：第三方库插桩") -- 来自公众号：搜狐技术产品

[你不好奇 Linux 是如何收发网络包的？](https://mp.weixin.qq.com/s/ISQ2qutpJjYOdtM3taeO_A "你不好奇 Linux 是如何收发网络包的？") -- 来自公众号：小林coding

[App 启动提速实践和一些想法](https://mp.weixin.qq.com/s/v2Ym9GPU4J8xCFFNYcpJhg "App 启动提速实践和一些想法") -- 来自公众号：starming

[iOS Forensic Toolkit破解iPhone 5和5c密码](https://mp.weixin.qq.com/s/rFkYFJnIbRf0N-7kBlbzXA "iOS Forensic Toolkit破解iPhone 5和5c密码") -- 来自公众号：iOS进阶宝典

[iOS 性能监控：Runloop 卡顿监控的坑](https://mp.weixin.qq.com/s/vMRQ0VuHLxpaY9oCNd5G8w "iOS 性能监控：Runloop 卡顿监控的坑")  -- 来自公众号：老司机技术周报

[漫画：什么是红黑树？](https://juejin.cn/post/6844903519632228365 "漫画：什么是红黑树？") -- 来自掘金：程序员小灰

[iOS编译速度如何稳定提高10倍以上之一](https://juejin.cn/post/6903407900006449160#heading-19 "iOS编译速度如何稳定提高10倍以上之一") -- 来自掘金：Mr_Coder

[我看技术人的成长路径](https://juejin.cn/post/6906006025925558279 "我看技术人的成长路径") -- 来自掘金：阿里巴巴云原生

[App Store App隐私保护问卷填写指引](https://info.umeng.com/detail?id=398&cateId=1 "App Store App隐私保护问卷填写指引") -- 来自友盟：最新资讯

