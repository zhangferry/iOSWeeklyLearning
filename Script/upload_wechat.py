# -*- coding: utf-8 -*-
from werobot import WeRoBot
import os
import json
import requests
from selenium import webdriver


class WebDriver:
    def __init__(self, driver_path):
        self.brower = webdriver.Chrome(executable_path=driver_path)
        website = self.brower.get("https://whaoa.github.io/markdown-nice/")
        page_source = self.brower.page_source
        title = self.brower.title
        # print(website)
        print(page_source)
        print(title)


class WeRoBotClint:

    def __init__(self):
        robot = WeRoBot()
        robot.config["APP_ID"] = os.getenv("wx2dfe81f38281cfd9")
        robot.config["APP_SECRET"] = os.getenv("ef5e460dd2941f640aa6eaf69b97d1c4")
        self.we_client = robot.client
        self.we_token = self.we_client.grant_token()

    def upload_media(self, media_file):
        res_json = self.we_client.upload_permanent_media("image", open(media_file, "rb"))
        media_id = res_json["media_id"]
        url = res_json["url"]
        return media_id

    # 因werobot暂未支持，所以直接采用接口访问
    def upload_article(self, content):
        articles = {
            "articles": [
                {
                    "thumb_media_id": "JqgEfa5SNzBYVoHTccyIRsGDDhotpIMnUnwCL2L6pp_JfvIA3qdDBc9kYJmlzGi4",
                    "author": "zhangferry",
                    "title": "Happy Day",
                    "content_source_url": "https://zhangferry.com/2022/07/24/github_action_for_blog_deploy/",
                    "content": content,
                    # 图文信息描述
                    "digest": "描述信息",
                    "need_open_comment": 1
                }
            ]
        }

        client = NetworkClint()
        token = client.get_access_token()
        headers = {'Content-type': 'text/plain; charset=utf-8'}
        datas = json.dumps(articles, ensure_ascii=False).encode('utf-8')
        postUrl = "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=%s" % token

        r = requests.post(postUrl, data=datas, headers=headers)
        resp = json.loads(r.text)
        print(resp)


class NetworkClint:
    def __init__(self):
        self.__accessToken = ""
        self.__leftTime = 0

    def __real_get_access_token(self):
        post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
                   "client_credential&appid=%s&secret=%s" % (
                   os.getenv('WECHAT_APP_ID'), os.getenv('WECHAT_APP_SECRET')))
        print(post_url)
        response = requests.request(method="post", url=post_url)
        response_json = json.loads(response.text)

        self.__accessToken = response_json["access_token"]
        self.__leftTime = response_json["expires_in"]

    def get_access_token(self):
        if self.__leftTime < 10:
            self.__real_get_access_token()
        return self.__accessToken


if __name__ == '__main__':
    local_path = "/Users/zhangferry/Desktop/wechat_content"
    local_img_path = "/Users/zhangferry/Desktop/WechatIMG9.jpeg"
    driver_path = "/Users/zhangferry/Developer/chromedriver"

    driver = WebDriver(driver_path)

    # os.environ['WECHAT_APP_ID'] = ""
    # os.environ['WECHAT_APP_SECRET'] = ""
    # with open(local_path, "r") as fp:
    #     file_content = fp.read()
    #     print(file_content)
    #
    #     clinet = WeRoBotClint()
    #     # res = clinet.upload_media(local_img_path)
    #     # print(res)
    #     clinet.upload_article(file_content)


temp_token = "59_FzaJlr22Qak-Sd4XNnXGjUprHTp7xaDQV_RDv8BRpal_-TyEPyaYUlWNpLHAvJxYpZoPqtpMb-1nMzV6ZuJDVFi8QwMYJz88SKE86U-SNX_wDPiOpwaZ6D8O9UXOuR0aEjYh3rIBk4NDe8LVNFIaAGADVY"
