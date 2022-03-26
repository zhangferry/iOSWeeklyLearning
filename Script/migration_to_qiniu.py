# migration gitee to qiniu
import os
import re
from ast import Str

from qiniu import Auth
import qiniu

repo_path = "/Users/zhangferry/Desktop/iOSWeeklyLearning"
images_path = "/Users/zhangferry/Downloads/Images-master"


def parse_urls(dir):
    # traversal_dir = ["Articles", "Resources", "WeeklyLearning", "CategorySummary", "Interview"]
    traversal_dir = ["WeeklyLearning"]
    for subdir in os.listdir(dir):
        if subdir in traversal_dir:
            # local_path = Path(local_path)
            sub_root = repo_path + "/" + subdir
            for idx, file in enumerate(os.listdir(sub_root)):
                if ".md" not in file:
                    continue
                # if idx == 1:
                #     break
                file = sub_root + "/" + file
                print(file)
                with open(file, 'r') as fp:
                    content = fp.read()
                    regular_expre(content, file)


def regular_expre(content: Str, path: Str):
    # result is wrapped by brackets
    link_res = r"https://gitee.com/zhangferry/Images/raw/master/"
    rex = r"!\[.*\]\(({}.*)\)".format(link_res)
    print(rex)
    pattern = re.compile(rex)
    res_list = pattern.findall(content)
    for res in res_list:
        # pure link
        print(res)
        file_name = f"{res}".split("/")[-1]
        new_link = f"http://r9ccmp2wy.hb-bkt.clouddn.com/Images/{file_name}"
        # print(new_link)
        # upload_file(path)
        content = content.replace(res, new_link)
        
    # print(content)
    # replace = re.sub(rex, content,  content)
    # write back
    with open(path, "w") as fp:
        fp.write(content)


def upload_file(file_path):
    host = "https://upload-z1.qiniup.com"

    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'HF6aHnsNHPJRePvl2PTE7Z_jWT_9kts2t4vgyB-u'
    secret_key = 'Db-SRqLu9T0-1W3I8LfyM__aCGyvsuGBHbxn2v_A'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'moyuweekly'
    # 上传后保存的文件名
    key = f"Images/{os.path.basename(file_path)}"
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    ret, info = qiniu.put_file(token, key, file_path, version='v2')
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == qiniu.etag(file_path)
    print(f"upload {key} success")


def upload_images_repo(path):
    traversal_dir = ["blog", "gitee", "iOSWeeklyLearning"]
    for subdir in os.listdir(path):
        if subdir in traversal_dir:
            # local_path = Path(local_path)
            sub_root = path + "/" + subdir
            for image_name in os.listdir(sub_root):
                image_path = sub_root + "/" + image_name
                print(image_path)
                upload_file(image_path)


parse_urls(repo_path)
# upload_file(file)
# upload_images_repo(images_path)