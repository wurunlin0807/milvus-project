import os
from dotenv import load_dotenv, find_dotenv


class MyTest:
    def __init__(self):
        load_dotenv(find_dotenv())
        pass

    @staticmethod
    def prompt():
        return ("""# 身份锚定
        你是专业检索词转化工程师，隶属于代码检索系统支撑团队，核心职责是将用户输入的通俗自然语言需求，转化为可直接被代码检索模块调用的标准化检索内容，确保后续检索结果精准匹配用户真实需求。

        # 操作执行流程
        ## 第一步：多维度检索词扩展
        输入：第一步输出的核心要素清单
        处理动作：
        将口语化表达修改为规范化表达。并生成多个近似的含义，以便从多维度进行检索。

        # 输出规范
        1. 结构框架：每一点按照/n换行隔开。最高不拓展三点
        """)

    @staticmethod
    def promptafter():
        return ("""# 你将扮演银行网点的柜台客户经理，你的核心职责是基于银行官方发布的服务知识库内容，专业、耐心、准确地解答用户提出的各类银行业务相关问题。
        """)

    @staticmethod
    def model_PROVIDERS():
        CURRENT_PROVIDER = "volcano"
        PROVIDERS = {
            "volcano": {
                "base_url": os.environ.get('DOUBAO_base_url'),
                # .env 文件中对应的环境变量名
                "api_key_env": os.environ.get('DOUBAO_ARK_API_KEY'),
                "model": "doubao-seed-2-0-mini-260428",    # 火山引擎的模型名/接入点ID
            },
            # "qwen": {
            #     "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            #     "api_key_env": "DASHSCOPE_API_KEY",        # .env 文件中对应的环境变量名
            #     "model": "qwen-plus",                      # 千问的模型名
            # },
        }
        return PROVIDERS, CURRENT_PROVIDER
