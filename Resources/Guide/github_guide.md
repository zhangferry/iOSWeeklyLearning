# 在摸鱼周报里使用 Github

摸鱼周报的资源文件和协作流程都在Github上，所以我们有必要对它有一个大概的了解，特别是协作过程会用到的那些步骤。本篇文档主要是对这些关键步骤进行说明。

## 贡献内容

摸鱼周报贡献内容的方式有两种：Issue、Pull Request。

Issue 适用于读者，PR 适用于联合编辑，我们来讲下 PR 的协作方式，大致流程可以看下下面这张图。

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210626113835.png)

1-4 用于首次提交的场景，5-7用于后续的提交场景。

这里第5步有两种方式完成：

**Moyu Remote -> My Remote -> Local**

这里的同步分为两步进行，Moyu Remot -> My Remote 这一步需要利用 Github 针对Fork仓库增加的 Fetch upstream 功能：

![](https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/20210626112400.png)

点击 Fetch and merge 即可完成Moyu远程仓库到自己远程仓库的同步。之后我们还需通过本地的 Git 进行同步：

```bash
$ git fetch origin
# 同步远程仓库代码，这一步有很多指令，rebase和merge均可
$ git rebase main
```

**Moyu Remote -> Local**

这种方式是一步完成同步，为了让本地仓库可以直接 Fetch Moyu Repo，需要额外添加一个远程库关联：

```bash
# 添加仓库关联，moyu为仓库名，也可以自定义为别的名字，通常它还叫upstream。这时本地应该有origin，moyu两个远程仓库
$ git remote add moyu git@github.com:zhangferry/iOSWeeklyLearning.git
# 拉取moyu仓库代码，如果有输出内容，说明需要同步
$ git fetch moyu
# 指定moyu仓库分支
$ git rebase moyu/main
```

## Pull Request

目前仓库只有 main 分支，所以 PR 指向 `zhangferry:main` 即可。**需要保证每次提交 PR 之前，已经完成了远程仓库的同步**。

### PR 修改

PR的作用主要是审核，如果已经提交了 PR，自己发现或者被审核员评论格式出错，文案出错的情况，仅需再次修改然后 push 即可。PR 是一个动态的过程，它代表的 My Remote 与 Moyu Remote 之间的差异，两者任意内容发生变化，对应的 PR 内容就会自动更新。

### PR 关闭

当 PR 被打回时才需要关闭。

## 其他 Github 功能

### Project

访问地址是这个：https://github.com/zhangferry/iOSWeeklyLearning/projects/1。其主要用于摸鱼周报的发版事项同步。

### README

README 用于介绍周报的大致情况和协作者。协作者的管理使用了 [all-contributors ](https://github.com/all-contributors/all-contributors)这个工具，为了便于添加和更新协作者的身份信息，引入了 `@all-contributors Bot🤖`，可以在 PR 的 Conversation 对话框里输入指令唤起机器人进行操作，命令如下：

```
@all-contributors please add @<username> for <contributions>
```

不同职责对应有不同 emoji 表情，含义对照可以查看[这里](https://allcontributors.org/docs/en/emoji-key)。