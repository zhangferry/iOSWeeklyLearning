## 面试选题

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Synchronized 源码解读

**Synchronized** 作为 Apple 提供的同步锁机制中的一种，以其便捷的使用性广为人知，作为面试中经常被考察的知识点，我们可以带着几个面试题来解读源码：

1. `sychronized`  是如何与传入的对象关联上的？
2. 是否会对传入的对象有强引用关系？
3. 如果 `synchronized` 传入 nil 会有什么问题？
4. 当做key的对象在 `synchronized` 内部被释放会有什么问题？
5. `synchronized` 是否是可重入的,即是否可以作为递归锁使用？

#### 查看 synchronized 源码所在

通常查看底层调用有两种方式，通过 `clang` 查看编译后的 cpp 文件梳理，第二种是通过汇编断点梳理调用关系；这里采用第一种方式。命令为 `xcrun --sdk iphoneos clang -arch arm64 -rewrite-objc -fobjc-arc -fobjc-runtime=ios-14.2 ViewController.m`


核心代码就是  `objc_sync_enter` 和 `objc_sync_exit` ，拿到函数符号后可以通过 Xcode 设置 symbol 符号断点获知该函数位于哪个系统库，这里直接说结论是在 libobjc 中，objc是开源的，全局搜索后定位到 objc/objc-sync 的文件中；

#### Synchronized 中重要的数据结构

核心数据结构有三个，`SyncData` 和 `SyncList` 以及 `sDataLists`；结构体成员变量注释如下：

```c
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

通过源码可以获知 `objc_sync_enter` 和 `objc_sync_exit` 核心逻辑都是 id2data()，入参为作为 key 的对象，以及状态枚举值。

**代码流程如下：**

- 通过关联的对象地址获取 `SyncList` 中存储的的 `SyncData` 和 lock 锁对象；
- 使用 fastCacheOccupied 标识，用来记录是否已经填充过快速缓存。
    - 首先判断是否命中 TLS 快速缓存，对应代码 `SyncData *data = (SyncData *)tls_get_direct(SYNC_DATA_DIRECT_KEY);`
    - 未命中则判断是否命中二级缓存 `SyncCache`,  对应代码 `SyncCache *cache = fetch_cache(NO);`
    - 命中逻辑处理类似，都是使用 switch 根据入参决定处理加锁还是解锁，如果匹配到，则使用 `result` 指针记录
        - 加锁，则将 lockCount ++，记录 key object 对应的 `SyncData` 变量 lock 的加锁次数，再次存储回对应的缓存。
        - 解锁，同样 lockCount--，如果 ==0，表示当前线程中 object 关联的锁不再使用了，对应缓存中 `SyncData` 的 threadCount 减1，当前线程中 object 作为 key 的加锁代码块完全释放
    
- 如果两个缓存都没有命中，则会遍历全局表 `SyncDataLists`,  此时为了防止多线程影响查询，使用了  `SyncList`  结构中的 lock 加锁（注意区分和SyncData中lock的作用）。

     查找到则说明存在一个 `SyncData` 对象供其他线程在使用，当前线程使用需要设置 threadCount + 1 然后存储到上文的缓存中；对应的代码块为：

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

![](https://cdn.zhangferry.com/Images/weekly_43_interview_02.png)

当 id2data() 返回了 `SyncData` 对象后，`objc_sync_try_enter` 会调用 `data->mutex.tryLock(); `尝试加锁，其他线程再次执行时如果判断已经加锁，则进行资源等待

以上是对源码的解读，需要对照着 `libobjc` 源码阅读会更好的理解。下面回到最初的几个问题：

1. 锁是如何与你传入 `@synchronized` 的对象关联上的

    答： 由 `SyncDataLits` 可知是通过对象地址关联的，所以任何存在内存地址的对象都可以作为 synchronized 的 key 使用

2. 是否会对关联的对象有强引用

    答：根据 `StripedMap` 里的代码可以没有强引用，只是将内存地址值进行位计算然后作为 key 使用，并没有指针指向传入的对象。

3. 如果 synchronize 传入 nil 会有什么问题

    答：通过 `objc_sync_enter` 源码发现，传入 nil 会调用 `objc_sync_nil`, 而 `BREAKPOINT_FUNCTION` 对该函数的定义为 `asm()""` 即空汇编指令。不执行加锁，所以该代码块并不是线程安全的。

4. 假如你传入 `@synchronized` 的对象在 `@synchronized` 的 block 里面被释放或者被赋值为 `nil` 将会怎么样

    答：通过 `objc_sync_exit` 发现被释放后，不会做任何事，导致锁也没有被释放，即一直处于锁定状态，但是由于对象置为nil，导致其他异步线程执行 `objc_sync_enter` 时传入的为 nil，代码块不再线程安全。

5. `synchronized` 是否是可重入的，即是否为递归锁 

    答：是可递归的，因为 `SyncData` 内部是对 os_unfair_recursive_lock 的封装，os_unfair_recursive_lock 结构通过 os_unfair_lock 和 count 实现了可递归的功能，另外通过lockCount记录了重入次数
    

**知识点总结：**

- id2data 函数使用拉链法解决了哈希冲突问题（更多哈希冲突方案查看 [摸鱼周报39期](https://mp.weixin.qq.com/s/DolkTjL6d-KkvFftd2RLUQ) ），

- 在查找缓存上支持了 **TLS 快速缓存** 以及 **SyncCache**  二级缓存和 `SyncDataLists` 全局查找三种方式：
- `Sychronized` 使用注意事项，请参考 [正确使用多线程同步锁@synchronized()](https://link.juejin.cn/?target=https%3A%2F%2Fwww.jianshu.com%2Fp%2F2dc347464188 "[正确使用多线程同步锁@synchronized()")

参考：

* [关于 @synchronized，这儿比你想知道的还要多-杨萧玉](https://link.juejin.cn/?target=http%3A%2F%2Fyulingtianxia.com%2Fblog%2F2015%2F11%2F01%2FMore-than-you-want-to-know-about-synchronized%2F "关于 @synchronized，这儿比你想知道的还要多-杨萧玉")
* [正确使用多线程同步锁@synchronized()](https://link.juejin.cn/?target=https%3A%2F%2Fwww.jianshu.com%2Fp%2F2dc347464188 "[正确使用多线程同步锁@synchronized()")

***

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Dealloc 使用注意事项及解析

关于 Dealloc 的相关面试题以及应用， 周报里已经有所提及。例如 [三十八期：dealloc 在哪个线程执行](https://mp.weixin.qq.com/s/a1aOOn1sFh5EaxISz5tAxA) 和 [四十二期：OOM 治理 FBAllocationTracker 实现原理](https://mp.weixin.qq.com/s/ybANWeLNHPOTkr5_alha9g)，可以结合今天的使用注意事项一起学习。

#### 避免在 dealloc 中使用属性访问

在很多资料中，都明确指出，应该尽量避免在 dealloc 中通过属性访问，而是用成员变量替代。

> 在初始化方法和 dealloc 方法中，总是应该直接通过实例变量来读写数据。- 《Effective Objective-C 2.0》第七条
>
> Always use accessor methods. Except in initializer methods and dealloc. -  WWDC 2012 Session 413 - Migrating to Modern Objective-C
>
> The only places you shouldn’t use accessor methods to set an instance variable are in initializer methods and dealloc. - [Practical Memory Management](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/mmPractical.html#//apple_ref/doc/uid/TP40004447-SW4)

除了可以提升访问效率，也可以防止发生 crash。有文章介绍 crash 的原因是：析构过程中，类结构不再完整，当使用 `accessor` 时，实际是向当前实例发送消息，此时可能会存在 crash。

> 笔者对这里也不是很理解，根据 `debug`  分析析构过程实际是优先调用了实例覆写的 `dealloc`  后，才依次处理 `superclass 的 dealloc`、 `cxx_destruct` 、`Associated`、`Weak Reference`、`Side Table`等结构的，最后执行 `free`，所以不应该发生结构破坏导致的 crash，希望有了解的同学指教一下

笔者个人的理解是：Apple 做这种要求的原因是不想让子类影响父类的构造和析构过程。例如以下代码，子类通过覆写了 `Associated`方法， 会影响到父类的 `dealloc` 过程。

```objectivec
@interface HWObject : NSObject
@property(nonatomic) NSString* info;
@end
    
@implementation HWObject
- (void)dealloc {
    self.info = nil;
}
- (void)setInfo:(NSString *)info {
    if (info)
    {
        _info = info;
        NSLog(@"%@",[NSString stringWithString:info]);
    }
}
@end

@interface HWSubObject : HWObject
@property (nonatomic) NSString* debugInfo;
@end

@implementation HWSubObject
- (void)setInfo:(NSString *)info {
    NSLog(@"%@",[NSString stringWithString:self.debugInfo]);
}
- (void)dealloc {
    _debugInfo = nil;
}
- (instancetype)init {
    if (self = [super init]) {
        _debugInfo = @"This is SubClass";
    }
    return self;
}
@end
```

造成 crash 的原因是 `HWSubObject:dealloc()` 中释放了变量 `debugInfo`，然后调用 `HWObject:dealloc()` ，该函数使用 `Associated` 设置 `info` ，由于子类覆写了 `setInfo`，所以执行子类 `setInfo`。该函数内使用了已经被释放的变量 `debugInfo`。**正如上面说的， 子类通过重写 Associated，最终影响到了父类的析构过程。**

#### dealloc 是什么时候释放变量的

其实在 `dealloc` 中无需开发处理成员变量， 当系统调用 `dealloc`时会自动调用析构函数（`.cxx_destruct`）释放变量，参考源码调用链：`[NSObject dealloc] => _objc_rootDealloc => rootDealloc => object_dispose => objc_destructInstance => object_cxxDestruct => object_cxxDestructFromClass `

```cpp
static void object_cxxDestructFromClass(id obj, Class cls)
{
    // 遍历 self & superclass
        // SEL_cxx_destruct 是在 map_images 时在 Sel_init 中赋值的， 其实就是 .cxx_destruct 函数
        dtor = (void(*)(id))
            lookupMethodInClassAndLoadCache(cls, SEL_cxx_destruct);
            // 执行
            (*dtor)(obj);
        }
    }
}
```

沿着 superClass 链通过 `lookupMethodInClassAndLoadCache `去查询 `SEL_cxx_destruct`函数，查找到调用。`SEL_cxx_destruct` 是 `objc` 在初始化调用 `map_images` 时，在 `Sel_init` 中赋值的，值就是 `.cxx_destruct`。

而 `cxx_destruct` 就是用于释放变量的，当类中新增了变量后，会自动插入该函数，这里可以通过 `LLDB watchpoint ` 监听实例的属性值变化， 然后查看堆栈信息验证。

![](https://cdn.zhangferry.com/Images/weekly_44_interview_02.jpg)

#### 避免在 dealloc 中使用 __weak

```objective-c
- (void)dealloc {
    __weak typeof(self) weakSelf = self;
}
```

当在 `dealloc`中使用了 `__weak` 后会直接 crash，报错信息为：`Cannot form weak reference to instance (0x2813c4d90) of class xxx. It is possible that this object was over-released, or is in the process of deallocation.` 报错原因是 `runtime` 在存储弱引用计数过程中判断了当前对象是否正在析构中， 如果正在析构则抛出异常

核心源码如下：

```cpp
id  weak_register_no_lock(weak_table_t *weak_table, id referent_id,   id *referrer_id, WeakRegisterDeallocatingOptions deallocatingOptions) {
    // ... 省略
        if (deallocating) {
            if (deallocatingOptions == CrashIfDeallocating) {
                _objc_fatal("Cannot form weak reference to instance (%p) of " "class %s. It is possible that this object was " "over-released, or is in the process of deallocation.", (void*)referent, object_getClassName((id)referent));
            } 
    // ... 省略
}

```

#### 避免在 dealloc 中使用 GCD

例如一个经常在子线程中使用的类，内部需要使用 `NSTimer` 定时器，定时器由于需要加到 NSRunloop 中，为了简单，这里加到了主线程， 而定时器有一个特殊性：**定时器的释放和创建必须在同一个线程**，所以释放也需要在主线程，示例代码如下（*以上代码仅作为示例代码，并非实际开发使用*）：

```objectivec
- (void)dealloc {
		[self invalidateTimer];
}

- (void)fireTimer {
    __weak typeof(self) weakSelf = self;
    dispatch_async(dispatch_get_main_queue(), ^{
        if (!weakSelf.timer) {
            weakSelf.timer = [NSTimer scheduledTimerWithTimeInterval:1.0 repeats:YES block:^(NSTimer * _Nonnull timer) {
                NSLog(@"TestDeallocModel timer:%p", timer);
            }];
            [[NSRunLoop currentRunLoop] addTimer:weakSelf.timer forMode:NSRunLoopCommonModes];
        }
    });
}

- (void)invalidateTimer {
    dispatch_async(dispatch_get_main_queue(), ^{
        //  crash 位置
        if (self.timer) {
            NSLog(@"TestDeallocModel invalidateTimer:%p model:%p", self->_timer, self);
            [self.timer invalidate];
            self.timer = nil;
        }
    });
}
- (vodi)main {
    dispatch_async(dispatch_get_global_queue(0, 0), ^{
        HWSubObject *obj = [[HWSubObject alloc] init];
        [obj fireTimer];
    });
}
```

代码会在`invalidateTimer::if (self.timer)` 处发生 crash， 报错为 `EXC_BAD_ACCESS`。原因很简单，因为 `dealloc`最终会调用 `free()`释放内存空间，而后 `GCD`再访问到 `self` 时已经是野指针，所以报错。

>  可以使用 `performSelector`代替 `GCD`实现， 确保线程操作先于 dealloc 完成。

总结：面试中对于内存管理和 dealloc 相关的考察应该不会很复杂，建议熟读一次源码，了解 `dealloc` 的调用时机以及整个释放流程，然后理解注意事项，基本可以一次性解决 `dealloc` 的相关面试题。

* [为什么不能在init和dealloc函数中使用accessor方法](https://cloud.tencent.com/developer/article/1143323 "为什么不能在init和dealloc函数中使用accessor方法")
* [ARC下，Dealloc还需要注意什么？](https://gitkong.github.io/2019/10/24/ARC%E4%B8%8B-Dealloc%E8%BF%98%E9%9C%80%E8%A6%81%E6%B3%A8%E6%84%8F%E4%BB%80%E4%B9%88/ "ARC下，Dealloc还需要注意什么？")
* [Practical Memory Management](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/mmPractical.html#//apple_ref/doc/uid/TP40004447-SW4 "Practical Memory Management")


***
整理编辑：[JY](https://juejin.cn/user/1574156380931144)

### Swift 的 weak 是如何实现的？

在 Swift 中，也是拥有 `SideTable` 的，`SideTable` 是针对有需要的对象而创建，系统会为目标对象分配一块新的内存来保存该对象额外的信息。

对象会有一个指向 `SideTable` 的指针，同时 `SideTable` 也有一个指回原对象的指针。在实现上为了不额外多占用内存，目前只有在创建弱引用时，会先把对象的引用计数放到新创建的 `SideTable` 去，再把空出来的空间存放 `SideTable` 的地址，会通过一个标志位来区分对象是否有 `SideTable`。

```Swift 
class JYObject {
    var age :Int = 18
    var name:String = "JY"
}
var t = JYObject()
weak var t2 = t
print("----")
```

我们在`print`处打上断点，查看 t2 对象

```
(lldb) po t2
▿ Optional<JYObject>
  ▿ some : <JYObject: 0x6000001a9710>

(lldb) x/8gx  0x6000001a9710
0x6000001a9710: 0x0000000100491e18 0xc0000c00001f03dc
0x6000001a9720: 0x0000000000000012 0x000000000000594a
0x6000001a9730: 0xe200000000000000 0x0000000000000000
0x6000001a9740: 0x00007efd22b59740 0x000000000000009c
(lldb) 
```

通过查看汇编，定义了一个`weak`变量，编译器自动调用了`swift_weakInit`函数，这个函数是由`WeakReference`调用的。说明`weak`字段在编译器声明的过程当中自动生成了`WeakReference`对象。

```C++
WeakReference *swift::swift_weakInit(WeakReference *ref, HeapObject *value) {
		ref->nativeInit(value);
  	return ref;
}

void nativeInit(HeapObject *object) {
    auto side = object ? object->refCounts.formWeakReference() : nullptr;
    nativeValue.store(WeakReferenceBits(side), std::memory_order_relaxed);
}

template <>
HeapObjectSideTableEntry* RefCounts<InlineRefCountBits>::formWeakReference() {
    // 创建一个 Side Table
  	auto side = allocateSideTable(true);
  	if (side)
      // 增加一个弱引用
    	return side->incrementWeak();
  	else
    	return nullptr;
}
```

我们来看一下`allocateSideTable`方法，是如何创建一个`Side Table`的

```C++
template <>
HeapObjectSideTableEntry* RefCounts<InlineRefCountBits>::allocateSideTable(bool failIfDeiniting) {
  //1.拿到原有的引用计数
  auto oldbits = refCounts.load(SWIFT_MEMORY_ORDER_CONSUME);
  
  // 判断是否有SideTable，
  if (oldbits.hasSideTable()) {
    // Already have a side table. Return it.
    return oldbits.getSideTable();
  } 
  else if (failIfDeiniting && oldbits.getIsDeiniting()) {
    // Already past the start of deinit. Do nothing.
    return nullptr;
  }

  // Preflight passed. Allocate a side table.
  
  // FIXME: custom side table allocator
 
  //2.通过HeapObject创建了一个HeapObjectSideTableEntry实例对象
  HeapObjectSideTableEntry *side = new HeapObjectSideTableEntry(getHeapObject());
 
  //3.将创建的实例对象地址给了InlineRefCountBits，也就是 RefCountBitsT
  auto newbits = InlineRefCountBits(side);
  
  do {
    if (oldbits.hasSideTable()) {
      // Already have a side table. Return it and delete ours.
      // Read before delete to streamline barriers.
      auto result = oldbits.getSideTable();
      delete side;
      return result;
    }
    else if (failIfDeiniting && oldbits.getIsDeiniting()) {
      // Already past the start of deinit. Do nothing.
      return nullptr;
    }
     
    // 将原有的引用计数存储
    side->initRefCounts(oldbits);
     
  } while (!refCounts.compare_exchange_weak(oldbits, newbits,
                                             std::memory_order_release,
                                             std::memory_order_relaxed));
  return side;
}
```

> 总结一下上面所做的事情
>
> 1.拿到原有的引用计数
> 2.通过 HeapObject 创建了一个 HeapObjectSideTableEntry 实例对象
> 3.将创建的实例对象地址给了`InlineRefCountBits`，也就是 RefCountBitsT。

构造完 `Side Table` 以后，对象中的 `RefCountBitsT` 就不是原来的引用计数了，而是一个指向 `Side Table` 的指针，然而由于它们实际都是 `uint64_t`，因此需要一个方法来区分。区分的方法我们可以来看 `InlineRefCountBits` 的构造函数：

```C++
//弱引用
LLVM_ATTRIBUTE_ALWAYS_INLINE
  RefCountBitsT(HeapObjectSideTableEntry* side)
    : bits((reinterpret_cast<BitsType>(side) >> Offsets::SideTableUnusedLowBits)
           | (BitsType(1) << Offsets::UseSlowRCShift)
           | (BitsType(1) << Offsets::SideTableMarkShift))
  {
    assert(refcountIsInline);
  }
```

> 在弱引用方法中把创建出来的地址做了偏移操作然后存放到了内存当中。
>
> `SideTableUnusedLowBits` = 3，所以，在这个过程中，传进来的`side`往右移了 3 位，下面的两个是 62 位和 63 位标记成 1

我们接着来看一下 ` HeapObjectSideTableEntry ` 的结构

```C++
class HeapObjectSideTableEntry {
  // FIXME: does object need to be atomic?
  std::atomic<HeapObject*> object;
  SideTableRefCounts refCounts;

  public:
  HeapObjectSideTableEntry(HeapObject *newObject)
    : object(newObject), refCounts()
  { }
```

我们来尝试还原一下拿到弱引用计数 ：

`0xc0000c00001f03dc`62位和63位清0得到 `HeapObjectSideTableEntry` 实例对象的地址`0xC00001F03DC`

它既然是右移 3 位，那么我左移 3 位把它还原，`HeapObjectSideTableEntry`左移三位 得到`0x10062AFE0`

![](https://cdn.zhangferry.com/Images/20220302155825.png)


- `0x6000001a9710` 就是实例对象的地址
- `0x0000000000000002`就是弱引用计数
  这里弱引用为`2`的原因是因为`SideTableRefCountBits`初始化的时候从`1`开始

`Side Table`的生命周期与对象是分离的，当强引用计数为 0 时，只有 `HeapObject` 被释放了，并没有释放`Side Table`，只有所有的 `weak` 引用者都被释放了或相关变量被置 `nil` 后，`Side Table` 才能得以释放。


***

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### Autorelease 细节速记

本文内容是基于 `Autorelease-818`版本源码来分析的， 如果你还未了解 `Autorelease`的原理，请先按照另一位编辑的文章学习 [AutoreleasePool](https://mp.weixin.qq.com/s/Z3MWUxR2SLtmzFZ3e5WzYQ)。下面会介绍一些源码细节。

#### AutoreleasePool 数据结构

`AutoreleasePool`底层数据结构是基于 `AutoreleasePoolPage`, 本质上是个双向链表， 每一页的大小为 4K,可以在 `usr/include/mach/arm/vm_param.h`文件中查看 `PAGE_MIN_SIZE`的值，

```cpp
#define PAGE_MAX_SHIFT          14
#define PAGE_MAX_SIZE           (1 << PAGE_MAX_SHIFT)

#define PAGE_MIN_SHIFT          12
#define PAGE_MIN_SIZE           (1 << PAGE_MIN_SHIFT)

class AutoreleasePoolPage : private AutoreleasePoolPageData
{
    static size_t const SIZE =
        // `PROTECT_AUTORELEASEPOOL`默认是定义为 0 的，
    #if PROTECT_AUTORELEASEPOOL
            PAGE_MAX_SIZE;  // must be multiple of vm page size 必须是 vm 页面大小的倍数 定义为1<<14 = 4096K,正好是虚拟页大小
    #else
            PAGE_MIN_SIZE;  // size and alignment, power of 2 大小和对齐， 2的指数倍
    #endif
}
```

#### 64 位系统下的存储优化

在最新的 `818`版本代码中，`AutoreleasePoolPage::add()`中对连续添加的相同对象存储方式做了优化，使用 `LRU` 算法结合新的`AutoreleasePoolEntry` 对象来合并存储，简化后核心源码如下：

```cpp
struct AutoreleasePoolPageData
    struct AutoreleasePoolEntry {
            uintptr_t ptr: 48;  // 关联的 autorelease 的对象
            uintptr_t count: 16; // 关联对象 push 的次数
            static const uintptr_t maxCount = 65535; // 2^16 - 1 可以存储的最大次数
        };
	// ...其他变量
}

id *add(id obj)
{
      // .. 准备工作
        for (uintptr_t offset = 0; offset < 4; offset++) {
             AutoreleasePoolEntry *offsetEntry = topEntry - offset;
             if (offsetEntry <= (AutoreleasePoolEntry*)begin() || *(id *)offsetEntry == POOL_BOUNDARY) {
                 break;
             }
             if (offsetEntry->ptr == (uintptr_t)obj && offsetEntry->count < AutoreleasePoolEntry::maxCount) {
                  if (offset > 0) {
                       AutoreleasePoolEntry found = *offsetEntry;
                       // 将offsetEntry + 1中
                       memmove(offsetEntry, offsetEntry + 1, offset * sizeof(*offsetEntry));
                       *topEntry = found;
                  }
                  topEntry->count++;
                  ret = (id *)topEntry;  // need to reset ret
                  goto done;
             }
        // 旧版本依次插入对象的存储方式
}
```

如果使用 `LRU` 算法, 则插入时从 `next`指针向上遍历最近的四个对象， 遍历中如果和当前对象匹配，则 `Entry` 实体记录的 `count`属性加一, 然后通过 `memmove`函数移动内存数据，将匹配的 `Entry`放到距离 `next`指针最近的位置，以实现 `LRU`的特征。如果只是单纯的合并存储，则只匹配 `next`指针相邻的`Entry`，未匹配到则插入

> 是否开启合并和 `LRU`的环境变量为`OBJC_DISABLE_AUTORELEASE_COALESCING` & `OBJC_DISABLE_AUTORELEASE_COALESCING_LRU`
>
> 另外最好一起准备下缓存淘汰算法，因为如果面试中提到了 `LRU`，面试官很可能会延伸到缓存算法实现，比如 `LFU`、`LRU`。

#### 和线程以及 Runloop 的关系

`AutoreleasePool`和线程的直观关系：

1. 数据结构中存储了和线程相关的成员变量 `thread`，

2. 在实现方案中使用了 `TLS`线程相关技术用来存储状态数据。例如 `Hotpage`以及 `EMPTY_POOL_PLACEHOLDER`等状态值。

3. `objc`初始化时调用了 `AutoreleasePoolPage::init()`，该函数内部通过 `pthread_key_init_np`注册了回调函数 `tls_dealloc`,在线程销毁时调用清理 `Autorelease`相关内容。大致流程为：`_pthread_exit` => `_pthread_tsd_cleanup` => `_pthread_tsd_cleanup_new` => `_pthread_tsd_cleanup_key` => `tls_dealloc`。相关源码可以在 `libpthread`中查看。

    ```cpp
    static void tls_dealloc(void *p) 
    {
        if (p == (void*)EMPTY_POOL_PLACEHOLDER) {
            // No objects or pool pages to clean up here.
            return;
        }
        // reinstate TLS value while we work
        setHotPage((AutoreleasePoolPage *)p);
    
        if (AutoreleasePoolPage *page = coldPage()) {
            if (!page->empty()) objc_autoreleasePoolPop(page->begin());  // pop all of the pools
            if (slowpath(DebugMissingPools || DebugPoolAllocation)) {
                // pop() killed the pages already
            } else {
                page->kill();  // free all of the pages
            }
        }
        // clear TLS value so TLS destruction doesn't loop
        setHotPage(nil);
    }
    ```

    由以上流程可知，子线程处理 `Autorelease` 的时机一般有两种：线程销毁时 & 自定义 `pool`作用域退出时

    在主线程中由于开启了 `Runloop`并且主动注册了两个回调，所以在每次 `Runloop`循环时都会去处理默认添加的 `AutoreleasePool`，该详细内容请参考文章  [AutoreleasePool](https://mp.weixin.qq.com/s/Z3MWUxR2SLtmzFZ3e5WzYQ)，这也不做重复复述。

#### Autorelease ARC环境下基于 tls 的返回值优化方案以及失效场景

主要是通过嵌入 `objc_autoreleaseReturnValue` & `objc_retainAutoreleasedReturnValue`两个函数，基于 `tls`存储状态值实现优化。

优化思路概括为：

- `objc_autoreleaseReturnValue` 通过 `__builtin_return_address()`函数可以查找到函数返回后下一条指令的地址，判断是否为 `mov x29, x29`（arm64）进而决定是否进行优化，
- 如果开启优化会设置 `tls`存储` 状态值 1 `并直接返回对象，否则放入自动释放池走普通逻辑
- `objc_retainAutoreleasedReturnValue`调用`acceptOptimizedReturn`校验 `tls`中的值是否为 1，为 1 表示启动优化直接返回对象， 否则走未优化逻辑先 `retain` 再放入 自动释放池

> 优化思路是基于 `tls`以及`__builtin_return_address()`实现的，以是否插入无实际效果的汇编指令 `mov x29, x29`作为优化标识。 另外查看源码时需要注意 `objc_retainAutoreleasedReturnValue`和`objc_retainAutoreleaseReturnValue`的区别

ARC 下函数返回值是否一定会开启优化呢，存在一种情况会破坏系统的优化逻辑，即 `for`或者`while`等场景。示例如下：

```objective-c
- (HWModel *)takeModel {
//    for (HWModel *model in self.models) {}
    HWModel *model = [HWModel new];
    return model;
}
```

如果打开注释代码，会导致返回的 `model`未优化，通过动态调试可以查看原因。

注释 `for`代码后跳转用的 `b`指令，所以 `lr` 寄存器存储的是调用方调用 `takeModel`函数后的指令地址

![](https://cdn.zhangferry.com/Images/weekly_45_interview_02.png)

有 `for` 循环时，跳转到 `objc_autoreleaseReturnValue`的汇编指令是 `bl`。

![](https://cdn.zhangferry.com/Images/weekly_45_interview_01.png)

`bl`表示执行完函数后继续执行后续指令，后续汇编指令目的主要是为了检测是否存在函数调用栈溢出操作，详细解释可以参考[Revisit iOS Autorelease  二](http://satanwoo.github.io/2019/07/07/RevisitAutorelease2/)。这造成我们上面提到的 `__builtin_return_address()`函数获取到的返回值下一条指令地址，并不是优化标识指令 `mov x29 x29`，而是检测代码指令，导致优化未开启。

> 未开启优化的影响是多做一次 `retain`操作和两次 `autorelease`操作， 笔者未测试出五子棋前辈遇到的 `Autorelease` 对象未释放的情况， 可能是后续 apple 已经优化过，如果读者有不同的结果，欢迎指教

总结： 以上是笔者在搜集面试题时关于 `AutoreleasePool`的一些扩展内容，再次强调需要精读[AutoreleasePool](https://mp.weixin.qq.com/s/Z3MWUxR2SLtmzFZ3e5WzYQ)，尤其需要掌握 `ARC` 下手动处理的几种场景。希望各位可以对 `Autorelease`面试题一网打尽。

* [黑幕背后的Autorelease](https://blog.sunnyxx.com/2014/10/15/behind-autorelease/ "黑幕背后的Autorelease")
* [AutoreleasePool](https://mp.weixin.qq.com/s/Z3MWUxR2SLtmzFZ3e5WzYQ "AutoreleasePool")
* [Revisit iOS Autorelease  一](http://satanwoo.github.io/2019/07/02/RevisitAutorelease/?nsukey=jw8uyyU1C%2BzqPgSpg5Kie0F9Bj4HNHiPMBkxPWPBuEs1ZyVoZwklMAJVkv0TeJgILqxLQOH2a0Di8DhFj5abLdtFE3p09pb3az4o9B7IY7rvyZHamZN1OIh5zBQZv1J%2FnHLc6QkiMW%2Fo2PY9fVAeVQN%2FQ5lBojKaT%2FXmKQuCTY5E1MoBK4Ir7Qi6un5pXxvKQutSkFhgEVUn%2FboyV6pdxQ%3D%3D "Revisit iOS Autorelease  一")
* [Revisit iOS Autorelease  二](http://satanwoo.github.io/2019/07/07/RevisitAutorelease2/ "Revisit iOS Autorelease  二")
* [iOS13 一次Crash定位 - 被释放的NSURL.host](https://segmentfault.com/a/1190000020058030 "iOS13 一次Crash定位 - 被释放的NSURL.host")

***

整理编辑：[JY](https://juejin.cn/user/1574156380931144)

### 静态库和动态库的区别

#### 静态库（Static Library）

特点如下：

- 分发文件大

- 静态库默认仅将有用到的类文件 `link` 到 `Mach-O` 中 （以类文件为最小链接单位）

- ipa 包小（为了 App 瘦身，尽量将代码放静态库中）

    - 静态库中某个目标文件的代码没有被任何地方引用，则这个目标文件不会被链接到可执行文件中去（分类代码经常被优化掉，一般都使用 `-Objc` 和 `-all_load` 或者 `-force_load` 来处理静态库分类加载问题）

- App 冷启动速度快
	- 前提是不使用 `动态库拆分` 搭配 `动态库懒加载方案`
	- App 启动流程中有 `rebase` 和 `bind`，多个静态库只需要 `rebase` 和 `bind` 一次

- 存在符号冲突可能
- 共享 `TEXT 段`
	- iOS 9 以前单个 Mach-O 的 TEXT 限制 60M
	- iOS 9 以后单个 Mach-O 的 TEXT 限制 500M
- 不需要额外签名验证  
- 静态库符号的可见性可以在链接期间被修改 
- 文件格式多为 `fat` 格式的静态库文件
- 形式多为 `.a` 与 `.framework`
- 静态库不含 `bitcode` 时，引用静态库的目标部署时就不能包含 `bitcode`   

####  动态库（Dynamic Library）
特点如下：

- 分发文件小

- ipa 包大（前提是不考虑懒加载的情况）
	- 动态库会把整个 `lib` 复制进 `ipa` 中

- App 冷启动速度慢
	- App 启动流程中有 `rebase` 和 `bind`，多个动态库只需要多次 `rebase` 和 `bind`

- 需要设置合适的 `runpath` 

- 需要动态加载

- 需要签名且需要验证签名
	- 会检查 `framework` 的签名，签名中必须包含 `TeamIdentifier`，并且 `framework` 和 host App 的 `TeamIdentifier` 必须一致
	- Xcode 重签名，保证动态库签名一致性

- 需要导出符号

- 重复的 `arch` 结构

- App 与动态库中重复代码可以共存，不会发生符号冲突
	- 因为可执行文件在构建链接阶段，遇到静态库则吸附进来，遇到动态库则打个标记，彼此保持独立性。
	- 对于来自动态库的符号，编译器会打个标记，交给 `dyld` 去加载和链接符号，也就是把链接的过程推迟到了运行时执行。（比如 App 使用的是 3.0 版本 SDK，动态库使用的是 1.0 版本 SDK，能正常运行，但是会有风险）

- 链接后需要包含分发大小

- 冷启动过程中，默认会在 `main` 函数之前加载
	- 默认情况下，过多的动态库会拖慢冷启动速度
	- 如果采用懒加载动态库的形式，能够加快 App 的启动速度，可以使用 `dlopen` 和 `bundle` 懒加载优化

- 文件格式 `Mach-O`（一个没有 `main` 函数的可执行文件）

- 动态库不包含 `bitcode` 时，引用动态库的目标部署时可以包含 `bitcode`

- `CocoaPods` 从 `v0.36.0` 开始，可添加关键字 `use_frameworks!` 编译成类似 `Embedded Framework` 的结构（可以称之为 `umbrella framework`）
	- 缺点：默认把项目的依赖全部改为动态库（可使用 `use_modular_headers!`，也可以在 `podsepc` 添加 `s.static_framework = true` 规避）
	- `CocoaPods` 执行脚本把动态库嵌入到 `.app` 的 `Framework` 目录下（相当于在 `Embedded Binaries` 加入动态库）

***

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### OC 对象如何知道存在关联的弱引用指针

我们都知道在释放对象之前会检查是否存在弱引用指针， 而判断 OC 对象存在弱引用的依据是什么呢？

如果卷过八股文，肯定了解 `isa` 优化过后使用了 `union`存储更多的数据，其中有一个 `bit:weakly_referenced`是和弱引用指针相关的。

在弱引用对象创建成功后，会去设置该位的值为 1。结构如下：

```cpp
#     define ISA_BITFIELD                                                      \
        uintptr_t nonpointer        : 1;                                       \
        uintptr_t has_assoc         : 1;                                       \
        uintptr_t has_cxx_dtor      : 1;                                       \
        uintptr_t shiftcls          : 33; /*MACH_VM_MAX_ADDRESS 0x1000000000*/ \
        uintptr_t magic             : 6;                                       \
        uintptr_t weakly_referenced : 1;                                       \
        uintptr_t unused            : 1;                                       \
        uintptr_t has_sidetable_rc  : 1;                                       \
        uintptr_t extra_rc          : 19
```

但是未优化的 `isa`存储的是类对象的内存地址，不能存储弱引用信息， 那么它关联的弱引用信息应该存储在哪？答案是 **引用计数表**。

在学习内存管理 `release & retain`流程时，发现引用计数表都是通过 `SIDE_TABLE_RC_ONE` 进行增减操作的。并未直接获取到引用计数后进行 `+/- 1`。该掩码定义处还给出了其他的定义：

```cpp
#define SIDE_TABLE_WEAKLY_REFERENCED (1UL<<0)
#define SIDE_TABLE_DEALLOCATING      (1UL<<1)  // MSB-ward of weak bit
#define SIDE_TABLE_RC_ONE            (1UL<<2)  // MSB-ward of deallocating bit
```

从定义大概猜到，引用计数表中获取到的数值，从第三位开始是真正的引用计数。第一位是用来表示是否存在弱引用指针的。第二位表示正在析构中。

我们在 `weak`创建流程中的关键函数 `storeWeak`中可以证实这一点，该函数在操作完弱引用表之后， 会设置对象的相关弱引用标识位，具体函数是`setWeaklyReferenced_nolock `

```c
inline void
objc_object::setWeaklyReferenced_nolock()
{
    isa_t newisa, oldisa = LoadExclusive(&isa.bits);
    do {
        newisa = oldisa;
        // 未优化的 isa
        if (slowpath(!newisa.nonpointer)) {
            ClearExclusive(&isa.bits);
            sidetable_setWeaklyReferenced_nolock();
            return;
        }

        // 优化过的 isa
        if (newisa.weakly_referenced) {
            ClearExclusive(&isa.bits);
            return;
        }
        newisa.weakly_referenced = true;
    } while (slowpath(!StoreExclusive(&isa.bits, &oldisa.bits, newisa.bits)));
}

// 引用技术表中设置标识位
void
objc_object::sidetable_setWeaklyReferenced_nolock()
{
#if SUPPORT_NONPOINTER_ISA
    ASSERT(!isa.nonpointer);
#endif

    SideTable& table = SideTables()[this];

    table.refcnts[this] |= SIDE_TABLE_WEAKLY_REFERENCED;
}
```

`setWeaklyReferenced_nolock `判断如果是优化过的 `isa` 直接设置对应的 `weakly_referenced = 1` 。

如果是非优化的 `isa`，则通过查找引用计数表设置对应的位置为 1。

在对象释放过程中，查找对象关联弱引用的逻辑具体实现在 `objc_object::clearDeallocating()`中，如果判断是优化后 `isa`则调用 `clearDeallocating_slow`查找 `isa.weakly_referenced`；如果是未优化 `isa` 则调用 `objc_object::sidetable_clearDeallocating()`查找，可自行查看。

另外关于 swift 弱引用可以学习 [周报四十五期](https://mp.weixin.qq.com/s/_N98ADlfQCUkxYjmH0SvZw)

***

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### `StripeMap<T>` 模板类

`StripeMap<T>` 是 OC `Runtime` 中定义的一个类，用于引用计数表、`Synchroinzed`、以及属性设置时的 `lock`列表等。**该类可以理解成是一种特殊的 hashmap。**

特殊性体现在：一般的 hashmap key&value 是一一对应的，即使存在哈希冲突，也会通过其他方法解决该冲突，但是`StripeMap`是 key&value 多对一的。

我们去思考下 apple 为什么要将内存管理的表结构设计为 `StripeMap` 类型？先了解下简化后定义：

```cpp
enum { CacheLineSize = 64 };

template<typename T>
class StripedMap {
#if TARGET_OS_IPHONE && !TARGET_OS_SIMULATOR
    enum { StripeCount = 8 };
#else
    enum { StripeCount = 64 };
#endif
    struct PaddedT {
        T value alignas(CacheLineSize); // 对齐
    };

    PaddedT array[StripeCount];
};
```

`StripeMap`存在的意义就是优化高频访问 `<T>`产生的性能瓶颈，尤其是在多线程资源竞争场景下。根据注释主要体现在以下方面

- 对象结构内部维护一个数组，根据设备的不同分成不同的页，移动设备是 8 页，其他是 64 页。
- 它使用对象的地址作为 key，进行哈希运算后获取一个 index，取得对应的 `<T>` value 。映射关系为 `void* -> <T>`
- 做内存对齐，提高cpu 缓存命中率

#### 分离锁优化

`StripeMap` 实质上是对分离锁概念的实现，简单概述下个人对分离锁的理解

我们都知道多线程场景下，如果多个变量都会被多线程访问和修改，最好的办法是针对不同的变量用不同的锁对象来实现资源管理。这样可以避免访问一个变量时，多线程访问其他不相关的变量时被阻塞等待。这其实是对分拆锁的应用。即避免对同一个锁访问等待。

而分离锁则是对上述思路的进一步优化，针对同一个高频访问的对象来说，分段管理可以解决线程之间的资源竞争。拿 `SideTables`举例来说：

将 `SideTables` 表结构分拆为 8 份，每一份维护一个锁对象。这样在高频访问时，在保证线程安全的同时最多可以支持访问所有的 8 页表数据。实现思路是数组 + 哈希函数（将地址指针转换为 index 索引）。 

```cpp
typedef unsigned long uintptr_t;

static unsigned int indexForPointer(const void *p) {
     uintptr_t addr = reinterpret_cast<uintptr_t>(p);
     return ((addr >> 4) ^ (addr >> 9)) % StripeCount;
}
```

将地址指针强制转换为 `uintptr_t` 无符号长整型，`uintptr_t` 定义为 8 字节，保证了指针（8 字节）的全量转换不会溢出。
然后通过位运算以及取模保证 index 落在 StripeCount 索引范围内。

#### CPU Cache Line

在上面优化方式第三条提到，在定义模板类型 `<T>` 时，使用 `CacheLineSize`做了内存对齐。
通常来讲，内存对齐的目的是为了加快 CPU 的访问，这里也不例外，

但是好奇的是 OC 中常见的内存对齐大小一般是对象的 16 字节对齐。而 StripedMap 定义了 64 字节对齐是出于什么考虑。

这里直接给出结论（理论部分不感兴趣的同学可以直接跳过）：**CacheLine 是 CPU Cache 缓存和主内存一次交换数据的大小，不同 CPU 上不同，Mac & iOS 上是 64 字节,这里是为了解决 `Cpu Cache`中的伪共享（False Sharing）问题。**

出于探索心理，搜索了一下关键字。因为笔者对操作系统了解不多，所以只是做一个概述：

1. CPU 和内存之间由于存在巨大的频率差距，影响数据访问速度从而诞生了 `CPU Cache` 的概念，`Cache Line` 是 `CPU Cache`之间数据传输和操作的最小单位。意味着每一次缓存之间的数据交换都是`Cache Line`的倍数。这是前置条件。

2. 另外一个重要的点是不同核心之间 L1 和 L2 缓存是不共享的，其他核心中的线程要访问当前核心缓存中的数据需要发送 `RFO 消息`，当前核心重置命中的的`Cache Line`状态，并经过一次 L1 / L2 => L3/主内存的数据写入，另外一个核心再次读取后才能访问。如果频繁的在两个核心线程中访问。会造成性能损耗。

我们假设一个场景， 两个不相关的变量 `var1` 和 `var2` 小于 64 字节，并且内存中紧邻，这时一个核心加载了包含 `var1 和 var2` 内存区域的`Cache Line` 并更新了 `var1`的值，此时处于另外一个核心需要访问 `var2`就会出现上面第二条的情况。

解决这类问题的思路就是空间换时间。也是 `StripedMap` 的做法。内存对齐，尽量保证不同页的 `SideTable`表结构会在不同的 `Cahce Line`上。这样不同的核心线程就可以做到同时处理两个变量值。

* [Objective-C runtime源码小记-StripedMap](https://juejin.cn/post/6869014441284141063 "Objective-C runtime源码小记-StripedMap")
* [【译】CPU 高速缓存原理和应用](https://segmentfault.com/a/1190000022785358 "【译】CPU 高速缓存原理和应用")


***

整理编辑：[JY](https://juejin.cn/user/1574156380931144)

### 事件响应与传递

#### 当指尖触碰屏幕，触摸事件由触屏生成后如何传递到当前应用？

通过 `IOKit.framework` 事件发生，被封装为 `IOHIDEvent `对象，然后通过 `mach port`  转发到 `SpringBoard`（也就是桌面）。然后再通过`mach port`转发给当前 APP 的主线程，主线程`Runloop`的`Source1`触发,`Source1`回调内部触发`Source0回调`，`Source0`的回调内部将事件封装成`UIEvent` ，然后调用`UIApplication`的`sendEvent`将`UIEvent`传给了`UIWindow`。

>  `souce1`回调方法： `__IOHIDEventSystemClientQueueCallback()`
>
>  `souce0`回调方法:    `__UIApplicationHandleEventQueue()`

寻找最佳响应者，这个过程也就是`hit-testing`，确定了响应链，接下来就是传递事件。

如果事件找不到能够响应的对象，最终会释放掉。`Runloop` 在事件处理完后也会睡眠等待下一次事件。

#### 寻找事件的最佳响应者（Hit-Testing）

当 APP 接受到触摸事件后，会被放入到当前应用的一个事件队列中（先发生先执行），出队后，`Application` 首先将事件传递给当前应用最后显示的`UIWindow`，询问是否能够响应事件，若窗口能够响应事件，则向下传递子视图是否能响应事件，优先询问后添加的视图的子视图，如果视图没有能够响应的子视图了，则自身就是最合适的响应者。

```objectivec
- (UIView *)hitTest:(CGPoint)point withEvent:(UIEvent *)event {
    //3种状态无法响应事件
     if (self.userInteractionEnabled == NO || self.hidden == YES ||  self.alpha <= 0.01) return nil; 
    //触摸点若不在当前视图上则无法响应事件
    if ([self pointInside:point withEvent:event] == NO) return nil; 
    //从后往前遍历子视图数组 
    int count = (int)self.subviews.count; 
    for (int i = count - 1; i >= 0; i--) { 
        // 获取子视图
        UIView *childView = self.subviews[i]; 
        // 坐标系的转换,把触摸点在当前视图上坐标转换为在子视图上的坐标
        CGPoint childP = [self convertPoint:point toView:childView]; 
        //询问子视图层级中的最佳响应视图
        UIView *fitView = [childView hitTest:childP withEvent:event]; 
        if (fitView) {
            //如果子视图中有更合适的就返回
            return fitView; 
        }
    } 
    //没有在子视图中找到更合适的响应视图，那么自身就是最合适的
    return self;
}
```

#### 传递事件

找到最佳响应者后开始传递事件

`UIApplication sendEvent ` =>`UIWindow sendEvent` =>`UIWindow _sendTouchesForEvent` =>`touchesBegin` 

#### UIApplication 是怎么知道要把事件传给哪个 window 的？window 又是怎么知道哪个视图才是最佳响应者的呢？

在`hit-testing`过程中将 `Window`与 `view`绑定在 `UIEvent`上的`touch`对象

#### 响应者为什么能够处理响应事件，提供了哪些方法？

```objectivec
//手指触碰屏幕，触摸开始
- (void)touchesBegan:(NSSet<UITouch *> *)touches withEvent:(nullable UIEvent *)event;
//手指在屏幕上移动
- (void)touchesMoved:(NSSet<UITouch *> *)touches withEvent:(nullable UIEvent *)event;
//手指离开屏幕，触摸结束
- (void)touchesEnded:(NSSet<UITouch *> *)touches withEvent:(nullable UIEvent *)event;
//触摸结束前，某个系统事件中断了触摸，例如电话呼入
- (void)touchesCancelled:(NSSet<UITouch *> *)touches withEvent:(nullable UIEvent *)event;
```

#### 触摸事件如何沿着响应链流动？

在确定最佳响应者之后，优先给最佳的对象响应，如果最佳对象要将事件传递给其他响应者，这个从底到上的过程叫做响应链。

#### 如果有 UIResponder、手势、UIControl 同时存在，是怎么处理的？

系统提供的有默认 `action` 操作的 `UIControl`，例如 `UIButton、UISwitch` 等的单击，响应优先级比手势高，而自定义的却比手势识别器要低，然后才是  `UIResponder` 。

`Window` 在将事件传递给 `hit-tested view` 之前，会先将事件传递给相关的手势识别器,并由手势识别器优先识别。若手势识别器成功识别了事件，就会取消 `hit-tested view`对事件的响应；若手势识别器没能识别事件，`hit-tested view` 才完全接手事件的响应权。

#### Window怎么知道要把事件传递给哪些手势识别器？

`event` 绑定的`touch`对象维护了一个手势数组，在 `hit-testing` 的过程中收集对应的手势识别器， `Window` 先将事件传递给这些手势识别器，再传给 `hit-tested view`。一旦有手势识别器成功识别了手势，`Application` 就会取消`hit-tested view`对事件的响应。

#### 手势识别器与UIResponder对于事件响应的联系？

* `Window`先将绑定了触摸对象的事件传递给触摸对象上绑定的手势识别器，再发送给触摸对象对应的 `hit-tested view`。

* 手势识别器识别手势期间，若触摸对象的触摸状态发生变化，事件都是先发送给手势识别器再发送给 `hit-test view`。

* 手势识别器若成功识别了手势，则通知 `Application` 取消 `hit-tested view` 对于事件的响应，并停止向 `hit-tested view` 发送事件；

* 若手势识别器未能识别手势，而此时触摸并未结束，则停止向手势识别器发送事件，仅向 `hit-test view` 发送事件。

* 若手势识别器未能识别手势，且此时触摸已经结束，则向 `hit-tested view` 发送 `end` 状态的 `touch`事件以停止对事件的响应。

>  **cancelsTouchesInView** 若设置成YES，则表示手势识别器在识别手势期间，截断事件，即不会将事件发送给hit-tested view。
>
>  **delaysTouchesBegan** 若设置成NO，则在手势识别失败时会立即通知Application发送状态为end的touch事件给hit-tested view以调用 `touchesEnded:withEvent:` 结束事件响应。

#### 有哪些情况无法响应？

* **不允许交互**：`userInteractionEnabled = NO`

* **隐藏**（`hidden = YES `）：如果父视图隐藏，那么子视图也会隐藏，隐藏的视图无法接收事件

* **透明度**：alpha < 0.01 如果设置一个视图的透明度<0.01，会直接影响子视图的透明度。alpha：0.0~0.01为透明。

### 参考

[iOS触摸事件全家桶](https://www.jianshu.com/p/c294d1bd963d "iOS触摸事件全家桶")

***

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### mmap 应用

`mmap`是系统提供的一种虚拟内存映射文件的技术。可以将一个文件或者其他对象映射到进程的地址空间，实现文件磁盘地址和进程中虚拟内存地址之间的映射关系。

在 iOS 中经常用在对性能要求较高的场景使用。例如常见的 `APM` 的日志写入，大文件读写操作等。

> `mmap`还有可以用来做共享内存进程通信、匿名内存映射，感兴趣的同学可以自行学习

#### 普通`I/O`流程

普通的读写操作，由于考虑虚拟内存权限安全的问题，所有操作系统级别的行为（例如 `I/O`）都是在内核态处理的。同时  `I/O` 操作为了平衡主存和磁盘之间的读写速度以及保护磁盘写入次数，做了缓存处理，即 `page cache`该缓存是位于内核态主存中的。

内核态空间，用户进程是无法直接访问的，可以间接通过**系统调用**获取并拷贝到用户态空间进行读取。 即一次读操作的简化流程为：

1. 用户进程发起读取数据操作`read()`。

2. `read()`通过系统调用函数调用内核态的函数读取数据

3. 内核态会判断读取内存页是否在 `Page Cache`中，如果命中缓存，则直接拷贝到主存中供用户进程使用

4. 如果未命中，则先从磁盘将数据按照 `Page Size`对齐拷贝到 `Page Cache`中，然后再次执行上面步骤 3

所以一次普通读写，最多需要经历两次数据拷贝，一次是从磁盘映射到 `Page cache`，第二次是`Page Cachef`拷贝到用户进程空间。

以上只是简化后的流程，对文件读写操作感兴趣的可以通过该文章学习[从内核文件系统看文件读写过程 ](https://www.cnblogs.com/huxiao-tee/p/4657851.html "从内核文件系统看文件读写过程")

#### 优缺点

由上可知 `mmap`相比普通的文件读写，优势在于可以有选择的映射，只加载一部分内容到进程虚拟内存中。另一方面，由于 `mmap`是直接映射磁盘文件到虚拟内存，减少了数据交换的次数，所以写入性能也更快。

有利必有弊，mmap 也存一些缺点，例如要求加载的最小单位为 VM Page Size，所以如果是小文件，该方法会导致碎片空间浪费。

#### mmap API 示例

`mmap` 实际应用主要是 `mmap() & munmap()`两个函数实现。两个函数原型如下：

```cpp
/// 需要导入头文件
#import <sys/mman.h>

void* mmap(void* start,size_t length,int prot,int flags,int fd,off_t offset);
 int munmap(void* start,size_t length);
```

函数参数：

- `start`：映射区的起始位置，设置为零表示由系统决定映射区的起始位置
- `length`： 映射区长度，单位是字节， 不足一页内存按一整页处理
- `prot`：期望的内存保护标志，不能与文件打开模式冲突，支持 `|` 取多个值
    - `PROT_EXEC`: 页内容允许执行
    - `PROT_READ`：页内容允许读取
    - `PROT_WRITE`：页内容可以写入
    - `PROT_NONE`：不可访问
- `flags`：指定映射对象的类型，映射选项和映射页是否可以共享（这里只注释使用的两项，其他更多定义可以自行查看）
    - `MAP_SHARED`：与其它所有映射这个文件对象的进程共享映射空间。对共享区的写入，相当于输出到文件。
    - `MAP_FILE`：默认值，表示从文件中映射
- `fd`：有效的文件描述词。一般是由open()函数返回，其值也可以设置为-1，此时需要指定flags参数中的MAP_ANON,表明是匿名映射。
- `off_set`：文件映射的偏移量，通常设置为0，代表从文件最前方开始，对应offset必须是分页大小的整数倍。

`mmap` 回写时机并不是实时的，调用 `msync()`或者`munmap()` 时会从内存中回写到文件，系统异常退出也会进行内容回写，不会导致日志数据丢失，所以特别适合日志文件写入。

> Demo 可以参考开源库 `OOMDetector` 中的 `HighSppedLogger` 类的使用封装，有比较完整的映射、写入、读取、同步的代码封装，可直接使用。

#### 注意事项

`mmap` 允许映射到内存中的大小大于文件的大小，最后一个内存页不被使用的空间将会清零。但是如果映射的虚拟内存过大，超过了文件实际占用的内存页数量，后续访问会抛出异常。

示例可以参考《认真分析mmap：是什么 为什么 怎么用》中的情景二：

![](https://cdn.zhangferry.com/Images/weekly_51_interview.png)

超出文件大小的虚拟内存区域，文件所在页的内存仍可以访问，超出所在页的访问会抛出 `Signal` 信号异常。

#### 参考

- [认真分析mmap：是什么 为什么 怎么用 ](https://www.cnblogs.com/huxiao-tee/p/4660352.html "认真分析 mmap: 是什么 为什么 怎么用")
- [C语言mmap()函数：建立内存映射](http://c.biancheng.net/cpp/html/138.html "C语言mmap()函数：建立内存映射")
- [OOMDetector](https://github.com/Tencent/OOMDetector "OOMDetector")


***

整理编辑：[JY](https://juejin.cn/user/1574156380931144)

### load方法为什么耗时？

我们都知道启动优化的时候，减少`+load`方法能够减少启动时间。

如果`+load` 方法里的内容很简单，会影响启动时间么？比如这样的一个`+load `方法？

```C++
+ (void)load 
{
    printf("123");
}
```

这段代码编译完之后，这个函数会储存在`Mach-O`中的`TEXT`两个段中，`__text`存函数二进制，`cstring`存储字符串 123

要执行`printf`函数，首先需要访问`__text`触发一次`page In` 读入物理内存，为了要打印字符串，还需要访问`cstring`，还会触发一次`page In`

有很多同学不了解`page In`，这里介绍一下，首先先要知道`mmap`

`mmap` 的全称是 `memory map`，是一种内存映射技术，可以把文件映射到虚拟内存的地址空间里，这样就可以像直接操作内存那样来读写文件。

当读取虚拟内存，其对应的文件内容在物理内存中不存在的时候，会触发一个事件：` Page In`，把对应的文件内容读入物理内存中。

`Page In`又做了哪些事情呢？

* MMU找到空闲的物理内存页面
* 触发磁盘IO，把数据读入到物理内存
* 如果是TEXT段的页，要进行解密（iOS13之后不需要解密）
* 对解密后的页，进行签名验证

 为了执行这个函数，系统付出了两个`page In`的代价，所以一旦`load`方法过多，会影响启动速度


***

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### CRC 实践应用：理论推导

`CRC` 全称叫做循环冗余校验（Cyclic Redundancy Check），是一种根据网络数据包或电脑文件等数据产生**简短固定位数校验码**的一种散列函数。常用于网络数据传输中的差错校验，其特征是信息字段和校验字段的长度可以任意选定。

> 类似作用的还有 **奇偶偶校验、累加和校验等**

#### 理论基础一：多项式运算

`CRC`是基于多项式运算实现的，计算机系统中需要传输的数据可以看做是二进制表示的，例如数值42（ 0x2A） = 0b 10 1010。二进制同时也可以改写成多项式格式表示（简化版）：0b 10 1010 = 2^5 + 2^3 + 2^1（这里将系数为 0 的项删除，并省略了每一项的系数 1）。

CRC 算法推到过程，可以参考《循環冗餘校驗-维基百科》简介部分：

1. 将数据转换成多项式格式，记作 M(x) 作为被除数。
2. 和接收方协定一个多项式记作 K(x)，作为除数 。专有名词被称为**生成多项式**
3. 二者做除法。最终可以表示为 `M(x) * x^n = Q(x) * K(x) - R(x)`。**Q(x)**看做是商，**R(x)**看着为余数。**x^n** 表示左移 n 位（等价于数据低位补 n 个零），n 的取值是生成多项式 K(x) 的位数 - 1。例如上面的 0b 10 1010 位数为 6，所以 n = 5。
4. 然后将 M(x) + R(x) 的和作为新的数据传输到接收端，接收端收到后再除以多项式 K(x)，如果余数为零说明数据没有修改，如果余数不为零说明  M(x) 部分有了变动，即数据发生了改变。

> 这里余数为零并不是绝对的表明数据没修改，存在数据改动后校验余数为零的可能，一般被称为误码率。也是衡量差错校验算法的指标之一。

实际编码中，**K(x)** 并不是随意选取的，而是使用一些已经规定的效率更高的多项式的值，根据 **K(x)** 位数不同，校验函数也命名不同，例如常见的 **CRC-8、CRC-16、CRC-32、CRC-64等**。

例如 CRC-16 对应的生成多项式 PLOY 为：（x^16 + x^15 + x^2 + 1），表示为 0b 1 1000 0000 0000 0101 = 0x18005。

#### 理论基础二：模 2 除法

上面讲了多项式格式转换以及作用。那么模 2 除法是做什么的呢？

在第三步中提到两个多项式做除法，实际这里并不是采取普通的除法运算，而是模 2 除法，特点是在进行余数计算时，针对每一位的加减运算皆采用不进位 & 不借位思想。即:

```cpp
0 - 0 = 0;
0 - 1 = 1;
1 - 0 = 1;
1 - 1 = 0;
```

是不是看着很熟悉，对的，其实模 2 除法中的位加减运算本质上是二进制的位异或运算（`xor`）。

#### CRC 直接计算法

基于以上两个理论，我们总结下 `CRC`算法的步骤：

1. 将要传输的数据用二进制形式展开，并选定一个生成多项式 K，K 的二进制长度为 W+1，则位宽为 W 
2. 在要传输的二进制数据后补 W 个 0，并初始化寄存器值为零。 
4. 用二进制展开后的数据以模 2 除法除以k，数据首位是 1 则商 1，为 0 则商零，最终计算得到的余数即为循环冗余校验和

根据上面的算法思想，我们这里通过一个计算实例验证：

![](https://cdn.zhangferry.com/Images/weekly_53_interview_01.png)

上面的计算过程省略了商为 0 的余数计算，转换为程序逻辑代码如下：

```cpp
#define CRC_WIDTH   3
#define CRC_POLY    0x9     // 1001b

// 这里是需要进行校验的数据
int data = 0xB1C;           // 0b 1011 0001 1100 
// 左移补 0 这里 W = 3
data <<= CRC_WIDTH;
// 初始化结果
int crc = 0;
//  依次针对每一 bit 位进行计算 总位数 = 数据位宽 + 多项式位宽
for(int shift_bit = DATA_WIDTH + CRC_WIDTH;  shift_bit >  0;  shift_bit--) {
    // regs << 1 目的是移除当前寄存器中最高位的值，使用剩余的bit 数据做计算，因为无论最高位是零或者 1，最终计算后都是 0，（最高位为 0 则商零 和 0 做异或， 为 1 则商 1 和多项式做异或，多项式最高位为 1 ）
    // (data >> (shift_bit - 1)) & 0x1是为了获取数据中指定位的值，  & 0x1是为了只取最低位的 1 bit ，示例 1011 就是依次取 1、0、1、1
    // 整句的目的是移除寄存器最高位数据，然后用待计算的数据补充
    crc = (crc << 1)  |  ((data >> (shift_bit - 1)) & 0x1);
    // 获取待计算数据的最高 bit 位是 0 还是 1， 如果商为 1 则需要 xor 异或计算，
    if(crc >> CRC_WIDTH & 0x1)    {
        crc = crc ^ CRC_POLY;
    }
}
```

**CRC 直接计算法看上去就像在循环消除被除数的首位数据**，每一轮计算都可以消除最高位 bit 值，得到余数后，继续计算消除首位。直到无法求商时，最终的余数值就是 CRC。

该思路虽然简单，但是如果需要被检验的数据很大时，每一个 bit 位都需要进行移位 & 异或操作，占用系统运算资源且相对速度慢。所以为了优化效率，采用空间换时间的思路。也就是**驱动表法**

#### 进阶一 驱动表法（查表法）

驱动表思路是一次性计算好多位数据的 CRC 值存储在表中，使用时直接用对应位数的数据和表中的 CRC做异或。

由于计算机系统中一般以字节为最小数据单位，所以 CRC 表一般以 8 bit 作为最小生成单位，**该思路利用了异或结合律(A Xor B Xor C = A Xor ( B Xor C ))。**

示例表位宽简化为 4 bit 如下所示：

![](https://cdn.zhangferry.com/Images/weekly_53_interview_03.png)

观察选中内容两种计算顺序，针对0b 1011每一位数据计算余数的结果和先进行除数的多次异或，然后再和数据 0b 1011异或的结果是一致的，驱动表就是这样实现的，提前计算初始化1011的余数值并存入表中，可以实现该值的重复利用，以空间换取后续同样数据的计算时间。

表的生成代码如下(以一字节为例)，8 位二进制可以表示的数据范围为 0 ~ 255，针对每一个数据生成对应的 CRC 表：

```cpp
#define CRC_POLY    0x11C
static uint64_t crc_table[256];

for (int i = 0; i < (1<<8); i++) {
    uint64_t crc = i;
      /* 每一字节数据都需要计算 8 次以求取 CRC 的异或值 */
    for (int j=8; j > 0; --j) {
        if (crc & 0x80)  /* 判断最高位是否为1 决定商 1 或者商 0 */ {
            /* 最高位为1，不需要异或，往左移一位，然后与 CRC_POLY异或 */
            crc = (crc << 1) ^ CRC_POLY;
        }
        else {
            /* 最高位为0时，不需要异或，整体数据往左移一位 */
            crc = (crc << 1);
        }
    }
    crc_table[i] = crc;
}
```

使用 CRC 表计算数据，当前数据最高位字节作为查表的索引，reg 专业名词叫做寄存器，可以理解为一个双字节的滑动窗口，初始值为 0，沿着数据字节链每次移动一个字节。

计算步骤如下：

1. register左移一个字节，从原始数据中读入一个新的字节到寄存器的低字节位。
2. 利用刚从 register 移出的高位字节作为 index 定位 table 中的一个 CRC 值，因为生成时也是以该数据计算的 CRC 值。
3. 把这个 CRC 值 XOR 到 register 中组成下一次计算的新的数据，此时最高位的字节已经被消除。
4. 如果还有未处理的数据则回到第一步继续执行。

代码示例：

```cpp
unsigned char   buff[] = {0x31, 0x32, 0x33, 0x34};
unsigned int    len  = sizeof(buff);
unsigned char   *pointer;
unsigned int    regs;

pointer = buff;
regs = 0;

// 在数据长度内迭代计算 CRC
while(len--){
    //  (regs>>8)&0xFF 是为了获取寄存器中的高位字节数据
    // (regs<<8)|*pointer++ 操作时将寄存器高位字节移除，然后寄存器低位字节数据用我们需要计算的数据补充，相当于一次滑动操作。
    regs = ((regs << 8) | *pointer++) ^ table[(regs >> 8) & 0xFF];
}

// 处理数据需要扩展的多项式位宽的补位数据，扩展的数据都是零, 根据 CRC_POLY    0x11C 扩展了 8 bit位一个字节
for(int i = 0;  i< 1; i++) {
    regs = (regs << 8) ^ table[(regs >> 8) & 0xFF];
}
```

驱动表法和直接计算法在思路上是很类似的，都是在循环的消除高 bit 位或高位字节的数据。

以上是 CRC 的一个理论推导过程，下期周报将以 `OOMDetecor` 中的实例讲解实际应用中的变体操作有哪些。

- [【脑冻结】CRC我就拿下了](https://www.cnblogs.com/poiu-elab/archive/2012/10/22/2734715.html "【脑冻结】CRC我就拿下了")
- [不要跑，CRC没这么难！（简单易懂的CRC原理阐述）](https://segmentfault.com/a/1190000018094567 "不要跑，CRC没这么难！（简单易懂的CRC原理阐述）")

***

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
    if(first) {
        first = 0;
        // 针对单个字节值生成单表
        for (n = 0; n < 256; n++) {
            c = (uint64_t)n;
            for (k = 0; k < 8; k++) {
                // LSB 右移生成逻辑， 主要适用于小端模式
                f (c & 1)
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
    
uint64_t rapid_crc64(uint64_t crc, const char *buf, uint64_t len) {
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

有别于[《#53 周报》](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)中的单表查询方式，`OOMDetector`将 `crc_table`定义为`crc_table[8][256]`二维矩阵的多表查询。其中单维度的表仍然以字节大小（8 bit）作为位宽生成，即单个表大小为 `2 ^ 8 = 256`，`crc_table[8]`表示不同权重的单表， 这种方式称为 CRC 位域多表查询 。

**CRC 位域多表查表方法与传统的 CRC 查表方法最大的不同在于多表级联压缩表格空间。**

如果是传统单表查询，一次性查询双字节数据的 CRC，需要单表大小为 `256 * 256`，采用多表级联只需要 `2 *256`，实现了极大的空间压缩。

更详细的原理可以参考《CRC位域多表查表方法》，这里只理解该优化依赖的核心性质：`crc_table[A ^ B] = crc_table[A] ^ crc_table[B]`。

从 CRC 计算的本质出发，其实就是依次的计算每一 bit 位的余数，而余数的结果值，只和 `POLY`计算的次数和顺序有关。

我们以示例 `0xBC`来拆解这个计算过程:

1. 采用右移的计算方式，左移和右移的区别在下小结中讲解。`1011 1010（0xBA`） 计算 CRC Table 简化为：

    ```cpp
    1011 1010 ^ (poly ^ 0>>1 ^ poly>>2 ^ poly>>3 ^ poly>>4 ^ 0>>5 ^ poly>>6 ^ 0>>7)
    ```

2. 现在 `0xBA` 根据异或性质分解为 `0xB0 ^ 0x0A`。

3. 我们单独计算 `0xB0` 和 `0x0A`的 CRC 值，来看他们的计算过程
    ```cpp
    0xB0 = 0b 1011 0000;
    CRC[0xB0] = 1011 0000 ^ (poly ^ 0>>1 ^ poly>>2 ^ poly>>3 ^ 0>>4 ^ 0>>5 ^ 0>>6 ^ 0>>7);
    
    0x0A = 0b 0000 1010;
    CRC[0x0A] =  0000 1010 ^ (0 ^ 0>>1 ^ 0>>2 ^ 0>>3 ^ poly>>4 ^ 0>>5 ^ poly>>6 ^ 0>>7)
    ```
    
4. 上面两个公式做异或，最终结果值和 `CRC[0xBA]`相等

    ```cpp
    CRC[0xB0] ^ CRC[0x0A] = 1011 0000 ^ (poly ^ 0>>1 ^ poly>>2 ^ poly>>3 ^ 0>>4 ^ 0>>5 ^ 0>>6 ^ 0>>7) ^ 0000 1010 ^ (0 ^ 0>>1 ^ 0>>2 ^ 0>>3 ^ poly>>4 ^ 0>>5 ^ poly>>6 ^ 0>>7);
    
    // 由于 0 异或任何值还是原值，结果可以简化为:
    1011 0000 ^ 0000 1010 ^ (poly ^ 0>>1 ^ poly>>2 ^ poly>>3 ^ poly>>4 ^ 0>>5 ^ poly>>6 ^ 0>>7)；
    ```

5. 即证明 CRC 性质：`crc_table[A ^ B] = crc_table[A] ^ crc_table[B]`成立。

CRC 级联查表另一个需要解决的就是多字节数据的权重问题，上面证明了 CRC 性质可行性，但是在查表时为了方便，使用的索引并非是直接拆解的数据，例如 `CRC[0x AA BB] = CRC[0x AA 00] ^ CRC[0xBB]` ，两次查表索引分别为 `0xBB 和0xAA`，并非是 `0xBB 和 0xAA 00`。

权重就是指的由 `CRC[0xAA]` 计算 `CRC[0xAA 00] ... CRC[0xAA 00 00 00 00 00 00 00]` 等数据，实现也很简单，可以看做是已知单表crc_table[256]的值，求数据的值，即 `init_crc_table_for_oom()`中第二个 `for` 的目的。

#### 生成表-单表反向计算（reversed）

`OOMDetector` 生成单表时区别于传统的 MSB 左移(<<) 计算方式，采用的是 LSB 右移(>>) 生成方式。原因是 iOS 的主机字节序是小端模式，但是一般规范中要求数据在网络传输过程中采用网络字节序（大端模式）。

> 一个系统中针对每一个字节内的 bit 位也是有顺序的，称为位序。

位序一般和主机字节序是一致的，例如一个数据 `0x11 22` 在 iOS 内存中的存储为 `0x22 0x11 `，实际 `0x11 = 0b 0001 0001`的存储顺序也是逆序的，表示为 `0b 1000 1000`。

为了按照网络字节序传输规范作为计算 CRC 顺序的依据，小端的机器上在使用 CRC 时都采用右移计算，即 `0b 1000 1000`按照右移顺序依次计算 `0 0 0 1 0 0 0 1`，这样保证了规范性，无论其他 server 接收端是大端模式还是小端模式，在拿到数据后自己按照主机字节序重新计算即可。

**反向计算最重要的一点：由于计算顺序反向，所以 POLY生成多项式的值相对于传统给定的生成多项式值，也要做位序的反向生成新的 POLY值。**

#### 查表

在 `rapid_crc64()`查表中一次计算了 8 字节数据的 CRC 值，根据`crc_table[A ^ B] = crc_table[A] ^ crc_table[B]`性质，查表操作以对应权重的字节数据在相应的级联表中查找值即可，具体到每一个级联表，和单字节的查表逻辑一致。最终结果是各个权重字节数据的异或结果。

示例计算数据为 `0x AA BB CC DD 11 22 33 44` ，在小端模式是逆序存储的，所以在计算 CRC 值时是从低字节到高字节（即从右到左）顺序计算的。分解计算步骤来分析：

1. 根据异或计算的性质 `0x AA BB CC DD 11 22 33 44 = 0x44 ^ 0x33 00 ^ 0x 22 00 00 ^ 0x11 00 00 00 ... ^ 0xAA 00 00 00 00 00 00 0`
2. 结合 CRC 性质 `CRC[0x AA BB CC DD 11 22 33 44] = CRC[0x44] ^ CRC [0x33 00] ^ .... CRC[0xAA 00 00 00 00 00 00 00]`
3. 根据二维级联表，查找每一个字节的 CRC，`CRC[0x 3300] = crc_table[1][0x33]`。注意这里是用 `0x33`作为索引计算数据 `0x33 00`的值，和计算数据 `0x33` 是有区别的，所以在生成表时需要做二次遍历以生成不同权重的单表值。（这里的权重可以理解为单字节数据在 8 个字节中的位置，从左到右为 MSB => LSB）

`OOMDetector` 在查表之前和查表之后都做了一次取反操作 `c = ~c`，该变体的目的是解决普通 CRC 无法区分只有起始 0 的个数不同的两个数据。（暂时未理解这个目的，所以直接引用 wiki 中的解释）

> [《循環冗餘校驗-wiki》](https://zh.wikipedia.org/wiki/%E5%BE%AA%E7%92%B0%E5%86%97%E9%A4%98%E6%A0%A1%E9%A9%97 "循環冗餘校驗-wiki")：移位寄存器可以初始化成1而不是0。同样，在用算法处理之前，消息的最初n个数据位要取反。这是因为未经修改的CRC无法区分只有起始0的个数不同的两条消息。而经过这样的取反过程，CRC就可以正确地分辨这些消息了。

- [CRC位域多表查表方法](https://www.eefocus.com/HotPower/blog/12-09/285545_d6429.html/ "CRC位域多表查表方法")

***

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)

### iOS WebView 中的 User-Agent

User-Agent 中文名为用户代理，简称 UA（后文中的 User-Agent 统一用 UA 表示），它是一个特殊的字符串头，内容涵盖客户端的操作系统类型及版本、CPU 类型、浏览器及版本、浏览器语言等；`WebView` 会在每个 URL 请求头中携带该信息。

UA 在项目中的常见应用：

1. 区分访问客户端是移动端还是 PC，如果是移动端还可以区分是 iOS 或者 Android。
2. 收集有关访问者的统计信息，例如渠道信息等。
3. 传递一些基础数据，例如站点、协议版本号、app 名称等等和业务相关的基础信息。

#### UA 字符串格式 

**UA 字符串格式：**Mozilla/[version] ([system and browser information]) [platform] ([platform details]) [extensions]

由于浏览器厂商的历史兼容性问题，很多字段值都没有严格按照格式排布，有些字段值和最初的定义也不具有对应价值。各部分描述参考如下：

- Mozilla/[version]：设计目的是描述浏览器名称以及版本，但是由于浏览器兼容性问题，已经没有实际意义，一般值为 `"Mozilla/5.0"`。
- ([system and browser information])：CPU 操作系统以及浏览器信息，值是以 `;`分割的。例如 `"Macintosh; Intel Mac OS X 10_13_6"` Macintosh 指的是 Mac 平台、CPU 类型是 intel、 操作系统为 10.13.6 MacOS。
- [platform]： 浏览器渲染引擎，chrome/safari浏览器的值一般为 `"AppleWebKit/xxx"` 表示内核为`webkit/blink`。
- ([platform details])： 浏览器渲染其他补充信息，同样由于兼容性问题，值不具有代表意义，例如 iOS 上是 `(KHTML, like Gecko)`
- [extensions]：扩展字段，主要描述了浏览器信息以及自定义字段，自定义字段是 key/value 形式，例如 `protocol/1.0.0` 传递协议版本等内容。扩展字段中一些字段描述：
    - Chrome：Chrome/版本号
    - Safari：Safari/版本号 （chrome 浏览器后面也会带 Safari 字段）
    - Version：Version/版本号
    - Mobile：移动设备标识，一般指内部版本号，苹果设备会带版本号，安卓设备不含版本号

iPhone 上的示例格式如下:

```cpp
Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X)  AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148
```

其他数据值类型参考[解析Navigator.userAgent的迷惑行为](https://juejin.cn/post/6908647211945590791 "解析Navigator.userAgent的迷惑行为")

#### 获取系统的 UA

iOS 获取 UA 的方式是相似的，都是直接调用 js  查询 `navigator.userAgent`；区别在于执行 js 的 api 不同。iOS 已经淘汰了 `UIWebView` 所以这里只做对比了解就可以。

```objectivec
// UIWebView
UIWebView *webView = [[UIWebView alloc] initWithFrame:CGRectZero];
self.userAgent = [webView stringByEvaluatingJavaScriptFromString:@"navigator.userAgent"] ?:@"";

// WkWebView
WKWebViewConfiguration *config = [[WKWebViewConfiguration alloc] init];
if (@available(iOS 13.0, *)) {
   config.defaultWebpagePreferences.preferredContentMode = WKContentModeMobile;
}
WKWebView *webView = [[WKWebView alloc] initWithFrame:CGRectZero configuration:config];
[webView evaluateJavaScript:@"navigator.userAgent" completionHandler:^(id _Nullable response, NSError *_Nullable error) {
        self.userAgent = (NSString *)response;
}];
```

`UIWebView` 是同步方式， `WKWebView` 是异步方式，所以要注意如果是使用 `WKWebView`，确保 user-agent 已经设置完成后再创建 web 页面，否则会造成自定义信息的丢失。

#### 修改 UA

一般场景因为业务需求，经常需要在 UA 里添加自定义值，有三种方式来修改默认的 UA 值。

1. 修改系统 UA，程序一旦杀死更改的 UA 也会随即失效，如果希望保持更改 UA，则需要在每次应用启动时重新更改系统User-Agent。修改后使用 `NSUserDefaults` 进行缓存，APP 内所有的 H5 页面共享使用。

```objectivec
- (void)updateSystemUserAgent:(NSString *)userAgent {
    [[NSUserDefaults standardUserDefaults] registerDefaults:@{@"UserAgent":userAgent}];
    [[NSUserDefaults standardUserDefaults] synchronize];
}
```

2. iOS 12支持修改局部的 UA，此时 UA 仅在当前的 `WebView`的生命周期内生效，随着 `WebView` 销毁，更改的 UA 信息就会随机失效。作用域是针对 `WebView` 实例的。

```objectivec
- (void)updateCustomUserAgent:(NSString *)userAgent {
    [self.wkWebView setCustomUserAgent:userAgent];
}
```


3. 通过 `applicationNameForUserAgent` 设置，该方式非直接覆盖，而是将设置的值追加到默认值的后面。也是仅针对当前 config 生效的。

```objectivec
let config = WKWebViewConfiguration()
config.applicationNameForUserAgent = "Custom User Agent"
let webview = WKWebView(frame: .zero, configuration: config)
    
// 修改后的UA 值为：`Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Custom UserAgent`。
```

`applicationNameForUserAgent`在客户端获取默认值仅有 `Mobile/16A404`，实际上 web 页面获取到的是完整的值。

> **三种方式的优先级：**`customUserAgent > UserDefault > applicationNameForUserAgent`

#### 注意事项

1. `WKWebView` 获取系统 UA 为异步方式，如果需要多次设置 UA，则需要依次进行，否则会造成覆盖问题。

2. 修改自定义 UA，需要在创建加载页面的 `WKWebView` 前设置好。所以一般情况是在 `AppDelegate中`使用临时对象调用 `evaluateJavaScript:@"navigator.userAgent"`，否则会造成加载页面的 `WKWebView`首次使用 UA 失效。需要重新 reload webview 才生效。

3. 由于第一种经常造成莫名失效问题， 建议使用 2、3 设置方式。

- [iOS - User Agent 的应用和设置](https://www.cnblogs.com/lxlx1798/p/10819610.html "iOS - User Agent 的应用和设置")
- [WKWebView 设置自定义UserAgent正确姿势](https://juejin.cn/post/6844903632152821773 "WKWebView 设置自定义UserAgent正确姿势")
- [记使用WKWebView修改user-agent在iOS 12踩的一个坑](https://cloud.tencent.com/developer/article/1158832 "记使用WKWebView修改user-agent在iOS 12踩的一个坑")

***

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

    

## 摸一下鱼

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Graphviz

**地址**：http://www.graphviz.org/

**软件状态**：免费

**软件介绍**：

贝尔实验室开发的有向图/无向图自动布局应用，支持 dot 脚本绘制结构图，流程图等。

![Graphviz](https://cdn.zhangferry.com/Images/20220217174238.png)

对产物`.gz`文件进行解析查看的途径。

- 在线网站：[GraphvizOnline](http://dreampuf.github.io/GraphvizOnline "GraphvizOnline")
- vs 插件：Graphviz (dot) language support for Visual Studio Code


结合`cocoapods-dependencies`插件，我们可以解析`podfile`文件来分析项目的`pod`库依赖，生成`.gz`文件。

* 生成`.gz`文件：`pod dependencies --graphviz`
* 生成依赖图：`pod dependencies --image`
* 生成`.gz`文件及依赖图：`pod dependencies --graphviz --image`


整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 南大软件分析课程

**地址**：https://www.bilibili.com/video/BV1b7411K7P4

南京大学《软件分析》课程系列，非常难得的高质量课程，可以通过[这里](https://pascal-group.bitbucket.io/teaching.html "软件分析课件")获取所有课程的课件。

### iOS 开发学习图谱

**地址**：http://hdjc8.com/iOSRoadMap/

一份特别丰富的 iOS 开发学习图谱，其中包含了许多 iOS 开发的资源，编者认为这本图谱不适合作为学习的一个路线，适合作为一份让你了解 iOS 有哪些知识点的图谱，其中的许多的知识点很适合作为查漏补缺的一个工具。在我们做工作中常常会仅做某些领域内的工作，导致在不短的一段时间内接触的技术是比较窄的，假如你突然想了解一些别的知识点，你可以来这本图谱中闲逛一下，看看有什么知识点是你感兴趣的，也许有一些是你以前感兴趣但是由于种种原因没来及了解的内容！

***


整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### EasyFind 

**地址**：https://easyfind.en.softonic.com/mac

**软件状态**：免费

**软件介绍**：

小而强大的文件搜索应用，媲美 `windows` 下的 `Everything`。

![EasyFind](https://cdn.zhangferry.com/Images/easyfind-easyfind.png)




整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 程序员做饭指南

**地址**：https://github.com/Anduin2017/HowToCook

一个由社区驱动和维护的做饭指南。在这里你可以学习到各色菜式是如何制作的，以及一些厨房的使用常识和知识。比较有意思的是，该仓库里的菜谱大都对制作过程中的细节和用量描述准确，比如菜谱中有 `不允许使用不精准描述的词汇，例如：适量、少量、中量、适当。` 等非常严格准确的要求，对几乎每个菜谱都做到了简洁准确，非常有意思，也非常欢迎大家贡献它~

***


整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### nginxedit 

**地址**：https://www.nginxedit.cn/

**软件状态**：免费

**软件介绍**：

`Nginx`在线配置生成工具，配置高性能，安全和稳定的`Nginx`服务器的最简单方法。

![nginxedit](https://cdn.zhangferry.com/Images/Nginx%E5%9C%A8%E7%BA%BF%E9%85%8D%E7%BD%AE%E7%94%9F%E6%88%90%E5%B7%A5%E5%85%B7.png)


整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Swift 实现的设计模式

**地址**：https://oldbird.run/design-patterns/#/

一份由 Swift 语言实现的设计模式教程。其中设计模式的举例清晰明了，代码也简洁易懂，大部分例子中有 UML 图来帮助理解，其中也会有一些对于不同设计模式之间区别与联系的总结和归纳，是很不错的学习设计模式的资源。

![](https://cdn.zhangferry.com/Images/20220302215124.png)

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

本次推荐一系列关于 UI 调试的软件，包含电脑端以及 App 端两种类型；

**电脑端**

- [Reveal](https://revealapp.com/)：经典UI调试软件，但需要付费；
- [Lookin](https://lookin.work/)：腾讯出品的一款免费好用的 iOS UI 调试软件；

**App 端**

- [FLEX](https://github.com/FLEXTool/FLEX)：FLEX (Flipboard Explorer) 是一套用于 iOS 开发的应用内调试工具；
- [啄幕鸟iOS开发工具](https://github.com/alibaba/youku-sdk-tool-woodpecker)：阿里出品的一套用于 iOS 开发的应用内调试工具；

> 其中 Reveal、Lookin、FLEX 都有对应的`Tweak`，有越狱设备的小伙伴可以玩一玩；


整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### KKBOX iOS/Mac OS X 基礎開發教材

**地址**：https://zonble.gitbooks.io/kkbox-ios-dev/content/

一份来自台湾 KKBOX 的 iOS/Mac OS 开发部门编写的新人学习材料。这份学习材料不算是从 0 到 1 的入门材料，阅读这份教材需要一些简单的基础，教材主要是在你已经会一些简单 OC 代码的基础上帮助你深入探讨一些在代码中常见的小问题和小细节，也是对技术探索方向的一些指引和指导。教材中的描述语言非常亲切不生硬，就像是有一位同龄人在你旁边指导你的代码有什么问题一样，阅读体验非常不错，虽然内容略有陈旧，但也值得新手开发者阅读一下。

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Aria2GUI 

**地址**：https://github.com/yangshun1029/aria2gui

**软件状态**：免费

**软件介绍**：

`Aria2GUI` 是一款支持多种协议的轻量级命令行下载工具，可以轻松的下载离线资源。

![Aria2GUI](https://cdn.zhangferry.com/Images/687474703a2f2f692e696d6775722e636f6d2f4d455a7150397a2e706e67.png)



整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Rust 数据结构与算法

**地址**：https://github.com/QMHTMY/RustBook

一本 Rust 书籍，有简体和繁体版（英文版和日文版正在撰写中），内容包括算法分析，基本数据结构和算法，外加一些实战，共有九章。包含了大家常用的常见的数据结构的实现和讲解，配有详实的代码和清晰简明的图解。

![](https://cdn.zhangferry.com/Images/%E6%88%AA%E5%B1%8F2022-03-17%20%E4%B8%8B%E5%8D%886.37.13.png)

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### flomo

**地址**：https://flomoapp.com/

**软件状态**：免费

**软件介绍**：

 `flomo` 是新一代卡片笔记工具，秉承尼克拉斯 · 卢曼（Niklas Luhmann）的卡片笔记法理念，让你能更好的利用碎片时间积累知识，建立知识间的关联。

![flomo](https://files.mdnice.com/user/15579/203f041f-a6ec-4d0a-af5b-599a579225c1.png)

### MoneyProgress

**地址**：https://github.com/Lakr233/MoneyProgress

**软件状态**：免费

**软件介绍**：

老王的又一力作：钱条。

> 上班的进度条，开始搬砖吧。

![MoneyProgress](https://files.mdnice.com/user/15579/65fa2fe0-11ad-4a00-9d5f-4007ebb2edab.png)


整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Java 全栈知识体系

**地址**：https://pdai.tech/

以 Java 开发为背景的全栈开发知识体系，内容包含软件开发、算法、面试、架构、项目、产品团队以及一些方法论的思考。站内资源海量详实，文章和网站的排版和设计很规范，阅读起来非常舒适，也多有漂亮的示意图来帮助读者理解，内容非常丰富。关于这个网站的建立初衷以及介绍可以看[这里](https://pdai.tech/md/about/me/about-me.html#q2---%E5%81%9A%E8%BF%99%E4%B8%AA%E7%BD%91%E7%AB%99%E7%9A%84%E5%88%9D%E8%A1%B7%E6%98%AF%E4%BB%80%E4%B9%88 "Java 全栈知识体系建设初衷")。

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Decode

**地址**：https://microcodingapps.com/products/decode.html

**软件状态**：$8.99

**软件介绍**：

 将 `Xcode Interface Builder` 文件（`Xib` 和 `Storyboard` 文件）转换为 `Swift` 源代码。

![Decode](http://cdn.zhangferry.com/top-d338be7e-1200.png)



整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 即时教程

**地址**：https://js.design/courses

由[即时设计](https://js.design/)社区组织的精选设计课程，即时设计是一款可以在线实时协作的专业 UI 设计工具，类似 Figma。在即时教程中你可以找到来自各大视频网站平台创作者们的免费高质量课程。从零基础开始一步步到做案例，进阶技巧，应有尽有，非常适合想学一点 UI 知识的程序员们。

![](https://cdn.zhangferry.com/Images/20220331222838.png)

***

整理编辑：[CoderStar]()

### AppleParty

**地址**：https://github.com/37iOS/AppleParty

**软件状态**：开源

**软件介绍**：

介绍一个我们周报团队成员所在公司开源的一个项目：`AppleParty`

`AppleParty` 是三七互娱旗下37手游 iOS 团队研发，实现快速操作 `App Store Connect` 后台的自动化 `macOS` 工具。

支持功能：

* 内购买项目管理（批量创建和更新）；
* 批量商店图和预览视频上传和更新；
* 邮件发送工具；
* 二维码扫描和生成工具；

![AppleParty](http://cdn.zhangferry.com/06.jpeg)


整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### 闲话 Swift 协程

**地址**：https://www.bennyhuo.com/book/swift-coroutines/

该系列博客从浅入深地介绍了 Swift 在 5.5 中新支持的协程特性。该系列文章介绍了 Swift 协程的特性，内容以 Swift 协程的基本概念、语法设计、使用场景等方面为基础展开，也会与大前端开发者常见的 Kotlin、JavaScript 做对比（作者是 Kotlin GDE），作者希望这个系列能给大家一个更多元化的视角来理解这个语法特性，十分推荐。

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Quiver

**地址**：https://yliansoft.com/#quiver

**软件状态**：免费

**软件介绍**：

`Quiver`是为程序员打造的笔记本。它让您可以在一个笔记中轻松混合文本、代码、`Markdown` 和 `LaTeX`，使用出色的代码编辑器编辑代码，实时预览 `Markdown` 和 `LaTeX`，并通过全文搜索立即找到任何笔记。

包含`MacOS`、`iOS`两端。

![Quiver](http://cdn.zhangferry.com/screenshot1.png)

### iTab

**地址**：https://www.itab.link/

**软件状态**：免费

**软件介绍**：

一款浏览器空白 Tab 页定制工具，支持几乎所有主流浏览器。iTab 提供了很多模板，你可以自由地搭建属于自己的 Tab 页。同时配备备忘录，TODO 等功能，浏览器在平常的工作中使用频率非常高，综合体验下来，把一部分内容聚焦到浏览器中的 Tab 页确是一个提高效率的好方案。

![](https://cdn.zhangferry.com/Images/20220421230343.png)


整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### iOS 高性能app架构

**地址**：https://github.com/dudongge/iOS_Architecture

该仓库是 [Advanced iOS App Architecture (1st Edition)](https://zh.sg1lib.org/book/5002805/90c154) 的翻译本，对于译文修改了一些错别字，有 pdf 和 word 可以选择。本书主要讨论了在开发 App 的时候，代码在各种架构中的表现和细节的不同，讨论了各种架构的优缺点以及在 iOS 中，这些架构又有何特点和不同。


***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Bartender

**地址**：https://www.macbartender.com/

**软件状态**：免费

**软件介绍**：可以免费试用4周，购买费用 $15;

`Bartender`是一款很棒的菜单栏管理工具，有效解决当屏幕比较小时，顶部菜单栏显示不全的问题；

![Bartender](http://cdn.zhangferry.com/20220427102101.png)



整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Python 最佳实践指南

**地址**：https://pythonguidecn.readthedocs.io/zh/latest/

这是一份关于 Python 的实践指南，该指南目前持续不断地更新与完善，在 Github 上有 5.8k 的 Stars。它旨在为 Python 初学者和专家提供一个关于 Python 安装、配置和日常使用的最佳实践手册。涵盖各种平台的 Python 安装、优秀的模块推荐、配合不同的 web 框架和工具、如何写出优雅的 Python 代码等内容。链接中的这份是该指南的中文版。

![](https://cdn.zhangferry.com/Images/52-python.png)

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### IINA

**地址**：https://iina.io/

**软件状态**：免费

**软件介绍**：

适用于 `macOS` 的 **现代** 媒体播放器，`IINA` 由开源媒体播放器 `mpv` 提供支持，几乎可以播放您拥有的所有媒体文件。

![iina](http://cdn.zhangferry.com/sc-sky.png)


整理编辑：[zhangferry](https://zhangferry.com)

### Skr_Learning

**地址**：https://github.com/Kiprey/Skr_Learning

这里将定期记录着一些与`Sakura`师傅以及一群小伙伴共同学习的内容与进度。是一篇学习汇报，内容包括但不限于C++ STL、编译原理、LLVM IR Pass代码优化、CSAPP Lab、uCore操作系统等等。持续更新ing...

感觉 Github 也是一种很好的记录学习过程的平台！

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### CotEditor

**地址**：https://coteditor.com/

**软件状态**：免费

**软件介绍**：

适用于 `macOS` 的纯文本编辑器，轻巧、整洁并且功能强大。

![CotEditor](http://cdn.zhangferry.com/screenshot@2x.png)




整理编辑：[zhangferry](https://zhangferry.com)

### 英语进阶指南

地址：https://babyyoung.gitbook.io/english-level-up-tips/

![](https://cdn.zhangferry.com/Images/20220518204154.png)

英语是程序员绕不过去的一项技能，虽然我们可能从小学就开始接触英语了，但直到毕业工作，英语能够不成为学习障碍还是一件不容易的事情。这其中的差别很大成分可以归结为学习方法，这份文档就是这样一个注重方法和可操作性的英语学习指南。

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### itsycal

**地址**：https://www.mowglii.com/itsycal/

**软件状态**：免费

**软件介绍**：

一款简洁的适用于`mac`的日历软件。

![itsycal](http://cdn.zhangferry.com/20220526142405.png)



整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### TypeScript 入门教程

**地址**：https://ts.xcatliu.com/

这是一份 TypeScript 的入门教程，与官方手册不同，这份 TypeScript 入门教程着重于从 JavaScript 程序员的角度总结思考，循序渐进的理解 TypeScript，示例丰富，比官方文档更易读。同时作者也指出，本书比较适合已经熟悉 JavaScript 的开发者，不适合没有学习过 JavaScript 的人群。

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

### Mac-CLI

**地址**：https://github.com/guarinogabriel/Mac-CLI

**软件状态**：免费

**软件介绍**：

面向开发人员的 `macOS` 命令行工具。

![Mac-CLI](http://cdn.zhangferry.com/demo.gif)



整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

### Exploring Swift Memory Layout

**地址**：https://www.youtube.com/watch?v=ERYNyrfXjlg

一份来自 GOTO Conferences 有关 Swift Memory Layout 的一小时讲座，该讲座深入浅出的讲解了 Swift 中各种例如指针、结构体、类、枚举、数组、协议等我们平时使用的这些工具在内存中是以什么样的形式存在，以及如何解决一些常见问题。对于想了解这部分知识的朋友，这个讲座视频将是一个不错的开胃菜。

![memorylayout](https://cdn.zhangferry.com/Images/memorylayout.png)

***

1、[Felibe444](https://twitter.com/felibe444 "Felibe444") 总结了 WWDC22 里 What's new in Swift 和 What's new in UIKit 对应的功能点，并将它们做成 Sketchnote：

![](https://cdn.zhangferry.com/Images/20220623091955.png)

![](https://cdn.zhangferry.com/Images/20220623092017.png)

2、iOS 16、iPadOS 16、macOS 13、watchOS 9、tvOS 16 发布了第二个 beta 版本。

![](https://cdn.zhangferry.com/Images/FV34em9WAAAAAzH.jpeg)

3、[Apple Logo Artwork](https://www.figma.com/community/file/1117235995751919225 "Apple Logo Artwork")：

![](https://cdn.zhangferry.com/Images/20220619104319.png)

早在 2018 年，苹果公司就发出了独特的媒体邀请，它为自己的 logo 设计了无数个独特、多彩的版本，每个人似乎都收到了不同风格的邀请。苹果公司的商标图案从抽象到经典各不相同，由多位艺术家参与设计。在 Figma 上的这个仓库收录了多达 350 个 Logo。

4、[Brooklyn](https://github.com/pedrommcarrasco/Brooklyn "Brooklyn") 一款 Mac 版屏保，灵感来源于 2018 年的 Apple Event，这些素材正是 Apple Logo Artwork，效果非常酷炫。

![](https://cdn.zhangferry.com/Images/showcase.gif)

5、[PicX](https://github.com/XPoet/picx "PicX") 是一款基于 GitHub API & jsDelivr 开发的具有 CDN 加速功能的图床管理工具。

***

整理编辑：[东坡肘子](https://www.fatbobman.com)、[师大小海腾](https://juejin.cn/user/782508012091645/posts)

1、[Goldfishies](https://goldfishies.com "Goldfishies")：开启真·摸鱼模式，在线养金鱼，有 5 种皮肤的鱼可选。对程序员来说刚刚好，不幼稚。

![](http://cdn.zhangferry.com//Images/20220630214456.png)

2、[MusicForProgramming](https://musicforprogramming.net/fortyone "MusicForProgramming")：极客风的听歌网站，纯文字的音乐播放器，作者说里面都是适合编程的音乐。

![](http://cdn.zhangferry.com//Images/20220630213027.png)

3、[网页设计博物馆](https://www.webdesignmuseum.org/ "网页设计博物管")：该网站收录了从 1996 开始至今的一些主流网站的页面样式，从这里能清晰的感受网站设计这几十年的变化趋势。看一下 Apple 在 1999 年发布 Power Mac G4 的页面，突出重点，结构清晰。再说 Power Mac G4，用现在的眼光来看，它依然像是一款未来项的产品，Apple 的设计真的很超强。

![](https://cdn.zhangferry.com/Images/20220630235025.png)

4、[Stackoverflow 的年度调查](https://survey.stackoverflow.co/2022/ "Stackoverflow 的年度调查")：调查结果来源于 70000 多个开发者的问卷分析，看两个比较有意思的结果吧。

参与调查的开发者的身份，全栈和后端所占比例非常高，移动开发相比就少很多了。

![](https://cdn.zhangferry.com/Images/20220701000811.png)

薪水和使用开发语言、工作年限之间的关系，这一批调查者占总人数的一半以上，工作年限从 9 年到 22 年，所以至少在国外大龄程序员是一个很常见的现象。

![](https://cdn.zhangferry.com/Images/20220701002813.png)

***

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

1、[iOS Icon Gallery](https://www.iosicongallery.com/ "iOS Icon Gallery")：一个收录 App Store 上精美的 iOS/macOS/watchOS icon 的网站，可以为作为设计师的你在设计 icon 时提供良好的设计灵感。

![](https://cdn.zhangferry.com/Images/20220707204618.png)

![](https://cdn.zhangferry.com/Images/20220707204501.png)

2、[Thief](https://thief.im/ "Thief")：`Thief` 是一款基于 `Electron`开发的跨平台多功能(`真正创新的`)摸鱼软件，为了上班族打造的`上班必备神器`，使用此软件可以让上班`倍感轻松`，远离 `ICU`。

- **多功能** 不仅仅支持 `小说摸鱼` ，还支持 `股票`、`基金`、`网页`、`视频`、`直播`、`PDF`、`游戏 `等摸鱼模式
- **隐蔽性** 每种摸鱼模式都提供了不同的摸鱼 **技巧**，可以很隐秘地进行摸鱼
- **跨平台** 支持 `Win` + `Mac` + `Linux` , 不管你用什么系统，`Thief` 都让你无缝隙摸鱼

![](https://cdn.zhangferry.com/Images/20220707205920.png)

![](https://cdn.zhangferry.com/Images/20220707210020.png)

3、[Objective-See's Tools](https://objective-see.org/tools.html "Objective-See's Tools")：提供了一系列保护 Mac 的免费、开源的工具。

![](https://cdn.zhangferry.com/Images/20220707211351.png)

4、[sao-gen-gen 骚话生成器生成器](https://github.com/disksing/sao-gen-gen "sao-gen-gen 骚话生成器生成器")：一款用来生成骚话生成器的生成器，你可以通过提交 GitHub Issue 来创建你的生成器！

![](https://cdn.zhangferry.com/Images/20220707212753.png)

![](https://cdn.zhangferry.com/Images/20220707213902.png)

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

![](https://cdn.zhangferry.com/Images/20220714233011.png)

- [iconpark](https://iconpark.oceanengine.com/home "iconpark")：字节出品的一款图标网站；
- [iconfont](https://www.iconfont.cn/ "iconfont")：估计这个大家都知道，就不介绍了；
- [icons8](https://icons8.com/animated-icons "icons8")：Icons8 推出的动态图标网站；
- [openmoji](https://openmoji.dashgame.com/#/ "openmoji")：面向设计师、开发人员和其他人的开源表情符号！

自己做`Side Project`的时候用的上哦！

***

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1. [JSON Hero](https://github.com/jsonhero-io/jsonhero-web "JSON Hero")，一款让你轻松直观地查看 JSON 文档的工具，为你提供类似 Mac Finder 体验的工具。

   ![](https://cdn.zhangferry.com/Images/features-treeview.gif)

   如果你的 JSON 文件足够庞大，这款软件必不可少。

2. [SingleFile](https://github.com/gildas-lormeau/SingleFile "SingleFile")是一种 Web 扩展（和 CLI 工具），与Chrome、Firefox（桌面和移动）、Microsoft Edge、Vivaldi、Brave、Waterbox、Yandex browser 和 Opera 兼容。它可以帮助您将完整的网页保存到单个 HTML 文件中。

3. [State-of-the-Art Shitcode Principles](https://github.com/trekhleb/state-of-the-art-shitcode "State-of-the-Art Shitcode Principles") 这是一个`Shitcode`书写准则，来学习下「垃圾」代码的艺术。

   ```swift
   /// 💩 Mix variable/functions naming style
   
   ///Good 👍🏻
   let wWidth = 640;
   let w_height = 480;
   
   ///Bad 👎🏻
   let windowWidth = 640;
   let windowHeight = 480;
   ```

4. [This-repo-has-N-stars](https://github.com/fslongjin/This-repo-has-838-stars "This-repo-has-N-stars") 如项目名称所示，这个项目有 N 个 Star，当 Star 的数量发生改变时，项目名称会被动态地更新。

5. [摸鱼游戏](https://moyu.games "摸鱼游戏") 可能是一个全方位的摸鱼指南，无论你是想休闲娱乐还是需要学习，都能给你提供不一样内容。

6. [Qwerty Learner](https://qwerty.kaiyi.cool/ "Qwerty Learner")：练打字，学英语，学编程词汇，一个网站全搞定w(ﾟДﾟ)w

   ![](https://cdn.zhangferry.com/Images/20220721230920.png)

7. Apple 全系系统迎来了一波更新，最新版本如下：

   | OS      | Version | Build |
   | ------- | ------- | ----- |
   | iOS     | 15.6    | 19G71 |
   | iPadOS  | 15.6    | 19G71 |
   | macOS   | 12.5    | 21G72 |
   | watchOS | 8.7     | 19U66 |
   | tvOS    | 15.6    | 19M65 |

***

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[Flowful](https://flowful.app "Flowful") 是一个提供多种氛围类型环境音乐（ 由程序生成 ）的播放器网站。其目标是通过可定制的环境音乐生成器来激发无尽的专注。经过试听后，很难说这些音乐是否能够起到开发助力器的作用，但相当地适合冥想。目前网站提供的音乐大多数都是免费的。

![Flowful](https://cdn.zhangferry.com/Images/flowful.png)

2、[Tencent/lemon-cleaner](https://github.com/Tencent/lemon-cleaner "Tencent/lemon-cleaner")：腾讯柠檬清理是针对 macOS 系统专属制定的清理工具。主要功能包括重复文件和相似照片的识别、软件的定制化垃圾扫描、可视化的全盘空间分析、内存释放、浏览器隐私清理以及设备实时状态的监控等。重点聚焦清理功能，对上百款软件提供定制化的清理方案，提供专业的清理建议，帮助用户轻松完成一键式清理。

腾讯的柠檬清理在上周开源了。这个 app 是针对 macOS 系统专属制定的清理工具。此次开源的是完整版本（ App Store 版本中功能不全 ）。社区对于腾讯的这次开源行为给予了良好的反馈，48 小时该项目已经获得了 1K+ 的 star 。由于此次的开源很突然且并不符合腾讯的一贯风格，不少人打趣说是否开发团队领大礼包了。

![腾讯柠檬清理](https://cdn.zhangferry.com/Images/lemon-cleaner.png)

3、[便携小空调](http://game.waimai.zone/air/ "便携小空调")：今年夏天，世界各地都进入了烤箱模式，每个人都渴望在充满冷气的房间里，听着音乐，喝着冷饮。便携小空调将为你提供全方位的空调体验（ 除了不制冷 ），为你的精神空间带来一丝冰凉。

![便携小空调](https://cdn.zhangferry.com/Images/air-conditioner.png)

4、[Awesome Readme Template](https://github.com/Louis3797/awesome-readme-template "Awesome Readme Template")：一个开源项目，提供了数种 Readme 模板。降低使用者创建文档的难度，为摸鱼提供便利。

5、[回村三天，二舅治好了我的精神内耗](https://www.bilibili.com/video/BV1MN4y177PB?spm_id_from=333.337.search-card.all.click&vd_source=47c38aa7a1b9837457a41f3f489f9377 "回村三天，二舅治好了我的精神内耗")：从夏日祭到 CBA 侵权，最近几天 B 站的日子不太好过。不知道横空出世的二舅能否缓解 BiliBili 的危机。

6、[文昌哪些地方可以观测火箭发射](http://haikou.bendibao.com/tour/20201030/47241.shtm "文昌哪些地方可以观测火箭发射")：随着“问天”舱的对接成功，我国的空间站建设又向前迈进了一大步。2022 下半年海南文昌还会迎来多次的发射，有兴趣现场观看的小伙伴应该提前做好攻略。

***

现在的网页功能是非常强，不只是各种各样的应用，现在很多操作系统都搬到了网页上，本期内容会推荐几个在线的操作系统，虽然不知真的操作系统，但作为预览，功能还是很丰富的。

1、[win11在线体验](https://win11.blueedge.me/ "win 11 在线体验")：该项目使用React实现的，代码地址：https://github.com/blueedgetechno/win11React 。

![](https://cdn.zhangferry.com/Images/20220731124759.png)

2、[操作系统风格的博客](goodmanwen.github.io "操作系统风格的博客")：这是一个 Blog 项目，该 Blog 的主题是模拟 Linux 桌面主题中的 Deepin distro。其本质是一个托管在 Github Page 上的博客，你也可以配置一个这样酷酷的主题。

![](https://cdn.zhangferry.com/Images/20220731130051.png)

3、[dustinbrett.com](dustinbrett.com "dustinbrett.com")：一个模拟 Windows 的网站，也可以把它理解成一个作者的个人网站。这里面还集成了一个毁灭战士早期的版本，你可以在这个网站里玩它。

![](https://cdn.zhangferry.com/Images/20220731143028.png)

4、[copy/v86](https://copy.sh/v86/ "https://copy.sh/v86/")：在浏览器中运行 x86 操作系统，这个模拟跟前面提到的 H5 技术不同，它是采用 WebAssembly 把原来的 x86 OS 代码转成 wasm 在线上运行的，更贴近「真」操作系统。

![](https://cdn.zhangferry.com/Images/20220731150332.png)

这个是远程运行的 Windows 98 系统：

![](https://cdn.zhangferry.com/Images/20220731145541.png)

***

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

1、[空气投篮](https://apps.apple.com/cn/app/%E7%A9%BA%E6%B0%94%E6%8A%95%E7%AF%AE/id1625289361 "空气投篮")：一款体感识别空气投篮模拟器 app。根据提示佩戴 Apple Watch，识别投篮手势动作，模拟真实的空心入网的空间音效。还有飞盘模式、巴掌模式、摩托模式等你探索。但是需要付费，价格 6 元，感兴趣的可以去体验一下。

![](https://cdn.zhangferry.com/Images/20220811223405.png)

2、[TO-D 杂志](https://2d2d.io/ "TO-D 杂志")：《TO-D 杂志》是一个专注于探讨全球 To-D 领域相关产品、创业公司、融资等资讯的开源独立杂志。To-D 即 To Developers，它并非一个独立的领域划分，它通常和 To-C, To-B 可能存在重叠。大家熟知的 Jetbrains, Postman, GitLab 等都属于 To-D 产品。

《TO-D 杂志》最早为诞生在字节跳动内部的一份名为《To-D 观察室》的飞书文档，作者从 2021 年 12 月 23 号开始编写第一篇文章，每周在内网更新。目标读者主要为字节跳动内部的工程师、产品经理和对开发者领域感兴趣的同学，并且受到大家的众多好评。后来于 2022 年 3 月 22 号开始在这里正式对外发表。

![](https://cdn.zhangferry.com/Images/20220811224205.png)

3、[dot-to-ascii](https://dot-to-ascii.ggerganov.com/ "dot-to-ascii")：Graphviz to ASCII converter using Graph::Easy。

![](https://cdn.zhangferry.com/Images/20220811224732.png)

4、[Popovers](https://github.com/aheze/Popovers "Popovers")：一个显示弹窗的库。简单、现代、可高度定制。不无聊！

![](https://cdn.zhangferry.com/Images/20220811225210.png)

5、[appsmith](https://github.com/appsmithorg/appsmith "appsmith")：一个用于构建内部工具的强大的开源框架。

![](https://cdn.zhangferry.com/Images/20220811225727.png)

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

1. 介绍两款动态图片生成器，可根据访问地址上携带的参数动态控制返回图片的大小、格式等属性，适合Mock 数据等场景；

- [placeholder](https://placeholder.com/ "placeholder")
- [dummyimage](https://dummyimage.com/ "dummyimage")

2. [iOS 16 Beta 6 发布](https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-16-release-notes "iOS 16 Beta 6 发布")： Beta 5 版本引入电量百分比，低电量会自动显示，Beta 6 改为根据配置显示。

   ![](https://cdn.zhangferry.com/Images/20220819001035.png)

3. [iPhone 14 发布日期确认](https://www.bloomberg.com/news/articles/2022-08-17/apple-targets-sept-7-for-iphone-14-launch-in-flurry-of-devices#xj4y7vzkg "iPhone14发布日期确认")：根据 Bloomberg 的报道，Apple 已经确定了 iPhone 14 的发布时间：9 月 7 号。iPhone 14 Pro有一对针孔，用于前置摄像头和FaceID扫描器。介时还会有 Macs，低端和高端的 iPad，以及三款 Apple Watch。

   ![](https://cdn.zhangferry.com/Images/20220818233911.png)

4. [karanpratapsingh - 系统设计课程](https://www.karanpratapsingh.com/courses/system-design "karanpratapsingh - 上的系统设计课程")：karan pratap singh 个人做的免费的系统设计课程，短小精悍，但涉及基础设施、数据和存储等各类知识，对此感兴趣可以看看。

5. [karanpratapsingh - 学习Go语言](https://www.karanpratapsingh.com/courses/go "karanpratapsingh 学习 GO语言")：同样来自 karan pratap singh，他本人也是 Go 语言开发者，该课程可以作为入门教程。

6. Apple 生态中内购，特别是订阅型内购是一项非常重要的获取收入的功能，随着 Apple 在订阅功能上的完善，其对应的状态也越来越多。以服务端通知类型为例其组合状态以多大数十种，那怎么区分各个状态之间的切换流程呢，这有有一张图进行了很好的总结。

   ![](https://cdn.zhangferry.com/Images/iap_subscription.png)

7. 前几天群里看到一个笑话，分享出来（手动狗头）：
	![](https://cdn.zhangferry.com/Images/20220819002542.png)

***

整理编辑：[东坡肘子](https://www.fatbobman.com)

1. [微软开源表情符 —— Fluent Emoji](https://github.com/microsoft/fluentui-emoji "微软开源图标项目 —— Fluent Emoji")：微软开源了 1800 多个表情符（持续增加中），在 Github 和 Figma 社区中均可获取。表情符提供了多种样式（ 3D、彩色、平面、高度比 ）和六种肤色。新表情符已经被用于 Teams 的最新版本之中了。

![微软开源表情符](https://cdn.zhangferry.com/Images/66-fluentui-emoji.jpg)

2. [Shortcuts.design - 快捷键大全](https://shortcuts.design "Shortcuts.design - 快捷键大全")：汇总整理了一些热门的设计、开发、效率工具的快捷键。提供了查询功能，对于跨平台产品分别提供了 Mac 和 Windows 的不同键位清单。

![快捷键大全](https://cdn.zhangferry.com/Images/66-shortcuts-design.jpg)

3. [Evil.js](https://juejin.cn/post/7134882958845935647 "Evil.js")：不知道上周是否有小伙伴因它而影响了摸鱼的时间。目前 Github 和 NPM 均已对其进行了删除。此次事件已经引发了有关投毒与反投毒的热烈讨论。

![Evil.js](https://cdn.zhangferry.com/Images/66-evil-js.jpg)

4. [猫咪插画制作](https://uchinoko-maker.jp "猫咪插画制作")：东京一家设计公司推出的网站，通过捏脸的方式制作个性猫咪插画。目前可用的选项不多，仍无法做到准确传神。可以持续关注它的后续演变。

![猫咪插画制作](https://cdn.zhangferry.com/Images/66-cat-maker.jpg)

5. [将微信删除了，为什么还占用大量的空间](https://www.bilibili.com/video/BV1UG4y1a75w?vd_source=47c38aa7a1b9837457a41f3f489f9377 "将微信删除了，为什么还占用大量的空间")：微信的删除操作只是不向你显示标记删除的记录了，记录仍然保存在你的设备中。B 站 up 主玄离199 通过视频告诉你微信中不能清理的“其他空间到底存了什么”。up 主还制作了另一条视频探讨关于微信在手机上存了什么，要怎么清理。

![将微信删除了，为什么还占用大量的空间](https://cdn.zhangferry.com/Images/66-delete-weixin-message.jpg)

***

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

1、[Superhuman 3D 捏人](https://superhuman.fun/ "3D 捏人")：Superhuman 3D character builder for your interfaces。

![](https://cdn.zhangferry.com/Images/20220901232647.png)

2、[cnchar](https://theajack.github.io/cnchar/ "cnchar")：功能全面、多端支持的汉字拼音笔画 js 库。

![](https://cdn.zhangferry.com/Images/20220901233322.png)

3、[Swifty Compiler](https://apps.apple.com/cn/app/swifty-compiler/id1544749600 "Swifty Compiler")：一个可以在 iPhone/iPad 上编写和运行 Swift 代码的 app。

![](https://cdn.zhangferry.com/Images/20220901233246.png)

4、[iStats](https://github.com/Chris911/iStats "iStats")：iStats 是一款命令行版的电脑运行状态记录工具，使用 Ruby 开发。安装和使用方式非常简单：

```
gem install iStats
```
![](https://cdn.zhangferry.com/Images/20220901225407.png)

5、[YuIndex](https://github.com/liyupi/yuindex)：一款极客范儿的浏览器主题，你可以在一个网页版的终端中完成多数需求。目前支持搜索、书签管理、音乐、todo 等功能，可以在这里体验：https://www.yuindex.com/ ：

![](https://cdn.zhangferry.com/Images/20220901230609.png)

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

介绍几个关于iOS开发国际化的工具；

- genstrings：Xcode内置工具，从指定的 C 或者 Objective-C 源文件生成 `.strings` 文件；
- ibtool：Xcode内置工具，正如 `genstrings` 作用于源代码，而 `ibtool` 作用于 `XIB` 文件；
- bartycrouch：bartycrouch 可以依据 interfaces 文件( xib 文件) 和代码(swift 、m、h 文件)来增量更新 strings 文件。在这里 增量 是指 bartycrouch 会默认保留已经翻译的值及改变了的注释；
- Poedit：Poedit 是一款基于多语言的本地化工具，支持 Win/Mac/Linux 三大主流平台，经常被用于本地化各种计算机软件；

***

整理编辑：[zhangferry](https://zhangferry.com)

1、关于升级到 iOS 16，看到有不少人反馈手机发热严重。我之前也遇到过，重启手机可以解决。如果仍未解决有可能是小组件后台请求频繁或者 App 适配问题导致的，可以关闭小组件或者等 App 适配。还有一种方案是 iOS 降级，提前下载 iOS 15 固件包，利用 iTunes 或者爱思助手进行固件安装，但这种方案有比较大的风险，不太建议。

iOS 16 升级之后，最大的变化当属锁屏小组件了，最近用到两个在锁屏组件上功能还不错的 App：[Lock Launcher](https://apps.apple.com/cn/app/id1636719674 "Lock Launcher")、[Top Widgets](https://apps.apple.com/cn/app/id1527221228 "Top Widges")。它们都可以支持在锁屏界面配置微信/支付宝健康码，还有自定义图标、多种内置跳转指令，以下是我的锁屏配置。

![](https://cdn.zhangferry.com/Images/20220921-232143.jpeg)

2、[hexclock](https://www.jacopocolo.com/hexclock/ "hexclock")：一个把当前时间作为 16 进制颜色表达的网站，当前时间 22:30:41。

![](https://cdn.zhangferry.com/Images/20220901223058.png)

3、[emojimix](https://emojimix.app/ "emojimix")：Emoji 混合网站，它可以将两个完全不同的 emoji 进行混合。下面这张可以命名为「面包猫」。

![](https://cdn.zhangferry.com/Images/20220921221449.png)

4、[能不能好好说话](https://lab.magiconch.com/nbnhhsh/ "能不能好好说话")：面对越来越多的网络缩略语，有时真是让人头大，比较常见的「yyds」、「xswl」、「awsl」还能理解，但是像「bdjw」、「jdl」就要上网去查了。这个「能不能好好说话」是[「神奇海螺试验场」](https://lab.magiconch.com/ "神奇海螺试验场")里的一个工具，这些网络缩略语含义可以从这里快速找到。

![](https://cdn.zhangferry.com/Images/20220921223040.png)

***

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1、[麦当劳-营养计算器](https://www.mcdonalds.com.cn/nutrition_calculator "麦当劳-营养计算器")：如同其提及的，这是一款计算麦当劳套餐卡路里的网页，你可以怀揣着健康饮食的心来面对你手中的汉堡和多冰可乐。

![](https://cdn.zhangferry.com/Images/nutrition_calculator.png)

2、[Wooden Fish](https://apps.apple.com/app/id1522144157 "Wooden Fish"): 木鱼-念经助手。一个模拟真实敲木鱼的App。如果你是一个虔诚的基督徒，你可以试试 [我的圣经](https://apps.apple.com/cn/app/my-holy-rosary-%E6%88%91%E7%9A%84%E5%9C%A3%E7%BB%8F-%E6%9C%89%E5%A3%B0%E8%AF%BB%E7%89%A9/id1188342937?mt=12 "我的圣经")。

![](https://cdn.zhangferry.com/Images/wooden_fish.png)

3、[Vectornator](https://www.vectornator.io "Vectornator"): 一款好用的插图绘制软件。

![](https://cdn.zhangferry.com/Images/vectornator.png)

> 官网的交互体验感觉很不错

***

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[迷宫生成器](https://www.mazegenerator.net/ "迷宫生成器")：一个可以生成多种形状、规格迷宫的网站。生成的迷宫图形可以以 PDF 的格式下载，并且会附带迷宫解法。

![image-20221013094111617](https://cdn.zhangferry.com/Images/image-20221013094111617.png)

2、[老地图查询](https://www.oldmapsonline.org/ "老地图查询")：该网站汇总了大量文献中的老地图，选择你要查询的位置，网站会列出与其相关的各个时期的老地图资料。

![image-20221013095128193](https://cdn.zhangferry.com/Images/image-20221013095128193.png)

3、[来自幽灵的数字](https://www.anumberfromtheghost.com/ "来自幽灵的数字")：Peter Adams 为自己的音乐创建的一个虚幻的空间。音乐与视觉共同营造了一个梦幻的氛围。

![image-20221013100119087](https://cdn.zhangferry.com/Images/image-20221013100119087.png)

4、[imagesTool —— 无需上传的在线图片处理服务](https://imagestool.com/zh_CN/ "imagesTool —— 无需上传的在线图片处理服务")：提供了格式转换、水印、拼接、Gif 处理、视频转 Gif 等多项功能。所有工具均使用浏览器本地技术实现，无需上传，速度更快、隐私也更有保障。

![image-20221013101815464](https://cdn.zhangferry.com/Images/image-20221013101815464.png)

5、[第一批彩色字体在谷歌字体上发布](https://material.io/blog/color-fonts-are-here "第一批彩色字体在谷歌字体上发布")：通过 COLRv1 格式，字体设计师可以设计并制作更富表现力的可定义字体。本次一共发布了九款彩色字体。Chrome、Android 和 Google 字体 API 中已经提供了对 COLRv1 格式的支持。

![1-google-font.png](https://cdn.zhangferry.com/Images/71-google-font.png)

***

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

1、[CleverToolKit](https://apps.apple.com/us/app/clevertoolkit/id6443766349?l=zh&mt=12 "CleverToolKit")：iOS 开发者辅助工具，页面简洁，体积小巧。

目前包含 json2model 功能，将 json 解析成项目中使用的 Model，支持 Swift、OC 两种语言，Swift 支持的框架包括 Codable、SwiftyJSON、HandyJSON，OC 支持的框架包括 YYModel、MJExtension。同时该功能还支持了 Xcode Editor Extension，无需打开工具在 Xcode 内部便可以实现操作，共享工具外部设置。

后续还会添加一些好用的功能到这个软件中去。

![](https://cdn.zhangferry.com/Images/20221020221106.png)

![](https://cdn.zhangferry.com/Images/20221020221117.png)

![](https://cdn.zhangferry.com/Images/WechatIMG907.png)

2、[Mac-QuickLook](https://github.com/haokaiyang/Mac-QuickLook "Mac-QuickLook")：收录了许多好用的 QuickLook 的插件和软件包。

![](https://cdn.zhangferry.com/Images/20221020210850.png)

3、[MenuBarX](https://apps.apple.com/cn/app/menubarx-%E5%BC%BA%E5%A4%A7%E7%9A%84%E8%8F%9C%E5%8D%95%E6%A0%8F%E6%B5%8F%E8%A7%88%E5%99%A8/id1575588022?mt=12 "MenuBarX")：一款强大的 Mac 菜单栏浏览器，把网页添加到菜单栏上，像原生 App 一样即开即用，为你打开 Web Apps 的新世界。

![](https://cdn.zhangferry.com/Images/20221020213844.png)

![](https://cdn.zhangferry.com/Images/20221020213939.png)

4、[SpiderCard 蜘蛛纸牌 for Mac](https://github.com/KelvinQQ/SpiderCard "SpiderCard 蜘蛛纸牌 for Mac")：仿 Windows 经典单机游戏 —— 蜘蛛纸牌。

![](https://cdn.zhangferry.com/Images/shot_1.png)

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

1、最近在写脚本，这期介绍几个帮助脚本语言接收参数更优雅的三方库；

- shell: [getoptions](https://github.com/ko1nksm/getoptions "getoptions")
- python: [python-fire](https://github.com/google/python-fire "python-fire")
- js：[commander.js](https://github.com/tj/commander.js "commander.js")
- ruby：[commander](https://github.com/commander-rb/commander "commander")

2、[原神助手 - mac端](https://github.com/zhangferry/genshin-helper "原神助手-mac端")：最近在玩原神，偶然间看到一个原神助手的工具：[vikiboss/genshin-helper](https://github.com/vikiboss/genshin-helper "vikiboss/genshin-helper")，支持原神签到、祈愿分析、游戏详细数据等功能。项目是基于 Electron 和 React 开发的，作者因为没有 mac 电脑，仅提供了windows的包。于是我 fork 了该项目，添加了 mac 版本的包，大家如果有需要可以自行下载。

祈愿分析抓取祈愿详情分析页面的链接填入即可：

![](https://cdn.zhangferry.com/Images/20221103093409.png)

3、[网页飙车](https://slowroads.io/ "网页飙车")：该游戏可以通过程序自动生成景观和道路，用户可以在这条路上驾驶，无需登录，无需安装，只有无尽的道路。

如果不想亲自开车的话，按 F 键可以打开自动驾驶，用 E 键切换自己喜欢的场景，用 C 键切换摄像头，只是看看风景，享受坐车的乐趣。

![](https://cdn.zhangferry.com/Images/20221030162820.png)

***

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1. [知识图谱](https://cnkgraph.com "知识图谱")：一个根据年历、地图、人物等生成文学图谱。关于本月的相关文献，关于本地的相关诗词，关于某地的相关文档。

没事的时候准备准备，有可能用的上。

![](https://cdn.zhangferry.com/Images/知识图谱.png)

2. [Thief](https://github.com/cteamx/Thief "Thief]"): 作者说这是**一款真正的创新摸鱼神器**。一款创新跨平台摸鱼神器，支持小说、股票、网页、视频、直播、PDF、游戏等摸鱼模式，为上班族打造的上班必备神器，使用此软件可以让上班倍感轻松，远离 ICU。
3. [iMobie M1 App Checker](https://www.imobie.com/m1-app-checker/ "iMobie M1 App Checker"): 这款应用由专注于 Apple 领域 10 年的 iMobie 团队打造，旨在为所有需要平稳过渡到苹果自研 Mx 芯片的用户提供帮助，可以实现对所有已安装 App 的 CPU 类型检测，同时提供检查 iOS 应用是否可以安装到 Mac 端。
4. [pose-monitor](github.com/linyiLYi/pose-monitor "pose-monitor"): 国内开发者在 GitHub 开源的一款 Android 应用：「PoseMon 让爷康康」，可借助 AI 技术，实时监测不良坐姿，并及时给出语音提示。应用不需要联网使用，所有 AI 特性均在手机本地运行，不需要将视频画面传输至外部服务器，仅需要摄像头权限用于获取姿态画面。
5. [顶瓜瓜](https://apps.apple.com/cn/app/id1629577265 "顶瓜瓜")：顶瓜瓜是一款检测头部位置、帮助保持坐姿的 App。将设备放在桌上，打开摄像头，即可开始坐姿守护。你会化身为一只头顶西瓜的动物，当你低头、歪头时，西瓜会掉下来。功能通过设备的原深感相机（True Depth Camera）实现，无需购买其他智能硬件，无需穿戴、无接触。无需联网，全部本地计算，保护您的隐私！

***

整理编辑：[zhangferry](https://zhangferry.com)

1、[Learn X in Y minutes](https://learnxinyminutes.com/ "Learn X in Y minutes")：这是一个用于快速学习一门编程语言或开发工具的网站。根据二八定律，一件工具，其 20% 的功能，就能满足 80% 的需求。所以打算初尝一门编程语言，最佳的方式就是先了解那20%最重要的功能，这个网站的目的就在于此。

2、[我用400天，做了一款让所有人免费商用的开源字体](https://www.bilibili.com/video/BV1sP411g7PZ "我用400天，做了一款让所有人免费商用的开源字体")：这是B站up主 [oooooohmygosh](https://space.bilibili.com/38053181) 的一期视频，讲述自己用 400 天时间一直在做的一款开源字体，开源地址：[smiley-sans](https://github.com/atelier-anchor/smiley-sans "smiley-sans")。我们都知道代码是可以被开源的，但其实字体也是能够开源的。国内大部分字体都是在已有开源字体基础上进行的二次修改，从零开始设计一款字体的人则非常少。因为这代表着需要考虑整个字体的风格统一性，英文还好，中文汉字那么多，想想都是一个巨大的工程。而且得意黑还支持了泛欧陆、越南文在内的100多种语言，真的很强。

虽然会很辛苦，视频中更多感受到的却是作者和一起协作的小伙伴的创作热情，大家都认为这是一件有意义的事，相信这件事能帮助到更多的人，所以做起来也乐此不疲。这才是开源精神啊。

![](https://cdn.zhangferry.com/Images/20221116233128.png)

3、[isowords](https://github.com/pointfreeco/isowords "isowords")：一款开源的单词游戏项目，用 SwiftUI 开发，可以用来学习用 SwiftUI 做完整项目的话可以如何设计。

![](https://cdn.zhangferry.com/Images/20221116235723.png)

4、[interview warmup](https://grow.google/certificates/interview-warmup/ "interview warmup")：Google 推出的一个能够模拟面试的网站，你需要提前告诉它你是做什么的，然后 AI 会根据你的回答自动生成几道题。回答过程会全程录音，然后根据结果给你打分，还会提一些建议。你也可以反复练习，以提高面试能力。

![](https://cdn.zhangferry.com/Images/20221117000646.png)

5、[DumpApp](https://www.dumpapp.com/ "DumpApp")：一个专注于 iOS 应用砸壳和签名的网站，还提供企业签，个人签等服务，有些内容需要付费。

***

整理编辑：[zhangferry](https://zhangferry.com)

1、[Combine operators cheat sheet](https://tanaschita.com/20221121-cheatsheet-combine-operators/ "Combine operators cheat sheet")：Combine 里有很多操作符，这些操作符很多并不能通过命名就完全区分出来，那该如何记忆和理解这些操作符的含义呢，tanaschita 用 SwiftUI 实现了这些操作符的可视化表达。如果你看过 RxSwift 的文档应该对这些图标非常亲切。

![](https://cdn.zhangferry.com/Images/20221124201158.png)

2、[Session, cookie, token, JWT, SSO 和 OAuth 2.0 是什么](https://twitter.com/alexxubyte/status/1595455518583029764 "Session, cookie, token, JWT, SSO 和 OAuth 2.0 是什么")：这几种常用的身份校验技术有什么区别呢， Alex Xu 做了这样一张图用于解释它们的区别以及用于解决的问题。

![](https://cdn.zhangferry.com/Images/20221124205007.png)

3、[电脑端微信不断写日志](https://v.douyin.com/rVWRmUG/ "微信在电脑不断写日志")：来源于抖音一位技术博主的视频，详细描述了微信在电脑端不断写日志的过程。利用 Xcode 的 Instruments 里的 File Activity，采集微信在后台的文件读取记录。会发现很多 xlog 日志的生成，但因为文件是加密的，我们并不能解析里面是什么内容。我看了我电脑里的日志，有三天我的电脑都是没有打开的，但是却能找到这几天的 xlog 日志，也就是说即使是休眠状态，微信依然在尝试写东西。该日志并非完全本地，还会通过网络进行上传。目前关于这些数据是做什么的还没有查到任何相关资料。

如果你感觉不放心，可以通过这种方式，关闭日志写权限：

```bash
$ sudo chmod 400 ~/Library/Containers/com.tencent.xinWeChat/Data/Library/Caches/com.tencent.xinWeChat/2.0b4.0.9/log
```

4、对于新技术很多开发都会抑制不住想去尝试，比如 SwiftUI，当你有这种想法时你可能会理解这张图的含义。

![](https://cdn.zhangferry.com/Images/20221124205551.png)

5、[Github 推出的两种开源字体 mona & hubot sans](https://github.com/mona-sans "Github 推出的两种开源字体 mona & hubot sans")：这是一种强大而通用的字体，以Degarism风格设计，灵感来源于工业时代的怪诞风格。Mona Sans在产品、网络和印刷领域都很有效。Hubot Sans 字体更修长，有一种独特的技术感。

![](https://cdn.zhangferry.com/Images/20221124211158.png)

6、[Moyu.Games](https://moyu.games/ "摸鱼游戏")：一个站点聚合网站，一直工作也挺累的，偶尔摸摸鱼吧。

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

1. 最近CSDN上线的一款新工具箱应用-- [猿如意](https://devbit.csdn.net/ "猿如意")，内置一些好用的效率工具；

![猿如意](http://cdn.zhangferry.com/20221201180541.png)

类似的工具还有 [uTools](https://www.u.tools/ "uTools")

![uTools](http://cdn.zhangferry.com/20221201181157.png)

2. [来个电话](https://apps.apple.com/cn/app/%E6%9D%A5%E4%B8%AA%E7%94%B5%E8%AF%9D-%E5%81%87%E6%9D%A5%E7%94%B5%E8%AE%A9%E4%BD%A0%E8%84%B1%E8%BA%AB%E8%A7%A3%E5%9B%B4/id985946832 "来个电话") 是一款可以帮助你从无聊的无意义社交中脱身解围的应用。不仅是精确到分钟的来电时间，还一比一仿真了系统的来电界面，当你耳朵贴近手机时也会自动熄灭屏幕，让你能毫无破绽、以假乱真的离开无聊的聚会。原价 12 元，目前限免中。设置界面如下：

    ![](https://cdn.zhangferry.com/Images/weekly_77_moyu_1.png)

3、[CampusShame](https://github.com/forthespada/CampusShame "CampusShame")：Github 上总结的校招污点和非污点公司名单。校招污点行为**包括**但不限于：毁意向书、毁两方协定、毁三方协定、试用期裁员、大量裁应届生。

4、[Roadmap.sh](https://roadmap.sh/ "Roadmap.sh")：这是一个致力于帮助开发者学习和选择的社区，这里提供了很多岗位的 Roadmap 和优质学习资料。

![](https://cdn.zhangferry.com/Images/20221201233541.png)

5、[email 是如何工作的？](https://twitter.com/alexxubyte/status/1593637888834473984 "email 是如何工作的？")：这张图描述了邮件服务的工作原理。

![](https://cdn.zhangferry.com/Images/20221202000720.png)

邮件服务主要有两套协议组成，一个是 SMTP 用于存储邮件内容，一个是 IMAP/POP 用于拉取邮件内容，对于不同的邮件服务，会由接收方进行发送，这里用的是 SMTP 协议。

6、[正则表达式速查卡](https://twitter.com/linuxtoy/status/1597754607697948673 "正则表达式速查卡")：正则表达式是一种很实用的文本模式匹配语言，Linuxtoy 总结了这份速查卡。

![](https://cdn.zhangferry.com/Images/20221202002037.png)

***

整理编辑：[Mim0sa](https://juejin.cn/user/1433418892590136/posts)

1. Apple 官方放出的 [Stable Diffusion with Core ML on Apple Silicon ](https://machinelearning.apple.com/research/stable-diffusion-coreml-apple-silicon "Stable Diffusion with Core ML on Apple Silicon")，你现在可以在 Apple 的平台上以 CoreML 的形式运行 Stable Diffusion 了。

   ![sd_apple](https://cdn.zhangferry.com/Images/sd_apple.jpg)

2. 一个很棒的配色网站 [randoma11y](https://randoma11y.com/ "randoma11y")，可以无限生成配色组合。

   ![randoma11yImg](https://cdn.zhangferry.com/Images/randoma11yImg.png)

3. [purrli](https://purrli.com/ "purrli") 一个可以听猫咪不同状态声音的网站。

   ![purrliImg](https://cdn.zhangferry.com/Images/purrliImg.png)

4. [dotown](https://dotown.maeda-design-room.net/ "dotown") 一个由前任天堂设计师的创意团队建立的像素风格的透明素材网站，这些素材的都使用尽可能低的分辨率进行抽象的点阵表达，风格一致，充满怀旧游戏氛围，极具特色。

   ![dotownImg](https://cdn.zhangferry.com/Images/dotownImg.png)

5. 一份在 Webstorm 中配置 Touchbar 的[指南](https://juejin.cn/post/7174175965113745416 "指南")。

6. [赛百味的台湾官网](https://subway.com.tw/GoWeb2/include/meals-nutrition.html "赛百味的台湾官网")有所有三明治的营养信息，虽然产品略有不同但有需要的话也可以参考一下。

   ![subwayImg](https://cdn.zhangferry.com/Images/subwayImg.png)


***

整理编辑：[zhangferry](zhangferry.com)

1、[【深度解读】喧嚣过后，再来聊聊灵动岛](https://www.bilibili.com/video/BV1W14y1N7MY "【深度解读】喧嚣过后，再来聊聊灵动岛")：这是ZEALER官方频道的一期视频，作者从 Apple 的开发者文档和UI交互的深层用意两方面去考虑灵动岛的设计意图。灵动岛的主要作用是「补上了iOS高频更新信息管理缺失的一环」，由此也延伸出了几个观点：

* 微信消息不可能适配灵动岛
* 灵动岛未来不会成为多任务的入口

2、[Hello 算法](https://www.hello-algo.com/ "Hello 算法")：「如果您是 **算法初学者**，完全没有接触过算法，或者已经有少量刷题，对数据结构与算法有朦胧的理解，在会与不会之间反复横跳，那么这本书就是为您而写！」这本书第一作者是 Krahets，力扣全网阅读量最高博主。 他曾经求职也踩过算法的雷，于是就有了后来的发愤图强，并写作这本面相初学者的算法小书。

![](https://cdn.zhangferry.com/Images/20221216000024.png)

3、[那些独立开发者（非外包）都是怎么养活自己的](https://www.v2ex.com/t/900741 "哪些独立开发者都是怎么养活自己的")：来自 V2EX 上的一个帖子，评论区有很多独立开发者的项目。我们可以发现一些有趣的独立项目，同时也能看到一些独立开发者的生活状态，这条路不那么容易走。如果你向往独立开发的话，也可以了解他们遇到的问题。

4、[新冠病毒感染者居家预防治疗指南](https://docs.qq.com/doc/DTVZTdENJbnhWaFpQ "新冠病毒感染者居家预防治疗指南")：随着防疫政策的放开，身边有越来越多的人🐑了，🐑了该如何应对？这份在线文档综合多份机构的新冠治疗指南汇总制作而成，比如什么症状应该用什么药？跟自己同住的人应该如何防护？如何消杀？儿童、孕妇被感染应该如何处理？去医院就诊应该注意什么情况？另外还提供了很多中医和饮食相关的注意事项。


***

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

1、[A Tour in the Wonderland of Math with Python](https://github.com/neozhaoliang/pywonderland "A Tour in the Wonderland of Math with Python") 通过渲染高质量的图像、视频和动画来展示数学之美。

![](https://cdn.zhangferry.com/Images/125026787-dad59700-e0b7-11eb-889f-b0c737413b6a.png)

2、[MindForger](https://www.mindforger.com/#home "MindForger")，是一款个人知识管理工具

![](https://cdn.zhangferry.com/Images/1-title-screen.jpg)

MindForger的目标是模仿人类的思维--学习、回忆、识别、联想、遗忘--以实现与你的思维的协同，使你的搜索、阅读和写作更有效率。

不仅如此，MindForger 尊重隐私，并确保知识安全。

不仅仅是一个markdown 编辑器，更是一个辅助的智能助手。

3、[LearnGPT](https://www.learngpt.com/ "LearnGPT")：ChatGPT 是一个非常强大的工具，但对于它能做什么我们大多数情况还是随便想一些问题或者通过其他人发的测试样例进行了解。为了大家更方便了解 ChatGPT，这个网站专门收集了跟 ChatGPT 对话产生的有意思的问题。

![](https://cdn.zhangferry.com/Images/20221229225526.png)

4、[Open Source Software Insight](https://ossinsight.io/ "Open Source Software Insight")：一个洞悉开源软件的网站，从非常多的维度总结了当前开源软件的趋势，还可以以数据视角去了解仓库和开发者的各类信息，主要数据来源为 Github。

![](https://cdn.zhangferry.com/Images/20221229231811.png)

![](https://cdn.zhangferry.com/Images/20221229231119.png)

5、[Twitter - 今年你阅读过的，或者学习到的最有趣的内容是什么](https://twitter.com/github/status/1608134934891270147 "Twitter")：来自 Github 官方推文，评论区有很多优质的内容。

***

整理编辑：[CoderStar](https://mp.weixin.qq.com/mp/homepage?__biz=MzU4NjQ5NDYxNg==&hid=1&sn=659c56a4ceebb37b1824979522adbb15&scene=18)

1、[openwrite](https://openwrite.cn/ "openwrite") 提供了基于`MarkDown`的写作工具以及一文多发的工具，适合需要做新媒体矩阵的程序员。

![](http://cdn.zhangferry.com/20230112163018.png)

2、[Asimov](https://github.com/stevegrunwell/asimov "Asimov")  自动检查本地磁盘把开发依赖的文件包全部从 TimeMachine 移出掉的好用工具。

3、[Github Trends](https://www.githubtrends.io/wrapped "Github Trends")：一个 Github 图标统计工具，需要首先给仓库 Star 你才能用这个功能。

![](https://cdn.zhangferry.com/Images/github-wrapped.png)

4、[开源软件指南](https://opensource.guide/ "开源软件指南")：关于开源软件的一份指南，如何向开源软件共享，如何做自己的开源软件，如何围绕开源做社区，还有这些环节的最佳实践。

![](https://cdn.zhangferry.com/Images/20230112223404.png)

5、[AI-powered code review](https://codeball.ai/ "AI-powered code review")：AI 加持的 Code review 工具，对于开源软件是免费的，目前使用形式是基于 Github Action。

![](https://cdn.zhangferry.com/Images/20230112225337.png)

## 本周学习

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


***

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


***

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### 基础知识回顾：iOS 中的 const 修饰符

`const` 修饰符将其后的变量设置为常量，`const` 在 \* 之前和 \* 之后的区别在于，常量指针是否可以指向其他的 内存块。以 iOS 中的字符串为例：

#### NSString

```objective-c
NSString *const str1 = @"str1";
// str1 = @"str1***str1"; //报错:Cannot assign to variable 'str1' with const-qualified type 'NSString *const __strong'
```

如示例所示，常量指针已经指向 `@"str1"` ，不能再指向其他的内存 `@"str1***str1"` ，因此不能修改常量指针指向的内容，常量指针仍然指向原内存中的内容。因为是 `NSString` ，所以改变指针指向的内存，才能改变指针指向的内容，常量指针指向的内存不变，所指向的内容就不会变。

当 `const`修饰了 \* 时，常量指针可以指向其他的内存，释放掉原来的内存，从而可以修改常量指针指向的内容(因为指向的内存变了)：

```objective-c
NSString const *str2 = @"str2";
str2 = @"str2***str2";
```

#### NSMutableString

如果把 `NSString` 换成 `NSMutableString` 情况就不一样了。以下示例可以修改原内存中的内容，也可以指向其他的内存：

```objective-c
NSMutableString const *var1 = [@"str" mutableCopy]; 
[var1 appendString:@"__var"]; // 改变内存中的内容
var1 = [@"123" mutableCopy]; // var1指向新的内存 NSLog(@"var1:%@",var1);
```

而当 `const` 修饰 \* 时可以修改原内存中的内容，但是不能指向其他的内存:

```objective-c
NSMutableString *const var2 = [@"str" mutableCopy];
[var2 appendString:@"__var"];//改变内存中的内容
var2 = [@"123" mutableCopy];//var2不能指向新的内存，报错:Cannot assign to variable 'var2' with
const-qualified type 'NSMutableString *const __strong'
    NSLog(@"var2:%@", var2);
```


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

***
整理编辑：[皮拉夫大王在此](https://juejin.cn/user/281104094332653)

> 本期优秀博客的主题为：ARM64 汇编入门及应用。汇编代码对于我们大多数开发者来说是既熟悉又陌生的领域，在日常开发过程中我们经常会遇到汇编，所以很熟悉。但是我们遇到汇编后，大多数人可能并不了解汇编代码做了什么，也不知道能利用汇编代码解决什么问题而常常选择忽略，因此汇编代码又是陌生的。本期博客我搜集了 3 套汇编系列教程，跟大家一道进入 ARM64 的汇编世界。
>
> **阅读学习后我将获得什么？**
>
> 完整阅读三套学习教程后，我们可以阅读一些逻辑简单的汇编代码，更重要的是多了一种针对疑难 bug 的排查手段。
>
> **需要基础吗？**
>
> 我对汇编掌握的并不多，在阅读和学期过程期间发现那些需要思考和理解的内容，作者们都介绍的很好。

1、[[C in ASM(ARM64)]](https://zhuanlan.zhihu.com/p/31168062 "[C in ASM(ARM64)]") -- 来自知乎：知兵

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：推荐先阅读此系列文章。作者从语法角度解释源码与汇编的关系，例如数组相关的汇编代码是什么样子？结构体相关的汇编代码又是什么样子。阅读后我们可以对栈有一定的理解，并且能够阅读不太复杂的汇编代码，并能结合指令集说明将一些人工源码翻译成汇编代码。

2、[iOS汇编入门教程](https://juejin.cn/post/6844903576855117831 "iOS汇编入门教程") -- 来自掘金：Soulghost

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：页师傅出品经典教程。相对前一系列文章来说，更多地从 iOS 开发者的角度去看到和应用汇编，例如如何利用汇编代码分析 NSClassFromString 的实现。文章整体的深度也有所加深，如果读者有一定的汇编基础，可以从该系列文章开始阅读。

3、[深入iOS系统底层系列文章目录](https://juejin.cn/post/6844903847027015694 "深入iOS系统底层系列文章目录") -- 来自掘金：欧阳大哥2013

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：非常全面且深入的底层相关文章集合。有了前两篇文章的铺垫，可以阅读该系列文章做下拓展。另外作者还在 [深入iOS系统底层之crash解决方法](https://juejin.cn/post/6844903670404874254 "深入iOS系统底层之crash解决方法") 文章中一步步带领我们利用汇编代码排查野指针问题。作为初学者我们可以快速感受到收益。

***
整理编辑：[@我是熊大](https://github.com/Tliens)

> 本期优秀博客的主题为：脚手架/CLI。在项目最开始的时候，脚手架工具，就会帮你搭建好架子，并生成一些基本代码。脚手架的存在有利于团队统一架构风格，加速项目开发。

1、[从0构建自己的脚手架/CLI知识体系](https://juejin.cn/post/6966119324478079007 "从0构建自己的脚手架/CLI知识体系") -- 来自掘金：IT老班长

[@我是熊大](https://github.com/Tliens)：如何生成搭建脚手架呢？本文作者使用 NodeJS，从0开始搭建了一个脚手架，每一步都很详细，介绍了热门脚手架工具库，没有 NodeJS 基础的也能看懂，非常适合作为新手篇入场学习。

2、[iOS自动化工具Gckit CLI](https://seongbrave.github.io/gckit/guide/#%E6%B5%81%E7%A8%8B%E8%AF%B4%E6%98%8E "iOS自动化工具Gckit CLI") -- 来自博客：SeongBrave

[@我是熊大](https://github.com/Tliens)：在项目开发中，大家水平参差不齐，代码风格迥异，尤其是有新人加入团队时，适应期会比较长。那有没有可能让新同学也能像老同学一样，不仅快速进行开发，而且代码风格也近似呢？Gckit CLI 就是为此诞生的，大家在看完上篇文章后就可以对该库进行调整了，打造属于自己的自动化工具


3、[Swift + RxSwift MVVM 模块化项目实践](https://juejin.cn/post/6844903821160742919 "Swift + RxSwift MVVM 模块化项目实践") -- 来自掘金：SeongBrave

[@我是熊大](https://github.com/Tliens)：本文是 Gckit 作者的实践总结，主要讲解通过 CocoaPods 结合 Gckit-CLI 实现开发效率的最大化的一些项目实践。


4、[iOS自动化方案附脚本](https://juejin.cn/post/6948239939809050638 "iOS自动化方案附脚本") -- 来自掘金：我是熊大

[@我是熊大](https://github.com/Tliens)：不同的电脑开发环境不同，多人协作下，因环境不同会导致各种问题，比如 CocoaPods 的版本不同，就会导致某些库无法下载，.lock文件频繁更新等。本文介绍了如何统一开发环境，以及自动化脚本的使用，可以把它放进你的脚手架工具中。文章最后提到了关于脚手架工具的遐想。

***

> 转眼间 SwiftUI 已推出接近 3 年。越来越多的开发者尝试使用 SwiftUI 来构建其应用。本期介绍的博文将更多地涉及 SwiftUI 的进阶技巧，帮助开发者对 SwiftUI 有更加深入的认识和理解。

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[无法解释的 SwiftUI —— SwiftUI 的编程语言本质](https://wezzard.com/post/2022/03/unexplained-swiftui-the-programming-language-nature-of-swiftui-d20e "Unexplained SwiftUI - The Programming Language Nature of SwiftUI") -- 来自：WeZZard

[@东坡肘子](https://www.fatbobman.com/)：作者 WeZZard 从一个十分新颖的角度来看待、分析 SwiftUI。通过一个斐波纳契数示例，来展示 SwiftUI 的图灵完整性，进而提出一个有趣的观点——SwiftUI 是一种编程语言，而不是 UI 框架。

2、[SwiftUI 底层：可变视图](https://movingparts.io/variadic-views-in-swiftui "SwiftUI under the Hood: Variadic Views") -- 来自：The Moving Parts Team

[@东坡肘子](https://www.fatbobman.com/)：本文介绍了一些 View 协议中尚未公开的 API。通过使用这些 API，开发者可以编写出更加强大、灵活，且与原生实现类似的容器，构建自己的布局逻辑。作者 Moving Parts 团队当前正在开发一个功能强大的 SwiftUI 组件库。

3、[了解 SwiftUI 如何以及何时决定重绘视图](https://www.donnywals.com/understanding-how-and-when-swiftui-decides-to-redraw-views/ "Understanding how and when SwiftUI decides to redraw views") -- 来自：Donny Wals

[@东坡肘子](https://www.fatbobman.com/)：作者通过观察和实践，尝试了解和总结 SwiftUI 中对视图重绘的规律。尽管该文没有给出内部实现的具体证明，但沿着作者的测试路径，读者依然可以从中获取到相当宝贵的经验。

4、[了解 SwiftUI 的 onChange](https://www.fatbobman.com/posts/onChange/ "了解 SwiftUI 的 onChange") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：onChange 是从 SwiftUI 2.0 后提供的功能，可以将其作为另一种驱动视图重绘的手段。本文将对 onChange 的特点、用法、注意事项以及替代方案做以详细介绍。结合上文「了解 SwiftUI 如何以及何时决定重绘视图」以及「SwiftUI 视图的生命周期研究」一文，可以对视图的计算、布局、绘制有更深入的了解。

5、[谁说我们不能对 SwiftUI 视图进行单元测试？](https://nalexn.github.io/swiftui-unit-testing/ "Who said we cannot unit test SwiftUI views?") -- 来自：Alexey Naumov

[@东坡肘子](https://www.fatbobman.com/)：因为很难构建依赖和运行环境，对 SwiftUI 视图进行单元测试是十分困难的。Alexey Naumov 是著名的 SwiftUI 测试框架 ViewInspector 的作者，本文介绍了他在创建 ViewInspector 框架背后的故事，其中有关获取 SwiftUI 黑盒中秘密的思路和途径十分值得借鉴。

6、[高级 SwiftUI 动画 1-5](https://mp.weixin.qq.com/s/5KinQfNtcovf_451UGwLQQ "高级 SwiftUI 动画") -- 来自：Javier 中文版：Swift 君

[@东坡肘子](https://www.fatbobman.com/)：仅需少量的代码，SwiftUI 即可为开发者实现相当优秀的动画效果。但如果想创建更加炫酷、灵活、高效的动画则需要掌握更多的知识和高级技巧。本系列文章已持续更新 2 年之久（SwiftUI 诞生至今不到 3 年），详细讲解了各种有关 SwiftUI 高级动画的内容。

***

整理编辑：皮拉夫大王在此

> 本期优秀博客主题相对轻松，聊聊面试相关和成长相关的事情。本来想借助本期内容整理下 `rebase` & ` bind ` 的相关技术细节，但是这周被某些自媒体散布的裁员消息给刷屏了，恰巧我本人也是在最近换了工作，因此借助这个机会和大家一起暂停下技术学习的脚步，抬头看看外面的情况。
>
> **阅读后你将获得什么？**
>
> - 如果你在犹豫自己是不是该换工作，那么可以从文章中找到部分答案；
> - 东野浪子和苍耳两位大佬是非常资深的大厂面试官，他们的建议是非常中肯的；
> - 我本人近期面试的一些细节；
> - 尽管不认同面试问八股文，但是还是给大家准备了八股集合，以供大家增强面试信心；


1、**如果你在犹豫期，请看下文**

1.1 [浅谈如何理性的判断自己是否应该换工作](https://mp.weixin.qq.com/s/h5G7LCCAPPh6GfwvRHhkOw) -- 来公众号：东野职场派

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：去年推荐过这篇文章，考虑到目前是金三银四，有些同学可能之前没有看过，因此再推荐一次。

2、**面试官篇：知己知彼，面试官的关注点**

2.1 [给面试者的一些建议](https://djs66256.github.io/2021/12/22/2021-12-22-%E7%BB%99%E9%9D%A2%E8%AF%95%E8%80%85%E7%9A%84%E4%B8%80%E4%BA%9B%E5%BB%BA%E8%AE%AE/#more "给面试者的一些建议") -- 来自：苍耳的技术博客

2.2 [面试过500+位候选人之后，想谈谈面试官视角的一些期待](https://mp.weixin.qq.com/s/kv-_oZObp7QRHeAbrkdfsA) -- 来公众号：东野职场派

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：以上两篇文章的观点本质上来说是一致的，面试官期望候选人是在平时工作中是有所思考和行动的人，而不是临时抱佛脚去应试。**因此用半年时间去刷题复习基础知识，不如用这个时间去认真打磨一个项目**。

3、**候选人篇：近期面试的一些细节**

3.1 [刚换工作，说点找工作相关的事情~](https://mp.weixin.qq.com/s/0BTRFr4m5FGH3fztIMkmVw) -- 来自公众号：皮拉夫大王在此

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：这是我本人近期的亲身经历，前段时间和几个朋友聊了聊换工作的事情。包括：该走该留？如何准备？如何写简历？如何投简历？面试中和面试后各有哪些问题？等等

4、**最全基础知识整理**

4.1 [《史上最全iOS八股文面试题》2022年](https://blog.51cto.com/u_15068388/5076104 "《史上最全iOS八股文面试题》2022年") -- 来自51CTO：宇夜iOS 

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：面试中多多少少会考察到部分基础知识，对基础不放心的同学可以看看。

***

整理编辑：[@我是熊大](https://github.com/Tliens)

> 本期优秀博客的主题为：程序员如何自我提升。学习前辈们的经验，找到适合自己的路径。

1、[程序员如何在业余时间提升自己](https://juejin.cn/post/6995079191548936223 "程序员如何在业余时间提升自己") -- 来自掘金：阿里巴巴大淘宝技术

[@我是熊大](https://github.com/Tliens)：工作本身就很忙碌，如何在繁忙的工作中利用碎片化时间学习或是做自己感兴趣的事情，来自4名淘系技术的工程师的分享。

2、[阿里毕玄：程序员如何提升自己的硬实力](https://segmentfault.com/a/1190000018005178 "阿里毕玄：程序员如何提升自己的硬实力") -- 来自segmentfault：阿里云云栖号

[@我是熊大](https://github.com/Tliens)：作者从生物专业转到程序员，从业余程序员到职业程序员。

3、[如何提升你的能力？给年轻程序员的几条建议](https://tech.glowing.com/cn/advices-to-junior-developers "如何提升你的能力？给年轻程序员的几条建议") -- 来自Glow 技术团队博客

[@我是熊大](https://github.com/Tliens)：作者前后服务于NVIDIA、Google、Slide、Glow。在Glow，作者的个人的工作也从Developer，Tech Lead，Engineering Manager到CTO，他的看法可能会更全面。

4、[程序员一定会有35岁危机吗](https://juejin.cn/post/7012542827204706318 "程序员一定会有35岁危机吗") -- 来自掘金：黄轶

[@我是熊大](https://github.com/Tliens)：一个资深架构师的分享，正如他所说，企业并不是排斥大龄程序员，而是排斥能力与自己工龄不匹配的大龄程序员。

***

> 本期将整理一些有关最近发布的 Swift 5.6 和 Xcode 13.3 的新特性和新功能的博文。

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[Swift 5.6 新特性](https://juejin.cn/post/7077369199626027039 "Swift 5.6 新特性") -- 来自掘金：YungFan

[@东坡肘子](https://www.fatbobman.com/)：Swift 5.6 为该语言引入了一系列新的特性，同时为了协助开发者顺利地过渡至 Swift 6 而完善了部分其他功能。本文对 Swift 5.6 的新特性进行了介绍。另外，在 Swift 每次升级后，hackingwithswift.com 都会有专文介绍新添加的内容，感兴趣的朋友可以持续关注。

2、[Swift 5.6 SE-0335 Introduce existential any 的理解](https://juejin.cn/post/7078192732635676680 "Swift 5.6 SE-0335 Introduce existential any 的理解") -- 来自掘金：赤脊山的豺狼人

[@东坡肘子](https://www.fatbobman.com/)：在Swift 5.6 的新功能中，引入了一个新的关键字 any 来标记 existential type。这种变化有可能在未来破坏现有代码，使其在 Swift 6 中会出现兼容性问题。所有的 Swift 开发者都应及时对其有所了解。本文的作者将对 any 的用法和存在的理由进行介绍和探讨。

3、[在GitHub页面上将DocC文档作为静态网站发布](https://www.createwithswift.com/publishing-docc-documention-as-a-static-website-on-github-pages/ "Publishing DocC Documentation as a Static Website on GitHub Pages") -- 来自：Moritz Philip Recke

[@东坡肘子](https://www.fatbobman.com/)：Swift 5.6 为 Swift Package Manager 实现了可扩展的构建工具（SE-0303）及其扩展命令插件（SE-0332）等功能。本教程展示了如何利用新功能生成 DocC 文档，并将其处理为可静态托管的文档。

4、[Xcode 13.3 添加了在私有存储库中使用 SPM 二进制依赖项的能力](https://blog.eidinger.info/xcode-133-supports-spm-binary-dependency-in-private-github-release "Xcode 13.3 supports SPM binary dependency in private GitHub release") -- 来自：Marco Eidinger

[@东坡肘子](https://www.fatbobman.com/)：无法通过二进制发布库是阻碍开发者全面转向 Swift Package Manager 的一个重要因素。在 Xcode 12 中添加了XCFramework ，使得二进制发布得以可能。Xcode 13.3 再接再厉，增加了 XCFramework 对私有存储库的支持。开发者通过在开发私有的闭源库时将其代码作为二进制文件提供，以进一步保护其知识产权。

5、[Swift异步算法介绍](https://www.swift.org/blog/swift-async-algorithms/ "Swift异步算法介绍") -- 来自：Tony Parker

[@东坡肘子](https://www.fatbobman.com/)：Swift 5.5 为 Swift 带来了全新的异步开发体验。近日，苹果公开了跨平台开源项目 Swift Async Algorithms，为开发者提供了更加自然、高效地处理异步序列的能力。该库需要 Swift 5.6 的支持。

***

整理编辑：皮拉夫大王在此

> 本期优秀博客主题为重新了解`rebase` & ` bind` 。前段时间字节发了篇关于iOS 15`fixup-chain`机制的相关文章，其中`rebase`机制引起了大家热烈的讨论。在讨论的过程中，包括我在内的部分同学纠正了之前对`rebase`的错误认识，因此有必要跟大家一块再来学习下`rebase` & ` bind`
>
> **在阅读之前，先来问几个问题：**
>
> - `reabse` 时会修改TEXT段的数据吗？如果不修改，那静态链接时还不知道ASLR后的真实地址难道不需要通过rebase修正吗？如果要修改，TEXT段不是只读段吗，为什么可以修改呢？
> - iOS 15之前的`fixup-chain`机制与之前的`rebase` & ` bind`有何不同？
>
> 如果你想真正了解`rebase` & ` bind`机制，那么这两个问题要弄清楚。

1、**复习iOS的rebase和bind**

1.1 [深入理解 Symbol](https://mp.weixin.qq.com/s/uss-RFgWhIIPc6JPqymsNg) -- 来自公众号：小集

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：在了解rebase和bind之前必须要了解iOS的符号，符号是bind的桥梁。文章中对符号的介绍比较详细，包含之前很少提到的lazy symbol，weak symbol等。

1.2 [给实习生讲明白 Lazy/Non-lazy Binding](https://juejin.cn/post/7001842254495268877 "给实习生讲明白 Lazy/Non-lazy Binding") -- 来自掘金：No

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：这篇文章是对bind讲解的浅显易懂，非常适合之前不了解bind的同学阅读。

1.3 [图解 Mach-O 中的 got](https://juejin.cn/post/6918645161303998478 "图解 Mach-O 中的 got") -- 来自掘金：微微笑的蜗牛

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：这篇文章也是介绍相关知识的，可以补充阅读。

2、**关于iOS15的fixup机制**

2.1  [iOS 15 如何让你的应用启动更快]( https://juejin.cn/post/6978750428632580110 "iOS 15 如何让你的应用启动更快") -- 来自掘金：ZacJi

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：iOS15的fixup介绍将主要通过三篇文章，逐次加深深度。阅读这篇文章后，大家应该要弄清楚作者所说的启动加速的原因，以及与二进制重排是否有关系。

2.2 [从野指针探测到对iOS 15 bind 的探索](https://mp.weixin.qq.com/s/BNIWBwemmz4isbjBb9-pnQ) -- 来自公众号：皮拉夫大王在此

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：在阅读了《iOS 15 如何让你的应用启动更快》，进一步探索了bind机制并且加以应用。

2.3 [iOS15 动态链接 fixup chain 原理详解](https://mp.weixin.qq.com/s/k_RI2in_Q5hwT33KWig34A) -- 来自公众号：字节跳动终端技术

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：更加完善地介绍iOS 15的fixup机制。


***

整理编辑：[@我是熊大](https://github.com/Tliens)

> 本期优秀博客的主题为：iOS 内购。

1、[iOS内购详解](https://juejin.cn/post/7029252038252822564 "iOS内购详解") -- 来自掘金：QiShare

[@我是熊大](https://github.com/Tliens)：本文是QiShare针对内购写的一篇文章，包含了内购前的准备、内购流程、恢复购买、内购掉单等内容。

2、[iOS内购（IAP）自动续订订阅类型总结](https://www.jianshu.com/p/9531a85ba165 "iOS内购（IAP）自动续订订阅类型总结") -- 来自简书：凡几多

[@我是熊大](https://github.com/Tliens)：本文主要介绍自动订阅的相关情况。自动续期订阅与其他的购买不同，是比较复杂的一种情况。自动续期订阅类型是有连续性的，其中还有免费试用期、促销期、宽限期的概念。用户还可以取消续订，恢复续订等，这无疑又增加了复杂性。

3、[iOS项目技术还债之路《二》IAP掉单优化](https://juejin.cn/post/6844904021229060103 "iOS项目技术还债之路《二》IAP掉单优化") -- 来自掘金：njuxjy

[@我是熊大](https://github.com/Tliens)：IAP掉单一定是大多数开发者不可避免的问题，作者针对掉单情况做了非常详细的总结，如果你也正有类似的问题，推荐阅读。

4、[苹果iOS内购三步曲：App内退款、历史订单查询、绑定用户防掉单！--- WWDC21](https://juejin.cn/post/6974733392260644895 "苹果iOS内购三步曲：App内退款、历史订单查询、绑定用户防掉单！--- WWDC21") -- 来自掘金：37手游iOS技术运营团队

[@我是熊大](https://github.com/Tliens)：本文是基于WWDC21的总结，介绍了最新的内购情况，StoreKit 2的出现让内购更简单。惊喜的是：客户端已经支持用户退款了。

5、[SwiftyStoreKit](https://github.com/bizz84/SwiftyStoreKit "SwiftyStoreKit") -- 来自SwiftyStoreKit

[@我是熊大](https://github.com/Tliens)：一个star高达5.9k的开源库，支持内购查询、购买、校验、结束交易等。api简洁易懂，能帮助你在项目中快速接入内购，美中不足的是不支持订单退订，这还需要自己开发。

***

> 本期将介绍一些有特点的中文技术博客。虽然其中大多的内容与 iOS 或 Swift 关系不大，但对于开扩视野、了解其他领域的动态很有帮助。

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[漩涡的博客](https://xuanwo.io "漩涡的博客") -- 来自：Xuanwo

[@东坡肘子](https://www.fatbobman.com/)：作者是一名受雇于开源项目 datafuselabs 的全职开发者，工作中主要使用的是 Rust 语言。每周他都会介绍当周的项目进展，包括：技术分享、开源运营、开发感受等。从中可以对商业运营的开源项目的参与和运作有所了解。

2、[科技爱好者周刊](https://www.ruanyifeng.com/blog/ "科技爱好者周刊") -- 来自：阮一峰

[@东坡肘子](https://www.fatbobman.com/)：内容包罗万象，包含技术分享、软件推荐、科技动态、奇闻异事等等。最大的特点是读者的参与度高，留言踊跃。

3、[codedump的网络日志](https://www.codedump.info "codedump的网络日志") -- 来自：codedump

[@东坡肘子](https://www.fatbobman.com/)：作者对存储引擎、分布式开发、缓存服务等内容情有独钟，撰写了大量的相关文章。近期开始从 C 转向 Rust ，估计今后有关 Rust 的内容也会逐渐增多。

4、[体验碎周报](https://www.ftium4.com "体验碎周报") -- 来自：龙爪槐守望者

[@东坡肘子](https://www.fatbobman.com/)：作者是一个交互设计师，每周的博文都会汇总大量有关交互设计的文章、案例、动态、评论、分析等内容。即使你从事的工作与交互无关，从中也能有所收获。

5、[13 的 Apple 开发者周报](https://ethanhuang13.substack.com "13 的 Apple 开发者周报") -- 来自：Ethan Huang

[@东坡肘子](https://www.fatbobman.com/)：以 Twitter 上的信息汇总为主，内容包括：苹果官方消息、媒体报道、技术资源、趣事小梗等内容，并且每周还会制作一个由苹果开发者参与的 podcast。对了解对岸开发者的开发状态有一定的帮助。

***

> 本期优秀博客的主题为：App Extension。

1、[iOS - App Extension 整体总结](https://www.cnblogs.com/junhuawang/p/8178276.html "iOS - App Extension 整体总结") -- 来自博客园：俊华

[@我是熊大](https://github.com/Tliens)：本文比较全面的介绍了 App Extension 的种类以及使用方法，平时不怎么使用的 Extension 竟然有十几种。通过此文应该能对 Extension 有个整体的了解。

2、[App与Extensions间通信共享数据](http://yulingtianxia.com/blog/2015/04/06/Communication-between-your-App-and-Extensions/ "App与Extensions间通信共享数据") -- 来自博客：杨萧玉

[@我是熊大](https://github.com/Tliens)：本文利用 WatchKit Extension 实现了 App 与 Watch 之间的通信，介绍了Containing app 与 App Extension 之间如何进行通信和数据共享。

3、[Photo Editing Extension 详解](https://colin1994.github.io/2016/03/12/Photo-Editing-Extension/ "Photo Editing Extension 详解") -- 来自博客：colin

[@我是熊大](https://github.com/Tliens)：本文通过一个 Demo 演示，介绍了 Photo Editing Extension 如何开发。

4、[iOS14 Widget小组件开发(Widget Extension)](https://www.jianshu.com/p/94a98c203763 "iOS14 Widget小组件开发(Widget Extension)") -- 来自简书：Singularity_Lee

[@我是熊大](https://github.com/Tliens)：iOS14 之后出现了非常重要的 Extension，这就是 Widget，桌面小组件，本文十分详细的介绍了如何开发Widget，如果你也有开发需求，推荐阅读。

5、[揭秘 iOS App Extension 开发 —— Today 篇](https://www.jianshu.com/p/bbc6a95d9c54 "揭秘 iOS App Extension 开发 —— Today 篇") -- 来自简书：Cyandev

[@我是熊大](https://github.com/Tliens)：在iOS14之前，是没有桌面组件的，那时候叫做 Today Extension，但在 iOS14 之后，这个 Extension 已经被 Widget 代替。本文借助一个 todo 的 Demo，介绍了 Today Extension。

***

整理编辑：皮拉夫大王在此

> 本期博客主题：iOS 内存。如果你对以下几个问题不了解的话，推荐阅读本期的博客。
> - 什么是 MMU？什么是 clean/dirty/compressed memory？
> - 申请 malloc(1)，malloc_size 是多少？
> - 小内存释放，内存会立即还给系统吗？
> - TCMalloc 主要解决什么问题？

1. [iOS Memory 内存详解 (长文)](https://juejin.cn/post/6844903902169710600#heading-2 "iOS Memory 内存详解 (长文)") -- 来自掘金：RickeyBoy

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：本文主要介绍了 iOS 内存相关的基础知识，可以帮助读者建立内存知识全景图。我们可以带着问题去阅读这篇文章：（1）、虚拟内存是如何映射到物理内存的？（2）、clean/dirty memory是如何区分的？一块 dirty memory 的单位大小是多少？

2. [深入理解内存分配](https://sq.sf.163.com/blog/article/178605610527186944 "深入理解内存分配") -- 来自网易数帆：阿凡达

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：内存分配的硬核文章，内容很有意思。通过阅读这篇文章，首先我们会了解 free 的过程，顺带也就能理解作者举的例子：str[0]='a' 报错非 bad_access 的原因了。另外作者列举了多种替换系统默认内存分配方式，这也是比较有意思的一点。

3. [Matrix-iOS 内存监控](https://cloud.tencent.com/developer/article/1427932 "Matrix-iOS 内存监控") -- 来自腾讯云：微信终端团队

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：来自微信的 matrix 内存监控原理介绍工具，能够抓取每个对象生成时的堆栈。与 OOMDetector 的原理一致，但是性能上更胜一筹。如此大量且高频的堆栈抓取和保存，matrix 是如何做优化的？可以通过阅读本文来了解细节。

4. [TCMalloc解密](https://wallenwang.com/2018/11/tcmalloc/ "TCMalloc解密") -- 来自：Wallen's Blog

[@皮拉夫大王](https://juejin.cn/user/281104094332653)：对《深入理解内存分配》中提到的 TCMalloc 感兴趣的可以继续阅读这篇文章。


***

> 在 Swift 中有两种特性（ Attributes ），分别用于修饰声明和类型。特性提供了有关声明和类型的更多信息。本期将汇总一些介绍声明特性的文章以帮助大家更好的掌握和使用特性这个强大的工具。

整理编辑：[东坡肘子](https://www.fatbobman.com)

1、[@available 与调用方进行沟通](https://mp.weixin.qq.com/s/e2_mWNx4HduM57LF0xTvqA) -- 来自：OldBirds

[@东坡肘子](https://www.fatbobman.com/)：保持代码不变很难，因为需求不断在变化，系统、框架不断在更新。那么项目实践中，往往会废弃掉一些类或方法。如果是自己独立维护代码，且不需要将代码给他人使用，废弃 API 对你来说是非常简单的，直接改动源码即可。但是对于多人合作的项目，特别是开源的库，废弃一个公开的 API 不是简单地改动下代码就可以，因为你的改动将会影响使用你这个库的所有代码。公开的 API 的更新换代，就相当于你改动了和别人约定的契约一样，这也侧面反映了作者的专业水平。那么如果要废弃一个 API，在 Swift 中我们该如何做？

2、[了解 Swift 中的 @inlinable](https://swiftrocks.com/understanding-inlinable-in-swift.html "了解 Swift 中的 @inlinable") -- 来自：Bruno Rocha

[@东坡肘子](https://www.fatbobman.com/)：@inlinable 特性是 Swift 中较少为人所知的属性之一。和其他同类特性一样，它的目的是启用一组特定的微优化，开发者可以用它来提高应用程序的性能。本文将介绍这个属性是如何工作的，并分析使用它的利弊。

3、[ViewBuilder 研究 —— 掌握 Result builders](https://mp.weixin.qq.com/s/4TwfyhWHVjm3Dv-Vz7MYvg) -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：结果构造器能按顺序构造一组嵌套的数据结构。利用它，可以以一种自然的声明式语法为嵌套数据结构实现一套领域专门语言（ DSL ），SwiftUI 的声明式特性即来源于此。本文将探讨结果构造器的实现原理，以及如何使用它来创建自己的 DSL 。

4、[@testable 的隐藏成本](https://paul-samuels.com/blog/2021/03/29/thoughts-on-testable-import/ "@testable 的隐藏成本") -- 来自：Paul Samuels

[@东坡肘子](https://www.fatbobman.com/)：在单元测试中，开发者通过为 import 添加 @testable 特性以改变代码的可见性。在需要的时候，这当然是有用的，但它常常被过于急切地使用而没有考虑到可能导致的一些问题。本文将探讨一下使用 @testable 可能导致的一些潜在的设计问题。本文的作者并不是说使用 @testable 是错误的，而是开发者需要为此做的一些设计权衡。

5、[Swift 中的 @objc、@objcMembers 关键字探讨](https://mp.weixin.qq.com/s?__biz=MzkwMDIxNDA3NA==&mid=2247483745&idx=1&sn=8f1db6e0a109754ed73bd3438f64285e&chksm=c0463d34f731b4222e8c238448d19e71f801b25d459b57be673305bcee2ae9cd5aa09a120f01&token=912344454&lang=zh_CN#rd) -- 来自：剑老师

[@东坡肘子](https://www.fatbobman.com/)：我们说 Objective-C 是一门动态语言，决策会尽可能地推迟到运行时。而 Swit 是一门静态语言，也就是说 Swift 的对象类型、调用的方法都是在编译期就确定的，这也是为什么 Swift 比 OC 性能高的原因。但是在 Swift 中所有继承自 NSObject 的类，仍然保留了 Objective-C 的动态性。如果想要使用它的动态性就需要加上 @objc 关键字，本篇文章就来讲一下，哪些情况需要用到 @objc。

6、[为自定义属性包装类型添加类 @Published 的能力](https://mp.weixin.qq.com/s/USGJbLnR-l8Ajgcj8Vb7_A) -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：属性包装器允许你在一个独特的包装器对象中提取通用逻辑。你可以把属性包装器看作是一个额外的层，它定义了一个属性是如何在读取时存储或计算的。它有利于改善 getters 和 setters 中发现重复性代码的几率。本文介绍了 Swift 编译器如何将属性包装类型转译为标准的 Swift 代码，并通过几个实例让读者对属性包装器的用法有更深的了解。

***

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

***

> 每年一度的苹果开发者盛会在不久前落幕了。今年的 WWDC 一如既往地精彩。我们将分几期将一些有关 WWDC 2022 上推出的新内容、新技术介绍给大家。

整理编辑：[东坡肘子](https://www.fatbobman.com), [Mimosa](https://juejin.cn/user/1433418892590136)

1、[怎么快速看完 WWDC22](https://www.ethanhuang13.com/p/144 "怎么快速看完 WWDC22") -- 来自：Ethan Huang

[@东坡肘子](https://www.fatbobman.com/)：今年的 WWDC 2022 很精彩，内容也非常多。跟其他人不同的是，Ethan Huang 写的不是整理好的笔记、个别的知识点，而是一套有效率的吸收策略。涵盖：建立全面的印象、挑选有兴趣的主题深入以及如何利用社群来发现重要的知识。

2、[WWDC22 笔记](https://ming1016.github.io/2022/06/10/wwdc22-notes/ "WWDC22 笔记") -- 来自：戴铭

[@东坡肘子](https://www.fatbobman.com/)：边看、边记、边整理是本文的特色。作者采用了类似日记的方式，记录并整理了自己在观看 WWDC 2022 期间的每日心得。这种方式也值得其他的开发者借鉴。

3、[Swift 5.7 新特性](https://juejin.cn/post/7107058234409615373 "Swift 5.7 新特性") -- 来自：Paul Hudson 中文译者：猫克杯

[@东坡肘子](https://www.fatbobman.com/)：Swift 5.7 变化巨大，新特性中包括正则表达式， if let 速记语法，以及围绕 any 和 some 关键字的一致性改动。在本文中，Paul Hudson 想向你介绍重大变化，提供一些实际操作示例，以便你可以快速了解和掌握。

4、[WWDC 2022 在线休息室中有关 SwiftUI 的讨论](https://swiftui-lab.com/digital-lounges-2022/ "WWDC 2022 在线休息室中有关 SwiftUI 的讨论") -- 来自：Javier

[@东坡肘子](https://www.fatbobman.com/)：从 WWDC 2021 开始，苹果引入了在线休息室（ Digital Lounge ），为广大开发者提供了同苹果各个团队的工程师和设计师展开文字形式的讨论，针对最新技术提出问题，寻求编程方面的帮助以及结交演讲嘉宾的机会。今年 Javier 一如既往地对 WWDC 2022 在线休息室中有关 SwiftUI 方面的讨论进行了整理，并添加了自己的评论。

5、[SwiftUI 4.0 的全新导航系统](https://www.fatbobman.com/posts/new_navigator_of_SwiftUI_4/ "SwiftUI 4.0 的全新导航系统") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：长久以来，开发者对 SwiftUI 的导航系统颇有微词。受 NavigationView 的能力限制，开发者需要动用各种技巧乃至黑科技才能实现一些本应具备的基本功能（例如：返回根视图、向堆栈添加任意视图、返回任意层级视图 、Deep Link 跳转等 ）。SwiftUI 4.0 对导航系统作出了重大改变，提供了以视图堆栈为管理对象的新 API ，让开发者可以轻松实现编程式导航。本文将对新的导航系统作以介绍。

6、[WWDC 2022 Swift Student Challenge Submissions](https://wwdc.github.io/2022 "WWDC 2022 Swift Student Challenge Submissions") -- 来自：WWDC Students

[@Mimosa](https://juejin.cn/user/1433418892590136)：一年一度的 [WWDC Swift Student Challenge](https://developer.apple.com/wwdc22/swift-student-challenge/) 随着 WWDC 22 的召开也随之落幕了，全球无数学生开发者通过提交作品来争抢 300 多张 WWDC 现场门票，在这个网站可以看到许多优秀学生开发者今年制作的作品，以及视频演示链接，其中许多作品效果令人惊艳，难以想象其中某些作品仅出自初高中生之手。

7、[WWDC 2022 Summary for Designers](https://uxmisfit.com/2022/06/06/wwdc-2022-summary/ "WWDC 2022 Summary for Designers") -- 来自：Thalion

[@Mimosa](https://juejin.cn/user/1433418892590136)：最关注每年 WWDC 的群体莫过于程序员了，但其实除了程序员之外，也有许多并非是 Coder 的人在默默地关注着，设计师（UX/UI）就是其中的一员。本文作者通过自己的视角来解读了对于设计师们来说，这次 WWDC 中有哪些值得注意的点、在新系统中，有哪些地方更加提升了用户的体验的、以及一些他自己的看法等等。

***

> 每年一度的苹果开发者盛会在不久前落幕了。今年的 WWDC 一如既往地精彩。我们将分几期将一些有关 WWDC 2022 上推出的新内容、新技术介绍给大家。

整理编辑：[远恒之义](https://github.com/eternaljust)，[Mimosa](https://juejin.cn/user/1433418892590136)

1、[WWDC22: Wrap up and recommended talks](https://www.hackingwithswift.com/articles/254/wwdc22-wrap-up-and-recommended-talks "WWDC22: Wrap up and recommended talks") -- 来自：hackingwithswift

[@远恒之义](https://github.com/eternaljust)：WWDC22 精彩纷呈，本文作者回顾了他参与本次活动的过程，一些现场有趣的故事，10 个最喜欢的演讲主题，6 个推荐视频来了解刚推出的新内容，还有几个丰富的 WWDC22 周边社区活动。

2、[在 SwiftUI 利用 Live Text API 從圖片中擷取文本](https://www.appcoda.com.tw/live-text-api/ "在 SwiftUI 利用 Live Text API 從圖片中擷取文本") -- 来自：appcoda

[@远恒之义](https://github.com/eternaljust)：在新的 iOS 16，Apple 发布了 Live Text API，可以将图像转换为机器可读的文本格式。我们只需使用 VisionKit 中的一个新类别 DataScannerViewController，来启用有 Live Text 功能的相机，就能提取出图像中的文本。本文同时为你提供了一个 demo 来快速上手体验。

3、[iOS CarPlay｜WWDC22 - 通过 CarPlay 让你的 App 发挥更大的作用](https://juejin.cn/post/7114239495360233479 "iOS CarPlay｜WWDC22 - 通过 CarPlay 让你的 App 发挥更大的作用") -- 来自：师大小海腾

[@远恒之义](https://github.com/eternaljust)：时隔 2 年，CarPlay 迎来了大更新。在 iOS16 中新增的两种支持 CarPlay 的 App 类型：Fueling App 和 Driving Task App。感兴趣的话，和作者一起来探索 Navigation App 如何在受支持车辆中的数字仪表盘上实时绘制地图。

此外，Apple 今年给我们带来了 CarPlay Simulator，它是一个 Mac App，可以帮助你在不离开办公桌的情况下连接 iPhone Device 来开发和测试 CarPlay App，模拟真实环境，而无需经常来回跑到你的车上或购买售后市场主机进行测试。这大幅度提升了开发者的开发测试体验。

4、[用 Table 在 SwiftUI 下创建表格](https://www.fatbobman.com/posts/table_in_SwiftUI/ "用 Table 在 SwiftUI 下创建表格") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：Table 是 SwiftUI 3.0 中为 macOS 平台提供的表格控件，开发者通过它可以快捷地创建可交互的多列表格。在 WWDC 2022 中，Table 被拓展到 iPadOS 平台，让其拥有了更大的施展空间。本文将介绍 Table 的用法、分析 Table 的特点以及如何在其他的平台上实现类似的功能。

5、[What’s the difference between any and some in Swift 5.7?](https://www.donnywals.com/whats-the-difference-between-any-and-some-in-swift-5-7/ "What’s the difference between any and some in Swift 5.7?") -- 来自：Donny Wals

[@Mimosa](https://juejin.cn/user/1433418892590136)：作者通过举例来说明了在 Swift 5.7 中你该如何选择 some 还是 any 关键词，阐述了他们之间的不同，同时谈了一下该如何正确的使用它们，以及未来可能在 Swift 6 中的表现。在作者的另一篇文章 [What are primary associated types in Swift 5.7?](https://www.donnywals.com/what-are-primary-associated-types-in-swift-5-7/) 中它也谈到了，在实际使用场景，例如关联类型的使用中，some 和 any 关键词对程序的影响。

6、[深入理解 Git 底层实现原理](http://chuquan.me/2022/05/21/understand-principle-of-git/ "深入理解 Git 底层实现原理") -- 来自：楚权

[@Mimosa](https://juejin.cn/user/1433418892590136)：大家平时都在使用 Git，但是其中的底层实现原理大家了解么？该文章作者从 Git 整体的架构出发，分层讲解了各层作用，主要谈了对象数据库的设计等。同时也给出了基于其原理的一个设计案例 —— CocoaPods Source 管理机制。文章整体写的通俗易懂，配图也简洁大方。

***

> 本期内容仍以介绍 WWDC 2022 上推出的新技术为主

1、[Grid 格狀排版](https://youtu.be/N2pXtupyblI "Grid 格狀排版") -- 来自：Jane

[@东坡肘子](https://www.fatbobman.com/)：这个视频会介绍 iOS16 新推出的 Grid —— 网格排版 View 。Grid 是一个十分强大的网格排版工具，极大地改善了 SwiftUI 的版式控制能力。视频会从经典的网格解决方案 GeometryReader 写法讲起，更具体地呈现 Grid 所解决的问题。接着会介绍与 Grid 相关的四个 modifier。

2、[SwiftUI 布局 —— 对齐](https://www.fatbobman.com/posts/layout-alignment/ "SwiftUI 布局 —— 对齐") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：“对齐”是 SwiftUI 中极为重要的概念，然而相当多的开发者并不能很好地驾驭这个布局利器。在 WWDC 2022 中，苹果为 SwiftUI 增添了 Layout 协议，让我们有了更多的机会了解和验证 SwiftUI 的布局原理。本文将结合 Layout 协议的内容对 SwiftUI 的“对齐”进行梳理，希望能让读者对“对齐”有更加清晰地认识和掌握。

3、[Swift Protocol 背后的故事 —— Swift 5.6/5.7](http://zxfcumtcs.github.io/2022/06/30/SwiftProtocol3/ "Swift Protocol 背后的故事 —— Swift 5.6/5.7") -- 来自：雪峰

[@东坡肘子](https://www.fatbobman.com/)：本文是系列文章的第三篇（ 前两篇为 Swift Protocol 背后的故事 —— 实践、Protocol 背后的故事 —— 理论 ），介绍了 Swift 5.6/5.7 在 Protocol 上的相关扩展和优化，主要包括：any、Opaque Parameter、Unlock existentials for all protocols 以及 Primary Associated Types 等内容。

4、[利用 SwiftUI 的新 Charts API 輕鬆建立漂亮的折線圖](https://www.appcoda.com.tw/swiftui-line-charts/ "利用 SwiftUI 的新 Charts API　輕鬆建立漂亮的折線圖") -- 来自：Simon Ng

[@远恒之义](https://github.com/eternaljust)：在 iOS 16 的新版 SwiftUI 中，Apple 重磅更新带来了 Charts 框架。在此之前，我们需要自定义构建图表，或者是依靠第三方库来建立图表。等到现在，我们简单使用 Charts API，就能轻松上手构建折线图。除此之外，开发者还可以更方便地创建动画化和互动的其他图表。

5、[How to Use ShareLink for Sharing Data Like Text and Photos](https://www.appcoda.com/swiftui-sharelink/ "How to Use ShareLink for Sharing Data Like Text and Photos") -- 来自：Simon Ng

[@远恒之义](https://github.com/eternaljust)：当前在 SwiftUI 项目中，我们如果需要调用系统分享数据，必须通过桥接 UIActivityViewController 来实现。在 iOS 16 中，SwiftUI 推出一个名为 ShareLink 的视图控件，当用户点击分享链接时，它会弹出显示系统分享列表，让用户将内容共享到其他应用程序或复制数据以供以后使用。本文将向你展示如何使用 ShareLink 来分享文本、URL 链接和图像等数据。

6、[Implementing a custom native calendar using UICalendarView in iOS16 and Swift](https://ohmyswift.com/blog/2022/06/12/implementing-a-custom-native-calendar-using-uicalendarview-in-ios16-and-swift/ "Implementing a custom native calendar using UICalendarView in iOS16 and Swift") -- 来自：Rizwan Ahmed

[@远恒之义](https://github.com/eternaljust)：以前，面对复杂的日历显示交互需求，我们通常选择第三方日历组件或者自定义日历视图来实现。今年，Apple 引入了原生 UICalendarView，支持在 iOS 16 创建自定义日历视图。本文将介绍如何使用 UICalendarView 来实现自定义原生日历，并支持单选与多选日期。

7、[How to change status bar color in SwiftUI](https://sarunw.com/posts/swiftui-status-bar-color/ "How to change status bar color in SwiftUI") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：在 UIKit 中，我们有很多方法可以[改变状态栏的样式](https://sarunw.com/posts/how-to-set-status-bar-style/ "改变状态栏的样式")。
然而在 SwiftUI 中，我们无法直接更改状态栏样式，需要通过视图修饰符 .preferredColorScheme 来间接修改。这种方式将影响应用程序中的每个视图，相当于手动设置了浅色与深色模式。在 iOS 16 中，我们使用新的修饰符 .toolbarColorScheme 来影响特定导航堆栈上的状态栏，也可以单独在目标视图中再次设置来覆盖此值。

***

> 对于国内的 iOSer 来说，WWDC 内参是一个较好的了解 WWDC 新内容途径，目前超过三成的文章已经出炉，今年的内参质量更上一层楼。今年我们部分摸鱼编辑参与其中，你可以查看[WWDC22内参参与体验](https://mp.weixin.qq.com/s/1x6JaHxb-bT3NtDb56BHDw)，今天还有机会获得邀请码呦。

1、[使用 LLDB 调试 Swift](https://xiaozhuanlan.com/topic/4809126537 "使用 LLDB 调试 Swift") -- 来自：WWDC22内参

[@夏天](https://juejin.cn/user/3298190611456638)：使用 LLDB 调试 Swift 代码时，有时候有点力不从心，有时候找不到源码，有时候指令失效等。文章介绍了几个解决方案来解决命令失效的问题。文章最后还介绍了如何正确的为打包 Framework 设置参数，确保 LLDB 能够正常运行。

2、[Safari 和 WebKit 新特性介绍](https://xiaozhuanlan.com/topic/1560743928 "Safari 和 WebKit 新特性介绍") -- 来自：WWDC22内参

[@夏天](https://juejin.cn/user/3298190611456638)：苹果关于 Safari 和 WebKit 的更新，可能是其为了追平某些功能在各个浏览器上相同或相似的体验。文章介绍了一些前端的概念，以及几个有助于前端开发的网站 [Can I use](https://caniuse.com/) 和 [MDN](https://developer.mozilla.org/en-US/)。

3、[在 SwiftUI 中组合各种自定义布局](https://xiaozhuanlan.com/topic/1507368249 "在 SwiftUI 中组合各种自定义布局") -- 来自：WWDC22内参

[@夏天](https://juejin.cn/user/3298190611456638)：Grid 是一个十分强大的网格排版工具，极大地改善了 SwiftUI 的版式控制能力。除了 Grid， 文章还介绍了 `ViewThatFits` 以及使用 `AnyLayout` 在不同的布局类型之间平滑地过渡。

4、[快速链接：优化构建和启动耗时](https://xiaozhuanlan.com/topic/1509638472 "快速链接：优化构建和启动耗时") -- 来自：WWDC22内参

[@夏天](https://juejin.cn/user/3298190611456638)：一篇关于实现更快构建和优化 APP 提交和缩短启动耗时的文章。文章介绍了静态链接和动态链接相关的概念，并引申其原理内容。构建和启动相关的知识，一直是 iOS 开发中较为深奥的一部分，文章介绍的内容无论你是学习还是准备面试，都有一定的作用。

5、[Swift 新特性介绍](https://xiaozhuanlan.com/topic/2498765013 "Swift 新特性介绍") -- 来自：WWDC22内参

[@夏天](https://juejin.cn/user/3298190611456638)：是一篇让你快速了解今 Swift 更新内容的文章，为你提供了最近几年 Swift 发展的概览，介绍了今年更新的内容。如果你需要对今年 Swift 更新内容有一个了解，不失为一种途径。

7、[探索 In-App Purchase 集成和迁移](https://xiaozhuanlan.com/topic/8024563197 "探索 In-App Purchase 集成和迁移") -- 来自：WWDC22内参

[@夏天](https://juejin.cn/user/3298190611456638)：IAP 可能是部分国内开发者上架 App Store 的一种`阻碍`。去年 Apple 对 IAP 大拆大建，今年也新增了部分功能。如果你近期有关于 IAP 相关的内容，可以回顾最近两年的内参，对你有不小的帮助。

6、[Swift 编程语言](https://www.cnswift.org/ "Swift 编程语言")--来自：cnswift

[@Hello World](https://juejin.cn/user/2999123453164605/posts)：比 SwiftGG `更快` 的 Swift 中文版本。

***

1、[SwiftUI中的后台任务](https://swiftwithmajid.com/2022/07/06/background-tasks-in-swiftui/ "SwiftUI中的后台任务") -- 来自：Majid

[@东坡肘子](https://www.fatbobman.com/)：苹果随着 iOS 13 一起发布了一个 BackgroundTasks 框架。该框架允许开发者使用代码在后台智能地安排工作。在 SwiftUI 4.0 中，苹果又新增了 backgroundTask 视图修饰器，进一步降低了使用后台框架的难度。Majid 将通过本文介绍如何在 SwiftUI 中安排和处理后台任务。

2、[SwiftUI 布局 —— 尺寸](https://www.fatbobman.com/posts/layout-dimensions-1/ "SwiftUI 布局 —— 尺寸") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：在 SwiftUI 中，尺寸这一布局中极为重要的概念，似乎变得有些神秘。无论是设置尺寸还是获取尺寸都不是那么地符合直觉。本文将从布局的角度入手，为你揭开盖在 SwiftUI 尺寸概念上面纱，了解并掌握 SwiftUI 中众多尺寸的含义与用法；并通过创建符合 Layout 协议的 frame 和 fixedSize 视图修饰器的复制品，让你对 SwiftUI 的布局机制有更加深入地理解。

3、[WWDC 2022 数字会客室中有关 Core Data 的内容](https://useyourloaf.com/blog/wwdc22-core-data-lab-notes/ "WWDC 2022 数字会客室中有关 Core Data 的内容") -- 来自：Keith Harrison

[@东坡肘子](https://www.fatbobman.com/)：在 WWDC 2022 中，虽然苹果没有为 Core Data 增加新的功能，但这并不意味着 Core Data 在苹果生态中变得不那么重要。Keith Harrison 整理了在 WWDC 2022 数字会客室中有关 Core Data 方面的一些讨论，主要涉及：数据同步、异步加载等方面的内容。

4、[Bottom Sheet in SwiftUI on iOS 16 with presentationDetents modifier](https://sarunw.com/posts/swiftui-bottom-sheet/ "Bottom Sheet in SwiftUI on iOS 16 with presentationDetents modifier") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：底部表单(Bottom Sheet)是一种类似 Apple 地图主页面拖动的控件，你可以从设备屏幕底部向上滑动，来调整页面内容的显示大小。在 iOS 15 UIKit 中，Apple 推出了 `UISheetPresentationController`，支持展示 `.medium` 和 `.large` 两种形态。今年，iOS 16 SwiftUI 推出了 `presentationdetents` 修饰符，除了支持之前的大中尺寸，新的修饰符还升级了三种设置方式：固定高度(`.height`)，分数(`.fraction`)以及自定义高度逻辑(`.custom`)。

5、[利用新的 ImageRenderer API 輕鬆把 SwiftUI 視圖轉換為圖像](https://www.appcoda.com.tw/imagerenderer-swiftui/ "利用新的 ImageRenderer API 輕鬆把 SwiftUI 視圖轉換為圖像") -- 来自：Simon Ng

[@远恒之义](https://github.com/eternaljust)：iOS 16 SwiftUI 新推出了 `ImageRenderer`。利用这个 API，我们可以轻松把 SwiftUI 中的视图转换为图像，再保存这个图像到系统相册中。同时，分享视图转换后的图像也是轻而易举的操作。此外，通过设置 `ImageRenderer` 类别中的 `scale` 属性，你还可以调整渲染图像的比例，从而提高图像的解析度。

6、[信息安全 | 互联网时代，如何建立信任？](https://mp.weixin.qq.com/s?__biz=Mzg3MjcxNzUxOQ==&mid=2247484972&idx=1&sn=4f0d819e8ab9456bd2ee81942abb3f22&chksm=ceea4b8cf99dc29ad27798c860c9db89621d81497fb6a5d206ed0602d75cffbb1bfdbec5809a&token=2062691669&lang=zh_CN#rd) -- 来自公众号：Bo2SS

[@doubleLLL3](https://github.com/doubleLLL3)：文章从信息安全是什么说起，到为什么，到怎么做，脉络清晰，层层递进，最后还聊了一些相关的应用加深理解。

通过文章可以让读者回答并理解以下问题：

1）信息传输一般使用对称加密+非对称加密，为什么？不能只使用其中一种吗？

2）信息安全为什么需要数字签名？

3）为什么签名前需要做哈希操作？

4）信息安全为什么需要数字证书？

文章的终极目标是：当我们在遇到密码学相关问题时，不再恐惧和迷惑。

***

1、 [开源｜WBBlades 重要节点更新-专为提效而设计](https://mp.weixin.qq.com/s/tXxhnDKerobyxoWuEBGjNQ) -- 来自：58技术

[@皮拉夫大王]()：给 iOS 开发人员提供基于 Mach-O 文件解析的工具集，工具包括无用类检测（支持 OC 和 Swift）、包大小分析（支持单个静态库/动态库的包大小分析）、点对点崩溃解析（基于系统日志，支持有符号状态和无符号状态），主要基于 Mach-O 文件的分析、轻量符号表剥离，系统日志解析等技术手段。

2、[iOS 不必现崩溃的点对点解析以及治理](https://mp.weixin.qq.com/s/tGvE-2flzhm4skkrfbUIBA) -- 来自：58技术

[@皮拉夫大王]()：本文章中介绍 iOS 端发生崩溃后，在无法复现的情况下如何针对各种不同类型的崩溃日志进行解析，包括普通堆栈，wakesup 崩溃，json 格式日志，bugly 堆栈类型等。此外还介绍了系统日志存在异常情况进行自动修正的方法，包括进程名称丢失，基地址丢失，偏移地址错误等。

3、[西瓜视频iOS启动优化实践](https://juejin.cn/post/7122472926792089607 "西瓜视频iOS启动优化实践") -- 来自：QYizhong

[@Mimosa](https://juejin.cn/user/1433418892590136)：本文介绍了在西瓜视频在 iOS 启动方面做了哪些努力去优化，将启动时面临的问题都一一列出，并根据问题的不同性质和影响阶段，提供了不同的优化的方案，并配上精致的动画来帮助读者理解优化前后的区别。同时也介绍了防劣化与监控的相关知识和实践来保证保持优化效果以及感知线上劣化情况。

4、[Background Modes Tutorial: Getting Started](https://www.raywenderlich.com/34269507-background-modes-tutorial-getting-started "Background Modes Tutorial: Getting Started") -- 来自：raywenderlich

[@Mimosa](https://juejin.cn/user/1433418892590136)：这是一篇面向新手的 Background Modes 开发指南，通过该教程，你可以了解到应用程序可以在后台执行的逻辑，以及四个样例：播放音频、获取位置更新、有限长度任务、后台请求。并且有 Swift 5.5 的代码工程样例佐以配合。

5、[WWDC 22 Sessions 手绘笔记](https://drive.google.com/drive/folders/1Ux57jowC_IziRpJgPrvqf4M6GlLxslOL "WWDC 22 Sessions 手绘笔记") -- 来自：manu

[@Mimosa](https://juejin.cn/user/1433418892590136)：来自 Apple 系统开发工程师 [manu](https://twitter.com/codePrincess) 的 WWDC 22 手绘笔记，包含多个 What's New 系列以及 Create ML、Actors 等热门 session。她的手绘笔记制作精美、风格强烈，言简意赅的概括了 session 的内容，非常推荐大家看一下。

6、[SwiftUI Split View Configuration](https://useyourloaf.com/blog/swiftui-split-view-configuration "SwiftUI Split View Configuration") -- 来自：useyourloaf

[@Mimosa](https://juejin.cn/user/1433418892590136)：本文主要讨论了在 iOS 16 SwiftUI 中使用 NavigationSplitView 创建两列或三列布局的过程，提到了一些在 beta 或者之后版本可能出现的坑以及对应的解决方案。

***

1、[Experimenting with Live Activities](https://oleb.net/2022/live-activity/ "Experimenting with Live Activities") -- 来自：Ole Begemann

[@远恒之义](https://github.com/eternaljust)：上周更新的 iOS 16 beta 4 是第一个支持实时活动 Live Activities 的版本，实时活动是一个类似于小组件的视图，放置在锁定屏幕底部并能实时更新。苹果官方推荐的有用示例包括现场体育比分或火车出发时间。

本文作者和一群朋友设计了一个小盒子，可以连接到自行车的轮毂发电机，测量速度和距离，并通过蓝牙将数据发送到 iOS 应用程序，再利用 Live Activities 把数据同步更新到手机锁定屏幕上。本文是作者使用该 API 来实现第一个 Live Activities 的笔记，文中展示了一个实际操作视频，同时介绍了作者使用 Live Activities 的一些尝试和疑问，主要关于实时活动的几点：使用限制条件、锁屏配色、动画控制以及代码共享。

2、[Ultimate guide on Timer in Swift](https://www.swiftanytime.com/ultimate-guide-on-timer-in-swift/ "Ultimate guide on Timer in Swift") -- 来自：Team SA

[@远恒之义](https://github.com/eternaljust)：计时器 Timer 是用于在特定时间间隔后执行任何任务的类。计时器在 Swift 中使用非常方便，我们可以用于执行有延迟的任务或重复的工作。本文介绍以下了内容：如何执行任务，重复和非重复的定时器，使用 RunLoop 模式，跟踪计时器，定时器优化以减少能源和功率影响。这些内容覆盖了 Timer 方方面面的使用场景，是一份 Swift 计时器的终极指南。

3、[Variable Color in SF Symbols 4](https://sarunw.com/posts/sf-symbols-variable-color/ "Variable Color in SF Symbols 4") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：今年在 WWDC22 中，Apple 推出了 SF Symbols 4，带来了新特性可变颜色 Variable Color，你可以根据百分比值来更改符号的外观显示。新功能将有利于一些可以显示进度趋势的符号，例如 Wi-Fi 信号、扬声器响度。需要注意的是，并非所有符号都支持可变颜色。你需要下载最新的 SF Symbols App，通过从左侧面板中选择“变量”类别来浏览支持可变颜色的符号。

4、[How to Use the SwiftUI PhotosPicker](https://swiftsenpai.com/development/swiftui-photos-picker/?utm_source=rss&utm_medium=rss&utm_campaign=swiftui-photos-picker "How to Use the SwiftUI PhotosPicker") -- 来自：Lee Kah Seng

[@远恒之义](https://github.com/eternaljust)：在今年的 WWDC22 中，Apple 对 SwiftUI 进行了大量改进，SwiftUI 终于在 iOS 16 中获得了自己的原生图片选择器视图 PhotosPicker。PhotosPicker 视图支持 PHPickerViewController 中所有常见的功能，包括单选、多选、资源类型过滤和相册切换等功能。在 SwiftUI 中使用 PhotosPicker 视图非常简单，本文将介绍如何使用该图片选择器。

5、[实时切换 Core Data 的云同步状态](https://www.fatbobman.com/posts/real-time-switching-of-cloud-syncs-status/ "实时切换 Core Data 的云同步状态") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：在 WWDC 2019 上，苹果推出了 Core Data with CloudKit API，极大地降低了 Core Data 数据的云同步门槛。由于该服务对于开发者来说几乎是免费的，因此在之后的几年中，越来越多的开发者在应用中集成了该服务，并为用户带来了良好的跨设备、跨平台的使用体验。本文将对实时切换 Core Data 云同步状态的实现原理、操作细节以及注意事项进行探讨和说明。

6、[避免 SwiftUI 视图的重复计算](https://www.fatbobman.com/posts/avoid_repeated_calculations_of_SwiftUI_views/ "避免 SwiftUI 视图的重复计算") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：在 SwiftUI 中，每个视图都有与其对应的状态，当状态变化时，SwiftUI 都将重新计算与其对应视图的 body 值，这就是 SwiftUI “视图是状态的函数”的基本概念。如果视图响应了不该响应的状态，或者视图的状态中包含了不该包含的成员，都可能造成 SwiftUI 对该视图进行不必要的更新（重复计算），当类似情况集中出现，将直接影响应用的交互响应，并产生卡顿的状况。通常我们会将这种多余的计算行为称之为过度计算或重复计算。本文将介绍如何减少（甚至避免）类似的情况发生，从而改善 SwiftUI 应用的整体表现。

***

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1、[Xamarin 文档](https://docs.microsoft.com/zh-cn/xamarin/ "Xamarin 文档") -- 来自：Microsoft

[@夏天](https://juejin.cn/user/3298190611456638)：除了常见的 React Native、Flutter、Weex 之外，在跨平台上还有一些值得尝试的跨平台方案，比如来自 Microsoft 的 Xamarin 就允许你使用 .NET 代码和特定于平台的用户界面生成适用于 Android、iOS 和 macOS 的本机应用。也许，这不失为一个新的全栈选择。

2、[Qt](https://www.qt.io/ "Qt") -- 来自：*Qt* Company 

[@夏天](https://juejin.cn/user/3298190611456638)：除了上文的 C# 之外，由 *Qt* Company 开发的跨平台 C++ 图形用户界面应用程序开发框架。C ++ 拥有卓越的性能，那么用它开发出来的桌面或移动端应用是否能够在编写之初就能够凌驾在其他应用之上呢？当然其涵盖的点还包括嵌入式及微控制器（MCU），一次学习，干啥都行。除了付费以外，似乎没啥缺点。

3、[Geeks for Geeks](https://practice.geeksforgeeks.org/home "Geeks for Geeks") -- 来自：GeeksforGeeks

[@夏天](https://juejin.cn/user/3298190611456638)：一个对开发者来说很全面的网站，提供了算法，系统设计等基础内容。还提供了 [Practice](https://practice.geeksforgeeks.org/explore?page=1&curated[]=1&sortBy=submissions&curated_names[]=SDE%20Sheet) 和一些付费/免费的课程及文章。你也可以订阅他们的 [YouTube 账号](https://www.youtube.com/geeksforgeeksvideos) 观看视频课程，教程中的 CS Subject 适合大量入门或者基础不扎实的程序员。不过语言教学没有 Swift...

4、[iOS Conf SG](https://iosconf.sg/ "iOS Conf SG") -- 来自：iOS Conf SG

[@夏天](https://juejin.cn/user/3298190611456638)：号称东南亚最大的 iOS 开发者大会。从 2016 年举办至今已有 6 年，一个纯为 iOS 开发者举办的开发者大会。每年大概有 15 个左右的视频来讲述一些 iOS 相关的视频，你可以在 [YouTube ](https://www.youtube.com/c/iOSConfSG) 进行观看。

***

> 本期介绍三个着重于报道 Swift 语言发展的电子报以及近期的几篇优秀博文

1、[Swift 周报](https://mp.weixin.qq.com/s/npUMmAzYjzThEjrf0jJ4GQ "Swift 周报") -- 来自：Swift社区

[@东坡肘子](https://www.fatbobman.com/)：由于英文版的 Swift 周报停更，由国内 Swift 爱好者维护的中文版 Swift 周报也停滞了一段时间。从八月开始，中文版 Swift 周报重装上阵，全部内容由周报编辑组自行整理。当前模块分为：新闻、提案、Swift 论坛、推荐博文等。

2、[波报|Pofat 的 Swift 中文电子報](https://pofat.substack.com/archive "波报|Pofat 的 Swift 中文电子報") -- 来自：Pofat

[@东坡肘子](https://www.fatbobman.com/)：Pofat 是一个在苹果生态系打滚多年的 App 工程师，出于对 “工作的表层之下” 有更多了解的渴望，创办了波报，作为他用来探索的手段。当前的内容包括：Swift 和 LLVM 官方消息、Swift 和 LLVM 论坛新鲜事、Swift （或其它相关）的底层原理探讨等内容。

3、[Swift Evolution Monthly](https://se-monthly.flinedev.com/issues/swift-evolution-monthly-first-issue-background-history-chris-lattner-6-proposals-1092625 "Swift Evolution Monthly") -- 来自：Cihat Gündüz

[@东坡肘子](https://www.fatbobman.com/)：由 Cihat Gündüz 于数月前创建的月报，专注于介绍进展中的 Swift 提案。创建该刊物很大的原因也是由于 Swift Weekly Brief 的停刊。

4、[iOS 中的手势传递（一）操作系统层](https://juejin.cn/post/7132069500656517151 "iOS 中的手势传递（一）操作系统层") -- 来自：RickeyBoy

[@东坡肘子](https://www.fatbobman.com/)：通常我们处理手势是在 UIView 层级，直接使用 UIButton、UIGestureRecognizer 等来捕获手势，而本文重点讲的是在此之前，手势识别与传递的过程，在介绍整个过程的同时，也能对整个操作系统的工作方式有一定的了解。

5、[在 SwiftUI 中用 Text 实现图文混排](https://www.fatbobman.com/posts/mixing_text_and_graphics_with_Text_in_SwiftUI/ "在 SwiftUI 中用 Text 实现图文混排") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/)：SwiftUI 提供了强大的布局能力，不过这些布局操作都是在视图之间进行的。当我们想在 Text 中进行图文混排时，需要采用与视图布局不同的思路与操作方式。本文将首先介绍一些与 Text 有关的知识，并通过一个实际案例，为大家梳理出在 SwiftUI 中用 Text 实现图文混排的思路。

6、[Github 实用小技巧](https://xuanwo.io/reports/2022-32/ "Github 实用小技巧") -- 来自：漩涡

[@东坡肘子](https://www.fatbobman.com/)：漩涡从一个开源项目从业者的角度，介绍了一些他在工作中经常使用的 Github 实用小技巧。包括：引用 Github Issues/PR/Discussion、使用 Fix / Close 来关联一个 Issue、可折叠的区块、Draft / Ready for review、请求 Review、引用回复等内容。

***

整理编辑：[Mim0sa](https://juejin.cn/user/1433418892590136)

1、[从响应式编程到 Combine 实践](https://mp.weixin.qq.com/s/b_q6R64xkq8Rl9EiIde4MA "从响应式编程到 Combine 实践") -- 来自：字节跳动技术团队

[@Mim0sa](https://juejin.cn/user/1433418892590136)：来自字节跳动技术团队的 Combine 实践记录，文章从浅到深讲解了响应式编程的特点、选择 Combine 的理由以及具体实践。也介绍了 Combine 中的三个关键概念，事件发布／操作变形／订阅使用，也提及了一些常见错误等，很适合不是特别了解响应式编程的同学。

2、[不改一行业务代码，飞书 iOS 低端机启动优化实践](https://mp.weixin.qq.com/s/KQJ5QXHdhwHRN65KdD45qA "不改一行业务代码，飞书 iOS 低端机启动优化实践") -- 来自：字节跳动技术团队

[@Mim0sa](https://juejin.cn/user/1433418892590136)：低端机启动优化实践，文章讨论了在低端机的情况下，会在启动时有哪些特点，介绍了在 GCD queue 上发现的问题和优化方案。

3、[RunLoop的实际使用](https://mp.weixin.qq.com/s/GrkCUyxsoxqdkbeJcoAIdw "RunLoop的实际使用") -- 来自：搜狐技术产品

[@Mim0sa](https://juejin.cn/user/1433418892590136)：来自搜狐技术产品的一篇比较基础的 RunLoop 文章，从线程保活开始介绍了 RunLoop 在实际开发中的使用，然后介绍了卡顿监测和 Crash 防护中的高阶使用。

4、[iOS下锁的独白](https://mp.weixin.qq.com/s/3d365xrDKp7TwwY_htloiA "iOS下锁的独白") -- 来自：搜狐技术产品

[@Mim0sa](https://juejin.cn/user/1433418892590136)：来自搜狐技术产品的一篇关于锁的文章，介绍了 iOS 中的锁有哪一些，以及如何使用。文章中的代码和注释清晰明了，归纳的也很全。

5、[Avoiding race conditions in Swift](https://medium.com/swiftcairo/avoiding-race-conditions-in-swift-9ccef0ec0b26 "Avoiding race conditions in Swift") -- 来自：Mostafa Abdellateef

[@Mim0sa](https://juejin.cn/user/1433418892590136)：一篇关于如何避免竞争的文章，文章内容比较简单，但是观点很深入，探讨了在软件的设计中去避免资源的竞争，靠的不是一味的使用各种锁、栅栏，而是精良的设计。文中举的例子生动易懂且随文的图片制作精良。

6、[How do 3D transforms of iOS views work under the hood?](https://www.thealexanderlee.com/blog/how-do-3d-transforms-of-ios-views-work-under-the-hood "How do 3D transforms of iOS views work under the hood?") -- 来自：Alex Lee

[@Mim0sa](https://juejin.cn/user/1433418892590136)：本文主要介绍了 3D transforms 的各种变化是怎么得来的，配有手绘介绍图，但需要一点点数学知识才可以读懂。


***

1、[在 SwiftUI 中实现视图居中的若干种方法](https://www.fatbobman.com/posts/centering_the_View_in_SwiftUI/ "在 SwiftUI 中实现视图居中的若干种方法") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：将某个视图在父视图中居中显示是一个常见的需求，即使对于 SwiftUI 的初学者来说这也并非难事。在 SwiftUI 中，有很多手段可以达成此目的。本文将介绍其中的一些方法，并对每种方法背后的实现原理、适用场景以及注意事项做以说明。

2、[SwiftUI Navigation 框架的新功能](https://www.appcoda.com.tw/swiftui-navigation/ "SwiftUI Navigation 框架的新功能") -- 来自：AppCoda 编辑团队

[@远恒之义](https://github.com/eternaljust)：自推出以来，NavigationView 一直都是 SwiftUI Navigation 框架的致命弱点。它之前不支持 NavigationLink 中延迟载入目标视图，无法以编程方式导航 Deep Link。在 iOS 16 中，Apple 推出了一个以数据驱动的新导航结构 NavigationStack，让开发者可以从堆栈中推入和弹出视图，NavigationPath 用于管理 routing 堆栈，同时使用 navigationDestination 修饰符来有效率地导航视图。

3、[ContextMenu in SwiftUI](https://www.swiftanytime.com/contextmenu-in-swiftui/ "ContextMenu in SwiftUI") -- 来自：Team SA

[@远恒之义](https://github.com/eternaljust)：在 UiKit 中，使用 3D Touch 按压可实现 Peek 和 Pop 快速预览内容并提供上下文菜单操作，这是一个非常棒的交互体验。在 SwiftUI 中，我们可以用 Menu 弹出菜单进行交互，使用 ContextMenu 则能达到和 UiKit 类似的体验。本文将介绍使用 .contextMenu 修饰符来长按触发上下文菜单，并结合 Menu 和 Button 来添加子菜单。

4、[SwiftUI Gauge](https://sarunw.com/posts/swiftui-gauge/ "SwiftUI Gauge") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：仪表 Gauge 在 iOS 16 (SwiftUI 4) 中引入，是一种能显示范围内值的视图。在现实世界中，仪表是用于测量某物的大小、数量或内容，比如燃油表、温度表、转速表和速度表等仪器设备。Gauge 和 Slider 有些类似，你可以将 Gauge 视为 ProgressView 和 Slider 的结合。本文将介绍 Gauge 的使用方法，几种样式标签显示，以及如何进行自定义仪表视图。

5、[Lock screen widgets in SwiftUI](https://swiftwithmajid.com/2022/08/30/lock-screen-widgets-in-swiftui/ "Lock screen widgets in SwiftUI") -- 来自：Majid

[@远恒之义](https://github.com/eternaljust)：锁屏小组件是 iOS 16 最重磅的功能更新，作为 iPhone 设备上最顶级的访问入口，我们需要把握住用户使用自家 App 的曝光机会。实现锁屏小部件非常简单，因为它的 API 能与主屏幕小部件共享相同的代码。本文将介绍如何为我们的应用程序实现锁屏小部件。


***

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1. [基于 LLVM 自制编译器——序](http://chuquan.me/2022/07/17/compiler-for-kaleidoscope-00/ "基于 LLVM 自制编译器——序")  -- 来自：楚权的世界

   [@夏天](https://juejin.cn/user/3298190611456638)：文章是基于官方教程 [《My First Language Frontend with LLVM Tutorial》](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/index.html "《My First Language Frontend with LLVM Tutorial》") 的翻译，有助于加深对编译原理的理解。

   这位大佬的其他内容也值得推荐。

2. [How to improve iOS build times with modularization](https://www.runway.team/blog/how-to-improve-ios-build-times-with-modularization "How to improve iOS build times with modularization") -- 来自：Bruno Rocha

   [@夏天](https://juejin.cn/user/3298190611456638)：文章分析了影响 iOS 构建的因素，以及当我们使用模块化后如何使用 **API/Impl** 技术更快地编译相互依赖的模块。

3. [ARC and Memory Management in Swift](https://www.raywenderlich.com/966538-arc-and-memory-management-in-swift "ARC and Memory Management in Swift") -- 来自：RayWenderlich

   [@夏天](https://juejin.cn/user/3298190611456638)：RayWenderlich 教程系列的文章质量都比较高，本文介绍了 ARC 的工作原理以及内存管理的最佳实践，顺便介绍了如何发现内存泄露，很完整的一个教程。

4. [Hot Reloading in Swift](https://www.merowing.info/hot-reloading-in-swift/ "Hot Reloading in Swift") —— Krzysztof Zabłocki

   [@夏天](https://juejin.cn/user/3298190611456638)：如同 Injection  一样的帮助热重载的工具[DyCI](https://github.com/DyCI/dyci-main "DyCI")，文章并没有涉足原理，但是讲述了一些设计历程。

5. [App 如何通过注入动态库的方式实现极速编译调试？](https://time.geekbang.org/column/article/87188 "App 如何通过注入动态库的方式实现极速编译调试？")—— 戴铭《iOS 开发高手课》

   [@夏天](https://juejin.cn/user/3298190611456638)：使用动态库加载方式进行极速调试，简单分析了 Flutter 和 Injection 的原理。

***

整理编辑：[东坡肘子](https://www.fatbobman.com)

> 本期将介绍近期的几篇优秀博文

1、[SwiftUI布局协议](https://swiftui-lab.com/layout-protocol-part-1/ "SwiftUI布局协议") -- 来自：Javier

[@东坡肘子](https://www.fatbobman.com/)：在 SwiftUI 诞生初期，SwiftUI-Lab 的 Javier 便对 SwiftUI 进行了深入地研究，可以说很多 SwiftUI 的使用者都是通过阅读他的文章才开始了解 SwiftUI 的布局机制。针对今年 SwiftUI 新增的 Layout 协议，Javier 也贡献出了精彩研究文章。文章共分上下两部分，上篇着重介绍理论，下篇提供了许多有趣的案例演示。

2、[iPhone 14 屏幕尺寸](https://useyourloaf.com/blog/iphone-14-screen-sizes/ "iPhone 14 屏幕尺寸") -- 来自：Keith Harrison

[@东坡肘子](https://www.fatbobman.com/)：iPhone 14 Pro 和 iPhone 14 Pro Max 用灵动岛替换了刘海，这导致了屏幕的分辨率也发生了变化。本文对 2022 年 iPhone 14 系列机型的屏幕尺寸的变化做了总结。

3、[如何判断 ScrollView、List 是否正在滚动中](https://www.fatbobman.com/posts/how_to_judge_ScrollView_is_scrolling/ "如何判断 ScrollView、List 是否正在滚动中") -- 来自：Holly Borla

[@东坡肘子](https://www.fatbobman.com/)：SwiftUI 4 重写了 ScrollView 和 List 的底层实现，这意味着以前通过 Hack 的方式获取滚动状态的手段将不再有效。本文将介绍几种在 SwiftUI 中获取当前滚动状态的方法，每种方法都有各自的优势和局限性。

4、[Swift 5.7 正式发布](https://www.swift.org/blog/swift-5.7-released/ "Swift 5.7 正式发布") -- 来自：Holly Borla

[@东坡肘子](https://www.fatbobman.com/)：Swift 5.7 现已正式发布! Swift 5.7包括对语言和标准库的重大补充，对编译器的增强以获得更好的开发者体验，对Swift生态系统中的工具的改进，包括SourceKit-LSP和Swift Package Manager，完善的Windows支持等等。

5、[Combine中的内存管理](https://tanaschita.com/20220912-memory-management-in-combine/ "Combine中的内存管理") -- 来自：Holly Borla

[@东坡肘子](https://www.fatbobman.com/)：就像其他异步操作一样，内存管理是 Combine 的一个重要部分。一个订阅者只要想接收值就需要保留一个订阅，然而，一旦不再需要订阅，所有的引用应该被正确地释放。在这种情况下，一个常见的问题是我们是否应该使用弱引用。本文将通过一些例子来帮助读者更好地理解 Combine 中的内存管理。

6、[Apple Watch 应用开发系列](https://juejin.cn/post/7136115417323405325 "Apple Watch 应用开发系列") -- 来自：Layer

[@东坡肘子](https://www.fatbobman.com/)：2015 年 4 月 24 日，Apple 发布了第一代 Apple Watch。 无论我们对 Apple Watch 看法如何，watchOS 肯定是我们要支持的 Apple 生态系统的一部分，确保我们的应用获得更大的曝光率。作者将通过创建一个 watchOS 应用程序，来展示如何将我们现有的 iOS 开发知识转移到 watchOS 上来。

7、[灵动岛开发演示](https://www.youtube.com/watch?v=gEWvV-TmjqE&t=65s "灵动岛开发演示") -- 来自：Kavsoft

[@东坡肘子](https://www.fatbobman.com/)：Kavsoft 将在本视频中演示如何使用 SwiftUI 开发可用于 Apple iPhone 14 Pro 灵动岛的 Live Actitivy。

***

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

1、[How necessary are the programming fundamentals?](https://swiftrocks.com/how-necessary-are-the-programming-fundamentals "How necessary are the programming fundamentals?") -- 来自： Bruno Rocha

[@Mimosa](https://juejin.cn/user/1433418892590136)：我们平时写写业务代码好像用不到高深的算法、数据结构等知识，但是在大厂的面试中似乎又不可避免以高难度的形态出现，那这些编程基础知识到底有什么用呢？本文的作者讨论了这一普遍的现象，并以生动的例子提出了自己的见解和类比，并解释了这种情况出现的原因，同时也对这种略显病态的面试流程提出了自己的看法，如果你也有类似的疑惑，相信这篇文章可以给你一些启发。

2、[DocC Tutorial for Swift](https://www.raywenderlich.com/34919511-docc-tutorial-for-swift-getting-started "DocC Tutorial for Swift") -- 来自： raywenderlich

[@Mimosa](https://juejin.cn/user/1433418892590136)：在 WWDC21 上，Apple 推出了 DocC，这是一个文档编译器，可以在 Xcode 文档窗口中构建和查看 Swift 包的文档。Apple 在 WWDC22 中扩展了 DocC 功能，因此它也可以记录 Swift 和 Objective-C 项目。在这个教程中，会告诉你 DocC 的工作原理、一些实操的例子以及如何导出和发布。

3、[How to create Rounded Corners Button in UIKit](https://sarunw.com/posts/uikit-rounded-corners-button/ "How to create Rounded Corners Button in UIKit") -- 来自： Sarunw

[@Mimosa](https://juejin.cn/user/1433418892590136)：相信很多人还不知道在 iOS 15 之后，我们可以使用 `UIButton.Configuration` 来设置按钮的圆角以及其他表现，这篇文章就带大家熟悉一下这个好用的配置属性。

4、[聊聊 iOS 中的像素对齐](https://juejin.cn/post/7124658703088910350 "聊聊 iOS 中的像素对齐") -- 来自： JPlay

[@Mimosa](https://juejin.cn/user/1433418892590136)：当一个 UILabel 的宽度是 500.001 和 500 时会有什么区别？本文探讨了像素不对齐出现的原因以及系统像素补齐的原则，并给出了一些避免和解决的方法。

5、[重新开始学习计算机](https://juejin.cn/post/7124660156612214814 "重新开始学习计算机") -- 来自： JPlay

[@Mimosa](https://juejin.cn/user/1433418892590136)：这是一份一位程序员面对 35 岁职业魔咒的应对之道：拥有扎实的、广泛的、不受平台局限的计算机基础知识。


***

1、[StateObject 与 ObservedObject](https://www.fatbobman.com/posts/StateObject_and_ObservedObject/ "StateObject 与 ObservedObject") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：StateObject 和 ObservedObject 两者都是用来订阅可观察对象（ 符合 ObservableObject 协议的引用类型 ）的属性包装器。当被订阅的可观察对象通过内置的 Publisher 发送数据时（ 通过 @Published 或直接调用其 objectWillChange.send 方法 ），StateObject 和 ObservedObject 会驱动其所属的视图进行更新。StateObject 是在 SwiftUI 2.0 中才添加的属性包装器，它的出现解决了在某些情况下使用 ObservedObject 视图会出现超预期的问题。本文将介绍两者间的异同，原理以及注意事项。

2、[SwiftUI 开发之旅：适配深色模式](https://juejin.cn/post/7150553079060889614 "SwiftUI 开发之旅：适配深色模式") -- 来自：掘金 new_cheng

[@远恒之义](https://github.com/eternaljust)：从 iOS 13 开始，苹果支持了深色模式，在昏暗的环境中，我们打开深色模式可获得出色的视觉体验。SwiftUI 默认支持深色模式，对于基本视图的文字和背景都有默认的深色模式样式。本文作者介绍了 Color Set、overrideUserInterfaceStyle 等适配方法，还有如何支持用户手动切换颜色模式。对于深色模式的适配，推荐采用 Assets.xcassets 的方式去定义一个完整的颜色集来适配。

3、[How to dismiss sheet in SwiftUI](https://sarunw.com/posts/swiftui-dismiss-sheet/ "How to dismiss sheet in SwiftUI") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：模态或表单（.sheet）是 iOS 中的核心展示之一。在 SwiftUI 中有三种方法（`in the same view`、`with @Binding`、`with @Environment`）来关闭表单，具体的方式取决于你的视图结构以及支持的最低 iOS 版本。

4、[SwiftUI List Style examples](https://sarunw.com/posts/swiftui-list-style/ "SwiftUI List Style examples") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：SwiftUI 中的 list 列表有多种样式，基于不同的平台也支持许多不同的风格。本文中将专注于 iOS 平台，介绍六种不同的风格：`.automatic`、`.insetGrouped`、`.grouped`、`.inset`、`.plain`、`.sidebar`，每种样式都有简单的代码示例和展示配图。

5、[How to show badge on Tab Bar Item in SwiftUI](https://sarunw.com/posts/swiftui-tabbar-badge/ "How to show badge on Tab Bar Item in SwiftUI") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：tabItem 上的红点角标非常能吸引用户的注意，通常与应用程序图标上未读通知的数量相关联。在 SwiftUI 中，我们能非常方便的实现这个功能，使用 `badge(_:)` 来修饰选项卡栏项目（tabItem），支持设置整数（`.badge(3)`）和字符串（`.badge("99+")`）。

6、[How To Automatically Create .gifs From The iOS Simulator](https://digitalbunker.dev/automatically-create-gifs-from-the-ios-simulator/ "How To Automatically Create .gifs From The iOS Simulator")  -- 来自：digitalbunker

[@远恒之义](https://github.com/eternaljust)：如何在不需要任何第三方工具的情况下，直接从 iOS 模拟器录制视频并导出 .gif？首先，请按住 Option 键并将鼠标悬停在模拟器“保存屏幕”按钮上。按下该 Option 键，此设置将更改为“录制屏幕”。接着，你可以像往常一样继续录制你的应用程序。最后，停止录制，在视频预览消失之前，右键单击它并选择“另存为动画 GIF”。

![来自 digitalbunker 的演示操作 gif](https://cdn.zhangferry.com/Images/ios-simulator-gif.gif)

***

> 本期我们将推荐一些与实时活动和灵动岛有关的优秀内容

1、[在 iOS 16 中显示实时活动](https://swiftwithmajid.com/2022/09/21/displaying-live-activities-in-ios16/ "在 iOS 16 中显示实时活动") -- 来自：Majid

[@东坡肘子](https://www.fatbobman.com/)：实时活动小组件是 iOS 16 最突出的功能之一。iOS 16 允许我们在锁屏界面或 iPhone 14 Pro 的灵动岛区域显示来自应用程序持续活动的实时状态。本文将介绍如何使用新的 ActivityKit 框架为我们的应用程序构建实时活动小组件。

2、[掌握 SwiftUI 的灵动岛](https://swiftwithmajid.com/2022/09/28/mastering-dynamic-island-in-swiftui/ "掌握 SwiftUI 的灵动岛") -- 来自：Majid

[@东坡肘子](https://www.fatbobman.com/)：本文将介绍如何使用灵动岛功能在 iPhone 14 Pro 上显示应用程序中的实时活动，是上篇文章的延续。

3、[灵动岛 Dynamic Island 初探](https://kingnight.github.io/programming/2022/09/28/灵动岛Dynamic-Island初探.html "灵动岛 Dynamic Island 初探") -- 来自：Kingnight

[@东坡肘子](https://www.fatbobman.com/)：本篇文章将从软件开发角度，探索灵动岛的展现形式、功能限制、如何具体实现、适用场景等各方面的问题；帮助还不了解相关信息的开发者快速理解这一新的展现形式，并结合自身产品形态做出创新。

4、[为 iPhone 14 Pro 的灵动岛设计](https://uxdesign.cc/designing-for-iphone-14-pro-dynamic-island-90ea7f68b71 "为 iPhone 14 Pro 的灵动岛设计") -- 来自：Niels Boey

[@东坡肘子](https://www.fatbobman.com/)：作者是一个产品设计师，本文将从设计师的角度对灵动岛功能进行了介绍和讲解。

5、[实时活动（ Live Activity ）- 在锁定屏幕和灵动岛上显示应用程序的实时数据](https://juejin.cn/post/7144268555779850248 "实时活动（ Live Activity ）- 在锁定屏幕和灵动岛上显示应用程序的实时数据") -- 来自：Layer

[@东坡肘子](https://www.fatbobman.com/)：本文参考、翻译并实现了 Apple‘s documentation activitykit displaying live data with live activities 及 Updating and ending your Live Activity with remote push notifications 内容，并提供了范例代码。

6、[如何激活灵动岛中的像素](https://twitter.com/iphone15ultra/status/1580821164594585600 "如何激活灵动岛中的像素") -- 来自：iPhone 15 Ultra

[@东坡肘子](https://www.fatbobman.com/)：打开黑暗模式 -> 在后台播放一些音乐 -> 转到设置 -> 辅助功能 -> 显示与文本大小 -> 开启/关闭智能反转 -> 你将看到完整的💊。

7、[iOS灵动岛【电商商品秒杀】开发实践](https://juejin.cn/post/7153236337074634788 "iOS灵动岛【电商商品秒杀】开发实践") -- 来自掘金

[@邓利兵](https://github.com/erduoniba)：iOS灵动岛【电商商品秒杀】开发实践，详细讲解了灵动岛的基本概念、开发基本要素及细节。Demo中展示了主工程和灵动岛Widget的通讯方式及灵动岛Widget的布局方式。

***

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1、[Check for internet connection with Swift](https://stackoverflow.com/questions/30743408/check-for-internet-connection-with-swift "Check for internet connection with Swift") -- Stack Overflow

[@夏天](https://juejin.cn/user/3298190611456638): 当存在在 iOS App 上监测网络状态的需求时，不妨看一看这个提问，在回答中介绍了通过 `SCNetworkReachability` 来实现网络状态监听及 `NWPathMonitor`。如果你的系统支持的版本在 `iOS 12` 以上并且你有需要实现一个网络状态监听的程序，可以试一试`NWPathMonitor`。

2、[Detecting Internet Access on iOS 12+ | by Ross Butler | Medium](https://medium.com/@rwbutler/nwpathmonitor-the-new-reachability-de101a5a8835 "Detecting Internet Access on iOS 12+ | by Ross Butler | Medium") -- Medium

[@夏天](https://juejin.cn/user/3298190611456638): 这是一篇关于如果通过 `NWPathMonitor` 来实现 `iOS 12` 以上实现网络可达性判断的文章，文章介绍了 `NWPathMonitor` 的优点以及在后面断网时的不足，并且介绍了一个兼容的库 [Connectivity](https://github.com/rwbutler/Connectivity)，但是该库由于使用了 `Combine` 并不兼容 iOS 13 以下了。

3、[我是如何在新西兰找到iOS开发工作的？](https://www.youtube.com/channel/UCiEbxa6e5o3mtBJIwhRxbHA?sub_confirmation=1 "我是如何在新西兰找到iOS开发工作的？")-- 陈宜龙(@iOS程序犭袁)

[@夏天](https://juejin.cn/user/3298190611456638):  陈宜龙大佬是我学习 iOS 比较追寻的一个博主了，最近他润去了新西兰，可以查看他的其他的  `YouTube`  视频。


***

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

1、[SwifterSwift](https://github.com/SwifterSwift/SwifterSwift "SwifterSwift") -- github

[@夏天](https://juejin.cn/user/3298190611456638): SwifterSwift 是 **500 多个原生 Swift 扩展的集合**，为 iOS、macOS、tvOS、watchOS 和 Linux 提供了（超过 500 个）适用于各种原生数据类型、UIKit 和 Cocoa 类的便捷方法、语法糖和性能改进。

![](https://cdn.zhangferry.com/Images/SwifterSwift.png)

2、[货拉拉用户 iOS 端卡顿优化实践](https://juejin.cn/post/7160951025782751263 "货拉拉用户 iOS 端卡顿优化实践") -- 货拉拉技术

[@Mimosa](https://juejin.cn/user/1433418892590136)：卡顿优化一直是客户端性能治理的重要方向之一，优化卡顿，将 APP 的用户体验做到极致，在一定程度上能够提升用户的忠诚度和 APP 的市场占有率。本文是货拉拉技术通过检测卡顿以及对卡顿的治理实践的记录，同时也总结了一些在编码阶段就规避卡顿的方法。

3、[云音乐 iOS 端代码静态检测实践](https://mp.weixin.qq.com/s/5ZcGBCnrUYwUA0RXyPJt9w "云音乐iOS端代码静态检测实践") -- 网易云音乐技术团队

[@Mimosa](https://juejin.cn/user/1433418892590136)：本文是网易云音乐技术团队保障代码质量、防止代码劣化的一套静态代码检测实践，文中代码详尽，步骤也很清晰地记录了通过定制 OCLint 并自定义规则、优化静态检测耗时的过程。

4、[Swift Package Manager 工程实践](https://mp.weixin.qq.com/s/q7jolU99K7FI9JvAxjwRwg "Swift Package Manager 工程实践") -- 狐友技术团队

[@Mimosa](https://juejin.cn/user/1433418892590136)：本文将详细介绍狐友团队在引入 Swift Package Manager 进行工程实践中，探索和累积的相关知识和实践经验，我们将从结构设计、资源处理、链接方式的选择、编译与链接参数设置、异常处理，这五个方面展开详细介绍，每个小部分结尾都提供了最佳实践的总结。

5、[5-Second Test](https://babich.biz/5-second-test-in-product-design/ "5-Second Test") -- Nick Babich

[@Mimosa](https://juejin.cn/user/1433418892590136)：5 秒测试是一个简单的练习，可以帮助衡量用户对您的设计的第一印象。本文是有关如何使用此类测试的快速指南，对于 app 开发来说，对我们的产品设计有点作用。

6、[百度APP iOS端内存优化实践-内存管控方案](https://mp.weixin.qq.com/s/dETOGD3NYU2SdZhxGu0SZg) --  百度App技术

[@Hello World](https://juejin.cn/user/2999123453164605/posts)：内存问题是业务开发中经常被忽视的问题，恰恰它又是很多 Crash 的罪魁祸首。例如 OOM，如何治理内存成了开发中的重要一环。本文从基础原理出发讲述了如何监控内存。并从源码角度分析了应该如何选取内存指标作为衡量的阈值。

***

> 本期将推荐最近的一些优秀博文

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[Swift 正则速查手册](https://onevcat.com/2022/11/swift-regex/ "Swift 正则速查手册") -- 来自：王巍

[@东坡肘子](https://www.fatbobman.com/): 与其他语言和平台相比，正则表达式一直是 Swift 语言一个相当大的痛点。Swift 5.7 引入了大量与正则表达式相关的改进。作者在本文中对与新正则有关的话题、方法与示例进行了详尽整理。

2、[深入理解 Aspects 设计原理](http://chuquan.me/2022/11/13/understand-principle-of-aspects/ "深入理解 Aspects 设计原理") -- 来自：楚权

[@东坡肘子](https://www.fatbobman.com/): Aspects 是一款轻量且简易的面向切面编程的框架，其基于 Objective-C Runtime 原理实现。Aspects 允许开发者对类的所有实例的实例方法或单个实例的实例方法添加额外的代码，并且支持设置代码的执行时机。本文记录作者在阅读 Aspects 源码后的一些收获和思考。

3、[Swift 包管理器中的二进制目标](https://www.avanderlee.com/optimization/binary-targets-swift-package-manager/ "Swift 包管理器中的二进制目标") -- 来自：Antoine van der Lee

[@东坡肘子](https://www.fatbobman.com/): Swift Package Manager（SPM）允许软件包将 xcframework bundle 声明为可用目标。该技术通常用于提供对闭源库的访问，并且可以通过减少获取 SPM 存储库所花费的时间来提高 CI 性能。在向项目添加二进制目标时，必须考虑其优缺点，并了解 xcframeworks 在它们支持的平台上所能发挥作用。

4、[如何在 SwiftUI 中创建条形图](https://mp.weixin.qq.com/s/xPykVjkb9aLtu8rha3tQqA) -- 来自：Swift 社区

[@东坡肘子](https://www.fatbobman.com/): Apple 在 WWDC 2022 期间宣布了一个名为 Swift Charts 的全新框架，方便开发者创建与苹果官方水准相当的图表应用。本文是 Swift 社区推出的有关 Swift Charts 系列文章中的一篇，其他内容还包括：[如何创建折线图](https://mp.weixin.qq.com/s/V_qXskB41WYHwaPdV877mg)、[在 Swift 图表中使用 Foudation 库中的测量类型](https://mp.weixin.qq.com/s/V_qXskB41WYHwaPdV877mg) 等内容。

5、[用 ViewInspector 进行 SwiftUI 视图的单元测试](https://augmentedcode.io/2022/11/14/basic-unit-tests-for-swiftui-view-with-viewinspector/ "用 ViewInspector 进行 SwiftUI 视图的单元测试") -- 来自：Toomas Vahter

[@东坡肘子](https://www.fatbobman.com/): 为 UIKit 代码编写单元测试很容易，但对于 SwiftUI 的视图来说则要困难许多。目前主要通过两种途径进行这项工作：使用 pointfreeco 的 SnapshotTesting 库进行快照测试或使用 ViewInspector 检查视图。作为 ViewInspector 的作者， Toomas Vahter 将通过本文向你展示如何为 SwiftUI 的视图构建单元测试。

6、[Ask Apple 2022 十月问答汇总](https://www.fatbobman.com/tags/ask-apple-2022/ "Ask Apple 2022 十月问答汇总") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): Ask Apple 为开发者与苹果工程师创造了在 WWDC 之外进行直接交流的机会。作者用四篇文章对 10 月份活动中与 SwiftUI 和 Core Data 有关的问答内容进行了整理。或许是受到开发者对本次活动正向反馈的鼓励，在本周苹果继续举办了 Ask Apple 活动，有逐步常态化的趋势。其中【集锦-简体中文】频道不仅会对英文问答进行汇总，同时也会用中文为开发者解答各类问题，希望广大开发者能够踊跃参与。

***

整理编辑：[远恒之义](https://github.com/eternaljust)

1、[在 SwiftUI 中创建自适应的程序化导航方案](https://www.fatbobman.com/posts/adaptive-navigation-scheme/ "在 SwiftUI 中创建自适应的程序化导航方案") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：随着苹果对 iPadOS 的不断投入，越来越多的开发者都希望自己的应用能够在 iPad 中有更好的表现。尤其当用户开启了台前调度（ Stage Manager ）功能后，应用对不同视觉大小模式的兼容能力就越发显得重要。本文将就如何创建可自适应不同尺寸模式的程序化导航方案这一内容进行探讨。

2、[简介 iOS 16 新的 Layout 协议](https://www.appcoda.com.tw/ios16-layout-protocol/ "简介 iOS 16 新的 Layout 协议") -- 来自：appcoda

[@远恒之义](https://github.com/eternaljust)：在 iOS 16 中，Apple 推出了 Layout 协议，希望进一步简化在 SwiftUI 构建 UI Layout 的步骤。本文将介绍这个新协议的用途和使用方法，并用它们的 Layout 规则创建属于自己的容器。

3、[Swift project in 2023](https://www.swift.org/blog/focus-areas-2023/ "Swift project in 2023") -- 来自：swift.org

[@远恒之义](https://github.com/eternaljust)：来自 Swift 官网博客的消息，Swift 核心团队收集并整理了社区和论坛所关注的信息，列出了他们明年的工作计划和内容。其中核心团队会更新重组，将创建更多工作组，包括一个致力于提高 Swift 跨平台可用性的工作组。语言工作组专注于在五个主要语言领域：Concurrency（并发）、Generics（泛型）、Ownership（内存所有权）、Macros（宏）和 C++ interoperability（C++ 互操作性）。同时编译器开发团队将改进编译器与构建系统和自身其他调用的交互方式。其他还包括对 Swift 包管理器的优化，文档工作组将开发工具来解决文档需求，网站工作组专注于通过多种方式增强 swift.org 网站，服务器工作组专注于提升服务器和 Linux 上的 Swift 状态等。

4、[如何在 SwiftUI 中使用手势](https://www.swiftanytime.com/gestures-in-swiftui/ "如何在 SwiftUI 中使用手势") -- 来自：swiftanytime

[@远恒之义](https://github.com/eternaljust)：在如今的触摸屏手机中，实体按键快消失殆尽了，几乎所有的操作都基于手指手势。现代手机可以识别多种手势感应：点击、拖动、滑动、捏合、双击、旋转、摇动、触摸和长按等等，本文将介绍 SwiftUI 中一些基本且最常用的手势使用。

5、[SwiftUI 按钮的基本用法](https://sarunw.com/posts/swiftui-button-basic/ "SwiftUI 按钮的基本用法") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：SwiftUI 中的按钮十分方便使用和自定义。按钮界面很简单，只需要做两件事：动作和标签。动作是一种方法或闭包，当用户单击或点击按钮时会调用它，标签是描述按钮用途的视图，可以是文本、图标图像或任何自定义视图。使用自定义按钮也非常容易，任选 `buttonStyle(_:)` 内置五种按钮样式之一即可。

6、[如何在 SwiftUI 中使用自定义字体](https://sarunw.com/posts/swiftui-custom-font/ "如何在 SwiftUI 中使用自定义字体") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：要在 SwiftUI 中使用自定义字体，你需要执行以下步骤：查找在你的应用中能免费使用的自定义字体；将字体文件添加到你的 Xcode 项目，同时在 Info.plist 中引入注册；最后使用 `custom(_:size:)` 方法来初始化字体。

***

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

1、[当谈论协程时，我们在谈论什么](https://mp.weixin.qq.com/s/IO4ynnKEfy2Rt-Me7EIeqg)  -- 来自： 腾讯程序员

[@夏天](https://juejin.cn/user/3298190611456638): 本文详细介绍了协程的概念，作者通过文章来回答了四个问题： 

* **Q1 (Why):** 为什么需要协程？
* **Q2 (What):** 到底什么是协程？
* **Q3 (How):** 怎么实现协程 (库)？
* **Q4 (Usage):** 使用协程时需要注意什么？

不但能够帮助你理解协程，而且文章结构清晰。

2、[Be careful with Obj-C bridging in Swift](https://swiftrocks.com/be-careful-with-objc-bridging-in-swift "Be careful with Obj-C bridging in Swift") -- 来自：SwiftRocks

[@夏天](https://juejin.cn/user/3298190611456638): 当我们要将 Swift 中 `String` 转为 `NSString` 时，一般使用 `as` 语法糖来进行转换，但是作者认为这并不是一个安全的方案。 

3、[Understanding `@inlinable` in Swift](https://swiftrocks.com/understanding-inlinable-in-swift "Understanding `@inlinable` in Swift") -- 来自：SwiftRocks

[@夏天](https://juejin.cn/user/3298190611456638): 了解 `@inlinable` 是如何工作的，通过使用 `@inlinable` 可以提高我们的某些代码的性能。

4、[App Store and TestFlight review times](https://www.runway.team/appreviewtimes "App Store and TestFlight review times") --  来自：RUNWAY

[@夏天](https://juejin.cn/user/3298190611456638): 一个关于 App Store 和 TestFlight 审核时间的统计的文章。当我们上架到 App Store 和 TestFlight 时，我们大概需要多久才能审核成功。


***

> 本期将推荐近期的一些优秀博文，涵盖 ChatGPT、SwiftUI、Swift 等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[注册 ChatGPT 全攻略](https://zhuanlan.zhihu.com/p/589365506 "注册 ChatGPT 全攻略") -- 来自：BoxChen

[@东坡肘子](https://www.fatbobman.com/): 上周 IT 届最火爆的新闻莫过于 OpenAI 推出了用于人机交流的 ChatGPT 模型。遗憾的是，由于验证码的关系，国内开发者很难亲身体验。本文将介绍通过接入码平台实现注册的全过程。由于原文网站访问不便，附带的是知乎转载的地址。

2、[用 OpenAI 的 ChatGPT 会话机器学习模型为 SwitfUI 应用程序创建工作代码](https://www.createwithswift.com/prototyping-swiftui-interfaces-with-openais-chatgpt/ "用 OpenAI 的 ChatGPT 会话机器学习模型为 SwitfUI 应用程序创建工作代码") -- 来自：Moritz Philip Recke

[@东坡肘子](https://www.fatbobman.com/): 最近一段时间，OpenAI 发布了许多人工智能 API 和机器学习模型，支持文本摘要、翻译、解析非结构化数据、分类、文本组合等用例。最新添加的是一个名为 ChatGPT 的模型，它是作为对话工具实现的。本文将介绍如何使用 OpenAI 的 ChatGPT 会话机器学习模型为 SwitfUI 应用程序创建工作代码。

3、[在 SwiftUI 中构建自定义布局](https://swiftwithmajid.com/2022/11/16/building-custom-layout-in-swiftui-basics/ "在 SwiftUI 中构建自定义布局") -- 来自：Majid

[@东坡肘子](https://www.fatbobman.com/): SwiftUI 4 中提供了 Layout 协议，允许开发者在不使用GeometryReader 的情况下挖掘布局系统来构建自定义布局。作者将通过三篇文章（ 基础、缓存、间距 ）介绍如何通过新的布局协议在 SwiftUI 中构建布局。

4、[MacOS Ventura 系统 ssh 不再支持 ssh-rsa 的原因及解决办法](https://blog.twofei.com/881/ "MacOS Ventura 系统 ssh 不再支持 ssh-rsa 的原因及解决办法") -- 来自：桃子

[@东坡肘子](https://www.fatbobman.com/): 升级到 MacOS Ventura 系统后，如果尝试使用 ssh 登录服务器，大概率会发现无法登录。本文将分析出现问题的原因并提供解决的办法。

5、[SwiftUI 与 Core Data](https://www.fatbobman.com/posts/modern-Core-Data-Problem/ "SwiftUI 与 Core Data") -- 来自：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 如何让 Core Data 融入流行的应用架构体系，在 SwiftUI、TCA、Unit Tests、Preview 等环境下更加顺畅地工作已成为很多开发者当前主要困扰。作者将通过几篇文章来介绍近半年来在这方面的一些想法、收获、体会及实践。

6、[Swift Error](https://juejin.cn/post/7130593449174106149/ "Swift Error") -- 来自：移动端小伙伴

[@东坡肘子](https://www.fatbobman.com/): 在开发中，往往最容易被忽略的内容就是对错误的处理。有经验的开发者，能够对自己写的每行代码负责，而且非常清楚自己写的代码在什么时候会出现异常，这样就能提前做好错误处理。Swift Error Handling 能够让开发者快速而简便的告知编译器一个函数能否抛出错误，并且在抛出后以合适的方式去处理错误。作者将通过两篇文章对 Swift Error 的用法、特点、优化等内容进行介绍。

***

整理编辑：[Mim0sa](https://juejin.cn/user/1433418892590136/posts)

1、[源码探索SwiftUI框架—TCA](https://juejin.cn/post/7164699554711863326 "源码探索SwiftUI框架—TCA") -- 来自：合合信息

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：本文将会详细的带你体验 TCA 框架该如何去使用，从定义、绑定到调用，并从源码探析整个流程的逻辑，清晰易懂。同时 TCA 也还在快速的发展和推进中，可以期待 TCA 的完善。

2、[《游戏学导论》- 笔记](http://pjhubs.com/2022/01/29/game05/ "《游戏学导论》- 笔记") -- 来自：PJHubs

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：这是一份博主学习华科熊硕老师的《游戏学导论》的系列笔记文章，主要讨论了游戏作为人文社会的一部分中，人与游戏之间的关系和理解，感兴趣的朋友可以读一下。

3、[GCDWebServer 使用详解](https://xiaovv.me/2018/11/30/GCDWebServer-BasicUse/ "GCDWebServer 使用详解") -- 来自：笑忘书店

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：GCDWebServer 是一个基于 GCD 的轻量级服务器框架，使用 GCDWebServer 我们可以很轻松的在我们的应用中搭建一个 HTTP 服务器，比如可以使用 GCDWebServer 来实现一个无线U盘 App。该篇文章比较详细的讲解了这个框架的主要使用流程，有两种语言的实现，代码内容详实。

4、[SwiftOnTap](https://swiftontap.com/ "SwiftOnTap") -- 来自：SwiftOnTap

[@Mim0sa](https://juejin.cn/user/1433418892590136/posts)：这是一份看起来很像官方文档，但是又比官方文档详细很多的 SwiftUI 文档，由一些 iOS 开发者一起维护，将一些在官方文档上写的不清楚、不详细的地方重新编写，填补了 Apple 文档的一些漏洞，其中各种 UI 类的实现还有动画和图片作为辅佐，很好用。

***

整理编辑：[@远恒之义](https://github.com/eternaljust)

1、[SwiftUI 与 Core Data —— 安全地响应数据](https://www.fatbobman.com/posts/modern-Core-Data-Respond-Data-safely/ "SwiftUI 与 Core Data —— 安全地响应数据") -- 来自：东坡肘子

[@远恒之义](https://github.com/eternaljust)：保证应用不因 Core Data 的原因导致意外崩溃是对开发者的起码要求。本文将介绍可能在视图中产生严重错误的原因，如何避免，以及在保证视图对数据变化实时响应的前提下如何为使用者提供更好、更准确的信息。

2、[如何使用 SwiftUI Grid API 创建网格布局](https://www.appcoda.com.tw/swiftui-grid-api/ "如何使用 SwiftUI Grid API 创建网格布局") -- 来自：Simon Ng

[@远恒之义](https://github.com/eternaljust)：Grid 视图是一种容器视图，它以二维布局排列其他视图，Grid 为开发人员提供了构建基于网格的布局的更多选项。你可以使用 HStack 和 VStack 来构建类似的布局，不过 Grid 视图可以为你节省大量代码并使你的代码可读性更高，你可以尝试使用 Grid 来构建一些有趣的布局。

3、[如何对 SwiftUI list 中的列表行进行重新排序](https://sarunw.com/posts/swiftui-list-onmove/ "如何对 SwiftUI list 中的列表行进行重新排序") -- 来自：sarunw

[@远恒之义](https://github.com/eternaljust)：想要启用 SwiftUI 列表行重新排序，你只需执行以下步骤即可：创建数据源（必须是可变的）、使用填充列表视图 `ForEach`、将 `onMove(perform:)` 修饰符应用于 `ForEach`、手动移动项目 `onMove` 的闭包，调用方法十分简单方便。

4、[如何创建 iOS 锁屏小部件？](https://swiftsenpai.com/development/create-lock-screen-widget/?utm_source=rss&utm_medium=rss&utm_campaign=create-lock-screen-widget "如何创建 iOS 锁屏小部件？") -- 来自：Lee Kah Seng

[@远恒之义](https://github.com/eternaljust)：在 iOS 16 中，Apple 新增了锁定屏幕，其中锁屏小组件带来 app 新的曝光入口。与桌面小组件类似，锁屏小组件主要用 WidgetKit 来实现功能。不同的是，Apple 引入了 3 个新的不同类型的锁屏小组件：`accessoryCircular`、`accessoryRectangular` 和 `accessoryInline`，前两个为小与中两种尺寸，后者为单行文本。

5、[用 SwiftUI 实现 AI 聊天对话 app - iChatGPT](https://juejin.cn/post/7175051294808211512 "用 SwiftUI 实现 AI 聊天对话 app - iChatGPT") -- 来自掘金：37手游iOS技术运营团队

[@远恒之义](https://github.com/eternaljust)：iChatGP 是一款用 SwiftUI 实现的开源 ChatGPT app，支持系统 iOS 14.0+、iPadOS 14.0+、macOS 11.0+，目前已实现 ChatGPT 基本聊天功能：直接与 ChatGPT 对话，并且保留上下文；复制问题和回答内容；快捷重复提问。

6、[EBPF 介绍](https://coolshell.cn/articles/22320.html "EBPF 介绍") -- 来自：酷壳

[@远恒之义](https://github.com/eternaljust)：eBPF（extened Berkeley Packet Filter）是一种内核技术，它允许开发人员在不修改内核代码的情况下运行特定的功能。eBPF 比起传统的 BPF 来说，传统的 BPF 只能用于网络过滤，而 eBPF 则可以用于更多的应用场景，包括网络监控、安全过滤和性能分析等。耗子叔在文末留了一个彩蛋，聊了聊他对大火的 ChatGPT 一些看法。


***

> 本期将推荐近期的一些优秀博文，涵盖如何保护剪切板内容、SwiftUI 的视图风格、iOS 应用启动优化等方面的内容

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[如何防止复制和粘贴到其他 iOS 应用程序中](https://blog.eidinger.info/prevent-copy-paste-into-other-ios-apps "如何防止复制和粘贴到其他 iOS 应用程序中") -- 来自：Marco Edinger

[@东坡肘子](https://www.fatbobman.com/): 在企业应用程序中，经常需要通过防止最终用户将内容复制和粘贴到其他应用程序中来保护敏感信息。在这篇文章中，作者将向你展示为 iOS 应用程序引入这种高级剪贴板保护功能的多种方法。

2、[掌握 Swift Concurrency 的 AsyncStream](https://www.donnywals.com/understanding-swift-concurrencys-asyncstream/ "掌握 Swift Concurrency 的 AsyncStream") -- 来自：Donny wals

[@东坡肘子](https://www.fatbobman.com/): 创建自定义的异步序列的最好方法是什么？实现 AsyncSequence 协议并构建你的 AsyncIterator 确实可以解决一切问题，但实现起来很繁琐而且容易出错。在这篇文章中，作者将向你展示如何利用 Swift 的 AsyncStream 来构建自定义的异步序列，在你需要的时候产生数值。

3、[SwiftUI 视图的样式 —— 视图样式是如何工作的](https://peterfriese.dev/posts/swiftui-styling-views/ "SwiftUI 视图的样式 —— 视图样式是如何工作的") -- 来自：Peter Friese

[@东坡肘子](https://www.fatbobman.com/): SwiftUI 视图的样式是一个强大的概念，让开发者在设计应用程序时具有很大的灵活性，且不会丢失我们使用的视图的语义。支持此概念的 SwiftUI 视图列表令人印象深刻：按钮、选择器、菜单、切换、指示器、文本和标签、集合视图、导航视图、窗口和工具栏以及组等。因此，下次在你需要定制 UI 元素的特殊外观时，请先查看苹果的文档，看看是否已经有满足你需求的风格。如果没有，本文将告诉你如何创建自定义样式。

4、[Dependencies —— Point Free 发布了新的开源依赖库](https://www.pointfree.co/blog/posts/92-a-new-library-to-control-dependencies-and-avoid-letting-them-control-you "Dependencies —— Point Free 发布了新的开源依赖库") -- 来自：Point Free

[@东坡肘子](https://www.fatbobman.com/): 依赖性是指你的应用程序中需要与不受你控制的外部系统交互的类型和功能。典型的例子是向服务器发出网络请求的 API 客户端，但也有一些看似无害的东西，如 UUID 和日期初始化器、文件访问、用户默认值，甚至时钟和计时器，都可以被认为是依赖关系。Point Free 将 TCA 中广受好评的依赖功能分离出来构建成一个独立且开源的依赖管理系统，以便让更多的开发者受益。

5、[云音乐 iOS 启动性能优化「开荒篇」](https://juejin.cn/post/7145672412883845127 "云音乐 iOS 启动性能优化「开荒篇」") -- 来自：网易云音乐技术团队

[@东坡肘子](https://www.fatbobman.com/): App 启动作为用户使用应用的第一个体验点，直接决定着用户对 App 的第一印象。网易云音乐作为一个有着近 10 年发展历史的 App，随着各种业务不停的发展和复杂场景的堆叠，不同的业务和需求不停地往启动链路上增加代码，这给 App 的启动性能带来了极大的挑战。而随着云音乐用户基数的不断扩大和深度使用，越来越多的用户反馈启动速度慢，况且启动速度过慢更甚至会降低用户的留存意愿。因此，云音乐 iOS App 急需要进行一个专项针对启动性能进行优化。本文将介绍云音乐技术团队在 App 启动优化方面所做出的努力。（ 编者同大多数评论的想法一致，在不解决开屏广告的情况下，一切基于技术层面的优化都很难让用户有较大的感知 ）

