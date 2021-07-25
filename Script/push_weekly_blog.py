import os
import sys
import argparse # 参数模块
from shutil import copyfile
# 读取文件

# 脚本执行路径
def getSourceFile(index):
    executePath = sys.path[0]
    weeklyFilePath = executePath + "/../" + "WeeklyLearning"
    sourcePath = f"{weeklyFilePath}_{index}.md"
    return sourcePath


# 复制文件到目标路径
def moveFile(source):
    target = "/Users/zhangferry/zhangferry.github.io/source/_posts"
    copyfile(source, target)
    fileName = source.split("/")[-1]
    newPath = f"{target}/{fileName}"
    return newPath

# 拼接标题头
def assemblyHeadText():
    # f
    title = "---"

# 修改文件
def modifyFile(filePath, newData):
    with open(filePath, "r+") as fileHandler:
        lines = fileHandler.readlines
        if lines[0] != "---":
            old = filePath.read()
            filePath.seek(0)
            filePath.write(newData)
            filePath.write(old)
            
# 发布


# main

parser = argparse.ArgumentParser(description='Input the weekly index')
parser.add_argument('index', type=int, help='Please input the weekly index')

args = parser.parse_args()
index = args.index

targetFile = getSourceFile(index)
print(targetFile)

