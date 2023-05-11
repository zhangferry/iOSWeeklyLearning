# iOS 摸鱼周报 #93 | AIGC 尝试

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：App Store 5 月 9 日增强全球定价机制已更新
> * 内容推荐：模块化架构、Deep Dish Swift 总结、TabularData 框架相关博文。
> * 摸一下鱼：最近利用 AIGC 做的一些尝试；GPT 需求设想方案汇总；一个摘要总结插件 glarity；面向开发者的 ChatGPT Prompt 编写指南

## 本期话题

### [ App Store 5 月 9 日增强全球定价机制已更新](https://developer.apple.com/cn/news/upcoming-requirements/?id=05092023a " App Store 5 月 9 日增强全球定价机制已更新")

[@远恒之义](https://github.com/eternaljust)：本周二上午，有同事反馈公司的部分 App 内购商品的价格发生了变化，App 商品显示页面价格与实际付款弹窗 App Store 价格不一致，大多相差几元。这个问题是 Apple 于 5 月 9 日升级更新了增强全球定价机制导致的，如果你在 2023 年 3 月 8 日后没有修改选择 App 的基准国家或地区，那么你的 App 和一次性 App 内购买项目的价格都将默认以美国商店美元为基础，自动调整在其他国家和地区的价格。你可通过在 App Store Connect 后台[更改 App 价格的基准国家或地区](https://developer.apple.com/cn/help/app-store-connect/manage-app-pricing/set-a-price "更改 App 价格的基准国家或地区")，此变更会自动同步到 App 所关联的 App 内购买项目，App 的价格以及同步引起的 App 内购买项目价格也会立即更新生效（修改价格的操作账号必须拥有账户持有人、管理或 App 管理的职能）。

## 内容推荐

推荐近期的一些优秀博文，涵盖：模块化架构、Deep Dish Swift 总结、TabularData 框架等方面的内容。

整理编辑：[东坡肘子](https://www.fatbobman.com/)

1、[使用 SwiftUI 构建大型应用程序：模块化架构指南](https://azamsharp.com/2023/02/28/building-large-scale-apps-swiftui.html "使用 SwiftUI 构建大型应用程序：模块化架构指南") -- 作者：Mohammad Azam

[@东坡肘子](https://www.fatbobman.com/): 应用程序架构是一个复杂的话题。最终，项目的最佳架构取决于许多因素，如项目的规模和复杂性、团队的技能和经验、项目的目标和要求。本文介绍了使用 SwiftUI 构建大型应用程序时的模块化架构指南。指南涵盖了单元测试、数据和文件访问、测试视图模型而不验证用户界面以及理想的测试等方面。成功的应用程序架构的关键是选择适合项目独特需求的模式，并随着项目的发展不断对架构进行评估和调整。

2、[WWDC 2023, 我期待 SwiftUI 带来的新变化](https://www.fatbobman.com/posts/What-I-Hope-to-See-for-SwiftUI-at-WWDC-2023/ "WWDC 2023, 我期待 SwiftUI 带来的新变化") -- 作者：东坡肘子

[@东坡肘子](https://www.fatbobman.com/): 还有约 20 天就到 2023 年的 WWDC 了。开发者们都非常期待苹果会在当天带来哪些新功能。在本文中，作者希望 SwiftUI 能够提供更多原生、稳定的底层 API，例如以属性为粒度的视图关联、统一的 Gesture 逻辑、更完善的文字输入和显示、稳定、高效的 ForEach 实现、向前兼容性等。作者希望苹果能够充分利用 Swift 5.8 提供的 @backDeployed 特性，增强老版本的功能并修复 bug。

3、[Deep Dish Swift 总结](https://danielsaidi.com/blog/2023/04/30/deep-dish-swift-day-1 "Deep Dish Swift 总结") -- 作者：Daniel Saidi

[@东坡肘子](https://www.fatbobman.com/): 随着疫情得到控制，越来越多的线下活动得以顺利举办。作者用了三篇博文总结了 2023 年 Deep Dish Swift 会议的演讲内容。第一天的演讲涵盖了独立开发者的讲座、订阅模型、CI/CD 自动化和 ASO。第二天的演讲涵盖了公司销售、Swift 算法、模块化架构、导师制、Swift Playgrounds 和SwiftUI 导航。第三天的演讲涵盖了服务器端 Swift 和 GraphQL、使用 Swift 创建演示文稿、实时活动、代码风格和 DocC 文档。这次会议涵盖了广泛的 Swift 开发相关主题，使与会者从各个角度深入了解 Swift 语言。

4、[使用 TabularData 来转储模型数据](https://www.swiftjectivec.com/using-the-tabulardata-framework-to-dump-json-or-csv-data-in-swift/ "使用 TabularData 来转储模型数据") -- 作者：Jordan Morgan

[@东坡肘子](https://www.fatbobman.com/): TabularData 框架是一种用于解析 .csv 和 .json 文件的工具，可用于将这些文件导入或导出，并将日志转储到你的控制台中。通过使用数据创建 DataFrame，你可以轻松地对数据进行排序、筛选和可视化。该框架还提供了数据增强和格式化的 API，例如组合列以解码你自己的模型，或使用 numericSummary 打印出统计数据。作者分享了使用 DataFrame 进行可扫描性的小技巧，特别是在处理大量数据时。本文提供了如何创建 DataFrame 并操作数据的示例。

5、[增强 Turbo Native 应用程序：如何隐藏 Web 渲染的内容](https://masilotti.com/hide-web-rendered-content-on-turbo-native-apps/ "增强 Turbo Native 应用程序：如何隐藏 Web 渲染的内容") -- 作者：Joe Masilotti

[@东坡肘子](https://www.fatbobman.com/): 该文讨论了如何在 Turbo Native 应用中隐藏 Web 渲染内容，以增强其原生体验。建议隐藏基于 Web 的标题，并依赖本地导航栏来显示页面标题。使用自定义用户代理标识本地应用，并使用 Rails 助手来识别 Turbo Native 应用。提供了使用 CSS 的缓存友好解决方案，并建议将设计和逻辑集中在应用程序的标题栏周围。文章结尾还介绍了其他可以优化 Turbo Native 应用原生感的小技巧。



## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

### AIGC 尝试

1、开了一个小红书的账号，发布 AI 生成的图片，图片主题是原神相关人物。目前为止发了有 13 期，粉丝也才涨了 60+，效果不算好。这个东西要做起来，也是体力活，AI 生成的图片不稳定，需要不断调整关键词，还得是手动筛选。

我对比了几个粉丝量比较大的号，他们做的比较早，已经有了固定的画风，图片调教的也非常精细，我试了很多办法都没有能做出类似的效果。下面左侧是我的账号，右侧是某一个大佬账号，能感觉出差距。再考虑运营问题，想要做起来绝非易事。

做的过程中，对大多数二次元模型都尝试了一遍，也踩了不少坑，如果对这方面有兴趣，也欢迎交流，小红书账号是：zhangferry。

![](https://cdn.zhangferry.com/Images/202305102306989.png)	

2、开发了一个浏览器插件：[SummarAI](https://github.com/zhangferry/SummarAI "SummarAI")，利用 AI 快速阅读，并输出文章摘要。这个需求也是我的日常痛点之一，经常看到一些别人推荐的好的文章，想好好阅读一下，但是信息多，时间少；不读吧，又感觉可惜。要是能有一个人帮我把整篇内容汇总一下，并告诉我里面讲了什么，我再根据这个信息决定再细读，还是就算完了该有多好。特别是整理周报，也需要浏览很多信息，这个想法我很早就有了，只不过一直拖到五一，才算是给实践下来。

看下效果，让它帮我总结 [Meta open-sources multisensory AI model that combines six types of data](https://www.theverge.com/2023/5/9/23716558/meta-imagebind-open-source-multisensory-modal-ai-model-research "Meta open-sources multisensory AI model that combines six types of data")这篇文章：

![](https://cdn.zhangferry.com/Images/202305102326596.png)

当然这个工具还比较初级，还有很多问题需要解决：

* 标准功能的完善，像是 AI 模型的切换、预制 prompt 的配置等

* GPT 3.5 英翻中还是会偶尔出现一些语病问题，需要再增加一个修饰步骤

* 对于较长文本，受限于模型能力，无法一次读取。当前用的 gpt-3.5-turbo，最大仅支持 4096 个token
* 无法二次交互。第一轮对话已经拿到了文本信息，如果对总结内容不满意，或者像再让 AI 补充信息，还无法做到

### AI 见闻

1、[GPT产品需求设想&解决方案/工具](https://bytedance.feishu.cn/sheets/TcHTsRSczhda3BtpLQ4cMeVNnSf "GPT产品需求设想&解决方案/工具")：AIGC 相关领域的新产品、新想法每天都会出现很多，让人应接不暇。除了有希望寻找对应的 AI 工具来帮助解决问题的人，也会有希望找到痛点，来做出 AI 产品以解决对应问题的人。博主向阳乔木整理了一份飞书文档，刚好应对这两种诉求：GPT产品需求设想&解决方案/工具，文档以需求为维度记录了来管理，并对当前产品形态列了三个档位：基本解决、能用但不好用、暂无解决方案。

2、[AI 孙燕姿](https://www.bilibili.com/video/BV1io4y1w73k/?vd_source=f78da65b081aa6d30ae7bf2aded1d695 "AI 孙燕姿")：有人用 [so-vits-svc]("https://github.com/svc-develop-team/so-vits-svc" "so-vits-svc") 这个项目模拟出了孙燕姿嗓音唱周杰伦的歌的效果，后续还「孙燕姿」还翻唱了许嵩、朴树等歌手的作品。孙燕姿的声音自带一种高级感，这歌被她一唱都别有新意。不过这是否构成侵权还没有响应的法律出台，so-vits-svc也因为担心法律风险，已经被 Archive 了。

3、[Glarity](https://glarity.app/zh-CN "Glarity")：是最近一个比较火的插件，它可以为搜索引擎的结果、网页甚至 YouTube 视频生成摘要。这个插件跟我想做的效果类似，但还有一些功能并没有达到理想的状态，该插件已经开源：[chatgpt-google-summary-extension](https://github.com/sparticleinc/chatgpt-google-summary-extension "chatgpt-google-summary-extension")，也是我学习的目标之一。它对于视频摘要的处理是通过获取视频字幕，转成文字再生成的。

4、[ChatGPT Prompt Engineering for Developers](https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/1/introduction "ChatGPT Prompt Engineering for Developer")：这个吴恩达的 DeepLearning.AI 和OpenAI 联合推出的面相开发者的 ChatGPT 课程。网上有搬运的中文版视频，但缺少了官网的交互式界面。原版课程会配有 Juptyter 的交互区，可以实时的修改和调试代码，API Key 也都预制进去了，只要一步步运行代码就可以了。

![](https://cdn.zhangferry.com/Images/202305110014905.png)

## 关于我们

iOS 摸鱼周报，主要分享开发过程中遇到的经验教训、优质的博客、高质量的学习资料、实用的开发工具等。周报仓库在这里：https://github.com/zhangferry/iOSWeeklyLearning ，如果你有好的的内容推荐可以通过 issue 的方式进行提交。另外也可以申请成为我们的常驻编辑，一起维护这份周报。另可关注公众号：iOS成长之路，后台点击进群交流，联系我们，获取更多内容。

### 往期推荐

[iOS 摸鱼周报 #92 | Swift Foundation 预览版发布](https://mp.weixin.qq.com/s/AQaY2DA2h8S-XEYoQ0u7Ew)

[iOS 摸鱼周报 #91 | 免费的网站托管平台 Vercel](https://mp.weixin.qq.com/s/93YLa8ankkEVcp4pop2A6A)

[iOS 摸鱼周报 #90 | 面相任务的 GPT 项目诞生](https://mp.weixin.qq.com/s/Bx8N9HqMP5HE9mzy6l3QVA)

[iOS 摸鱼周报 #89 | WWDC 23 公布](https://mp.weixin.qq.com/s/3B_R0j8dpXpR5G9bCRsyXw)

[iOS 摸鱼周报 #88 | 把 AI 集成到研发流程](https://mp.weixin.qq.com/s/ex3aHSPjKj9woxQwHyRzZA)

![](https://cdn.zhangferry.com/Images/WechatIMG384.jpeg)
