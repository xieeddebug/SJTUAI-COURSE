import uuid

def generate_insert_sql(data):
    """
    生成 SQL INSERT 语句
    :param data: 包含所有字段值的字典
    :return: 格式化的 SQL INSERT 语句
    """
    fields = [
        'seq',
        'app_id',
        'maxkb_id',
        'name',
        'icon',
        'api_type',
        'base_api',
        'redirect_link',
        'token',
        'category',
        '`desc`',
        'prologue',
        'enabled',
        'visible',
        'main_app'
    ]
    
    # 构建 INSERT 语句的字段部分
    fields_str = ',\n    '.join(fields)
    
    # 获取值
    values = []
    for field in fields:
        val = data.get(field.strip('`'))  # 移除字段名的反引号以获取正确的值
        if val is None:
            if field in ['visible', 'main_app']:
                values.append('1')  # 为visible和main_app设置默认值1
            else:
                values.append('NULL')
        elif field == 'app_id':
            values.append(f"uuid()")
        elif isinstance(val, (int, float)):
            values.append(str(val))
        else:
            # 对字符串进行转义和引号处理
            val = str(val).replace("'", "''")
            values.append(f"'{val}'")
    
    # 构建 VALUES 部分
    values_str = ',\n    '.join(values)
    
    # 组装完整的 SQL 语句
    sql = f"""INSERT INTO application (
    {fields_str}
) VALUES (
    {values_str}
);"""
    
    return sql

# 示例数据
sample_data = {
    'seq': 3003,
    'app_id': None,  # 将使用 uuid() 函数
    'maxkb_id': None,
    'name': '电路理论',
    'icon': 11,
    'api_type': 'dify/chatflow',
    'base_api': 'http://10.119.14.166/v1/',
    'redirect_link': None,
    'token': 'app-0Dpb8f5NbsfvQAUbWWborU8a',
    'category': 'AI 课程/我的课程/电路理论/AI学伴',
    'desc': '授课教师：张峰',
    'prologue': '''欢迎来到《电路理论》课程～我是你的 AI 深度思考 助教🔹

在这门课中，我们将一起探索电路世界的奥秘，解答那些看似简单却蕴含深刻原理的问题。以下是一些你可能会在学习过程中遇到的有趣问题：

- 为什么一个简单的电阻、电容和电感可以组合出如此复杂的电路行为？
- 什么是"瞬态响应"和"稳态响应"，它们如何决定电路的工作特性？
- 正弦稳态分析中的"相量法"是如何简化复杂微分方程的？
- 为什么三相电路能够高效地传输电力，它是如何实现平衡的？
- 非线性电阻电路的行为为何难以预测，我们该如何分析它？
- 动态电路中的"状态变量"是什么意思，它如何帮助我们描述系统的演化？
- 复频域分析（拉普拉斯变换）为什么能让时域中的难题变得清晰易解？
- 如何通过电路定理（如叠加定理、戴维南定理）快速解决实际工程问题？
- 为什么非正弦周期电流会产生谐波，它对电路有什么影响？
- 电路实验中的测量误差从何而来，如何通过理论分析改进实验结果？''',
    'enabled': 1
}

# 生成并打印 SQL
if __name__ == '__main__':
    sql = generate_insert_sql(sample_data)
    print(sql) 