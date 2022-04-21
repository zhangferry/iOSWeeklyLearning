************************************************
整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。

### 输入网址进入网页按回车刷新网页都发生了什么？URL 输入到显示的过程？

1. **DNS 解析**：当用户输入一个网址并按下回车键的时候，浏览器获得一个域名，而在实际通信过程中，我们需要的是一个 IP 地址，因此我们需要先把域名转换成相应 IP 地址；
2. **TCP 连接**：浏览器通过 DNS 获取到 Web 服务器真正的 IP 地址后，便向 Web 服务器发起 TCP 连接请求，通过 TCP 三次握手建立好连接后，浏览器便可以将 HTTP 请求数据发送给服务器了；
3. **发送 HTTP 请求**：浏览器向 Web 服务器发起一个 HTTP 请求，HTTP 协议是建立在 TCP 协议之上的应用层协议，其本质是在建立起的 TCP 连接中，按照 HTTP 协议标准发送一个索要网页的请求。在这一过程中，会涉及到负载均衡等操作；
4. **处理请求并返回**：服务器获取到客户端的 HTTP 请求后，会根据 HTTP 请求中的内容来决定如何获取相应的文件，并将文件发送给浏览器；
5. **浏览器渲染**：浏览器根据响应开始显示页面，首先解析 HTML 文件构建 DOM 树，然后解析 CSS 文件构建渲染树。如果页面有 JavaScript 脚本文件，那么 JavaScript 文件下载完成并加载后，通过 DOM API 和 CSSOM API 来操作渲染树，等到渲染树构建完成后，浏览器开始布局渲染树并将其绘制到屏幕上；
6. **断开连接**：客户端和服务器通过四次挥手终止 TCP 连接。

### 拥塞控制有哪些阶段？如何实现拥塞控制？TCP 的拥塞控制解释一下？

1. 拥塞控制考虑整个网络，是全局性的考虑；
2. **慢启动算法**：由小到大逐渐增加发送数据量，每收到一个报文确认就加 1 倍的报文数量，以指数规律增长，增长到慢启动阈值后就不增了；
3. **拥塞避免算法**：维护一个拥塞窗口的变量，只要网络不拥塞，就试探着拥塞窗口调大，以加法规律增长，该算法可以保证在网络不拥塞的情况下，发送更多的数据；
4. **快速重传**：接收端收到的序列号不连续时，连发 3 个重复的确认报文给发送方；
5. **快速恢复**：拥塞窗口变为原来的一半，阈值也变为发生拥塞时大小的一半，继续拥塞避免算法。

### TCP 怎么保证可靠传输？TCP 怎样实现可靠传输的？TCP 为什么可以保证可靠传输？怎么理解 TCP 的连接，可靠和字节流？

1. **数据分块**：应用数据被分割成 TCP 认为最适合发送的数据块；
2. **序列号和确认应答**：TCP 给发送的每一个包进行编号，在传输的过程中，每次接收方收到数据后，都会对传输方进行确认应答，即发送 ACK 报文，这个 ACK 报文当中带有对应的确认序列号，告诉发送方成功接收了哪些数据以及下一次的数据从哪里开始发。除此之外，接收方可以根据序列号对数据包进行排序，把有序数据传送给应用层，并丢弃重复的数据；
3. **校验和**：TCP 将保持它首部和数据部分的检验和。这是一个端到端的检验和，目的是检测数据在传输过程中的任何变化。如果收到报文段的检验和有差错，TCP 将丢弃这个报文段并且不确认收到此报文段；
4. **流量控制**：TCP 连接的双方都有一个固定大小的缓冲空间，发送方发送的数据量不能超过接收端缓冲区的大小。当接收方来不及处理发送方的数据，会提示发送方降低发送的速率，防止产生丢包。TCP 通过滑动窗口协议来支持流量控制机制；
5. **拥塞控制**：当网络某个节点发生拥塞时，减少数据的发送；
6. **ARQ 协议**：也是为了实现可靠传输的，它的基本原理就是每发完一个分组就停止发送，等待对方确认。在收到确认后再发下一个分组；
7. **超时重传**：当 TCP 发出一个报文段后，它启动一个定时器，等待目的端确认收到这个报文段。如果超过某个时间还没有收到确认，将重发这个报文段。

***
整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**计算机网络**，以下题目均来自真实面试场景。计算机网络是面试必考的知识点，最好比较系统的去学习了解，推荐书籍：《图解 TCP/IP》、《网络是怎样连接的》；推荐付费课程：[计算机网络通关 29 讲](https://t7.lagounews.com/RR7FRYRDsi3B1 "计算机网络通关 29 讲")，大家可以根据自己喜欢的学习方式进行选择。


### 什么是 TCP 的三次握手和四次挥手？

我们先来看一下 TCP 报文头部结构：

![](http://cdn.zhangferry.com/Images/20210704165732.png)

握手阶段主要依靠以下几个标志位：
* SYN：在建立连接时使用，用来同步序号。SYN=1 代表这是一个请求建立连接或同意建立连接的报文，只有前两次握手中 SYN 才为 1，带 SYN 标志的 TCP 报文段称为同步报文段；
  * 当 SYN=1，ACK=0 时，表示这是一个请求建立连接的报文段
  * 当 SYN=1，ACK=1 时，表示对方同意建立连接
* ACK：表示前面确认号字段是否有效。ACK=1 代表有效。带 ACK 标志的 TCP 报文段称为确认报文段；
* FIN：表示通知对方本端数据已发送完毕，要关闭连接了。带 FIN 标志的 TCP 报文段称为终止报文段。

**三次握手是指建立一个 TCP 连接时，需要客户端和服务端总共发送 3 个包，需要三次握手才能确认双方的接收与发送能力是否正常。**

![](http://cdn.zhangferry.com/Images/20210703051424.png)

1. 客户端向服务端发起连接请求，需要发送一个 SYN 报文到服务端。
2. 当服务端收到客户端发过来的 SYN 报文后，返回给客户端 SYN、ACK 报文。`这时候服务端可以确认客户端的发送能力和自己的接收能力正常`。
3. 客户端收到该报文。`这时候客户端可以确认双方的发送和接收能力都正常`。然后客户端再回复 ACK 报文给服务端，服务端收到该报文。`这时候服务端可以确认客户端的接收能力和自己的发送能力正常。所以这时候双方都可以确认自己和对方的接收与发送能力都正常`。就这样客户端和服务端通过 TCP 建立了连接。

**四次挥手的目的是关闭一个 TCP 连接。**

![](http://cdn.zhangferry.com/Images/20210703051443.png)

1. 客户端主动发起连接断开，发送一个 FIN 报文到服务端；
2. 服务端返回给客户端 ACK 报文。此时服务端处于关闭等待状态，而不是立马给客户端发 FIN 报文，这个状态还要持续一段时间，因为服务端可能还有数据没发完。`此时客户端到服务端的连接已经断开。但客户端和服务端之间所建立的 TCP 连接通道是全双工的，此时只是处于半关闭状态，所以服务端到客户端可能还会传递数据`；
3. 当服务端的数据都发送完毕后，给客户端发送一个 FIN，ACK 报文；
4. 客户端回应一个 ACK 报文。注意客户端发出 ACK 报文后不是立马释放 TCP 连接，而是要经过 2MSL（最长报文段寿命的 2 倍时长）后才释放 TCP 连接。而服务端一旦收到客户端发出的确认报文就会立马释放 TCP 连接，所以服务端结束 TCP 连接的时间要比客户端早一些。`此时服务端到客户端的连接也已经断开，整个 TCP 连接关闭`。


### 为什么 TCP 连接是三次握手？两次不可以吗？

TCP 是一个全双工协议，它要保证双方都具有接收与发送的能力。

因为需要考虑连接时丢包的问题，如果只握手两次，第二次握手时如果服务端发给客户端的确认报文段丢失，此时服务端已经准备好了收发数据（可以理解为服务端已经连接成功），而客户端一直没收到服务端的确认报文，所以客户端就不知道服务端是否已经准备好了（可以理解为客户端未连接成功），这种情况下客户端不会给服务端发数据，也会忽略服务端发过来的数据。

如果是三次握手，即便发生丢包也不会有问题，比如如果第三次握手客户端发的确认报文丢失，服务端在一段时间内没有收到确认报文的话就会重新进行第二次握手，也就是服务端会重发 SYN 报文段，客户端收到重发的报文段后会再次给服务端发送确认报文。


### 为什么 TCP 连接是三次握手，关闭的时候却要四次挥手？

主要是建立连接时接收者的 SYN-ACK 一同发送了，而关闭时 FIN 和 ACK 却不能同时发送，因为断开连接要处理的情况比较多，比如服务器端可能还有发送出的消息没有得到 ACK，也可能服务器资源需要释放等。所以先发一个 ACK 表示已经收到了发送方的请求，等上述情况都有了确定的处理，再发 FIN 表示接收方已经完成了后续工作。

类比现实世界中，你收到了一个 Offer，出于礼貌你先回复一下，然后思考一段时间再回复 HR 最终的结果。


### 为什么客户端发出第四次挥手的确认报文后要等 2MSL 的时间才能释放 TCP 连接？

这里同样是要考虑丢包的问题，如果第四次挥手的报文丢失，服务端没收到确认报文就会重发第三次挥手的报文，这样报文一去一回最长时间就是 2MSL，所以需要等这么长时间来确认服务端确实已经收到了。

参考：[https://zhuanlan.zhihu.com/p/141396896](https://zhuanlan.zhihu.com/p/141396896 "https://zhuanlan.zhihu.com/p/141396896")

***
整理编辑：[反向抽烟](opooc.com)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析会按照主题讲解一些高频面试题，本期面试题是 **block 的变量捕获机制**。

### block 的变量捕获机制

block 的变量捕获机制，是为了保证 block 内部能够正常访问外部的变量。

1、对于全局变量，不会捕获到 block 内部，访问方式为`直接访问`；作用域的原因，全局变量哪里都可以直接访问，所以不用捕获。

2、对于局部变量，外部不能直接访问，所以需要捕获。

* auto 类型的局部变量（我们定义出来的变量，默认都是 auto 类型，只是省略了），block 内部会自动生成一个同类型成员变量，用来存储这个变量的值，访问方式为`值传递`。**auto 类型的局部变量可能会销毁，其内存会消失，block 将来执行代码的时候不可能再去访问那块内存，所以捕获其值**。由于是值传递，我们修改 block 外部被捕获变量的值，不会影响到 block 内部捕获的变量值。
* static 类型的局部变量，block 内部会自动生成一个同类型成员变量，用来存储这个变量的地址，访问方式为`指针传递`。static 变量会一直保存在内存中， 所以捕获其地址即可。相反，由于是指针传递，我们修改 block 外部被捕获变量的值，会影响到 block 内部捕获的变量值。    
* 对于对象类型的局部变量，block 会连同它的所有权修饰符一起捕获。
    * 如果 block 是在栈上，将不会对对象产生强引用
    * 如果 block 被拷贝到堆上，将会调用 block 内部的 `copy(__funcName_block_copy_num)`函数，copy 函数内部又会调用 `assign(_Block_object_assign)`函数，assign 函数将会根据变量的所有权修饰符做出相应的操作，形成强引用（retain）或者弱引用。
    * 如果 block 从堆上移除，也就是被释放的时候，会调用 block 内部的 `dispose(_Block_object_dispose)`函数，dispose 函数会自动释放引用的变量（release）。
* 对于 `__block`（可用于解决 block 内部无法修改 auto 变量值的问题） 修饰的变量，编译器会将 `__block` 变量包装成一个 `__Block_byref_varName_num` 对象。它的内存管理几乎等同于访问对象类型的 auto 变量，但还是有差异。
    * 如果 block 是在栈上，将不会对 `__block` 变量产生强引用
    * 如果 block 被拷贝到堆上，将会调用 block 内部的 copy
    函数，copy 函数内部又会调用 assign 函数，assign 函数将会直接对 `__block` 变量形成强引用（retain）。
    * 如果 block 从堆上移除，也就是被释放的时候，会调用 block 内部的 dispose 函数，dispose 函数会自动释放引用的 `__block` 变量（release）。
    ![](https://user-gold-cdn.xitu.io/2020/2/23/170724cf4ff4b2bd?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
* 被 `__block `修饰的对象类型的内存管理：
    * 如果 `__block` 变量是在栈上，将不会对指向的对象产生强引用
    * 如果 `__block` 变量被拷贝到堆上，将会调用 `__block` 变量内部的 `copy(__Block_byref_id_object_copy)`函数，copy 函数内部会调用 assign 函数，assign 函数又会根据变量的所有权修饰符做出相应的操作，形成强引用（retain）或者弱引用。（注意：这里仅限于 ARC 下会 retain，MRC 下不会 retain，所以在 MRC 下还可以通过 `__block` 解决循环引用的问题）
    * 如果 `__block` 变量从堆上移除，会调用 `__block` 变量内部的 dispose 函数，dispose 函数会自动释放指向的对象（release）。
    
    

掌握了 block 的变量捕获机制，我们就能更好的应对内存管理，避免因使用不当造成内存泄漏。

常见的 block 循环引用为：`self(obj) -> block -> self(obj)`。这里 block 强引用了 self 是因为对于对象类型的局部变量，block 会连同它的所有权修饰符一起捕获，而对象的默认所有权修饰符为 __strong。

```objectivec
self.block = ^{
    NSLog(@"%@", self);
};
```

> 为什么这里说 self 是局部变量？因为 self 是 OC 方法的一个隐式参数。

为了避免循环引用，我们可以使用 `__weak` 解决，这里 block 将不再持有 self。

```objectivec
__weak typeof(self) weakSelf = self;
self.block = ^{
    NSLog(@"%@", weakSelf);
};
```

为了避免在 block 调用过程中 self 提前释放，我们可以使用 `__strong` 在 block 执行过程中持有 self，这就是所谓的 Weak-Strong-Dance。

```objectivec
__weak typeof(self) weakSelf = self;
self.block = ^{
    __strong typeof(self) strongSelf = weakSelf;
    NSLog(@"%@", strongSelf);
};
```

当然，我们平常用的比较多的还是 `@weakify(self)` 和 `@strongify(self)` 啦。

```objectivec
@weakify(self);
self.block = ^{
    @strongify(self);
    NSLog(@"%@", self);
};
```

如果你使用的是 RAC 的 Weak-Strong-Dance，你还可以这样：

```objectivec
@weakify(self, obj1, obj2);
self.block = ^{
    @strongify(self, obj1, obj2);
    NSLog(@"%@", self);
};
```

如果是嵌套的 block：

```objectivec
@weakify(self);
self.block = ^{
    @strongify(self);
    self.block2 = ^{
        @strongify(self);
        NSLog(@"%@", self);
    }
};
```

你是否会疑问，为什么内部不需要再写 @weakify(self) ？这个问题就留给你自己去思考和解决吧！

相比于简单的相互循环引用，block 造成的大环引用更需要你足够细心以及敏锐的洞察力，比如：

```objectivec
TYAlertView *alertView = [TYAlertView alertViewWithTitle:@"TYAlertView" message:@"This is a message, the alert view containt text and textfiled. "];
[alertView addAction:[TYAlertAction actionWithTitle:@"取消" style:TYAlertActionStyleCancle handler:^(TYAlertAction *action) {
    NSLog(@"%@-%@", self, alertView);
}]];
self.alertController = [TYAlertController alertControllerWithAlertView:alertView preferredStyle:TYAlertControllerStyleAlert];
[self presentViewController:alertController animated:YES completion:nil];
```

这里循环引用有两处：

1. `self -> alertController -> alertView -> handlerBlock -> self`
2. `alertView -> handlerBlock -> alertView`

避免循环引用：

```objectivec
TYAlertView *alertView = [TYAlertView alertViewWithTitle:@"TYAlertView" message:@"This is a message, the alert view containt text and textfiled. "];
@weakify(self, alertView);
[alertView addAction:[TYAlertAction actionWithTitle:@"取消" style:TYAlertActionStyleCancle handler:^(TYAlertAction *action) {
    @strongify(self, alertView);
    NSLog(@"%@-%@", self, alertView);
}]];
self.alertController = [TYAlertController alertControllerWithAlertView:alertView preferredStyle:TYAlertControllerStyleAlert];
[self presentViewController:alertController animated:YES completion:nil];
```

> 另外再和你提一个小知识点，当我们在 block 内部直接使用 _variable 时，编译器会给我们警告：`Block implicitly retains self; explicitly mention 'self' to indicate this is intended behavior`。
>
> 原因是 block 中直接使用 `_variable` 会导致 block 隐式的强引用 self。Xcode 认为这可能会隐式的导致循环引用，从而给开发者带来困扰，而且如果不仔细看的话真的不太好排查，笔者之前就因为这个循环引用找了半天，还拉上了我导师一起查找原因。所以警告我们要显式的在 block 中使用 self，以达到 block 显式 retain 住 self 的目的。改用 `self->_variable` 或者 `self.variable`。
> 
> 你可能会觉得这种困扰没什么，如果你使用 `@weakify` 和 `@strongify` 那确实不会造成循环引用，因为 `@strongify` 声明的变量名就是 self。那如果你使用 `weak typeof(self) weak_self = self;` 和 `strong typeof(weak_self) strong_self = weak_self` 呢？

***
整理编辑：[反向抽烟](https://blog.csdn.net/opooc)、[师大小海腾](https://juejin.cn/user/782508012091645)

面试解析是新出的模块，我们会按照主题讲解一些高频面试题，本期主题是**属性及属性关键字**。

### 谈属性及属性关键字

#### @property、@synthesize 和 @dynamic

##### @property

属性用于封装对象中数据，属性的本质是 ivar + setter + getter。

可以用 @property 语法来声明属性。@property 会帮我们自动生成属性的 setter 和 getter 方法的声明。

##### @synthesize

帮我们自动生成 setter 和 getter 方法的实现以及 _ivar。

你还可以通过 @synthesize 来指定实例变量名字，如果你不喜欢默认的以下划线开头来命名实例变量的话。但最好还是用默认的，否则影响可读性。

如果不想令编译器合成存取方法，则可以自己实现。如果你只实现了其中一个存取方法 setter or getter，那么另一个还是会由编译器来合成。但是需要注意的是，如果你实现了属性所需的全部方法（如果属性是 readwrite 则需实现 setter and getter，如果是 readonly 则只需实现 getter 方法），那么编译器就不会自动进行 @synthesize，这时候就不会生成该属性的实例变量，需要根据实际情况自己手动 @synthesize 一下。

```objectivec
@synthesize ivar = _ivar;
```

##### @dynamic

告诉编译器不用自动进行 @synthesize，你会在运行时再提供这些方法的实现，无需产生警告，但是它不会影响 @property 生成的 setter 和 getter 方法的声明。@dynamic 是 OC 为动态运行时语言的体现。动态运行时语言与编译时语言的区别：动态运行时语言将函数决议推迟到运行时，编译时语言在编译器进行函数决议。

```objectivec
@dynamic ivar;
```

以前我们需要手动对每个 @property 添加 @synthesize，而在 iOS 6 之后 LLVM 编译器引入了 `property autosynthesis`，即属性自动合成。换句话说，就是编译器会自动为每个 @property 添加 @synthesize。

那你可能就会问了，@synthesize 现在有什么用呢？

1. 如果我们同时重写了 setter 和 getter 方法，则编译器就不会自动为这个 @property 添加 @synthesize，这时候就不存在 _ivar，所以我们需要手动添加 @synthesize。
2. 如果该属性是 readonly，那么只要你重写了 getter 方法，`property autosynthesis` 就不会执行，同样的你需要手动添加 @synthesize 如果你需要的话，看你这个属性是要定义为存储属性还是计算属性吧。
3. 实现协议中要求的属性。

此外需要注意的是，分类当中添加的属性，也不会 `property autosynthesis` 哦。因为类的内存布局在编译的时候会确定，但是分类是在运行时才加载并将数据合并到宿主类中的，所以分类当中不能添加成员变量，只能通过关联对象间接实现分类有成员变量的效果。如果你给分类添加了一个属性，但没有手动给它实现 getter、setter（如果属性是 readonly 则不需要实现）的话，编译器就会给你警告啦 `Property 'ivar' requires method 'ivar'、'setIvar:' to be defined - use @dynamic or provide a method implementation in this category`，编译器已经告诉我们了有两种解决方式来消除警告：

1. 在这个分类当中提供该属性 getter、setter 方法的实现
2. 使用 @dynamic 告诉编译器 getter、setter 方法的实现在运行时自然会有，您就不用操心了。当然在这里 @dynamic 只是消除了警告而已，如果你没有在运行时动态添加方法实现的话，那么调用该属性的存取方法还是会 Crash。


#### 属性修饰符分类


分类|属性关键字
--|--
原子性|`atomic`、`nonatomic`
读写权限|`readwrite`、`readonly`
方法名|`setter`、`getter`
内存管理|`assign`、`weak`、`unsafe_unretained`、`retain`、`strong`、`copy`
可空性|(`nullable`、`_Nullable` 、`__nullable`)、<br>(`nonnull`、`_Nonnull`、`__nonnull`)、<br>(`null_unspecified`、`_Null_unspecified` 、`__null_unspecified`)、<br>`null_resettable`
类属性|`class`


##### 原子性

属性关键字|用法
-- |--
atomic|原子性（默认），编译器会自动生成互斥锁（以前是自旋锁，后面改为了互斥锁），对 setter 和 getter 方法进行加锁，可以保证属性的赋值和取值的原子性操作是线程安全的，但不包括操作和访问。<br>比如说 atomic 修饰的是一个数组的话，那么我们对数组进行赋值和取值是可以保证线程安全的。但是如果我们对数组进行操作，比如说给数组添加对象或者移除对象，是不在 atomic 的负责范围之内的，所以给被 atomic 修饰的数组添加对象或者移除对象是没办法保证线程安全的。
nonatomic|非原子性，一般属性都用 nonatomic 进行修饰，因为 atomic 耗时。

##### 读写权限

属性关键字|用法
--|--
readwrite|可读可写（默认），同时生成 setter 方法和 getter 方法的声明和实现。
readonly|只读，只生成 getter 方法的声明和实现。为了达到封装的目的，我们应该只在确有必要时才将属性对外暴露，并且尽量把对外暴露的属性设为 readonly。如果这时候想在对象内部通过 setter 修改属性，可以在类扩展中将属性重新声明为 readwrite；如果仅在对象内部通过 _ivar 修改，则不需要重新声明为 readwrite。


##### 方法名

属性关键字|用法
--|--
setter|可以指定生成的 setter 方法名，如 setter = setName。这个关键字笔者在给分类添加属性的时候会用得比较多，为了避免分类方法“覆盖”同名的宿主类（或者其它分类）方法的问题，一般我们都会加前缀，比如 bbIvar，但是这样生成的 setter 方法名就不美观了（为 setBbIvar），于是就使用到了 setter 关键字 `@property (nonatomic, strong, setter = bb_setIvar:) NSObject *bbIvar;`
getter|可以指定生成的 getter 方法名，如 getter = getName。使用示例：`@property (nonatomic, assign, getter = isEnabled) BOOL enabled;`

##### 内存管理

属性关键字|用法
--|--
assign|1. 既可以修饰基本数据类型，也可以修饰对象类型；<br>2. setter 方法的实现是直接赋值，一般用于基本数据类型 ；<br>3. 修饰基本数据类型，如 NSInteger、BOOL、int、float 等；<br>4. 修饰对象类型时，不增加其引用计数；<br>5. 会产生悬垂指针（悬垂指针：assign 修饰的对象在被释放之后，指针仍然指向原对象地址，该指针变为悬垂指针。这时候如果继续通过该指针访问原对象的话，就可能导致程序崩溃）。
weak|1. 只能修饰对象类型；<br>2. ARC 下才能使用；<br>3. 修饰弱引用，不增加对象引用计数，主要可以用于避免循环引用；<br>4. weak 修饰的对象在被释放之后，会自动将指针置为 nil，不会产生悬垂指针；<br>5. 对于视图，通常还是用在 xib 和 storyboard 上；代码中对于有必要进行 remove 的视图也可以使用 weak，这样 remove 之后会自动置为 nil。
unsafe_unretained|1. 既可以修饰基本数据类型，也可以修饰对象类型；<br>2. MRC 下经常使用，ARC 下基本不用；<br>3. 同 weak，区别就在于 unsafe_unretained 会产生悬垂指针；<br>4. weak 对性能会有一定的消耗，当一个对象 dealloc 时，需要遍历对象的 weak 表，把表里的所有 weak 指针变量值置为 nil，指向对象的 weak 指针越多，性能消耗就越多。所以 unsafe_unretained 比 weak 快。当明确知道对象的生命周期时，选择 unsafe_unretained 会有一些性能提升。比如 A 持有 B 对象，当 A 销毁时 B 也销毁。这样当 B 存在，A 就一定会存在。而 B 又要调用 A 的接口时，B 就可以存储 A 的 unsafe_unretained 指针。虽然这种性能上的提升是很微小的。但当你很清楚这种情况下，unsafe_unretained 也是安全的，自然可以快一点就是一点。而当情况不确定的时候，应该优先选用 weak。
retain|1. MRC 下使用，ARC 下基本使用 strong；<br>2. 修饰强引用，将指针原来指向的旧对象释放掉，然后指向新对象，同时将新对象的引用计数加 1；<br>3. setter 方法的实现是 release 旧值，retain 新值，用于 OC 对象类型。
strong|1. ARC 下才能使用；<br>2. 原理同 retain；<br>3. 但是在修饰 block 时，strong 相当于 copy，而 retain 相当于 assign。
copy|setter 方法的实现是 release 旧值，copy 新值，一般用于 block、NSString、NSArray、NSDictionary 等类型。使用 copy 和 strong 修饰 block 其实都一样，用 copy 是为了和 MRC 下保持一致的写法；用于 NSString、NSArray、NSDictionary 是为了保证赋值后是一个不可变对象，以免遭外部修改而导致不可预期的结果。


##### 可空性

[Nullability and Objective-C](https://developer.apple.com/swift/blog/?id=25 "Nullability and Objective-C")

苹果在 Xcode 6.3 引入的一个 Objective-C 的新特性 `nullability annotations`。这些关键字可以用于属性、方法返回值和参数中，来指定对象的可空性，这样编写代码的时候就会智能提示。在 Swift 中可以使用 `?` 和 `!` 来表示一个对象是 `optional` 的还是 `non-optional`，如 `UIView?` 和 `UIView!`。而在 Objective-C 中则没有这一区分，`UIView` 即可表示这个对象是 `optional`，也可表示是 `non-optioanl`。这样就会造成一个问题：在 Swift 与 Objective-C 混编时，Swift 编译器并不知道一个 Objective-C 对象到底是 `optional` 还是 `non-optional`，因此这种情况下编译器会隐式地将 Objective-C 的对象当成是 `non-optional`。引入 `nullability annotations` 一方面为了让 iOS 程序员平滑地从 Objective-C 过渡到 Swift，另一方面也促使开发者在编写 Objective-C 代码时更加规范，减少同事之间的沟通成本。

关键字 `__nullable` 和 `__nonnull` 是苹果在 Xcode 6.3 中发行的。由于与第三方库的潜在冲突，苹果在 Xcode 7 中将它们更改为 `_Nullable` 和 `_Nonnull`。但是，为了与 Xcode 6.3 兼容，苹果预定义了宏 `__nullable` 和 `__nonnull` 来扩展为新名称。同时苹果同样还支持没有下划线的写法 `nullable` 和 `nonnull`，它们的区别在与放置位置不同。

>注意：此类关键词仅仅提供警告，并不会报编译错误。只能用于声明对象类型，不能声明基本数据类型。

属性关键字|用法
--|--
nullable、_Nullable 、__nullable|对象可以为空，区别在于放置位置不同
nonnull、_Nonnull、__nonnull|对象不能为空，区别在于放置位置不同
null_unspecified、_Null_unspecified 、__null_unspecified|未指定是否可为空，区别在于放置位置不同
null_resettable|1. getter 方法不能返回为空，setter 方法可以为空；<br>2. 必须重写 setter 或 getter 方法做非空处理。否则会报警告 `Synthesized setter 'setName:' for null_resettable property 'name' does not handle nil`


###### 使用效果

```objectivec
@interface AAPLList : NSObject <NSCoding, NSCopying>
// ...
- (AAPLListItem * _Nullable)itemWithName:(NSString * _Nonnull)name;
@property (copy, readonly) NSArray * _Nonnull allItems;
// ...
@end

// --------------

[self.list itemWithName:nil]; // warning!
```

###### Audited Regions：Nonnull 区域设置

如果每个属性或每个方法都去指定 `nonnull `和 `nullable`，将是一件非常繁琐的事。苹果为了减轻我们的工作量，专门提供了两个宏： `NS_ASSUME_NONNULL_BEGIN` 和 `NS_ASSUME_NONNULL_END`。在这两个宏之间的代码，所有简单指针类型都被假定为 `nonnull`，因此我们只需要去指定那些 `nullable` 指针类型即可。示例代码如下：

```objectivec
NS_ASSUME_NONNULL_BEGIN
@interface AAPLList : NSObject <NSCoding, NSCopying>
// ...
- (nullable AAPLListItem *)itemWithName:(NSString *)name;
- (NSInteger)indexOfItem:(AAPLListItem *)item;

@property (copy, nullable) NSString *name;
@property (copy, readonly) NSArray *allItems;
// ...
@end
NS_ASSUME_NONNULL_END

// --------------

self.list.name = nil;   // okay

AAPLListItem *matchingItem = [self.list itemWithName:nil];  // warning!
```

###### 笔者的一些经验总结

* 使用好可空性关键字可以让 Objective-C 开发者平滑地过渡到 Swift，而不会被 Swift 可选类型绊倒。
* 使用好可空性关键字可以让代码更加规范，比如你不应该将一个指定为 nonnull 的属性赋值为 nil。
* `NS_ASSUME_NONNULL_BEGIN` 和 `NS_ASSUME_NONNULL_END` 只是苹果为了减轻我们的工作量而提供的宏，而不是允许我们忽略可空性关键字。
* 如果你没有指定属性/方法参数为 nullable 的话，当给该属性赋值/传参 nil 的时候，会得到烦人的警告。
* 进行混编的时候，如果你没有给一个可为空的属性指定 nullable，就无法进行可选链式调用，因为 Swift 会把它当作非可选类型来处理，而且你还不能强制解包，因为它可能为 nil，这时候你就得加一层保护。


##### 类属性 class

属性可以分为实例属性和类属性：

* 实例属性：每个实例都有一套属于自己的属性值，它们之前是相互独立的；
* 类属性：可以为类本身定义属性，无论创建了多少个该类型的实例，这些属性都只有唯一一份，因为类是单例。

说白了就是实例属性与 instance 关联，类属性与 class 关联。

用处：类属性用于定义某个类型所有实例共享的数据，比如所有实例都能用的一个常量/变量（就像 C 语言中的静态常量/静态变量）。

通过给属性添加 class 关键字来定义`类属性`。

```objectivec
@property (class, nonatimoc, strong) NSObject *object;
```

类属性是不会进行 `property autosynthesis` 的，那怎么关联值呢？

* 如果是存储属性
    1. 在 .m 中定义一个 static 全局变量，然后在 setter 和 getter 方法中对此变量进行操作。
    2. 在 setter 和 getter 方法中使用关联对象来存储值。笔者之前遇到的一个使用场景就是，类是通过 Runtime 动态创建的，这样就没办法使用 static 全局变量存储值。于是笔者在父类中定义了一个类属性并使用关联对象来存储值，这样动态创建的子类就可以给它的类属性关联值了。
* 如果是计算属性，就直接实现 setter 和 getter 方法就好。

#### 其它补充

在设置属性所对应的实例变量时，一定要遵从该属性所声明的语义：

```objectivec
@property (nonatomic, copy) NSString *name;

— (instancetype)initWithName:(NSString *)name {
    if (self = [super init]) {
        _name = [name copy];
    }
   	return self;
}
```

若是自己来实现存取方法，也应该保证其具备相关属性所声明的性质。

参考：[iOS - 再谈 OC 属性及属性关键字](https://juejin.cn/post/6986323251911720997/ "iOS - 再谈 OC 属性及属性关键字")

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)

本期讲解**深浅拷贝的知识点**。文章将从深拷贝和浅拷贝的区别开始讲起，然后讲解在 iOS 中对 mutable 对象与 immutable 对象进行 copy 与 mutableCopy 的结果，以及如何对集合对象进行真正意义上的深拷贝，最后带你实现对自定义对象的深浅拷贝。

### 对深浅拷贝的理解

我们先要理解拷贝的目的：产生一个副本对象，跟源对象互不影响。

#### 深拷贝和浅拷贝

拷贝类型|拷贝方式|特点
--|--|--
深拷贝|内存拷贝，让副本对象指针和源对象指针指向 `两片` 内容相同的内存空间。|1. 不会增加被拷贝对象的引用计数；<br>2. 产生了一个内存分配，出现了两块内存。
浅拷贝|指针拷贝，对内存地址的复制，让副本对象指针和源对象指针指向 `同一片` 内存空间。|1. 会增加被拷贝对象的引用计数；<br>2. 没有进行新的内存分配。<br>注意：如果是小对象如 NSString，可能通过 `Tagged Pointer` 来存储，没有引用计数。

简而言之：

* 深拷贝：内存拷贝，产生新对象，不增加被拷贝对象引用计数
* 浅拷贝：指针拷贝，不产生新对象，增加被拷贝对象引用计数，相当于执行了 retain
* 区别：1. 是否影响了引用计数；2. 是否开辟了新的内存空间

![](http://cdn.zhangferry.com/Images/20210724043958.png)

#### 在 iOS 中对 mutable 对象与 immutable 对象进行 copy 与 mutableCopy 的结果

iOS 提供了 2 个拷贝方法：

* copy：不可变拷贝，产生不可变副本
* mutableCopy：可变拷贝，产生可变副本

对 mutable 对象与 immutable 对象进行 copy 与 mutableCopy 的结果：

源对象类型|拷贝方式|副本对象类型|拷贝类型（深/浅）
:--:|:--:|:--:|:--:
mutable 对象|copy|不可变|深拷贝
mutable 对象|mutableCopy|可变|深拷贝
immutable 对象|copy|不可变|`浅拷贝`
immutable 对象|mutableCopy|可变|深拷贝

>注：这里的 immutable 对象与 mutable 对象指的是系统类 NSArray、NSDictionary、NSSet、NSString、NSData 与它们的可变版本如 NSMutableArray 等。

一个记忆技巧就是：对 immutable 对象进行 copy 操作是 `浅拷贝`，其它情况都是 `深拷贝`。

我们还可以根据拷贝的目的加深理解：

* 对 immutable 对象进行 copy 操作，产生 immutable 对象，因为源对象和副本对象都不可变，所以进行指针拷贝即可，节省内存
* 对 immutable 对象进行 mutableCopy 操作，产生 mutable 对象，对象类型不同，所以需要深拷贝
* 对 mutable 对象进行 copy 操作，产生 immutable 对象，对象类型不同，所以需要深拷贝
* 对 mutable 对象进行 mutableCopy 操作，产生 mutable 对象，为达到修改源对象或副本对象互不影响的目的，需要深拷贝

#### 使用 copy、mutableCopy 对集合对象进行的深浅拷贝是针对集合对象本身的

使用 copy、mutableCopy 对集合对象（Array、Dictionary、Set）进行的深浅拷贝是针对集合对象本身的，对集合中的对象执行的默认都是浅拷贝。也就是说只拷贝集合对象本身，而不复制其中的数据。主要原因是，集合内的对象未必都能拷贝，而且调用者也未必想在拷贝集合时一并拷贝其中的每个对象。

如果想要深拷贝集合对象本身的同时，也对集合内容进行 copy 操作，可使用类似以下的方法，copyItems 传 YES。但需要注意的是集合中的对象必须都符合 NSCopying 协议，否则会导致 Crash。

```objectivec
NSArray *deepCopyArray = [[NSArray alloc]initWithArray:someArray copyItems:YES];
```

>注：`initWithArray:copyItems:` 方法不是所有情况下都深拷贝集合对象本身的。如果执行 `[[NSArray alloc]initWithArray:@[] copyItems:aBoolValue];`，也就是源对象为不可变的空数组的话，对源对象本身执行的是浅拷贝，苹果对 `@[]` 使用了享元。

但是，如果集合中的对象的 copy 操作是浅拷贝，那么对于集合来说还不是真正意义上的深拷贝。比如，你需要对一个 `NSArray<NSArray *>` 对象进行真正的深拷贝，那么内层数组及其内容也应该执行深拷贝，可以对该集合对象进行 `归档` 然后 `解档`，只要集合中的对象都符合 NSCoding 协议。而且，使用这种方式，无论集合中存储的模型对象嵌套多少层，都可以实现深拷贝，但前提是嵌套的子模型也需要符合 NSCoding 协议才行，否则会导致 Crash。

```objectivec
NSArray *trueDeepCopyArray = [NSKeyedUnarchiver unarchiveObjectWithData:[NSKeyedArchiver archivedDataWithRootObject:oldArray]];
```

![](http://cdn.zhangferry.com/Images/20210724054744.png)


>需要注意的是，使用 `initWithArray:copyItems:` 并将 copyItems 传 YES 时，生成的副本集合对象中的对象（下一个级别）是不可变的，所有更深的级别都具有它们以前的可变性。比如以下代码将 Crash。
>
>```objectivec
>NSArray *oldArray = @[@[].mutableCopy];
>NSArray *deepCopyArray = [[NSArray alloc] initWithArray:oldArray copyItems:YES];
>NSMutableArray *mArray = deepCopyArray[0]; // deepCopyArray[0] 已经被深拷贝为 NSArray 对象
>[mArray addObject:@""]; // Crash
>```
>而 `归档解档集合` 的方式会保留所有级别的可变性，就像以前一样。

#### 实现对自定义对象的拷贝

如果想要实现对自定义对象的拷贝，需要遵守 `NSCopying` 协议，并实现 `copyWithZone:` 方法。

* 如果要浅拷贝，`copyWithZone:` 方法就返回当前对象：return self；
* 如果要深拷贝，`copyWithZone:` 方法中就创建新对象，并给希望拷贝的属性赋值，然后将其返回。如果有嵌套的子模型也需要深拷贝，那么子模型也需符合 NSCopying 协议，且在属性赋值时调用子模型的 copy 方法，以此类推。

如果自定义对象支持可变拷贝和不可变拷贝，那么还需要遵守 `NSMutableCopying` 协议，并实现 `mutableCopyWithZone:` 方法，返回可变副本。而 `copyWithZone:` 方法返回不可变副本。使用方可根据需要调用该对象的 copy 或 mutableCopy 方法来进行不可变拷贝或可变拷贝。

#### 以下代码会出现什么问题？

```objectivec
@interface Model : NSObject
@property (nonatomic, copy) NSMutableArray *array;
@end
```

不论赋值过来的是 NSMutableArray 还是 NSArray 对象，进行 copy 操作后都是 NSArray 对象（深拷贝）。由于属性被声明为 NSMutableArray 类型，就不可避免的会有调用方去调用它的添加对象、移除对象等一些方法，此时由于 copy 的结果是 NSArray 对象，所以就会导致 Crash。

参考：[iOS 面试解析 - 对深浅拷贝的理解](https://juejin.cn/post/6988858119182876680 "iOS 面试解析 - 对深浅拷贝的理解")

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)

本期讲解 load 和 initialize 的相关知识点。

### load 和 initialize 的区别

区别|load|initialize
--|--|--
调用时刻|在 `Runtime` 加载类、分类时调用<br>（不管有没有用到这些类，在程序运行起来的时候都会加载进内存，并调用 `load` 方法）。<br><br>每个类、分类的 `load`，在程序运行过程中只调用一次（除非开发者手动调用）。|在`类`第一次接收到消息时调用。<br><br>如果子类没有实现 `initialize` 方法，会调用父类的 `initialize`，所以父类的 `initialize` 方法可能会被调用多次，但不代表父类初始化多次，每个类只会初始化一次。
调用方式|① 系统自动调用 `load` 方式为直接通过函数地址调用；<br>② 开发者手动调用 `load` 方式为消息机制 `objc_msgSend` 函数调用。|消息机制 `objc_msgSend` 函数调用。
调用顺序|① 先调用类的 `load`，按照编译先后顺序调用（先编译，先调用），调用子类的 `load` 之前会先调用父类的 `load`；<br>② 再调用分类的 `load`，按照编译先后顺序调用（先编译，先调用）（注意：通过消息机制调用分类方法是：后编译，优先调用）。|① 先调用父类的 `initialize`<br>② 再调用子类的 `initialize`<br>（先初始化父类，再初始化子类）。

### 手动调用子类的 load 方法，但是子类没有实现该方法，会怎样？

* `load` 方法可以继承，手动调用 `load` 的方式是通过消息机制调用，先查找子类是否实现了 `load` 方法，由于子类没有实现，就会去查找父类，如果父类实现了 `load` 方法则调用，否则继续逐级查找；
* 如果父类的分类实现了 `load` 方法，那么会调用分类的，因为分类方法会“覆盖”同名宿主类方法；
* 如果存在多个父类的分类都实现了 `load` 方法的话，那么会调用最后参与编译的分类的 `load` 方法。


***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)

本期讲解 **block 类型** 的相关知识点。你是否遇到过这样的面试题：
* block 都有什么类型？
* 栈 block 存在什么问题？
* block 每种类型调用 copy 的结果分别是怎样的？

希望以下的总结能帮助到你。如果你对内容有任何疑问，或者有更好的解答，都可以联系我们。

### block 类型

block 有 3 种类型：栈块、堆块、全局块，最终都是继承自 NSBlock 类型。

block 类型|描述|环境
:--:|:--:|:--:
`__NSGlobalBlock__`<br>（ _NSConcreteGlobalBlock ）|全局 block，保存在数据段区（.data 区）|定义在全局区，或者没有访问自动局部变量
`__NSStackBlock__`<br>（ _NSConcreteStackBlock ）|栈 block，保存在栈区|访问了自动局部变量
`__NSMallocBlock__`<br>（ _NSConcreteMallocBlock ）|堆 block，保存在堆区|`__NSStackBlock__` 调用了 copy

**1. 栈块**

定义块的时候，其所占的内存区域是分配在栈中的。块只在定义它的那个范围内有效。

```objectivec
void (^block)(void);
if ( /* some condition */ ) {
    block = ^{
        NSLog(@"Block A");
    };
} else {
    block = ^{
        NSLog(@"Block B");
    };
}
block();
```

上面的代码有危险，定义在 if 及 else 中的两个块都分配在栈内存中，当出了 if 及 else 的范围，栈块可能就会被销毁。如果编译器覆写了该块的内存，那么调用该块就会导致程序崩溃。或者数据可能会变成垃圾数据，尽管将来该块还能正常调用，但是它捕获的变量的值已经错乱了。

>若是在 ARC 下，上面 block 会被自动 copy 到堆，所以不会有问题。但在 MRC 下我们要避免这样写。

**2. 堆块**

为了解决以上问题，可以给块对象发送 copy 消息将其从栈拷贝到堆区，堆块可以在定义它的那个范围之外使用。堆块是带引用计数的对象，所以在 MRC 下如果不再使用堆块需要调用 release 进行释放。

```objectivec
void (^block)(void);
if ( /* some condition */ ) {
    block = [^{
        NSLog(@"Block A");
    } copy];
} else {
    block = [^{
        NSLog(@"Block B");
    } copy];
}
block();
[block release];
```

**3. 全局块**

如果运行块所需的全部信息都能在编译期确定，包括没有访问自动局部变量等，那么该块就是全局块。全局块可以声明在全局内存中，而不需要在每次用到的时候于栈中创建。
全局块的 copy 操作是空操作，因为全局块决不可能被系统所回收，其实际上相当于单例。

```objectivec
void (^block)(void) = ^{
    NSLog(@"This is a block");
};
```

**每一种类型的 block 调用 copy 后的结果如下所示：**

block 类型|副本源的配置存储区|复制效果
:--|:--|:--
_NSConcreteGlobalBlock|程序的数据段区（.data 区）|什么也不做
_NSConcreteStackBlock|栈|从栈复制到堆
_NSConcreteMallocBlock|堆|引用计数增加

参考：[iOS 面试解析｜block 的类型](https://juejin.cn/post/6994082409687810079 "iOS 面试解析｜block 的类型")


***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)

本期通过一个 demo 讲解 `isMemberOfClass:`、`isKindOfClass:` 两个方法的相关知识点。

**以下打印结果是什么？**（严谨点就添加个说明吧：Person 类继承于 NSObject 类）

```objectivec
BOOL res1 = [[NSObject class] isKindOfClass:[NSObject class]];
BOOL res2 = [[NSObject class] isMemberOfClass:[NSObject class]];
BOOL res3 = [[Person class] isKindOfClass:[Person class]];
BOOL res4 = [[Person class] isMemberOfClass:[Person class]];

NSLog(@"%d, %d, %d, %d", res1, res2, res3, res4);
```

打印结果：1, 0, 0, 0

**解释：**

以下是 objc4-723 中 `isMemberOfClass:`、`isKindOfClass:` 方法以及 `object_getClass()` 函数的实现。

```objectivec
+ (BOOL)isMemberOfClass:(Class)cls {
    return object_getClass((id)self) == cls;
}

- (BOOL)isMemberOfClass:(Class)cls {
    return [self class] == cls;
}

+ (BOOL)isKindOfClass:(Class)cls {
    for (Class tcls = object_getClass((id)self); tcls; tcls = tcls->superclass) {
        if (tcls == cls) return YES;
    }
    return NO;
}

- (BOOL)isKindOfClass:(Class)cls {
    for (Class tcls = [self class]; tcls; tcls = tcls->superclass) {
        if (tcls == cls) return YES;
    }
    return NO;
}

Class object_getClass(id obj)
{
    if (obj) return obj->getIsa();
    else return Nil;
}
```

emmm 整理的时候发现后面的版本又做了小优化，具体就不展开了，不过原理不变，以下是 824 版本的：

```objectivec
+ (BOOL)isMemberOfClass:(Class)cls {
    return self->ISA() == cls;
}

- (BOOL)isMemberOfClass:(Class)cls {
    return [self class] == cls;
}

+ (BOOL)isKindOfClass:(Class)cls {
    for (Class tcls = self->ISA(); tcls; tcls = tcls->getSuperclass()) {
        if (tcls == cls) return YES;
    }
    return NO;
}

- (BOOL)isKindOfClass:(Class)cls {
    for (Class tcls = [self class]; tcls; tcls = tcls->getSuperclass()) {
        if (tcls == cls) return YES;
    }
    return NO;
}
```

由此我们可以得出结论：

* `isMemberOfClass:` 方法是判断当前 `instance/class` 对象的 `isa` 指向是不是 `class/meta-class` 对象类型；
* `isKindOfClass:` 方法是判断当前 `instance/class` 对象的 `isa` 指向是不是 `class/meta-class` 对象或者它的子类类型。

显然 `isKindOfClass:` 的范围更大。如果方法调用者是 instance 对象，传参就应该是 class 对象。如果方法调用着是 class 对象，传参就应该是 meta-class 对象。所以 res2-res4 都为 0。那为什么 res1 为 1 呢？

因为 NSObject 的 class 的对象的 isa 指向它的 meta-class 对象，而它的 meta-class 的 superclass 指向它的 class 对象，所以 `[[NSObject class] isKindOfClass:[NSObject class]]` 成立 。

![](http://cdn.zhangferry.com/Images/objc-isa-class-diagram.jpg)

总之，`[instance/class isKindOfClass:[NSObject class]]` 恒成立。（严谨点，需要是 NSObject 及其子类类型）


***
整理编辑：[FBY展菲](https://github.com/fanbaoying)

本期面试解析讲解的是离屏渲染的相关知识点。

### 为什么圆角和裁剪后 iOS 绘制会触发离屏渲染？

默认情况下每个视图都是完全独立绘制渲染的。
而当某个父视图设置了圆角和裁剪并且又有子视图时，父视图只会对自身进行裁剪绘制和渲染。

当子视图绘制时就要考虑被父视图裁剪部分的绘制渲染处理，因此需要反复递归回溯和拷贝父视图的渲染上下文和裁剪信息，再和子视图做合并处理，以便完成最终的裁剪效果。这样势必产生大量的时间和内存的开销。

解决的方法是当父视图被裁剪和有圆角并且有子视图时，就单独的开辟一块绘制上下文，把自身和所有子视图的内容都统一绘制在这个上下文中，这样子视图也不需要再单独绘制了，所有裁剪都会统一处理。当父视图绘制完成时再将开辟的缓冲上下文拷贝到屏幕上下文中去。这个过程就是离屏渲染！！

所以离屏渲染其实和我们先将内容绘制在位图内存上下文然后再统一拷贝到屏幕上下文中的双缓存技术是非常相似的。使用离屏渲染主要因为 iOS 内部的视图独立绘制技术所导致的一些缺陷而不得不才用的技术。

推荐阅读：[关于iOS离屏渲染的深入研究](https://zhuanlan.zhihu.com/p/72653360 "关于iOS离屏渲染的深入研究")


***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

本期解析一道 GCD 死锁题。

分别在 mainThread 执行 test1 和 test2 函数，问执行情况如何？

```swift
  func test1() {
      DispatchQueue.main.sync { // task1
          print("1") 
      }
  }

  func test2() {
      print("1")
      let queue = DispatchQueue.init(label: "thread")
      queue.async { // task1
          print("2")
          DispatchQueue.main.sync { // task3
              print("3")
              queue.sync { // task4
                  print("4")
              }
          }
          print("5")
      }
      print("6")
      queue.async { // task2
          print("7")
      }
      print("8")
  }
```

1. 死锁。
   1. mainThread 当前正在执行 test1 函数。
   2. 这时候使用 sync 函数往 mainQueue 中提交 task1 以同步执行，需要 task1 执行完毕后才会返回。
   3. 由于队列 FIFO，要想从 mainQueue 取出 task1 放到 mainThread 执行，需要先等待上一个 task 也就是 test1 函数先执行完，而 test1 此时又被 sync 阻塞，需要 sync 函数先返回。因此 test1 与 task1 循环等待，产生死锁。
2. 打印 1、6、8、2、3，然后死锁。
   1. 创建一个 serialQueue。使用 async 函数往指定队列提交 task 以异步执行会直接返回，不会阻塞，因此打印 1、6、8，并且 mainThread 执行完 test2。
   2. 从 serialQueue 中取出 task1 放到一条 childThread 执行，因为是 serialQueue 所以 task2 需要等待 task1 执行完毕才会执行。 执行 task1，打印 2；
   3. 使用 sync 函数往 mainQueue 提交 task3。**此时 task1 被阻塞，需要等待 task3 执行完毕**，才会接下去打印 5；
   4. mainThread 当前没有在执行 task，因此执行 task3，打印 3；
   5. 接着，使用 sync 往 serialQueue 中提交 task4，**此时 task3 被阻塞，需要等待 task4 执行完毕**；
   6. 此时该 childThread 正在执行 task1，**因此 task4 需要等待 task1 先执行完毕**。
   7. 此时，task1 在等待 task3，task3 在等待 task4，task4 在等待 task1。循环等待，产生死锁。

使用 GCD 的时候，我们一定要注意死锁问题，不要使用 `sync 函数` 往 `当前 serialQueue` 中添加 task，否则会卡住当前 serialQueue，产生死锁。

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

本期解析 KVO 的实现原理。

Apple 使用了 isa-swizzling 方案来实现 KVO。

**注册：**

当我们调用 `addObserver:forKeyPath:options:context:` 方法，为 **被观察对象** a 添加 KVO 监听时，系统会在运行时动态创建 a 对象所属类 A 的子类 `NSKVONotifying_A`，（如果是在Swift工程中，因为命名空间的存在，生成的类名会是`NSKVONotifying_ModuleName.A`） 并且让 a 对象的 isa 指向这个子类，同时重写父类 A 的 **被观察属性** 的 setter 方法来达到可以通知所有 **观察者对象** 的目的。

这个子类的 isa 指针指向它自己的 meta-class 对象，而不是原类的 meta-class 对象。

重写的 setter 方法的 SEL 对应的 IMP 为 Foundation 中的 `_NSSetXXXValueAndNotify` 函数（XXX 为 Key 的数据类型）。因此，当 **被观察对象** 的属性发生改变时，会调用 _NSSetXXXValueAndNotify 函数，这个函数中会调用：

* `willChangeValueForKey:` 方法
*  父类 A 的 setter 方法
*  `didChangeValueForKey:` 方法

**监听：**

而 willChangeValueForKey: 和 didChangeValueForKey: 方法内部会触发 **观察者对象** 的监听方法：`observeValueForKeyPath:ofObject:change:context:`，以此完成 KVO 的监听。

willChangeValueForKey: 和 didChangeValueForKey: 触发监听方法的时机：

* didChangeValueForKey: 方法会直接触发监听方法
* `NSKeyValueObservingOptionPrior` 是分别在值改变前后触发监听方法，即一次修改有两次触发。而这两次触发分别在 willChangeValueForKey: 和 didChangeValueForKey: 的时候进行的。如果注册方法中 options 传入 NSKeyValueObservingOptionPrior，那么可以通过只调用 willChangeValueForKey: 来触发改变前的那次 KVO，可以用于在属性值即将更改前做一些操作。

**移除：**

在移除 KVO 监听后，被观察对象的 isa 会指回原类 A，但是 NSKVONotifying_A 类并没有销毁，还保存在内存中，不销毁的原因想必大家也很容易理解，其实就是一层缓存，避免动态类的频繁创建/销毁。

**重写方法：**

NSKVONotifying_A 除了重写 setter 方法外，还重写了 class、dealloc、_isKVOA 这三个方法（可以通过 class_copyMethodList 获得），其中：

* class：返回父类的 class 对象，目的是为了不让外界知道 KVO 动态生成类的存在，隐藏 KVO 实现（通过此处我们可以知道获取对象所属类的方式最好是使用class方法，而不是isa指针）；
* dealloc：释放 KVO 使用过程中产生的东西；
* _isKVOA：用来标志它是一个 KVO 的类。

参考：[iOS - 关于 KVO 的一些总结](https://juejin.cn/post/6844903972528979976 "iOS - 关于 KVO 的一些总结")

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

本期面试解析讲解的知识点是 **KVC 取值和赋值过程的工作原理**。

**Getter**

以下是 `valueForKey:` 方法的默认实现，给定一个 `key` 作为输入参数，在消息接收者类中操作，执行以下过程。
* ① 按照 `get<Key>`、`<key>`、`is<Key>`、`_<key>` 顺序查找方法。
	<br>如果找到就调用取值并执行 ⑤，否则执行 ②；
* ② 查找 `countOf<Key>`、`objectIn<Key>AtIndex:`、`<key>AtIndexes:` 命名的方法。
	<br>如果找到第一个和后面两个中的至少一个，则创建一个能够响应所有 `NSArray` 的方法的集合代理对象（类型为 `NSKeyValueArray`，继承自 `NSArray`），并返回该对象。否则执行 ③；
    * 代理对象随后将其接收到的任何 `NSArray` 消息转换为 `countOf<Key>`、`objectIn<Key>AtIndex:`、`<Key>AtIndexes:` 消息的组合，并将其发送给 `KVC` 调用方。如果原始对象还实现了一个名为 `get<Key>:range:` 的可选方法，则代理对象也会在适当时使用该方法。
* ③ 查找 `countOf<Key>`、`enumeratorOf<Key>`、`memberOf<Key>:` 命名的方法。
	<br>如果三个方法都找到，则创建一个能够响应所有 `NSSet` 的方法的集合代理对象（类型为 `NSKeyValueSet`，继承自 `NSSet`），并返回该对象。否则执行④；
    * 代理对象随后将其接收到的任何 `NSSet` 消息转换为 `countOf<Key>`、`enumeratorOf<Key>`、`memberOf<Key>:` 消息的组合，并将其发送给 `KVC` 调用方。
* ④ 查看消息接收者类的 `+accessInstanceVariablesDirectly` 方法的返回值（默认返回 `YES`）。如果返回 `YES`，就按照 `_<key>`、`_is<Key>`、`<key>`、`is<Key>` 顺序查找成员变量。如果找到就直接取值并执行 ⑤，否则执行 ⑥。如果 `+accessInstanceVariablesDirectly` 方法返回 `NO` 也执行 ⑥。
* ⑤ 如果取到的值是一个对象指针，即获取的是对象，则直接将对象返回。
	* 如果取到的值是一个 `NSNumber` 支持的数据类型，则将其存储在 `NSNumber` 实例并返回。
	* 如果取到的值不是一个 `NSNumber` 支持的数据类型，则转换为 `NSValue` 对象, 然后返回。
* ⑥ 调用 `valueForUndefinedKey:` 方法，该方法抛出异常 `NSUnknownKeyException`，程序 `Crash`。这是默认实现，我们可以重写该方法对特定 `key` 做一些特殊处理。

**Setter**

以下是 `setValue:forKey:` 方法的默认实现，给定 `key` 和 `value` 作为输入参数，尝试将 `KVC` 调用方 `key` 的值设置为 `value`，执行以下过程。
* ① 按照 `set<Key>:`、`_set<Key>:` 顺序查找方法。
	<br>如果找到就调用并将 `value` 传进去（根据需要进行数据类型转换），否则执行 ②。
* ② 查看消息接收者类的 `+accessInstanceVariablesDirectly` 方法的返回值（默认返回 `YES`）。如果返回 `YES`，就按照 `_<key>`、`_is<Key>`、`<key>`、`is<Key>` 顺序查找成员变量（同 Getter）。如果找到就将 `value` 赋值给它（根据需要进行数据类型转换），否则执行 ③。如果 `+accessInstanceVariablesDirectly` 方法返回 `NO` 也执行 ③。
* ③ 调用 `setValue:forUndefinedKey:` 方法，该方法抛出异常 `NSUnknownKeyException`，程序 `Crash`。这是默认实现，我们可以重写该方法对特定 `key` 做一些特殊处理。

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

本期面试解析讲解的知识点是 Objective-C 的消息机制（上）。为了避免篇幅过长这里不会展开太细，而且太细的笔者我也不会😅，网上相关的优秀文章数不胜数，如果大家看完还有疑惑🤔一定要去探个究竟🐛。

**消息机制派发**

“消息机制派发” 是 Objective-C 的消息派发方式，其 “动态绑定” 机制让所要调用的方法在运行时才确定，支持开发者使用 “method-swizzling”、“isa-swizzling” 等黑魔法来在运行时改变调用方法的行为。除此之外，还有 “直接派发”、“函数表派发” 等消息派发方式，这些方式在 Swift 中均有应用。

“消息” 这个词好像不常说，更多的是称之为 “方法”。其实，给某个对象 “发送消息” 就相当于在该对象上“ 调用方法”。完整的消息派发由 `接收者`、`选择子` 及 `参数` 构成。在 Objective-C 中，给对象发送消息的语法为：

```objectivec
id returnValue = [someObject message:parameter];
```

在这里，someObject 叫做 `接收者`，message 叫做 `选择子`，`选择子` 与 `参数` 合起来称为 `消息`。编译器看到此消息后，会将其转换为一条标准的 C 语言函数调用，所调用的函数为消息机制的核心函数 `objc_msgSend`：

```objectivec
void objc_msgSend(id self, SEL _cmd, ...)
```

该函数参数个数可变，能接受两个或两个以上参数。前面两个参数 `self 消息接收者` 和 `_cmd 选择子` 即为 Objective-C 方法的两个隐式参数，后续参数就是消息中的那些参数（也就是方法显式参数）。

Objective-C 中的方法调用在编译后会转换成该函数调用，比如以上方法调用会转换为：

```objectivec
id returnValue = objc_msgSend(someObject, @selector(message:), parameter);
```

> 除了 objc_msgSend，还有其它函数负责处理边界情况：
>
> * objc_msgSend_stret：待发送的消息返回的是结构体
> * objc_msgSend_fpret：待发送的消息返回的是浮点数
> * objc_msgSendSuper：给父类发消息
> * ......

在讲了一大段废话之后（废话居然占了这么大篇幅 wtm），该步入重点了，objc_msgSend 函数的执行流程是什么样的？

objc_msgSend 执行流程通常分为三大阶段：`消息发送`、`动态方法解析`、`消息转发`。而有些地方又将 `动态方法解析` 阶段归并到 `消息转发` 阶段中，从而将其分为了 `消息发送` 和 `消息转发` 两大阶段，比如《Effective Objective-C 2.0》。好吧，其实我也不知道哪种是通常😅。

**消息发送**

* 判断 receiver 是否为 nil，是的话直接 return，这就是为什么给 nil 发送消息却不会 Crash 的原因。
* 去 receiverClass 以及逐级遍历的 superclass 中的 cache_t 和 class_rw_t 中查找 IMP，找到就调用。如果遍历到 rootClass 还没有找到的话，则进入 `动态方法解析` 阶段。
* 该阶段还涉及到 `initialize 消息的发送`、`cache_t 缓存添加、扩容 ` 等流程。

**动态方法解析**

**消息转发**

由于篇幅原因，剩下的内容我们下期再见吧👋。

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

本期面试解析讲解的知识点是 Objective-C 的消息机制（下）。在上一期摸鱼周报中我们讲解了 objc_msgSend 执行流程的第一大阶段 `消息发送`，那么这一期我们就来聊聊后两大阶段 `动态方法解析` 与 `消息转发`。

**动态方法解析**

如果 `消息发送` 阶段未能处理未知消息，那么就会进行一次 `动态方法解析`。我们可以在该阶段通过动态添加方法实现，来处理未知消息。`动态方法解析` 后，会再次进入 `消息发送` 阶段，从 “去 receiverClass 的 method cache 中查找 IMP” 这一步开始执行。

具体来说，在该阶段，Runtime 会根据 receiverClass 的类型是 class/meta-class 来调用以下方法：

```objectivec
+ (BOOL)resolveInstanceMethod:(SEL)sel;
+ (BOOL)resolveClassMethod:(SEL)sel;
```

我们可以重写以上方法，并通过 `class_addMethod` 函数来动态添加方法实现。需要注意的一点是，实例方法存储在类对象中，类方法存储在元类对象中，因此这里要注意传参。

```c
BOOL class_addMethod(Class cls, SEL name, IMP imp, const char *types)
```

如果我们在该阶段正确地处理了未知消息，那么再次进入到 `消息发送` 阶段肯定能找到 IMP 并调用，否则将进入 `消息转发` 阶段。

**消息转发**

`消息转发` 又分为 Fast 和 Normal 两个阶段，顾名思义 Fast 更快。

1. Fast：找一个备用接收者，尝试将未知消息转发给备用接收者去处理。

具体来说，就是给 receiver 发送一条如下消息，注意有类方法和实例方法之分。

```objectivec
+/- (id)forwordingTargetForSelector:(SEL)selector;
```

如果我们重写了以上方法，并正确返回了一个 != receiver 的对象（备用接收者），那么 Runtime 就会通过 objc_msgSend 给备用接收者发送当前的未知消息，开启新的消息执行流程。

如果该阶段还是没能处理未知消息，就进入 Normal。需要注意，在 Fast 阶段无法修改未知消息的内容，如果需要，请在 Normal 阶段去处理。

2. Normal：启动完整的消息转发，将消息有关的全部细节都封装到一个 NSInvocation 实例中，再给接收者最后一次机会去处理未知消息。

具体来说，Runtime 会先通过调用以下方法来获取适合未知消息的方法签名。

```objectivec
+/- (NSMethodSignature *)methodSignatureForSelector:(SEL)aSelector;
```

然后根据这个方法签名，创建一个封装了未知消息的全部内容（target、selector、arguments）的 NSInvocation 实例，然后调用以下方法并将该 NSInvocation 实例作为参数传入。

```objectivec
+/- (void)forwardInvocation:(NSInvocation *)invocation;
```

我们可以重写以上方法来处理未知消息。在 `forwardInvocation:` 方法中，我们可以直接将未知消息转发给其它对象（代价太大，不如在 Fast 处理），或者改变未知消息的内容再转发给其它对象，甚至可以定义任何逻辑。

如果到了 Normal 还是没能处理未知消息，如果是没有返回方法签名，那么将调用 `doesNotRecognizeSelector:`；如果是没有重写 `forwardInvocation:`，将调用 NSObject 的 `forwardInvocation:` 的默认实现，而该方法的默认实现也是调用 `doesNotRecognizeSelector:`，表明未知消息最终未能得到处理，以 Crash 程序结束 objc_msgSend 的全部流程。

**一些注意点**

* 重写以上方法时，不应由本类处理的未知消息，应该调用父类的实现，这样继承体系中的每个类都有机会处理未知消息，直至 NSObject。
* 以上几个阶段均有机会处理消息，但处理消息的时间越早，性能就越高。
  - 最好在 `动态方法解析` 阶段就处理完，这样 Runtime 就可以将此方法缓存，稍后这个对象再接收到同一消息时就无须再启动 `动态方法解析` 与 `消息转发` 流程。
  - 如果在 `消息转发` 阶段只是单纯想将消息转发给备用接收者，那么最好在 Fast 阶段就完成。否则还得创建并处理 NSInvocation 实例。
* `respondsToSelector:`  会触发 `动态方法解析`，但不会触发 `消息转发`。


***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

Q：以下两段代码的执行情况分别如何？

```objectivec
  dispatch_queue_t queue = dispatch_get_global_queue(0, 0);
  for (int i = 0; i < 1000; i++) {
      dispatch_async(queue, ^{
          self.name = [NSString stringWithFormat:@"abcdefghij"];
      });
  }
```

```objectivec
  dispatch_queue_t queue = dispatch_get_global_queue(0, 0);
  for (int i = 0; i < 1000; i++) {
      dispatch_async(queue, ^{
          self.name = [NSString stringWithFormat:@"abcdefghi"];
      });
  }
```

* 第一段代码，self.name 是 `__NSCFString` 类型，存储在堆，需要维护引用计数，其 setter 方法实现为先 release 旧值，再 retain/copy 新值。这里异步并发执行 setter 就可能会有多条线程同时 release 旧值，过度释放对象，导致 Crash。
* 第二段代码，由于指针足够存储数据，字符串的值就直接通过 `Tagged Pointer` 存储在了指针上，self.name 是 `NSTaggedPointerString` 类型。在 `objc_release` 函数中会判断指针是不是 `Tagged Pointer`，是的话就不对对象进行 release 操作，更不会过度释放而导致 Crash 了。

这里是 release 的实现：

```c
__attribute__((aligned(16), flatten, noinline))
void 
objc_release(id obj)
{
    if (!obj) return;
    if (obj->isTaggedPointer()) return;
    return obj->release();
}
```


***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

Q：执行以下代码，打印结果是什么？

```objectivec
dispatch_async(dispatch_get_global_queue(0, 0), ^{
    NSLog(@"1");
    [self performSelector:@selector(test) withObject:nil afterDelay:.0];
    NSLog(@"3");
});

- (void)test {
    NSLog(@"2");
}
```

打印结果为 1、3。原因是：

1. `performSelector:withObject:afterDelay:` 的本质是拿到当前线程的 RunLoop 往它里面添加 timer
2. RunLoop 和线程是一一对应关系，子线程默认没有开启 RunLoop
3. 当前 `performSelector:withObject:afterDelay:` 在子线程执行

所以 2 不会打印。


***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

Q：能否向编译后的类增加实例变量？能否向运行时动态创建的类增加实例变量？为什么？

A：

* 不能向编译后的类增加实例变量。类的内存布局在编译时就已经确定，类的实例变量列表存储在 class_ro_t Struct 里，编译时就确定了内存大小无法修改，所以不能向编译后的类增加实例变量。
* 能向运行时动态创建的类增加实例变量。运行时动态创建的类只是通过 alloc 分配了类的内存空间，没有对类进行内存布局，内存布局是在类初始化过程中完成的，所以能向运行时动态创建的类增加实例变量。

```objectivec
Class newClass = objc_allocateClassPair([NSObject class], "Person", 0);
class_addIvar(newClass, "_age", 4, 1, @encode(int));
class_addIvar(newClass, "_name", sizeof(NSString *), log2(sizeof(NSString *)), @encode(NSString *));
objc_registerClassPair(newClass); // 要在类注册之前添加实例变量
```

***
整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

现代开发⼯程师在⾯试过程中，算法⾯试往往有⼀定程度的重要性。

算法⾯试作为基本功之⼀，它包含了太多的逻辑思维，可以考察你思考问题的逻辑和解决问题的能⼒。完全类似的业务选手只能靠`挖掘`，但当⼀个⼈逻辑思维和能⼒不错的情况下，其业务匹配及后期上⼿概率也会很⾼。 

⾯试算法题⽬在难度上（尤其是代码难度上）会略低⼀些，倾向于考察⼀些基础数据结构与算法，通过交流暴露更多的⾯试题细节。

这也就是为什么现代算法⾯试中推崇**⼀题多解**，在实际算法⾯试中出现原题的概率往往不⾼，随着与面试官交流且探讨让已知的面试题出现变化。

下⾯我们以 [LeetCode](https://leetcode.com) 开篇 [TwoSum](https://leetcode.com/problems/two-sum/ "LeetCode - #1 Two Sum") 来简要说明。

> 默认读者有关于时间复杂度和空间复杂度的概念。

### TwoSum

给定⼀个整数数组 `nums` 和⼀个整数⽬标值 `target` ，请你在该数组中找出**和**为⽬标值 `target` 的那**两个**整数，并返回它们的数组下标。 

你可以假设每种输⼊**只会对应⼀个答案**。但是，数组中**同⼀个元素**在答案⾥不能重复出现。 

你可以按**任意顺序**返回答案。 

**示例 1：**

```
输⼊：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
```

**示例 2：**

```
输⼊：nums = [3,2,4], target = 6 
输出：[1,2]
```

**示例 3：**

```
输⼊：nums = [3,3]，target = 6 
输出： [0,1]
```

**提示：**

* `2 <= nums.length <= 104` 
* `-109 <= nums[i] <= 109`
* `-109 <= target <= 109`
* **只会存在⼀个有效答案**

### 解析

作为⼏乎⼈⼈  [LeetCode](https://leetcode.com)  ，⼈⼈ Code 过的经典题⽬，本题的最优解就是时间复杂度及空间复杂度皆为 O(n) 的解法

```swift
class Solution {
  func twoSum(_ nums: [Int], _ target: Int) -> [Int] { 
    var dict: [Int: Int] = [:]
    
    for (i, n) in nums.enumerated() { 
      if let index = dict[target - n] { 
        return [i, index] 
      } 
      dict[n] = i 
    }
    
    return []
  }

}
```

但是这种面试原题，往往不是我们能正好遇到的。

#### 删减版两数之和

给定⼀个整数数组 `nums` 和⼀个整数⽬标值 `target` ，请你在该数组中找出和为⽬标值 target 的那**两个**整数，并返回它们的数组下标。

**示例 1：**

```
输⼊：nums = [2,7,11,15], target = 9 
输出：[0,1] 解释：
因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
```

这就很像我们会遇到的初始问题，现在我们一起跟`面试官` 来确认一下面试题吧！

##### 确认异常状态即确认出参与⼊参的限制

我们需要确保两数之和不会超过值的最⼤限制 `Int.Max` 以及会不会超过 `Int.min`

需要跟⾯试官确认参数的限制，以及超出限制以后返回的结果

##### 确认是否有多个答案及结果顺序，及同⼀位置能否⽤多次

确认是否存在**多个**答案，确认数组中是否存在相同数据，以及确认是否需要展示所有正确的值即答案是否唯一且两数下标是否是顺序的

例如：

```
输⼊：nums = [2,2,7,11,15], target = 9
```

这个答案可能是 `[0, 2]` 或 `[1, 2]` 这也会导致最终代码的编写

##### 确认是否整数数组是否有序

对于已经排序的数组，我们可以利⽤双指针的思想来优化我们的代码

```swift
class Solution {
  func twoSum(_ nums: [Int], _ target: Int) -> [Int] { 
    guard nums.count > 0 else {
      return []
    }

    var start = 0 
    var end = nums.count-1 
    while start < end {
      let sum = nums[start] + nums[end] 
      if sum == target { 
        return [start, end] 
      } else if sum < target { 
        start += 1 
      } else { 
        end -= 1 
      }
    } 
    
    return []
  }
}
```

##### ...

当然可能还有其他变种，如果你有什么想法也可以来丰富所有的示例。

### 总结

算法⾯试题是⼀个与⾯试官交流的好途径，而在⾯试过程中⼀步步与⾯试官交流，可以展现⾯试者逻辑思维能⼒以及沟通交流能⼒。

在实际遇到面试题的时候，我们不着急写出具体的代码，展现你的**思维过程**，利用交流丰富你的表现，思维能力和沟通交流能力。


***
整理编辑：[夏天](https://juejin.cn/user/3298190611456638) 

**树**作为最常见的数据结构之一，在算法中有举足轻重的地位。

理解树有助于我们理解很多其他的数据结构，例如**图**，**栈**等。也有助于我们理解一些算法类型，例如，**回溯算法**和**动态规划**。当然在练习关于树的解题过程中，也能够加深我们对**深度优先**及**广度优先**算法的理解。

今天我们以二叉树的**三序遍历**为题，来开启我们二叉树的学习。

### 题目

给定一个二叉树，返回他的 _**前序**_ _**中序**_ _**后序**_ 三种遍历

> 输入: [4,2,6,1,3,5,7]
>     4
>    /   \
>   2     6
>  / \   / \ 
> 1  3 5  7

#### 输出

前序遍历：首先访问根结点，然后遍历左子树，最后遍历右子树（根->左->右）

> 顺序：访问根节点->前序遍历左子树->前序遍历右子树
>
> 前序遍历: [4, 2, 1, 3, 6, 5, 7]

中序遍历：首先遍历左子树，然后访问根节点，最后遍历右子树（左->根->右）

> 顺序：中序遍历左子树->访问根节点->中序遍历右子树
>
> 中序遍历: [1, 2, 3, 4, 5, 6, 7]

后序遍历：首先遍历左子树，然后遍历右子树，最后访问根节点（左->右->根）

> 顺序：后序遍历左子树->后序遍历右子树->访问根节点
>
> 后续遍历: [1, 3, 2, 5, 7, 6, 4]

二叉树的遍历方法一般有三种

* 递归
* 迭代（常规迭代加**颜色标记法**）
* 莫里斯遍历（今天暂时不涉及）

### 递归

在树的深度优先遍历中（包括前序、中序、后序遍历），递归方法最为直观易懂，但考虑到效率，我们通常不推荐使用递归。

递归步骤一般需要遵循以下三种：

1. 确定递归的参数以及返回值
2. 确定递归的终止条件，**递归算法一定有终止条件**，避免死循环。
3. 确定单次递归的逻辑

```swift
/// traversals 为输出的数组
func preorder(_ node: TreeNode?) {
    guard let node = node else {
        return
    }
    /// 前序遍历
    traversals.append(node.val) 
    preorder(node.left)
    preorder(node.right)
    /// 中序遍历
    preorder(node.left)
    traversals.append(node.val) 
    preorder(node.right)
    /// 后序遍历
    preorder(node.left)
    preorder(node.right)
    traversals.append(node.val) 
}
```

#### 迭代

二叉树的迭代步骤一般是将节点加入到一个 `栈` 中，然后通过访问栈头/栈尾，根据遍历顺序访问所有的符合的节点。

##### 前序遍历

```swift
func preorderIteration(_ root: TreeNode?) {
    var st:[TreeNode?] = [root]
    while !st.isEmpty {
        let node = st.removeFirst()
        if node != nil {
            traversals.append(node!.val)
        } else {
            continue
        }
        st.insert(node?.right, at: 0)
        st.insert(node?.left, at: 0)
    }
}
```

##### 中序遍历

```swift
func inorderIteration(_ root: TreeNode?) {
    var st:[TreeNode?] = []
    var cur:TreeNode? = root
    while cur != nil || !st.isEmpty {
        if cur != nil {
            st.insert(cur, at: 0)
            cur = cur?.left
        } else {
            cur = st.removeFirst()
            traversals.append(cur!.val)
            cur = cur?.right
        }
    }
}
```

##### 后序遍历

后序遍历其遍历步骤是 `左→右→中`，但是这个代码实现起来不简单。 所以我们可以先访问依次访问 `中→右→左` 的节点，最后将得到结果进行 `reversed`，其结果最终变成 `左→右→中` 。

```swift
func postorderIteration(_ root: TreeNode?) {
    var st:[TreeNode?] = [root]
    while !st.isEmpty {
        let node = st.removeFirst()
        if node != nil {
            print(node!.val)
            traversals.append(node!.val)
        } else {
            continue
        }
        st.insert(node?.left, at: 0)
        st.insert(node?.right, at: 0)
    }
    traversals = traversals.reversed()
}
```

#### 颜色标记法

传统的迭代由上述代码可知，比较繁琐，而且迭代过程中易错。参照 [颜色标记法-一种通用且简明的树遍历方法](https://leetcode-cn.com/problems/binary-tree-inorder-traversal/solution/yan-se-biao-ji-fa-yi-chong-tong-yong-qie-jian-ming/ "颜色标记法-一种通用且简明的树遍历方法") ，利用一个**兼具栈迭代方法的高效，又像递归方法一样简洁易懂的方法，更重要的是，这种方法对于前序、中序、后序遍历，能够写出完全一致的代码**。

其核心方法如下：

* 标记节点的状态，已访问的节点标记为 **1**，未访问的节点标记为 **0**

* 遇到未访问的节点，将节点标记为 **0**，然后根据三序排序的要求，按照特定的顺序入栈

  >  // 前序 `中→左→右` 按照 `右→左→中`
  >
  >  // 中序 `左→中→右` 按照 `右→中→左`
  > 
  >  // 后序 `左→右→中` 按照 `中→右→左`

* 结果数组中加入标记为 **1** 的节点的值

```swift
    func tuple(_ root: TreeNode?) -> [Int] {
        var traversals = [Int]()
        var statck = [(0, root)]
        while !statck.isEmpty {
            let (isVisted, node) = statck.removeLast()
            if node == nil {
                continue
            }
            if isVisted == 0 {
//                ///前序遍历
//                statck.append((0, node?.right))
//                statck.append((0, node?.left))
//                statck.append((1, node))
//                ///中序遍历
//                statck.append((0, node?.right))
//                statck.append((1, node))
//                statck.append((0, node?.left))
                ///后序遍历
                statck.append((1, node))
                statck.append((0, node?.right))
                statck.append((0, node?.left))
            } else {
                traversals.append(node!.val)
            }
        }
        return traversals
    }
```

利用颜色标记法可以简单的理解迭代的方法，并写出模板代码。

#### 莫里斯遍历

作为兼具性能及低空间复杂度的**莫里斯遍历**，可以在线下讨论。

***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

### Swift 中 struct 和 class 的区别，值类型和引用类型的区别

**struct & class**

在 Swift 中，其实 `class` 与 `struct` 之间的核心区别不是很多，有很多区别是值类型与引用类型这个区别隐形带来的天然的区别。

- `class` 可以继承，`struct` 不能继承（当然 `struct` 可以利用 `protocol` 来实现类似继承的效果。）；受此影响的区别有：

- - `struct` 中方法的派发方式全都是直接派发，而 `class` 中根据实际情况有多种派发方式，详情可看 [CoderStar｜Swift 派发机制](https://mp.weixin.qq.com/s?__biz=MzU4NjQ5NDYxNg==&mid=2247483768&idx=1&sn=0a6be7a9c5a374cbc5c5ba9a3c48020a&scene=21#wechat_redirec)；

- `class` 需要自己定义构造函数，`struct` 默认生成；

- `class` 是引用类型，`struct` 是值类型；受此影响的区别有：

- - `struct` 改变其属性受修饰符 let 影响，不可改变，`class` 不受影响；
  - `struct` 方法中需要修改自身属性时 (非 `init` 方法)，方法需要前缀修饰符 `mutating`；
  - `struct` 因为是值类型的原因，所以自动线程安全，而且也不存在循环引用导致内存泄漏的风险；
  - ...

- ...

**值类型 & 引用类型**

- 存储方式及位置：大部分值类型存储在栈上，大部分引用类型存储在堆上；
- 内存：值类型没有引用计数，也不会存在循环引用以及内存泄漏等问题；
- 线程安全：值类型天然线程安全，而引用类型需要开发者通过加锁等方式来保证；
- 拷贝方式：值类型拷贝的是内容，而引用类型拷贝的是指针，从一定意义上讲就是所谓的深拷贝及浅拷贝

你可以在 [CoderStar｜从 SIL 角度看 Swift 中的值类型与引用类型](https://mp.weixin.qq.com/s/6bvZ1YIhf2WCNsdkukTlew) 中查看详细内容。


***
整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)

### 事件传递及响应链

对于 iOS 的事件传递及响应链，你是否还掌握得不够好，推荐阅读我们编辑 @Mim0sa 和 @CoderStar 的这几篇文章以及 Apple 的文档，相信你一定能在面试中所向披靡。

* [@Mim0sa：iOS | 事件传递及响应链](https://juejin.cn/post/6894518925514997767 "@Mim0sa：iOS | 事件传递及响应链")
* [@Mim0sa：iOS | 响应链及手势识别](https://juejin.cn/post/6905914367171100680 "@Mim0sa：iOS | 响应链及手势识别")
* [@CoderStar：iOS 中的事件响应](https://mp.weixin.qq.com/s/OFwC7Z3iir2wKPJoRpLhFw "@CoderStar：iOS 中的事件响应")
* [@Apple：Event Handling Guide for iOS](https://github.com/zhangferry/iOSWeeklyLearning/blob/main/Resources/Books/Event%20Handling%20Guide%20for%20iOS%20官方文档.pdf "@Apple：Event Handling Guide for iOS")
* [Event Handling Guide for iOS 中文翻译版](https://github.com/zhangferry/iOSWeeklyLearning/blob/main/Resources/Books/Event%20Handling%20Guide%20for%20iOS%20中文翻译版.pdf "Event Handling Guide for iOS 中文翻译版")


***
整理编辑：[夏天](https://juejin.cn/user/3298190611456638) 

面试题：HTTP/1.0，HTTP/1.1，HTTP/2 有哪些区别？

### 什么是 HTTP

HTTP（超文本传输协议，HyperText Transfer Protocol）是互联网上应用最为广泛的一种网络协议。其默认使用 80 端口，由 HTTP 客户端发起一个请求，建立一个到服务器指定端口（默认是 80 端口）的 **TCP** 连接。

### HTTP/1.0

老的 HTTP 协议标准是 **HTTP/1.0**，为了提高系统的效率，**HTTP/1.0** 规定浏览器与服务器只保持短暂的连接，每次请求都需要与服务器建立一个 TCP 连接，服务器完成请求处理后立即断开 TCP 连接，服务器不会跟踪客户也不会记录已经请求过的请求。

这就是  **HTTP/1.0** 的两个主要特性：

* 无状态：服务器不跟踪不记录请求过的状态
* 无连接：每次请求都需要建立 TCP 连接

对于 `无状态` 来说，可以通过设置 `cookie` 或 `seesion` 等机制来实现身份校验和状态记录。

影响一个 HTTP 网络请求的因素主要有两个：**带宽**和**延迟**。 当下，网络设施的逐渐完善使得带宽问题得到较好的解决，从而**延迟**成为主要的影响因素。

**HTTP/1.0** `无连接` 特性导致两种了性能缺陷：

* **连接无法复用**

  连接无法复用会导致每次请求都需要进行一次 TCP 连接（即 3 次握手 4 次挥手）和慢启动，降低了网络使用率。

* **队头阻塞**

  在前一个请求响应到达之后下一个请求才能发送，如果前一个阻塞，后面的请求也会阻塞的。这会导致带宽无法被充分利用，以及后续健康请求被阻塞。

### HTTP/1.1

为了消除  **HTTP/1.0** 标准中的歧义内容和提升性能，我们很快的就过渡到了 **HTTP/1.1** 标准，也是当前使用最为广泛的 HTTP 协议 ：

* **默认支持长连接**：在 Header 中新增 `Connection` 参数，其值默认为 `Keep-Alive`。默认保持长连接，数据传输完成后保持 TCP 连接不断开，可以继续使用这个通道传输数据。
  > 默认的服务端的长连接时间是 30S。在 iOS 端的实践过程中会有概率出现下面的错误：
  >
  > > Error Domain=NSURLErrorDomain Code=-1005 "The network connection was lost.
* **HTTP pipeline**：基于长连接的基础，在同一个 TCP 连接上可以传送多个 HTTP 请求和响应，减少了建立和关闭连接的消耗和延迟。管道化可以不等第一个请求响应继续发送后面的请求，但响应的顺序还是按照请求的顺序返回。
* **缓存处理**：相较于 **HTTP/1.0**，**HTTP/1.1** 提供了更为丰富的缓存策略。在 **HTTP/1.0** 中主要是根据 Header 里的 `If-Modified-Since`、`Expires` 来做为判断缓存的标准，**HTTP/1.1** 则引入了诸如 `Entity tag`、`If-Unmodified-Since`、 `If-Match`、 `If-None-Match` 等缓存方式。并且还在 Header 中新增了 `Cache-control` 参数来管理缓存。
* **断点传输**：相较于 **HTTP/1.0** 无法部分返回数据对象，**HTTP/1.1** 在 Header 中新增了两个参数来支持**请求响应分块**，客户端发请求时对应的是 `Range`，服务器端响应时对应的是 `Content-Range`。
* **Host 头处理**： **HTTP/1.0** 认为每台服务器都指向了唯一的 IP 地址，请求消息中的 URL 中并没有主机的信息。在 **HTTP/1.1** 中新增了 Host 头域，能够使不同域名配置在同一个 IP 地址的服务器上。

### HTTP/2

**SPDY 协议是 HTTP/2 协议的基础**。**HTTP/2** 最大的改进就是从**文本协议**转变为**二进制协议**。

* **帧、消息、流和 TCP 连接**：**HTTP/2** 将一个 TCP 连接分为若干个流（`Stream`），每个流中可以传输若干消息（`Message`），每个消息由若干最小的二进制帧（`Frame`）组成。**HTTP/2** 中，每个用户的操作行为被分配了一个流编号（`stream ID`），这意味着用户与服务端之间创建了一个 TCP 通道；协议将每个请求分割为二进制的控制帧与数据帧部分，以便解析。
* **多路复用**：基于二进制分帧，在同一域名下所有访问都是从同一个 TCP 连接中走，HTTP 消息被分解为独立的帧，无序发送，服务端根据标识符和首部将消息重新组装起来。
* **请求优先级**：为了避免多路复用可能会导致关键请求被阻塞，即利用请求优先级完成高优先级请求先处理。
* **HPACK 算法**：**HTTP/2** 引入了头部压缩算法。利用合适的压缩算法来处理消息头的数据。避免了重复 Header 的传输，减小了传输数据的大小。
* **服务端推送（Server Push）**：在 **HTTP/2**  中，服务器可以对客户端的一个请求发送多个响应。

***
整理编辑：[zhangferry](https://zhangferry.com)

### dealloc 在哪个线程执行

在回答这个问题前需要了解 `dealloc` 在什么时机调用，`dealloc` 是在对象最后一次 `release` 操作的时候进行调用的，对应的源码在 `rootRelease` 中，针对 `nonpointer` 和 SideTable 有两种释放的操作。

 SideTable 管理的引用计数会调用 `sidetable_release`：

```c
uintptr_t
objc_object::sidetable_release(bool performDealloc)
{
#if SUPPORT_NONPOINTER_ISA
    ASSERT(!isa.nonpointer);
#endif
    SideTable& table = SideTables()[this];

    bool do_dealloc = false;

    table.lock();
    auto it = table.refcnts.try_emplace(this, SIDE_TABLE_DEALLOCATING);
    auto &refcnt = it.first->second;
    if (it.second) {
        do_dealloc = true;
    } else if (refcnt < SIDE_TABLE_DEALLOCATING) {
        // SIDE_TABLE_WEAKLY_REFERENCED may be set. Don't change it.
        do_dealloc = true;
        refcnt |= SIDE_TABLE_DEALLOCATING;
    } else if (! (refcnt & SIDE_TABLE_RC_PINNED)) {
        refcnt -= SIDE_TABLE_RC_ONE;
    }
    table.unlock();
    if (do_dealloc  &&  performDealloc) {
          // 可以释放的话，调用dealloc
        ((void(*)(objc_object *, SEL))objc_msgSend)(this, @selector(dealloc));
    }
    return do_dealloc;
}
```

对于 `nonpointer` 指针管理的引用计数，会修改 `extra_rc`值，需要释放时在`rootRelease`方法的底部还是会调用：

```c
if (do_dealloc  &&  performDealloc) {
    ((void(*)(objc_object *, SEL))objc_msgSend)(this, @selector(dealloc));
}
```

这里可以看出 `dealloc` 的调用并没有设置线程，所以其执行会根据触发时所在的线程而定，就是说其即可以是子线程也可以是主线程。这个也可以很方便的验证。

### NSString *str = @"123" 这里的 str 和  "123" 分别存储在哪个区域

可以先做一下测试：

```objectivec
NSString *str1 = @"123"; // __NSCFConstantString
NSLog(@"str1.class=%@, str1 = %p, *str1 = %p", str1.class, str1, &str1);
// str1.class=__NSCFConstantString, str1 = 0x1046b8110, *str1 = 0x7ffeeb54dc50
```

这时的 str1 类型是 `__NSCFConstantString`，str1 的内容地址较短，它代表的是常量区，指向该常量区的指针 `0x7ffeeb54dc50` 是在栈区的。

再看另外两种情况：

```objectivec
NSString *str2 = [NSString stringWithFormat:@"%@", @"123"];
NSLog(@"str2.class=%@, str2 = %p, *str2 = %p", str2.class, str2, &str2);
// str2.class=NSTaggedPointerString, str2 = 0xe7f1d0f8856c5253, *str2 = 0x7ffeeb54dc58

NSString *str3 = [NSString stringWithFormat:@"%@", @"iOS摸鱼周报"]; //
NSLog(@"str3.class=%@, str3 = %p, *str3 = %p", str3.class, str3, &str3);
// str3.class=__NSCFString, str3 = 0x600002ef8900, *str3 = 0x7ffeeb54dc30
```

这里的字符串类型为 `NSTaggedPointerString` 和 `__NSCFString`，他们的指针都是在栈区，这三个对象的指针还是连续的，内容部分，前者在指针里面，后者在堆区。（栈区地址比堆区地址更高）

这里再回顾下内存的分区情况，大多数情况我们只需关注进程的虚拟内存就可以了：

![](http://cdn.zhangferry.com/Images/20211216172748.png)

***
整理编辑：[zhangferry](https://zhangferry.com)

### HTTPS 建立的过程中客户端是如何保证证书的合法性的？

HTTPS 的建立流程大概是这样的：

1、Client -> Server: 支持的协议和加密算法，随机数 A

2、Server -> Client: 服务器证书，随机数 B

3、Client -> Server: 验证证书有效性，随机数 C

4、Server -> Client: 生成秘钥，SessionKey = f(A + B + C)

5、使用 SessionKey 进行对称加密沟通

其中第 3 步，就需要客户端验证证书的有效性。有效性的验证主要是利用证书的信任链和签名。

#### 证书信任链

我们以 `zhangferry.com`这个网站的 HTTPS 证书为例进行分析：

![](http://cdn.zhangferry.com/Images/20211223165541.png)

`zhangferry.com` 的证书里有一个 Issuer Name 的分段，这里表示的是它的签发者信息。其签发者名称是 *TrustAsia TLS RSA CA*，而我们可以通过上面的链式结构发现，其上层就是*TrustAsia TLS RSA CA*。再往上一层是 *DigiCert Global Root CA*，所以证书签发链就是：*DigiCert Global Root CA* -> *TrustAsia TLS RSA CA* -> *zhangferry.com*。

其中 *DigiCert Global Root CA* 是根证书，它的签发者是它自己。根证书由特定机构颁发，被认为是可信的。我们的电脑在安装的时候都会预装一些 CA 根证书，查看钥匙串能够找到刚才的根证书：

![](http://cdn.zhangferry.com/Images/20211223170915.png)

如果能够验证签发链是没有篡改的，那就可以说明当前证书有效。

#### 签发有效

要验证 *DigiCert Global Root CA*（简称 A） 签发了 *TrustAsia TLS RSA CA*（简称 B） ，可以利用 RSA 的非对称性。这里分两步：签发、验证。

签发：A 对 B 签发时，由 B 的内容生成一个 Hash 值，然后 A 使用它的私钥对这个 Hash 值进行加密，生成签名，放到 B 证书里。

验证：使用 A 的公钥（操作系统内置在钥匙串中）对签名进行解密，得到签发时的 Hash 值 H1，然后单独对 B 内容进行 Hash 计算，得到 H2，如果 H1== H2，那么就说明证书没有被篡改过，验证通过。

这些过程中使用到的对称加密算法和 Hash 算法都会在证书里说明。同理逐级验证，直到最终的证书节点，都没问题就算是证书验证通过了。流程如下：

![](http://cdn.zhangferry.com/Images/20211223174908.png)

图片来源：https://cheapsslsecurity.com/blog/digital-signature-vs-digital-certificate-the-difference-explained/

### Hash 冲突的解决方案

当两个不同的内容使用同一个 Hash 算法得到相同的结果，被称为发生了 Hash 冲突。Hash 冲突通常有两种解决方案：开放定址法、链地址法。

#### 开放定址法

开放定址法的思路是当地址已经被占用时，就再重新计算，直到生成一个不被占用地址。对应公式为：

![](http://cdn.zhangferry.com/Images/20211223221219.png)

其中 di 为增量序列，m 为散列表长度， i 为已发生的冲突次数。根据 di 序列的内容不同又分为不同的处理方案：

di = 1, 2, 3...(m-1)，为线性数列，就是线性探测法。

di = 1^2, 2^2, 3^2...k^2，为平方数列，就是平法探测法。

di = 伪随机数列，就是伪随机数列探测法。

#### 链地址法

链地址法是用于解决开放定址法导致的数据聚集问题，它是采用一个链表将所有冲突的值一一记录下来。

#### 其他方法

再哈希法：设置多个哈希算法，如果冲突就更换算法，重新计算。

建立公共溢出区：将哈希表和溢出数据分开存放，冲突内容填入溢出表中。

参考：[wiki-散列表](https://zh.wikipedia.org/wiki/%E5%93%88%E5%B8%8C%E8%A1%A8 "wiki-散列表")

***
整理编辑：[zhangferry](https://zhangferry.com)

### dyld 2 和 dyld 3 有哪些区别

dyld 是动态加载器，它主要用于动态库的链接和程序启动加载工作，它目前有两个主要版本：dyld 2 和 dyld 3。

**dyld 2**

[dyld2](https://github.com/opensource-apple/dyld/tree/master/src "dyld开源地址") 从 iOS 3.1 开始引入，一直到 iOS 12 被 dyld 3 全面代替。它经过了很多次版本迭代，我们现在常见的特性比如 ASLR，Code Sign，Shared Cache 等技术，都是在 dyld 2 中引入的。dyld 2 的执行流程是这样的：

![](http://cdn.zhangferry.com/Images/20220104235847.png)

- 解析 `mach-o` 头文件，找到依赖库，依赖库又可能有别的依赖，这里会进行递归分析，直到获得所有 dylib 的完整图。这里数据庞大，需要进行大量的处理；
- 映射所有 `mach-o` 文件，将它们放入地址空间；
- 执行符号查找，若你的程序使用 `printf` 函数，将会查找 `printf` 是否在库系统中，然后我们找到它的地址，将它复制到你的程序中的函数指针上；
- 进行 bind 和 rebase，修复内部和外部指针；
- 运行一些初始化任务，像是加载 category、load 方法等；
- 执行 main；

**dyld 3**

dyld 3 在 2017 年就被引入至 iOS 11，当时主要用来优化系统库。现在，在 iOS 13 中它也将用于启动第三方 APP，完全替代 dyld 2。

dyld 3 最大的特点就是引入了启动闭包，闭包里包含了启动所需要的缓存信息，而且这个闭包在进程外就完成了。在打开 APP 时，实际上已经有不少工作都完成了，这会使 dyld 的执行更快。

最重要的特性就是启动闭包，闭包里包含了启动所需要的缓存信息，从而提高启动速度。下图是 dyld 2 和 dyld 3 的执行步骤对比：

![](http://cdn.zhangferry.com/Images/20220105001119.png)

dyld 3 的执行步骤分两大步，以图中虚线隔开，虚线以上进程外执行，以下进程创建时执行：

* 前 3 步查找依赖和符号相对耗时，且涉及一些安全问题，所以将这些信息做成缓存闭包写入磁盘里，对应地址：`tmp/com.apple.dyld`。闭包会在重启手机/更新/下载 App 的首启等时机创建。

* 进程启动时，读取闭包并验证闭包有效性。

* 后面步骤同 dyld 2 

[iOS 13中dyld 3的改进和优化](https://easeapi.com/blog/blog/83-ios13-dyld3.html "iOS 13中dyld 3的改进和优化")

[iOS dyld 前世今生](https://www.yotrolz.com/posts/c2aae680/ "iOS dyld 前世今生")

### 编译流程

一般的编译器架构，比如 LLVM 采用的都是三段式，也即从源码到机器码需要经过三个步骤：

前端 Frontend -> 优化器 Optimizer -> 后端 Backend

这么设计的好处就是将编译职责进行分离，当新增语言或者新增 CPU 架构时，只需修改前端和后端就行了。

其中前端受语言影响，Objective-C 和 Swift 对应的前端分别是 clang 和 swiftc。下图整理了两种语言的编译流程：

![](http://cdn.zhangferry.com/Images/ios_compiler.png)

#### 前端

编译前端做的工作主要是：

1. 词法分析：将源码进行分割，生成一系列记号（token）。
2. 语法分析：扫描上一步生成的记号生成语法树，该分析过程采用上下文无关的语法分析手段。
3. 语义分析：语义分析分为静态语义分析和动态语义分析两种，编译期间确认的都是静态语义分析，动态语义需运行时期间才能确定。该步骤包括类型匹配和类型转换，会确认语法树中各表达式的类型。

之后导出 IR 中间件供优化器使用。这一步 Swift 会比 ObjC 多几个步骤，其中一个是 ClangImporter，这一步用于兼容 OC。它会导入 Clang Module，把 ObjC 或者 C 的 API 映射为 Swift API，导出结果能够被语义分析器使用。

另外一个不同是 Swift 会有几个 SIL 相关的步骤（蓝色标注），SIL 是 Swift Intermediate Language 的缩写，意为 Swift 中间语言，它不同于 IR，而是特定于 Swift 的中间语言，适合用于对 Swift 源码进行分析和优化。它这里又分三个步骤：

1. 生成原始的 SIL
2. 进行一些数据流诊断，转成标准 SIL
3. 做一些特定于 Swift 的优化，包括 ARC、泛型等

#### 优化器

编译前端会生成统一的 IR (Intermediate Representation) 文件传入到优化器，它是一种强类型的精简指令集，对目标指令进行了抽象。Xcode 中的 Optimization Level 的几个优化等级: `-O0` , `-O1` , `-O2` , `-O3` , `-Os`，即是这个步骤处理的。

如果开启了 Bitcode，还会转成 Bitcode 格式，它是 IR 的二进制形式。

#### 后端

这个步骤相对简单，会根据不同的 CPU 架构生成汇编和目标文件。

#### 链接

项目编译是以文件为单位的，跨文件调用方法是无法定位到调用地址的，链接的作用就是用于绑定这些符号。链接分为静态链接和动态链接两种：

* 静态链接发生在编译期，在生成可执行程序之前会把各个 .o 文件和静态库进行一个链接。常用的静态链接器为 GNU 的 `ld`，LLVM4 里也有自己的链接器 `lld`。

* 动态链接发生在运行时，用于链接动态库，它会在启动时找到依赖的动态库然后进行符号决议和地址重定向。动态链接其为 `dyld`。

[Swift.org - Swift Compiler](https://www.swift.org/swift-compiler/#compiler-architecture "Swift.org - Swift Compiler")

***
整理编辑：[zhangferry](https://zhangferry.com)

### 如何检测内存泄露

**内存泄漏**指的是程序中已动态分配的堆内存（程序员自己管理的空间）由于某些原因未能释放或无法释放的现象。该现象会造成系统内存的浪费，导致程序运行速度变慢甚至系统崩溃。

在 ARC 模式下，导致内存泄露的主要原因是循环引用，其次是非 OC 对象的内存处理、野指针等。针对内存泄露的检测方案也基本从以上几种类型中入手，它们可以分为两类：工具类和代码类。

#### 工具类

工具类比较多：

* Instruments 里的 Leaks

* Memory Graph Debugger

* Schems 里的 Memory Management

* XCTest 中的 XCTMemoryMetric

前两种方式比较常见，后两种内存泄露还需要借助于 Xcode 导出的 memgraph 文件，结合 `leaks`、`malloc_history` 等命令行工具进行分析。工具类检测方案都有一个缺点就是比较繁琐，开发阶段很容易遗漏，所以基于代码的自动化内存泄露检测方案更适合使用。

#### 代码类

代码类检测泄露方式有三个典型的库。

**MLeaksFinder**

地址：https://github.com/Tencent/MLeaksFinder

它的基本原理是这样的，当一个 ViewController 被 pop 或 dismiss 之后，我们认为该 ViewController，包括它上面的子 ViewController，以及它的 View，View 的 subView 等等，都很快会被释放，如果某个 View 或者 ViewController 没释放，我们就认为该对象泄漏了。

它是基于 Method Swizzled 方式，需要 Hook ViewController 的 `viewDidDisappear` ，`viewWillAppear` 等方法。所以仅适用于 Objective-C 项目。

**LifetimeTracker**

地址：https://github.com/krzysztofzablocki/LifetimeTracker

LifetimeTracker 是使用 Swift 实现的，可以同时支持 OC 和 Swift 项目。它的原理是用一个协议表达监听泄露能力，我们提前设置监听入口和允许存在的对象个数。内部维护一个类似引用计数一样的数值，进入监听会进行一个 +1 操作，还会监听该对象的 `deinit` 方法，如果调用执行 `-1`。如果该「引用计数」大于我们设置的最大对象个数，就触发可视化的泄露警告。

简化一些流程之后的代码：

```swift
internal func track(_ instance: Any, configuration: LifetimeConfiguration, file: String = #file) {
    let instanceType = type(of: instance)
    let configuration = configuration
    configuration.instanceName = String(reflecting: instanceType)

    func update(_ configuration: LifetimeConfiguration, with countDelta: Int) {
        let groupName = configuration.groupName ?? Constants.Identifier.EntryGroup.none
        let group = self.trackedGroups[groupName] ?? EntriesGroup(name: groupName)
        group.updateEntry(configuration, with: countDelta)
        // 检测当前计数是否大于最大引用数
        if let entry = group.entries[configuration.instanceName], entry.count > entry.maxCount {
            self.onLeakDetected?(entry, group)
        }
        self.trackedGroups[groupName] = group
    }
    // 开始检测，计数+1
    update(configuration, with: +1)

    onDealloc(of: instance) {
        // 执行deinit，计数-1
        update(configuration, with: -1)
    }
}
```

**FBRetainCycleDetector**

地址：https://github.com/facebook/FBRetainCycleDetector

上面两种方案都是粗略的检测，是 ViewController 或者 View 级别的，要想知道更具体的信息，到底哪里导致的循环应用就无能为力了。而 FBRetainCycleDetector 就是用于解决这类问题，因为需要借助 OC 的动态特性，所以该库无法在 Swift 项目中发挥作用。

它的实现相对上面两个方案更复杂一些，大致原理是基于 `DFS` 算法，把整个对象之间的强引用关系当做图进行处理，查找其中的环，就找到了循环引用。

核心是寻找对象之间的强引用关系，在 OC 语言中，强引用关系主要发生在这三种场景里，针对这三种场景也有不同的处理方案：

**类的成员变量**

通过 `runtime` 的 `class_getIvarLayout` 获取描述该类成员变量的布局信息，然后通过 `ivar_getOffset` 遍历获取成员变量在类结构中的偏移地址，然后获取强引用变量的集合。

**关联对象**

利用 fishhook hook `objc_setAssociatedObject` 和 `objc_removeAssociatedObjects` 这两个方法，对通过 `OBJC_ASSOCIATION_RETAIN`和`OBJC_ASSOCIATION_RETAIN_NONATOMIC` 策略进行关联的对象进行保存。

**block 持有**

理解这个原理还需要再回顾下 block 的内存布局，FBRetainCycleDetector 对 block 结构体进行了等价的封装：

```c
struct BlockLiteral {
    void *isa;
    int flags;
    int reserved;
    void (*invoke)(void *, ...);
    struct BlockDescriptor *descriptor;
    // imported variables
};

struct BlockDescriptor {
  unsigned long int reserved;                // NULL
  unsigned long int size;
  // optional helper functions
  void (*copy_helper)(void *dst, void *src); // IFF (1<<25)
  void (*dispose_helper)(void *src);         // IFF (1<<25)
  const char *signature;                     // IFF (1<<30)
};
```

在 `BlockLiteral` 结构体的 descriptor 字段之后的位置会存放 block 持有的对象，但是并非所有对象都是我们需要的，我们只需要处理强引用对象即可。而恰恰 block 的引用对象排列基于寻址长度对齐，较大地址放在前面，且强引用对象会排在弱引用之前，所以从 descriptor 之后的成员变量，可以按固定的指针长度依次取出对象。这之后的对象用 `FBBlockStrongRelationDetector` 封装，但这有可能会多取对象，比如 weak 类型的引用其实是不需要捕捉的。

该库的做法是重写 `FBBlockStrongRelationDetector` 对象的 release 方法，仅设置标记位，然后外部调用它的 dispose 方法，这样其强引用对象都会调用 release，被调用这部分都是强引用对象。

```objectivec
static NSIndexSet *_GetBlockStrongLayout(void *block) {
    ...
    void (*dispose_helper)(void *src) = blockLiteral->descriptor->dispose_helper;
    const size_t ptrSize = sizeof(void *);    
    const size_t elements = (blockLiteral->descriptor->size + ptrSize - 1) / ptrSize;

    void *obj[elements];
    void *detectors[elements];

    for (size_t i = 0; i < elements; ++i) {
        FBBlockStrongRelationDetector *detector = [FBBlockStrongRelationDetector new];
        obj[i] = detectors[i] = detector;
    }

    @autoreleasepool {
        dispose_helper(obj);
    }
    ...
}
```

当拿到以上所有强引用关系时就可以利用 DFS 深度优先搜索遍历引用树，查找是否有环形引用了。

`FBRetainCycleDetector` 的检测方案明显更复杂、更耗时，所以几乎不可能针对所有对象都进行检测，所以更好的方案是配合 MLeaksFinder 或者 facebook 自己的 [FBAllocationTracker](https://github.com/facebookarchive/FBAllocationTracker "FBAllocationTracker")，先找到潜在泄露对象，然后分析这些对象的强引用关系，查找是否存在循环引用。

**其他方案**

在资料查找过程中还发现了另一个库 [BlockStrongReferenceObject](https://github.com/tripleCC/Laboratory/tree/master/BlockStrongReferenceObject "BlockStrongReferenceObject") ，它只检测 Block 导致的循环引用问题，跟 `FBRetainCycleDetector` 类似，也是要分析 block 内存布局。但不同的是，它可以完全根据内存布局，来定位到强引用对象。主要是依据 block 和 clang 源码进行分析得出，真的非常强👍🏻，如果对实现细节感兴趣可以阅读这篇文章：[聊聊循环引用的检测](https://triplecc.github.io/2019/08/15/%E8%81%8A%E8%81%8A%E5%BE%AA%E7%8E%AF%E5%BC%95%E7%94%A8%E7%9A%84%E6%A3%80%E6%B5%8B/ "聊聊循环引用的检测")。

参考：

[检测和诊断 App 内存问题](https://mp.weixin.qq.com/s/E80VEIJma66fj7BZy1cCeQ)

[draveness的源码分析 - FBRetainCycleDetector](https://github.com/draveness/analyze/tree/master/contents/FBRetainCycleDetector "draveness的源码分析 - FBRetainCycleDetector")

***
整理编辑：[zhangferry](https://zhangferry.com)

### 如何治理 OOM

OOM（Out Of Memory）指的是应用内存占用过高被系统强制杀死的情况，通常还会再分为 FOOM （前台 OOM） 和 BOOM （后台 OOM）两种。其中 FOOM 现象跟常规 Crash 一样，对用户体验影响比较大。

OOM 产生的原因是应用内存占用过高，治理方法就是降低内存占用，这可以分两部分进行：

1、现存代码：问题检测，查找内存占用较大的情况进行治理。

2、未来代码：防裂化，对内存使用进行合理的规范。

#### 问题检测

OOM 与其他 Crash 不同的一点是它的触发是通过 `SIGKILL` 信号进行的，常规的 Crash 捕获方案无法捕获这类异常。那么该如何定位呢，线下我们可以通过 Schems 里的 Memory Management，生成 memgraph 文件进行内存分析，但这无法应用到线上环境。目前主流的线上检测 OOM 方案有以下几个：

**FBAllocationTracker**

由 Facebook 提出，它会 hook OC 中的 `+alloc` 和 `+ dealloc` 方法，分别在分配和释放内存时增加和减少实例计数。

```objectivec
@implementation NSObject (AllocationTracker)

+ (id)fb_newAlloc
{
 id object = [self fb_originalAlloc];
 AllocationTracker::tracker()->incrementInstanceCountForClass([object class]);
 return object;
}

- (void)fb_newDealloc
{
 AllocationTracker::tracker()->decrementInstanceCountForClass([object class]);
 [self fb_originalDealloc];
}
@end
```

然后，当应用程序运行时，可以定期调用快照方法来记录当前活动的实例数。通过实例数量的异常变化来定位发生OOM的问题。

该方案的问题是无法检测非 OC 对象的内存占用，且没有堆栈信息。

参考：[Reducing FOOMs in the Facebook iOS app](https://engineering.fb.com/2015/08/24/ios/reducing-fooms-in-the-facebook-ios-app/ "Reducing FOOMs in the Facebook iOS app")

**OOMDetector**

这个是腾讯采用的方案。

通过 Hook iOS 系统底层内存分配的相关方法（包括 `malloc_*zone`相关的堆内存分配以及 `vm*_allocate` 对应的 VM 内存分配方法），跟踪并记录进程中每个对象内存的分配信息，包括分配堆栈、累计分配次数、累计分配内存等，这些信息也会被缓存到进程内存中。在内存触顶的时候，组件会定时 Dump 这些堆栈信息到本地磁盘，这样如果程序爆内存了，就可以将爆内存前 Dump 的堆栈数据上报到后台服务器进行分析。

![](http://cdn.zhangferry.com/Images/20220119232138.png)

参考：[【腾讯开源】iOS爆内存问题解决方案-OOMDetector组件](https://juejin.cn/post/6844903550187733000 "【腾讯开源】iOS爆内存问题解决方案-OOMDetector组件")

**Memory Graph**

这个是字节采用的方案，基于内存快照生成内存分布情况。线上 Memory Graph 核心的原理是扫描进程中所有 Dirty 内存，通过内存节点中保存的其他内存节点的地址值建立起内存节点之间的引用关系的有向图，用于内存问题的分析定位，整个过程不使用任何私有 API。该方案实现细节未开源，目前已搭载在字节跳动火山引擎旗下应用性能管理平台（[APMInsight](https://www.volcengine.com/product/apminsight "APMInsight")）上，供开发者注册使用。

![](http://cdn.zhangferry.com/Images/20220120225034.png)

[有一篇文章](https://juejin.cn/post/6895583288451465230 "分析字节跳动解决OOM的在线Memory Graph技术实现")分析了这个方案的实现原理：通过 mach 内核的 `vm_*region_recurse/vm_region_recurse64` 函数遍历进程内所有 VM Region。这里包括二进制，动态库等内存，我们需要的是 Malloc Zone，然后通过 `malloc*_get_all_zones` 获取 libmalloc 内部所有的 zone，并遍历每个 zone 中管理的内存节点，获取 libmalloc 管理的存活的所有内存节点的指针和大小。再根据指针判断是 OC/Swift 对象，还是 C++ 对象，还是普通的 Buffer。

参考：[iOS 性能优化实践：头条抖音如何实现 OOM 崩溃率下降50%+](https://juejin.cn/post/6885144933997494280 "iOS 性能优化实践：头条抖音如何实现 OOM 崩溃率下降50%+")

#### 防劣化

防劣化即防止出现 OOM 的一些手段，可以从以下方面入手：

- 内存泄漏：关于内存泄漏的检测可以见[上期内容](https://mp.weixin.qq.com/s/DNXrfZgx0JaXyvfVZ4sYVA)。
- autoreleasepool：在循环里产生大量临时对象，内存峰值会猛涨，甚至出现 OOM。适当的添加 autoreleasepool 能及时释放内存，降低峰值。
- 大图压缩：可以降低图片采样率。
- 前后台切换：后台更容易发生 OOM，因为后台可利用的内存更小，我们可以在进入后台时考虑释放一些内存。

***
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

![](http://cdn.zhangferry.com/Images/weekly_43_interview_02.png)

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

![](http://cdn.zhangferry.com/Images/weekly_44_interview_02.jpg)

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


***整理编辑：[JY](https://juejin.cn/user/1574156380931144)

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

![](http://cdn.zhangferry.com/Images/20220302155825.png)


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

![](http://cdn.zhangferry.com/Images/weekly_45_interview_02.png)

有 `for` 循环时，跳转到 `objc_autoreleaseReturnValue`的汇编指令是 `bl`。

![](http://cdn.zhangferry.com/Images/weekly_45_interview_01.png)

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

在存在优势的同时，也有一些缺点，例如 `mmap` 要求加载的最小单位为 `VM Page Size`，所以如果是小文件，该方法会导致碎片空间浪费。

#### mmap API 示例

`mmap` 实际应用主要是 `mmap() & munmap()`两个函数实现。两个函数原型如下：

```cpp
/// 需要导入头文件
#import <sys/mman.h>

void* mmap(void* start,size_t length,int prot,int flags,int fd,off_t offset);
 int munmap(void* start,size_t length);
```

函数参数：

- `start`：映射区的其实位置，设置为零表示由系统决定映射区的起始位置
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
- `off_set`：文件映射的偏移量，通常设置为0，代表从文件最前方开始对应offset必须是分页大小的整数倍。

`mmap` 回写时机并不是实时的，调用 `msync()`或者`munmap()` 时会从内存中回写到文件，系统异常退出也会进行内容回写，不会导致日志数据丢失，所以特别适合日志文件写入。

> Demo 可以参考开源库 `OOMDetector` 中的 `HighSppedLogger` 类的使用封装，有比较完整的映射、写入、读取、同步的代码封装，可直接使用。

#### 注意事项

`mmap` 允许映射到内存中的大小大于文件的大小，最后一个内存页不被使用的空间将会清零。但是如果映射的虚拟内存过大，超过了文件实际占用的内存页数量，后续访问会抛出异常。

示例可以参考[认真分析mmap：是什么 为什么 怎么用 ](https://www.cnblogs.com/huxiao-tee/p/4660352.html)中的情景二：

![](http://cdn.zhangferry.com/Images/weekly_51_interview.png)

超出文件大小的虚拟内存区域，文件所在页的内存扔可以访问，超出所在页的访问会抛出 `Signal` 信号异常

#### 参考

- [认真分析mmap：是什么 为什么 怎么用 ](https://www.cnblogs.com/huxiao-tee/p/4660352.html "认真分析 mmap: 是什么 为什么 怎么用")
- [C语言mmap()函数：建立内存映射](http://c.biancheng.net/cpp/html/138.html "C语言mmap()函数：建立内存映射")
- [OOMDetector](https://github.com/Tencent/OOMDetector "OOMDetector")


