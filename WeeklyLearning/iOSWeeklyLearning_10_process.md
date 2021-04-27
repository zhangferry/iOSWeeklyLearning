# iOS摸鱼周报 第十期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享大家开发过程遇到的经验教训及学习内容。虽说是周报，但当前内容的贡献途径还未稳定下来，如果后续的内容不足一期，可能会拖更到下一周再发。所以希望大家可以多分享自己学到的开发小技巧和解bug经历。

周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，可以查看README了解贡献方式；另可关注公众号：iOS成长之路，后台点击进群交流，联系我们。

## 开发Tips



## 那些Bug

### iOS 蓝牙设备名称缓存问题总结

整理编辑：[FBY展菲](https://juejin.cn/user/3192637497025335/posts)

**问题背景**

* 当设备已经在 App 中连接成功后
* 修改设备名称
* App 扫描到的设备名称仍然是之前的名称
* App 代码中获取名称的方式为（perpheral.name）

**问题分析**

当 APP 为中心连接其他的蓝牙设备时。

首次连接成功过后，iOS系统内会将该外设缓存记录下来。

下次重新搜索时，搜索到的蓝牙设备时，直接打印 （peripheral.name），得到的是之前缓存中的蓝牙名称。

如果此期间蓝牙设备更新了名称，（peripheral.name）这个参数并不会改变，所以需要换一种方式获取设备的名称，在广播数据包内有一个字段为 kCBAdvDataLocalName，可以实时获取当前设备名称。

**问题解决**

下面给出OC 和 Swift 的解决方法：

OC

```
-(void)centralManager:(CBCentralManager *)central didDiscoverPeripheral:(CBPeripheral *)peripheral advertisementData:(NSDictionary<NSString *,id> *)advertisementData RSSI:(NSNumber *)RSSI{
        NSString *localName = [advertisementData objectForKey:@"kCBAdvDataLocalName"];
} 
```

Swift

```
func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {
        let localName = advertisementData["kCBAdvDataLocalName"]
}
```

## 编程概念

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645)，[zhangferry](https://zhangferry.com)



## 优秀博客

整理编辑：[皮拉夫大王在此](https://www.jianshu.com/u/739b677928f7)



## 学习资料

整理编辑：[Mimosa](https://juejin.cn/user/1433418892590136)

1、[LearnOpenGL CN](https://learnopengl-cn.github.io/)

欢迎来到 OpenGL 的世界。这个工程只是我([Joey de Vries](http://joeydevries.com/))的一次小小的尝试，希望能够建立起一个完善的 OpenGL 教学平台。无论你学习 OpenGL 是为了学业，找工作，或仅仅是因为兴趣，这个网站都将能够教会你现代(Core-profile)  OpenGL 从基础，中级，到高级的知识。LearnOpenGL 的目标是使用易于理解的形式，使用清晰的例子，展现现代 OpenGL 的所有知识点，并与此同时为你以后的学习提供有用的参考。

> 该教程是[原教程](https://learnopengl.com/)的中文翻译教程

2、[VisuAlgo](https://visualgo.net/en)

由新加坡国立大学的教授和学生发起、制作并完善的「数据结构和算法动态可视化」网站，在该网站你可以看到许多经典、非经典的，常见的、非常见的算法的可视化，清晰明了的图形化表现和实时的代码解读可以帮助读者更好地理解各种算法及数据结构。同时该网站支持自动问题生成器和验证器（在线测验系统）。

![Animation of Graph Traversal Algorithm](https://www.comp.nus.edu.sg/images/resources/20200309-graph-traversal.gif)

## 工具推荐

整理编辑：[brave723](https://juejin.cn/user/307518984425981/posts)

### Application Name

**地址**：

**软件状态**：

**使用介绍**



## 联系我们

[摸鱼周报第五期](https://zhangferry.com/2021/02/28/iOSWeeklyLearning_5/)

[摸鱼周报第六期](https://zhangferry.com/2021/03/14/iOSWeeklyLearning_6/)

[摸鱼周报第七期](https://zhangferry.com/2021/03/28/iOSWeeklyLearning_7/)

[摸鱼周报第八期](https://zhangferry.com/2021/04/11/iOSWeeklyLearning_8/)

![](https://gitee.com/zhangferry/Images/raw/master/gitee/wechat_official.png)
