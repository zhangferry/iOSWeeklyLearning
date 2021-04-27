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
