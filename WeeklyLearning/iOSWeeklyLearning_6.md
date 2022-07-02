# iOS摸鱼周报 第六期

![](https://cdn.zhangferry.com/Images/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享大家开发过程遇到的经验教训及学习内容。虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug经历。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips

开发小技巧收录。

### YYModel解析数据提供默认值

当在OC中使用YYModel解析JSON数据时，对于不存在或者返回`null`的数据都会按照`nil`处理。而有些时候我们可能不希望该字段被置为nil，而是希望提供一个默认值，比如NSString类型，如果无法解析就返回`@""`，空字符串。这在一些需要把特定参数包到NSDictionary或者NSArray里的场景不会引起崩溃，也省去了一些判断判空的代码。

实现这个目的需要两个步骤：

**1、找到特性类型的属性**

可以使用runtime提供的`property_copyAttributeList`方法，主要代码是：

```objectivec
static const char *getPropertyType(objc_property_t property) {
    //这里也可以利用YYClassPropertyInfo获取对应数据
    unsigned int attrCount;
    objc_property_attribute_t *attrs = property_copyAttributeList(property, &attrCount);
    if (attrs[0].name[0] == 'T') {
        return attrs[0].value;
    }
    return "";
}
```

通过`attrs[0].name[0] == 'T'`找到对应属性的编码类型，取出value，NSString对应的`value`是`@"NSString"`。

其他的编码类型可以参考[这里](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html#//apple_ref/doc/uid/TP40008048-CH100-SW1 "Objective-TypeEncodings")。

找到需要替换的属性就可以替换了，使用KVC的形式：

```objectivec
[self setValue:obj forKey:propertyName];
```

**2、在JSON换Model完成的时候进行默认值替换**

这段函数写到哪里合适呢，在NSObject+YYModel.h里找到了这个方法：

```objectivec
- (BOOL)modelCustomTransformFromDictionary:(NSDictionary *)dic;
```

该方法用于校验转成的Model是否符合预期，执行到这里时Model已经完成了转换，我们就可以在这里调用上面写的默认值替换方法。

**封装使用**

我已经写好了一个实现，代码在[这里](https://github.com/zhangferry/YYModel/blob/master/YYModel/NSObject%2BDefaultValue.m "NSObject+DefaultValue")。

使用的时候我们只需在Model类里引用`NSObject+DefaultValue.h`这个头文件，然后实现这个方法即可：

```objectivec
- (YYPropertyType)provideDefaultValueType {
    return YYPropertyTypeNSString;
}
```

表明我们需要将类中的所有属性在不存在的时候用空字符串代替。

**备注**：YYModel有个[issue](https://github.com/ibireme/YYModel/issues/66 "YYModel issue 66")是讨论这个问题的，但是听作者的意思，这个扩展不应该放到这个库里，所以也就没有当做PR提过去。

### iOS11支持的架构调整

i386架构现在已经用的很少了，它是intel的32位架构，对于iPhone5及以下的模拟器会使用到。虽然用的不多但很多脚本（例如CocoaPods）还是需要这个架构的支持。Xcode12已经移除了iPhone5的模拟器，如果想打出这个架构的包，默认情况是不可行的。我们可以将Build Setting里`Build Active Architecture Only`里的Debug选项置为NO，这样编译出的包是带所有架构的，包括i386。

但是当我们把包的最低支持版本设置为iOS11及以上，这时编译的包就没有i386了，应该是苹果做了移除该架构的处理。如果我们仍需要导出这个架构，就需要用`xcodebuild`命令指定架构实现了，实现命令如下：

```shell
$ xcodebuild -project ProjectName.xcodeproj -target TargetName -sdk iphonesimulator -arch i386 -configuration Debug -quiet BUILD_DIR=build
```

## 编程概念

### 什么是关系型数据库

关系型数据库，是指采用了关系模型来组织数据的数据库。

关系模型是在1970年由IBM的研究员E.F.Codd博士首先提出的，在之后的几十年中，关系模型的概念得到了充分的发展并逐渐成为主流数据库结构的主流模型。

简单来说，关系模型指的就是二维表格模型，而一个关系型数据库就是由二维表及其之间的联系所组成的一个数据组织。

关系型数据库的代表是：SQL Server、Oracle、Mysql

他们的优点是容易理解，二维表结构也更贴近现实世界，使用起来也很方便，使用通用的SQL语句就可以完成增删改查等操作。关系型数据库另一个比较大的优势是它的完整可靠，大大降低了数据冗余和数据不一致的概率。

但很多事物都用两面性，关系数据库也不例外，它在处理高并发，通常每秒在上万次的读写请求时，硬盘I/O就会面临很大的瓶颈问题。

### 什么是非关系型数据库
非关系型数据库也叫NoSQL，用于区别依赖SQL语句的关系数据库，NoSQL还有另一层解读：Not only SQL。

非关系型数据库主要是用于解决关系型数据库面临的高并发读写瓶颈，这个类型数据库种类繁多，但都有一个共同点，就是去掉关系数据库的关系型特性，使得数据库的扩展更加容易。

但它也有一定的缺点就是无事务处理，数据结构相对复杂，处理复杂查询时相对欠缺。

非关系数型数据库分为4大类：

文档型：常用于Web应用，典型的有MongoDB、CouchDB

Key-Value型：处理大量数据的高访问负载，内容缓存，典型的有Redis、Oracle BDB

列式数据库：处理分布式的文件系统，典型的有Cassandra、HBase

图形数据库：用于社交网络，推荐系统，典型的有Neo4J、InfoGrid

SQL和NoSQL没有孰强孰弱，NoSQL也并不会代替SQL，只有结合自身的业务特点才能发挥出这两类数据库的优势。

### 什么是ACID
ACID是指数据库管理系统在写入或者更新资料时，为保证事务可靠性，所必须具有的四个特性。
A（atomicity）指原子型：一个事务里的所有操作，要么全部完成，要么全部不完成，不存在中间状态，如果中间过程出错，就回滚到事务开始前的状态。

C（consistency）一致性：在事务开始之前和结束之后，数据库完整性没有被破坏。

I（isolation）隔离性：数据库允许多个并发事务同时对其数据进行读写和修改的能力，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致。

D（durability）持久性：事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。
通常关系型数据库都是遵守这四个特性的，而非关系型数据库通常是打破了四个特性的某几条用于实现高并发、易扩展的能力。

### 什么是数据库范式
简单的说，范式是为了消除重复数据减少冗余数据，从而让数据库内的数据更好的组织，让磁盘空间得到更有效利用的一种标准化规范，满足高等级的范式的先决条件是满足低等级范式。(比如满足2nf一定满足1nf)。

范式只是针对关系型数据库的规范，当前有六种范式：第一范式（1NF）、第二范式（2NF）、第三范式（3NF）、巴斯-科德范式（BCNF），第四范式（4NF）和第五范式（5NF）又被称为完美范式。这里的NF是Normal form的缩写，翻译为范式。

1NF就是每一个属性都不可再分。不符合第一范式则不能称为关系数据库。

2NF要求数据库表中的每个实例或记录必须可以被唯一地区分。

3NF要求一个关系中不包含已在其它关系已包含的非主关键字信息。

BCNF是在3NF基础上，任何非主属性不能对主键子集依赖（在3NF基础上消除对主码子集的依赖）

4NF是消除表中的多值依赖，也就是说可以减少维护数据一致性的工作。

如果它在4NF 中并且不包含任何连接依赖关系并且连接应该是无损的，则关系在5NF 中。

使用的范式越高则表越多，表多就会带来更高的查询复杂度，使用何种范式需跟实际情况而定，通常满足BCNF即可。

### 什么是ER图
ER图是 Entity Relationship Diagram 的简写，也叫实体关系图，它主要应用于数据库设计的概念设计阶段，用于描述数据之间的关系。

它有三种主要元素：

1、实体：表示数据对象，使用矩形表示

2、属性：表示对象具有的属性，使用椭圆表示

3、联系：表示实体之间的关系，使用菱形表示，关联关系有三种：1:1 表示一对一，1：N表示一对多，M : N表示多对多。

使用直线将联系的各方进行连接。

![](https://cdn.zhangferry.com/Images/20210314140748.png)

横线表示键，双矩形表示弱实体，成绩单依赖于学生而不可单独存在。

### 什么是数据库索引
索引是对数据库表中一列或者多列的值进行排序的一种数据接口。使用索引可以加快数据的查找，但设置索引也是有一定代价的，它会增加数据库存储空间，增加插入，删除，修改数据的时间。

数据库索引能够提高查找效率的原因是索引的组织形式使用B+树（也可能是别的平衡树），B+树是一种多叉平衡树，查找数据时可以利用类似二分查找的原则进行查找，对于大量的数据的查找，它可以显著提高查找效率。

因为使用平衡树的缘故对于删除和新增数据都可能打破原有树的平衡，就需要重新组织数据结构，维持平衡，这就是增加索引耗时的原因。

对于非聚集索引（非主键字段索引），字段数据会被复制一份出来，用于生成索引，所以会增加存储空间。对非聚集索引的查找是先查找到指定值，然后通过附加的主键值，再使用主键值通过聚集索引查找到需要的数据。

参考：[B+树详解](https://ivanzz1001.github.io/records/post/data-structure/2018/06/16/ds-bplustree#1-b%E6%A0%9 "B+树详解") 

## 优秀博客

[函数节流（Throttle）和防抖（Debounce）解析及其OC实现](https://mp.weixin.qq.com/s/h1MYGTYtYo9pcHmqw6tHBw "函数节流（Throttle）和防抖（Debounce）解析及其OC实现")  -- 来自公众号：iOS成长之路

[2021阿里淘系工程师推荐书单](https://mp.weixin.qq.com/s/zi7qWTg8xGf3GaxW6Czj2A "2021阿里淘系工程师推荐书单") -- 来自公众号：淘系技术

[分析字节跳动解决OOM的在线Memory Graph技术实现](https://juejin.cn/post/6895583288451465230 "分析字节跳动解决OOM的在线Memory Graph技术实现") -- 来自掘金：有点特色

[iOS 稳定性问题治理：卡死崩溃监控原理及最佳实践](https://juejin.cn/post/6937091641656721438 "iOS 稳定性问题治理：卡死崩溃监控原理及最佳实践") -- 来自掘金：字节跳动技术团队

[一个iOS流畅性优化工具](https://juejin.cn/post/6934720152546050078 "一个iOS流畅性优化工具") -- 来自掘金：BangRaJun

[iOS防黑产虚假定位检测技术](https://juejin.cn/post/6938197133908672519 "iOS防黑产虚假定位检测技术") -- 来自掘金：欧阳大哥2013

[【译】Flutter 2.0 正式版发布，全平台 Stable](https://juejin.cn/post/6935621027116531720 "[译]Flutter 2.0 正式版发布，全平台 Stable") -- 来自掘金：恋猫de小郭

[如何做一场高质量的分享](https://juejin.cn/post/6938208336802217991 "如何做一场高质量的分享") -- 来自掘金：相学长


## 学习资料

### iOS开发者资源大全

![](https://cdn.zhangferry.com/Images/20210313212015.png)

**推荐来源**：[cat13954](https://github.com/cat13954)

本文档针对市面上几乎所有和 iOS 开发相关的资源文档进行重新整理、融合和补充，更适合国内开发者。

文档内容包含了数十套教程、数千个框架、不计其数的工具、网站、资料等等，目前总计 4600+，涵盖了和 iOS 学习、日常工作中相关的方方面面，不管是 iOS 新手、还是老手，都是值得收藏的一个资源文档。

对于初学者来说，可以先款速浏览一下该文档，先对 iOS 整个生态提前有个完整的印象，打开眼界，对于今后的学习、工作能节省很多时间，少走一些弯路。

对于老手，本文对内容排版也做了优化，便于查找，对于 github 开源项目，也将 Star 标注出来，以便于筛选，对于支持 Swift 项目也做了相应标记。

## 工具推荐

推荐好用的工具。

### F.lux

**推荐来源**：[zhangferry](zhangferry.com)

**地址**：https://justgetflux.com/

**软件状态**：免费

**使用介绍**

电脑的显示器亮度一般是全天保持不变的，这个亮度对于白天使用来说没有任何问题，但是对于夜间使用的话就会有些刺眼，出于对视力的保护，夜间应该让屏幕亮度低一些，暖一些。

F.lux就是处理这一问题的软件，他可以根据时间调节屏幕颜色，白天亮度像太阳光，在夜间时会让屏幕看着更像是室内光。

![](https://cdn.zhangferry.com/Images/20210314141348.png)



### Kap

**推荐来源**：[highway](https://github.com/HighwayLaw)

**地址**：https://getkap.co/

**软件状态**：免费，[开源](https://github.com/wulkano/kap "Kap开源地址")

**使用介绍**

一款开源且简洁高效的屏幕录制软件，可以导出为GIF，MP4，WebM，APNG等格式，而且会有很不错的压缩率。

![](https://cdn.zhangferry.com/Images/20210313211617.png)

鉴于微信公众号对GIF的两条限制：

1、不能超过300帧

2、大小不能超过2M

我们需要对一些GIF进行修剪和压缩才能上传。

删除帧数有一个简单的方法：用Mac自带的预览功能打开GIF，选中想要删除的帧，按Command + Delete即可删除指定帧。另外对于多个连续帧的选中，可以先单击选中第一帧，再按住Shift单击选中末尾帧，即可选中这个区间连续的所有帧。

对于GIF的压缩，推荐另一个工具：docsmall。

### docsmall

**推荐来源**：[zhangferry](zhangferry.com)

**地址**：https://docsmall.com/gif-compress

**软件状态**：免费，Web端

**使用介绍**

上传需要压缩的gif文件即可

![](https://cdn.zhangferry.com/Images/20210313211739.png)

## 联系我们

[摸鱼周报第三期](https://zhangferry.com/2021/01/10/iOSWeeklyLearning_3/)

[摸鱼周报第四期](https://zhangferry.com/2021/01/24/iOSWeeklyLearning_4/)

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

![](https://cdn.zhangferry.com/Images/wechat_official.png)
