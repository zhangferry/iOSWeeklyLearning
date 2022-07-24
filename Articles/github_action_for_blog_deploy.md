# 利用 Github Action 实现博客自动发版

![](https://cdn.zhangferry.com/Images/carl-heyerdahl-KE0nC8-58MQ-unsplash.jpg)

 ## 背景

先说下背景需求，在摸鱼周报的整理流程中，最后一步需要生成公众号的原文链接，原文链接指向的是个人博客地址。博客需要发布才能产生外部链接，发布到不费事，但是操作步骤重复，且因为涉及博客推送相关的配置都在我的个人电脑里，所有步骤必须由我来完成。来回多次之后就考虑将这个流程做成自动化了，目标是让周报协作者都可以实现博客推送，用到的实现方式是 Github Action。

## 实现思路

在开始之前先了解下原先的发布流程，如下图表示：

![](https://cdn.zhangferry.com/Images/20220719235714.png)

整个过程涉及 3 个仓库：

* Moyu Repo。管理周报文章的公共仓库，协作者可以通过它拉取和推送内容。

* Blog Repo。管理博客内容的私有仓库，周报只是其中一部分。

* Blog Website。博客的网站，它部署在一台腾讯云服务器上，它也是私有的。

因为涉及两个私有仓库，普通协作者都没有他们的访问权限，所以发布流程都依赖我来完成。解决方案就是消除发布流程对权限的依赖，理想流程是这样的：

![](https://cdn.zhangferry.com/Images/20220719235757.png)

这样触发入口就都集中在了共有仓库，协作者也可以参与博客发布。要实现这个流程需要将需求分为两步：

1、Moyu Repo 通过 Github Action 推送 Moyu 内容到 Blog Repo。

2、Blog Repo 通过 Github Action 发布内容到网站。

这其中最关键的是访问私有仓库时如何处理权限的问题。

## Github Action

这里先简单了解下 Github Action。它是 Github 提供的为仓库定义自动化流程的方案，类似 Jenkins、GitLab CI/CD。Github Action 有一套自己的流水线配置方式，所有的流程都可以通过一个 yml 文件下发。Gtihub Action 有自己的虚拟机，支持 Windows Server/Linux/Mac，使用者无需关心环境配置问题，可以直接使用。

配置入口如下图所示：

![](https://cdn.zhangferry.com/Images/20220724120626.png)

点击`set up a workflow yourself`，即创建了一个用于编排自动化任务的 workflow，它对应一个 yml 文件，所有的配置流程都在这里进行。

自动化任务配置前我们需要先考虑这几个问题：什么时机触发？在什么设备运行？如何执行自动化任务？我们看一个简单的例子来学习下 Github Action 如何定义这些行为：

```yml
name: GitHub Actions Demo
on: [push]
jobs:
  Explore-GitHub-Actions:
    runs-on: ubuntu-latest
    steps:
      - run: echo "🎉 The job was automatically triggered by a ${{ github.event_name }} event."
      - name: Check out repository code
        uses: actions/checkout@v3
```

name 表示当前流水线的名字。

### 什么时机触发

在什么场景触发，对应的key 是 `on`。上面Demo里的`[push]`，表示仓库发生push行为时触发任务。on 还有其他几种触发途径：

* pull_request：提交 PR 时触发
* schedule：定时触发，可以按 cron 语法配置定频
* workflow_dispatch：手动触发，有用户手动激活触发行为

### 在什么设备运行

对应的关键词是`runs-on`，Demo里指定值为`ubuntu-latest`，表示执行设备是一个 ubuntu 设备。Github Action 还支持 macOS 环境，目前有三个 macOS 版本可以支持：

| 虚拟环境             | YAML标签                   |
| -------------------- | -------------------------- |
| macOS Monterey 12    | macos-12                   |
| macOS Big Sur 11     | macos-latest` 或 `macos-11 |
| macOS Catalina 10.15 | macos-10.15                |

需要注意：macos-latest 不是最新的 macos 版本，而是 macOS 11。iOS 开发中我们可能还会关心 Xcode 版本，Ruby 版本等。以 macOS 12 虚拟机为例，Xcode 版本：

| Version          | Build    | Path                           |
| ---------------- | -------- | ------------------------------ |
| 13.4.1 (default) | 13F100   | /Applications/Xcode_13.4.1.app |
| 13.4             | 13F17a   | /Applications/Xcode_13.4.app   |
| 13.3.1           | 13E500a  | /Applications/Xcode_13.3.1.app |
| 13.2.1           | 13C100   | /Applications/Xcode_13.2.1.app |
| 13.1             | 13A1030d | /Applications/Xcode_13.1.app   |

Ruby版本：2.7.6/3.0.4/3.1.2。

其他预制环境可以参考这篇文档：[macos-12-Readme](https://github.com/actions/virtual-environments/blob/main/images/macos/macos-12-Readme.md "macos-12-Readme")。

另外 Github Action 还支持将自己的设备定义为运行机，你可以在这里了解：[About self-hosted runners](https://docs.github.com/cn/enterprise-server@3.1/actions/hosting-your-own-runners/about-self-hosted-runners "About self-hosted runners")；支持联机调试，可以通过这个插件了解：[A debugger for actions](https://github.com/marketplace/actions/a-debugger-for-actions "A debugger for actions")。

### 如何执行自动化任务

有两种执行任务的方式，一种是直接在 yml 文件里编辑脚本，关键词是`run`。像是 Demo 里的 echo 命令，我们可以直接输入 shell 命令进行执行。

另一种方式是插件市场，像下面这种形式：

```yml
- name: Check out repository code
		uses: actions/checkout@v3
```

就是使用了 `actions/checkout@v3` 这个插件。Github 有一个插件市场，可以搜索所需插件。像是 Code review，SSH 登录等都有封装好的插件可以直接使用。

![](https://cdn.zhangferry.com/Images/20220723192554.png)

## 实现方案

有了这些 Github Action 知识，我们就可以开始实现我们的需求了。最终效果分成两个需求。

### Moyu Repo 向 Blog Repo 推送内容

我们按照前面的三个问题来设计这个功能。

#### 什么时机触发？

发布之前需要经过多次修改，会有多个 PR 和 Push 行为，而 Blog 发布需要等所有内容都准备完成才会执行，一般只有一次。所以考虑使用手动发布的方式，以下是配置内容：

```yml
# Action name
name: Weekly Article Deploy
# Controls when the workflow will run
on:
  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:
    inputs:
      weekly_index:
        description: 'weekly index for deploy'  
```

手动发布还补充了一个 `inputs`，用于接收输出参数，`weekly_index`为参数名，用于表示要发布第几期。执行效果如下所示：

![](https://cdn.zhangferry.com/Images/20220723194746.png)

#### 在什么设备运行？

这个需要根据执行任务来定，这里只涉及一些文本转换和仓库操作，所以任意机器都满足需求，ubuntu 资源比较多，调度会快那么一点点，所以都可的情况优先选 ubuntu。

```yml
# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest
```

Github Action 里有几个名词：workflow，job，steps，这里简单捋一下。整个 Yml 文件对应为一个 workflow，它表示一次完整的自动化任务运行过程。当前仓库的整个配置都是一个 workflow。

一个 workflow 可以包含一个或多个 job，这里的 `jobs` 下面一级内容就是各个 job。不同 job 之间可以串行也可以并行。`build`为会其中一个 job，也是本 workflow 唯一的 job。

#### 如何执行自动化任务？

这个流程需要做的事情是把 Moyu Repo 内容转成 Blog Repo 的格式，然后推送到 Blog Repo 里。前一步可以封装成一个脚本，后一步往私有仓库推送需要生成一个具有推送私有仓库权限的 token。

token 的生成需要到这里：个人头像 -> Settings -> Developer settings -> Personal access tokens，点击 Generate new token。这一步需要输入密码，然后我们可以选择所需权限去生成一个token。对于私有仓库的推送，我们选中这一个权限就可以了：

![](https://cdn.zhangferry.com/Images/20220723200801.png)

为了安全考虑，这个token生成之后只会可见一次，因为后面的步骤会使用，所以我们需要做好保存。

注意这个 token 是用户级别的，它可以用于访问修改该账户名下的任意仓库。

为了让 Github Action 可以访问到这个token，需要给它做一个配置。配置路径是：在该仓库下的 Settings（注意这个是仓库下的设置而非个人下的设置） -> Secrets -> Actions 点击 New repository secret。

![](https://cdn.zhangferry.com/Images/20220724012424.png)

Name 的话可以命名为 `ACCESS_TOKEN`，Value 为上一步生成的访问 token。这里配置的任意内容都可以通过Github Action 访问到，且是加密的，创建之后只能看到 Name 看不到 Value。

![](https://cdn.zhangferry.com/Images/20220724012350.png)

下面是具体配置：

```yaml
env:
  ACCESS_TOKEN: ${{ secrets.ACCESS_TOKEN }}

# Steps represent a sequence of tasks that will be executed as part of the job
steps:
  - name: print inputs
    run: |
      echo "Weekly Index: ${{ github.event.inputs.weekly_index }}"

  - name: Git Config
    run: |
      git config --global user.email moyuweekly@github.com
      git config --global user.name moyuweekly
  # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
  - uses: actions/checkout@v3

  # Runs a single command using the runners shell
  - name: Run a one-line script
    run: ./Script/ci_run.sh ${{ github.event.inputs.weekly_index }}
    shell: bash
```

`secrets.ACCESS_TOKEN` 表示的是该仓库下面 secrets 里 name 为 `ACCESS_TOKEN` 的内容。`${{}}`为 action 语法获取变量的写法。

因为我把对私有仓库的获取和推送都放到了执行脚本里，所以这里通过环境变量的形式把这个值传给脚本。

steps 用于表述运行步骤，这里是顺序执行的。上述流程涉及到4个执行步骤：

1、打印外部传参。`${{github.event.inputs.weekly_index}}` 表示输入的参数。

2、配置 git user 的 email 和 name。因为执行内容涉及提交操作，这里是为了标记自动化流程的提交。

3、uses 语法对应的是插件功能，这里输入插件名即可执行对应插件配置的功能。 `actions/checkout@v3` 是官方插件，用于拉取本仓库代码的。

4、执行脚本。我把私有仓库的拉取，内容的格式化，私有仓库推送都放到了这个脚本里。

私有仓库的管理需要考虑 Git 链接的形式，Git 链接有两种方式，一种是给 SSH 形式，这对于本地机器比较容易，对于不固定的打包机配置起来较为麻烦。第二种是 HTTPS 形式，HTTPS 是公有链接无法处理权限问题，但 Github 支持把 token 传入链接的形式来管理权限。这里选择使用HTTPS形式，配置的 Git 地址如下：

```
https://{github_token}@github.com/username/repo.git
```

对仓库的操作使用这个链接就可以解决权限问题了，执行结果如下：

![](https://cdn.zhangferry.com/Images/20220723203939.png)

左边是 job 描述，右边是 steps 描述，每个 steps 都可以展开查看详情。因为这里的步骤只有代码拉取推送和格式处理，所以执行很快。

### Blog Repo 发布网站

这个阶段对应的是 Blog Repo 推送内容到腾讯云服务器。还是按上面的流程设计实现方式：

#### 如何触发任务？

这个历程是上一步的承接，前一步已经定好了推送频率，这里可以接收到 push 即触发任务。

```yml
push:
    branches: [ "master" ]
```

#### 在什么机器触发？

这需要考虑到所使用的博客框架，如果是 Hexo/Jekyll 使用 Ubutu 就可以了。因为我将博客框架迁移到了 [Publish](https://github.com/JohnSundell/Publish "Publish")，Publish 是一个由 Swift 编写的静态博客框架，所以运行机器只能是 macOS。测试时发现 Publish 引用了`libswift_Concurrency.dylib` 这个库，所以还需要指定版本为 macos-12。

```yml
jobs:
  build:
    # macOS Monterey 12
    runs-on: macos-12
```

#### 如何执行自动化任务？

执行流程大概是这样的：编译 publish -> 使用 publish 把 md 源文件转成静态网站格式 -> 发布到腾讯云。

正常能获取到 publish 执行文件是无需编译的，但因为我为了让它兼容 hexo 的格式，做了一些魔改，所以我使用的 publish 是一个动态的版本，它需要随修改随时编译。

发布至腾讯云，也需要考虑权限问题，个人服务器没有 Github 那种 token 授权形式，只能借助于 SSH 了。

**SSH**

在开始之前再简单回顾下 SSH 登录的一点原理。SSH 支持密码和密钥两种登录方式，我们一般为省去繁琐的密码输入，会采用密钥登录的形式。密钥登录使用的是对称加密，一般的做法是登录端生成一对公私钥，把公钥放到服务端，私钥保存在本地。对称加密解决的是信息传输不会被篡改的问题，它无法防止中间人攻击，因为它没有HTTPS 那样的 CA 来验证可信性。SSH 选择的是通过手动验证的方式，关于手动验证不知你是否还还记得这段内容：

```
The authenticity of host 'host (172.168.*.*)' can't be established.
RSA key fingerprint is 98:2e:d7:e0:de:9f:ac:67:28:c2:42:2d:37:16:58:4d.
Are you sure you want to continue connecting (yes/no)?
```

它就是用来手动验证的，我们需要通过 host ip 验证该链接是来自于可信的服务器还是中间人。确定过一次之后，这个信息会被写到本地的 `known_hosts` 文件中，之后对于同一 ip 的服务器登录就不会再弹这个验证了。对于自动化流程来说，我们应该将私有服务器的验证信息直接填入`known_hosts`文件，跳过阻塞式的二次确认。

**流程配置**

有了以上知识，我们对于密钥的配置流程应该是如下图所示：

![](https://cdn.zhangferry.com/Images/20220723233812.png)

蓝色的钥匙为 pub_key，红色钥匙为 private_key，带钥匙的文件是 `know_hosts`。Github Action Runner 的配置流程如果都手动实现比较麻烦，我们可以使用[install-ssh-key](https://github.com/marketplace/actions/install-ssh-key "install-ssh-key")这个插件快速实现这个功能：

```yml
- name: Install SSH Key
      uses: shimataro/ssh-key-action@v2.3.1
      with:
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        # it's value doesn't matter
        known_hosts: 'knowen_host_value for ssh-rsa'
```

它要求两个参数，key 为 ssh 的 private key。SSH 私钥可以使用上个章节介绍的 Secrets Actions 进行存储，将其命名为 `SSH_PRIVATE_KEY`。

`known_hosts` 是对 Server 端的信任记录，用于免去手动确认的流程。这个内容的获取，有两种方式，你可以查看本地的 `known_hosts` 文件找到对应的目标服务器的记录，也可以利用 `ssh-keyscan` 去手动查找。

```bash
$ ssh-keyscan -H <host-ip>
```

这个结果会按多种加密算法产生多个结果，我们需要选择类型为 ssh-rsa 的内容，[因为Github Action 仅支持这一种加密结果](https://zellwk.com/blog/github-actions-deploy/ "Deploying to a server via SSH and Rsync in a Github Action")。

![](https://cdn.zhangferry.com/Images/20220724001820.png)

我们把这一条内容添加 `known_hosts` 参数即可。当然你也可以选择使用密钥的形式存放。

最重要的步骤已经完成了，下面就可以编译 publish 并发布内容了。

```yml
- name: Create Publish
  run: |
    git clone https://github.com/zhangferry/Publish.git ./publish
    cd publish
    make
    cd ..
- name: Blog Deploy
  run: |
    echo "begin deploy"
    ./publish/.build/release/publish-cli deploy
```

最后执行结果：

![](https://cdn.zhangferry.com/Images/20220723210525.png)

#### 遗留问题

往腾讯云服务器推送内容时遇到一个腾讯云给我发了告警邮件，说是检测到异地登录，来源IP是美国，危险等级高危。这个登录应该指的是 Github Action Runner 设备的登录，这个目前还没有找到有效的解决办法，因为IP是动态的，无法通过手动加白的形式避免。

另外也可关闭异地登录的报警，在[告警设置](https://console.cloud.tencent.com/cwp/setting)里关闭异地登录报警选项即可。但这种方式也存在一定的安全风险，因为它不是解决问题而是无视问题。

我暂时没有找到更好的解决方案，如果有人知道更好的处理方式，欢迎告知。