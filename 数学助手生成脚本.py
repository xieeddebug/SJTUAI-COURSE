import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import uuid
from datetime import datetime
import logging
import json
from pathlib import Path
import sys

# 检查Python版本
if sys.version_info < (3, 6):
    print("错误：需要Python 3.6或更高版本")
    sys.exit(1)

# 检查必要的依赖包
required_packages = ['pandas', 'tkinter']
try:
    for package in required_packages:
        __import__(package)
except ImportError as e:
    print(f"错误：缺少必要的依赖包 {e.name}")
    print("请运行：pip install -r requirements.txt")
    sys.exit(1)

# 配置日志
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"math_assistant_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 加载配置
def load_config():
    try:
        config_path = Path('config.json')
        if not config_path.exists():
            # 默认配置
            config = {
                "token": "app-EWokr4LKG0VczDlTVHAnKn6k",
                "output_dir": "generated_sql_files",
                "base_seq": 3000,
                "max_name_length": 50,
                "max_teacher_length": 20,
                "base_api": "http://10.119.14.166/v1/"
            }
            # 保存默认配置
            config_path.write_text(json.dumps(config, indent=4, ensure_ascii=False), encoding='utf-8')
            logging.info("已创建默认配置文件：config.json")
        else:
            with config_path.open('r', encoding='utf-8') as f:
                config = json.load(f)
                logging.info("已加载配置文件")
        return config
    except Exception as e:
        logging.error(f"加载配置文件失败：{str(e)}")
        sys.exit(1)

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
        token='app-wj2aSQ2rXSz5NjCMzceqXd40',  # 使用新的token
        prologue=prologue.replace("'", "''")  # 转义单引号
    )
    
    return sql_content

def process_excel_to_sql():
    """处理Excel文件并生成SQL文件"""
    try:
        # 获取脚本所在目录
        script_dir = Path(__file__).parent.absolute()
        os.chdir(script_dir)  # 切换到脚本所在目录
        logging.info(f"工作目录：{script_dir}")

        config = load_config()
        excel_file = select_excel_file()
        if not excel_file:
            logging.warning("未选择文件，程序退出")
            return
            
        output_dir = Path(config['output_dir'])
        output_dir.mkdir(exist_ok=True)
        
        # 验证Excel文件是否存在
        if not Path(excel_file).exists():
            logging.error(f"Excel文件不存在：{excel_file}")
            return

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