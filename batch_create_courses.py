import pandas as pd
import os
import re
import sys
import tkinter as tk
from tkinter import filedialog
from dify_automation import DifyAutomation
from excel_to_csv import select_file, excel_to_csv
from process_courses import extract_course_info, generate_course_content
import time

def batch_create_courses(csv_file=None):
    """
    批量创建课程
    """
    # Dify配置
    DIFY_BASE_URL = "your_dify_base_url"
    DIFY_TOKEN = "your_dify_token"
    try:
        # 创建SQL文件目录
        sql_dir = "dify_sql_files"
        if not os.path.exists(sql_dir):
            os.makedirs(sql_dir)
        
        # 如果没有提供CSV文件，提示选择Excel文件
        if not csv_file:
            excel_file = select_file()
            if not excel_file:
                print("未选择文件，程序退出")
                return
                
            if not excel_to_csv(excel_file):
                print("Excel转换失败，程序退出")
                return
                
            # 获取转换后的CSV文件名
            csv_file = os.path.splitext(os.path.basename(excel_file))[0] + ".csv"
        
        # 检查CSV文件是否存在
        if not os.path.exists(csv_file):
            print(f"错误：找不到 {csv_file} 文件")
            return
            
        # 读取CSV文件
        df = pd.read_csv(csv_file, engine='python', on_bad_lines='skip')
        
        # 显示CSV文件的列名
        print("\n=== CSV文件结构 ===")
        print("列名:", df.columns.tolist())
        print("="*50 + "\n")
        
        # 定义所需列名
        required_columns = {
            'course_name': 'Q1. 课程名称',
            'teacher': 'Q2. 课程负责人',
            'intro': 'Q4. 1. 课程简介（AI 问答欢迎语设置）',
            'questions': 'Q5. 2. 推荐问题（AI 问答预设可点击问题）',
            'redirect_url': 'Q6. 3. 已有课程外链资源（可选）'
        }
        
        # 检查所需列是否都存在
        for col_type, col_name in required_columns.items():
            if col_name not in df.columns:
                print(f"错误：找不到{col_type}列：{col_name}")
                print("可用的列名:", df.columns.tolist())
                return
        
        # 创建Dify实例
        dify = DifyAutomation(DIFY_BASE_URL, DIFY_TOKEN)
        
        # 用于存储已处理的课程名称
        processed_courses = set()
        
        # 创建结果记录文件
        results_file = 'creation_results.txt'
        with open(results_file, 'w', encoding='utf-8') as log_file:
            # 遍历每个课程
            for index, row in df.iterrows():
                course_name = ""
                teacher = ""
                try:
                    # 获取课程信息
                    course_name = str(row[required_columns['course_name']]).strip()
                    teacher = str(row[required_columns['teacher']]).strip()
                    intro = str(row[required_columns['intro']]).strip()
                    questions = str(row[required_columns['questions']]).strip()
                    redirect_url = str(row[required_columns['redirect_url']]).strip()
                    
                    # 提取纯网址（如果包含http或https）
                    if redirect_url:
                        url_match = re.search(r'https?://[^\s]+', redirect_url)
                        redirect_url = url_match.group(0) if url_match else None
                    
                    if not course_name or not teacher:
                        print(f"警告：课程名称或负责人为空，跳过该行")
                        continue
                    
                    # 检查课程是否已处理
                    if course_name in processed_courses:
                        print(f"跳过重复课程：{course_name}")
                        continue
                    
                    print(f"\n{'='*50}")
                    print(f"正在处理第 {len(processed_courses)+1} 个课程：{course_name}")
                    print(f"授课教师：{teacher}")
                    
                    # 应用信息
                    app_name = course_name  # 移除"AI 学伴"后缀
                    app_description = f"{course_name}课程的 AI 助教，授课教师：{teacher}"
                    
                    # 使用提供的简介和问题
                    opening_statement = intro if intro else f"欢迎来到《{course_name}》课程～我是你的 AI 助教，由{teacher}老师设计"
                    prompt_template = questions if questions else "\n".join([
                        f"1. 您想了解{course_name}课程的哪些具体内容？",
                        "2. 您在学习过程中遇到了什么困难？",
                        "3. 需要我为您解释某个概念吗？",
                        "4. 您希望深入了解课程中的哪个部分？",
                        "5. 有什么实践问题需要讨论吗？"
                    ])
                    
                    # 创建应用
                    app_id = dify.create_application(app_name, app_description)
                    if not app_id:
                        print(f"创建应用失败：{course_name}")
                        continue
                    
                    # 创建 API Key
                    api_key = dify.create_api_key(app_id)
                    if not api_key:
                        print(f"创建API Key失败：{course_name}")
                        continue
                    
                    # 更新提示词和开场白
                    if not dify.update_prompt_template(app_id, prompt_template, opening_statement):
                        print(f"更新提示词失败：{course_name}")
                        continue
                    
                    # 发布应用
                    if not dify.publish_application(app_id):
                        print(f"发布应用失败：{course_name}")
                        continue
                    
                    # 准备 SQL 数据
                    app_data = {
                        'seq': 3000 + len(processed_courses),
                        'app_id': app_id,
                        'maxkb_id': None,
                        'name': app_name,
                        'icon': 11,
                        'api_type': 'dify/chatflow',
                        'base_api': DIFY_BASE_URL + '/v1/',
                        'redirect_link': redirect_url,
                        'token': api_key,
                        'category': f'AI 课程/AI+课程/{course_name}/AI学伴',
                        'desc': '授课教师：' + teacher,
                        'prologue': opening_statement,
                        'enabled': 1
                    }
                    
                    # 生成SQL并保存到单独的文件
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    sql_filename = f"dify_insert_{timestamp}.sql"
                    sql_filepath = os.path.join(sql_dir, f"{course_name}")
                    
                    with open(sql_filepath, 'w', encoding='utf-8') as sql_file:
                        sql = dify.generate_sql(app_data)
                        sql_file.write(sql)
                    
                    # 同时写入汇总文件
                    log_file.write(f"\n-- {course_name} ({teacher})\n")
                    log_file.write(sql)
                    log_file.write("\n")
                    
                    print(f"成功创建课程：{course_name}")
                    print(f"App ID: {app_id}")
                    print(f"API Key: {api_key}")
                    print(f"SQL文件已保存到：{sql_filepath}")
                    
                    # 将课程添加到已处理集合
                    processed_courses.add(course_name)
                    
                    # 等待一段时间再处理下一个课程
                    if len(processed_courses) < len(df):
                        print("等待5秒后处理下一个课程...")
                        time.sleep(5)
                    
                except Exception as e:
                    error_msg = f"处理课程时出错"
                    if course_name:
                        error_msg += f" [{course_name}]"
                    error_msg += f": {str(e)}"
                    print(error_msg)
                    continue
            
        print("\n所有课程处理完成！")
        print(f"共处理了 {len(processed_courses)} 门不同的课程")
        print(f"详细结果已保存到 {results_file}")
        print(f"SQL文件已保存到 {sql_dir} 目录")
            
    except Exception as e:
        print(f"批量处理过程中出错: {str(e)}")

if __name__ == "__main__":
    # 如果有命令行参数，使用指定的CSV文件
    if len(sys.argv) > 1:
        batch_create_courses(sys.argv[1])
    else:
        # 否则启动GUI选择Excel文件
        batch_create_courses() 
