# -*- coding: UTF-8 -*-
import os
import sys
import argparse
import shutil
import time
import re


class BlogRepo:
    """blog仓库信息"""
    def __init__(self, token, git_url, branch):
        self.token = token
        self.git_url = git_url
        self.branch = branch
        self.execute_path = os.getcwd()
        self.repo_path = f"{self.execute_path}/.workspace"
        self.file_name = ""

    def clone_or_update_repo(self):
        # ssh 配置
        os.chdir(f"{self.execute_path}")
        if os.path.exists(self.repo_path):
            os.system(f"git pull")
        else:
            os.system(f"git clone {self.git_url} {self.repo_path}")
        os.chdir(f"{self.repo_path}")
        os.system(f"git reset --hard origin/{self.branch}")

    def get_blog_head_contents(self, title):
        """拼接文章抬头，固定内容"""
        top_line = "---"
        the_title = f"title: {title}"
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        today = f"date: {date}"

        cover = "cover: https://cdn.zhangferry.com/Images/moyu_weekly_cover.jpeg"
        tags = "tags:\n\t- iOS摸鱼周报"
        comments = "comments: true"
        empty_line = "\n"

        list_str = [top_line, the_title, today, cover, tags, comments, top_line, empty_line]
        total_title = "\n".join(list_str)
        return total_title

    # 修改文件
    def modify_file(self, title_str, file_path):
        """修改内容"""
        self.file_name = os.path.basename(file_path)
        with open(file_path, "r+") as fileHandler:
            lines = fileHandler.readlines()

            new_content = []
            if len(title_str) == 0:
                print(f"Add new article: {self.file_name}")
                title = lines[0].strip("#").strip()
                title_content = self.get_blog_head_contents(title)
                new_content.append(title_content)
            else:
                print(f"Update article: {self.file_name}")
                new_content.append(title_str)
            # 内容处理
            for index in range(0, len(lines)):
                if index > 3:
                    # 去除封面内容
                    new_content.append(lines[index])
            fileHandler.seek(0)
            for newline in new_content:
                fileHandler.write(newline)

    def push(self):
        """推送仓库"""
        os.chdir(f"{self.repo_path}")
        # print(self.repo_path)

        commit_msg = f"[Script]: update blog for {self.file_name}"
        os.system(f"git add . && git commit -m '{commit_msg}'")
        os.system(f"git push origin {self.branch}")


class BlogArticleBuilder:
    """创建博客文章，如果以存在会自动更新"""
    def __init__(self):
        parser = argparse.ArgumentParser(description='Input the weekly index')
        parser.add_argument('--index', '-i', type=int, help='Please input the weekly index')
        parse_args = parser.parse_args()
        self.weekly_index = parse_args.index

    def get_weekly_article_path(self):
        """get article source path"""
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
        article_path = self.get_weekly_article_path()
        print(article_path)
        # blog_repo.clone_or_update_repo()
        target_folder = f"{blog_repo.repo_path}/Content/posts"
        print(target_folder)
        head_str, target_path = self.copy_file_to_repo(source_path=article_path, target_folder=target_folder)
        blog_repo.modify_file(head_str, target_path)
        blog_repo.push()


if __name__ == '__main__':

    builder = BlogArticleBuilder()

    # 也可以通过环境变量传入
    blog_token = ""
    blog_git_url = "git@github.com:zhangferry/GithubPage.git"
    blog_branch = "master"
    blog_repo = BlogRepo(token=blog_token, git_url=blog_git_url, branch=blog_branch)
    builder.run_with(blog_repo=blog_repo)

    print("push weekly article success! 🚀")
