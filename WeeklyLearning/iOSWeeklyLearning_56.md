# iOS 摸鱼周报 #56 | WWDC 进行时

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：WWDC 进行时
> * 面试模块：iOS 中关键字符串该如何混淆加密？
> * 优秀博客：酷炫动画框架推荐
> * 学习资料：Exploring Swift Memory Layout（视频讲座）
> * 开发工具：Mac-CLI 一款面向开发人员的 `macOS` 命令行工具 

## 本期话题

### WWDC 进行时

[@zhangferry](zhangferry.com)：WWDC 进行时持续 5 天的 WWDC22 已经快到尾声了，作为科技圈最负盛名的开发者大会，它不仅吸引到众多 Apple 生态的开发者，还有大半个科技圈在跟进报道，Apple 的影响力可见一斑。WWDC 的意义对于 Apple 来说不只是发布新产品、新功能，它还体现了 Apple 想与开发者之间打造的一种紧密联系。

 为了加强这种联系 ，苹果在 Apple Park 对面建了全新的 Developer Center，以便于开发者和Apple工程师之间交流沟通；为了让 Apple 对开发者的支持范围更广，从去年秋天开始，还推出了各种线上 Tech Talks，除了宣讲各种最新技术，开发者还可以和 Apple 工程师直接交流；Apple 还在全球建立了 17 所 Academy，用于教授相关的开发技术。基于苹果的各种支持和完善的生态，目前全球已有3400 万相关开发者。这众多开发者跟 Apple 的关系又是互相成就的，可以看出 Apple 把生态这个事真是玩的明明白白。 

如果去考究 WWDC 的历史，结果可能会更令人惊讶，首届大会竟然早在 1983 年就举办了。1983 年是什么概念呢，那个时候微软才发布了第一个桌面操作系统 Microsoft Windows，这也是 Windows 这个名字第一次出现的时间。同年晚于 Winddows 三个月苹果发布了第一款搭载图形用户界面的个人电脑 Apple Lisa。乔布斯当年还对此耿耿于怀，图形化界面是苹果的首创却被 Windows 抢先发布。电影[史蒂夫·乔布斯 Steve Jobs](https://movie.douban.com/subject/25850443/ "史蒂夫·乔布斯 Steve Jobs") 就是以这场发布会为开头展开的。

WWDC 发展至今，举办地、演讲者、产品内容、形式都多次变化，但 Apple 还是当年的 Apple，它依然是那个被模仿的存在。这些年间诞生过了很多经典时刻，我找到了一份网友整理的从 2006 年到 2021 年的[Apple 苹果发布会合集](https://www.bilibili.com/video/BV1m4411q75C "Apple 苹果发布会合集")，如果想考考古可以前往观看。 

说到形式的变化 WWDC 因为疫情的原因演讲形式从幻灯片变成视频，感觉这更凸显了 Apple 的设计能力。视频内容相比幻灯片有更大的发挥空间，镜头间流畅的转场切换，贴近视频主题的录制场景，一些三维效果的渲染，以及精良的音效，都让整个视频内容更具趣味性和观赏性。Apple 这几年的片头动画也成了很多设计师争相效仿的对象。

WWDC 被称为 Apple 开发者的「春晚」真的很贴切，WWDC 进行时，大家好好体验剩下的发布会内容吧。

## 面试解析

整理编辑：[JY](https://juejin.cn/user/1574156380931144)

### iOS 中关键字符串该如何混淆加密？

很多开发的同学在项目中遇到`AppKey`以及一些密钥`SecretKey`的时候通常都会定义成宏，方便使用查看，但是这样做，是会有一定的风险，我们来看看有什么风险？

```objectivec
#define kWxAppID @"krystal69d7xxxxxx"  
 - (void)configureForWXSDK {
    [WXApi registerApp:kWxAppID universalLink:@"123123"];
}
```

利用 Hopper 打开 MachO 就可以看到：

![](https://cdn.zhangferry.com/Images/weekly_56_interview_01.jpg)

#### 解决办法

- 在方法中返回这个字符串，示例如下：

    ```objectivec
    #define KRYSTAL_ENCRYPT_KEY @"krystal_key"
    @implementation ViewController
    - (void)viewDidLoad {
        [super viewDidLoad];
        //使用函数代替字符串
        [self uploadDataWithKey:AES_KEY()];  
    }
        
    - (void)uploadDataWithKey:(NSString *)key{
        NSLog(@"%@",key);
    }
        
    static NSString * AES_KEY(){
        unsigned char key[] = {
            'k','r','y','s','t','a','l','_','k','e','y','\0',
        };
        return [NSString stringWithUTF8String:(const char *)key];
    }
    @end
    ```

    这样做能够简单的防护，但是如果逆向以后直接静态分析找到需要返回`key`的函数，也是能够很轻易的破解掉 

- 通过异或的方式（字符串正常会进入常量区，但是通过异或的方式编译器会直接换算成异步结果）

    ```objectivec
    #define STRING_ENCRYPT_KEY @"demo_AES_key"
    #define ENCRYPT_KEY 0xAC
    @interface ViewController ()
    @end
        
    @implementation ViewController
    - (void)viewDidLoad {
        [super viewDidLoad];
    //    [self uploadDataWithKey:STRING_ENCRYPT_KEY]; //使用宏/常量字符串
        [self uploadDataWithKey:AES_KEY()]; //使用函数代替字符串
    }
        
    - (void)uploadDataWithKey:(NSString *)key{
        NSLog(@"%@",key);
    }
        
    static NSString * AES_KEY(){
        unsigned char key[] = {
            (ENCRYPT_KEY ^ 'd'),
            (ENCRYPT_KEY ^ 'e'),
            (ENCRYPT_KEY ^ 'm'),
            (ENCRYPT_KEY ^ 'o'),
            (ENCRYPT_KEY ^ '_'),
            (ENCRYPT_KEY ^ 'A'),
            (ENCRYPT_KEY ^ 'E'),
            (ENCRYPT_KEY ^ 'S'),
            (ENCRYPT_KEY ^ '_'),
            (ENCRYPT_KEY ^ '\0'),
        };
        unsigned char * p = key;
        while (((*p) ^= ENCRYPT_KEY) != '\0') {
            p++;
        }
        return [NSString stringWithUTF8String:(const char *)key];
    }
    @end
    ```

    可以看到 通过`Hopper`打开直接是异或的结果：

    ![](https://cdn.zhangferry.com/Images/weekly_56_interview_02.jpg)

    

## 优秀博客

> 本期优秀博客的主题为：酷炫动画框架推荐。

开发过程中，如果需要比较复杂的动画，一般都是由设计师来处理，前端负责展示。设计师会给我们提供gif、webp、apng等格式的资源，然而因为资源体积或者效果的原因，我们需要一些特殊的实现方式，本期就推荐几个跨平台的酷炫动画框架：Lottie、SVGA、VAP、PAG。

1、[Lottie](https://github.com/airbnb/lottie-ios "Lottie") -- 来自Github：Airbnb

[@我是熊大](https://github.com/Tliens)：Lottie 是Airbnb开源的一套成熟的跨平台动画框架。

优势：

- 1. 因为动画文件通常是 图片+json描述文件，所以我们可以对动画进行解析和调整
- 2. 官方提供了非常多的免费动画，社区是这几个当中比较完善的
- 3. 多端效果能保持一致

缺点: 
- 1. 效果一般，有特效限制
- 2. 文件提交在动画比较复杂时依旧会达到数兆

2、[SVGA](https://svga.io/intro.html "SVGA") -- 来自博客：SVGA

[@我是熊大](https://github.com/Tliens)：SVGA 是一种跨平台的开源动画格式，同时兼容 iOS / Android / Web。SVGA 除了使用简单，性能卓越，同时让动画开发分工明确，各自专注各自的领域，大大减少动画交互的沟通成本，提升开发效率。

3、[VAP](https://github.com/Tencent/vap "VAP") -- 来自Github：VAP

[@我是熊大](https://github.com/Tliens)：VAP是企鹅电竞开发，用于播放特效动画的实现方案。具有高压缩率、硬件解码等优点。同时支持 iOS,Android,Web 平台。

4、[PAG](https://www.jianshu.com/p/94a98c203763 "PAG") -- 来自博客：PAG

[@我是熊大](https://github.com/Tliens)：PAG 是一套完整的动画工作流解决方案。提供从 AE (Adobe After Effects) 导出插件，到桌面预览工具，再到覆盖 iOS，Android，macOS，Windows，Linux 和 Web 等各平台的渲染 SDK。PAG 方案目前已经接入了腾讯系 40 余款应用，包括微信，手机QQ，王者荣耀，腾讯视频，QQ音乐等头部产品。

## 见闻

> 这一周阅读/浏览到的有趣的资讯。

1、[最新研究显示 App Store 助力中国小型开发团队在全球市场斩获成功](https://www.apple.com.cn/newsroom/2022/05/new-research-highlights-global-success-of-small-businesses-and-chinese-entrepreneurs-on-the-app-store/ "最新研究显示 App Store 助力中国小型开发团队在全球市场斩获成功") -- 来自 Apple Newsroom

[@远恒之义](https://github.com/eternaljust)：小型开发团队如何才能在 App Store 上获得成功？来自中国的三个独立开发团队有着不同的答案。

谜底科技的柳毅和梁逸伦夫妇，分工明确，一个掌舵，一个编程，成功推出了 10 款 app，其中包括广受好评的 OffScreen。创新对他们而言，就是坚持将最新的 Apple 技术和开发工具应用到他 app 中，把用户体验做到极致。OffScreen 支持“同播共享”功能，可以和朋友连线进入专注模式；OffScreen 和谜底时钟都支持 iOS 15 的时效性通知，降低实时通知的优先等级，在用户完成专注任务后再显示通知内容。

王维东零基础学习编程，专注的他，自学市场交易和数字货币的知识，开发出了拥有专业性的貔貅记账。貔貅记账是一款完全运用 Swift 和 Apple 原生框架开发的 app，也是 Apple 平台上的独占应用。王维东的目标是只在 Apple 生态 iOS、iPad 和 Apple Watch 上开发貔貅记账，专注做一款 app，且只做一款。

独立游戏制作人陈虹曲，有自己的艺术追求，坚持亲手绘制游戏里每一张场景图、人物和用户界面，他的作品灵感都来源于生活。他的团队善用 Apple 开发工具，使用 SpriteKit 来开发高性能省电的 2D 游戏，常用 TestFlight 邀请用户进行版本测试。

通过 Apple 企业家培训营，谜底科技学会了思考如何将 app 的价值传递到用户手中。王维东和陈虹曲的成功，源于加入了 App Store 小型企业计划，当然，也少不了 App Store 编辑的推广帮助。

2、[Apple 设计大奖获奖者名单公布](https://developer.apple.com/cn/news/?id=9t542fct "Apple 设计大奖获奖者名单公布") -- 来自 Apple News

[@远恒之义](https://github.com/eternaljust)：2022 年是 Apple 设计大奖的第三年，苹果表彰在兼容并蓄、乐趣横生、优越互动、社会影响、视觉图，以及创新思维等六个类别，总共 12 款表现出色的 App 和游戏。中国区有多款应用作品入围提名，一起来了解这些获奖 App 和它们背后极具才华的开发者们吧。

3、[苹果用 M2 芯片，把 Mac 的「护城河」拓宽成「护城海」](https://mp.weixin.qq.com/s/ijFnTppnchoEvgxVnD3fGw) -- 来自公众号：APPSO

[@远恒之义](https://github.com/eternaljust)：随着苹果 M1 芯片的出现，iOS 开发者们再也不抱怨 Xcode 编译又卡又慢，视频博主们剪辑片子也更加丝滑，高性能和长续航的 Mac，大幅度提高了人们的生产力。时隔两年，按照苹果的节奏，M2 芯片的出现意味着「过渡期」已过，Mac 们已经与 x86 架构彻底告别，正式踏入 Arm 架构时代。最新的系统 iPadOS 16 与 macOS Ventura，在搭载 M1 芯片的 iPad Pro 与 iPad Air 上，部分界面和功能开始逐步打通，苹果的「个人电脑」的定义也将会发生改变：通指搭载 M 芯片的设备。

4、[你的手机电池，还撑得住一天吗？他们找到了给电池“延寿”的新方法](https://mp.weixin.qq.com/s/2LxOEqTH090i0JDDAAozoQ) -- 来自公众号：环球科学

[@远恒之义](https://github.com/eternaljust)：你有手机电量焦虑吗？我很早就开启了手机的“优化电池充电”选项，但也架不住时间的推移，电池最大容量的持续降低。上个月，我把用了三年的 iPhone 更换了官方电池，手机瞬间满血复活，又能再战两年（😎）。

> 不知道你现在的手机充一次电能用多久。有科学家也在关注相同的事情——锂离子电池的寿命。不过，他们利用更高精度的成像技术和机器学习方法，“看”到了电池电极颗粒的损伤，并发现了一个特别之处——这些颗粒的群体行为特征也许是设计和制造长寿命电池的关键。

5、[Kindle 笔记导出方法大合集](https://sspai.com/post/73662 "Kindle 笔记导出方法大合集") -- 来自少数派：文猫

[@远恒之义](https://github.com/eternaljust)：2022 年 6 月 2 日下午，亚马逊 Kindle 服务号发表了《重要通知 | Kindle 中国电子书店运营调整》，正式宣布退出中国市场。一代“盖泡面神器” Kindle 即将成为历史。使用 Kindle 看书的你，如何方便快捷地导出 Kindle 上的读书笔记？本文作者提供了官方导出笔记的渠道和几个第三方工具，同时也介绍了如何将 Kindle 读书笔记导入到自己常用的笔记软件。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Exploring Swift Memory Layout

**地址**：https://www.youtube.com/watch?v=ERYNyrfXjlg

一份来自 GOTO Conferences 有关 Swift Memory Layout 的一小时讲座，该讲座深入浅出的讲解了 Swift 中各种例如指针、结构体、类、枚举、数组、协议等我们平时使用的这些工具在内存中是以什么样的形式存在，以及如何解决一些常见问题。对于想了解这部分知识的朋友，这个讲座视频将是一个不错的开胃菜。

![memorylayout](https://cdn.zhangferry.com/Images/memorylayout.png)

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Mac-CLI

**地址**：https://github.com/guarinogabriel/Mac-CLI

**软件状态**：免费

**软件介绍**：

面向开发人员的 `macOS` 命令行工具。

![Mac-CLI](http://cdn.zhangferry.com/demo.gif)


## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #55 | WWDC 码上就位](https://mp.weixin.qq.com/s/zDhnOwOiLGJ_Nwxy5NBePw)

[iOS 摸鱼周报 #54 | Apple 辅助功能持续创新](https://mp.weixin.qq.com/s/6jdqa143Y5yr6lbjCuzlqA)

[iOS 摸鱼周报 #53 | 远程办公正在成为趋势](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

[iOS 摸鱼周报 #52 | 如何规划个人发展](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
