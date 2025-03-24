import pandas as pd
import os
import re

def extract_course_info(location):
    """
    从位置字段提取课程名称和授课教师
    例如：
    - 从 "数据挖掘 向立强" 提取 ("数据挖掘", "向立强")
    - 从 "水池模型实验{田新亮 船海}" 提取 ("水池模型实验", "田新亮")
    """
    # 提取花括号中的内容
    teacher = ""
    bracket_match = re.search(r'\{(.*?)\}', location)
    if bracket_match:
        # 如果有花括号，从花括号中提取第一个名字
        teacher = bracket_match.group(1).split()[0]
        # 移除花括号及其内容
        location = re.sub(r'\{.*?\}', '', location)
    else:
        # 如果没有花括号，提取空格后的第一个名字
        parts = location.split()
        if len(parts) > 1:
            teacher = parts[1]
    
    # 提取课程名称（第一个空格前的内容）
    course_name = location.split()[0] if location else ''
    
    return course_name, teacher

def generate_course_content(course_name, teacher):
    """
    根据课程名称和教师生成开场白和提示词
    """
    opening = f"欢迎来到{course_name}课程！我是您的AI助教，由{teacher}老师设计。我会协助您更好地学习本课程内容。"
    
    prompts = [
        f"1. 您想了解{course_name}课程的哪些具体内容？",
        "2. 您在学习过程中遇到了什么困难？",
        "3. 需要我为您解释某个概念吗？",
        "4. 您希望深入了解课程中的哪个部分？",
        "5. 有什么实践问题需要讨论吗？"
    ]
    
    return opening, "\n".join(prompts)

def process_csv_and_generate_sql():
    """
    处理CSV文件并生成SQL更新语句
    """
    try:
        csv_file = "survey_data.csv"
        if not os.path.exists(csv_file):
            print(f"错误：找不到 {csv_file} 文件")
            return
            
        # 读取CSV文件，处理引号内的逗号
        df = pd.read_csv(csv_file, engine='python', on_bad_lines='skip')
        
        # 创建SQL文件
        sql_filename = "course_updates.sql"
        with open(sql_filename, 'w', encoding='utf-8') as sql_file:
            # 遍历每个课程
            for _, row in df.iterrows():
                try:
                    location = str(row['位置'])
                    course, teacher = extract_course_info(location)
                    
                    if not course or not teacher:  # 如果没有提取到课程名称或教师，跳过该行
                        print(f"警告：无法从位置 '{location}' 提取完整信息")
                        continue
                        
                    course = course.replace("'", "''")  # 处理单引号
                    teacher = teacher.replace("'", "''")  # 处理单引号
                    
                    # 生成开场白和提示词
                    opening, prompts = generate_course_content(course, teacher)
                    opening = opening.replace("'", "''")  # 处理单引号
                    prompts = prompts.replace("'", "''")  # 处理单引号
                    
                    # 生成SQL更新语句
                    sql = f"""
-- {course} 课程更新
UPDATE courses 
SET 
    teacher = '{teacher}',
    course_name = '{course}',
    opening_statement = '{opening}',
    prompt_template = '{prompts}'
WHERE course_name = '{course}';

"""
                    sql_file.write(sql)
                    print(f"处理课程：{course} (授课教师：{teacher})")
                    
                except Exception as row_error:
                    print(f"处理行数据时出错: {str(row_error)}")
                    continue
            
        print(f"\n已生成SQL文件：{sql_filename}")
        print(f"共处理了 {len(df)} 门课程")
            
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")

if __name__ == "__main__":
    process_csv_and_generate_sql() 