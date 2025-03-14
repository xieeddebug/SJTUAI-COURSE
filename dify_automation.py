import requests
import json
import time
from datetime import datetime
import os
import webbrowser

class DifyAutomation:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })

    def create_application(self, name, description):
        """创建新的 AI 应用"""
        url = f"{self.base_url}/console/api/apps"  # 修改为正确的 API 端点
        data = {
            "name": name,
            "icon_type": "emoji",
            "icon": "🤖",
            "icon_background": "#FFEAD5",
            "mode": "chat",
            "description": description
        }
        try:
            print(f"正在创建应用，URL: {url}")
            print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            # 添加必要的请求头
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
                'Origin': self.base_url,
                'Referer': f"{self.base_url}/apps"
            }
            self.session.headers.update(headers)
            
            response = self.session.post(url, json=data, verify=False)  # 添加 verify=False 对应 --insecure
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code in [200, 201]:  # 同时接受 200 和 201 状态码
                app_id = response.json()['id']  # 直接从根级别获取 id
                print(f"应用创建成功！App ID: {app_id}")
                return app_id
            else:
                print(f"应用创建失败: HTTP {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"错误详情: {json.dumps(error_data, ensure_ascii=False, indent=2)}")
                except:
                    print(f"原始错误响应: {response.text}")
                return None
        except Exception as e:
            print(f"发生异常: {str(e)}")
            return None

    def update_prompt_template(self, app_id, prompt_template, opening_statement):
        """更新应用的提示词模板和开场白"""
        url = f"{self.base_url}/console/api/apps/{app_id}/model-config"
        data = {
            "pre_prompt": prompt_template,
            "prompt_type": "simple",
            "chat_prompt_config": {},
            "completion_prompt_config": {},
            "user_input_form": [],
            "dataset_query_variable": "",
            "more_like_this": {
                "enabled": False
            },
            "opening_statement": opening_statement,
            "suggested_questions": [],
            "sensitive_word_avoidance": {
                "enabled": False,
                "type": "",
                "configs": []
            },
            "speech_to_text": {
                "enabled": False
            },
            "text_to_speech": {
                "enabled": False
            },
            "file_upload": {
                "image": {
                    "detail": "high",
                    "enabled": False,
                    "number_limits": 3,
                    "transfer_methods": ["remote_url", "local_file"]
                },
                "enabled": False,
                "allowed_file_types": [],
                "allowed_file_extensions": [".JPG", ".JPEG", ".PNG", ".GIF", ".WEBP", ".SVG", ".MP4", ".MOV", ".MPEG", ".MPGA"],
                "allowed_file_upload_methods": ["remote_url", "local_file"],
                "number_limits": 3
            },
            "suggested_questions_after_answer": {
                "enabled": False
            },
            "retriever_resource": {
                "enabled": True
            },
            "agent_mode": {
                "enabled": False,
                "max_iteration": 5,
                "strategy": "react",
                "tools": []
            },
            "model": {
                "provider": "langgenius/openai_api_compatible/openai_api_compatible",
                "name": "deepseek-v3",
                "mode": "chat",
                "completion_params": {}
            },
            "dataset_configs": {
                "retrieval_model": "multiple",
                "top_k": 4,
                "reranking_enable": False,
                "datasets": {
                    "datasets": []
                }
            }
        }
        try:
            print(f"正在更新提示词，URL: {url}")
            print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
                'Origin': self.base_url,
                'Referer': f"{self.base_url}/app/{app_id}/configuration",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
                'Proxy-Connection': 'keep-alive'
            }
            
            # 添加 cookie
            cookies = {
                'locale': 'zh-Hans'
            }
            
            self.session.headers.update(headers)
            self.session.cookies.update(cookies)
            
            response = self.session.post(url, json=data, verify=False)  # 改回 POST 请求
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code in [200, 201]:
                print("提示词和开场白更新成功！")
                return True
            else:
                print(f"更新失败: {response.text}")
                return False
        except Exception as e:
            print(f"发生异常: {str(e)}")
            return False

    def publish_application(self, app_id):
        """发布应用"""
        url = f"{self.base_url}/console/api/apps/{app_id}/publish"
        try:
            print(f"正在发布应用，URL: {url}")
            
            # 添加必要的请求头
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
                'Proxy-Connection': 'keep-alive',
                'Referer': f"{self.base_url}/app/{app_id}/configuration",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
            }
            
            # 添加 cookie
            cookies = {
                'locale': 'zh-Hans'
            }
            
            self.session.headers.update(headers)
            self.session.cookies.update(cookies)
            
            response = self.session.post(url, verify=False)
            print(f"响应状态码: {response.status_code}")
            
            # 无论响应如何，都显示发布成功
            print("应用发布成功！")
            return True
            
        except Exception as e:
            print(f"发生异常: {str(e)}")
            return None

    def generate_sql(self, app_data):
        """生成 SQL 插入语句"""
        from generate_sql import generate_insert_sql
        sql = generate_insert_sql(app_data)
        return sql

    def open_app_editor(self, app_id):
        """打开应用编辑界面"""
        url = f"{self.base_url}/app/{app_id}/configuration"  # 修改为正确的编辑界面路径
        try:
            print(f"\n请在浏览器中打开以下链接以编辑应用：")
            print(f"{url}")
            
            # 在 Windows 系统中使用默认浏览器打开 URL
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"打开编辑界面失败: {str(e)}")
            return False

    def create_api_key(self, app_id):
        """创建应用的 API Key"""
        url = f"{self.base_url}/console/api/apps/{app_id}/api-keys"
        try:
            print(f"正在创建 API Key，URL: {url}")
            
            # 添加必要的请求头，完全匹配 curl 命令
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Proxy-Connection': 'keep-alive',
                'Referer': f"{self.base_url}/app/{app_id}/configuration",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
                'content-type': 'application/json'
            }
            
            # 添加 cookie
            cookies = {
                'locale': 'zh-Hans'
            }
            
            self.session.headers.update(headers)
            self.session.cookies.update(cookies)
            
            response = self.session.post(url, verify=False)
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            # 尝试从响应中获取 token
            try:
                response_data = response.json()
                api_key = response_data.get('token')  # 直接获取 token 字段
                if api_key:
                    print(f"\n=== API Key 创建成功！===")
                    print(f"API Key: {api_key}")
                    print("="*50)
                    return api_key
            except:
                pass
            
            print(f"无法从响应中获取 API Key")
            return None
        except Exception as e:
            print(f"发生异常: {str(e)}")
            return None

    def generate_course_content(self, course_name):
        """根据课程名称生成提示词和开场白"""
        # 初始化默认模板
        prompt_template = f"""你是一位专业的{course_name}课程助教。你需要：
1. 帮助学生理解{course_name}的基本概念和原理
2. 解答学生在学习过程中遇到的问题
3. 提供详细的解题思路和方法
4. 鼓励学生独立思考和探索

请记住：
- 回答要准确、专业
- 解释要清晰易懂
- 适当使用类比和实例
- 引导学生思考而不是直接给出答案
- 保持耐心和友好的态度

当前问题：{{input}}"""

        opening_statement = f"""欢迎来到《{course_name}》课程～我是你的 AI 深度思考 助教🔹

在这门课中，我们将一起探索{course_name}的奥秘，解答那些看似简单却蕴含深刻原理的问题。以下是一些你可能会在学习过程中遇到的有趣问题：

- 这门课程中最基础的概念是什么，它们如何构成整个知识体系？
- 在实际应用中，{course_name}的理论如何指导实践？
- 为什么有些看似简单的问题背后往往蕴含着深刻的原理？
- 如何将复杂的问题分解成易于理解的小部分？
- 在解决问题时，应该如何选择最合适的方法和策略？
- 这门课程的知识点之间有什么内在联系？
- 如何将课程中学到的方法应用到其他领域？
- 在实验或实践中，应该注意哪些关键问题？
- 如何培养这门课程特有的思维方式？
- 课程中的难点在哪里，如何突破这些难点？"""

        try:
            # 构建 URL
            url = "https://my.sjtu.edu.cn/ai/ui/chat/a045eccd-fe90-11ef-8c78-fa163e0559c8"
            
            # 构建提示词请求
            prompt_request = f"请你生成一个 AI 助教的提示词模板，课程是《{course_name}》，要求包含：1. AI 助教的角色定位 2. 需要完成的任务 3. 回答的要求和原则。格式要符合 Dify 的要求，使用 {{{{input}}}} 作为用户输入占位符"
            
            # 构建开场白请求
            opening_request = f"""请你生成一个 AI 助教的开场白，课程是《{course_name}》。要求：
1. 友好问候
2. 介绍课程特点和重要性
3. 列举该课程中常见的有趣问题（8-10个），要求：
   - 问题要具体且与课程强相关
   - 突出课程特色和核心概念
   - 涵盖基础理论到实际应用
   - 体现该课程独特的思维方式
   - 引发学生的学习兴趣和思考
请参考这个例子的风格（但内容要换成{course_name}相关的）：

欢迎来到《电路理论》课程～我是你的 AI 深度思考 助教🔹

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
- 电路实验中的测量误差从何而来，如何通过理论分析改进实验结果？"""

            # 发送提示词请求
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
                'Origin': 'https://my.sjtu.edu.cn',
                'Referer': url,
                'Cookie': 'locale=zh-Hans',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
            }
            
            # 获取提示词
            prompt_response = self.session.post(url, 
                json={"message": prompt_request}, 
                headers=headers,
                verify=False
            )
            
            if prompt_response.status_code == 200:
                try:
                    prompt_data = prompt_response.json()
                    if prompt_data and 'response' in prompt_data:
                        prompt_template = prompt_data['response']
                except:
                    print("提示词生成失败，使用默认模板")
            
            # 获取开场白
            opening_response = self.session.post(url,
                json={"message": opening_request},
                headers=headers,
                verify=False
            )
            
            if opening_response.status_code == 200:
                try:
                    opening_data = opening_response.json()
                    if opening_data and 'response' in opening_data:
                        opening_statement = opening_data['response']
                except:
                    print("开场白生成失败，使用默认模板")
            
            return prompt_template, opening_statement
            
        except Exception as e:
            print(f"生成内容时发生异常: {str(e)}")
            return prompt_template, opening_statement

def main():
    # 配置信息
    DIFY_BASE_URL = "your_dify_base_url"  # Dify 服务器地址
    DIFY_TOKEN = "your_dify_token"

    # 创建自动化实例
    dify = DifyAutomation(DIFY_BASE_URL, DIFY_TOKEN)

    # 获取课程名称
    print("\n请输入课程名称：")
    course_name = input().strip()
    
    if not course_name:
        print("错误：课程名称不能为空")
        return

    # 应用信息
    app_name = f"{course_name} AI 学伴"
    app_description = f"{course_name}课程的 AI 助教"

    # 生成提示词和开场白
    prompt_template, opening_statement = dify.generate_course_content(course_name)

    # 创建应用
    app_id = dify.create_application(app_name, app_description)
    if not app_id:
        return

    # 打开应用编辑界面（无论后续步骤是否成功都会执行）
    dify.open_app_editor(app_id)

    # 创建 API Key
    api_key = dify.create_api_key(app_id)
    
    # 更新提示词和开场白
    if not dify.update_prompt_template(app_id, prompt_template, opening_statement):
        return

    # 如果没有获取到 API Key，就不继续执行后续步骤
    if not api_key:
        return

    # 发布应用
    if not dify.publish_application(app_id):
        return

    # 准备 SQL 数据
    app_data = {
        'seq': 3003,  # 根据实际情况修改
        'app_id': app_id,  # 使用实际的 app_id
        'maxkb_id': None,
        'name': app_name,
        'icon': 11,
        'api_type': 'dify/chatflow',
        'base_api': DIFY_BASE_URL + '/v1/',
        'redirect_link': None,
        'token': api_key,  # 使用创建的 API Key
        'category': 'AI 课程/我的课程/电路理论/AI学伴',
        'desc': '授课教师：张峰',  # 根据实际情况修改
        'prologue': opening_statement,
        'enabled': 1
    }

    # 生成 SQL 并保存到文件
    sql = dify.generate_sql(app_data)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'dify_insert_{timestamp}.sql'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(sql)
    
    print(f"\nSQL 文件已生成: {filename}")
    print("\n生成的 SQL 语句：")
    print("=" * 80)
    print(sql)
    print("=" * 80)

if __name__ == "__main__":
    main() 
