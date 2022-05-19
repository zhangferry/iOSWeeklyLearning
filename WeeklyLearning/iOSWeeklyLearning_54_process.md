iOS 摸鱼周报 52 | 如何规划个人发展

![](http://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：Apple 在辅助功能上继续创新；IAP 自动续订提价通知更新
> * 面试模块：学习 OOMDetector 中的 CRC64 应用实践
> * 优秀博客：
> * 学习资料：一份英语进阶指南
> * 开发工具：

## 本期话题

### [Apple 在辅助功能上的又一创新](https://www.apple.com/newsroom/2022/05/apple-previews-innovative-accessibility-features/ "Apple 在辅助功能上的又一创新")

![](http://cdn.zhangferry.com/Images/20220519094126.png)

[@zhangferry](zhangferry.com)：作为一款受众非常广的产品，针对特殊人群的辅助功能就显得尤为重要，不得不说 Apple 对辅助功能的重视程度和探索精神都是值得尊敬的。最近 Apple 又公布了一些基于软硬件和机器学习带来的辅助功能提升。

针对盲人和视力障碍的人群：Apple 基于配有 LiDAR 的设备可以探测到前方是否有门，门距离自己有多远，甚至要通过推还是拉的方式开门都能识别出来。

针对行动不便的人群：有一项 iPhone 结合 Apple Watch 的功能，借助于 Apple Watch 的 Mirroring 功能，可以用手机远程操作 Apple Watch。同时 Apple Watch 也有提升，通过 AssistiveTouch 技术，可以让 Apple Watch 识别特定手势，像是手指两次捏合的手势可以用于接电话、拍照、暂定音乐等。

针对听力障碍的人群：在 iPhone、iPad、Mac 配备了实时字幕功能，不只是针对 Facetime，对于任意音频内容，包括外部 App 都可以使用。样式是在设备顶部展示一个文本转义框，字体大小还可调整。

同时 VoiceOver 也进一步完善，增加了 20 多个地区语言的支持。

### [IAP 自动续订提价通知更新](https://developer.apple.com/news/?id=tpgp89cl "IAP 自动续订提价通知更新")

[@zhangferry](zhangferry.com)：自动续订是 Apple Store 付费产品使用最广泛的一个订阅选项。当一个已经被用户续订的产品进行提价时，Apple 会通过邮件、推送和 App 内消息的形式告知用户，如果用户未选择接受变更价格，下个续订周期就会默认中断。这可能会导致部分用户的不理解，影响其体验。该项改进意在增加一些条件，使得提价之后的续订周期可以默认延续。这个条件是：每年提价不超过一次，同时订阅价格上调不超过 5 美元和 50%，或者年度订阅价格上调不超过 50 美元和 50%，并且是在法律允许的范围内。该举措仍会通知到用户价格的变更。

## 面试解析

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### 学习 OOMDetector 中的 CRC64 应用实践

以  `OOMDetector` 中对 CRC64 的应用讲解实际应用时的一些变体操作。示例代码如下:

```cpp
#define POLY64REV     0x95AC9329AC4BC9B5ULL
static uint64_t crc_table[8][256];

void init_crc_table_for_oom(void) {
    uint64_t c;
        int n, k;
        static int first = 1;
        if(first){
            first = 0;
            // 针对单个字节值生成单表
            for (n = 0; n < 256; n++)
            {
                c = (uint64_t)n;
                for (k = 0; k < 8; k++)
                {
                    // LSB 右移生成逻辑， 主要适用于小端模式
                    if (c & 1)
                        c = (c >> 1) ^ POLY64REV;
                    else
                        c >>= 1;
                }
                crc_table[0][n] = c;
            }
            
            // 生成不同权重的 CRC 值
            for (n = 0; n < 256; n++) {
                c = crc_table[0][n];
                for (k = 1; k < 8; k++) {
                    c = crc_table[0][c & 0xff] ^ (c >> 8);
                    crc_table[k][n] = c;
                }
            }
        }
    }
    
    uint64_t rapid_crc64(uint64_t crc, const char *buf, uint64_t len)
    {
        register uint64_t *buf64 = (uint64_t *)buf;
        register uint64_t c = crc;
        register uint64_t length = len;
        // 取反
        c = ~c;
        while (length >= 8) {
            c ^= *buf64++;
            // 根据不同权重的字节数据查表
            c = crc_table[0][c & 0xff] ^ crc_table[1][(c >> 8) & 0xff] ^ \
                crc_table[2][(c >> 16) & 0xff] ^ crc_table[3][(c >> 24) & 0xff] ^\
                crc_table[4][(c >> 32) & 0xff] ^ crc_table[5][(c >> 40) & 0xff] ^\
            crc_table[6][(c >> 48) & 0xff] ^ crc_table[7][(c >> 56) & 0xff];
            length -= 8;
        }
        
        // 这里注释的内容，是单字节计算的逻辑，即每次计算一个字节，可能最早的 OOMDetector 采用的是该计算方式。
//        buf = (char *)buf64;
//        while (length > 0) {
//            crc = (crc >> 8) ^ crc_table[0][(crc & 0xff) ^ *buf++];
//            length--;
//        }
        
        // 取反
        c = ~c;
        return c;
    }
```

主要有两步操作，CRC 生成表以及 CRC 查表。以这两步出发学习一下 CRC 实际应用中的变体以及目的。

#### 生成表-多表级联

有别于《#53 周报》中的单表查询方式，`OOMDetector`将 `crc_table`定义为`crc_table[8][256]`二维矩阵的多表查询。其中单维度的表仍然以字节大小（8 bit）作为位宽生成，即单个表大小为 `2 ^ 8 = 256`，`crc_table[8]`表示不同权重的单表， 这种方式称为 CRC 位域多表查询 。

**CRC 位域多表查表方法与传统的 CRC 查表方法最大的不同在于多表级联压缩表格空间。**

如果是传统单表查询，一次性查询双字节数据的 CRC，需要单表大小为 `256 * 256`，采用多表级联只需要 `2 *256`，实现了极大的空间压缩。

更详细的原理可以参考《CRC位域多表查表方法》，这里只理解该优化依赖的核心性质：`crc_table[A ^ B] = crc_table[A] ^ crc_table[B]`。

从 CRC 计算的本质出发，其实就是依次的计算每一 bit 位的余数，而余数的结果值，只和 `POLY`计算的次数和顺序有关。

我们以示例 `0xBC`来拆解这个计算过程:

1. 采用右移的计算方式，左移和右移的区别在下小结中讲解。`1011 1010（0xBA`） 计算 CRC Table 简化为：`1011 1010 ^ (poly ^ 0>>1 ^ poly>>2 ^ poly>>3 ^ poly>>4 ^ 0>>5 ^ poly>>6 ^ 0>>7)`
2. 现在 `0xBA` 根据异或性质分解为 `0xB0 ^ 0x0A`。
3. 我们单独计算 `0xB0` 和 `0x0A`的 CRC 值，来看他们的计算过程
    - `0xB0 = 0b 1011 0000` ，所以 `CRC[0xB0] = 1011 0000 ^ (poly ^ 0>>1 ^ poly>>2 ^ poly>>3 ^ 0>>4 ^ 0>>5 ^ 0>>6 ^ 0>>7)`
    - `0x0A = 0b 0000 1010`，同理 `CRC[0x0A] =  0000 1010 ^ (0 ^ 0>>1 ^ 0>>2 ^ 0>>3 ^ poly>>4 ^ 0>>5 ^ poly>>6 ^ 0>>7)`
4. 上面两个公式做异或， `CRC[0xB0] ^ CRC[0x0A] = 1011 0000 ^ (poly ^ 0>>1 ^ poly>>2 ^ poly>>3 ^ 0>>4 ^ 0>>5 ^ 0>>6 ^ 0>>7) ^ 0000 1010 ^ (0 ^ 0>>1 ^ 0>>2 ^ 0>>3 ^ poly>>4 ^ 0>>5 ^ poly>>6 ^ 0>>7)`由于 0 异或任何值还是原值，结果可以简化为 `1011 0000 ^ 0000 1010 ^ (poly ^ 0>>1 ^ poly>>2 ^ poly>>3 ^ poly>>4 ^ 0>>5 ^ poly>>6 ^ 0>>7)`。这个值和 `CRC[0xBA]`相等。
5. 即证明 CRC 性质：`crc_table[A ^ B] = crc_table[A] ^ crc_table[B]`成立。

CRC 级联查表另一个需要解决的就是多字节数据的权重问题，上面已经 CRC 性质可行性，但是在查表时为了方便，使用的索引并非是直接拆解的数据，例如 `CRC[0x AA BB] = CRC[0x AA 00] ^ CRC[0xBB]` ，两次查表索引分别为 `0xBB 和0xAA`，并非是 `0xBB 和 0xAA 00`。

权重就是指的由 `CRC[0xAA]` 计算 `CRC[0xAA 00] ... CRC[0xAA 00 00 00 00 00 00 00]` 等数据，实现也很简答，可以看做已知单表crc_table[256]的值，求数据的值，即 `init_crc_table_for_oom()`中第二个 `for` 的目的。

#### 生成表-单表反向计算（reversed）

`OOMDetector` 生成单表时区别于传统的 MSB 左移(<<) 计算方式，采用的是 LSB 右移(>>) 生成方式。原因是 iOS 的主机字节序是小端模式，但是一般规范中要求数据在网络传输过程中采用网络字节序（大端模式）。

> 一个系统中针对每一个字节内的 bit 位也是有顺序的，称为位序。

位序一般和主机字节序是一致的，例如一个数据 `0x11 22` 在 iOS 内存中的存储为 `0x22 0x11 `，实际 `0x11 = 0b 0001 0001`的存储顺序也是逆序的，表示为 `0b 1000 1000`。

为了按照网络字节序传输规范作为计算 CRC 顺序的依据，小端的机器上在使用 CRC 时都采用右移计算，即 `0b 1000 1000`按照右移顺序一次计算 `0 0 0 1 0 0 0 1`，这样保证了规范性，无论其他 server 接收端是大端模式还是小端模式，在拿到数据后自己按照主机字节序重新计算即可。

**反向计算最重要的一点：由于计算顺序反向，所以 POLY生成多项式的值相对于传统给定的生成多项式值，也要做位序的反向生成新的 POLY值。**

#### 查表

在 `rapid_crc64()`查表中一次计算了 8 字节数据的 CRC 值，根据`crc_table[A ^ B] = crc_table[A] ^ crc_table[B]`性质，查表操作以对应权重的字节数据在相应的级联表中查找值即可，具体到每一个级联表，和单字节的查表逻辑一致。最终结果是各个权重字节数据的异或结果。

示例计算数据为 `0x AA BB CC DD 11 22 33 44` ，在小端模式是逆序存储的，所以在计算 CRC 值时是从低字节到高字节（即从右到左）顺序计算的。分解计算步骤来分析：

1. 根据异或计算的性质 `0x AA BB CC DD 11 22 33 44 = 0x44 ^ 0x33 00 ^ 0x 22 00 00 ^ 0x11 00 00 00 ... ^ 0xAA 00 00 00 00 00 00 0`
2. 结合 CRC 性质 `CRC[0x AA BB CC DD 11 22 33 44] = CRC[0x44] ^ CRC [0x33 00] ^ .... CRC[0xAA 00 00 00 00 00 00 00]`
3. 根据二维级联表，查找每一个字节的 CRC，`CRC[0x 3300] = crc_table[1][0x33]`。注意这里是用 `0x33`作为索引计算数据 `0x33 00`的值，和计算数据 `0x33` 是有区别的，所以在生成表时需要做二次遍历以生成不同权重的单表值。（这里的权重可以理解为单字节数据在 8 个字节中的位置，从左到右为 MSB => LSB）

`OOMDetector` 在查表之前和查表之后都做了一次取反操作 `c = ~c`，该变体的目的是解决普通 CRC 无法区分只有起始 0 的个数不同的两个数据。（暂时未理解这个目的，所以直接引用 wiki 中的解释）

> 《循環冗餘校驗-wiki》：移位寄存器可以初始化成1而不是0。同样，在用算法处理之前，消息的最初n个数据位要取反。这是因为未经修改的CRC无法区分只有起始0的个数不同的两条消息。而经过这样的取反过程，CRC就可以正确地分辨这些消息了。

- [CRC位域多表查表方法](https://www.eefocus.com/HotPower/blog/12-09/285545_d6429.html/ "CRC位域多表查表方法")

- [循環冗餘校驗-wiki](https://zh.wikipedia.org/wiki/%E5%BE%AA%E7%92%B0%E5%86%97%E9%A4%98%E6%A0%A1%E9%A9%97 "循環冗餘校驗-wiki")

## 优秀博客



## 见闻

> 这一周阅读/浏览到的有趣的资讯。

1、[Mac 与游戏无缘，M1 来了也没用](https://mp.weixin.qq.com/s/z10cepyRBFVPql52Ym1m0g) -- 来自公众号：APPSO

[@远恒之义](https://github.com/eternaljust)：提到游戏，具体到 PC 端的游戏，Mac 电脑基本是沾不上边的。传统意义上的 PC 游戏，指的是在 Windows 电脑上玩的游戏，Mac 电脑只是一个生产力工具。我曾下载过战网客户端，在 Mac 上玩暴雪游戏《炉石传说》，但这样原生支持 Mac 平台的厂商并不多。我也用过腾讯 START 云游戏，对网络要求很高，在 MacBook 上玩《英雄联盟》，打团时的延迟尚能接受。最近拿 PS5 手柄在 iPad 上试玩 Arcade 游戏，游戏体验还不错，也能兼容 Mac 平台。那么，为什么 Mac 距离主流游戏市场这么远呢？M1 芯片的到来，能给 Mac 游戏带来新的机遇吗？作者在文中给出了答案。

2、[对 iPod 说再见，我想带你走进无数人的「青春记忆」](https://sspai.com/post/73225 "对 iPod 说再见，我想带你走进无数人的「青春记忆」") -- 来自少数派：宛潼

[@远恒之义](https://github.com/eternaljust)：停产了，售罄了，下架了，拥有 20 年寿命的 iPod，走到了生命的终点。作为一款音乐播放器，iPod 的产品线十分丰富。无论是初代经典 iPod Classic，还是短暂尝试的 iPod mini，还有被用户吐槽最多的 iPod shuffle，多次探索新形态、新功能和新技术的 iPod nano，功能强大的 iPod touch，这些都已成为了历史，让人怀恋。拥有过 iPod 的你，是否也有「爷青结」的感叹呢。就让本文的作者带你一起了解 iPod 相关的彩蛋产品，唤起你的「青春记忆」吧。

3、[Bash tips: Colors and formatting (ANSI/VT100 Control sequences)](https://misc.flogisoft.com/bash/tip_colors_and_formatting "Bash tips: Colors and formatting (ANSI/VT100 Control sequences)")

[@zhangferry](zhangferry.com)：终端常见的输出样式是黑白，但实际上它还可以设置颜色和一些简单的格式，这些样式的配置可以利用 ANSI 转义码。整个过程分为两步，第一，让 Bash 识别转义码，第二步，指定转义码颜色。看一个例子：

```bash
$ echo -e "\e[31mRed Text\e[0m"
```

这个命令输出内容是红色文本的 Red Text，参数含义说明如下：

| Option |                         Description                          |
| :----: | :----------------------------------------------------------: |
|   -e   |                     开启反斜杠的转义功能                     |
|  \e[   | 它是 Bash 识别转义的起始标志符。`\e` 是 ASCII 码中的 ESC，表示控制符，8 进制表示为 `\033`，也是常见用法。`[` 是转义序列开始标记符 |
|  31m   |     由 ANSI 转义码定义，31 表示红色，m 表示颜色取值结束      |
| \e[0m  |         `\e` 含义同上，开始识别 ANSI，0 表示重置设置         |

4、[Airport](https://app.airport.community/ "Airport")

![](http://cdn.zhangferry.com/Images/airport_screenshoot.jpeg)

[@zhangferry](zhangferry.com)：TestFlight 是 Apple 用于提供内测功能的应用，一般我们只是用它测试自己的应用或者已安装应用的升级尝鲜。TestFlight 版本的 App 有这些优点：审核相比 AppStore 要松很多、功能限制少、对于需要内购的产品可以 0 元尝鲜。但是对于外界还有哪些不为人熟知的 TF 版应用我们是不清楚的，Airport 要做的事情就是这个，你可以在这里根据分类和搜索挑选你喜欢的应用参与测试。

5、[大疆无人机模拟飞行](https://start.dji.com/ "大疆无人机模拟飞行")

![](http://cdn.zhangferry.com/Images/20220519114451.png)

[@zhangferry](zhangferry.com)：这是大疆出的无人机模拟飞行体验网站，打开之后等待页面渲染完成就可以在一个虚拟城市里体验操纵无人机的感觉。该模拟还配备了视角切换、拍照、录像等物理机具备的所有几乎所有功能。同时还有物理撞击的模拟，也就是说如果你飞行中撞到了建筑物，无人机也是会坠毁的，第一视角的坠毁效果做的很不错。

## 学习资料

整理编辑：[zhangferry](https://zhangferry.com)

### 英语进阶指南

地址：https://babyyoung.gitbook.io/english-level-up-tips/

![](http://cdn.zhangferry.com/Images/20220518204154.png)

英语是程序员绕不过去的一项技能，虽然我们可能从小学就开始接触英语了，但直到毕业工作，英语能够不成为学习障碍还是一件不容易的事情。这其中的差别很大成分可以归结为学习方法，这份文档就是这样一个注重方法和可操作性的英语学习指南。

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### CotEditor

**地址**：https://coteditor.com/

**软件状态**：免费

**软件介绍**：

适用于 `macOS` 的纯文本编辑器，轻巧、整洁并且功能强大。

![CotEditor](http://cdn.zhangferry.com/screenshot@2x.png)



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #51 | 游戏版号恢复发放](https://mp.weixin.qq.com/s/ogjhELipiVFRaYJkT2NQwA)

[iOS 摸鱼周报 第五十期](https://mp.weixin.qq.com/s/6IS0RlytWxjeRHyh0f2fXA)

[iOS 摸鱼周报 第四十九期](https://mp.weixin.qq.com/s/6GvVh8_CJmsm1dp-CfIRvw)

[iOS摸鱼周报 第四十八期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](http://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
