# iOS摸鱼周报 第十六期

![](https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png)

iOS摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

## 开发Tips

### 图片压缩

在 iOS 减包的 Tip 中，我们了解到资源问题是影响包大小的主要部分，而图片资源是开发过程中最常见的。使用正确的图片压缩工具能够有效的进行减包。

#### 有损压缩和无损压缩

常见的压缩工具有 tinypng，pngquant，ImageAlpha、ImageOptim、pngcrush、optipng、pngout、pngnq、advpng 等，根据其压缩方式分成两大阵营：有损压缩和无损压缩

根据资料显示，tinypng、pngquant、ImageAlpha、pngnq 都是有损压缩，基本采用的都是quantization算法，将 24 位的 PNG 图片转换为 8 位的 PNG 图片，减少图片的颜色数；pngcrush、optipng、pngout、advpng 都是无损压缩，采用的都是基于 LZ/Huffman 的DEFLATE 算法，减少图片 IDAT chunk 区域的数据。一般有损压缩的压缩率会大大高于无损压缩。

#### 推荐压缩工具

对于项目中常见的背景图、占位图和大的标签图来说，推荐使用以下两种工具

* [TinyPNG4Mac](https://github.com/kyleduo/TinyPNG4Mac)：利用 [tinify](https://tinify.cn) 提供的API，目前 tinify 的免费版压缩数量是单词不超过 20 张且大小不超过 5 M。对于一般的 iOS 应用程序来说，足够日常开发的使用
* [ImageOptim-CLI](https://github.com/JamieMason/ImageOptim-CLI)：自动先后执行压缩率较高的为 [ImageAlpha](http://pngmini.com/) 的有损压缩 加上 [ImageOptim](https://imageoptim.com/) 的无损压缩。

可以通过查看[这个表格](http://jamiemason.github.io/ImageOptim-CLI/comparison/png/photoshop/desc/)对比 TinyPng 和 ImageOptim-CLI 。

对于小图来说，例如我们常见的 icon 图标来说，我们通过改变其编码方式为 RGB with palette 来达到图片压缩效果。你可以使用 ImageOptim 改变图片的编码方式为 RGB with palette。

```shell
imageoptim -Q --no-imageoptim --imagealpha --number-of-colors 16 --quality 40-80 ./1.png
```

通过 [Palette Images](http://www.manifold.net/doc/mfd9/palette_images.htm) 深入了解 `palette`。

这里的压缩是指使用 Xcode 自带的压缩功能。

#### Xcode `负优化`

我们一般使用  Assets Catalogs 对图片资源进行管理。其会存在对应的优化方式

![](https://raw.githubusercontent.com/LoneyIsError/blog_images/main/640.webp)

在构建过程中，Xcode 会通过自己的压缩算法重新对图片进行处理。在构建 Assets Catalogs 的编译产物 Assest.car 的过程中，Xcode 会使用 `actool` 对  Assets Catalogs  中的 png 图片进行解码，由此得到 Bitmap 数据，然后再运用 actool 的编码压缩算法进行编码压缩处理。所以不改变编码方式的无损压缩方法最终的包大小来说，可能没有什么作用。

对同一张图片，在不同设备、iOS 系统上 Xcode 采用了不同的压缩算法这也导致了下载时候不同的设备针对图片出现大小的区别。

你可以利用 `assetutil` 工具分析 `Assest.car` 来得到其具体的压缩方法

```shell
sudo xcrun --sdk iphoneos assetutil --info ***.app/Assets.car > ***.json
```

其注意 `Compression` 、`Encoding`、`SizeOnDisk`。

> 可以在  Assets Catalogs 中添加 jpg 文件，然后找到对应的文件部分，判断其是否会被转换成 png 格式

```json
 {
    "AssetType" : "Image",
    "BitsPerComponent" : 8,
    "ColorModel" : "RGB",
    "Colorspace" : "srgb",
    "Compression" : "deepmap2",
    "Encoding" : "ARGB",
    "Name" : "image",
    "NameIdentifier" : 51357,
    "Opaque" : false,
    "PixelHeight" : 300,
    "PixelWidth" : 705,
    "RenditionName" : "image.png",
    "Scale" : 1,
    "SHA1Digest" : "294FEE01362591334E3C3B4ECE54AF0EA8491781",
    "SizeOnDisk" : 113789,
    "Template Mode" : "automatic"
  }
```

如果启用  APP Thinning 来生成不同设备的 ipa 包，然后针对每个 ipa 包都进行一次解压缩，并获取其中的 Assets.car 导出对应的 assets.json 似乎有些冗余，你也可以利用京东商城的 APP 瘦身实践中提及的  `assetutil`  的方法从通用包的 Assets.car 文件导出指定设备的 Assets.car 文件

```shell
sudo xcrun --sdk iphoneos assetutil --idiom phone --subtype 570 --scale 3 --display-gamut srgb --graphicsclass MTL2,2 --graphicsclassfallbacks MTL1,2:GLES2,0 --memory 1 --hostedidioms car,watch xxx/Assets.car -o xxx/thinning_assets.car
```

#### 压缩的`危害`

不要盲目的追求最大的压缩比，既需要考虑压缩出图片的质量，也需要考虑经过 Xcode 最终构成文件的真实大小。

压缩完成的图片尽量在高分辨率的设备上看看会不会有什么问题，让 UI 妹子好好看看，会不会出现噪点、毛边等现象。

如果一个图片经过有损压缩最终导致其在 Assets.car 中 `SizeOnDisk` 值变得很大的话，但其在各个设备上的表现情况又挺好，你可以尝试将其加到 bundle 中使用，并将其图片格式修改为 `Data`，这样 Xcode 就不会对齐进行压缩处理了。不过不要忘记将调用方法改为 `imageWithContentOfFile:`。

![](https://raw.githubusercontent.com/LoneyIsError/blog_images/main/截屏2021-06-25 17.44.37.png)

![](https://raw.githubusercontent.com/LoneyIsError/blog_images/main/截屏2021-06-25 17.44.37.png)




## 那些Bug


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