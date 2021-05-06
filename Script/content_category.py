# -*- coding: UTF-8 -*-
import os
import sys
import re

categoryMap = {"Articles": "优秀博客", "Concepts": "编程概念", "Resources":"学习资料", "Tools": "开发利器"}

weeklyFile = "WeeklyLearning"
categoryFile = "categorySummary"

def readWeeklyMd():
    # 脚本执行路径
    executePath = sys.path[0]
    weeklyFilePath = executePath + "/../" + weeklyFile
    categoryFilePath = executePath + "/../" + categoryFile
    print(weeklyFilePath)

    # 开始之前会擦除之前数据
    for key in categoryMap:
        subFile = categoryFilePath + "/" + key + ".md"
        if os.path.exists(subFile):
            with open(subFile, "r+", encoding='utf-8') as file:
                file.seek(0)
                file.truncate()

    output = {"Articles":[], "Concepts":[], "Resources": [], "Tools": []}
    # 为了保证读取的顺序
    count = len(os.listdir(weeklyFilePath)) - 1
    for index in range(count):

        subFile = "{}/iOSWeeklyLearning_{}.md".format(weeklyFilePath, index + 1)
        print(subFile)
        if os.path.exists(subFile):
            with open(subFile) as file:
                lines_content = file.readlines()
                for k, v in categoryMap.items():
                    output[k] = filterData(lines_content, v)
            # print(output)
            writeToFile(categoryFilePath, output)
    return output

def filterData(lines_data, category_name):
    begin = "## " + category_name
    print(category_name)
    output_lines = []
    isStart = False
    isEnd = False
    for line_content in lines_data:
        # print(line_content)
        if begin in line_content:
            isStart = True
        elif line_content.count("#") == 2 and isStart:
            isEnd = True
        elif isEnd:
            # print("====")
            print(output_lines)
            return output_lines
        elif isStart:
            output_lines.append(line_content)
            # print(line_content)
    return output_lines

def writeToFile(filePath, contentMap):

    for key in contentMap:
        subFile = filePath + "/" + key + ".md"
        if os.path.exists(subFile):
            with open(subFile, "a", encoding='utf-8') as file:
                file.write("***")
                for content_line in contentMap[key]:
                    file.writelines(content_line)
    print("write success!")

output_read = readWeeklyMd()
# print(output_read)