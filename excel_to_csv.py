import pandas as pd
import os
import sys
import tkinter as tk
from tkinter import filedialog

def select_file():
    """
    打开文件选择对话框
    :return: 选择的文件路径
    """
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(
        title="选择Excel文件",
        filetypes=[
            ("Excel文件", "*.xlsx;*.xls"),
            ("所有文件", "*.*")
        ]
    )
    return file_path

def excel_to_csv(excel_file):
    """
    将Excel文件转换为CSV格式，保存在当前目录
    :param excel_file: Excel文件路径
    """
    try:
        if not excel_file:  # 如果没有选择文件，直接返回
            return False
            
        # 读取Excel文件中的所有工作表
        excel = pd.ExcelFile(excel_file)
        sheet_names = excel.sheet_names
        
        # 获取文件名（不包含扩展名）
        base_name = os.path.splitext(os.path.basename(excel_file))[0]
        
        # 转换每个工作表
        for sheet_name in sheet_names:
            # 读取工作表
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            # 构建输出文件名（保存在当前目录）
            if len(sheet_names) == 1:
                output_file = f"{base_name}.csv"
            else:
                output_file = f"{base_name}_{sheet_name}.csv"
            
            # 保存为CSV，确保正确处理中文
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"已将工作表 '{sheet_name}' 转换为: {output_file}")
            
        return True
    except Exception as e:
        print(f"转换过程中出错: {str(e)}")
        return False

def main():
    # 如果有命令行参数，使用命令行模式
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    else:
        # 使用图形界面模式
        excel_file = select_file()
        if not excel_file:
            return
    
    # 检查文件是否存在
    if not os.path.exists(excel_file):
        print(f"错误: 文件 '{excel_file}' 不存在")
        return
    
    # 执行转换
    if excel_to_csv(excel_file):
        print("转换完成！")
    else:
        print("转换失败！")

if __name__ == "__main__":
    main() 