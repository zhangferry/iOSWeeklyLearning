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

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210704165732.png)

握手阶段主要依靠以下几个标志位：
* SYN：在建立连接时使用，用来同步序号。SYN=1 代表这是一个请求建立连接或同意建立连接的报文，只有前两次握手中 SYN 才为 1，带 SYN 标志的 TCP 报文段称为同步报文段；
  * 当 SYN=1，ACK=0 时，表示这是一个请求建立连接的报文段
  * 当 SYN=1，ACK=1 时，表示对方同意建立连接
* ACK：表示前面确认号字段是否有效。ACK=1 代表有效。带 ACK 标志的 TCP 报文段称为确认报文段；
* FIN：表示通知对方本端数据已发送完毕，要关闭连接了。带 FIN 标志的 TCP 报文段称为终止报文段。

**三次握手是指建立一个 TCP 连接时，需要客户端和服务端总共发送 3 个包，需要三次握手才能确认双方的接收与发送能力是否正常。**

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210703051424.png)

1. 客户端向服务端发起连接请求，需要发送一个 SYN 报文到服务端。
2. 当服务端收到客户端发过来的 SYN 报文后，返回给客户端 SYN、ACK 报文。`这时候服务端可以确认客户端的发送能力和自己的接收能力正常`。
3. 客户端收到该报文。`这时候客户端可以确认双方的发送和接收能力都正常`。然后客户端再回复 ACK 报文给服务端，服务端收到该报文。`这时候服务端可以确认客户端的接收能力和自己的发送能力正常。所以这时候双方都可以确认自己和对方的接收与发送能力都正常`。就这样客户端和服务端通过 TCP 建立了连接。

**四次挥手的目的是关闭一个 TCP 连接。**

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210703051443.png)

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

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210724043958.png)

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

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210724054744.png)


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

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/objc-isa-class-diagram.jpg)

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

