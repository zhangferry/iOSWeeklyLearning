# -*- coding: UTF-8 -*-
import os
import sys
import argparse # 参数模块
import shutil
import time

blog_path = "/Users/zhangferry/zhangferry.github.io"

# 读取文件
def getSourceFile(index):
    executePath = sys.path[0]
    weeklyFilePath = executePath + "/../" + "WeeklyLearning" + "/iOSWeeklyLearning"
    sourcePath = f"{weeklyFilePath}_{index}.md"
    return sourcePath


# 复制文件到目标路径
def moveFile(source):
    fileName = source.split("/")[-1]
    target = f"{blog_path}/source/_posts/{fileName}"
    if os.path.exists(target):
        print("you had copy file before")
    else:
        shutil.copyfile(source, target)
        print("move file success")
    return target

# 拼接标题头
def assemblyHeadText(title):
    topLine = "---"
    theTitle = f"title: {title}"
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    today = f"date: {date}"

    cover = "cover: https://gitee.com/zhangferry/Images/raw/master/gitee/iOS摸鱼周报模板.png"
    tags = "tags:\n\t- iOS周报"
    comments = "comments: true"
    emptyline = "\n"

    listStr = [topLine, theTitle, today, cover, tags, comments, topLine, emptyline]
    totalTitle = "\n".join(listStr)
    return totalTitle


# 修改文件
def modifyFile(filePath):
    with open(filePath, "r+") as fileHandler:
        lines = fileHandler.readlines()
        
        newContent = []
        if "#" in lines[0]:
            print("modidfying target file")
            title = lines[0].strip("#").strip()
            titleContent = assemblyHeadText(title)
            newContent.append(titleContent)
            print(len(lines))
            # print(lines.count())
            for index in range(0, len(lines)):
                if index > 3:
                    newContent.append(lines[index])
            # old = filePath.read()
            print(newContent)
            fileHandler.seek(0)
            for newline in newContent:
                fileHandler.write(newline)
            # filePath.write(old)
            
# 运行和发布
def runAndPublic(isPublic):
    # os.system的执行每次都是开启一个subshell，导致更新执行目录退出来会复原，所以使用复合语句完成所有任务
    # 还可以使用os提供的os.chdir('/home/data')
    os.chdir(f"{blog_path}")
    if isPublic:
        os.system(f"hexo g && hexo d")
    else:
        val = os.system('ls -al')
        print(val)
        os.system(f"hexo g && hexo s")
    


parser = argparse.ArgumentParser(description='Input the weekly index')
parser.add_argument('--index', '-i', type=int, help='Please input the weekly index')
parser.add_argument('--isPublic', '-isP', type=int, help='you can asign is public, default is 0')

# main
if __name__ == '__main__':
    args = parser.parse_args()
    index = args.index
    isPublic = args.isPublic

    sourceFile = getSourceFile(index)
    print(sourceFile)
    targetPath = moveFile(sourceFile)
    print(targetPath)
    modifyFile(targetPath)
    runAndPublic(isPublic)
