# iOS 摸鱼周报 #64 | 与 App Store 专家会面交流

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题



## 本周学习

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
