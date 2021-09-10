# iOS摸鱼周报 第二十七期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

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

### iOS 识别虚拟定位调研 

整理编辑：[FBY展菲](https://github.com/fanbaoying)

#### 前言

最近业务开发中，有遇到我们的项目 app 定位被篡改的情况，在 `android` 端表现的尤为明显。为了防止这种黑产使用虚拟定位薅羊毛，`iOS` 也不得不进行虚拟定位的规避。

#### 第一种：使用越狱手机

一般 app 用户存在使用越狱苹果手机的情况，一般可以推断用户的行为存在薅羊毛的嫌疑（也有 app 被竞品公司做逆向分析的可能），因为买一部越狱的手机比买一部正常的手机有难度，且在系统升级和 `appstore` 的使用上，均不如正常手机，本人曾经浅浅的接触皮毛知识通过越狱 `iPhone5s` 进行的 app 逆向。

**代码实现**

```swift
/// 判断是否是越狱设备
/// - Returns: true 表示设备越狱
func isBrokenDevice() -> Bool {
    
    var isBroken = false
    
    let cydiaPath = "/Applications/Cydia.app"
    
    let aptPath = "/private/var/lib/apt"
    
    if FileManager.default.fileExists(atPath: cydiaPath) {
        isBroken = true
    }
    
    if FileManager.default.fileExists(atPath: aptPath) {
        isBroken = true
    }
    
    return isBroken
}
```

#### 第二种：使用爱思助手

对于使用虚拟定位的场景，大多应该是司机或对接人员打卡了。而在这种场景下，就可能催生了一批专门以使用虚拟定位进行打卡薅羊毛的黑产。对于苹果手机，目前而言，能够很可以的实现的，当数爱思助手的虚拟定位功能了。

**使用步骤：** 下载爱思助手 mac 客户端，连接苹果手机，工具箱中点击虚拟定位，即可在地图上选定位，然后点击修改虚拟定位即可实现修改地图的定位信息。

**原理：** 在未越狱的设备上通过电脑和手机进行 `USB` 连接，电脑通过特殊协议向手机上的 `DTSimulateLocation` 服务发送模拟的坐标数据来实现虚假定位，目前 `Xcode` 上内置位置模拟就是借助这个技术来实现的。

**识别方式**

一、通过多次记录爱思助手的虚拟定位的数据发现，其虚拟的定位信息的经纬度的高度是为 0 且经纬度的数据位数也是值得考究的。

二、把定位后的数据的经纬度上传给后台，后台再根据收到的经纬度获取详细的经纬度信息，对司机的除经纬度以外的地理信息进行深度比较，优先比较 `altitude`、`horizontalAccuracy`、`verticalAccuracy` 值，根据值是否相等进行权衡后确定。

三、具体识别流程

* 通过获取公网 `ip`，大概再通过接口根据 `ip` 地址可获取大概的位置，但误差范围有点大。
* 通过 `Wi-Fi` 热点来读取 `app` 位置
* 利用 `CLCircularRegion` 设定区域中心的指定经纬度和可设定半径范围，进行监听。
* 通过 `IBeacon` 技术，使用 `CoreBluetooth` 框架下的 `CBPeripheralManager` 建立一个蓝牙基站。这种定位直接是端对端的直接定位，省去了 `GPS` 的卫星和蜂窝数据的基站通信。

四、iOS防黑产虚假定位检测技术 文章的末尾附的解法本人有尝试过，一层一层通过 kvc 读取 CLLocation 的 _internal 的 fLocation，只能读取到到此。

代码实现太多，可以**阅读原文**获取

参考：[iOS 识别虚拟定位调研](https://mp.weixin.qq.com/s/ZbZ4pFzzyfrQifmLewrxsw "iOS 识别虚拟定位调研")

## 面试解析

整理编辑：[师大小海腾](https://juejin.cn/user/782508012091645/posts)


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
