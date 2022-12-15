# iOS 摸鱼周报 #64 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题



## 本周学习

整理编辑：[JY](https://juejin.cn/user/1574156380931144/posts)
#### Xcode 僵尸对象Zombie Objects

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
