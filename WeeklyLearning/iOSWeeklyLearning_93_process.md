# iOS 摸鱼周报 #90

![](https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg)

### 本期概要

> * 本期话题：
> * 本周学习：
> * 内容推荐：
> * 摸一下鱼：

## 本期话题

### [ App Store 5 月 9 日增强全球定价机制已更新](https://developer.apple.com/cn/news/upcoming-requirements/?id=05092023a " App Store 5 月 9 日增强全球定价机制已更新")

[@远恒之义](https://github.com/eternaljust)：本周二上午，有同事反馈公司的部分 App 内购商品的价格发生了变化，App 商品显示页面价格与实际付款弹窗 App Store 价格不一致，大多相差几元。这个问题是 Apple 于 5 月 9 日升级更新了增强全球定价机制导致的，如果你在 2023 年 3 月 8 日后没有修改选择 App 的基准国家或地区，那么你的 App 和一次性 App 内购买项目的价格都将默认以美国商店美元为基础，自动调整在其他国家和地区的价格。你可通过在 App Store Connect 后台[更改 App 价格的基准国家或地区](https://developer.apple.com/cn/help/app-store-connect/manage-app-pricing/set-a-price "更改 App 价格的基准国家或地区")，此变更会自动同步到 App 所关联的 App 内购买项目，App 的价格以及同步引起的 App 内购买项目价格也会立即更新生效（修改价格的操作账号必须拥有账户持有人、管理或 App 管理的职能）。

## 本周学习

整理编辑：[Hello World](https://juejin.cn/user/2999123453164605/posts)



## 内容推荐

整理编辑：[@远恒之义](https://github.com/eternaljust)



## 摸一下鱼

整理编辑：[zhangferry](https://zhangferry.com)

### AIGC 尝试

1、开了一个小红书的账号，名字是：zhangferry。发布 AI 生成的图片，选的主题是原神。目前为止发了有 12 期，粉丝才涨了 50+，效果不算好。我看了几个粉丝量比较大的几个号，他们做的比较早，会有成系列的风格慢慢推出，图片调制的也非常精细，我试了很多办法都没有能做出类似的效果。下面左侧是我的账号，右侧是某一个大佬账号，确实有差距。这类画风和 Lora 如何结合我还没有搞明白，如果有知道或者对这个方向有兴趣的大佬欢迎一起交流。

![](https://cdn.zhangferry.com/Images/202305102306989.png)	

2、开发了一个浏览器插件：[SummarAI](https://github.com/zhangferry/SummarAI "SummarAI")，利用 AI 快速阅读，并输出文章摘要。这个需求也是我的日常痛点之一，经常看到一些别人推荐的好的文章，想好好阅读一下，但是信息多，时间少；不读吧，又感觉可惜。要是能有一个人帮我把整篇内容汇总一下，并告诉我里面讲了什么，我再根据这个信息决定再细读，还是就算完了该有多好。特别是整理周报，也需要浏览很多信息，这个想法我很早就有了，只不过一直拖到五一，才算是给实践下来。

看下效果，让它帮我总结 [Meta open-sources multisensory AI model that combines six types of data](https://www.theverge.com/2023/5/9/23716558/meta-imagebind-open-source-multisensory-modal-ai-model-research "Meta open-sources multisensory AI model that combines six types of data")这篇文章：

![](https://cdn.zhangferry.com/Images/202305102326596.png)

当然这个工具还比较初级，还有很多问题需要解决：

* 标准功能的完善，像是 AI 模型的切换、预制 prompt 的配置等

* 对于较长文本，受限于模型能力，无法一次读取。当前用的 gpt-3.5-turbo，最大仅支持 4096 个token
* 无法二次交互。第一轮对话已经拿到了文本信息，如果对总结内容不满意，或者像再让 AI 补充信息，还无法做到

### AI 见闻

1、[GPT产品需求设想&解决方案/工具](https://bytedance.feishu.cn/sheets/TcHTsRSczhda3BtpLQ4cMeVNnSf "GPT产品需求设想&解决方案/工具")：AIGC 相关领域的新产品、新想法每天都会出现很多，让人应接不暇。除了有希望寻找对应的 AI 工具来帮助解决问题的人，也会有希望找到痛点，来做出 AI 产品以解决对应问题的人。博主向阳乔木整理了一份飞书文档，刚好应对这两种诉求：GPT产品需求设想&解决方案/工具，文档以需求为维度记录了来管理，并对当前产品形态列了三个档位：基本解决、能用但不好用、暂无解决方案。

2、[AI 孙燕姿](https://www.bilibili.com/video/BV1io4y1w73k/?vd_source=f78da65b081aa6d30ae7bf2aded1d695 "AI 孙燕姿")：有人用 [so-vits-svc]("https://github.com/svc-develop-team/so-vits-svc" "so-vits-svc") 这个项目模拟出了孙燕姿嗓音唱周杰伦的歌的效果，后续还「孙燕姿」还翻唱了许嵩、朴树等歌手的作品。孙燕姿的声音自带一种高级感，这歌被她一唱都别有新意。不过这是否构成侵权还没有响应的法律出台，so-vits-svc也因为担心法律风险，已经被 Archive 了。

3、[Glarity](https://glarity.app/zh-CN "Glarity")：是最近一个比较火的插件，它可以为搜索引擎的结果、网页甚至 YouTube 视频生成摘要。目前也开源了，因为跟我做的插件功能类似，也是我学习的目标之一。视频的摘要是通过获取视频字幕，转成文字再生成的。

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
