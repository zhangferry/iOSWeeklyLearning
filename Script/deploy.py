# -*- coding: UTF-8 -*-
import os
import sys
import argparse
import shutil
import time
import re


def is_ci_env():
    if os.environ.get("CI"):
        return True
    else:
        return False


class BlogRepo:
    """blog仓库信息"""
    def __init__(self, git_url, branch):
        self.git_url = git_url
        self.branch = branch
        self.execute_path = os.getcwd()
        if os.path.basename(self.execute_path) == "Script":
            # 保证工作目录建立在父级目录
            self.execute_path = f"{self.execute_path}/.."
        self.repo_path = f"{self.execute_path}/.workspace"
        self.file_name = ""

    def clone_or_update_repo(self):
        # ssh 配置
        if os.path.exists(self.repo_path):
            os.chdir(f"{self.repo_path}")
            r1 = os.system("pwd")
            print(r1)
            res = os.system("git fetch")
            if res != 0:
                raise RuntimeError("execute git pull failed")
            print(res)
        else:
            os.chdir(f"{self.execute_path}")
            os.system(f"git clone {self.git_url} {self.repo_path}")
        os.chdir(f"{self.repo_path}")
        os.system(f"git reset --hard origin/{self.branch}")

    def get_blog_head_contents(self, title, file_path, tags):
        """拼接文章抬头，固定内容"""
        top_line = "---"
        the_title = f"title: {title}"
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        today = f"date: {date}"

        date_path_format = time.strftime("%Y/%m/%d", time.localtime())
        file_name_format = os.path.splitext(self.file_name)[0]
        # for real address
        blog_url = f"https://zhangferry.com/{date_path_format}/{file_name_format}"
        print(f"Blog url: {blog_url}")

        cover, tags_str = self.ready_blog_head(file_path=file_path, tags=tags)
        comments = "comments: true"
        empty_line = "\n"

        list_str = [top_line, the_title, today, cover, tags_str, comments, top_line, empty_line]
        total_title = "\n".join(list_str)
        return total_title

    def ready_blog_head(self, file_path, tags):
        if "iOSWeeklyLearning" in self.file_name:
            cover_url = "https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg"
            tags_value = ["iOS摸鱼周报"]
        else:
            with open(file_path, "r") as fileHandler:
                lines = fileHandler.read()
                # find the first img as cover
                cover_url = re.findall(r"!\[.*\]\((.*)\)", lines)[0]
            tags_value = tags.split(",")
        tags_value_str = "tags:"
        for tag_value in tags_value:
            tags_value_str += f"\n\t- {tag_value}"
        cover = f"cover: {cover_url}"
        return cover, tags_value_str

    # 修改文件
    def modify_file(self, title_str, file_path, tags):
        """修改内容"""
        self.file_name = os.path.basename(file_path)
        with open(file_path, "r+") as fileHandler:
            lines = fileHandler.readlines()

            new_content = []
            if len(title_str) == 0:
                print(f"Add new article: {self.file_name}")
                title = lines[0].strip("#").strip()
                title_content = self.get_blog_head_contents(title, file_path, tags)
                new_content.append(title_content)
            else:
                print(f"Update article: {self.file_name}")
                new_content.append(title_str)
            # 内容处理
            for index in range(0, len(lines)):
                if index > 3:
                    # 去除封面内容
                    new_content.append(lines[index])

        with open(file_path, "w") as fp:
            for newline in new_content:
                fp.writelines(newline)

    def deploy(self):
        """推送仓库"""
        os.chdir(f"{self.repo_path}")
        # print(self.repo_path)

        commit_msg = f"[Script]: update blog for {self.file_name}"
        os.system(f"git add . && git commit -m '{commit_msg}'")

        res = os.system(f"git push origin {self.branch}")
        if res != 0:
            raise RuntimeError("git push error")
        if not is_ci_env():
            # 本地触发一次deploy为了提前发布时间
            os.system("publish deploy")


class BlogArticleBuilder:
    """创建博客文章，如果以存在会自动更新"""
    def __init__(self, args=None):
        if not args:
            args = sys.argv[1:]
        parse_args = self.parse_args(args)
        self.weekly_index = parse_args.index
        self.article_name = parse_args.name
        self.tags = parse_args.tags

    def parse_args(self, args):
        parser = argparse.ArgumentParser(description='Input the article identifier')
        parser.add_argument('--index', '-i', type=int, help='Please input the weekly index')
        parser.add_argument('--name', '-n', type=str, help='Please input the Articles name')
        parser.add_argument('--tags', '-t', type=str, help='Please input article tags, separate with commas')
        return parser.parse_args(args)

    def get_weekly_article_path(self):
        """get weekly article source path"""
        # scripts path
        script_path = sys.path[0]
        weekly_folder_path = script_path + "/../" + "WeeklyLearning"
        if not self.weekly_index:
            current_index = 1
            for file in os.listdir(weekly_folder_path):
                res_number = re.findall(r"_(\d+)\.md", file)
                if res_number and int(res_number[0]) > current_index:
                    current_index = int(res_number[0])
            self.weekly_index = current_index

        return f"{weekly_folder_path}/iOSWeeklyLearning_{self.weekly_index}.md"

    def get_personal_article_path(self):
        """get personal artcile source path"""
        if not self.article_name:
            raise Exception("You must assign article name")
        script_path = sys.path[0]
        articles_folder_path = script_path + "/../" + "Articles"
        article_path = articles_folder_path + f"/{self.article_name}.md"
        if not os.path.exists(article_path):
            raise Exception("Article path is not exist")
        return article_path

    # 复制文件到目标路径
    def copy_file_to_repo(self, source_path, target_folder):
        """copy weekly file to blog repo"""
        file_name = source_path.split("/")[-1]
        target_path = f"{target_folder}/{file_name}"
        head_str = ""
        if os.path.exists(target_path):
            title_array = []
            with open(target_path, "r") as fileHandler:
                for line in fileHandler.readlines():
                    # 遇到第二个 --- 符号就结束读取
                    title_array.append(line)
                    if "---" in line and len(title_array) > 1:
                        break
            title_array.append("\n")
            head_str = "".join(title_array)

        shutil.copyfile(source_path, target_path)
        print("copy file success")
        return head_str, target_path

    def run_with(self, blog_repo):
        if self.article_name:
            article_path = self.get_personal_article_path()
        else:
            article_path = self.get_weekly_article_path()
        # print(article_path)
        blog_repo.clone_or_update_repo()
        target_folder = f"{blog_repo.repo_path}/Content/posts"
        # print(target_folder)
        head_str, target_path = self.copy_file_to_repo(source_path=article_path, target_folder=target_folder)
        blog_repo.modify_file(head_str, target_path, self.tags)
        blog_repo.deploy()


if __name__ == '__main__':

    builder = BlogArticleBuilder()

    if is_ci_env():
        # 通过环境变量传入
        blog_token = os.environ["ACCESS_TOKEN"]
        blog_git_url = f"https://{blog_token}@github.com/zhangferry/GithubPage.git"
    else:
        blog_git_url = "git@github.com:zhangferry/GithubPage.git"
    blog_branch = "master"
    blog_repo = BlogRepo(git_url=blog_git_url, branch=blog_branch)
    builder.run_with(blog_repo=blog_repo)

    print("Deploy weekly article success! It will take effect in about 10 minutes 🚀")
