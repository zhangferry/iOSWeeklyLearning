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
调用时刻|在 `Runtime` 加载类、分类时调用<br>（不管有没有用到这些类，在程序运行起来的时候都会加载进内存，并调用 `+load` 方法）。<br><br>每个类、分类的 `+load`，在程序运行过程中只调用一次（除非开发者手动调用）。|在`类`第一次接收到消息时调用。<br><br>如果子类没有实现 `+initialize` 方法，会调用父类的 `+initialize`，所以父类的 `+initialize` 方法可能会被调用多次，但不代表父类初始化多次，每个类只会初始化一次。
调用方式|① 系统自动调用 `+load` 方式为直接通过函数地址调用；<br>② 开发者手动调用 `+load` 方式为消息机制 `objc_msgSend` 函数调用。|消息机制 `objc_msgSend` 函数调用。
调用顺序|① 先调用类的 `+load`，按照编译先后顺序调用（先编译，先调用），调用子类的 `+load` 之前会先调用父类的 `+load`；<br>② 再调用分类的 `+load`，按照编译先后顺序调用（先编译，先调用）（注意：通过消息机制调用分类方法是：后编译，优先调用）。|① 先调用父类的 `+initialize`<br>② 再调用子类的 `+initialize`<br>（先初始化父类，再初始化子类）。

### 手动调用子类的 load 方法，但是子类没有实现该方法，为什么会去调用父类的 load 方法，且是调用父类的分类的 load 方法呢？
因为 load 方法可以继承，手动调用 load 的方式为是消息机制的调用，会去类方法列表里找对应的方法，由于子类没有实现，就会去父类的方法列表中查找。因为分类方法会“覆盖”同名宿主类方法，所以如果父类的分类实现了 load 方法，那么会调用分类的。如果存在多个分类都实现 load 方法的话，那么会调用最后参与编译的分类的 load 方法。

