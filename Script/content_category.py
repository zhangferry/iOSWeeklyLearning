# -*- coding: UTF-8 -*-
import os
import sys
from deploy import get_latest_weekly_index

category_map = {
    "Topic": ["本期话题"],
    "Articles": ["优秀博客", "内容推荐"],
    "Interviews": ["面试解析"],
    "Learnings": ["本周学习", "开发Tips"],
    "Concepts": ["编程概念"],
    "Resources": ["工具推荐", "摸一下鱼", "学习资料"]
}

weeklyFile = "WeeklyLearning"
categoryFile = "CategorySummary"


def export_category(from_index=1, to_index=1, merged_file=None):
    execute_path = sys.path[0]
    weekly_folder = execute_path + "/../" + weeklyFile
    category_folder = execute_path + "/../" + categoryFile

    if not merged_file:
        category_files = [f"{category_folder}/{category}.md" for category in category_map]
    else:
        category_files = [f"{category_folder}/{merged_file}.md"]

    for category_file in category_files:
        if os.path.exists(category_file):
            with open(category_file, "r+", encoding='utf-8') as file:
                file.seek(0)
                file.truncate()

    if merged_file:
        export_yearly_category(category_folder, weekly_folder, from_index, to_index, merged_file)
    else:
        export_weekly_category(category_folder, weekly_folder)


def export_weekly_category(category_folder, weekly_folder):
    """导出周报文档"""
    # 为了保证读取的顺序
    latest_index = get_latest_weekly_index(weekly_folder) - 1
    for index in range(latest_index):
        weekly_file = f"{weekly_folder}/iOSWeeklyLearning_{index + 1}.md"
        print(weekly_file)
        export_content = export_topic_content(weekly_file)
        write_to_file(category_folder, export_content)


def export_yearly_category(category_folder, weekly_folder, from_index=1, to_index=1, merged_file=None):
    """导出年度文档"""
    weekly_group = {}
    yearly_group = {}
    black_list = ["Topic"]
    subject_name_map = {
        "Articles": "优秀博客",
        "Learnings": "本周学习",
        "Resources": "摸一下鱼",
        "Interviews": "面试选题"
    }

    sorted_category = ["面试选题", "摸一下鱼", "本周学习", "优秀博客"]
    sorted_group = []

    for index in range(from_index - 1, to_index):
        weekly_file = f"{weekly_folder}/iOSWeeklyLearning_{index + 1}.md"
        print(weekly_file)
        export_content = export_topic_content(weekly_file)

        weekly_group[index] = export_content

    for index, content in weekly_group.items():
        for category, content_lines in content.items():
            if category in black_list or not content_lines:
                continue

            category_name = subject_name_map[category]
            current_list = yearly_group.get(category_name, [])
            # 同一类别分组
            if len(current_list):
                current_list.append("***\n")
            current_list.extend(content_lines)
            yearly_group[category_name] = current_list

    for item in sorted_category:
        sorted_group.append({item: yearly_group[item]})

    write_to_file(category_folder, sorted_group, merged_file)


def export_topic_content(weekly_file):
    output = dict.fromkeys(category_map.keys(), [])
    if os.path.exists(weekly_file):
        with open(weekly_file) as file:
            lines_content = file.readlines()
            for category, topic_list in category_map.items():
                topic_content_list = []
                for topic in topic_list:
                    topic_content_list.extend(filter_data(lines_content, topic))
                output[category] = topic_content_list
        # print(output)
    return output


def filter_data(lines_data, category_name):
    begin = "## " + category_name
    print(f"category: {category_name}")
    output_lines = []
    is_start = False
    is_end = False
    for line_content in lines_data:
        # print(line_content)
        if begin in line_content:
            is_start = True
        elif line_content.count("#") == 2 and is_start:
            is_end = True
        elif is_end:
            # print("====")
            # print(output_lines)
            return output_lines
        elif is_start:
            output_lines.append(line_content)
            # print(line_content)
    return output_lines


def write_to_file(file_path, content_group, merged_file=None):
    """如果传入merged_file会将所有的category合并到一个文件"""
    for category in content_group:

        if merged_file:
            category_file = f"{file_path}/{merged_file}.md"
            category_name = list(category.keys())[0]
            category_content = category[category_name]
        else:
            category_name = category
            category_file = f"{file_path}/{category_name}.md"
            category_content = content_group[category_name]
        # if os.path.exists(sub_file):
        with open(category_file, "a", encoding='utf-8') as file:
            if merged_file:
                file.write(f"## {category_name}\n")
            else:
                file.write("***")
            for content_line in category_content:
                file.writelines(content_line)
    print("write success!")
