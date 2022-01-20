# iOS 摸鱼周报 第四十二期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：
> * Tips：
> * 面试模块：
> * 优秀博客：
> * 学习资料：
> * 开发工具：

## 本期话题

[@zhangferry](https://zhangferry.com)：

## 开发 Tips

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### openssh8.8默认禁用ssh-rsa加密算法导致git验证失效

问题源自于最近无意间在工作机上升级了openssh版本(后续才发现是版本问题), 导致所有基于ssh方式的git操作全部失效;

git pull一直提示请输入密码, 在我输入了无数次个人gitlab密码仍然失败后,第一直觉是我的ssh密钥对出了问题, 重新生成并上传了新的公钥,还是同样的提示;

使用 ssh -vT命令查看了详细的日志信息, 最终发现了问题所在.在解析日志之前, 这里先了解一下简化的ssh密钥登录的原理:

我们都知道ssh是基于非对称加密的一种通信加密协议,常用于做登录校验, 

一般支持两种方式: **口令登录和公钥登录**; 由于篇幅问题这里只介绍公钥的简化流程, 如果想了解探索过程以及git使用ssh的一些技巧,可以查看原文

登录分为两部分:

- 生成会话密钥
  - 客户端和服务端互相发送ssh协议版本以及openssh版本, 并约定协议版本
  - 客户端和服务端互相发送支持的加密算法并约定使用的算法类型
  - 服务端生成非对称密钥,并将公钥以及公钥指纹发送到客户端
  - 客户端和服务端分别使用DH算法计算出会话密钥,后续所有流程都会使用会话密钥加密传输
- 验证阶段
  - 如果是公钥登录, 则会将客户端将公钥指纹信息 使用上述的会话密钥加密发送到服务端
  - 服务端拿到后解密, 并去authorized_keys中匹配对应的公钥, 生成一个随机数,使用该客户端公钥加密后发送到客户端
  - 客户端使用自己的私钥解密,获取到随机数, 使用会话密钥对随机数加密,并做MD5生成摘要发送给服务端
  - 服务器端对原始随机数也使用会话密钥加密后计算MD5, 对比两个值是否相等决定是否登录

> 常说的ssh只是一种抽象的协议标准的, 实际开发中我们使用的是开源openssh库, 该库是对ssh这一抽象协议标准的实现

以上是ssh协议登录校验的流程概要,我们了解到在验证阶段会用到客户端的公钥, openssh会判断公钥生成算法类型, 由于不再支持ssh-rsa, publickey方式失败后会尝试使用口令登录方式, 这也是一直提示我们输入密码的原因;.具体可以通过日志查看:

这里针对日志做了简化, 部分内容做了注释, 你也可以对照自己的log日志查看更详细的过程
```shell
ssh -vT git@github.com

# 日志如下
# 版本信息
OpenSSH_8.8p1, OpenSSL 1.1.1m  14 Dec 2021 
# 读取配置文件
debug1: Reading configuration data /Users/clownfish/.ssh/config
debug1: Reading configuration data /usr/local/etc/ssh/ssh_config
...
# 查找身份文件, 成功返回0, 失败返回-1, 由于本地只有默认的id_ras 所以只有这一项返回0
debug1: identity file /Users/clownfish/.ssh/id_rsa type 0
debug1: identity file /Users/clownfish/.ssh/id_rsa-cert type -1
...

# 版本号
debug1: Local version string SSH-2.0-OpenSSH_8.8
debug1: Remote protocol version 2.0, remote software version OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.8
...
# 查找到host
debug1: Found key in /Users/clownfish/.ssh/known_hosts:5

debug1: Will attempt key: /Users/clownfish/.ssh/id_rsa RSA SHA256:7KTOiN2jUDgc5SJm22GnEk5TpshjTBk/lU9stwJYx48
... # Will attempt key 尝试其他类型密钥

# 认证支持两种方式, 公钥和口令
debug1: Authentications that can continue: publickey,password
debug1: Next authentication method: publickey
debug1: Offering public key: /Users/clownfish/.ssh/id_rsa RSA SHA256:7KTOiN2jUDgc5SJm22GnEk5TpshjTBk/lU9stwJYx48
# 针对上文找到的public key 没有相互支持的签名算法
debug1: send_pubkey_test: no mutual signature algorithm
... # Trying private key 尝试其他私有key
# 尝试口令登录
debug1: Next authentication method: password
... # 一直提示输入密码
```

找到关键字**no mutual signature supported**.去查了一下,发现是**openssh8.8版本问题不再支持ssh-rsa**, 
openssh 8.8 release notes中说明默认会自动转换, 但是链接到版本较低的server时(从日志中可以看到我们server的版本是6.6),还是要手工处理

那么解决办法也就有了,  要么重新生成其他算法的秘钥对上传, 要么修改配置再次开启支持, 这里只针对第二种
在config中做如下配置:
```
Host * # 第一行说明对所有主机生效
  PubkeyAcceptedKeyTypes=+ssh-rsa # 第二行是将ssh-rsa加会允许使用的范围, 没配置会提示no mutual signature supported.表示找不到匹配的签名算法
  # HostKeyAlgorithms +ssh-rsa # 第三行是指定所有主机使用的都是ssh-rsa算法的key, 我个人测试可以不写,如果仍不生效可以打开测试
```
再次测试发现可以正常登录

另外开局提到的,提示输入的密码,其实应该是登录服务器git用户的密码,而不是指的gitlab中的个人账号密码;
因为git使用ssh目的仅仅是登录校验,而不用于访问数据,由于个人对server端了解的较少, 所以在这里也坑了很久, 希望了解的同学多多指教

* [解决Openssh8.8后ssh-rsa算法密钥对校验失效问题](https://juejin.cn/post/7055116684335513631/ "解决Openssh8.8后ssh-rsa算法密钥对校验失效问题")
* [OpenSSH Release Notes](https://www.openssh.com/releasenotes.html "OpenSSH Release Notes")

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

## 优秀博客

整理编辑：[我是熊大](https://juejin.cn/user/1151943916921885)

1、[2021 年终总结](https://onevcat.com/2021/12/2021-final/ "2021 年终总结") -- 来自博客：王巍 (onevcat)

[@我是熊大](https://github.com/Tliens)：王巍，拥有知名开源库Kingfisher，创办了网站[ObjC CN](https://objccn.io/)，是iOS开发者重点关注对象。

2、[大厂逃离后上岸人员的年终总结](https://juejin.cn/post/7047809990916046862 "大厂逃离后上岸人员的年终总结") -- 来自掘金：东方赞

[@我是熊大](https://github.com/Tliens)：工作不卷，生活要开心，收入稳中有升。

3、[下一个五年计划起航 ！](https://halfrost.com/halfrost_2020/ "下一个五年计划起航 ！") -- 来自博客：halfrost

[@我是熊大](https://github.com/Tliens)：霜神是前阿里巴巴资深后端工程师，iOS 开发届的大佬级别人物，这是2020的年终总结，来的更晚一些。

4、[【年度总结】2021年度总结](https://blog.yuusann.com/corpus/article/21021 "【年度总结】2021年度总结") -- 来自博客：郑宇琦

[@我是熊大](https://github.com/Tliens)：郑宇琦，LinkedIn高级研发工程师，曾就职于百度，作者过去一年的经历十分丰富，生活不止有coding。

5、[2020年我阅读了87本书，推荐这12本好书给你](https://mp.weixin.qq.com/s/f6_Sa_C4uU983UBaiMtJdQ "2020年我阅读了87本书，推荐这12本好书给你") -- 来自公众号： 千古壹号

[@我是熊大](https://github.com/Tliens)：作者是京东的一位前端开发，读书爱好者，一年的读书清单有87本之多。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### 摸鱼单词

**地址**：https://apps.apple.com/cn/app/id1488909953?mt=12

**软件状态**：免费

**软件介绍**：

软件作者自述：电脑大部分使用场景是用来办公，如果在办公之余可以背背单词就很好啦，于是就有了摸鱼单词。专注于利用碎片时间学习记忆英语单词。

> 和《摸鱼周报》相得益彰，作者也是一直在维护这个软件。

![摸鱼单词](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/Snipaste_2022-01-18_20-46-39%E7%9A%84%E5%89%AF%E6%9C%AC.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS 成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
