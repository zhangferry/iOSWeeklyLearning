# Swift Proposals

## Generic Subscripts

地址：https://github.com/apple/swift-evolution/blob/main/proposals/0148-generic-subscripts.md

该提案是用于在下标里支持泛型，用于规定下标的取值类型。下标能够用泛型约束是很有意义的，而且更符合直觉。

要实现下标方法支持泛型，需要考虑两点，在哪增加参数和在哪增加泛型的where语句。

提案提供了一个解决方案：

```swift
extension Dictionary {

 subscript<Indices: Sequence>(indices: Indices) -> [Iterator.Element] where Indices.Iterator.Element == Index {

  // ...

 }
}
```

该提案在Swift4实现。

## Rationalizing Sequence end-operation names

地址：https://github.com/apple/swift-evolution/blob/main/proposals/0132-sequence-end-ops.md

Swift的Sequence和Collection提供了很多从前和从后访问数据的方法，它们有这些：

first、last、prefix(_:)、suffix(_:)、dropFirst(_:)、dropLast(_:)、removeFirst(_:)、removeLast(_:)

first即可以表达第一个元素的含义，又可以表达最开始的几个元素的含义。

drop的命名更是具有误导性，因为没有加ing或者ed，所以光看名字是不知道它要表达的含义的。

对于另外几个获取序列切片的方法，比如数组里面的prefix(_:)和prefix(upTo:)含义一样，但是suffix(_:)和suffix(from:)却不同，另外，suffix(from:)里的索引值，你能准确推断出它是从起始位置还是末尾位置开始算的吗？

该提案提供了一些解决方案，和新的命名形式，可以参考下：

![img](https://app.yinxiang.com/shard/s60/res/4320069c-b734-490b-a65b-c00be4289603.png)

## Remove Optional Comparison Operators

地址：https://github.com/apple/swift-evolution/blob/main/proposals/0121-remove-optional-comparison-operators.md

以前的Swift版本是支持Comparable协议的，它们的写法是这样的：

```swift
public func < <T : Comparable>(lhs: T?, rhs: T?) -> Bool

public func > <T : Comparable>(lhs: T?, rhs: T?) -> Bool

public func <= <T : Comparable>(lhs: T?, rhs: T?) -> Bool

public func >= <T : Comparable>(lhs: T?, rhs: T?) -> Bool
```

这样的设计可以实现这个效果：

```swift
[3, nil, 1, 2].sorted() // returns [nil, 1, 2, 3]
```

这样的目的是用于扩展Comparable的适用范围，但这个设计有时候又是反常识的，不存在或者说未初始化的内容也能参与排序有时会得出出乎意料的结果。

所以在Swift3的版本里去除了Comparable对Optional的支持，但是Equatable是支持Optional的。

## Distinguish between single-tuple and multiple-argument function types

地址：https://github.com/apple/swift-evolution/blob/main/proposals/0110-distingish-single-tuple-arg.md

看以下代码，分析x的类型：

```swift
let fn1 : (Int, Int) -> Void = { x in

​    // ...

}

let fn2 : (Int, Int) -> Void = { x, y in

​    // ...

}
```

在该提案实现之前，只有fn2的写法是被允许的，如果有多余一个参数的函数类型，在实现时就必须有同等数量的，参数与之相配。

如果想要让一个参数同时表示两个值，需要用闭包代替，fn1的写法需要改成：

```swift
let fn1 : ((Int, Int)) -> Void = { x in

    // ...
}
```

该提案的目的是打破这些限制，我们可以写成上面的示例样式，并且编译器会帮助我们判断fn1中x的类型为(Int, Int)，fn2中x和y类型为Int。

## Expanding Swift Self to class members and value types

地址：https://github.com/apple/swift-evolution/blob/main/proposals/0068-universal-self.md

该提案是为了扩展Self的作用使其可以直接访问类成员及值类型成员，并将dynamicType命名修改为Self。

看例子：

```swift
struct MyStruct {

  static func staticMethod() { ... }

  func instanceMethod() {

    MyStruct.staticMethod()

    self.dynamicType.staticMethod()

  }
}
```

self.dynamicType.staticMethod()的写法不够清晰，也与Swift常规命名形式不符，所以将其简化为Self.staticMethod()。

另外作为动态类型的替换，Self即可以是实例方法也可以在类方法中使用，均代表类型。

该提案Swift5.1生效。

## Swift Encoders

地址：https://github.com/apple/swift-evolution/blob/master/proposals/0167-swift-encoders.md

该提案为了扩展OC中NSCoding的功能，另外针对Swift提供了对JSON和property list的编解码类。

对应于`JSONEncoder&JSONDecoder`，`PropertyListEncoder&PropertyListDecoder`这几个类。

该提案还有一项内容是使 `NSKeyedArchiver`和 `NSKedUnarchiver`支持Codable，并将Foundation里的大部分类型适配了Codable协议。

SE-0166：https://github.com/apple/swift-evolution/blob/master/proposals/0166-swift-archival-serialization.md

## Offset-Based Access to Indices, Elements, and Slices

地址：https://github.com/apple/swift-evolution/blob/master/proposals/0265-offset-indexing-and-slicing.md

该提案的目的是为了解决字符串截取问题，对于一个较长的字符串，如果需要截取每行它开始的第5个元素，和末尾倒数第12个元素。当前的做法是这样的：

```swift
func parseRequirements(_ s: String) -> [(finish: Character, before: Character)] {

 s.split(separator: "\n").map { line in

  let finishIdx = line.index(line.startIndex, offsetBy: 5) // 5 after first

  let beforeIdx = line.index(line.endIndex, offsetBy: -12) // 11 before last

  return (line[finishIdx], line[beforeIdx])

 }
}
```

这里对于index的操作比较繁琐，提案建议是可以用这种形式实现：

```swift
func parseRequirements(_ s: String) -> [(finish: Character, before: Character)] {

 s.split(separator: "\n").map { line in

  (line[.first + 5]!, line[.last - 11]!)

 }
}
```

实现方案是增加一个OffsetBound结构体，该结构体作为Collection里subscript函数的参数类型，这样不光是String，实现Collection的所有类型都可以共享该特性。

该提案状态为修订，当前还未实现，可能在之后的Swift版本中我们就可以使用上这个特性了。

## Abolish ImplicitlyUnwrappedOptional type

地址：https://github.com/apple/swift-evolution/blob/main/proposals/0054-abolish-iuo.md

该提案在Swift4.2中采纳。

ImplicitlyUnwrappedOptional在Swift4.2版本之前是一个enum类型，它跟Optional作用类似，作为可选类型存在。

Optional的初始是这样的形式 let x: Int? = nil

ImplicitlyUnwrappedOptional的初始形式是这样的 let y: Int! = nil

注意这里废除的是IUO类型，该功能还是存在的。

这里可以想一下，如果执行print(y)会不会引发crash？

在Swift4.2之前的版本会导致崩溃，但在这之后的版本不会崩溃。Swift4.2废除了ImplicitlyUnwrappedOptional的形式，并对原有IUO类型在编译器层面进行了推导。

上面y的显示类型是Int!，但在输出是作为Int?处理的。

对于传递的时候例如let z = y，这里z也是Int?类型，不光是值类型，引用类型也是同样的逻辑。

引用类型可以通过init!()的形式实现原有的IUO类型。

这么处理的方式目的是为了安全，防止在类型传递和变量修改时导致强制解包带来的崩溃。

https://swift.gg/2016/07/21/wwdc-2016-increased-safety-in-swift-3/

## Defaulting non-Void functions so they warn on unused results

地址：https://github.com/apple/swift-evolution/blob/main/proposals/0047-nonvoid-warn.md

Swift有个编译关键字：@warn_unused_result，用于对没有使用返回值的函数进行警告，现在该关键字是函数声明的默认参数。但是有些使用场景我们可能不需要返回值，为了避免编译器的警告，一个做法是：

**_** = f()

但该做法有些生硬，那个为空的_的下划线仅仅用于应付警告问题也有些奇怪，于是诞生了一个新的编译关键字@discardableResult。如果声明在函数顶部，就会覆盖默认的@warn_unused_result，比如这样:

```swift
@discardableResult f()
```



该提案在Swift3中已经实现，未来规划是把@discardableResult当做一个类型修饰符，而不仅仅是编译器的声明符号，意思就是我们可以这样使用：

```swift
func f() -> @discardable T {}
```

## Remove implicit tuple splat behavior from function applications

地址：https://github.com/apple/swift-evolution/blob/main/proposals/0029-remove-implicit-tuple-splat.md

该提案废弃了原有Swift版本使用元组生成函数参数的特性。

该原有特性如下，对于如下函数。

```swift
func foo(a : Int, b : Int) {}
```

可以这样调用：foo(42, b : 17)

也可以这样调用：

```swift
let x = (1, b: 2)

foo(x)
```

对于第二种使用元组调用函数的形式，容易产生歧义，还增加了类型检查器的复杂性。

## Implicit returns from single-expression functions

地址：https://github.com/apple/swift-evolution/blob/master/proposals/0255-omit-return.md

对于如下Sequence的扩展函数

```swift
func sum() -> Element {
  return reduce(0, +)
}
```

可以省略return简写为

```swift
func sum() -> Element {
  reduce(0, +)
}
```

省略return的写法在map等高阶函数里是存在的：

```swift
let names = persons.map { $0.name }
```

这种写法不仅不会感觉到歧义，还是得表达更加清晰。

## Add first(where:) method to Sequence

地址：https://github.com/apple/swift-evolution/blob/main/proposals/0032-sequencetype-find.md

这个提案是在Sequence里增加一个first(where:)的方法，大多数使用过Swift的人应该都用过这个方法。提案里还给出了一个实现方案，这个实现的写法可以学一下：

![img](https://app.yinxiang.com/shard/s60/res/d74aa144-5c4f-4a0d-b09a-bd91d3cc7fdd.png)

这种把函数作为参数的高阶函数实现在Swift中非常常见，我们也可以仿照着定义一些适合自己的高阶函数。

```swift
extension Sequence {
 /// Returns the first element where `predicate` returns `true`, or `nil`
 /// if such value is not found.
 public func first(where predicate: @noescape (Self.Iterator.Element) throws -> Bool) rethrows -> Self.Iterator.Element? {
  for elt in self {
   if try predicate(elt) {
    return elt
   }
  }
  return nil
 }
}
```

## Abstract classes and methods

地址：https://github.com/apple/swift-evolution/blob/main/proposals/0026-abstract-classes-and-methods.md

该提案是用于实现类似Java，C#里的抽象类，抽象方法的。

看这个例子：

一个基类：

```swift
class RESTClient {

   var timeout = 3000

  var url : String {

    assert(false,"Must be overridden")

    return ""

  }
}
```

继承该基类的一个实现类：

```swift
class MyRestServiceClient : RESTClient {

  override var url : String {

    return "http://www.foo.com/client"

  }
}
```

这种实现，我们不得不在基类里为url参数填充一个无法调用的assert。如果有了抽象基类，抽闲方法的概念，我们可以这样实现该基类：

```swift
abstract class RESTClient {  

  var timeout = 3000

  abstract var url : String { get }

}
```

这样更简洁，也直接说明了，该类为抽象类，无法直接使用。

该提案当前状态为延后处理，之后的Swift版本可能就会支持这个功能。

## Optional Value Setter ??=

地址：https://github.com/apple/swift-evolution/blob/main/proposals/0024-optional-value-setter.md

该提案目的是为了以下场景，为optional提供默认值：

```swift
really.long.lvalue[expression] = really.long.lvalue[expression] ?? ""
```

简写成：

```swift
really.long.lvalue[expression] ??= ""
```

这个想法估计很多使用Swift的开发人员也都有想过。很早之前该提案就已提出，但最终被拒绝了，几个历史的关联讨论记录也没删除了，所以没法了解官方为什么拒绝该提案。

## Tuple comparison operators

**地址：**https://github.com/apple/swift-evolution/blob/main/proposals/0015-tuple-comparison-operators.md

该提案的目的是为了使tuple具有可比较性，该功能已在Swift2.2实现。

如果要比较两个tuple，需要tuple内的各个元素都要遵循Comparable且元素个数相同，等于的话需要所有元素值相等，如果是大于比较的话，会以第一个元素为准进行比较，当第一个元素相等时才会比较第二个元素，以此类推。

```swift
typealias customTuples = (first: String, second: Int)

let tuples1: customTuples = (first: "123", second: 123)

let tuples2: customTuples = (first: "124", second: 122)

let result = tuples1 < tuples2 //true
```

需要注意下 tuple 最多包含6个元素的Tuple变量进行比较，超过这个数量，Swift会报错。

## Generic Type Aliases

地址：https://github.com/apple/swift-evolution/blob/main/proposals/0048-generic-typealias.md

**昨天讲的那条提案只是说了aliases需要用于具体的类型，不能用于“虚”类型，这次提案对aliases作用又进行了扩展，使得它可以声明泛型，在Swift3中支持。**

**以下是Swift标准库中Dictionary里对aliases的使用。**

```swift
public struct Dictionary<Key, Value> where Key : Hashable {

  /// The element type of a dictionary: a tuple containing an individual

  /// key-value pair.

  public typealias Element = (key: Key, value: Value)

}
```

也可以对泛型进行约束

```swift
typealias DictionaryOfStrings<T: Hashable> = Dictionary<T, String>
```

## Importing Objective-C Lightweight Generics

**对应0057号提案：****https://github.com/apple/swift-evolution/blob/3abbed3edd12dd21061181993df7952665d660dd/proposals/0057-importing-objc-generics.md**

OC支持这种NSArray<NSString *> * 轻量级的泛型，用于桥接[String]。

该提案提出一些针对OC泛型更自由的写法：

可以在OC中写如下代码：

```objectivec
@interface MySet<T : id<NSCopying>> : NSObject

-(MySet<T> *)unionWithSet:(MySet<T> *)otherSet;

@end

@interface MySomething : NSObject

- (MySet<NSValue *> *)valueSet;

@end
```

转换成Swift就是：

```swift
class MySet<T : NSCopying> : NSObject {

 func unionWithSet(otherSet: MySet<T>) -> MySet<T>

}

class MySomething : NSObject {

 func valueSet() -> MySet<NSValue>

}
```

这里泛型T还限定了，参与构造的类型需要遵守NSCopying协议。

这么做的目的一个是为了桥接Swift里的泛型，还有就是用于支持OC中泛型的使用场景。

```swift
Optional Value Setter ??=

really.long.lvalue[expression] = really.long.lvalue[expression] ?? “"

//to

eally.long.lvalue[expression] ??= “”
```



## Removing var from Function Parameters

改提案已被采纳，在Swift3中应用。

看例子：

```swift
func foo(i: Int) {

 i += 1 // illegal

}

func foo(var i: Int) {

 i += 1 // OK, but the caller cannot observe this mutation.

}

func doSomethingWithInout(inout i: Int) {

 i += 1 // This will have an effect on the caller's Int that was passed.

}
```

在Swift3之前第二种写法是允许的，但被废弃了，原因有两个：

1、var和inout作用类似，容易引起开发的疑惑

2、var会使指类型拥有引用语义

另外可以使用这种形式替代原有var的写法，这也不会对外界的值产生影响。

func foo(i: Int) {

 var i = i

}

## Swift里的Result

Result的讨论对应 0235号提案：https://github.com/apple/swift-evolution/blob/master/proposals/0235-add-result.md 由Chris Lattner审查，已被采用并在Swift5中支持。

它主要是优化异步网络请求结果解析问题的，通常的网络请求会出现成功或者失败两种情况，你可能会这样处理：

```swift
URLSession.shared.dataTask(with: url) { (data, response, error) in

  guard error != nil else { self.handleError(error!) }

  guard let data = data, let response = response else { return // Impossible? }

  handleResponse(response, data: data)

}
```

而请求结果的成功或者失败应该是互斥，不可能同时存在或者同时不存在，这在上面的写法中并不能体现，于是出现了Result，你可以这样处理上面的请求：

```swift
URLSession.shared.dataTask(with: url) { (result: Result<(response: URLResponse, data: Data), Error>) in // Type added for illustration purposes.

  switch result {

  case let .success(success):

    handleResponse(success.response, data: success.data)

  case let .error(error):

    handleError(error)

  }
}
```

这就是Result的做法，你可以自定义实现，也可以在Swift5直接使用它：

```swift
enum Result<Success, Failure> where Failure : Error
```

关于该写法OneV曾经有篇博客讨论过：https://onevcat.com/2018/10/swift-result-error/

另外Result还有个功能是分割throw里的Error。

## 什么是Never

在Swift语言里有一个枚举是Never，它不包含任何内容：enum Never {}

Never的作用是代替@noreturn，这是Joe Groff在SE-0102里的提案：https://github.com/apple/swift-evolution/blob/master/proposals/0102-noreturn-bottom-type.md，Swift3已经引入了该类型。

它的作用是向编译器保证，该情况不会发生，不需额外检查。

举一个例子，Swift标准库里有一个Result的枚举：

```swift
enum Result<Success, Failure> where Failure : Error
```

它可以作为异步请求的返回值，我们在回调时需同时处理成功了错误回调。那对于一种特殊情况，它会永远返回正确的结果，即不需要处理错误。这时就可以使用Never实现：

```swift
Result<Success, Never>
```

这时接收回调结果的枚举解析，只处理success的情况就可以了。

参考：https://nshipster.cn/never/