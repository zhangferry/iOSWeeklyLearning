# iOS摸鱼周报 第四十三期

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg)

### 本期概要

> * 话题：dyld4 开源了。
> * Tips：Fix iOS12 libswift_Concurrency.dylib crash bug 
> * 面试模块：Synchronized 源码解读
> * 优秀博客：Swift Protocol 进阶
> * 学习资料：
> * 开发工具：贝尔实验室开发的有向图/无向图自动布局应用，支持 dot 脚本绘制结构图，流程图等。

## 本期话题

[@zhangferry](https://zhangferry.com)：Apple 最近开源了 [dyld4](https://github.com/apple-oss-distributions/dyld/ "dyld4") 的代码。通过阅读它的 Readme 文档，我们可以大致了解到 dyld4 相对 dyld3 做的改进有哪些。dyld3 出于对启动速度的优化，增加了启动闭包。应用首启和发生变化时将一些启动数据创建为闭包存到本地，下次启动将不再重新解析数据，而是直接读取闭包内容。这种方法的理想情况是应用程序和系统应很少发生变化，因为如果这两者经常变化，即意味着闭包可能面临失效。为了应对这类场景，dyld4 采用了 Prebuilt + JustInTime 的双解析模式，Prebuild 对应的就是 dyld3 中的启动闭包场景，JustInTime 大致对应 dyld2 中的实时解析，JustInTime 过程是可以利用 Prebuild 的缓存的，所以性能也还可控。应用首启、包体或系统版本更新、普通启动，dyld4 将根据缓存有效与否选择合适的模式进行解析。所以 dyld4 的设计目标不是更快，而是更灵活。

还有一点，细心的开发者还在 dyld4 源码里发现了 realityOS 及 realityOS_Sim 相关的代码注释。很大可能苹果的 VR/AR 设备已经准备差不多了，静待今年的 WWDC 吧。

## 开发Tips

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Fix iOS12 libswift_Concurrency.dylib crash bug 
最近很多朋友都遇到了 iOS12 上 libswift_Concurrency 的 crash 问题，Xcode 13.2 release notes 中有提到是 Clang 编译器 bug，13.2.1 release notes 说明已经修复，但实际测试并没有。

crash 的具体原因是 Xcode 编译器在低版本  iOS12 上没有将 libswift_Concurrency.dylib 库剔除，反而是将该库嵌入到 ipa 的 Frameworks 路径下，导致动态链接时 libswift_Concurrency 被链接引发 crash。

#### error 分析过程：
1. 通过报错信息 Library not loaded: /usr/lib/swift/libswiftCore.dylib 分析是动态库没有加载，提示是 libswift_Concurrency.dylib 引用了该库，但是 libswift_Concurrency 只有在 iOS15 系统上才会存在， iOS12 本该不链接这个库，猜测是类似 swift 核心库嵌入的方式，内嵌在了 ipa 包中；校验方式也很简单，通过 iOS12 真机 run 一下， 崩溃后通过 `image list` 查看加载的镜像文件会找到 libswift_Concurrency 的路径是 ipa/Frameworks 下的，通过解包 ipa 也证实了这一点。

2. 在按照 xcode 13.2 release notes 提供的方案，将 libswiftCore 设置为 weak 并指定 rpath 后，crash 信息变更，此时 error 原因是 `___chkstk_darwin` 符号找不到；根据 error Referenced from 发现还是 libswift_Concurrency 引用的，通过 `nm -u xxxAppPath/Frameworks/libswift_Concurrency.dylib` 查看所有未定义符号（类型为 U ）， 其中确实包含了 `___chkstk_darwin`，13.2 release notes 中提供的解决方案只是设置了系统库弱引用，没有解决库版本差异导致的符号解析问题。

3. error 提示期望该符号应该在 libSystem.B.dylib 中，但是通过找到 libSystem.B.dylib 并打印导出符号 `nm -gAUj libSystem.B.dylib`  发现即使是高版本的动态库中也并没有该符号，那么如何知道该符号在哪个库呢？这里用了一个取巧的方式，run iOS13 以上真机，并设置 symbol 符号 `___chkstk_darwin`， xcode 会标记所有存在该符号的库，经过第 1 & 2 步骤思考，认为是在查找 libswiftCore 核心库时 crash 的可能性更大。

    > libSystem.B.dylib 路径在 ~/Library/Developer/Xcode/iOS DeviceSupport/xxversion/Symbols/usr/lib/ 目录下

4. 如何校验呢，通过 xcode 上 iOS12 && iOS15 两个不同版本的 libswiftCore.dylib 查看导出符号，可以发现，12 上的 Core 库不存在，对比组 15 上是存在的，所以基本可以断定 symbol not found 是这个原因造成的；当然你也可以把其他几个库也采用相同的方式验证。

> 通过在 ~/Library/Developer/Xcode/iOS DeviceSupport/xxversion/Symbols/usr/lib/swift/libswiftCore.dylib 不同的 version 路径下找到不同系统对应的 libswiftCore.dylib 库，然后用 `nm -gUAj libswiftCore.dylib` 可以获取过滤后的全局符号验证。
> 
> 库的路径，可以通过 linkmap 或者运行 demo 打个断点，通过LLDB的image list查看。

分析总结：无论是根据 xcode 提供的解决方案亦或是 error 分析流程，发现根源还是因为在 iOS12 上链接了 libswift_Concurrency 造成的，既然问题出在异步库，解决方案也很明了，移除项目中的 libswift_Concurrency.dylib 库即可。

#### 解决方案
##### 使用 xcode13.1 或者 xcode13.3 Beta 构建

使用 xcode13.1 或者 xcode13.3 Beta 构建，注意 beta 版构建的 ipa 无法上传到 App Store。
该方法比较麻烦，还要下载 xcode 版本，耗时较多，如果有多版本 xcode 的可以使用该方法。

##### 添加 Post-actions 脚本移除

添加  Post-actions 脚本，每次构建完成后移除嵌入的libswift_Concurrency.dylib。
添加流程： `Edit Scheme... -> Build -> Post-actions -> Click '+' to add New Run Script`, 脚本内容为 `rm "${BUILT_PRODUCTS_DIR}/${FRAMEWORKS_FOLDER_PATH}/libswift_Concurrency.dylib" || echo "libswift_Concurrency.dylib not exists"`

  <img src="https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/weekly_43_tips_04.jpeg" style="zoom:50%;" />

##### 降低或移除使用 libswift_Concurrency.dylib 的三方库

**查找使用 concurrency 的三方库，降低到未引用 libSwiftConcurrency 前的版本，后续等 xcode 修复后再升级**
如果是通过 cocoapods 管理三方库，只需要指定降级版本即可。
但是需要解决一个问题，如何查找三方库中有哪些用到 concurrency 呢？

如果是源码，全局搜索相关的 `await & async` 关键字可以找到部分SDK，但如果是二进制 SDK 或者是间接使用的，则只能通过符号查找。
**查找思路：**

1. 首先明确动态库的链接是依赖导出符号的，即 xxx 库引用了 target_xxx 动态库时，xxx 是通过调用 target_xxx 的导出符号（全局符号）实现的，全局符号的标识是大写的类型，U 表示当前库中未定义的符号，即 xxx 需要链接其他库动态时的符号，符号操作可以使用 `llvm nm` 命令

2. 如何查看是否引用了指定动态库 target_xxx 的符号？可以通过 linkmap 文件查找，但是由于 libswift_Concurrency 有可能是被间接依赖的，此时 linkmap 中不存在对这个库的符号记录，所以没办法进行匹配，换个思路，通过获取 libswift_Concurrency 的所有符号进行匹配，libswift_Concurrency 的路径可以通过上文提到的 `image list` 获取， 一般都是用的 /usr/lib/swift 下的。
3. 遍历所有的库，查找里面用到的未定义符号（ U ）, 和 libswift_Concurrency 的导出符号进行匹配，重合则代表有调用关系。

为了节省校验工作量，提供 `findsymbols.sh` 脚本完成查找，构建前可以通过指定项目中 SDK 目录查找，或者也可以指定构建后 .app 包中的 Frameworks 查找。

**使用方法：**

1. 下载后进行权限授权， `chmod 777 findsymbols.sh`
2. 指定如下参数：
	- -f：指定单个二进制 framework/.a 库进行检查
    - -p：指定目录，检查目录下的所有 framework/.a 二进制 SDK
    - -o： 输出目录，默认是 `~/Desktop/iOS12 Crash Result` 

* [如何检测哪些三方库用了 libstdc++ ](https://www.jianshu.com/p/8de305624dfd?utm_campaign=hugo&utm_medium=reader_share&utm_content=note&utm_source=weixin-friends "如何检测哪些三方库用了 libstdc++ ")
* [After upgrading to Xcode 13.2.1, debugging with a lower version of the iOS device still crashes at launching](https://developer.apple.com/forums/thread/696960 "After upgrading to Xcode 13.2.1, debugging with a lower version of the iOS device still crashes at launching")
* [findsymbols.sh](https://gist.github.com/71f8d3fade74903cae443a3b50c2807f.git "findsymbols.sh")


## 面试解析

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Synchronized 源码解读

**Synchronized** 作为 Apple 提供的同步锁机制中的一种，以其便捷的使用性广为人知，作为面试中经常被考察的知识点，这里通过源码解读一下其实现原理。
为了不陷入层层嵌套的源码逻辑中，我们可以带着几个面试题来解读：

1. `sychronized`  是如何与传入的对象关联上的？
2. 是否会对传入的对象有强引用关系？
3. 如果 `synchronized` 传入 nil 会有什么问题？
4. 当做key的对象在 `synchronized` 内部被释放会有什么问题？
5. `synchronized` 是否是可重入的,即是否可以作为递归锁使用？

#### 查看 synchronized 源码所在

通常查看底层调用有两种方式，通过 `clang` 查看编译后的 cpp 文件梳理，第二种是通过汇编断点梳理调用关系；这里采用第一种方式。
代码示例如下

```
// ViewController.m
- (void)viewDidLoad {
    [super viewDidLoad];
    @synchronized (self)
    {
        int a = 10;
    }
}
```
执行 `xcrun --sdk iphoneos clang -arch arm64 -rewrite-objc -fobjc-arc -fobjc-runtime=ios-14.2 ViewController.m` 获取 ViewController.cpp，找到  `xx_ViewController_viewDidLoad` 相关的函数，简化后代码如下：

```cpp
{
     // 对象 
        id _rethrow = 0;
        id _sync_obj = (id)self;
    // 同步入口
        objc_sync_enter(_sync_obj);
    // 异常捕获
        try
            {
                struct _SYNC_EXIT
                {
                    _SYNC_EXIT(id arg) : sync_exit(arg) {}
                    ~_SYNC_EXIT()
                    {
                        objc_sync_exit(sync_exit);
                    }
                    id sync_exit;
                }
            
            // 初始化_SYNC_EXIT对象持有_sync_obj, 当调用析构函数时执行objc_sync_exit
                _sync_exit(_sync_obj);
            
                // 执行任务
                int a = 10;
            }
    // 这里是异常相关的代码
    }
```

核心代码就是  `objc_sync_enter` 和 `objc_sync_exit` 其他是执行的任务以及异常捕获相关，拿到函数符号后可以通过 xcode 设置 symbol 符号断点获知该函数位于哪个系统库，这里直接说结论是在 libobjc 中，objc是开源的，全局搜索后定位到 objc/objc-sync 的文件中；

由于篇幅太长，这里不引入所有源码解读，概述一下流程以及核心知识点：

#### Synchronized 重要数据结构

核心数据结构有三个，`SyncData` 和 `SyncList` 以及 `sDataLists`；结构体成员变量注释如下：

```
typedef struct alignas(CacheLineSize) SyncData {
    struct SyncData* nextData; // 指向下一个 SyncData 节点，作用类似链表
    DisguisedPtr<objc_object> object; // 绑定的作为 key 的对象
    int32_t threadCount;  // number of THREADS using this block  使用当前 obj 作为 key 的线程数
    recursive_mutex_t mutex; // 递归锁，根据源码继承链其实是 apple 自己封装了os_unfair_lock 实现的递归锁
} SyncData;

// SyncList 作为表中的首节点存在，存储着 SyncData 链表的头结点
struct SyncList {
    SyncData *data; // 指向的 SyncData 对象
    spinlock_t lock; // 操作 SyncList 时防止多线程资源竞争的锁，这里要和 SyncData 中的 mutex 区分开作用，SyncData 中的 mutex 才是实际代码块加锁使用的

    constexpr SyncList() : data(nil), lock(fork_unsafe_lock) { }
};

// Use multiple parallel lists to decrease contention among unrelated objects.
/ 两个宏定义，方便调用
#define LOCK_FOR_OBJ(obj) sDataLists[obj].lock
#define LIST_FOR_OBJ(obj) sDataLists[obj].data /
static StripedMap<SyncList> sDataLists; // 哈希表，以关联的 obj 内存地址作为 key，value是 SyncList 类型
```

> `StripedMap` 本质是个泛型哈希表，是 objc 源码中经常使用的数据结构，例如 retain/release 中的 SideTables 结构等。
>
> 一般以内存地址值作为 key，返回声明类型的 value，iOS中 存储容量是 8 Mac中 容量是 64 ，可以通过源码查看

#### 核心逻辑 id2data()

通过源码可以获知 `objc_sync_enter` 和 `objc_sync_exit` 核心逻辑都是 id2data()，入参为作为 key 的对象，以及枚举值，枚举值的作用是区分是加锁还是解锁逻辑。

id2data 函数使用拉链法解决了哈希冲突问题（更多哈希冲突方案查看 [摸鱼周报39期](https://mp.weixin.qq.com/s/DolkTjL6d-KkvFftd2RLUQ) ），这里使用的是 `SyncData` 链表结构。在查找缓存上支持了 **TLS 快速缓存** 以及 **SyncCache**  二级缓存和 `SyncDataLists` 全局查找三种方式：

- TLS快速缓存只记录首次节点填充，使用 `fastCacheOccupied` 作为状态标识。

- 如果没命中，则继续查找二级缓存 `SyncCache`,  调用链为 `fetch_cache -> _objc_fetch_pthread_data ->tls_get` 实际上仍然是通过线程 tls 私有数据存储的，该缓存存储了**所有属于当前线程**的 `SyncData` 对象。

- `SyncDataLists` 则是全局表，**记录的是所有线程**使用的 `SyncData` 节点。

**代码流程如下：**

- 通过关联的对象地址获取 `SyncList` 中存储的的 `SyncData` 和 lock 锁对象；
- 使用 fastCacheOccupied 标识，用来记录是否已经填充过快速缓存。
    - 首先判断是否命中 TLS 快速缓存，对应代码 `SyncData *data = (SyncData *)tls_get_direct(SYNC_DATA_DIRECT_KEY);`
    - 未命中则判断是否命中二级缓存 `SyncCache`,  对应代码 `SyncCache *cache = fetch_cache(NO);`
    - 命中逻辑处理类似，都是使用 switch 根据入参决定处理加锁还是解锁，如果匹配到，则使用 `result` 指针记录
        - 加锁，则将 lockCount ++, 记录 key object 对应的 `SyncData` 变量 lock 的加锁次数，再次存储回对应的缓存。
        - 解锁，同样 lockCount--, 如果 ==0，表示当前线程中 object 关联的锁不再使用了，对应缓存中 `SyncData` 的 threadCount 减1，当前线程中 object 作为 key 的加锁代码块完全释放
    
- 如果两个缓存都没有命中，则会遍历全局表 `SyncDataLists`,  此时为了防止多线程影响查询，使用了  `SyncList`  结构中的 lock 加锁（注意区分和SyncData中lock的作用）。

     查找到则说明存在一个 `SyncData` 对象供其他线程在使用，当前线程使用需要设置 threadCount + 1 表示新增一个线程，然后存储到上文的缓存中；对应的代码块为：

     ```cpp
     for (p = *listp; p != NULL; p = p->nextData) {goto done}
     ```

- 如果以上查找都未找到，则会生成一个 SyncData 节点, 并通过 `done` 代码段填充到缓存中。

    - 如果存在未释放的 `SyncData`, 同时 `theadCount == 0` 则直接填充新的数据，减少创建对象，实现性能优化，对应代码：

        ```cpp
        if ( firstUnused != NULL ) {//...}
        ```

    - 如果不存在，则新建 `SyncData` 对象，**并采用头插法**插入到链表的头部，对应代码逻辑

        ```cpp
        posix_memalign((void **)&result, alignof(SyncData), sizeof(SyncData));
        //....
        ```
        

最终的存储数据结构如下图所示：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/weekly_43_interview_02.png)

当 id2data() 返回了 `SyncData` 对象后，`objc_sync_try_enter` 会调用 `data->mutex.tryLock(); `尝试加锁，其他线程再次执行时如果判断已经加锁，则进行资源等待

以上是对源码的解读，需要对照着 `libobjc` 源码阅读会更好的理解。下面回到最初的几个问题：

1. 锁是如何与你传入 `@synchronized` 的对象关联上的

    答： 由 `SyncDataLits` 可知是通过对象地址关联的，所以任何存在内存地址的对象都可以作为 synchronized的key 使用

2. 是否会对关联的对象有强引用

    答：根据 `StripedMap` 里的代码可以没有强引用，只是将内存地址值进行位计算然后作为 key 使用，并没有指针指向传入的对象。

3. 如果 synchronize 传入 nil 会有什么问题

    答：通过 `objc_sync_enter` 源码发现，传入 nil 会调用 `objc_sync_nil`, 而 `BREAKPOINT_FUNCTION` 对该函数的定义为 `asm()""` 即空汇编指令。不执行加锁，所以该代码块并不是线程安全的。

4. 假如你传入 `@synchronized` 的对象在 `@synchronized` 的 block 里面被释放或者被赋值为 `nil` 将会怎么样

    答：通过 `objc_sync_exit` 发现被释放后，不会做任何事，导致锁也没有被释放，即一直处于锁定状态，但是由于对象置为nil，导致其他异步线程执行 `objc_sync_enter` 时传入的为 nil，代码块不再线程安全。

5. `synchronized` 是否是可重入的，即是否为递归锁 

    答：是可递归的，因为 `SyncData` 内部是对 os_unfair_recursive_lock 的封装，os_unfair_recursive_lock 结构通过 os_unfair_lock 和 count 实现了可递归的功能，另外通过lockCount记录了重入次数
    
> 需要记住的知识点包括存储数据结构以及如何解决哈希冲突，缓存查找方式等细节


#### synchronized 使用注意事项

因为 `synchronize` 也一种锁，所以在使用上也需要注意死锁以及性能问题，例如：

1. 尽量少或不使用 `self` 作为 key，避免外部在无意中造成死锁的可能，例如代码：

```Object-c
    //class A
    @synchronized (self) {
        [_sharedLock lock];
        NSLog(@"code in class A");
        [_sharedLock unlock];
    }
    
    //class B
    [_sharedLock lock];
    @synchronized (objectA) {
        NSLog(@"code in class B");
    }
    [_sharedLock unlock];
```

2. 精准的粒度控制

    通过源码可以看到, synchronized 相比其他锁只是多了查找过程，性能效率不会过低，之所以慢是更多的因为没有做好粒度控制，例如以下代码：

```OC
@synchronized (sharedToken) {
    [arrA addObject:obj];
}

@synchronized (sharedToken) {
    [arrB addObject:obj];
}
```

应该使用不同的对象作为key, 区分不同的加锁代码块

* [关于 @synchronized，这儿比你想知道的还要多-杨萧玉](https://link.juejin.cn/?target=http%3A%2F%2Fyulingtianxia.com%2Fblog%2F2015%2F11%2F01%2FMore-than-you-want-to-know-about-synchronized%2F "关于 @synchronized，这儿比你想知道的还要多-杨萧玉")
* [正确使用多线程同步锁@synchronized()](https://link.juejin.cn/?target=https%3A%2F%2Fwww.jianshu.com%2Fp%2F2dc347464188 "[正确使用多线程同步锁@synchronized()")
* [iOS摸鱼周报 第三十九期](https://mp.weixin.qq.com/s/DolkTjL6d-KkvFftd2RLUQ "iOS摸鱼周报 第三十九期")


## 优秀博客

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[在已实现协议要求方法的类型中如何调用协议中的默认实现](https://holyswift.app/conforming-to-a-protocol-and-using-default-function-implementation-at-the-same-time-in-swift "在已实现协议要求方法的类型中如何调用协议中的默认实现") -- 来自：Leonardo Maia Pugliese

[@东坡肘子](https://www.fatbobman.com/)：能够提供默认实现是 Swift 协议功能的重要特性。本文介绍了在已实现协议要求方法的类型中继续调用协议的默认实现的三种方式。解决的思路可以给读者不小的启发。在每篇博文中附带介绍一副绘画作品也是该博客的特色之一。

2、[通过 Swift 代码介绍 24 种设计模式](https://oldbird.run/design-patterns/ "通过 Swift 代码介绍 24 种设计模式") -- 来自：oldbird

[@东坡肘子](https://www.fatbobman.com/)：设计模式是程序员必备的基础知识，但是没有点年份，掌握也不是这么容易，所以例子就非常重要。概念是抽象的，例子是具象的。具象的东西，记忆和理解都会容易些。该项目提供了 24 种设计模式的 Swift 实现范例，对于想学习设计模式并加深理解的朋友十分有帮助。

3、[Combining protocols in Swift](https://www.swiftbysundell.com/articles/combining-protocols-in-swift/ "Combining protocols in Swift") -- 来自：Sundell

[@东坡肘子](https://www.fatbobman.com/)：组合和扩展均为 Swift 协议的核心优势。本文介绍了如何为组合后的协议添加具有约束的扩展。几种方式各有利弊，充分掌握后可以更好地理解和发挥 Swift 面向协议编程的优势。

4、[Swift Protocol 背后的故事](https://zxfcumtcs.github.io/2022/02/01/SwiftProtocol1/ "Swift Protocol 背后的故事") -- 来自： 赵雪峰

[@东坡肘子](https://www.fatbobman.com/)：本文共分两篇。上篇中，以一个 Protocol 相关的编译错误为引，通过实例对 Type Erasure、Opaque Types 、Generics 以及 Phantom Types 做了较详细的讨论。下篇则主要讨论 Swift Protocol 实现机制，涉及 Type Metadata、Protocol 内存模型 Existential Container、Generics 的实现原理以及泛型特化等内容。

5、[不透明类型](https://blog.mzying.com/index.php/archives/307/ "不透明类型") -- 来自：Mzying

[@东坡肘子](https://www.fatbobman.com/)：不透明类型是指我们被告知对象的功能而不知道对象具体是什么类型。作者通过三个篇章详细介绍了 Swift 的不透明类型功能，包括：不透明类型解决的问题（上）、返回不透明类型（中）、不透明类型和协议类型之间的区别 （下）。

## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 南大软件分析课程

**地址**：https://www.bilibili.com/video/BV1b7411K7P4

南京大学《软件分析》课程系列，非常难得的高质量课程，可以通过[这里](https://pascal-group.bitbucket.io/teaching.html)获取所有课程的课件。

### iOS 开发学习图谱

**地址**：http://hdjc8.com/iOSRoadMap/

一份特别丰富的 iOS 开发学习图谱，其中包含了许多 iOS 开发的资源，编者认为这本图谱不适合作为学习的一个路线，适合作为一份让你了解 iOS 有哪些知识点的图谱，其中的许多的知识点很适合作为查漏补缺的一个工具。在我们做工作中常常会仅做某些领域内的工作，导致在不短的一段时间内接触的技术是比较窄的，假如你突然想了解一些别的知识点，你可以来这本图谱中闲逛一下，看看有什么知识点是你感兴趣的，也许有一些是你以前感兴趣但是由于种种原因没来及了解的内容！

## 工具推荐

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Graphviz

**地址**：http://www.graphviz.org/

**软件状态**：免费

**软件介绍**：

贝尔实验室开发的有向图/无向图自动布局应用，支持 dot 脚本绘制结构图，流程图等。

![Graphviz](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220217174238.png)

对产物`.gz`文件进行解析查看的途径。

- 在线网站：[GraphvizOnline](http://dreampuf.github.io/GraphvizOnline)
- vs 插件：`Graphviz (dot) language support for Visual Studio Code`


结合`cocoapods-dependencies`插件，我们可以解析`podfile`文件来分析项目的`pod`库依赖，生成`.gz`文件。

* 生成`.gz`文件：`pod dependencies --graphviz`
* 生成依赖图：`pod dependencies --image`
* 生成`.gz`文件及依赖图：`pod dependencies --graphviz --image`

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第四十二期](https://mp.weixin.qq.com/s/ybANWeLNHPOTkr5_alha9g)

[iOS摸鱼周报 第四十一期](https://mp.weixin.qq.com/s/DNXrfZgx0JaXyvfVZ4sYVA)

[iOS摸鱼周报 第四十期](https://mp.weixin.qq.com/s/y4229I_l8aLILR7WA7y01Q)

[iOS摸鱼周报 第三十九期](https://mp.weixin.qq.com/s/DolkTjL6d-KkvFftd2RLUQ)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
