# 使用Category覆写系统方法问题讨论

这是一次非常有趣的解决问题经历，以至于我认为思路可能比问题本身更有意思。

首次提出这个问题的是[反向抽烟]()，我验证了这个奇怪的现象，并决定好好探究一下，即使重看了 Category 的源码但并没有找到合理解释，于是将这个问题抛到开发群里，最后由[皮拉夫大王]()给出了最为合理的解释。以下是这一过程的经历。

## 问题提出

**背景**：想为 UITextField 提供单独的属性 placeholderColor ，用来直接设置占位符的颜色，这个时候使用分类设置属性，重写 setter 和 getter，set中直接使用 KVC 的方式对属性的颜色赋值；这个时候就有个bug，如果在其他类中使用 UITextField 这个控件的时候，先设置颜色，再设置文字，会发现占位符的颜色没有发生改变。

**解决思路**：首先想到 UITextField 中的 Label 是使用的懒加载，当有文字设置的时候，就会初始化这个label，这时候就考虑先设置颜色根本就没起到作用；

**解决办法**：在分类中 placeholderColor 的 setter 方法中，使用runtime的`objc_setAssociatedObject`先把颜色保存起来，这样就能保证先设置的颜色不会丢掉，然后需要重写 `placeholder`的setter方法，让在设置完文字的时候，拿到先前保存的颜色，故要在`placeholderColor` 的getter中用`objc_getAssociatedObject`取，这里有个问题点，在分类中重写 `placeholder` 的setter方法的话，在外面设置 `placeholder` 的时候，根本不走自己重写的这个 `setPlaceholder`方法，而走系统自带的，这里我还没研究。然后为了解决这个问题，我自己写了个`setDsyPlaceholder方法`，在`setDsyPlaceholder`里面对标签赋值，同时添加已经保存好的颜色，然后与`setPlaceholder`做交换，bug修复。



这里大家先不要关注解决 placeholderColor 的方式是否正确，以免思路走偏。**首先应该避免使用Category 覆写系统方法**，但这里引出了一个问题：如果就是要覆写系统的方法，为啥没被执行呢。

## 问题探索

我测试发现自定义类是可以通过 Category 覆写的，当时选的是 UIViewController 的viewDidLoad 方法，其他几个 UIViewController 方法也试了都不可以。

所以猜测：**系统方法被做了特殊处理都不能覆写，只有自定义类可以覆写**。

有一个解释是：系统方法是会被缓存的，方法查找走了缓存，没有查完整的方法表。

这个说法好像能说得通，但是系统缓存是库的层面，方法列表的缓存又是另一个维度了。方法列表的缓存应该是应用间独立进行的，这样才能保证不同应用对系统库的修改不会相互影响。



这时有朋友提出他们之前使用Category 覆写过 UIScreen 的 mainScreen，是可以成功的。我试了下确实可以，观察之后发现该属性是一个类属性。又试了其他几个系统库的类属性，也都是可以的。

所以猜测变成了：**只有系统实例方法不能被覆写，类属性，类方法可以覆写**。

这时已经感觉奇怪了，这个规律也说不通。后来有朋友测试通过 Xcode10.3 能够覆写系统方法，好嘛。。。

这时的猜测变成了：**苹果在某个版本开始才做了系统方法覆写的拦截**。

## 可靠的证据

[皮拉夫大王在此]()验证了iOS12系统可以覆写（后来验证iOS13状况相同），iOS14不能覆写。

但iOS14的情况并不是所有的系统方法都覆盖不了，能否覆盖与类方法还是实例方法无关。
例如：`UIResponder`的分类，重写`init` 和 `isFirstResponder`，`init`可以覆盖，`isFirstResponder`不能覆盖。在iOS14的系统上NS的类，很多都可以被分类覆盖，但是UIKit的类，在涉及到UI的方法时，很多都无法覆盖。

这里猜测：**系统做了白名单，命中白名单的函数会被系统拦截和处理**。

以下是对 iOS14 状况的验证，覆写`isFirstResponder`，打印`method_list`：
```c
unsigned int count;
Method *list = class_copyMethodList(UIResponder.class, &count);
for (int i = 0; i < count; i++) {
    Method m = list[i];
    if ([NSStringFromSelector(method_getName(m)) isEqualToString:@"isFirstResponder"]) {
        IMP imp = method_getImplementation(m);
    }
}
```

`isFirstResponder`会命中两次，两次`po imp`的结果是：

```
//第一次
(libMainThreadChecker.dylib`__trampolines + 67272)
//第二次
(UIKitCore`-[UIResponder isFirstResponder])
```

同样的代码，在iOS12的设备也会命中两次，结果为：

```
//第一次
(SwiftDemo`-[UIResponder(xx) isFirstResponder] at WBOCTest.m:38)
//第二次
(UIKitCore`-[UIResponder isFirstResponder])
```

所以可以确认的是，分类方法是可以正常添加到系统类的，但在iOS14的系统中，覆写的方法却被`libMainThreadChecker.dylib`里的方法接管了，导致没有执行。

那么问题来了，这个`libMainThreadChecker.dylib`库是干嘛的，它做了什么？

Main Thread Checker是在Xcode9新增的功能，因为开销比较小，只占用1-2%的CPU，启动时间占用时间不到0.1s，所以被默认置为开的状态。它在调试期的普遍用法是用于帮助我们定位那些应该在主线程执行，却没有放到主线程的情况。

另外官方文档还有一个[解释](https://developer.apple.com/documentation/xcode/diagnosing_memory_thread_and_crash_issues_early?language=objc "Diagnosing Memory, Thread, and Crash Issues Early")：

> The Main Thread Checker tool dynamically replaces system methods that must execute on the main thread with variants that check the current thread. The tool replaces only system APIs with well-known thread requirements, and doesn’t replace all system APIs. Because the replacements occur in system frameworks, Main Thread Checker doesn’t require you to recompile your app.

这个家伙会动态的替换尝试重写需要在主线程执行的系统方法，但也不是所有的系统方法。这很好的解释了为什么本应被覆盖的系统方法却指向了`libMainTreadChecker.dylib`这个库，同时也解释了为什么有些方法可以覆写，有些却不可以。

测试发现当我们关闭了这个开关，iOS14的设备就可以正常执行覆写的方法了。

到此基本完事了，但还有一个问题没有解释，那就是为什么iOS14之前的设备，不受这个开关的影响？没有找到实质的证据，表明苹果是如何处理的，但是通过以上实验可以推测 iOS14 的设备确实是有这方面的特殊处理的。





