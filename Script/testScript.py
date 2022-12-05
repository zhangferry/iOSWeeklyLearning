import unittest
from deploy import BlogArticleBuilder, BlogRepo


class MyTestCase(unittest.TestCase):

    def setUp(self):
        article_args = ["--name", "cultivation_for_programmer_booknotes_2",
                        "--tags", "书评,读书笔记"]
        self.builder = BlogArticleBuilder(article_args)

    def test_deploy_article(self):
        blog_branch = "master"
        blog_git_url = "git@github.com:zhangferry/GithubPage.git"
        blog_repo = BlogRepo(git_url=blog_git_url, branch=blog_branch)
        self.builder.run_with(blog_repo=blog_repo)

    def test_deploy_weekly(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
