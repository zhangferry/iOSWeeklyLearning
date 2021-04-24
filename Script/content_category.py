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

    for key in categoryMap:
        subFile = categoryFilePath + "/" + key + ".md"
        if os.path.exists(subFile):
            with open(subFile, "r+", encoding='utf-8') as file:
                file.seek(0)
                file.truncate()

    output = {"Articles":[], "Concepts":[], "Resources": [], "Tools": []}
    for subFile in os.listdir(weeklyFilePath):
        subFile = weeklyFilePath + "/" + subFile
        print(subFile)
        if "process" not in subFile and ".md" in subFile:
            with open(subFile) as file:
                for k, v in categoryMap.items():
                    begin = "## " + v
                    end = "##"
                    output_lines = []
                    isStart = False
                    isEnd = False
                    lines_content = file.readlines()
                    for line_content in lines_content:
                        # print(line_content)
                        if begin in line_content:
                            isStart = True
                            print("isStart")
                            continue
                        if end in line_content and isStart:
                            print("isEnd")
                            isEnd = True
                            continue
                        if isEnd:
                            print("====")
                            print(output[k])
                            output[k] = output_lines
                            print(output[k])
                            print("====")
                            # print(output_lines)
                            break
                        if isStart:
                            output_lines.append(line_content)
                            # print(line_content)
                            continue
                    # print(read_data)
                    # for k, v in categoryMap.items():
                        
                    #     regx = "## " + v
                    #     if regx in line_content:
                    #         # start

                    #     # by regx   
                    #     regx = '{regx}(.*?)## '.format_map(vars())
                    #     regx = 'r\'{regx}\''.format_map(vars())
                    #     print(regx)
                    #     searchObj = re.findall(regx, read_data, re.M | re.S)
                    #     if searchObj:
                    #         print(searchObj)
                    #     else:
                    #         print("No match!!")
            print(output)
            writeToFile(categoryFilePath, output)
    return output

def writeToFile(filePath, contentMap):

    for key in contentMap:
        subFile = filePath + "/" + key + ".md"
        if os.path.exists(subFile):
            with open(subFile, "a", encoding='utf-8') as file:
                for content_line in contentMap[key]:
                    file.writelines(content_line)
    print("write success!")

output_read = readWeeklyMd()
print(output_read)