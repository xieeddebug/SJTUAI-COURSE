import pandas as pd
from openai import OpenAI
import re


def read_course_info(csv_path):
    df = pd.read_csv(csv_path)
    course_names = df['Q1. 课程名称']
    course_intros = df['Q4. 1. 课程简介（AI 问答欢迎语设置）']
    course_problems = df['Q5. 2. 推荐问题（AI 问答预设可点击问题）']
    return course_names, course_intros, course_problems


def get_deepseek_response(course_name, course_intro, course_problem):
    client = OpenAI(api_key="sk-fb180ec725f4452eac937651e7f71940", base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"你是{course_name}课程的 AI 助教，这门课的简介是：{course_intro}"},
            {"role": "user", "content": f"""以下是一些你可能会在学习电路理论过程中遇到的有趣问题：
             为什么一个简单的电阻、电容和电感可以组合出如此复杂的电路行为？
             什么是"瞬态响应"和"稳态响应"，它们如何决定电路的工作特性？
             正弦稳态分析中的"相量法"是如何简化复杂微分方程的？
             为什么三相电路能够高效地传输电力，它是如何实现平衡的？
             非线性电阻电路的行为为何难以预测，我们该如何分析它？
             动态电路中的"状态变量"是什么意思，它如何帮助我们描述系统的演化？
             复频域分析（拉普拉斯变换）为什么能让时域中的难题变得清晰易解？
             如何通过电路定理（如叠加定理、戴维南定理）快速解决实际工程问题？
             为什么非正弦周期电流会产生谐波，它对电路有什么影响？
             电路实验中的测量误差从何而来，如何通过理论分析改进实验结果？。
             请你仿照以上问题，为{course_name}设计问题。
             这里有我已经设计好的一些问题：{course_problem}。
             注意：如果我有已经设计好的问题，请你把已设计好的问题排在前面，总共8个问题即可。
             你不得输出其它任何内容，只需要输出问题即可，输出格式一定是- 问题内容，即便原来的问题是用序号罗列的，你也要替换成这个格式。"""}
        ],
        stream=False
    )
    return response.choices[0].message.content


def handle_sql(course_name, response):
    # 读取 SQL 文件内容
    with open(f'.\\dify_sql_files\\{course_name}.sql', 'r', encoding='utf-8') as file:
        sql_content = file.read()

    # 使用正则表达式提取 prologue 值
    prologue_pattern = re.compile(r"prologue,\s+enabled\s+\)\s+VALUES\s+\(\s+.+?,\s+.+?,\s+.+?,\s+.+?,\s+.+?,\s+.+?,\s+.+?,\s+.+?,\s+.+?,\s+.+?,\s+.+?,\s+'(.*?)',\s+\d+\s+\);", re.DOTALL)
    match = prologue_pattern.search(sql_content)

    if match:
        prologue_value = match.group(1)

        # 在这里对 prologue 值进行操作
        modified_prologue_value = f"""欢迎来到上海交通大学《{course_name}》课程～我是你的 AI 助教🔹
        以下是一些你可能会在学习过程中遇到的问题：
        {response}"""

        # 替换原始 prologue 值
        new_sql_content = prologue_pattern.sub(
            lambda m: m.group(0).replace(prologue_value, modified_prologue_value),
            sql_content
        )

        # 将修改后的内容写回 SQL 文件
        with open(f'.\\sql_files\\{course_name}.sql', 'w', encoding='utf-8') as file:
            file.write(new_sql_content)

        print(f"修改后的SQL文件已保存为 .\\sql_files\\{course_name}.sql")
    else:
        print("No prologue value found.")
        

def main():
    csv_path = "AI+课程主页建设素材收集_答卷数据_2025_03_14_15_16_21.csv"
    course_names, course_intros, course_problems = read_course_info(csv_path)
    for course_name, course_intro, course_problem in zip(course_names, course_intros, course_problems):
        response = get_deepseek_response(course_name, course_intro, course_problem)
        handle_sql(course_name, response)

if __name__ == "__main__":
    main()
