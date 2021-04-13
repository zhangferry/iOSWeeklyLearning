![](https://gitee.com/zhangferry/Images/raw/master/gitee/20210411201820.png)

## 前言

Apple 在 WWDC 2019 上宣布了 Mac Catalyst 技术，其作用是将 UIKit 从 iOS 移植到 macOS 上。我们可以在 Xcode 11 及更高版本中使用 Mac Catalyst 技术来为 iPad App 创建 Mac 版本，只需勾选一个复选框即可开启这项技术，但实际上成功创建完 Mac 版本并不这么轻松，我们还需要解决编译以及更多的适配问题。

在本篇文章中，我们谈一谈过程中基本上都会遇到的二进制库链接问题 “building for Mac Catalyst, but linking in object file built for iOS Simulator” 及其解决方案。

## 问题原因

二进制库中的 x86_64 架构指令是来自 iOS Simulator 的编译产物，其不适用于 Mac Catalyst，导致在 Mac Catalyst 下编译时链接出错。

## 解决方案

### 方案一：给二进制库添加 Mac Catalyst 支持

需要考虑两种情况：

**二进制库继续以 .a 或 .framework 的形式**

为解决这一问题，我们需要将 Mac 支持的架构合入到 fat 库，但通常会遇到这样的问题：

```
... and ... have the same architectures (archName) and can't be in the same fat output file
```

意为相同的架构指令不能合并到一个 fat 库中。

就比如，Xcode12 以上编译出的 iOS Simulator 是带有 arm64 架构指令的，为解决合成 fat 库报以上错误问题，我们需将 iOS Simulator 的 arm64 去除才能继续执行合并操作。但现在，iOS Simulator 和 Mac Catalyst 的 x86_64 都是必须，该怎么办呢？解决方案是为 Mac Catalyst 编译出 x86_64h，这样就能将其和 iOS Simulator 的 x86_64 进行合并。

但是，如果我们直接使用 ：

```bash
xcodebuild  -project "xxx.xcodeproj" -scheme "xxx" -destination  "generic/platform=macOS,variant=Mac Catalyst,name=Any Mac" ARCHS="x86_64h" -configuration "Release" 
```

命令尝试编译出包含 x86_64h 的 Mac Catalyst 二进制库的话，将会得到错误：

```
None of the architectures in ARCHS (x86_64h) are valid. Consider setting ARCHS to $(ARCHS_STANDARD) or updating it to include at least one value from VALID_ARCHS (arm64, armv7, armv7s, x86_64). (in target 'xxx' from project 'xxx')
```

原因是 Apple 的标准体系架构指令中默认是不包含 x86_64h 的。这就需要在 Build Settings 中给 `Architectures` 添加上 x86_64h，同时需要在 `User-Defined > VALID_ARCHS` 中添加上 x86_64h，因为该列表和 Architectures 列表的交集，才是 Xcode 最终生成二进制包所支持的指令集。

完成后我们将会在 Xcode 中看到设备多出了 My Mac (Intel (x86_64h)) 选项，这时候即可编译出含 x86_64h 的二进制库。

最后我们就可以合成包含 armv7、armv64、i386、x86_64、x86_64h 的 fat 库，这个库将同时支持 iOS、iOS Simulator 和 Mac Catalyst。

**二进制库转为 xcframework 形式**

相比较 fat 库，更推荐的方式是创建包含 iOS、iOS Simulator 和 Mac Catalyst 三种 Framework 变体的 XCFramework。XCFramework 是由 Xcode 创建的可分发二进制框架，它包含 framework 或 library 的变体，以便可以在多个平台（iOS、macOS、tvOS 和 watchOS）包括在 simulator 上使用。

XCFramework 是目前苹果支持且推荐的一种二进制框架格式。XCFramework 相比 Framework 有很多优点，感兴趣的话可以查阅相关资料。最后我们所需要的 xcframework 文件是以下这样的：

```swift
|____xxx.xcframework
| |____Info.plist
| |____ios-arm64_armv7
| | |____xxx.framework
| |____ios-arm64_i386_x86_64-simulator
| | |____xxx.framework
| |____ios-arm64_x86_64-maccatalyst
| | |____xxx.framework
```

### 方案二：阉割不支持的库及功能

让 Xcode 跳过那些不支持 macOS 架构的库的链接和编译阶段，也就是功能阉割。这是必要的，因为对于自家的二进制库可以很轻松的提供 xcframework，但对于三方库就不太好办了，只能联系第三方来给我们提供支持。还有就是有些库本身就不适用于 Mac 端，比如三方分享、一键登录等。这时候就需要针对 Mac 端对这些功能进行阉割，那具体要怎么进行阉割呢？

1、对于 Apple 自己的库，在我们启用 Mac Catalyst 技术时，Xcode 会尽可能为我们项目的 Mac 构建版本自动排除不兼容的框架。

2、对于手动集成的库，我们可以在 `General - Frameworks, Libraries, and Embedded Content` 中将它的 Platforms 设置为 iOS only。

3、我想大家还是比较关心通过 Cocoapods 集成的库怎么限制平台。

**对于动态库**

在 `Pods - project - framework target - Build phases - Compile Sources` 中将 .m 文件的 Platforms 设置为 iOS only，以跳过它们的编译。

**对于静态库**

由于它们已经被编译所以仅需链接即可。每当我们运行 pod install 或 pod update 时，CocoaPods 都会为我们生成一个 .xcconfig 配置文件。这些文件保存在我们的项目目录下。

```bash
${PODS_ROOT}/Target Support Files/Pods-MyAppTargetName/Pods-MyAppTargetName.debug.xcconfig
${PODS_ROOT}/Target Support Files/Pods-MyAppTargetName/Pods-MyAppTargetName.release.xcconfig
${PODS_ROOT}/Target Support Files/Pods-MyAppTargetName/Pods-MyAppTargetName.distribute.xcconfig
```

在该文件中我们可以看到以下配置内容：

```bash
OTHER_LDFLAGS = $(inherited) -ObjC -framework "FrameworkThatNotSupportsCatalyst" -framework "FrameworkThatSupportsCatalyst"
```

该配置内容所对应的就是 `App Target - Build Settings - Linking - Other Linker Flags` 的配置，我们要做的事情更改这部分内容，将仅支持 iOS 和 iPadOS 的库剥离出来，不让其参与 Mac 平台的链接。

```bash
OTHER_LDFLAGS = $(inherited) -ObjC -framework "FrameworkThatSupportsCatalyst"

OTHER_LDFLAGS[sdk=iphone*] = $(inherited) -ObjC -framework "FrameworkThatNotSupportsCatalyst"
```

**流程自动化**

你可以在这里获取脚本 [fermoya/remove_unsupported_libraries.rb](https://gist.github.com/fermoya/f9be855ad040d5545ae3cb254ed201e4 "fermoya/remove_unsupported_libraries.rb")，并将该脚本放在 Podfile 的同一目录下。

然后在 Podfile 中添加以下内容：

```bash
# Podfile
load 'remove_unsupported_libraries.rb'
target 'My target' do   
    use_frameworks!   
    # Install your pods   pod 
    ...
end
def unsupported_pods_forMacCatalyst   
    ['Bugly', 'UMCAnalytics', 'QQSDK', ...]
end
def supported_pods_forMacCatalyst   
    []
end
post_install do |installer|   
    $verbose = true # remove or set to false to avoid printing
    installer.configure_support_catalyst(supported_pods_forMacCatalyst, unsupported_pods_forMacCatalyst)
end
```

该部分内容摘自：

   - [https://betterprogramming.pub/macos-catalyst-debugging-problems-using-catalyst-and-cocoapods-579679150fa9](https://betterprogramming.pub/macos-catalyst-debugging-problems-using-catalyst-and-cocoapods-579679150fa9)
   - [https://betterprogramming.pub/why-dont-my-pods-compile-with-mac-catalyst-and-how-can-i-solve-it-ffc3fbec824e](https://betterprogramming.pub/why-dont-my-pods-compile-with-mac-catalyst-and-how-can-i-solve-it-ffc3fbec824e)


阉割完成后，我们还需要为使用到这些库的代码包上以下宏，以让 Xcode 在选择 Mac 端编译时忽略这些代码，否则会在编译时得到许多的 Undefined symbol 错误。

```swift
// Swift
#if !targetEnvironment(macCatalyst) 
// Code to exclude from Mac. 
#endif

// Objective-C
#if !TARGET_OS_MACCATALYST  // or !TARGET_OS_UIKITFORMAC
// Code to exclude from Mac. 
#endif
```

## 写在最后

使用 Mac Catalyst 技术来为 iPad App 创建 Mac 版本的过程中还有很多的适配问题需要处理，在研发收尾后我会发布一篇比较全面的，希望对大家有帮助。

