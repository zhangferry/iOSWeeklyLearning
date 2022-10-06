## 脚本说明

主要使用的脚本有两个，一个是是用于发布的 `deploy.py`，一个是用于归类的`content_category.py`。

## 发布

发布周报：

```bash
# --index 用于指定发布哪一期内容，如果不填会发布去除process标记的最大一期内容
$ python3 Script/deploy.py --index 60
```

为了简化执行流程，增加了一个shell的调用方式。

```bash
$ Script/ci_run.sh 60
```

同样，表示期数的 60 可以省略。

deploy.py 还有一个额外功能用于发布非周报类文章，可以执行下面的命令：

```bash
# --name 表示文件名，--tags 表示tag值，多个内容可以用逗号分割
$ python3 Script/deploy.py --name <file_name> --tags <tag1,tag2> 
```

## 周报内容聚类

`content_category.py` 主要用于识别周报里的内容并将其归类到`CategorySummary`文件夹中。

```bash
$ python3 Script/content_category.py
```

