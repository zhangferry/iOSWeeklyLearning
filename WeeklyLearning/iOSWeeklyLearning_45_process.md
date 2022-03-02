# iOS摸鱼周报 第四十二期

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

## 开发Tips

整理编辑：[夏天](https://juejin.cn/user/3298190611456638) [人魔七七](https://github.com/renmoqiqi)



## 面试解析
### Swift的weak是如何实现的？

在Swift中,也是拥有SideTable的，`SideTable` 是针对有需要的对象而创建，系统会为目标对象分配一块新的内存来保存该对象额外的信息。

对象会有一个指向 `SideTable` 的指针，同时 `SideTable` 也有一个指回原对象的指针。在实现上为了不额外多占用内存，目前只有在创建弱引用时，会先把对象的引用计数放到新创建的 `SideTable` 去，再把空出来的空间存放 `SideTable` 的地址，会通过一个标志位来区分对象是否有 `SideTable`。

```Swift 
    class JYObject{
        var age :Int = 18
        var name:String = "JY"
    }
     
      var t = JYObject()
        
      weak var t2 = t
        
      print("----")
```

我们在`print`处打上断点，查看t2对象

```C
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
HeapObjectSideTableEntry* RefCounts<InlineRefCountBits>::formWeakReference()
{
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
HeapObjectSideTableEntry* RefCounts<InlineRefCountBits>::allocateSideTable(bool failIfDeiniting)
{
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
     
  } while (! refCounts.compare_exchange_weak(oldbits, newbits,
                                             std::memory_order_release,
                                             std::memory_order_relaxed));
  return side;
}
```

> 总结一下上面所做的事情
>
> 1.拿到原有的引用计数
> 2.通过HeapObject创建了一个HeapObjectSideTableEntry实例对象
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

我们来尝试还原一下 拿到弱引用计数 

`0xc0000c00001f03dc`62位和63位清0得到 `HeapObjectSideTableEntry` 实例对象的地址`0xC00001F03DC`

它既然是右移 3 位，那么我左移 3 位把它还原，`HeapObjectSideTableEntry`左移三位 得到`0x10062AFE0`

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20220302155825.png)


- `0x6000001a9710` 就是实例对象的地址
- `0x0000000000000002`就是弱引用计数
  这里弱引用为`2`的原因是因为`SideTableRefCountBits`初始化的时候从`1`开始


`Side Table`的生命周期与对象是分离的，当强引用计数为 0 时，只有 `HeapObject` 被释放了，并没有释放`Side Table`，只有所有的 `weak` 引用者都被释放了或相关变量被置 `nil` 后，`Side Table` 才能得以释放

整理编辑：[JY](https://juejin.cn/user/1574156380931144)


## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)、[我是熊大](https://juejin.cn/user/1151943916921885)




## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)



## 工具推荐

整理编辑：[zhangferry](https://zhangferry.com)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS摸鱼周报 第十七期](https://mp.weixin.qq.com/s/3vukUOskJzoPyES2R7rJNg)

[iOS摸鱼周报 第十六期](https://mp.weixin.qq.com/s/nuij8iKsARAF2rLwkVtA8w)

[iOS摸鱼周报 第十五期](https://mp.weixin.qq.com/s/6thW_YKforUy_EMkX0OVxA)

[iOS摸鱼周报 第十四期](https://mp.weixin.qq.com/s/br4DUrrtj9-VF-VXnTIcZw)

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/WechatIMG384.jpeg)
