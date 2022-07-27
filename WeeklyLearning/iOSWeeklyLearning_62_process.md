# iOS 摸鱼周报 #62

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：
> * 岗位推荐：

## 本期话题



## 本周学习

整理编辑：[夏天](https://juejin.cn/user/3298190611456638)

### iOS 使用 Pod 在现有项目上集成 React Native

#### 问题背景

现有前端开发人员的技术栈为 React，在实践中尝试集成 RN

原生项目与 RN 项目为双独立项目，互不干预

现有项目较小，未涉及到组件化，且暂时未有相关沉淀

#### 解决方案

首先，获取 React Native  项目：我们将 RN 项目作为子项目集成现有原生项目中，利用 Git 提供的子模块功能，将一个 、RN  仓库作为 iOS 仓库的子目录。 子模块能让你将另一个仓库克隆到自己的项目中，同时还保持提交的独立。

> git submodule add <url> <repo_name>

其次，搭建 RN 开发环境，进入到 RN  的子目录中，参照[搭建开发环境](https://www.react-native.cn/docs/environment-setup)完成 [Node](http://nodejs.cn)、[Watchman](https://facebook.github.io/watchman)、[Yarn](http://yarnpkg.com/) 的安装，并通过命令安装 RN

> yarn add react-native

这里需要注意的是，我们是根据已有的子某块来创建的，所以我们还需要安装指定版本的 React

> yarn add react@xx.xx.xx

再次，安装成功之后，我们通过 CocoaPods 来完成相关依赖的安装。建议使用官方推荐 Podfile 完成安装

```ruby
require_relative '../node_modules/react-native/scripts/react_native_pods'
require_relative '../node_modules/@react-native-community/cli-platform-ios/native_modules'

platform :ios, '12.4'
install! 'cocoapods', :deterministic_uuids => false

production = ENV["PRODUCTION"] == "1"

target 'HelloWorld' do
  config = use_native_modules!

  # Flags change depending on the env values.
  flags = get_default_flags()

  use_react_native!(
    :path => config[:reactNativePath],
    # to enable hermes on iOS, change `false` to `true` and then install pods
    :production => production,
    :hermes_enabled => flags[:hermes_enabled],
    :fabric_enabled => flags[:fabric_enabled],
    :flipper_configuration => FlipperConfiguration.enabled,
    # An absolute path to your application root.
    :app_path => "#{Pod::Config.instance.installation_root}/.."
  )

  target 'HelloWorldTests' do
    inherit! :complete
    # Pods for testing
  end
  
end
```

你可以将 `react_native_pods` 文件移到原生项目目录，移除 `hermes` 和 `fabric` 这两个三方库，其余为 RN 必备的核心库。`native_modules` 中对应的是项目中添加的其他三方依赖的内容，你也可以手动安装。

最后，新增官网项目中的两个 `Build Phase` 用于启动 RN 服务。分别是

```shell
export RCT_METRO_PORT="${RCT_METRO_PORT:=8081}"
echo "export RCT_METRO_PORT=${RCT_METRO_PORT}" > "${SRCROOT}/../node_modules/react-native/scripts/.packager.env"
if [ -z "${RCT_NO_LAUNCH_PACKAGER+xxx}" ] ; then
  if nc -w 5 -z localhost ${RCT_METRO_PORT} ; then
    if ! curl -s "http://localhost:${RCT_METRO_PORT}/status" | grep -q "packager-status:running" ; then
      echo "Port ${RCT_METRO_PORT} already in use, packager is either not running or not running correctly"
      exit 2
    fi
  else
    open "$SRCROOT/../node_modules/react-native/scripts/launchPackager.command" || echo "Can't start packager automatically"
  fi
fi
```

和

```shell
set -e

WITH_ENVIRONMENT="../node_modules/react-native/scripts/xcode/with-environment.sh"
REACT_NATIVE_XCODE="../node_modules/react-native/scripts/react-native-xcode.sh"

/bin/sh -c "$WITH_ENVIRONMENT $REACT_NATIVE_XCODE"
```

至此，完成了在 iOS 中使用 Pod 在现有项目上集成 RN

以上就是单应用集成 RN 的方式，建议可以比对 CLI 自动化处的 iOS 项目来创造属于自己的脚本。

### 参考资料

[iOS 已有项目利用Pod集成RN](https://blog.csdn.net/ljmios/article/details/119451577)

[git-submodules](https://git-scm.com/docs/git-submodule)

## 内容推荐

1、 [开源｜WBBlades重要节点更新-专为提效而设计](https://mp.weixin.qq.com/s/tXxhnDKerobyxoWuEBGjNQ) -- 来自：58技术

[@皮拉夫大王]()：给iOS开发人员提供基于Mach-O文件解析的工具集，工具包括无用类检测（支持OC和Swift）、包大小分析（支持单个静态库/动态库的包大小分析）、点对点崩溃解析（基于系统日志，支持有符号状态和无符号状态），主要基于Mach-O文件的分析、轻量符号表剥离，系统日志解析等技术手段。

2、[iOS不必现崩溃的点对点解析以及治理](https://mp.weixin.qq.com/s/tGvE-2flzhm4skkrfbUIBA) -- 来自：58技术

[@皮拉夫大王]()：本文章中介绍iOS端发生崩溃后，在无法复现的情况下如何针对各种不同类型的崩溃日志进行解析，包括普通堆栈，wakesup崩溃，json格式日志，bugly堆栈类型等。此外还介绍了系统日志存在异常情况进行自动修正的方法，包括进程名称丢失，基地址丢失，偏移地址错误等。

## 摸一下鱼



## 岗位推荐



## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #56 | WWDC 进行时](https://mp.weixin.qq.com/s/ZyGV6WlFsZOX6Aqgrf1QRQ)

[iOS 摸鱼周报 #55 | WWDC 码上就位](https://mp.weixin.qq.com/s/zDhnOwOiLGJ_Nwxy5NBePw)

[iOS 摸鱼周报 #54 | Apple 辅助功能持续创新](https://mp.weixin.qq.com/s/6jdqa143Y5yr6lbjCuzlqA)

[iOS 摸鱼周报 #53 | 远程办公正在成为趋势](https://mp.weixin.qq.com/s/5chb-a9u7VMdLis1FG6B6Q)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
