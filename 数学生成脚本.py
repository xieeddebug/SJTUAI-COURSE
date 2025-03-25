import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import uuid
from datetime import datetime

# 默认欢迎语
DEFAULT_WELCOME = '''欢迎体验～我是你的AI数学推理助手🔹
- 如何证明一个数列的收敛性并求其极限？
- 在解几何问题时，如何通过构造辅助线找到突破口？
- 如何用归纳法证明一个数学命题对所有自然数成立？
- 在概率问题中，如何正确运用条件概率公式？
- 如何通过反证法解决一个复杂的逻辑命题？
- 在微积分中，如何判断一个函数的可导性并求导？
- 如何用矩阵运算解决线性方程组的推理问题？
- 在数论中，如何推理一个数的素性并分解其因子？'''

def select_excel_file():
    """选择Excel文件"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(
        title="选择Excel文件",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    return file_path

def generate_sql_content(row, seq_num):
    """生成SQL内容"""
    sql_template = """INSERT INTO application (
    seq,
    app_id,
    maxkb_id,
    name,
    icon,
    api_type,
    base_api,
    redirect_link,
    token,
    category,
    `desc`,
    prologue,
    enabled
) VALUES (
    {seq},
    uuid(),
    NULL,
    '{name}',
    11,
    'dify/chatflow',
    'http://10.119.14.166/v1/',
    NULL,
    '{token}',
    'AI 课程/AI+课程/{name}/AI数学推理助手',
    '授课教师：{teacher}',
    '{prologue}',
    1
);"""

    # 获取课程名称和教师
    name = str(row['Q1. 课程名称']).strip()
    teacher = str(row['Q2. 课程负责人']).strip()
    
    # 使用默认欢迎语
    prologue = DEFAULT_WELCOME
    
    # 替换SQL模板中的变量
    sql_content = sql_template.format(
        seq=3000 + seq_num,
        name=name,
        teacher=teacher,
        token='app-EWokr4LKG0VczDlTVHAnKn6k',  # 使用新的token
        prologue=prologue.replace("'", "''")  # 转义单引号
    )
    
    return sql_content

def process_excel_to_sql():
    """处理Excel文件并生成SQL文件"""
    # 选择Excel文件
    excel_file = select_excel_file()
    if not excel_file:
        print("未选择文件，程序退出")
        return
        
    # 创建输出目录
    output_dir = "generated_sql_files"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_file)
        
        # 检查必要的列是否存在
        required_columns = [
            'Q1. 课程名称',
            'Q2. 课程负责人',
            'Q3. 学院/单位',
            'Q4. 1. 课程简介（AI 问答欢迎语设置）',
            'Q5. 2. 推荐问题（AI 问答预设可点击问题）',
            'Q6. 3. 已有课程外链资源（可选）'
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"错误：Excel文件缺少以下列：{', '.join(missing_columns)}")
            print(f"现有列：{', '.join(df.columns)}")
            return
            
        # 处理每一行数据
        for index, row in df.iterrows():
            try:
                # 检查课程名称和教师是否为空
                if pd.isna(row['Q1. 课程名称']) or pd.isna(row['Q2. 课程负责人']):
                    print(f"跳过第 {index + 1} 行：课程名称或教师为空")
                    continue
                    
                # 生成SQL内容
                sql_content = generate_sql_content(row, index + 1)
                
                # 生成文件名（使用课程名称和时间戳）
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{str(row['Q1. 课程名称']).strip()}_math_{timestamp}.sql"
                filepath = os.path.join(output_dir, filename)
                
                # 保存SQL文件
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(sql_content)
                    
                print(f"已生成SQL文件：{filename}")
                
            except Exception as e:
                print(f"处理第 {index + 1} 行时出错：{str(e)}")
                continue
                
        print(f"\n处理完成！SQL文件已保存到 {output_dir} 目录")
        
    except Exception as e:
        print(f"处理Excel文件时出错：{str(e)}")

if __name__ == "__main__":
    process_excel_to_sql() 