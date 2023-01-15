import unittest
from deploy import BlogArticleBuilder, BlogRepo
from content_category import export_category


class MyTestCase(unittest.TestCase):

    def setUp(self):
        article_args = ["--name", "campus_to_recruitment",
                        "--tags", "面试,职场,校园"]
        self.builder = BlogArticleBuilder(article_args)

    def test_deploy_article(self):
        blog_branch = "master"
        blog_git_url = "git@github.com:zhangferry/GithubPage.git"
        blog_repo = BlogRepo(git_url=blog_git_url, branch=blog_branch)
        self.builder.run_with(blog_repo=blog_repo)

    def test_export_category(self):
        # export_weekly_category()
        export_category(from_index=43, to_index=81, merged_file="Summary-2022")


if __name__ == '__main__':
    unittest.main()
