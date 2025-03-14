# AI 课程批量创建工具

## 项目简介

这是一个用于批量创建 AI 课程助教的自动化工具。该工具可以通过 Excel 表格批量创建 Dify 应用，生成相应的 SQL 脚本，并自动配置课程助教的问答模板。

主要功能：
- Excel 数据自动导入
- Dify 应用自动创建
- API Key 自动生成
- SQL 脚本自动生成
- 课程助教提示词和开场白自动配置

## 环境依赖

```bash
pip install -r requirements.txt
```

## 使用说明

### 1. 准备数据
1. 创建 Excel 文件，包含以下必需列：
   - Q1. 课程名称
   - Q2. 课程负责人
   - Q4. 1. 课程简介（AI 问答欢迎语设置）
   - Q5. 2. 推荐问题（AI 问答预设可点击问题）
   - Q6. 3. 已有课程外链资源（可选）

### 2. 配置环境
1. 确保已安装所有依赖库
2. 检查并配置 Dify 相关参数：
   - DIFY_BASE_URL
   - DIFY_TOKEN

### 3. 运行程序

#### 方式一：图形界面选择文件
```bash
python batch_create_courses.py
```

#### 方式二：命令行指定 CSV 文件
```bash
python batch_create_courses.py path/to/your/file.csv
```

### 4. 输出文件
程序运行后将生成：
- 课程的 SQL 插入脚本（在 dify_sql_files 目录下）
- 创建结果日志（creation_results.txt）

## 注意事项
1. 确保 Excel 文件格式正确，列名完全匹配
2. 需要有效的 Dify API Token
3. 建议批量处理前先用单个课程测试
4. SQL 文件请谨慎使用，建议先审查后再执行
